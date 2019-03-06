from __future__ import print_function

import pandas as pd

from bokeh.plotting import figure
from bokeh.layouts import layout, column
from bokeh.models import ColumnDataSource, Div, HoverTool
from bokeh.models.widgets import DateRangeSlider, Select, MultiSelect
from bokeh.io import curdoc

from preproc import read_data_batch, preproc_data


checkee = read_data_batch()
checkee = preproc_data(checkee)

axis_map = checkee.columns
min_date = checkee.check_date.min().date()
max_date = checkee.check_date.max().date()

all_status = list(pd.unique(checkee.status)) + ['All']
all_app_types = list(pd.unique(checkee.type)) + ['All']

# Create Input controls
date_slid = DateRangeSlider(title="Check date range", start=min_date, end=max_date,
                            value=(min_date, max_date), step=1)
embassy_sel = MultiSelect(title="Embassy", value=['BeiJing'], options=pd.unique(checkee['loc']).tolist())
visa_type_sel = MultiSelect(title="Type of visa", value=['H1'], options=pd.unique(checkee['visa']).tolist())
status_sel = Select(title="Application status", value='All', options=all_status)
app_type_sel = Select(title="Type of application", value='All', options=all_app_types)

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], ID=[], complete_date=[]))

TOOLTIPS = [
    ("id", "@ID"),
    ("check date", "@x{%F}"),
    ("complete date", "@complete_date{%F}"),
    ("waiting days", "@y"),
]

p = figure(plot_height=600, plot_width=700, title="",
           toolbar_location='right', x_axis_type='datetime')
p.circle(x="x", y="y", source=source, size=7, line_color=None)#, fill_alpha="alpha")
p.add_tools(HoverTool(
    tooltips=TOOLTIPS,
    formatters={
        'x': 'datetime',
        'complete_date': 'datetime'
    }
))


def select_checkees():
    date_start, date_end = date_slid.value_as_datetime
    emb = set(embassy_sel.value)
    vtypes = set(visa_type_sel.value)
    status = status_sel.value
    atype = app_type_sel.value

    selected = checkee[
        (pd.to_datetime(checkee.check_date).between(date_start, date_end)) &
        (checkee['loc'].isin(emb)) &
        (checkee.visa.isin(vtypes))
    ]
    if status != "All":
        selected = selected[selected.status == status]
    if atype != "All":
        selected = selected[selected.type == atype]
    return selected


def update():
    df = select_checkees()
    p.title.text = "%d movies selected" % len(df)
    source.data = dict(
        x=pd.to_datetime(df.check_date),
        y=df.waiting_days,
        ID=df.id,
        complete_date=pd.to_datetime(df.complete_date),
    )


controls = [date_slid, embassy_sel, visa_type_sel, status_sel, app_type_sel]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'scale_width'  # 'scale_width' also looks nice with this example

inputs = column(*controls, sizing_mode=sizing_mode)
l = layout([
    [Div(text='', width=800)],
    [inputs, p],
], sizing_mode=sizing_mode)

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Checkees"
