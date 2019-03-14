from __future__ import print_function

from bokeh.layouts import layout, column
from bokeh.models import Div
from bokeh.models.widgets import DateRangeSlider, Select, MultiSelect

from plots import *


class Page(object):
    def __init__(self, data, sizing_mode='stretch_both'):
        self.full_data = data
        self.sizing_mode = sizing_mode
        self._init_controls()

        # page components
        self.abstract = ''
        self.control_col = column(*self.controls, sizing_mode=sizing_mode)
        self.scatter_plot = ScatterPlot()
        self.box_plot = BoxPlot()
        self.plot_col = column([self.scatter_plot.figure, self.box_plot.figure], sizing_mode=self.sizing_mode)

        # build layout
        self.layout = layout([
            # [Div(text=self.abstract, sizing_mode=sizing_mode)],
            [self.control_col, self.plot_col]
        ], sizing_mode=self.sizing_mode)

        # init selection
        self.update()

    def _init_controls(self):
        min_date = self.full_data.check_date.min().date()
        max_date = self.full_data.check_date.max().date()

        all_status = list(pd.unique(self.full_data.status)) + ['All']
        all_app_types = list(pd.unique(self.full_data.type)) + ['All']

        self.date_slid = DateRangeSlider(title="Check date range", start=min_date, end=max_date,
                                         value=(min_date, max_date), step=1)
        self.embassy_sel = MultiSelect(title="Embassy", value=['BeiJing'],
                                       options=pd.unique(self.full_data['loc']).tolist())
        self.visa_type_sel = MultiSelect(title="Type of visa", value=['H1'],
                                         options=pd.unique(self.full_data['visa']).tolist())
        self.status_sel = Select(title="Application status", value='All', options=all_status)
        self.app_type_sel = Select(title="Type of application", value='All', options=all_app_types)

        for ctrl in self.controls:
            ctrl.on_change('value', lambda attr, old, new: self.update())

    @property
    def components(self):
        return self.scatter_plot, self.box_plot

    @property
    def controls(self):
        return [self.date_slid, self.embassy_sel, self.visa_type_sel, self.status_sel, self.app_type_sel]

    def update(self):
        selected = self.select_data()
        for ele in self.components:
            ele.update_data(selected)

    def select_data(self):
        date_start, date_end = self.date_slid.value_as_datetime
        emb = set(self.embassy_sel.value)
        vtypes = set(self.visa_type_sel.value)
        status = self.status_sel.value
        atype = self.app_type_sel.value

        selected = self.full_data[
            (pd.to_datetime(self.full_data.check_date).between(date_start, date_end)) &
            (self.full_data['loc'].isin(emb)) &
            (self.full_data.visa.isin(vtypes))
        ]
        if status != "All":
            selected = selected[selected.status == status]
        if atype != "All":
            selected = selected[selected.type == atype]
        return selected
