2022 Elroy Air Airborne Systems Engineer Challenge

Submission by Jonathan Choi


Table of Contents

1. App layout and Input Processing
3. Callbacks and functions
4. Helper File
5. Current Issues and Works in Progress



1:App Layout

The following flight metrics logger is laid out using the Dash Library

The flight metrics logger currently displays 4 input data streams from the given csv file.
    Roll Acceleration, in radians per second squared
    Roll Rate, in radians per second
    Roll Attitude Command, in radians
    Roll Attitude Measured, in radians
    
Furthermore, when the datastream has rached its end, the logger will display the last 30 seconds of each data stream on its own respective graph separate from the 'live stream' graphs.

The app contains functions to:   
  isolate anomalies in data, given user input for threshold values on the vehicles maximum maneuvering values,
      (Found in the helper file called anom_datectionm and in anom detection section)
      (anom_detection.py and lines 306-339)
      
  increase or decrease 'live stream' rate or more specifically increase or decrease the refresh rate of the updating date,
      (Found in GUI interaction section, and in Update graphs section)
      (Lines 241-303)
      
  and the ability to select single parameters to display, or to display all.
      (Found in graph Display Dropdown)
      (lines 343-506)

Furthermore, before the actual dash app starts running, the input data is sorted and separated into singular input parameters.
    This means that independent of the input data, the app is able to display any given 4 parameters. 
    (lines 32-104)
    

2:Callbacks and Functions

Two types of callbacks were used:
    @app.callback(),
    app.clientside_callback().
    
The general @app.callbacks were used to update low refresh rate aspects such as:
    anomaly detection,
    last 30 second snippit display, 
    value displays such as refresh rate
    
The app.clientside_callback was used for aspects that needed quicker response times such as the 'live-stream' figure displays.
    Clientside callbacks store data and execute functions on the browser/clientside. 
    This reduces the time needed to execute functions as the request does not need to bounce between client and server.

Functions in use:

  Data Stream functions:
  1:
  
    @app.callback(
    Output('input-data', 'data'),
    Input('serverside-interval', 'n_intervals'),
    )
        def store_data(n_intervals):
            last_row = n_intervals*100
            stored_data = dataset.iloc[0:last_row]
            return stored_data.to_dict('records')    ## Data stored in Radians ##
            
        ## Stores Data on clientside for faster execution

        app.clientside_callback(
             """
             update_figures(n_intervals, data, name) {
                 return [
                 [{x: [[data[n_intervals]['time_s']]], y: [[data[n_intervals][name[0]]]]}, [0], 3000],
                 [{x: [[data[n_intervals]['time_s']]], y: [[data[n_intervals][name[1]]]]}, [0], 3000],
                 [{x: [[data[n_intervals]['time_s']]], y: [[data[n_intervals][name[2]]]]}, [0], 3000],
                 [{x: [[data[n_intervals]['time_s']]], y: [[data[n_intervals][name[3]]]]}, [0], 3000]
                 ]
                 
            ## This function uses the clientside callback to extend figure data faster than a serverside update.
            ## This is the only clientside callback and is used exclusivly for the 'live-time' stream

             }
             """,
             [Output(graph_names[0], 'extendData'),
              Output(graph_names[1], 'extendData'),
              Output(graph_names[2], 'extendData'),
              Output(graph_names[3], 'extendData'),],
             Input('refreshInterval','n_intervals'),
             State('input-data', 'data'),
             State('column-names', 'data'),
        )


  GUI functions:
  1:
  
    ## Displays refresh rate ##
    @app.callback(
        Output('my-output', 'children'),
        Input('refresh_slider', 'value')
    )
    def disp_ref_rate(value):
        return f'Refresh Rate: {value} hZ'
        
    ##  Returns the refresh rate value to an html.Div so the user can see what they have selected



  2:
  
    ## Slider to select refresh rate ##
    @app.callback(
        Output('refreshInterval', 'interval'),
        Input('refresh_slider', 'value'),
        )
    def update_interval(interval):
        intervalRateMs = (1/interval)*1000
        return intervalRateMs

    ##  Updates the dcc.Interval for the clientside callback
    ##  The serverside dcc.Interval is set for 1000ms or 1s
        
  Anomaly Detection functions:
  
  1:
  
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
      
    ##  Takes user values for maximum
        ##  Roll Acceleration
        ##  Roll Rate
        ##  Roll Attitude
    ##  Calls helper function that finds consecutive datapoints that have an absolute difference greater than the input values
    ##  Returns the first instance of an anomaly detected and displays it on the GUI
  
  Graph dropdown display functions:
  1:
  
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
            
      ##  Takes column titles from CSV file and matches it with dcc.Dropdown value to block selective figures from being displayed on the gui
      ##  The graphs not being displayed are still updated so that if the user decided to view another datastream later, the graph is still up to date
      
  2:
      
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
            
     ##  Function return the last 30 seconds of the datastream to the snippit graphs when the current time and the datastream end time are equal

  3:

    @app.callback(
        [Output(snip_container[0], 'style'),
        Output(snip_container[1], 'style'),
        Output(snip_container[2], 'style'),
        Output(snip_container[3], 'style'),
        ],
        Input('serverside-interval', 'n_intervals'),
        Input('serverside-interval', 'interval'),
        )
    def snip_Disp(n_intervals, interval):
        data_len = len(dataset)
        stopTime = dataset['time_s'][data_len-1]
        currentTime = (n_intervals*interval)/1000

        if currentTime == stopTime:
            return [{'display':'block'}, {'display':'block'}, {'display':'block'}, {'display':'block'}]
        else:
             return [{'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}]
             
     ##  Using the same method as the dropdown menu, we block or display the snippit graphs depending if the current time matches the dataset end time. 
  
