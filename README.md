# The Day, Hour by Hour — news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/vora95/makefun-news-image-20261126-burn/rank.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/vora95/makefun-news-image-20261126-burn/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Sum up Thursday 26 November 2026's world news in one image — as a
24-hour wire timeline. Six featured stories in chronological order on a
vertical timeline spine (mines in the Strait of Hormuz, Zaporizhzhia
losing power, a laser downing a drone, Houthis hitting Ras Tanura,
tariffs hammering markets, a Hamas security chief killed in Gaza), plus
sixteen more stories under "ALSO TODAY".

`main.py` (Python 3.13, standard library only) copies the shipped
`entry.png` (1024×1024, deterministic) to the output directory,
verifying its SHA-256, dimensions and size first. No network, no clock,
no randomness — running it twice writes byte-identical output.
