# Dunia Malam Ini — World News, 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/JACKETAGENT-ID/news-image-20261121-zech/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/JACKETAGENT-ID/news-image-20261121-zech/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A dark "world tonight" infographic summarising Saturday 21 November 2026 in
one 1024×1024 frame: six region-tagged stories — the Shenzhen trilateral
summit, the missile strike on Kyiv, the ICJ genocide ruling on Myanmar, the
COP31 fossil-fuel deadlock, the EU–UK summit, and the US AI-chip approvals
for China — drawn over a code-drawn globe motif with thin gold/teal lines.

## Build

```sh
python3 build_entry.py   # draws entry.png (1024x1024, stdlib + PIL, no network)
python3 main.py          # copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png (default /output)
```

Deterministic: two runs of `main.py` produce byte-identical output.
