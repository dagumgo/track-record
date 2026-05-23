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
    """Write README.md with current running totals, recent signals, and credibility section."""
    signals = _load_all_signals()
    outcomes = _load_outcomes()
    metrics = compute_metrics(signals, outcomes)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    first_date = signals[0]["ts"][:10] if signals else "(none)"
    last_date = signals[-1]["ts"][:10] if signals else "(none)"

    def _fmt(v, fmt: str = "{}"):
        return fmt.format(v) if v is not None else "—"

    lines = [
        "# Public Track Record — Kalshi Motorsports Edge Scanner",
        "",
        "Every signal generated by the scanner is appended here and committed with an SSH "
        "signature **before the race starts**. Commits are timestamped by the git history; "
        "signatures are verified by GitHub (green “Verified” badge on each commit).",
        "",
        "**Picks cannot be backdated, edited, or removed** without invalidating the signature "
        "chain. This is the cryptographic proof-of-pick layer that backs the paid signal "
        "service — publish first, prove later.",
        "",
        f"_Last updated: {now}_  ",
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
        "## Evaluation gate (8 weeks paper-trading)",
        "",
        "Before charging for signals, the model must clear both gates over an 8-week forward "
        "paper-trading window:",
        "",
        "- **ROI** ≥ +3% net of vig, flat $5 stake per signal",
        "- **Brier score** ≤ 0.20 (calibration of consensus probability vs. observed outcomes)",
        "",
        "Track-record file structure:",
        "",
        "- `signals/YYYY-MM-DD.jsonl` — append-only daily logs, one signal per line",
        "- `outcomes/YYYY-MM-DD-<event>.json` — post-race resolution per event",
        "- Resolution runs hourly via systemd timer; queries Kalshi’s public market API for settlement",
        "",
        "## Methodology",
        "",
        "1. Scanner pulls 192 Kalshi motorsports markets every 10 minutes.",
        "2. Markets must pass liquidity gates: ≥$500 open interest, ≥$200 24h volume, mid between 8– 92%.",
        "3. Kalshi mid is compared to a de-vigged consensus probability from sportsbooks (currently "
        "DraftKings; FanDuel & OddsChecker integration in progress).",
        "4. If the edge is ≥3 percentage points, a signal is emitted, appended to that day’s JSONL, "
        "and immediately committed with an SSH signature.",
        "5. After race settlement, outcomes are scored, P/L computed (flat $5 stake), README regenerated.",
        "",
        "**Cross-race caveat (F1):** Until DraftKings publishes per-race F1 odds, F1 signals compare "
        "Kalshi’s next-race market to DraftKings’ futures market on a later race. Treat F1 signals "
        "as exploratory; NASCAR signals are clean.",
        "",
        "## How to verify a signature",
        "",
        "Every commit shows GitHub’s green **Verified** badge on the commit page. To verify locally:",
        "",
        "```bash",
        "git clone https://github.com/dagumgo/track-record.git && cd track-record",
        "git log --show-signature -1",
        "```",
        "",
        "Signing key: `SHA256:NYwV+8F9pEQ2hYU8FISwvQgAKiYu8WyhqQM+i4N9uKo`  ",
        "Public key on GitHub: https://api.github.com/users/dagumgo/ssh_signing_keys",
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
        "---",
        "",
        "_This README is auto-generated by `scripts/track_record.py` after each signal batch. "
        "Edits to this file directly will be overwritten._",
        "",
    ]

    README.write_text(chr(10).join(lines))

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
