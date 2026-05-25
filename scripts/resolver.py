"""Resolve settled signals: query Kalshi for market outcomes, compute P/L, write outcomes/*.json.

Run after each race finishes (or as a recurring cron — idempotent, only resolves newly-settled markets).
"""
import json
import logging
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import httpx

TRACK_DIR = Path("/opt/kalshi-track-record")
SIGNALS_DIR = TRACK_DIR / "signals"
OUTCOMES_DIR = TRACK_DIR / "outcomes"
KALSHI_BASE = "https://api.elections.kalshi.com/trade-api/v2"

log = logging.getLogger("resolver")


def _run(cmd: list, check: bool = True, cwd: Path = TRACK_DIR) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=check, cwd=cwd)


def _load_all_signals() -> list:
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


def _load_existing_outcomes() -> set:
    """Return set of (event_ticker, ticker) pairs already resolved."""
    resolved = set()
    if not OUTCOMES_DIR.exists():
        return resolved
    for path in OUTCOMES_DIR.glob("*.json"):
        try:
            with path.open() as f:
                race = json.load(f)
            for s in race.get("signals", []):
                if s.get("settled"):
                    resolved.add((s.get("event_ticker", ""), s.get("market", "")))
        except (json.JSONDecodeError, KeyError):
            continue
    return resolved


def fetch_market_status(ticker: str) -> dict:
    """Query Kalshi for a single market's current status + result."""
    try:
        r = httpx.get(f"{KALSHI_BASE}/markets/{ticker}", timeout=15)
        r.raise_for_status()
        return r.json().get("market", {})
    except Exception as e:
        log.warning("Kalshi fetch failed for %s: %s", ticker, e)
        return {}


def compute_pnl(side: str, kalshi_mid: float, stake: float, result: str) -> float:
    """Returns P/L in dollars.
    BUY_YES @ mid m: cost m/share, payoff 1 if result=yes else 0.
    BUY_NO @ mid m: cost (1-m)/share, payoff 1 if result=no else 0.
    """
    if result == "void":
        return 0.0  # push
    if side == "BUY_YES":
        if result == "yes":
            return round(stake * (1 - kalshi_mid) / kalshi_mid, 4)
        return -stake
    if side == "BUY_NO":
        if result == "no":
            return round(stake * kalshi_mid / (1 - kalshi_mid), 4)
        return -stake
    return 0.0


def _outcome_label(side: str, result: str) -> str:
    if result == "void":
        return "push"
    if (side == "BUY_YES" and result == "yes") or (side == "BUY_NO" and result == "no"):
        return "won"
    if result in ("yes", "no"):
        return "lost"
    return "unsettled"


def resolve_pending() -> dict:
    """Scan all pending signals, query Kalshi for settled markets, write outcomes files."""
    signals = _load_all_signals()
    already_resolved = _load_existing_outcomes()

    # Group pending signals by event_ticker
    pending_by_event = defaultdict(list)
    pending_markets = set()
    for s in signals:
        ev = s.get("event", "") or s.get("event_ticker", "")
        mkt = s.get("market", "")
        if not mkt:
            continue
        if (ev, mkt) in already_resolved:
            continue
        pending_by_event[ev].append(s)
        pending_markets.add(mkt)

    if not pending_markets:
        log.info("No pending markets to resolve.")
        return {"checked": 0, "newly_settled": 0, "events_written": 0}

    log.info("Checking %d distinct pending markets across %d events…",
             len(pending_markets), len(pending_by_event))

    # Fetch live status for each unique market
    market_status: dict[str, dict] = {}
    for ticker in pending_markets:
        market_status[ticker] = fetch_market_status(ticker)

    newly_settled = 0
    events_written = 0

    for event_ticker, sigs in pending_by_event.items():
        # All markets for this event
        event_sigs_settled = []
        any_unsettled = False
        for s in sigs:
            mkt = s.get("market", "")
            status = market_status.get(mkt, {})
            mkt_status = (status.get("status") or "").lower()
            result = (status.get("result") or "").lower() if status.get("result") else None
            if mkt_status not in ("settled", "determined") or not result:
                any_unsettled = True
                continue
            # Compute outcome
            side = s.get("side", "")
            mid = float(s.get("kalshi_mid") or 0)
            stake = float(s.get("recommended_stake_usd") or 5)
            outcome = _outcome_label(side, result)
            pnl = compute_pnl(side, mid, stake, result)
            event_sigs_settled.append({
                **s,
                "event_ticker": event_ticker,
                "settled": True,
                "result": result,
                "outcome": outcome,
                "pnl_net": pnl,
                "resolved_ts": datetime.now(timezone.utc).isoformat(),
            })
            newly_settled += 1

        if not event_sigs_settled:
            continue

        OUTCOMES_DIR.mkdir(parents=True, exist_ok=True)
        settled_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        # Filename: <YYYY-MM-DD>-<event_ticker>.json (e.g., 2026-05-25-KXNASCARRACE-COC26.json)
        safe_event = event_ticker.replace("/", "_").replace(" ", "_")
        path = OUTCOMES_DIR / f"{settled_date}-{safe_event}.json"

        # If file exists, merge (append unique signal_ids)
        existing_sigs = []
        if path.exists():
            try:
                with path.open() as f:
                    existing_sigs = json.load(f).get("signals", [])
            except (json.JSONDecodeError, KeyError):
                pass
        existing_ids = {s.get("signal_id") for s in existing_sigs}
        merged = existing_sigs + [s for s in event_sigs_settled if s.get("signal_id") not in existing_ids]

        with path.open("w") as f:
            json.dump({
                "event_ticker": event_ticker,
                "resolved_ts": datetime.now(timezone.utc).isoformat(),
                "all_settled": not any_unsettled,
                "signals": merged,
            }, f, indent=2)
        events_written += 1
        log.info("Wrote %d settled signals for event %s -> %s",
                 len(event_sigs_settled), event_ticker, path.name)

    return {
        "checked": len(pending_markets),
        "newly_settled": newly_settled,
        "events_written": events_written,
    }


def commit_outcomes(message: str = "") -> bool:
    """Sign-commit outcomes/* + regenerated README. Returns True if a commit happened."""
    _run(["git", "add", "-A"])
    status = _run(["git", "status", "--porcelain"], check=False)
    if not status.stdout.strip():
        return False
    if not message:
        message = f"Resolve outcomes {datetime.now(timezone.utc).isoformat()}"
    _run(["git", "commit", "-m", message])
    push = _run(["git", "push", "origin", "main"], check=False)
    if push.returncode != 0:
        log.warning("git push failed: %s", push.stderr[:200])
    return True


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    summary = resolve_pending()
    log.info("Resolve summary: %s", summary)

    if summary["newly_settled"] > 0:
        # Regenerate README to reflect new metrics
        sys.path.insert(0, str(TRACK_DIR / "scripts"))
        from track_record import regenerate_readme
        regenerate_readme()
        commit_outcomes(f"Resolved {summary['newly_settled']} signal(s) across {summary['events_written']} event(s)")
        log.info("Committed.")


if __name__ == "__main__":
    main()
