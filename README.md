# Kalshi Motorsports Edge Scanner — Public Track Record

Cryptographically timestamped picks from a Kalshi motorsports edge scanner.
Every signal is committed (and SSH-signed) at the moment it's generated — no retroactive edits.

_Last updated: 2026-05-23 16:00 UTC_
_Tracking period: 2026-05-22 → 2026-05-23_

## Performance

| Metric | Value |
|---|---|
| Total signals issued | 147 |
| Settled | 0 |
| Pending | 147 |
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
| 2026-05-23 16:00 | `KXF1RACEPODIUM-CANGP26-ANT` | BUY_NO | Andrea Kimi Antonelli | 0.795 | 0.2054 | +58.96pp | pending |
| 2026-05-23 16:00 | `KXF1RACEPODIUM-CANGP26-HAM` | BUY_NO | Lewis Hamilton | 0.305 | 0.0453 | +25.97pp | pending |
| 2026-05-23 16:00 | `KXF1RACEPODIUM-CANGP26-NOR` | BUY_NO | Lando Norris | 0.46 | 0.1926 | +26.74pp | pending |
| 2026-05-23 16:00 | `KXF1RACEPODIUM-CANGP26-PIA` | BUY_NO | Oscar Piastri | 0.37 | 0.0856 | +28.44pp | pending |
| 2026-05-23 16:00 | `KXF1RACEPODIUM-CANGP26-RUS` | BUY_NO | George Russell | 0.735 | 0.2054 | +52.96pp | pending |
| 2026-05-23 14:36 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.14 | 0.0242 | +11.58pp | pending |
| 2026-05-23 14:05 | `KXNASCARRACE-CHA26-COZI` | BUY_NO | Connor Zilisch | 0.19 | 0.0171 | +17.29pp | pending |
| 2026-05-23 14:05 | `KXNASCARRACE-NOCEL26-COZI` | BUY_NO | Connor Zilisch | 0.1 | 0.0171 | +8.29pp | pending |
| 2026-05-23 14:05 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.115 | 0.0242 | +9.08pp | pending |
| 2026-05-23 13:23 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.15 | 0.0242 | +12.58pp | pending |
| 2026-05-23 11:20 | `KXNASCARRACE-COC26-DEHA` | BUY_NO | Denny Hamlin | 0.15 | 0.1173 | +3.27pp | pending |
| 2026-05-23 10:59 | `KXNASCARRACE-NOCEL26-COZI` | BUY_NO | Connor Zilisch | 0.145 | 0.0172 | +12.78pp | pending |
| 2026-05-23 04:35 | `KXNASCARRACE-NOCEL26-COZI` | BUY_NO | Connor Zilisch | 0.115 | 0.0172 | +9.78pp | pending |
| 2026-05-23 03:32 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.18 | 0.0243 | +15.57pp | pending |
| 2026-05-23 03:21 | `KXNASCARRACE-CHA26-COZI` | BUY_NO | Connor Zilisch | 0.22 | 0.0172 | +20.28pp | pending |
| 2026-05-23 03:11 | `KXNASCARRACE-CHA26-ROCH` | BUY_NO | Ross Chastain | 0.16 | 0.0243 | +13.57pp | pending |
| 2026-05-23 03:11 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.215 | 0.0243 | +19.07pp | pending |
| 2026-05-23 02:50 | `KXNASCARRACE-CHA26-COZI` | BUY_NO | Connor Zilisch | 0.25 | 0.0172 | +23.28pp | pending |
| 2026-05-23 02:20 | `KXNASCARRACE-CHA26-COZI` | BUY_NO | Connor Zilisch | 0.28 | 0.0172 | +26.28pp | pending |
| 2026-05-23 01:38 | `KXNASCARRACE-NOCEL26-ROCH` | BUY_NO | Ross Chastain | 0.185 | 0.0243 | +16.07pp | pending |

## How it works

1. The scanner pulls 192 Kalshi motorsports markets every 10 minutes.
2. For each market that passes liquidity gates, it compares Kalshi's mid-price to a de-vigged consensus across major US sportsbooks (currently DraftKings; FanDuel & OddsChecker WIP).
3. If the edge is ≥3pp, a signal is emitted, written to JSONL, and committed here.
4. After each race finishes, outcomes are scored and the README is regenerated.

## Trust

Every signal commit is SSH-signed by `git_signing_key` (SHA256:Z83PMzP2ydkRvD3oyO6zmLn2RgJaqlekgHxKkCKJkDE). Outcomes commits are also signed. Tampering with historical signals would invalidate signatures.
