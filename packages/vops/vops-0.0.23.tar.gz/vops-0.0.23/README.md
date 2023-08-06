# Vops
This python project uses data from yahoo finance to graph option profit-loss diagrams.

Note: any examples used here are outdated because the option contracts have expired.

## Installing
Installing with pip:
```bash
pip install vops
```

## Usage
Simple program graphing a long call option:
```python
from vops import scraping
from vops import graphing

optionObj = scraping.scrapeCallOptions('AMD')

graphing.graphLongCall(optionObj, 'AMD201231C00060000')
```
Graphing both short and long positions on a call option:
```python
optionObj = scraping.scrapeCallOptions('AMD')

graphing.graphCalls(optionObj, 'AMD201231C00060000')
```

Exporting graphs to a png:
```python
graphing.graphCalls(optionObj, 'AMD201231C00060000', export = True)
```

Output:

![plot](./res/options.png)

## Todo

* Add axis labels to all graphs
* Create method for graphing long and short put options simultaneously
* Merge call/put options chains
* Allow option chains from different chains to be scraped
