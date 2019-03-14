import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool


class ScatterPlot(object):
    def __init__(self):
        self.source = ColumnDataSource(data=dict(x=[], y=[], ID=[], complete_date=[]))
        self._init_hover()
        self._init_figure()

    def _init_hover(self):
        self.tooltips = [
            ("id", "@ID"),
            ("check date", "@x{%F}"),
            ("complete date", "@complete_date{%F}"),
            ("waiting days", "@y"),
        ]

        self.hover = HoverTool(
            tooltips=self.tooltips,
            formatters={
                'x': 'datetime',
                'complete_date': 'datetime'
            }
        )

    def _init_figure(self):
        self.figure = figure(plot_height=600, plot_width=700, title="",
                             toolbar_location='right', x_axis_type='datetime')

        self.figure.circle(x="x", y="y", source=self.source, size=7, line_color=None)  # , fill_alpha="alpha")
        self.figure.add_tools(self.hover)

    def update_data(self, df):
        self.figure.title.text = "%d cases selected" % len(df)
        self.source.data = dict(
            x=pd.to_datetime(df.check_date),
            y=df.waiting_days,
            ID=df.id,
            complete_date=pd.to_datetime(df.complete_date),
        )


class BoxPlot(object):
    def __init__(self):
        self.figure = figure(plot_height=600, plot_width=700, title="",
                             toolbar_location='right', x_axis_type='datetime')

    def update_data(self, df):
        pass
