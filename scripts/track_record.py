"""Track-record commit + README generator for /opt/kalshi-track-record/.

Called by signals.py after each compute_signals() run.
- Appends new signals to /opt/kalshi-track-record/signals/YYYY-MM-DD.jsonl
- Regenerates README.md with running totals
- Creates a signed git commit (SSH-signed via root's git_signing_key)
- Optionally pushes to remote if configured
"""
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

TRACK_DIR = Path("/opt/kalshi-track-record")
SIGNALS_DIR = TRACK_DIR / "signals"
OUTCOMES_DIR = TRACK_DIR / "outcomes"
README = TRACK_DIR / "README.md"


def _run(cmd: list, check: bool = True, cwd: Path = TRACK_DIR) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=check, cwd=cwd)


def append_signals(new_signals: list) -> int:
    """Append signals to today's JSONL file. Returns count of new lines written."""
    if not new_signals:
        return 0
    SIGNALS_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    daily_file = SIGNALS_DIR / f"{today}.jsonl"
    with daily_file.open("a") as f:
        for sig in new_signals:
            f.write(json.dumps(sig) + "\n")
    return len(new_signals)


def _load_all_signals() -> list:
    """Read all daily signals files into a list (oldest first)."""
    if not SIGNALS_DIR.exists():
        return []
    out = []
    for path in sorted(SIGNALS_DIR.glob("*.jsonl")):
        with path.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return out


def _load_outcomes() -> dict:
    """Load all settled outcomes keyed by signal_id."""
    if not OUTCOMES_DIR.exists():
        return {}
    by_signal = {}
    for path in OUTCOMES_DIR.glob("*.json"):
        try:
            with path.open() as f:
                race = json.load(f)
            for s in race.get("signals", []):
                sid = s.get("signal_id")
                if sid:
                    by_signal[sid] = s
        except (json.JSONDecodeError, KeyError):
            continue
    return by_signal


def compute_metrics(signals: list, outcomes: dict) -> dict:
    """Hit rate, ROI, Brier score across settled signals only."""
    settled = []
    for s in signals:
        sid = s.get("signal_id")
        o = outcomes.get(sid)
        if o and o.get("settled") is True:
            settled.append({**s, **o})

    total_signals = len(signals)
    n_settled = len(settled)
    if n_settled == 0:
        return {
            "total_signals": total_signals,
            "settled": 0,
            "pending": total_signals,
            "wins": 0,
            "losses": 0,
            "pushes": 0,
            "hit_rate_pct": None,
            "roi_pct": None,
            "brier": None,
            "total_staked_usd": 0,
            "total_pnl_usd": 0,
        }

    wins = sum(1 for s in settled if s.get("outcome") == "won")
    losses = sum(1 for s in settled if s.get("outcome") == "lost")
    pushes = sum(1 for s in settled if s.get("outcome") == "push")
    total_staked = sum(float(s.get("recommended_stake_usd", 5) or 5) for s in settled)
    total_pnl = sum(float(s.get("pnl_net", 0) or 0) for s in settled)
    hit_rate = wins / (wins + losses) * 100 if (wins + losses) > 0 else None
    roi = total_pnl / total_staked * 100 if total_staked > 0 else None

    # Brier: mean of (forecast - outcome)^2; forecast = consensus prob, outcome = 1 if won else 0
    brier_vals = []
    for s in settled:
        if s.get("outcome") not in ("won", "lost"):
            continue
        forecast = s.get("consensus")
        if forecast is None:
            continue
        actual = 1 if s.get("outcome") == "won" else 0
        # For BUY_NO signals, we're betting against the consensus — flip the comparison
        if s.get("side") == "BUY_NO":
            forecast = 1 - forecast
        brier_vals.append((forecast - actual) ** 2)
    brier = sum(brier_vals) / len(brier_vals) if brier_vals else None

    return {
        "total_signals": total_signals,
        "settled": n_settled,
        "pending": total_signals - n_settled,
        "wins": wins,
        "losses": losses,
        "pushes": pushes,
        "hit_rate_pct": round(hit_rate, 1) if hit_rate is not None else None,
        "roi_pct": round(roi, 2) if roi is not None else None,
        "brier": round(brier, 4) if brier is not None else None,
        "total_staked_usd": round(total_staked, 2),
        "total_pnl_usd": round(total_pnl, 2),
    }


def regenerate_readme() -> None:
    """Write README.md with current running totals and recent signals."""
    signals = _load_all_signals()
    outcomes = _load_outcomes()
    metrics = compute_metrics(signals, outcomes)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    first_date = signals[0]["ts"][:10] if signals else "(none)"
    last_date = signals[-1]["ts"][:10] if signals else "(none)"

    def _fmt(v, fmt: str = "{}"):
        return fmt.format(v) if v is not None else "—"

    lines = [
        "# Kalshi Motorsports Edge Scanner — Public Track Record",
        "",
        "Cryptographically timestamped picks from a Kalshi motorsports edge scanner.",
        "Every signal is committed (and SSH-signed) at the moment it's generated — no retroactive edits.",
        "",
        f"_Last updated: {now}_",
        f"_Tracking period: {first_date} → {last_date}_",
        "",
        "## Performance",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total signals issued | {metrics['total_signals']} |",
        f"| Settled | {metrics['settled']} |",
        f"| Pending | {metrics['pending']} |",
        f"| Wins / Losses / Pushes | {metrics['wins']} / {metrics['losses']} / {metrics['pushes']} |",
        f"| Hit rate | {_fmt(metrics['hit_rate_pct'], '{:.1f}%')} |",
        f"| ROI (net of vig, on flat stake) | {_fmt(metrics['roi_pct'], '{:+.2f}%')} |",
        f"| Brier score (lower is better) | {_fmt(metrics['brier'])} |",
        f"| Total staked (model units, $5/signal) | ${metrics['total_staked_usd']:.2f} |",
        f"| Net P/L | ${metrics['total_pnl_usd']:+.2f} |",
        "",
        "## Gate thresholds",
        "",
        "- Edge threshold: ≥3 percentage points between Kalshi mid and cross-book consensus",
        "- Liquidity gate: ≥$500 open interest, ≥$200 24h volume, mid between 8% and 92%",
        "- Recommended unit stake: $5 (flat)",
        "- 8-week gate eval: ≥3% ROI net + Brier ≤0.20",
        "",
        "## Recent signals (newest 20)",
        "",
        "| Time (UTC) | Market | Side | Driver | Kalshi mid | Consensus | Edge | Status |",
        "|---|---|---|---|---|---|---|---|",
    ]

    for s in list(reversed(signals))[:20]:
        sid = s.get("signal_id", "")
        o = outcomes.get(sid)
        if o and o.get("settled"):
            outcome = o.get("outcome", "?")
            pnl = o.get("pnl_net", 0) or 0
            status = f"{outcome} ({pnl:+.2f})"
        else:
            status = "pending"
        ts = s.get("ts", "")[:16].replace("T", " ")
        market = s.get("market", "")
        side = s.get("side", "")
        driver = s.get("driver", "")
        mid = s.get("kalshi_mid")
        cons = s.get("consensus")
        edge = s.get("edge_pp")
        lines.append(
            f"| {ts} | `{market}` | {side} | {driver} | {mid} | {cons} | {edge:+.2f}pp | {status} |"
        )

    lines += [
        "",
        "## How it works",
        "",
        "1. The scanner pulls 192 Kalshi motorsports markets every 10 minutes.",
        "2. For each market that passes liquidity gates, it compares Kalshi's mid-price to a "
        "de-vigged consensus across major US sportsbooks (currently DraftKings; FanDuel & OddsChecker WIP).",
        "3. If the edge is ≥3pp, a signal is emitted, written to JSONL, and committed here.",
        "4. After each race finishes, outcomes are scored and the README is regenerated.",
        "",
        "## Trust",
        "",
        "Every signal commit is SSH-signed by `git_signing_key` "
        "(SHA256:Z83PMzP2ydkRvD3oyO6zmLn2RgJaqlekgHxKkCKJkDE). "
        "Outcomes commits are also signed. Tampering with historical signals would invalidate signatures.",
        "",
    ]

    README.write_text("\n".join(lines))


def commit_and_push(message: str = "", push: bool = False) -> None:
    """Stage all changes, sign-commit, optionally push to origin/main."""
    _run(["git", "add", "-A"])
    # Only commit if there are changes
    status = _run(["git", "status", "--porcelain"], check=False)
    if not status.stdout.strip():
        return
    if not message:
        message = f"Auto signal+README update {datetime.now(timezone.utc).isoformat()}"
    _run(["git", "commit", "-m", message])
    if push:
        # Best effort — don't break the signal pipeline if remote not configured
        try:
            _run(["git", "push", "origin", "main"], check=False)
        except Exception:
            pass


def record_new_signals(new_signals: list, push: bool = False) -> int:
    """End-to-end: write signals, regenerate README, commit (and optionally push)."""
    if not new_signals:
        return 0
    n = append_signals(new_signals)
    regenerate_readme()
    msg = f"{n} new signal(s) at {datetime.now(timezone.utc).isoformat()}"
    commit_and_push(msg, push=push)
    return n


if __name__ == "__main__":
    # Manual run: regenerate README from existing data and commit if changed
    regenerate_readme()
    commit_and_push("Regenerate README", push=False)
    print("README regenerated and committed if changed.")
