import dash
from dash import html
from dash import dcc
import plotly.express as px
import anom_detection


import pandas as pd
import numpy as np

from dash.dependencies import Input, Output, State


#### Dataset saved on server ####
dataset = pd.read_csv("assets/roll_attitude_frequency_sweep.csv")


#initializes app at 1Hz refresh rate
intervalRateMs = 1000



app = dash.Dash(__name__, update_title=None)

def pull_data(data, i=0):
    return data.columns.values[i]



fig_list = {}
figure_containers = []
snips = []


column_names = []


container_names = []
graph_names = []
snip_container = []
snip_names = []
unit_conversion = [' [Degree/second^2]', ' [Degree/second]', ' [Degrees]']

#### Builds figure dictionaries for any input dataset ####
for name in dataset.columns.values:
    unit_index = name.index('_')
    if name[unit_index:] == '_s':
        #### For each column in input data, create a dictionary for that figure
        temp_dict = dict({
                    "data": [{"x":[],
                              "y":[]}],
                    "layout" : {"title": {"text": name},
                               "xaxis": {"title":"Time [s]"},
                               "yaxis": {"title": name}
                               }
                            })
        fig_list[name] = temp_dict
        
    elif name[unit_index:] == '_rps2':
        print(name[:unit_index]+unit_conversion[0])
        #### For each column in input data, create a dictionary for that figure
        temp_dict = dict({
                    "data": [{"x":[],
                              "y":[]}],
                    "layout" : {"title": {"text": name[:unit_index]},
                               "xaxis": {"title":"Time [s]"},
                               "yaxis": {"title": name[:unit_index]+unit_conversion[0]}
                               }
                            })
        snip = dict({
                "data": [{"x": dataset['time_s'][len(dataset)-3001:len(dataset)].values,
                          "y": dataset[name][len(dataset)-3001:len(dataset)].values*(180/3.1415)
                          }],
                "layout": {"title": {"text": "30 Second Snip"},
                           "xaxis": {"title":"Time [s]"},
                           "yaxis": {"title":name[:unit_index]+unit_conversion[0]}
                           }
                    })
        fig_list[name] = temp_dict
        snips.append(snip)
        
    elif name[unit_index:] == '_rps':
        print(name[:unit_index]+unit_conversion[1])
        #### For each column in input data, create a dictionary for that figure
        temp_dict = dict({
                    "data": [{"x":[],
                              "y":[]}],
                    "layout" : {"title": {"text": name[:unit_index]},
                               "xaxis": {"title":"Time [s]"},
                               "yaxis": {"title": name[:unit_index]+unit_conversion[1]}
                               }
                            })
        snip = dict({
                "data": [{"x": dataset['time_s'][len(dataset)-3001:len(dataset)].values,
                          "y": dataset[name][len(dataset)-3001:len(dataset)].values*(180/3.1415)
                          }],
                "layout": {"title": {"text": "30 Second Snip"},
                           "xaxis": {"title":"Time [s]"},
                           "yaxis": {"title":name[:unit_index]+unit_conversion[1]}
                           }
                    })
        fig_list[name] = temp_dict
        snips.append(snip)

    elif name[unit_index:] == '_rad':
        print(name[:unit_index]+unit_conversion[2])
        #### For each column in input data, create a dictionary for that figure
        temp_dict = dict({
                    "data": [{"x":[],
                              "y":[]}],
                    "layout" : {"title": {"text": name[:unit_index]},
                               "xaxis": {"title":"Time [s]"},
                               "yaxis": {"title": name[:unit_index]+unit_conversion[2]}
                               }
                            })
        snip = dict({
                "data": [{"x": dataset['time_s'][len(dataset)-3001:len(dataset)].values,
                          "y": dataset[name][len(dataset)-3001:len(dataset)].values*(180/3.1415)
                          }],
                "layout": {"title": {"text": "30 Second Snip"},
                           "xaxis": {"title":"Time [s]"},
                           "yaxis": {"title":name[:unit_index]+unit_conversion[2]}
                           }
                    })
        fig_list[name] = temp_dict
        snips.append(snip)

        
    #### Creates Ids for the live-time containter and figure
    #### and for the snip containter and figure
    cont = str(name)+'-cont'
    snip_cont = 'snip-'+str(name)+'-cont'
    graph = str(name)+'-graph'
    snip_graph = 'snip-'+str(name)+'-graph'

    #### Appends new ids to lists    
    container_names.append(cont)
    graph_names.append(graph)
    snip_container.append(snip_cont)
    snip_names.append(snip_graph)
    column_names.append(name)

    #### Uses for loop to create the necessary HTML components
    #### Creates a live time Div and graph
    #### Creates a snip Div and graph
    figure_containers.append(html.Div(id=cont,children = [dcc.Graph(id=graph, figure = fig_list[name])],))
    figure_containers.append(html.Div(id=snip_cont,children = [dcc.Graph(id=snip_graph,figure = {})],))




#### Removes Independent variable data
del fig_list[pull_data(dataset,0)]
del figure_containers[0]
del figure_containers[0]
del container_names[0]
del graph_names[0]
del snip_container[0]
del snip_names[0]
del column_names[0]




                             

##############################################################################################################################

#### App Layout for HTML and DCC ####

##############################################################################################################################

app.layout = html.Div([

    
    html.Div([
        html.Header([
                html.H1("Flight Metrics Logger",
                        style={
                            "fontSize": "48px",
                            "color": "Black",
                            "textAlign":"Center",
                            },
                        ),
                    ],
                    style={
                        "padding": '50px',
                        "background":'rgba(255,78,0,0.5)'
                        },
                ),
        ],
    ),

 
    #### Input for Anomaly Detection
    html.Br(),
    html.Div([
        html.H4("Input Vehicle Maximum Roll Rate, Acceleration, Attitude",
                    style={
                        "fontSize": "30px",
                        "color": "Black",
                        "textAlign":"Left"}
                ),
        html.Div([
            html.Div("Enter Maximum Roll Acceleration, Rate, and Attitude"),
            dcc.Input(id='pdot-val', placeholder="Rad per Second Squared"),
            dcc.Input(id='p-val', placeholder="Rad per Second"),
            dcc.Input(id='phi-val', placeholder="Rad"),
                ],
            ),
        html.Br(),
        html.Div(id='anom-time-0', children=''),
        html.Br(),
        html.Div(id='anom-time-1', children=''),
        html.Br(),
        html.Div(id='anom-time-2', children=''),
        html.Br(),
        
        html.Button('Run Anomaly Detection', id='run-anom', n_clicks=0),
        
        ],
    ),

    
    #### Add Slider for refresh rate
    html.Br(),
    html.Div([
        html.Div([
            html.H3("Data Display Rate, Hz",
                    style={
                        "fontSize": "30px",
                        "color": "Black",
                        "textAlign":"Center"}
            ),
            dcc.Slider(
                id='refresh_slider',
                min=1,
                max=100,
                step=3,
                value=1,
                ),
            ]),
        html.Div(id='my-output'),
        html.Div(id='time'),
        ],
    ),



    #### Add Checkboxes for selecting different metrics
    html.Br(),
    html.Div([
        html.H3("Select Data to be Displayed",
                style={
                    "fontSize": "30px",
                    "color": "Black",
                    "textAlign":"Center"}
                ),
        dcc.Dropdown(
                column_names+['Display All', 'None'],
                'Display All',
                id='dropdown',
            ),
        ],
    ),

    #### Paramter Graphs ####
    html.Div([
        dcc.Store(id='input-data', data = {}),
        dcc.Store(id='column-names', data = column_names),
        dcc.Store(id='snip-store', data = []),
        html.Div(id='live-graphs',
                 children = figure_containers,
                 ),
        
        dcc.Interval(id="refreshInterval",
                    interval=intervalRateMs,n_intervals=0),
        
        ],
    ),

    
    #### Serverside Updates ####
    dcc.Interval(id='serverside-interval',
                 interval = 1000,
                 n_intervals = 1
                 ),


    ],
)



##############################################################################################################################

#### Update graphs via clientside callback ####

##############################################################################################################################

@app.callback(
    Output('input-data', 'data'),
    Input('serverside-interval', 'n_intervals'),
    )
def store_data(n_intervals):
    last_row = n_intervals*100
    stored_data = dataset.iloc[0:last_row]
    return stored_data.to_dict('records')    ## Data stored in Radians ##
##
##app.clientside_callback(
##     """
##     function(n_intervals, data, name) {
##         return [
##         [{x: [[data[n_intervals]['time_s']]], y: [[data[n_intervals][name[0]]*(180/3.1415)]]}, [0], 3000],
##         [{x: [[data[n_intervals]['time_s']]], y: [[data[n_intervals][name[1]]*(180/3.1415)]]}, [0], 3000],
##         [{x: [[data[n_intervals]['time_s']]], y: [[data[n_intervals][name[2]]*(180/3.1415)]]}, [0], 3000],
##         [{x: [[data[n_intervals]['time_s']]], y: [[data[n_intervals][name[3]]*(180/3.1415)]]}, [0], 3000]
##         ]
##             
##     }
##     """,
##     [Output(graph_names[0], 'extendData'),
##      Output(graph_names[1], 'extendData'),
##      Output(graph_names[2], 'extendData'),
##      Output(graph_names[3], 'extendData'),],
##     Input('refreshInterval','n_intervals'),
##     State('input-data', 'data'),
##     State('column-names', 'data'),
##)

app.clientside_callback(
    """
    function(n_intervals, data) {
        return data[n_intervals]['time_s']
    }
    """,
    Output('time', 'children'),
    Input('refreshInterval','n_intervals'),
    State('input-data', 'data'),
)

##############################################################################################################################

#### GUI interactions ####

##############################################################################################################################


## Displays refresh rate ##
@app.callback(
    [Output('my-output', 'children'),
     Output('refreshInterval', 'interval')
     ],
    Input('refresh_slider', 'value')
)
def disp_ref_rate(value):
    clientInterval = (1/value)*1000
    return [f'Refresh Rate: {value} hZ', clientInterval]




##############################################################################################################################

#### Anomaly Detection ####

##############################################################################################################################



#### Anom Detection ####
@app.callback(
    [Output('anom-time-0', 'children'),
    Output('anom-time-1', 'children'),
    Output('anom-time-2', 'children'),],
    Input('run-anom', 'n_clicks'),
    State('pdot-val','value'),
    State('p-val','value'),
    State('phi-val','value'),
    
    )
def disp_anom(n_clicks, pdot_value, p_value, phi_value):
    anom_time_1 = []
    anom_time_2 = []
    anom_time_3 = []
    if n_clicks > 0:
        for name in column_names:
           anom_time_1.append(anom_detection.anomDetect(dataset[name], float(pdot_value))[0])
           anom_time_2.append(anom_detection.anomDetect(dataset[name], float(p_value))[0])
           anom_time_3.append(anom_detection.anomDetect(dataset[name], float(phi_value))[0])
           
        return [f'Roll Acceleration Anomaly detected at: {anom_time_1[0]/100} s',
                f'Roll Rate Anomaly detected at: {anom_time_2[1]/100} s',
                f'Roll Attitude Anomaly detected at: {anom_time_3[2]/100} s']
    else:
        return n_clicks



##############################################################################################################################

#### Graph Display Dropdown ####
#### Blocks not chosen graphs, displays chosen ones ####

##############################################################################################################################



## Disp Container selection ##
@app.callback(
    [Output(container_names[0], 'style'),
    Output(container_names[1], 'style'),
    Output(container_names[2], 'style'),
    Output(container_names[3], 'style'),
     ],
    Input('dropdown', 'value'),
    )
def dropdown_Disp(dropdown_val):
    if dropdown_val == str(column_names[0]):
        return [{'display':'block'}, {'display':'none'}, {'display':'none'}, {'display':'none'}]
    elif dropdown_val == str(column_names[1]):
        return [{'display':'none'}, {'display':'block'}, {'display':'none'}, {'display':'none'}]
    elif dropdown_val == str(column_names[2]):
        return [{'display':'none'}, {'display':'none'}, {'display':'block'}, {'display':'none'}]
    elif dropdown_val == str(column_names[3]):
        return [{'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'block'}]
    elif dropdown_val == 'Display All':
        return [{'display':'block'}, {'display':'block'}, {'display':'block'}, {'display':'block'}]
    else:
        return [{'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}]




##############################################################################################################################

#### Displays last 30 seconds of data ####
#### Hides graph/figure until end time is reached ####

##############################################################################################################################

#### last 30 second snip and display ####
@app.callback(
    Output(snip_names[0],'figure'),
    Input('serverside-interval', 'n_intervals'),
    Input('serverside-interval', 'interval'),
    )
def pop_snip_0(n_intervals, interval):
    data_len = len(dataset)
    stopTime = dataset['time_s'][data_len-1]
    currentTime = (n_intervals*interval)/1000

    if currentTime == stopTime:
        return snips[0]
    else:
        return dict()


#### last 30 second snip and display ####
@app.callback(
    Output(snip_names[1],'figure'),
    Input('serverside-interval', 'n_intervals'),
    Input('serverside-interval', 'interval'),
    )
def pop_snip_1(n_intervals, interval):
    data_len = len(dataset)
    stopTime = dataset['time_s'][data_len-1]
    currentTime = (n_intervals*interval)/1000

    if currentTime == stopTime:
        return snips[1]
    else:
        return dict()


#### last 30 second snip and display ####
@app.callback(
    Output(snip_names[2],'figure'),
    Input('serverside-interval', 'n_intervals'),
    Input('serverside-interval', 'interval'),
    )
def pop_snip_2(n_intervals, interval):
    data_len = len(dataset)
    stopTime = dataset['time_s'][data_len-1]
    currentTime = (n_intervals*interval)/1000

    if currentTime == stopTime:
        return snips[2]
    else:
        return dict()


#### last 30 second snip and display ####
@app.callback(
    Output(snip_names[3],'figure'),
    Input('serverside-interval', 'n_intervals'),
    Input('serverside-interval', 'interval'),
    )
def pop_snip_3(n_intervals, interval):
    data_len = len(dataset)
    stopTime = dataset['time_s'][data_len-1]
    currentTime = (n_intervals*interval)/1000

    if currentTime == stopTime:
        return snips[3]
    else:
        return dict()


@app.callback(
    [Output(snip_container[0], 'style'),
    Output(snip_container[1], 'style'),
    Output(snip_container[2], 'style'),
    Output(snip_container[3], 'style'),
    ],
    Input('serverside-interval', 'n_intervals'),
    Input('serverside-interval', 'interval'),
    )
def snip_disp(n_intervals, interval):
    data_len = len(dataset)
    stopTime = dataset['time_s'][data_len-1]
    currentTime = (n_intervals*interval)/1000

    if currentTime == stopTime:
        return [{'display':'block'}, {'display':'block'}, {'display':'block'}, {'display':'block'}]
    else:
         return [{'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}]
    
    





if __name__ == '__main__':
    app.run_server()
