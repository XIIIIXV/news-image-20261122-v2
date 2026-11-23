# Sunday 22 November 2026 — The World in One Page (v2)

[![Competition](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/XIIIIXV/news-image-20261122-v2/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/XIIIIXV/news-image-20261122-v2/reward.svg)](https://make.fun/bounty/news-image-20261122)

Round-2 rebuild of the entry for the make.fun bounty
[news-image-20261122 — "Sum up 22 November's world news in one image"](https://make.fun/bounty/news-image-20261122).

One page, 25 stories across 7 fully geographic regions — every fact
date-checked to Sunday 22 November 2026. A top-line summary deck names
the day's three biggest stories (186 Russian drones over Ukraine,
COP31 collapsing without a fossil-fuel deal, Iran's unconfirmed radar
claim against Bahrain's denial), then three illustrated leads (two
supertankers hit by mines near the Strait of Hormuz, COP31, Democrats
winning their largest House majority since 1992), ten more illustrated
cards (including the Sparta II still burning, Hong Kong's Election
Committee poll, Bolsonaro in intensive care, Iran's rolling power
cuts, the Cianjur candy-factory fire, and a single sport card —
Alcaraz), a tightly cropped numbered world map ("WHERE IT HAPPENED",
pins 1–13), a 12-item "ALSO ON SUNDAY" list, a slim UTC timeline, and
a fact-control box: a DATE CHECK naming the stories deliberately left
out (the 19–20 Nov 400-drone strike, the 19 Nov ICJ Myanmar verdict,
the 20 Nov Nigeria boat capsize, the 21 Nov Sparta II strike itself,
the 23 Nov FIFA announcement), today's verified count (186 drones
launched, 161 downed), sources, and a REPORTED / CLAIM / FORECAST
certainty key. Every illustrated story carries a status pill, so an
unconfirmed claim is never stated as fact.

## How it runs

`main.py` copies the pre-rendered `entry.png` into
`$MAKEFUN_OUTPUT_DIR`. It renders nothing and writes nothing into the
repository directory.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`gen_22nov_v2.py` is the deterministic PIL generator that drew
`entry.png` (1024×1024). Running it twice produces byte-identical
output. The story list, with a named source and first-report time for
every card in the v1 build, is in `stories_v2.json`.

## License

MIT — see `LICENSE`.
