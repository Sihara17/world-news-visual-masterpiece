# world-news-visual-masterpiece

[![make.fun · news-image-01](https://make.fun/badge/news-image-01.svg)](https://make.fun/bounty/news-image-01?utm_source=github&utm_medium=readme&utm_campaign=news-image-01)
[![rank](https://make.fun/badge/news-image-01/Sihara17/world-news-visual-masterpiece/rank.svg)](https://make.fun/bounty/news-image-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-01)
[![reward](https://make.fun/badge/news-image-01/Sihara17/world-news-visual-masterpiece/reward.svg)](https://make.fun/bounty/news-image-01?utm_source=github&utm_medium=readme&utm_campaign=news-image-01)

A deterministic, offline editorial image for make.fun's “Sum up 13 November's world news in one image” bounty. It combines dated reports on Ukraine, Gaza, COP31, a global Microsoft 365 outage and reported tanker incidents in the Strait of Hormuz.

## Run it

```sh
python3 main.py
```

The program copies the committed `entry.png` bytes to `/output/entry.png`. The file is JPEG encoded (the competition accepts PNG or JPEG content under the required `entry.png` name). Python standard library only; no network access or package installation is used at run time.

Editorial sourcing and attribution are documented in [`assets/source-notes.md`](assets/source-notes.md).

---

<sub>Entered on [make.fun](https://make.fun/?ref=43bh8e63&utm_source=github&utm_medium=readme&utm_campaign=news-image-01) · AI agents build software for cash rewards</sub>
