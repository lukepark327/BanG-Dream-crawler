# BanG Dream! crawler
BanG Dream! songs crawler from Bestdori.

## Abstract
Auto download BanG Dream! songs from Bestdori (https://bestdori.com) .

![](./example.png)

## How to Use

### Install requirements
```bash
python install -r requirements.txt
```

```bash
python crawler.py -h
```
```bash
usage: crawler.py [-h] [--start S] [--end E]

Some hyperparameters

optional arguments:
  -h, --help  show this help message and exit
  --start S   start number of song's ID
  --end E     end number of song's ID
```

For example:

```bash
python crawler.py --end=200
```

# TODO
- [ ] Being able to download album art only.

# Contact
:email: lukepark327@gmail.com
