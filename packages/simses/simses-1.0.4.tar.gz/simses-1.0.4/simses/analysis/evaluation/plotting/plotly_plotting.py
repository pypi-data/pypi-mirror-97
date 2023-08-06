from math import ceil, floor

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from simses.analysis.evaluation.plotting.axis import Axis
from simses.analysis.evaluation.plotting.plotter import Plotting


class PlotlyPlotting(Plotting):

    static_figure_index = 1
    __nbins = 100

    class Linestyle:
        DOTTED: str = 'dot'
        SOLID: str = 'solid'
        DASHED: str = 'dash'
        DASH_DOT: str = 'dashdot'

    def __init__(self, title: str, path: str):
        super().__init__()
        self.__title = title
        self.__path = path
        self.__figures: list = list()

    def layout(self, fig, xaxis: Axis, yaxis: [Axis]):
        if len(yaxis) == 1:
            yaxistitle = yaxis[0].label
        else:
            yaxistitle = ""
        fig.layout.title = self.__title
        fig.layout.font = dict(
                family="Times New Roman, monospace",  # TUM Guideline: Helvetica
                size=18,
                # color="#7f7f7f"
            )
        fig.update_layout(
            xaxis_title=xaxis.label,
            yaxis_title=yaxistitle,
            yaxis=dict(
                showexponent='all',
                exponentformat='e'
            ),
            showlegend=True,
            template="none",
        )
        fig.update_xaxes(showgrid=True, gridwidth=2, gridcolor='Lightgray',
                         showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(showgrid=True, gridwidth=2, gridcolor='Lightgray',
                         showline=True, linewidth=2, linecolor='black')

    def lines(self, xaxis: Axis, yaxis: [Axis], secondary=[]):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        self.layout(fig, xaxis, yaxis)
        fig.update_layout(legend=dict(x=0,y=1,traceorder="normal"))

        for i in range(len(yaxis)):
            if i in secondary:
                secondary_y_axis = True
            else:
                secondary_y_axis = False
            fig.add_trace(go.Scatter(
                x=xaxis.data,
                y=yaxis[i].data,
                mode='lines',
                name=yaxis[i].label,
                line=dict(color=yaxis[i].color, dash=yaxis[i].linestyle)
                ), secondary_y=secondary_y_axis
            )
        self.show(fig)

    def get_figures(self) -> list:
        return self.__figures

    # @staticmethod
    # def convert_to_html(figure) -> str:
    #     return figure.to_html(auto_play= False,
    #                           include_plotlyjs=True,
    #                           include_mathjax=False,
    #                           #post_script=plot_id,
    #                           full_html=False,
    #                           #default_height=()),
    #                           validate=True
    #                           )

    def show(self, fig):
        self.__figures.append(fig)
        # pio.write_image(fig,
        #                 self.__path+self.alphanumerize(self.__title)+"_{}.svg".format(Plotting.static_figure_index),
        #                 format='svg',#or 'svg'
        #                 scale=None,#>1 increases resolution
        #                 width=1600,
        #                 height=800,
        #                 validate=True
        #                 )
        self.static_figure_index += 1

    def histogram(self, yaxis: [Axis]):
        cols = ceil(len(yaxis) / 2)
        rows = ceil(len(yaxis) / 2)
        fig = make_subplots(rows=rows, cols=cols)
        for x in range(len(yaxis)):
            ydata = yaxis[x]
            fig.append_trace(go.Histogram(
                x=ydata.data,
                histnorm='percent',
                name=ydata.label,
                nbinsx=self.__nbins,
                marker={"color": ydata.color}
            ), row=floor(x/rows) + 1, col=(x % cols) +1)
        self.layout(fig, xaxis=Axis(data=None, label=None), yaxis=yaxis)
        self.show(fig)

    def bar(self, yaxis: [Axis], bars: int):
        titles = [yaxis[x].label.split(" ", 1)[1] for x in range(0, len(yaxis), bars)]
        cols = ceil(len(yaxis) / bars) # 2 pro row
        rows = ceil(len(yaxis) / (bars + cols))
        fig = make_subplots(rows=rows, cols=cols, subplot_titles=titles)
        for i in range(0, len(yaxis), bars):
            labels = []
            values = []
            colors = []
            for j in range(bars):
                ydata = yaxis[i + j]
                labels.append(ydata.label.split()[0])
                values.append(ydata.data.sum())
                colors.append(ydata.color)
            fig.append_trace(go.Bar(x=labels, y=values, name=titles[floor(i / bars)], marker_color=colors),
                             row=ceil((i + j) / 4), col=ceil((i + j) / 2))
        self.layout(fig, xaxis=Axis(data=None, label=None), yaxis=yaxis)
        fig.update_layout(showlegend=False)
        self.show(fig)

    def subplots(self, xaxis: Axis, yaxis: [Axis]):
        cols = ceil(len(yaxis) / 2)
        rows = ceil(len(yaxis) / 2)
        fig = make_subplots(rows=rows, cols=cols)
        for x in range(len(yaxis)):
            ydata = yaxis[x]
            fig.append_trace(go.Scatter(
                x=xaxis.data,
                y=ydata.data,
                name=ydata.label,
                line=dict(color=ydata.color, dash=ydata.linestyle)
                # line_color=ydata.color,
                # linestyle=ydata.linestyle
            ),
            row=floor(x/rows) + 1, col=(x % cols) +1)
        self.layout(fig, xaxis, yaxis)
        self.show(fig)