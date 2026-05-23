# Kalshi Motorsports Edge Scanner — Public Track Record

Cryptographically timestamped picks from a Kalshi motorsports edge scanner.
Every signal is committed (and SSH-signed) at the moment it's generated — no retroactive edits.

_Last updated: 2026-05-23 03:11 UTC_
_Tracking period: 2026-05-22 → 2026-05-23_

## Performance

| Metric | Value |
|---|---|
| Total signals issued | 132 |
| Settled | 0 |
| Pending | 132 |
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
| 2026-05-23 03:11 | `KXNASCARRACE-CHA26-ROCH` | BUY_NO | Ross Chastain | 0.16 | 0.0243 | +13.57pp | pending |
| 2026-05-23 03:11 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.215 | 0.0243 | +19.07pp | pending |
| 2026-05-23 02:50 | `KXNASCARRACE-CHA26-COZI` | BUY_NO | Connor Zilisch | 0.25 | 0.0172 | +23.28pp | pending |
| 2026-05-23 02:20 | `KXNASCARRACE-CHA26-COZI` | BUY_NO | Connor Zilisch | 0.28 | 0.0172 | +26.28pp | pending |
| 2026-05-23 01:38 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.185 | 0.0243 | +16.07pp | pending |
| 2026-05-23 00:58 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.145 | 0.0243 | +12.07pp | pending |
| 2026-05-23 00:58 | `KXF1RACEPODIUM-CANGP26-ANT` | BUY_NO | Andrea Kimi Antonelli | 0.605 | 0.2054 | +39.96pp | pending |
| 2026-05-23 00:58 | `KXF1RACEPODIUM-CANGP26-HAM` | BUY_NO | Lewis Hamilton | 0.52 | 0.0453 | +47.47pp | pending |
| 2026-05-23 00:47 | `KXNASCARRACE-CHA26-COZI` | BUY_NO | Connor Zilisch | 0.245 | 0.0172 | +22.78pp | pending |
| 2026-05-23 00:47 | `KXF1RACEPODIUM-CANGP26-ANT` | BUY_NO | Andrea Kimi Antonelli | 0.535 | 0.2054 | +32.96pp | pending |
| 2026-05-23 00:37 | `KXF1RACEPODIUM-CANGP26-LEC` | BUY_NO | Charles Leclerc | 0.165 | 0.0642 | +10.08pp | pending |
| 2026-05-23 00:37 | `KXF1RACEPODIUM-CANGP26-RUS` | BUY_NO | George Russell | 0.815 | 0.2054 | +60.96pp | pending |
| 2026-05-23 00:15 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.175 | 0.0243 | +15.07pp | pending |
| 2026-05-23 00:15 | `KXF1RACE-CANGP26-ANT` | BUY_NO | Andrea Kimi Antonelli | 0.375 | 0.2054 | +16.96pp | pending |
| 2026-05-23 00:05 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.295 | 0.0243 | +27.07pp | pending |
| 2026-05-22 23:55 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.16 | 0.0243 | +13.57pp | pending |
| 2026-05-22 23:55 | `KXF1RACEPODIUM-CANGP26-ANT` | BUY_NO | Andrea Kimi Antonelli | 0.57 | 0.2054 | +36.46pp | pending |
| 2026-05-22 23:44 | `KXNASCARRACE-NOCEL26-COZI` | BUY_NO | Connor Zilisch | 0.085 | 0.0172 | +6.78pp | pending |
| 2026-05-22 23:44 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.13 | 0.0243 | +10.57pp | pending |
| 2026-05-22 23:44 | `KXF1RACEPODIUM-CANGP26-LEC` | BUY_NO | Charles Leclerc | 0.12 | 0.0642 | +5.58pp | pending |

## How it works

1. The scanner pulls 192 Kalshi motorsports markets every 10 minutes.
2. For each market that passes liquidity gates, it compares Kalshi's mid-price to a de-vigged consensus across major US sportsbooks (currently DraftKings; FanDuel & OddsChecker WIP).
3. If the edge is ≥3pp, a signal is emitted, written to JSONL, and committed here.
4. After each race finishes, outcomes are scored and the README is regenerated.

## Trust

Every signal commit is SSH-signed by `git_signing_key` (SHA256:Z83PMzP2ydkRvD3oyO6zmLn2RgJaqlekgHxKkCKJkDE). Outcomes commits are also signed. Tampering with historical signals would invalidate signatures.
