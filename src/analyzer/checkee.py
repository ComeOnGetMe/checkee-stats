from __future__ import print_function

from bokeh.io import curdoc

from preproc import read_data_batch, preproc_data
from components import Page


batch = read_data_batch()
batch = preproc_data(batch)

p = Page(batch)
p.update()
curdoc().add_root(p.layout)
curdoc().title = 'Checkees'
