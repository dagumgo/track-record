# Kalshi Motorsports Edge Scanner — Public Track Record

Cryptographically timestamped picks from a Kalshi motorsports edge scanner.
Every signal is committed (and SSH-signed) at the moment it's generated — no retroactive edits.

_Last updated: 2026-05-22 23:03 UTC_
_Tracking period: 2026-05-22 → 2026-05-22_

## Performance

| Metric | Value |
|---|---|
| Total signals issued | 112 |
| Settled | 0 |
| Pending | 112 |
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
| 2026-05-22 23:03 | `KXNASCARRACE-COC26-DEHA` | BUY_NO | Denny Hamlin | 0.185 | 0.1174 | +6.76pp | pending |
| 2026-05-22 23:03 | `KXNASCARRACE-COC26-TYRE` | BUY_NO | Tyler Reddick | 0.145 | 0.0939 | +5.11pp | pending |
| 2026-05-22 23:03 | `KXNASCARRACE-CHA26-COZI` | BUY_NO | Connor Zilisch | 0.195 | 0.0172 | +17.78pp | pending |
| 2026-05-22 23:03 | `KXNASCARRACE-NOCEL26-COZI` | BUY_NO | Connor Zilisch | 0.155 | 0.0172 | +13.78pp | pending |
| 2026-05-22 23:03 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.165 | 0.0243 | +14.07pp | pending |
| 2026-05-22 23:03 | `KXF1RACEPODIUM-CANGP26-LEC` | BUY_NO | Charles Leclerc | 0.15 | 0.0642 | +8.58pp | pending |
| 2026-05-22 23:03 | `KXF1RACEPODIUM-CANGP26-NOR` | BUY_NO | Lando Norris | 0.49 | 0.1926 | +29.74pp | pending |
| 2026-05-22 23:03 | `KXF1RACEPODIUM-CANGP26-PIA` | BUY_NO | Oscar Piastri | 0.19 | 0.0856 | +10.44pp | pending |
| 2026-05-22 23:03 | `KXF1RACEPODIUM-CANGP26-VER` | BUY_NO | Max Verstappen | 0.24 | 0.1284 | +11.16pp | pending |
| 2026-05-22 23:03 | `KXF1RACE-CANGP26-ANT` | BUY_NO | Andrea Kimi Antonelli | 0.4 | 0.2054 | +19.46pp | pending |
| 2026-05-22 23:03 | `KXF1RACE-CANGP26-NOR` | BUY_YES | Lando Norris | 0.105 | 0.1926 | -8.76pp | pending |
| 2026-05-22 23:03 | `KXF1RACE-CANGP26-RUS` | BUY_NO | George Russell | 0.395 | 0.2054 | +18.96pp | pending |
| 2026-05-22 22:52 | `KXF1RACEPODIUM-CANGP26-HAM` | BUY_NO | Lewis Hamilton | 0.49 | 0.0453 | +44.47pp | pending |
| 2026-05-22 22:31 | `KXNASCARRACE-COC26-DEHA` | BUY_NO | Denny Hamlin | 0.185 | 0.1174 | +6.76pp | pending |
| 2026-05-22 22:31 | `KXNASCARRACE-COC26-TYRE` | BUY_NO | Tyler Reddick | 0.145 | 0.0939 | +5.11pp | pending |
| 2026-05-22 22:31 | `KXNASCARRACE-NOCEL26-COZI` | BUY_NO | Connor Zilisch | 0.165 | 0.0172 | +14.78pp | pending |
| 2026-05-22 22:31 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.155 | 0.0243 | +13.07pp | pending |
| 2026-05-22 22:31 | `KXF1RACEPODIUM-CANGP26-LEC` | BUY_NO | Charles Leclerc | 0.16 | 0.0642 | +9.58pp | pending |
| 2026-05-22 22:31 | `KXF1RACEPODIUM-CANGP26-NOR` | BUY_NO | Lando Norris | 0.475 | 0.1926 | +28.24pp | pending |
| 2026-05-22 22:31 | `KXF1RACEPODIUM-CANGP26-PIA` | BUY_NO | Oscar Piastri | 0.39 | 0.0856 | +30.44pp | pending |

## How it works

1. The scanner pulls 192 Kalshi motorsports markets every 10 minutes.
2. For each market that passes liquidity gates, it compares Kalshi's mid-price to a de-vigged consensus across major US sportsbooks (currently DraftKings; FanDuel & OddsChecker WIP).
3. If the edge is ≥3pp, a signal is emitted, written to JSONL, and committed here.
4. After each race finishes, outcomes are scored and the README is regenerated.

## Trust

Every signal commit is SSH-signed by `git_signing_key` (SHA256:Z83PMzP2ydkRvD3oyO6zmLn2RgJaqlekgHxKkCKJkDE). Outcomes commits are also signed. Tampering with historical signals would invalidate signatures.
