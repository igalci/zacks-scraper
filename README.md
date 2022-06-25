# zacks-scraper

Scrapes the zacks.com earnings tables.

## Usage

```python
from zacks_scraper.scraper import Scraper
my_scraper = Scraper ("AAPL")
data = my_scraper.get()
```