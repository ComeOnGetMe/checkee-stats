# Checkee Stats

US visa administrative processing time data analytics in Python.

* [Data source](https://checkee.info)
* Retriever - scrapy
* Analyzer - powered by [bokeh](https://bokeh.pydata.org/en/latest/)

### How to use

Scrape latest checkee.info reports
```
cd src/retriever
scrapy crawl checkee
```
This will populate the `data` folder.

Then start the visualization server by
```
cd src/analyzer
bokeh serve --show checkee.py
```
