# -*- coding: utf-8 -*-
import dash
from urllib.request import urlopen
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import plotly.graph_objects as go
import numpy as np

with urlopen('https://raw.githubusercontent.com/SophieNiu/infovisfinal/master/dataset/CleanedData/cleaned-us-115th-congress.geojson') as response:
    counties = json.load(response)
df = pd.read_csv('https://raw.githubusercontent.com/SophieNiu/infovisfinal/master/dataset/CleanedData/Congress_YCOM_2019_Data.csv', dtype={'geoid': int})
df['state_label'] = df['state_label'].apply(lambda x: 'Conneticut' if x == 'Connecticut' else x)

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

df2 = pd.read_csv('https://raw.githubusercontent.com/SophieNiu/infovisfinal/master/dataset/CleanedData/cleaned_district_events.csv')
df2['state'] = df2['state'].apply(lambda x: states[x])
for i in range(0, len(counties['features'])):
    counties['features'][i]['id'] = counties['features'][i]['properties']['geoid']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
available_indicators = df2['event'].unique()
available_indicators2 = df.columns.values

northeast = ['Maine', 'New Hampshire', 'Vermont', 'Massachusetts', 'Rhode Island', 'Conneticut', 'New York', 'New Jersey', 'Pennsylvania']
midwest = ['Ohio', 'Michigan', 'Indiana', 'Wisconsin', 'Illinois', 'Minnesota', 'Iowa', 'Missouri', 'North Dakota', 'South Dakota', 'Nebraska', 'Kansas']
south = ['Delaware', 'Maryland', 'Virginia', 'West Virginia', 'Kentucky', 'North Carolina', 'South Carolina', 'Tennessee', 'Georgia', 'Florida', 'Alabama', 'Mississippi', 'Arkansas', 'Louisiana', 'Texas', 'Oklahoma']
west = ['Montana', 'Idaho', 'Wyoming', 'Colorado', 'New Mexico', 'Arizona', 'Utah', 'Nevada', 'California', 'Oregon', 'Washington', 'Alaska', 'Hawaii']

northeast_dict = {state:'northeast' for state in northeast}
midwest_dict = {state:'midwest' for state in midwest}
south_dict = {state:'south' for state in south}
west_dict = {state:'west' for state in west}

northeast_dict.update(midwest_dict)
northeast_dict.update(south_dict)
northeast_dict.update(west_dict)
states_dict = northeast_dict

common = list(states_dict.keys())

df2 = df2[df2['state'].isin(common)]
df['region'] = df['state_label'].apply(lambda x: states_dict[x])
df2['region'] = df2['state'].apply(lambda x: states_dict[x])

colorsIdx = {'Democratic': 'blue', 'Republican': 'red'}
cols = df['party'].map(colorsIdx)

def title(text):
    if text == 'happening':
        return 'Percent of people who believe climate change is happening'
    elif text == 'happeningOppose':
        return 'Percent of people who believe climate change is not happening'
    else:
        return 'Percent of people who believe climate change is human imposed'

app.layout = html.Div(
    [
        html.Div([html.H1('Climate Change')],style={'text-align': 'center', 'padding-bottom': '30'}),
        html.Div([html.Span('Display: ', className='six columns', style={'text-align': 'right', 'width': '40%', 'padding-top': 10}), dcc.Dropdown(id='value-selected', value='happening', options=[{'label': 'Happening', 'value': 'happening'}, {'label': 'HappeningOppose', 'value': 'happeningOppose'}, {'label': 'Human', 'value': 'human'},{'label': 'HumanOppose', 'value': 'humanOppose'}], style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '70%'}, className='container')], className='row'), dcc.Graph(id='my-graph'),
        html.Div(
            [
                html.Div([html.Div([dcc.Graph(id='northeast-scatter')], className='six columns')]),
                html.Div([html.Div([dcc.Graph(id='midwest-scatter')], className='six columns')]),
                html.Div([html.Div([dcc.Graph(id='south-scatter')], className='six columns')]),
                html.Div([html.Div([dcc.Graph(id='west-scatter')], className='six columns')]),
            ], className='container'),
        html.Div([
            html.Div([dcc.Dropdown(id='value-selected2', value='Congressional District 1 (115th Congress), Alabama', options=[{'label':x, 'value': x} for x in df['GeoName'].values], style={'text-align':'center', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '49%'}), dcc.Graph(id='my-bars')], className='six columns'),
            html.Div([dcc.Dropdown(id='value-selected3', value='Congressional District 1 (115th Congress), Michigan', options=[{'label':x, 'value': x} for x in df['GeoName'].values], style={'text-align':'center', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '49%'}), dcc.Graph(id='my-bars2')], className='six columns')
        ], className='container'),
        html.Div([dcc.Dropdown(id='events-scatter-value',options=[{'label': i, 'value': i} for i in available_indicators],value='Excessive Heat'), html.Div([dcc.Graph(id='events-scatter')], style={'width': '49%', 'display': 'inline-block', 'text-align': 'center'})], className='container', style={'borderBottom': 'thin lightgrey solid','backgroundColor': 'rgb(250, 250, 250)','padding': '10px 5px'})
    ]
)
@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')]
)

def update_figure(selected):

    fig = go.Choroplethmapbox(
        customdata=df,
        geojson=counties, 
        locations=df['geoid'],
        z=df[selected],
        text=df['GeoName'], 
        autocolorscale=False, 
        colorscale='YlGnBu',
        marker={
            'line': {
                'color': 'rgb(250,250,248)',
                'width': 1
            }
        }, 
        colorbar={
            'thickness': 10,
            'len': 0.3,
            'x': 0.9,
            'y': 0.7, 
            'title': {
                'text': title(selected),
                'side': 'top'
            }
        }
    )
    return {
        'data': [fig], 
        'layout': go.Layout(
            mapbox_style='carto-positron', 
            mapbox_zoom=3.25, 
            mapbox_center = {
                'lat': 37.0902, 
                'lon': -95.7129}, 
                title=title(selected), 
                height=800
        )
    }

@app.callback(
    dash.dependencies.Output('my-bars', 'figure'),
    [dash.dependencies.Input('value-selected2', 'value')]
)

def update_bars(selected2):
    dff = df.loc[df['GeoName'] == selected2][['happening', 'happeningOppose', 'affectweather', 'affectweatherOppose', 'harmUS', 'harmUSOppose', 'worried', 'worriedOppose']]
    bars = go.Bar(
        y=list(dff.values[0]),
        x=['happening', 'happeningOppose', 'affectWeather', 'affectWeatherOppose', 'harmUS', 'harmUSOppose', 'worried', 'worriedOppose'],
        orientation='v',
        opacity=0.6
    )
    return {
        'data': [bars]
    }

@app.callback(
    dash.dependencies.Output('my-bars2', 'figure'),
    [dash.dependencies.Input('value-selected3', 'value')]
)

def update_bars(selected3):
    dff = df.loc[df['GeoName'] == selected3][['happening', 'happeningOppose', 'affectweather', 'affectweatherOppose', 'harmUS', 'harmUSOppose', 'worried', 'worriedOppose']]
    bars = go.Bar(
        y=list(dff.values[0]),
        x=['happening', 'happeningOppose', 'affectWeather', 'affectWeatherOppose', 'harmUS', 'harmUSOppose', 'worried', 'worriedOppose'],
        orientation='v',
        opacity=0.6
    )
    return {
        'data': [bars]
    }

@app.callback(
    dash.dependencies.Output('events-scatter', 'figure'),
    [dash.dependencies.Input('events-scatter-value', 'value')])

def update_graph(event):
    return {
        'data': [dict(
            y=df['geoid'].values,
            x=df2[df2['event'] == event]['alerts_total'],
            text=df['party'].values,
            customdata=df2[df2['event'] == event]['districtId'],
            mode='markers',
            marker={
                'color':cols, 
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            title='Events',
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest',
        )
    }

@app.callback(
    dash.dependencies.Output('northeast-scatter', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')])

def update_graph_northeast(selected):
    dff = df[df['region'] == 'northeast'][['geoid', 'party', 'happening', 'happeningOppose', 'human', 'humanOppose', 'GeoName']]
    dff2 = df2[df2['region'] == 'northeast']
    return {
        'data': [dict(
            x=dff2['alerts_total'].values,
            y=dff[selected].values,
            text=dff['GeoName'].values,
            mode='markers',
            marker={
                'color':cols, 
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            title='% Believe {} in the Northeast'.format(selected),
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest',
        )
    }


@app.callback(
    dash.dependencies.Output('midwest-scatter', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')])

def update_graph_midwest(selected):
    dff = df[df['region'] == 'midwest'][['geoid', 'party', 'happening', 'happeningOppose', 'human', 'humanOppose', 'GeoName']]
    dff2 = df2[df2['region'] == 'midwest']
    return {
        'data': [dict(
            x=dff2['alerts_total'].values,
            y=dff[selected].values,
            text=dff['GeoName'].values,
            mode='markers',
            marker={
                'color':cols, 
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            title='% Believe {} in the Midwest'.format(selected),
            color="red",
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest',
        )
    }

@app.callback(
    dash.dependencies.Output('south-scatter', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')])

def update_graph_south(selected):
    dff = df[df['region'] == 'south'][['geoid', 'party', 'happening', 'happeningOppose', 'human', 'humanOppose', 'GeoName']]
    dff2 = df2[df2['region'] == 'south']
    return {
        'data': [dict(
            x=dff2['alerts_total'].values,
            y=dff[selected].values,
            text=dff['GeoName'].values,
            mode='markers',
            marker={
                'color':cols, 
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            title='% Believe {} in the South'.format(selected),
            color="red",
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest',
        )
    }



@app.callback(
    dash.dependencies.Output('west-scatter', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')])

def update_graph_west(selected):
    dff = df[df['region'] == 'west'][['geoid', 'party', 'happening', 'happeningOppose', 'human', 'humanOppose', 'GeoName']]
    dff2 = df2[df2['region'] == 'west']

    return {
        'data': [dict(
            x=dff2['alerts_total'].values,
            y=dff[selected].values,
            text=dff['GeoName'].values,
            mode='markers',
            marker={
                'color':cols, 
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            title='% Believe {} in the West'.format(selected),
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest',
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)