# Kalshi Motorsports Edge Scanner — Public Track Record

Cryptographically timestamped picks from a Kalshi motorsports edge scanner.
Every signal is committed (and SSH-signed) at the moment it's generated — no retroactive edits.

_Last updated: 2026-05-23 17:02 UTC_
_Tracking period: 2026-05-22 → 2026-05-23_

## Performance

| Metric | Value |
|---|---|
| Total signals issued | 161 |
| Settled | 0 |
| Pending | 161 |
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
| 2026-05-23 17:02 | `KXF1RACEPODIUM-CANGP26-ANT` | BUY_NO | Andrea Kimi Antonelli | 0.81 | 0.2054 | +60.46pp | pending |
| 2026-05-23 17:02 | `KXF1RACEPODIUM-CANGP26-PIA` | BUY_NO | Oscar Piastri | 0.35 | 0.0856 | +26.44pp | pending |
| 2026-05-23 17:02 | `KXF1RACEPODIUM-CANGP26-VER` | BUY_NO | Max Verstappen | 0.24 | 0.1284 | +11.16pp | pending |
| 2026-05-23 16:41 | `KXF1RACEPODIUM-CANGP26-PIA` | BUY_NO | Oscar Piastri | 0.475 | 0.0856 | +38.94pp | pending |
| 2026-05-23 16:41 | `KXF1RACEPODIUM-CANGP26-RUS` | BUY_NO | George Russell | 0.465 | 0.2054 | +25.96pp | pending |
| 2026-05-23 16:30 | `KXNASCARRACE-CHA26-ROCH` | BUY_NO | Ross Chastain | 0.125 | 0.0241 | +10.09pp | pending |
| 2026-05-23 16:30 | `KXNASCARRACE-NOCEL26-COZI` | BUY_NO | Connor Zilisch | 0.13 | 0.0171 | +11.29pp | pending |
| 2026-05-23 16:30 | `KXF1RACEPODIUM-CANGP26-ANT` | BUY_NO | Andrea Kimi Antonelli | 0.755 | 0.2054 | +54.96pp | pending |
| 2026-05-23 16:30 | `KXF1RACEPODIUM-CANGP26-HAM` | BUY_NO | Lewis Hamilton | 0.17 | 0.0453 | +12.47pp | pending |
| 2026-05-23 16:30 | `KXF1RACEPODIUM-CANGP26-NOR` | BUY_NO | Lando Norris | 0.52 | 0.1926 | +32.74pp | pending |
| 2026-05-23 16:30 | `KXF1RACE-CANGP26-NOR` | BUY_YES | Lando Norris | 0.13 | 0.1926 | -6.26pp | pending |
| 2026-05-23 16:30 | `KXF1RACE-CANGP26-RUS` | BUY_NO | George Russell | 0.425 | 0.2054 | +21.96pp | pending |
| 2026-05-23 16:20 | `KXF1RACEPODIUM-CANGP26-VER` | BUY_NO | Max Verstappen | 0.21 | 0.1284 | +8.16pp | pending |
| 2026-05-23 16:10 | `KXNASCARRACE-COC26-CHBE` | BUY_NO | Christopher Bell | 0.105 | 0.0737 | +3.13pp | pending |
| 2026-05-23 16:00 | `KXF1RACEPODIUM-CANGP26-ANT` | BUY_NO | Andrea Kimi Antonelli | 0.795 | 0.2054 | +58.96pp | pending |
| 2026-05-23 16:00 | `KXF1RACEPODIUM-CANGP26-HAM` | BUY_NO | Lewis Hamilton | 0.305 | 0.0453 | +25.97pp | pending |
| 2026-05-23 16:00 | `KXF1RACEPODIUM-CANGP26-NOR` | BUY_NO | Lando Norris | 0.46 | 0.1926 | +26.74pp | pending |
| 2026-05-23 16:00 | `KXF1RACEPODIUM-CANGP26-PIA` | BUY_NO | Oscar Piastri | 0.37 | 0.0856 | +28.44pp | pending |
| 2026-05-23 16:00 | `KXF1RACEPODIUM-CANGP26-RUS` | BUY_NO | George Russell | 0.735 | 0.2054 | +52.96pp | pending |
| 2026-05-23 14:36 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.14 | 0.0242 | +11.58pp | pending |

## How it works

1. The scanner pulls 192 Kalshi motorsports markets every 10 minutes.
2. For each market that passes liquidity gates, it compares Kalshi's mid-price to a de-vigged consensus across major US sportsbooks (currently DraftKings; FanDuel & OddsChecker WIP).
3. If the edge is ≥3pp, a signal is emitted, written to JSONL, and committed here.
4. After each race finishes, outcomes are scored and the README is regenerated.

## Trust

Every signal commit is SSH-signed by `git_signing_key` (SHA256:Z83PMzP2ydkRvD3oyO6zmLn2RgJaqlekgHxKkCKJkDE). Outcomes commits are also signed. Tampering with historical signals would invalidate signatures.
