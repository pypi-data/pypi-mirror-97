from plotly.subplots import make_subplots
from IPython.display import display
import plotly.graph_objs as go
import pandas as pd
import ffn

class Report(object):
  
    def __init__(self, returns, positions, benchmark=None):
        self.returns = returns
        self.positions = positions
        self.benchmark = benchmark
        
    def __repr__(self):
            
        if self.benchmark is not None:
            performance = pd.DataFrame({
              'strategy': self.returns, 
              'benchmark': self.benchmark.dropna()}).dropna().rebase()
        else:
            performance = pd.DataFrame({
              'strategy': self.returns}).dropna().rebase()
        
        return self.create_performance_figure(performance, (self.positions!=0).sum(axis=1))
    
    @staticmethod
    def create_performance_figure(performance_detail, nstocks):

        # plot performance
        def diff(s, period):
            return (s / s.shift(period)-1)

        drawdowns = performance_detail.to_drawdown_series()

        fig = go.Figure(make_subplots(rows=4, cols=1, shared_xaxes=True, row_heights=[2,1,1,1]))
        fig.add_scatter(x=performance_detail.index, y=performance_detail.strategy/100-1, name='strategy', row=1, col=1, legendgroup='performnace', fill='tozeroy')
        fig.add_scatter(x=drawdowns.index, y=drawdowns.strategy, name='strategy - drawdown', row=2, col=1, legendgroup='drawdown', fill='tozeroy')
        fig.add_scatter(x=performance_detail.index, y=diff(performance_detail.strategy, 20), 
                        fill='tozeroy', name='strategy - month rolling return', 
                        row=3, col=1, legendgroup='rolling performance',)

        if 'benchmark' in performance_detail.columns:
            fig.add_scatter(x=performance_detail.index, y=performance_detail.benchmark/100-1, name='benchmark', row=1, col=1, legendgroup='performance', line={'color': 'gray'})
            fig.add_scatter(x=drawdowns.index, y=drawdowns.benchmark, name='benchmark - drawdown', row=2, col=1, legendgroup='drawdown', line={'color': 'gray'})
            fig.add_scatter(x=performance_detail.index, y=diff(performance_detail.benchmark, 20), 
                            fill='tozeroy', name='benchmark - month rolling return', 
                            row=3, col=1, legendgroup='rolling performance', line={'color': 'rgba(0,0,0,0.2)'})


        fig.add_scatter(x=nstocks.index, y=nstocks, row=4, col=1, name='nstocks', fill='tozeroy')
        fig.update_layout(legend={'bgcolor': 'rgba(0,0,0,0)'},
            margin=dict(l=60, r=20, t=40, b=20),
            height=600,
            width=800,
            xaxis4=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                              label="1m",
                              step="month",
                              stepmode="backward"),
                        dict(count=6,
                              label="6m",
                              step="month",
                              stepmode="backward"),
                        dict(count=1,
                              label="YTD",
                              step="year",
                              stepmode="todate"),
                        dict(count=1,
                              label="1y",
                              step="year",
                              stepmode="backward"),
                        dict(step="all")
                    ]),
                    x=0,
                    y=1,
                ),
                rangeslider={'visible': True, 'thickness': 0.1},
                type="date",
            ),
            yaxis={'tickformat':',.0%',},
            yaxis2={'tickformat':',.0%',},
            yaxis3={'tickformat':',.0%',},
          )
        display(fig)
        return ''