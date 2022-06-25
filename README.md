# zacks-scraper

Scrapes the zacks.com earnings tables.

## Usage

```
pip install git+https://github.com/igalci/zacks-scraper.git
```

```python
from zacks_scraper.scraper import Scraper
my_scraper = Scraper ("AAPL")
data = my_scraper.get()
```