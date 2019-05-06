import random
import json
import time
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State, Input, Output
import dash_daq as daq

app = dash.Dash(__name__)

# This is for gunicorn
server = app.server

##############################################################################################################
# Side panel
##############################################################################################################

satellite_dropdown = dcc.Dropdown(
    id='satellite-dropdown-component',
    options=[
        {
            'label': 'H45-K1',
            'value': 'h45-k1'
        },
        {
            'label': 'L12-5',
            'value': 'l12-5'
        },
    ],
    clearable=False
)

satellite_dropdown_text = html.P(
    id='satellite-dropdown-text',
    children=['Satellite Dashboard']
)

satellite_title = html.H1(
    id='satellite-name',
    children='')

satellite_body = html.P(
    className='satellite-description',
    id='satellite-description',
    children=['']
)

side_panel_layout = html.Div(
    id='panel-side',
    children=[
        satellite_dropdown_text,
        html.Div(
            id='satellite-dropdown',
            children=satellite_dropdown,
        ),
        html.Div(
            id='panel-side-text',
            children=[
                satellite_title,
                satellite_body
            ]
        )
    ],
)


##############################################################################################################
# Satellite location tracker
##############################################################################################################

# Helper to straighten lines on the map
def flatten_path(xy1, xy2):
    diff_rate = (xy2 - xy1) / 100
    res_list = []
    for i in range(100):
        res_list.append(xy1 + i * diff_rate)
    return res_list


map_data = [
    {
        'type': 'scattergeo',
        'lat': [0],
        'lon': [0],
        'hoverinfo': 'none',
        'mode': 'lines',
        'line': {
            'width': 2,
            'color': '#017e84',
        }
    },
    {
        'type': 'scattergeo',
        'lat': [0],
        'lon': [0],
        'hoverinfo': 'text+lon+lat',
        'text': 'Current Position',
        'mode': 'markers',
        'marker': {
            'size': 10,
            'color': 'black'
        }
    }
]

map_layout = {
    'geo': {
        'showframe': False,
        'showcoastlines': False,
        'showland': True,
        'showocean': True,
        'resolution': 100,
        'landcolor': 'white',
        'oceancolor': '#e8e3df',
        'scope': 'world',
        'showgrid': True,

    },
    'width': 865,
    'height': 610,
    'showlegend': False
}

map_graph = dcc.Graph(
    id='world-map',
    figure={
        'data': map_data,
        'layout': map_layout
    },
    config={
        'displayModeBar': False,
        'scrollZoom': False,
    }
)

##############################################################################################################
# Histogram
##############################################################################################################

histogram = dcc.Graph(
    id='graph-panel',
    figure={
        'data': [{
            'x': [i for i in range(60)],
            'y': [i for i in range(60)],
            'type': 'scatter',
            'marker': {
                'color': 'white',
            }
        }],
        'layout': {
            'title': 'Select A Property To Display',
            'width': 400,
            'height': 350,
            'margin': {
                'l': 35,
                'r': 70,
                't': 100,
                'b': 45
            },
            'xaxis': {
                'dtick': 5,
                'gridcolor': '#999999',
            },
            'yaxis': {
                'gridcolor': '#999999',
            },
            'plot_bgcolor': '#017e84',
            'paper_bgcolor': '#017e84',
            'font': {
                'color': 'white'
            },
        }
    },
    config={
        'displayModeBar': False
    }
)

##############################################################################################################
# Dash_DAQ elements
##############################################################################################################

utc = html.Div(
    id='control-panel-utc',
    children=[
        daq.LEDDisplay(
            id='control-panel-utc-component',
            value='16:23',
            label='Time',
            size=54,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

speed = html.Div(
    id='control-panel-speed',
    children=[
        daq.Gauge(
            id='control-panel-speed-component',
            label='Speed',
            min=0,
            max=40,
            showCurrentValue=True,
            value=27.859,
            units='1000km/h',
            color='#017e84',
            style={
                'color': 'black'
            }
        )
    ],
    n_clicks=0
)

elevation = html.Div(
    id='control-panel-elevation',
    children=[
        daq.Tank(
            id='control-panel-elevation-component',
            label='Elevation',
            min=0,
            max=1000,
            value=650,
            units='kilometers',
            showCurrentValue=True,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

temperature = html.Div(
    id='control-panel-temperature',
    children=[
        daq.Tank(
            id='control-panel-temperature-component',
            label='Temperature',
            min=0,
            max=500,
            value=290,
            units='Kelvin',
            showCurrentValue=True,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

fuel_indicator = html.Div(
    id='control-panel-fuel',
    children=[
        daq.GraduatedBar(
            id='control-panel-fuel-component',
            label='Fuel-Level',
            min=0,
            max=100,
            value=76,
            step=1,
            showCurrentValue=True,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

battery_indicator = html.Div(
    id='control-panel-battery',
    children=[
        daq.GraduatedBar(
            id='control-panel-battery-component',
            label='Battery-Level',
            min=0,
            max=100,
            value=85,
            step=1,
            showCurrentValue=True,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

longitude = html.Div(
    id='control-panel-longitude',
    children=[
        daq.LEDDisplay(
            id='control-panel-longitude-component',
            value='0000.0000',
            label='Longitude',
            size=24,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

latitude = html.Div(
    id='control-panel-latitude',
    children=[
        daq.LEDDisplay(
            id='control-panel-latitude-component',
            value='0050.9789',
            label='Latitude',
            size=24,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

solar_panel_0 = daq.Indicator(
    className='panel-lower-indicator',
    id='control-panel-solar-panel-0',
    label='Solar-Panel-0',
    labelPosition='bottom',
    value=True,
    color='#017e84',
    style={
        'color': '#black'
    }
)

solar_panel_1 = daq.Indicator(
    className='panel-lower-indicator',
    id='control-panel-solar-panel-1',
    label='Solar-Panel-1',
    labelPosition='bottom',
    value=True,
    color='#017e84',
    style={
        'color': '#black'
    }
)

camera = daq.Indicator(
    className='panel-lower-indicator',
    id='control-panel-camera',
    label='Camera',
    labelPosition='bottom',
    value=True,
    color='#017e84',
    style={
        'color': '#black'
    }
)

thrusters = daq.Indicator(
    className='panel-lower-indicator',
    id='control-panel-thrusters',
    label='Thrusters',
    labelPosition='bottom',
    value=True,
    color='#017e84',
    style={
        'color': '#black'
    }
)

motor = daq.Indicator(
    className='panel-lower-indicator',
    id='control-panel-motor',
    label='Motor',
    labelPosition='bottom',
    value=True,
    color='#017e84',
    style={
        'color': '#black'
    }
)

communication_signal = daq.Indicator(
    className='panel-lower-indicator',
    id='control-panel-communication-signal',
    label='Signal',
    labelPosition='bottom',
    value=True,
    color='#017e84',
    style={
        'color': '#black'
    }
)

map_toggle = daq.ToggleSwitch(
    id='control-panel-toggle-map',
    value=True,
    label='Show Satellite Path',
    color='#017e84',
    style={
        'color': '#black'
    }
)

minute_toggle = daq.ToggleSwitch(
    id='control-panel-toggle-minute',
    value=True,
    label='Past Hour - Past Minute',
    color='#017e84',
    style={
        'color': '#black'
    }
)

###############################################################################################################
# Control panel + map
##############################################################################################################
main_panel_layout = html.Div(
    id='panel-upper-lower',
    children=[
        dcc.Interval(
            id='interval',
            interval=1 * 2000,
            n_intervals=0
        ),
        html.Div(
            id='panel-upper',
            children=[
                map_graph,
                histogram,
            ]
        ),
        html.Div(
            id='panel-lower',
            children=[
                html.Div(
                    id='panel-lower-top-break',
                    children=[
                        map_toggle,
                        minute_toggle
                    ]
                ),
                html.Div(
                    id='panel-lower-0',
                    children=[
                        elevation,
                        temperature,
                        speed,
                        utc,
                    ]
                ),
                html.Div(
                    id='panel-lower-1',
                    children=[
                        html.Div(
                            id='panel-lower-led-displays',
                            children=[
                                latitude,
                                longitude,
                            ]
                        ),
                        html.Div(
                            id='panel-lower-indicators',
                            children=[
                                html.Div(
                                    id='panel-lower-indicators-0',
                                    children=[
                                        solar_panel_0,
                                        thrusters,
                                    ]
                                ),
                                html.Div(
                                    id='panel-lower-indicators-1',
                                    children=[
                                        solar_panel_1,
                                        motor,
                                    ]
                                ),
                                html.Div(
                                    id='panel-lower-indicators-2',
                                    children=[
                                        camera,
                                        communication_signal
                                    ]
                                ),
                            ]
                        ),
                        html.Div(
                            id='panel-lower-graduated-bars',
                            children=[
                                fuel_indicator,
                                battery_indicator
                            ]
                        ),
                    ]
                ),
            ]
        )
    ],
)

##############################################################################################################
# Data generation
##############################################################################################################

# Pandas
df_non_gps_h = pd.read_csv('./data/non_gps_data_h.csv')
df_non_gps_m = pd.read_csv('./data/non_gps_data_m.csv')
df_gps_m = pd.read_csv('./data/gps_data_m.csv')
df_gps_h = pd.read_csv('./data/gps_data_h.csv')

# Satellite H45-K1 data
df_non_gps_h_0 = pd.read_csv('./data/non_gps_data_h_0.csv')
df_non_gps_m_0 = pd.read_csv('./data/non_gps_data_m_0.csv')
df_gps_m_0 = pd.read_csv('./data/gps_data_m_0.csv')
df_gps_h_0 = pd.read_csv('./data/gps_data_h_0.csv')

# Satellite L12-5 data
df_non_gps_h_1 = pd.read_csv('./data/non_gps_data_h_1.csv')
df_non_gps_m_1 = pd.read_csv('./data/non_gps_data_m_1.csv')
df_gps_m_1 = pd.read_csv('./data/gps_data_m_1.csv')
df_gps_h_1 = pd.read_csv('./data/gps_data_h_1.csv')

##############################################################################################################
# Root
##############################################################################################################
root_layout = html.Div(
    id='root',
    children=[
        dcc.Store(id='store-placeholder'),
        dcc.Store(id='store-data', data={
            'hour_data': {
                'elevation': [df_non_gps_h['elevation'][i] for i in range(60)],
                'temperature': [df_non_gps_h['temperature'][i] for i in range(60)],
                'speed': [df_non_gps_h['speed'][i] for i in range(60)],
                'latitude': ['{0:09.4f}'.format(df_gps_h['lat'][i]) for i in range(60)],
                'longitude': ['{0:09.4f}'.format(df_gps_h['lon'][i]) for i in range(60)],
                'fuel': [df_non_gps_h['fuel'][i] for i in range(60)],
                'battery': [df_non_gps_h['battery'][i] for i in range(60)],
            },
            'minute_data': {
                'elevation': [df_non_gps_m['elevation'][i] for i in range(60)],
                'temperature': [df_non_gps_m['temperature'][i] for i in range(60)],
                'speed': [df_non_gps_m['speed'][i] for i in range(60)],
                'latitude': ['{0:09.4f}'.format(df_gps_m['lat'][i]) for i in range(60)],
                'longitude': ['{0:09.4f}'.format(df_gps_m['lon'][i]) for i in range(60)],
                'fuel': [df_non_gps_m['fuel'][i] for i in range(60)],
                'battery': [df_non_gps_m['battery'][i] for i in range(60)],
            },
            'hour_data_0': {
                'elevation': [df_non_gps_h_0['elevation'][i] for i in range(60)],
                'temperature': [df_non_gps_h_0['temperature'][i] for i in range(60)],
                'speed': [df_non_gps_h_0['speed'][i] for i in range(60)],
                'latitude': ['{0:09.4f}'.format(df_gps_h_0['lat'][i]) for i in range(60)],
                'longitude': ['{0:09.4f}'.format(df_gps_h_0['lon'][i]) for i in range(60)],
                'fuel': [df_non_gps_h_0['fuel'][i] for i in range(60)],
                'battery': [df_non_gps_h_0['battery'][i] for i in range(60)],
            },
            'minute_data_0': {
                'elevation': [df_non_gps_m_0['elevation'][i] for i in range(60)],
                'temperature': [df_non_gps_m_0['temperature'][i] for i in range(60)],
                'speed': [df_non_gps_m_0['speed'][i] for i in range(60)],
                'latitude': ['{0:09.4f}'.format(df_gps_m_0['lat'][i]) for i in range(60)],
                'longitude': ['{0:09.4f}'.format(df_gps_m_0['lon'][i]) for i in range(60)],
                'fuel': [df_non_gps_m_0['fuel'][i] for i in range(60)],
                'battery': [df_non_gps_m_0['battery'][i] for i in range(60)],
            },
            'hour_data_1': {
                'elevation': [df_non_gps_h_1['elevation'][i] for i in range(60)],
                'temperature': [df_non_gps_h_1['temperature'][i] for i in range(60)],
                'speed': [df_non_gps_h_1['speed'][i] for i in range(60)],
                'latitude': ['{0:09.4f}'.format(df_gps_h_1['lat'][i]) for i in range(60)],
                'longitude': ['{0:09.4f}'.format(df_gps_h_1['lon'][i]) for i in range(60)],
                'fuel': [df_non_gps_h_1['fuel'][i] for i in range(60)],
                'battery': [df_non_gps_h_1['battery'][i] for i in range(60)],
            },
            'minute_data_1': {
                'elevation': [df_non_gps_m_1['elevation'][i] for i in range(60)],
                'temperature': [df_non_gps_m_1['temperature'][i] for i in range(60)],
                'speed': [df_non_gps_m_1['speed'][i] for i in range(60)],
                'latitude': ['{0:09.4f}'.format(df_gps_m_1['lat'][i]) for i in range(60)],
                'longitude': ['{0:09.4f}'.format(df_gps_m_1['lon'][i]) for i in range(60)],
                'fuel': [df_non_gps_m_1['fuel'][i] for i in range(60)],
                'battery': [df_non_gps_m_1['battery'][i] for i in range(60)],
            }

        }),
        # For the case no components were clicked, we need to know what type of graph to preserve
        dcc.Store(id='store-data-config', data={
            'info_type': '',
            'satellite_type': '',
        }),
        # Check which graph should be displayed
        dcc.Store(id='store-previous-states', data={
            'elevation': 0,
            'temperature': 0,
            'speed': 0,
            'latitude': 0,
            'longitude': 0,
            'fuel': 0,
            'battery': 0,
        }
                  ),
        side_panel_layout,
        main_panel_layout
    ]
)

app.layout = root_layout


##############################################################################################################
# Callbacks Data
##############################################################################################################

# Add new data every second/minute
@app.callback(
    Output('store-data', 'data'),
    [Input('interval', 'n_intervals')],
    [State('store-data', 'data')]
)
def update_data(interval, data):
    new_data = data
    # Update H45-K1 data when sat==0, update L12-5 data when sat==1
    for sat in range(2):
        if sat == 0:
            gps_minute_file = df_gps_m_0
            gps_hour_file = df_gps_h_0
        else:
            gps_minute_file = df_gps_m_1
            gps_hour_file = df_gps_h_1
        
        m_data_key = 'minute_data_' + str(sat) 
        h_data_key = 'hour_data_' + str(sat)
        
        new_data[m_data_key]['elevation'].append(data[m_data_key]['elevation'][0])
        new_data[m_data_key]['elevation'] = new_data[m_data_key]['elevation'][1:61]
        new_data[m_data_key]['temperature'].append(data[m_data_key]['temperature'][0])
        new_data[m_data_key]['temperature'] = new_data[m_data_key]['temperature'][1:61]
        new_data[m_data_key]['speed'].append(data[m_data_key]['speed'][0])
        new_data[m_data_key]['speed'] = new_data[m_data_key]['speed'][1:61]
        new_data[m_data_key]['latitude'].append(
            '{0:09.4f}'.format(gps_minute_file['lat'][(60 + interval) % 3600]))
        new_data[m_data_key]['latitude'] = new_data[m_data_key]['latitude'][1:61]
        new_data[m_data_key]['longitude'].append(
            '{0:09.4f}'.format(gps_minute_file['lon'][(60 + interval) % 3600]))
        new_data[m_data_key]['longitude'] = new_data[m_data_key]['longitude'][1:61]

        new_data[m_data_key]['fuel'].append(data[m_data_key]['fuel'][0])
        new_data[m_data_key]['fuel'] = new_data[m_data_key]['fuel'][1:61]
        new_data[m_data_key]['battery'].append(data[m_data_key]['battery'][0])
        new_data[m_data_key]['battery'] = new_data['minute_data_0']['battery'][1:61]

        if interval % 60000 == 0:
            new_data[h_data_key]['elevation'].append(data[h_data_key]['elevation'][0])
            new_data[h_data_key]['elevation'] = new_data[h_data_key]['elevation'][1:61]
            new_data[h_data_key]['temperature'].append(data[h_data_key]['temperature'][0])
            new_data[h_data_key]['temperature'] = new_data[h_data_key]['temperature'][1:61]
            new_data[h_data_key]['speed'].append(data[h_data_key]['speed'][0])
            new_data[h_data_key]['speed'] = new_data[h_data_key]['speed'][1:61]
            new_data[h_data_key]['latitude'].append(
                '{0:09.4f}'.format(gps_hour_file['lat'][interval % 60]))
            new_data[h_data_key]['latitude'] = new_data[h_data_key]['latitude'][1:61]
            new_data[h_data_key]['longitude'].append(
                '{0:09.4f}'.format(gps_hour_file['lon'][interval % 60]))
            new_data[h_data_key]['longitude'] = new_data[h_data_key]['longitude'][1:61]
            new_data[h_data_key]['fuel'].append(data[h_data_key]['fuel'][0])
            new_data[h_data_key]['fuel'] = new_data[h_data_key]['fuel'][1:61]
            new_data[h_data_key]['battery'].append(data[h_data_key]['battery'][0])
            new_data[h_data_key]['battery'] = new_data[h_data_key]['battery']

    return new_data


##############################################################################################################
# Callbacks Histogram
##############################################################################################################

# Update the graph
@app.callback(
    [Output('graph-panel', 'figure'),
     Output('store-previous-states', 'data'),
     Output('store-data-config', 'data')],
    [Input('interval', 'n_intervals'),
     Input('satellite-dropdown-component', 'value'),
     Input('control-panel-toggle-minute', 'value'),
     Input('control-panel-elevation', 'n_clicks'),
     Input('control-panel-temperature', 'n_clicks'),
     Input('control-panel-speed', 'n_clicks'),
     Input('control-panel-latitude', 'n_clicks'),
     Input('control-panel-longitude', 'n_clicks'),
     Input('control-panel-fuel', 'n_clicks'),
     Input('control-panel-battery', 'n_clicks')],
    [State('store-data', 'data'),
     State('store-previous-states', 'data'),
     State('store-data-config', 'data')]
)
def update_graph(interval, satellite_type, minute_mode,
                 elevation_n_clicks, temperature_n_clicks, speed_n_clicks,
                 latitude_n_clicks, longitude_n_clicks, fuel_n_clicks,
                 battery_n_clicks, data, previous_states,
                 data_config):
    # Used to check stuff
    new_data_config = data_config
    info_type = data_config['info_type']
    new_states = previous_states

    # Update store-data-config['satellite_type']
    if satellite_type == 'h45-k1':
        new_data_config['satellite_type'] = 0
    elif satellite_type == 'l12-5':
        new_data_config['satellite_type'] = 1
    else:
        new_data_config['satellite_type'] = None

    # Decide the range of Y given if minute_mode is on
    def set_y_range(data_key):
        if data_key == 'elevation':
            if minute_mode:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'autorange': True
                }
            else:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'range': [0, 1000],
                    'autorange': False
                }

        elif data_key == 'temperature':
            if minute_mode:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'autorange': True
                }
            else:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'range': [0, 500],
                    'autorange': False
                }

        elif data_key == 'speed':
            if minute_mode:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'autorange': True
                }
            else:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'range': [0, 40],
                    'autorange': False
                }

        elif data_key == 'latitude':
            if minute_mode:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'autorange': True
                }
            else:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'range': [-90, 90],
                    'autorange': False,
                    'dtick': 30,
                }

        elif data_key == 'longitude':
            if minute_mode:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'autorange': True
                }
            else:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'range': [0, 360],
                    'autorange': False,
                }

        elif data_key == 'fuel' or data_key == 'battery':
            if minute_mode:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'autorange': True
                }
            else:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'range': [0, 100],
                    'autorange': False
                }

    # Function to update values
    def update_graph_data(data_key):
        string_buffer = ''
        if data_config['satellite_type'] == 0:
            string_buffer = '_0'
        elif data_config['satellite_type'] == 1:
            string_buffer = '_1'

        if minute_mode:
            figure['data'][0]['y'] = list(reversed(data['minute_data' + string_buffer][data_key]))
        else:
            figure['data'][0]['y'] = list(reversed(data['hour_data' + string_buffer][data_key]))

        # Graph title changes depending on graphed data
        figure['layout']['title'] = data_key.capitalize() + ' Histogram'
        return data_key

    # A default figure option to base off everything else from
    figure = {
        'data': [{
            'x': [i for i in range(60)],
            'y': [i for i in range(60)],
            'type': 'scatter',
            'marker': {
                'color': 'white',
            }
        }],
        'layout': {
            'title': 'Select A Propriety To Display',
            'width': 400,
            'height': 350,
            'margin': {
                'l': 35,
                'r': 70,
                't': 100,
                'b': 45
            },
            'xaxis': {
                'dtick': 5,
                'gridcolor': '#999999',
            },
            'yaxis': {
                'gridcolor': '#999999',
            },
            'plot_bgcolor': '#017e84',
            'paper_bgcolor': '#017e84',
            'font': {
                'color': 'white'
            }
        }
    }

    # First pass checks if a component has been selected
    if elevation_n_clicks != previous_states['elevation']:
        new_states['elevation'] += 1
        set_y_range('elevation')
        info_type = update_graph_data('elevation')

    elif temperature_n_clicks != previous_states['temperature']:
        new_states['temperature'] += 1
        set_y_range('temperature')
        info_type = update_graph_data('temperature')

    elif speed_n_clicks != previous_states['speed']:
        new_states['speed'] += 1
        set_y_range('speed')
        info_type = update_graph_data('speed')

    elif latitude_n_clicks != previous_states['latitude']:
        new_states['latitude'] += 1
        set_y_range('latitude')
        info_type = update_graph_data('latitude')

    elif longitude_n_clicks != previous_states['longitude']:
        new_states['longitude'] += 1
        set_y_range('longitude')
        info_type = update_graph_data('longitude')

    elif fuel_n_clicks != previous_states['fuel']:
        new_states['fuel'] += 1
        set_y_range('fuel')
        info_type = update_graph_data('fuel')

    elif battery_n_clicks != previous_states['battery']:
        new_states['battery'] += 1
        set_y_range('battery')
        info_type = update_graph_data('battery')

    # If no component has been selected, check for most recent info_type, to prevent graph from always resetting
    else:
        if info_type in ['elevation', 'temperature', 'speed', 'latitude', 'longitude', 'fuel', 'battery']:
            set_y_range(info_type)
            update_graph_data(info_type)
        return [figure, new_states, new_data_config]
    # Update store-data-config['info_type']
    new_data_config['info_type'] = info_type
    return [figure, new_states, new_data_config]


##############################################################################################################
# Callbacks Dropdown
##############################################################################################################

@app.callback(
    Output('satellite-name', 'children'),
    [Input('satellite-dropdown-component', 'value')]
)
def update_satellite_name(val):
    if val == 'h45-k1':
        return 'Satellite\nH45-K1'
    elif val == 'l12-5':
        return 'Satellite\nL12-5'
    else:
        return ''


@app.callback(
    Output('satellite-description', 'children'),
    [Input('satellite-dropdown-component', 'value')]
)
def update_satellite_description(val):
    if val == 'h45-k1':
        text = 'H45-K1, also known as GPS IIR-9 and GPS SVN-45, is an American navigation satellite which forms part ' \
               'of the Global Positioning System. It was the ninth Block IIR GPS satellite to be launched, out of ' \
               'thirteen in the original configuration, and twenty one overall. It was built by Lockheed Martin, using ' \
               'the AS-4000 satellite bus. -168 was launched at 22:09:01 UTC on 31 March 2003, atop a Delta II carrier ' \
               'rocket, flight number D297, flying in the 7925-9.5 configuration. The launch took place from Space ' \
               'Launch Complex 17A at the Cape Canaveral Air Force Station, and placed H45-K1 into a transfer orbit. ' \
               'The satellite raised itself into medium Earth orbit using a Star-37FM apogee motor.'
        return text

    elif val == 'l12-5':
        text = 'L12-5, also known as NRO Launch 22 or NROL-22, is an American signals intelligence satellite, ' \
               'operated by the National Reconnaissance Office. Launched in 2006, it has been identified as the first ' \
               'in a new series of satellites which are replacing the earlier Trumpet spacecraft. L12-5 was launched ' \
               'by Boeing, using a Delta IV carrier rocket flying in the Medium+(4,2) configuration. The rocket was the ' \
               'first Delta IV to launch from Vandenberg Air Force Base, flying from Space Launch Complex 6, a launch ' \
               'pad originally constructed as part of abandoned plans for manned launches from Vandenberg, originally ' \
               'using Titan rockets, and later Space Shuttles. The launch also marked the first launch of an Evolved ' \
               'Expendable Launch Vehicle from Vandenberg, and the first launch of an NRO payload on an EELV.'
        return text

    else:
        return ''


##############################################################################################################
# Callbacks Map
##############################################################################################################

@app.callback(
    Output('world-map', 'figure'),
    [Input('interval', 'n_intervals'),
     Input('control-panel-toggle-map', 'value'),
     Input('satellite-dropdown-component', 'value')],
    [State('world-map', 'figure'),
     State('store-data', 'data'),
     State('store-data-config', 'data')]
)
def update_word_map(clicks, toggle, satellite_type, old_figure, data, data_config):
    figure = old_figure
    string_buffer = ''

    # Set string buffer as well as drawing the satellite path
    if data_config['satellite_type'] == 0:
        string_buffer = '_0'
        figure['data'][0]['lat'] = [df_gps_m_0['lat'][i] for i in range(3600)]
        figure['data'][0]['lon'] = [df_gps_m_0['lon'][i] for i in range(3600)]

    elif data_config['satellite_type'] == 1:
        string_buffer = '_1'
        figure['data'][0]['lat'] = [df_gps_m_1['lat'][i] for i in range(3600)]
        figure['data'][0]['lon'] = [df_gps_m_1['lon'][i] for i in range(3600)]
    else:
        figure['data'][0]['lat'] = [df_gps_m['lat'][i] for i in range(3600)]
        figure['data'][0]['lon'] = [df_gps_m['lon'][i] for i in range(3600)]

    if clicks % 2 == 0:
        figure['data'][1]['lat'] = [float(data['minute_data' + string_buffer]['latitude'][-1])]
        figure['data'][1]['lon'] = [float(data['minute_data' + string_buffer]['longitude'][-1])]

    # If toggle is off, hide path
    if not toggle:
        figure['data'][0]['lat'] = []
        figure['data'][0]['lon'] = []
    return figure


##############################################################################################################
# Callbacks Components
##############################################################################################################

@app.callback(
    Output('control-panel-utc-component', 'value'),
    [Input('interval', 'n_intervals')],
)
def update_time(interval):
    hour = time.localtime(time.time())[3]
    hour = str(hour).zfill(2)

    minute = time.localtime(time.time())[4]
    minute = str(minute).zfill(2)
    return hour + ':' + minute


@app.callback(
    [Output('control-panel-elevation-component', 'value'),
     Output('control-panel-temperature-component', 'value'),
     Output('control-panel-speed-component', 'value'),
     Output('control-panel-fuel-component', 'value'),
     Output('control-panel-battery-component', 'value')],
    [Input('interval', 'n_intervals'),
     Input('satellite-dropdown-component', 'value')],
    [State('store-data-config', 'data'),
     State('store-data', 'data')]
)
def update_non_gps_component(clicks, satellite_type, data_config, data):
    string_buffer = ''
    if data_config['satellite_type'] == 0:
        string_buffer = '_0'
    if data_config['satellite_type'] == 1:
        string_buffer = '_1'

    new_data = []
    components_list = ['elevation', 'temperature', 'speed', 'fuel', 'battery']

    # Update each graph value
    for component in components_list:
        new_data.append(data['minute_data' + string_buffer][component][-1])

    return new_data


@app.callback(
    [Output('control-panel-latitude-component', 'value'),
     Output('control-panel-longitude-component', 'value')],
    [Input('interval', 'n_intervals'),
     Input('satellite-dropdown-component', 'value')],
    [State('store-data-config', 'data'),
     State('store-data', 'data')]
)
def update_gps_component(clicks, satellite_type, data_config, data):
    string_buffer = ''
    if data_config['satellite_type'] == 0:
        string_buffer = '_0'
    if data_config['satellite_type'] == 1:
        string_buffer = '_1'

    new_data = []
    for component in ['latitude', 'longitude']:
        val = list(data['minute_data' + string_buffer][component][-1])
        if val[0] == '-':
            new_data.append('0' + ''.join(val[1::]))
        else:
            new_data.append(''.join(val))
    return new_data


@app.callback(
    [Output('control-panel-latitude-component', 'color'),
     Output('control-panel-longitude-component', 'color')],
    [Input('interval', 'n_intervals'),
     Input('satellite-dropdown-component', 'value')],
    [State('store-data-config', 'data'),
     State('store-data', 'data')]
)
def update_gps_color(clicks, satellite_type, data_config, data):
    string_buffer = ''
    if data_config['satellite_type'] == 0:
        string_buffer = '_0'
    if data_config['satellite_type'] == 1:
        string_buffer = '_1'

    new_data = []

    for component in ['latitude', 'longitude']:
        value = float(data['minute_data' + string_buffer][component][-1])
        if value < 0:
            new_data.append('#ff8e77')
        else:
            new_data.append('#017e84')

    return new_data


@app.callback(
    Output('control-panel-communication-signal', 'value'),
    [Input('interval', 'n_intervals'),
     Input('satellite-dropdown-component', 'value')]
)
def update_communication_component(clicks, satellite_type):
    if clicks % 2 == 0:
        return False
    else:
        return True


if __name__ == '__main__':
    app.run_server(debug=True)
