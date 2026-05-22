# Kalshi Motorsports Edge Scanner — Public Track Record

Cryptographically timestamped picks from a Kalshi motorsports edge scanner.
Every signal is committed (and SSH-signed) at the moment it's generated — no retroactive edits.

_Last updated: 2026-05-22 22:16 UTC_
_Tracking period: (none) → (none)_

## Performance

| Metric | Value |
|---|---|
| Total signals issued | 0 |
| Settled | 0 |
| Pending | 0 |
| Wins / Losses / Pushes | 0 / 0 / 0 |
| Hit rate | — |
| ROI (net of vig, on flat stake) | — |
| Brier score (lower is better) | — |
| Total staked (model units, $5/signal) | $0.00 |
| Net P/L | $+0.00 |

## Gate thresholds

- Edge threshold: ≥3 percentage points between Kalshi mid and cross-book consensus
- Liquidity gate: ≥$500 open interest, ≥$200 24h volume, mid between 8% and 92%
- Recommended unit stake: $5 (flat)
- 8-week gate eval: ≥3% ROI net + Brier ≤0.20

## Recent signals (newest 20)

| Time (UTC) | Market | Side | Driver | Kalshi mid | Consensus | Edge | Status |
|---|---|---|---|---|---|---|---|

## How it works

1. The scanner pulls 192 Kalshi motorsports markets every 10 minutes.
2. For each market that passes liquidity gates, it compares Kalshi's mid-price to a de-vigged consensus across major US sportsbooks (currently DraftKings; FanDuel & OddsChecker WIP).
3. If the edge is ≥3pp, a signal is emitted, written to JSONL, and committed here.
4. After each race finishes, outcomes are scored and the README is regenerated.

## Trust

Every signal commit is SSH-signed by `git_signing_key` (SHA256:Z83PMzP2ydkRvD3oyO6zmLn2RgJaqlekgHxKkCKJkDE). Outcomes commits are also signed. Tampering with historical signals would invalidate signatures.
