from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.graph_objects as go

import plotly.express as px
from itertools import cycle
palette = cycle(px.colors.qualitative.Plotly)

import numpy as np


def create_ohlc_figure(data_df, underlying):
    fig = go.Figure(data=go.Ohlc(x=data_df.index,
                                 open=data_df['open'],
                                 high=data_df['high'],
                                 low=data_df['low'],
                                 close=data_df['close']))
    fig.update_layout(height=600, width=1600, title_text=f'Live minute {underlying}')
    return fig




def create_quote_signal_figure(data_df, signals_df, strategy_name):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.9, 0.1])
    fig.add_trace(
        go.Scatter(x=data_df.index, y=data_df['close'], name=f'quotes {strategy_name}'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=data_df.index, y=signals_df['value'], name=f'signals {strategy_name}'),
        row=2, col=1
    )
    fig.update_layout(height=600, width=1600, title_text=f'Live strategy {strategy_name}')
    return fig


def plot_multiple_time_series(data_df, error_message='no data available'):
    if data_df is None:
        fig = make_subplots(rows=1, cols=1)
        fig.update_layout(height=600, width=1000, title_text=error_message)
        return fig

    fig = make_subplots(rows=1, cols=1)
    constituents = [col for col in data_df.columns if col not in ['date','Date']]
    for me_constituent in constituents:
        trace_sig = go.Scatter(
            x=data_df.index,
            y=data_df[me_constituent],
            name=me_constituent,
            opacity=0.8)
        fig.append_trace(trace_sig, row=1, col=1)

    fig.update_layout(height=600, width=1600, title_text="Strategy performances",showlegend=True)
    fig.update_xaxes(rangeslider_visible=True)
    return fig

def plot_stacked_bar(data_df, title = ''):

    ts_data=[]
    for col in data_df.columns:
        me_x=list(range(len(data_df.index)))
        me_x=data_df.index
        me_y=data_df[col].values
        #print(me_x)
        #print(me_y)
        ts_data.append(go.Bar(name=col, x=me_x, y=me_y))

    fig = go.Figure(data=ts_data)
    fig.update_layout(barmode='stack', title=title)
    return fig



def plot_regime_close(data_df):
    assert 'regime' in data_df.columns
    assert 'close' in data_df.columns


    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=data_df.index, y=data_df['close'], name='close'),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=data_df.index, y=data_df['regime'], name='regime'),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Double Y Axis Example"
    )

    # Set x-axis title
    fig.update_xaxes(rangeslider_visible=True)
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
    fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)
    return fig






def plot_multiple_time_series(data_df, split =False, logy = True, title = 'Strategy performances', height=600 ,width=1600, put_on_same_scale = True, drop_na_inf = True):
    palette = cycle(px.colors.qualitative.Bold)
#    palette = cycle(px.colors.qualitative.Vivid)
#    palette = cycle(px.colors.qualitative.Safe)
#    data_df[~data_df.isin([np.nan, np.inf, -np.inf]).any(1)] = 0.
    if drop_na_inf:
        data_df.iloc[data_df.isin([np.nan, np.inf, -np.inf]).values] = 0.
    if split:
        fig = make_subplots(rows=1, cols=len(data_df.columns))
        constituents = [col for col in data_df.columns if col not in ['date','Date']]
        counter = 1
        for me_constituent in constituents:
            trace_sig = go.Scatter(
                x=data_df.index,
                y=data_df[me_constituent],
                name=me_constituent,
                opacity=0.8,
                text=me_constituent,
                hoverinfo='text',
                marker_color=next(palette)
            )
            fig.append_trace(trace_sig, row=1, col=counter)
            if logy:
                fig.update_yaxes(title_text="y-axis in logarithmic scale", type="log", row=1, col=counter)
            counter = counter+1

        fig.update_layout(height=height, width=width, title_text=title,showlegend=True)
        fig.update_xaxes(rangeslider_visible=True)
        if put_on_same_scale:
            fig.update_yaxes(range=[data_df[constituents].min().min(), data_df[constituents].max().max()])


        return fig
    else:
        fig = make_subplots(rows=1, cols=1)
        constituents = [col for col in data_df.columns if col not in ['date','Date']]
        for me_constituent in constituents:
            trace_sig = go.Scatter(
                x=data_df.index,
                y=data_df[me_constituent],
                name=me_constituent,
                opacity=0.8,
                text=me_constituent,
                hoverinfo='text',
                marker_color=next(palette)
            )
            fig.append_trace(trace_sig, row=1, col=1)

        if logy:
            fig.update_yaxes(title_text="y-axis in logarithmic scale", type="log", row=1, col=1)
        fig.update_layout(height=height, width=width, title_text=title,showlegend=True)
        fig.update_xaxes(rangeslider_visible=True)
        if put_on_same_scale:
            fig.update_yaxes(range=[data_df[constituents].min().min(), data_df[constituents].max().max()])

        return fig

def plot_multiple_turnover(data_df, ma = None):
    fig = make_subplots(rows=1, cols=1)
    constituents = [col for col in data_df.columns if col not in ['date','Date']]
    for me_constituent in constituents:
        if ma is not None:
            data_df[me_constituent] = data_df[me_constituent].rolling(ma).mean()

        trace_sig = go.Scatter(
            x=data_df.index,
            y=data_df[me_constituent],
            name=me_constituent,
            opacity=0.8)
        fig.append_trace(trace_sig, row=1, col=1)

    fig.update_layout(height=600, width=1600, title_text="Strategy performances",showlegend=True)
    fig.update_xaxes(rangeslider_visible=True)
    return fig


def plot_correlation(data_df):
    static_correlation_df = data_df.corr()

    fig = go.Figure(data=go.Heatmap(
        z=static_correlation_df.values,
        x=static_correlation_df.index,
        y=static_correlation_df.columns,
        colorscale='Viridis'))

    fig.update_layout(
        title='Signal correlation matrix',
        xaxis_nticks=36)
    return fig


