import dash
from dash import html
from dash import dcc


import pandas as pd

from dash.dependencies import Input, Output

dataset = pd.read_csv("assets/roll_attitude_frequency_sweep.csv")
global intervanRateMs
intervalRateMs = 1000
frameRateHz = 100
timeHistoryToDisplay = 30


app = dash.Dash(__name__, update_title=None) 

pdot = dict({
    "data": [{"x":[],
              "y":[]}],
    "layout" : {"title": {"text": "Roll Acceleration Command"},
               "xaxis": {"title":"Time [s]"},
               "yaxis": {"title":"Roll Acceleration, Rad/s^2"}
               }
            }) 


p = dict({
    "data": [{"x":[],
              "y":[]
              }],
    "layout": {"title": {"text": "Roll Rate"},
               "xaxis": {"title":"Time [s]"},
               "yaxis": {"title":"Roll Rate, Rad/s"}
               }
        })


phiCmd = dict({
    "data": [{"x":[],
              "y":[]
              }],
    "layout": {"title": {"text": "Roll Command"},
               "xaxis": {"title":"Time [s]"},
               "yaxis": {"title":"Roll Command, Rad"}
               }
        })


phiAttitude = dict({
    "data": [{"x":[],
              "y":[]
              }],
    "layout": {"title": {"text": "Roll Attitude"},
               "xaxis": {"title":"Time [s]"},
               "yaxis": {"title":"Roll Attitude, Rad"}
               }
        })


app.layout = html.Div([

    html.Div([
        html.H1("Flight Metrics Logger",
                style={
                    "fontSize": "48px",
                    "color": "Black",
                    "textAlign":"Center"},
                ),

        #### Add Slider for refresh rate
        html.Div([
            html.H6("Data Display Rate, Hz"),
            dcc.Slider(
                id='refresh_slider',
                min=1,
                max=20,
                step=2,
                value=13
                ),
            ]),
        html.Div(id='my-output')

        ]),

    #### Add Checkboxes for selecting different metrics

            #### Ability to overlay on single plot
    

    #### Add Input for file


    #### Anomalous detection
    
    dcc.Graph(id='rollAccelCmd', figure=pdot), 
    dcc.Interval(id="rollAccelCmdInterval",
                interval=intervalRateMs,n_intervals=0),

    dcc.Graph(id='rollRate', figure=p), 
    dcc.Interval(id="rollRateInterval",
                interval=intervalRateMs,n_intervals=0),

    dcc.Graph(id='rollCmd', figure=phiCmd), 
    dcc.Interval(id="rollCmdInterval",
                interval=intervalRateMs,n_intervals=0),

    dcc.Graph(id='rollAttitude', figure=phiAttitude), 
    dcc.Interval(id="rollAttitudeInterval",
                interval=intervalRateMs,n_intervals=0)

    ])

#### GUI interactions ####
@app.callback(
    Output('my-output', 'children'),
    Input('refresh_slider', 'value')
)
def disp_refRate(value):
    return f'Refresh Rate: {value} hZ'







@app.callback(
    Output('rollAccelCmd', 'extendData'),
    [Input('rollAccelCmdInterval', 'n_intervals')]
    )
def update_roll_accel_data(n_intervals):
    index  = int(n_intervals) % len(dataset)
    # tuple is (dict of new data, target trace index, number of points to keep)
    return dict(x=[[dataset['time_s'].values[index]]],
                y=[[dataset['rollAccelerationCommand_rps2'].values[index]]]), [0], frameRateHz*timeHistoryToDisplay
@app.callback(
    Output('rollAccelCmdInterval', 'interval'),
    [Input('refresh_slider', 'value')]
    )
def update_interval(interval):
    intervalRateMs = (1/interval)*1000
    return intervalRateMs
    





@app.callback(
    Output('rollRate', 'extendData'),
    [Input('rollRateInterval', 'n_intervals')]
    )
def update_roll_accel_data(n_intervals):
    index  = int(n_intervals) % len(dataset)
    # tuple is (dict of new data, target trace index, number of points to keep)
    return dict(x=[[dataset['time_s'].values[index]]],
                y=[[dataset['measuredRollRate_rps'].values[index]]]), [0], frameRateHz*timeHistoryToDisplay
@app.callback(
    Output('rollRateInterval', 'interval'),
    [Input('refresh_slider', 'value')]
    )
def update_interval(interval):
    if (1/interval)*1000 != intervalRateMs:
        intervalRateMs = (1/interval)*1000
        return intervalRateMs
    else:
        pass




@app.callback(
    Output('rollCmd', 'extendData'),
    [Input('rollCmdInterval', 'n_intervals')]
    )
def update_roll_accel_data(n_intervals):
    index  = int(n_intervals) % len(dataset)
    # tuple is (dict of new data, target trace index, number of points to keep)
    return dict(x=[[dataset['time_s'].values[index]]],
                y=[[dataset['rollAttitudeCommand_rad'].values[index]]]), [0], frameRateHz*timeHistoryToDisplay
@app.callback(
    Output('rollCmdInterval', 'interval'),
    [Input('refresh_slider', 'value')]
    )
def update_interval(interval):
    if (1/interval)*1000 != intervalRateMs:
        intervalRateMs = (1/interval)*1000
        return intervalRateMs
    else:
        pass




@app.callback(
    Output('rollAttitude', 'extendData'),
    [Input('rollAttitudeInterval', 'n_intervals')]
    )
def update_roll_accel_data(n_intervals):
    index  = int(n_intervals) % len(dataset)
    # tuple is (dict of new data, target trace index, number of points to keep)
    return dict(x=[[dataset['time_s'].values[index]]],
                y=[[dataset['measuredRollAttitude_rad'].values[index]]]), [0], frameRateHz*timeHistoryToDisplay
@app.callback(
    Output('rollAttitudeInterval', 'interval'),
    [Input('refresh_slider', 'value')]
    )
def update_interval(interval):
    if (1/interval)*1000 != intervalRateMs:
        intervalRateMs = (1/interval)*1000
        return intervalRateMs
    else:
        pass




if __name__ == '__main__':
    app.run_server()
