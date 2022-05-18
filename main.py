import dash
import dash_html_components as html
import dash_core_components as dcc


import pandas as pd

from dash.dependencies import Input, Output

dataset = pd.read_csv("assets/roll_attitude_frequency_sweep.csv")

intervalRateMs = 1000
frameRateHz = 100
timeHistoryToDisplay = 30


app = dash.Dash(__name__, update_title=None) 

fig = dict({
    "data": [{"x":[],
              "y":[]}],
    "layout" : {"title": {"text": "Roll Acceleration Command"}}} )

app.layout = html.Div([dcc.Graph(id='rollAccelCmd', figure=fig), 
                       dcc.Interval(id="rollAccelCmdInterval",
                       interval=intervalRateMs,n_intervals=0)])

@app.callback(Output('rollAccelCmd', 'extendData'), [Input('rollAccelCmdInterval', 'n_intervals')])
def update_roll_accel_data(n_intervals):
    index  = int(n_intervals) % len(dataset)
    # tuple is (dict of new data, target trace index, number of points to keep)
    return dict(x=[[dataset['time_s'].values[index]]], y=[[dataset['rollAccelerationCommand_rps2'].values[index]]]), [0], frameRateHz*timeHistoryToDisplay


if __name__ == '__main__':
    app.run_server()
