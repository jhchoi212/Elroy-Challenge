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
  
    store_data()
        Stores data on clientside for clientside callbacks to use.
        
    update_figures()   **** Clientside Callback
        This function uses the clientside callback to extend figure data faster than a serverside update.
        This is the only clientside callback and is used exclusivly for the 'live-time' stream

  GUI functions:
  
    disp_ref_rate()
        Returns the refresh rate value to an html.Div so the user can see what they have selected
    
    update_interval()
        Updates the dcc.Interval for the clientside callback
        The serverside dcc.Interval is set for 1000ms or 1s
        
  Anomaly Detection functions:
  
    disp_anom()
      Takes user values for maximum
        Roll Acceleration
        Roll Rate
        Roll Attitude
      Calls helper function that finds consecutive datapoints that have an absolute difference greater than the input values
      Returns the first instance of an anomaly detected and displays it on the GUI
  
  Graph dropdown display functions:
  
    dropdown_disp()
      Takes column titles from CSV file and matches it with dcc.Dropdown value to block selective figures from being displayed on the gui
      The graphs not being displayed are still updated so that if the user decided to view another datastream later, the graph is still up to date
      
    pop_snip_i()
      Function return the last 30 seconds of the datastream to the snippit graphs when the current time and the datastream end time are equal
      
    snip_disp_i()
      Using the same method as the dropdown menu, we block or display the snippit graphs depending if the current time matches the dataset end time. 
  
