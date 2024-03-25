import dash
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
df = pd.read_csv("https://raw.githubusercontent.com/daniguariso/HMT_Proposal/main/Data%20Proposal/Indicator_Data.csv")


app.layout = html.Div([
    html.Div([

        html.Div(["SDG",
            dcc.Dropdown(
                df['SDG Description'].unique(),
                'SDG 1: End poverty in all its forms everywhere',
                id='crossfilter-sdg'
            )], style={'fontSize': 17}),
        html.Div(["SDG Target",
            dcc.Dropdown(
                df['SDG Target Description'].unique(),
                'SDG Target 1.4: By 2030, ensure that all men and women, in particular the poor and the vulnerable, have equal rights to economic resources, as well as access to basic services, ownership and control over land and other forms of property, inheritance, natural resources, appropriate new technology and financial services, including microfinance',
                id='crossfilter-xaxis-column'
            )], style={'fontSize': 15}),
        html.Div(["SDG Indicator",
            dcc.Dropdown(
                df['SDG Indicator Description'].unique(),
                'Proportion of total adult population with secure tenure rights to land, with legally recognized documentation',
                id='crossfilter-sdg-indicator'
            )], style={'fontSize': 14})
        ]),

    html.Div([
         html.Div(dcc.Graph(id='x-time-series'),style={'display': 'inline-block'}),
         html.Div(dcc.Graph(id='y-time-series'), style={'display': 'inline-block'})
    ]),

])


def create_time_series(dff, title, ylabel, sdg_color):

    fig = px.scatter(dff, x='Year', y=ylabel)

    fig.update_traces(mode='lines+markers', marker=dict(color=sdg_color))

    fig.update_xaxes(showgrid=False)

    fig.add_annotation(font=dict(size=14), y=1.1, xref='paper', yref='paper', showarrow=False, align='center',
                       text=title)

  #  fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@callback(
    Output("crossfilter-xaxis-column", "options"),
    Input("crossfilter-sdg", "value")
)
def update_options_1(value_1):
    if not value_1:
        return dash.no_update
    return [o for o in df[df['SDG Description'] == value_1]['SDG Target Description'].unique()]

@callback(
    Output("crossfilter-sdg-indicator", "options"),
    Input("crossfilter-xaxis-column", "value")
)
def update_options_2(value_2):
    if not value_2:
        return dash.no_update
    return [o for o in df[df['SDG Target Description'] == value_2]['SDG Indicator Description'].unique()]


@callback(
    Output('x-time-series', 'figure'),
#    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-sdg-indicator', 'value'))

def update_x_timeseries(sdg_ind):
#    sdg_target = xaxis_column_name
    dff = df[df['SDG Indicator Description'] ==  sdg_ind]
#    dff = dff["Normalized Indicator"]
#    sdg_target_des = df[df['SDG Target Description'] == sdg_target]["SDG Indicator Description"].unique()[0]
    title = 'SDG Indicator Trend'
    ylabel = 'Normalized Indicator'
    sdg_color = df[df['SDG Indicator Description'] == sdg_ind]["Colour"].unique()[0]
    return create_time_series(dff, title, ylabel, sdg_color)


@callback(
    Output('y-time-series', 'figure'),
 #   Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-sdg-indicator', 'value'))

def update_y_timeseries(sdg_ind):
 #   sdg_target = xaxis_column_name
    dff = df[df['SDG Indicator Description'] ==  sdg_ind]
#    dff = dff["Budget Percentage"]
    title = 'Government Expenditure Trend'
    ylabel = 'Budget Percentage'
    sdg_color = df[df['SDG Indicator Description'] == sdg_ind]["Colour"].unique()[0]
    return create_time_series(dff, title, ylabel, sdg_color)


if __name__ == '__main__':
    app.run(debug=True)