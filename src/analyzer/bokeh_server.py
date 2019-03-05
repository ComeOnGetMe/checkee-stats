from __future__ import print_function
import pandas as pd
from os.path import join
from datetime import date

from bokeh.plotting import figure
from bokeh.layouts import layout, column
from bokeh.models import ColumnDataSource, Div
from bokeh.models.widgets import DateRangeSlider, Slider, Select, TextInput
from bokeh.io import curdoc

from preproc import DATA_DIR


def to_date(s):
    return date(*s.split('-'))


df = pd.DataFrame.from_csv(join(DATA_DIR, 'proced.csv'))
axis_map = df.columns
min_date = to_date(df.check_date.min())
max_date = to_date(df.check_date.max())
all_embassys = pd.unique(df['loc'])
all_status = pd.unique(df['status'])

# Create Input controls
reviews = Slider(title="Minimum number of reviews", value=80, start=10, end=300, step=10)
date_slid = DateRangeSlider(
    title="Min date checked", start=min_date, end=max_date, value=(date.today(), date.today()), step=1)
embassy_sel = Select(title="Embassy", value='BeiJing', options=pd.unique(df['loc']))
status_sel = Select(title="Application status", value='Clear', options=pd.unique(df['status']))
app_type_sel = Select(title="Type of application", value='New', options=pd.unique(df['type']))
visa_type_sel = Select(title="Type of visa", value='New', options=pd.unique(df['visa']))

x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Tomato Meter")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Number of Reviews")

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(check_date=[], waiting_days=[], ID=[], alpha=[]))

TOOLTIPS=[
    ("ID", "@id"),
    # ("Year", "@year"),
    # ("$", "@revenue")
]

p = figure(plot_height=600, plot_width=700, title="", toolbar_location=None, tooltips=TOOLTIPS)
p.circle(x="check_date", y="waiting_days", source=source, size=7, line_color=None, fill_alpha="alpha")


def select_movies():
    genre_val = genre.value
    director_val = director.value.strip()
    cast_val = cast.value.strip()
    selected = movies[
        (movies.Reviews >= reviews.value) &
        (movies.BoxOffice >= (boxoffice.value * 1e6)) &
        (movies.Year >= min_month.value) &
        (movies.Year <= max_month.value) &
        (movies.Oscars >= oscars.value)
        ]
    if (genre_val != "All"):
        selected = selected[selected.Genre.str.contains(genre_val)==True]
    if (director_val != ""):
        selected = selected[selected.Director.str.contains(director_val)==True]
    if (cast_val != ""):
        selected = selected[selected.Cast.str.contains(cast_val)==True]
    return selected


def update():
    df = select_movies()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title.text = "%d movies selected" % len(df)
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        color=df["color"],
        title=df["Title"],
        year=df["Year"],
        revenue=df["revenue"],
        alpha=df["alpha"],
    )

controls = [reviews, boxoffice, genre, min_month, max_month, oscars, director, cast, x_axis, y_axis]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = column(*controls, sizing_mode=sizing_mode)
l = layout([
    [desc],
    [inputs, p],
], sizing_mode=sizing_mode)

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Movies"
