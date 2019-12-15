# -*- coding: utf-8 -*-
import dash
from urllib.request import urlopen
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import plotly.graph_objects as go
import numpy as np
import copy

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

northeast_dict = {state:'Northeast' for state in northeast}
midwest_dict = {state:'Midwest' for state in midwest}
south_dict = {state:'South' for state in south}
west_dict = {state:'West' for state in west}

northeast_dict.update(midwest_dict)
northeast_dict.update(south_dict)
northeast_dict.update(west_dict)
states_dict = northeast_dict

common = list(states_dict.keys())

df2 = df2[df2['state'].isin(common)]
df['region'] = df['state_label'].apply(lambda x: states_dict[x])
df2['region'] = df2['state'].apply(lambda x: states_dict[x])

colorsIdx = {'Democratic': 'blue', 'Republican': 'red'}
colorsNum = {'Democratic': 0, 'Republican': 1}
cols = df['party'].map(colorsIdx)
p_num = df['party'].map(colorsNum)

df_region = df.groupby('region').mean().reset_index()[['region', 'happening', 'happeningOppose', 'affectweather', 'affectweatherOppose', 'harmUS', 'harmUSOppose', 'worried', 'worriedOppose']]
new = pd.merge(df2, df, left_on='districtId', right_on='geoid', how= 'right')

def get_county(geoid):
    for i in counties['features']:
        if i['id'] == geoid:
            return i

app.layout = html.Div(
    [
        html.Div([html.H1('What Factors Influence Climate Change Beliefs?')],style={'text-align': 'center', 'padding-bottom': '30'}),
        html.Div([html.H2('Do Frequent Weather Events Influence Climate Beliefs?')],style={'text-align': 'center', 'padding-bottom': '30'}),
        html.Div([html.P('''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ullamcorper gravida lorem finibus lobortis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. 
            Quisque tristique hendrerit metus ut hendrerit. Suspendisse id fringilla ipsum. Vivamus rutrum turpis eu arcu lacinia malesuada. Morbi a metus sit amet enim venenatis interdum. Donec faucibus dui vestibulum 
            eros interdum, ac lobortis diam finibus. Fusce malesuada mauris hendrerit tellus fringilla tempus. Ut iaculis mattis justo, ac malesuada dolor porta vitae. Cras viverra erat eu quam placerat, ut tempor justo suscipit. 
            Mauris in odio suscipit elit ultricies placerat et et ante. Nullam eget purus eu leo placerat placerat.''',  style={'marginTop': 100, 'text-align':'center', 'padding':'30'},)]),
        html.Div([
            html.P('''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ullamcorper gravida lorem finibus lobortis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. 
            Quisque tristique hendrerit metus ut hendrerit. Suspendisse id fringilla ipsum. Vivamus rutrum turpis eu arcu lacinia malesuada. Morbi a metus sit amet enim venenatis interdum. Donec faucibus dui vestibulum 
            eros interdum, ac lobortis diam finibus. Fusce malesuada mauris hendrerit tellus fringilla tempus. Ut iaculis mattis justo, ac malesuada dolor porta vitae. Cras viverra erat eu quam placerat, ut tempor justo suscipit. 
            Mauris in odio suscipit elit ultricies placerat et et ante. Nullam eget purus eu leo placerat placerat.''',  style={'marginTop': 100}, className='four columns'), 
            dcc.Graph(id='matt-graph', className='eight columns', config={'displayModeBar':False})
        ], className='container'),
        html.Div([dcc.Graph(id='ben-graph', className='nine columns'),
            html.P('''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ullamcorper gravida lorem finibus lobortis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. 
            Quisque tristique hendrerit metus ut hendrerit. Suspendisse id fringilla ipsum. Vivamus rutrum turpis eu arcu lacinia malesuada. Morbi a metus sit amet enim venenatis interdum. Donec faucibus dui vestibulum 
            eros interdum, ac lobortis diam finibus. Fusce malesuada mauris hendrerit tellus fringilla tempus. Ut iaculis mattis justo, ac malesuada dolor porta vitae. Cras viverra erat eu quam placerat, ut tempor justo suscipit. 
            Mauris in odio suscipit elit ultricies placerat et et ante. Nullam eget purus eu leo placerat placerat.''',  style={'marginTop': 100}, className='three columns')
        ], className='container'),
        html.Div([
            html.P('''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ullamcorper gravida lorem finibus lobortis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. 
            Quisque tristique hendrerit metus ut hendrerit. Suspendisse id fringilla ipsum. Vivamus rutrum turpis eu arcu lacinia malesuada. Morbi a metus sit amet enim venenatis interdum. Donec faucibus dui vestibulum 
            eros interdum, ac lobortis diam finibus. Fusce malesuada mauris hendrerit tellus fringilla tempus. Ut iaculis mattis justo, ac malesuada dolor porta vitae. Cras viverra erat eu quam placerat, ut tempor justo suscipit. 
            Mauris in odio suscipit elit ultricies placerat et et ante. Nullam eget purus eu leo placerat placerat.''',  style={'marginTop': 100}, className='four columns'), 
            dcc.Graph(id='ben-graph2', className='eight columns', config={'displayModeBar':False})
        ], className='container'),
        # html.Div([dcc.Graph(id='ben-graph2', className='nine columns'),
        #     html.P('''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ullamcorper gravida lorem finibus lobortis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. 
        #     Quisque tristique hendrerit metus ut hendrerit. Suspendisse id fringilla ipsum. Vivamus rutrum turpis eu arcu lacinia malesuada. Morbi a metus sit amet enim venenatis interdum. Donec faucibus dui vestibulum 
        #     eros interdum, ac lobortis diam finibus. Fusce malesuada mauris hendrerit tellus fringilla tempus. Ut iaculis mattis justo, ac malesuada dolor porta vitae. Cras viverra erat eu quam placerat, ut tempor justo suscipit. 
        #     Mauris in odio suscipit elit ultricies placerat et et ante. Nullam eget purus eu leo placerat placerat.''', style={'marginTop': 100}, className='three columns')
        # ], className='container'),
        html.Div(
            [
                dcc.Graph(id='northeast-scatter', className='three columns'),
                dcc.Graph(id='midwest-scatter', className='three columns'),
                dcc.Graph(id='south-scatter', className='three columns'),
                dcc.Graph(id='west-scatter', className='three columns')
            ], className='row'),
        html.Br(),
        html.Br(),
        html.Div([html.H2('How do opinions differ by region?')],style={'text-align': 'center', 'padding-bottom': '30'}),
        html.Br(),
        html.Div([
            html.Div([dcc.Dropdown(id='value-selected-region1', value='Northeast', options=[{'label':x, 'value': x} for x in df_region['region'].values], style={'text-align':'center', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '70%'}), dcc.Graph(id='my-bars3')], className='six columns'),
            html.Div([dcc.Dropdown(id='value-selected-region2', value='Midwest', options=[{'label':x, 'value': x} for x in df_region['region'].values], style={'text-align':'center', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '70%'}), dcc.Graph(id='my-bars4')], className='six columns')
        ], className='container'),
        html.Br(),
        html.Div([html.H2('How do opinions differ by district?')],style={'text-align': 'center', 'padding-bottom': '30'}),
        html.Br(),
        html.Div([
            html.Div([dcc.Dropdown(id='value-selected2', value='Congressional District 1 (115th Congress), Alabama', options=[{'label':x, 'value': x} for x in df['GeoName'].values], style={'text-align':'center', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '100%'}), dcc.Graph(id='my-bars')], className='six columns'),
            html.Div([dcc.Dropdown(id='value-selected3', value='Congressional District 1 (115th Congress), Michigan', options=[{'label':x, 'value': x} for x in df['GeoName'].values], style={'text-align':'center', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '100%'}), dcc.Graph(id='my-bars2')], className='six columns')
        ], className='container'),
        html.Br(),
        html.Div([dcc.Dropdown(id='value-selected', value='happening', options=[{'label': 'How many people believe climate change is happening?', 'value': 'happening'}, {'label': 'How many people don\'t believe climate change is happening?', 'value': 'happeningOppose'}, {'label': 'How many people believe climate change is caused by humans?', 'value': 'human'},{'label': 'How many people don\'t believe climate change is caused by humans?', 'value': 'humanOppose'}], style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '70%'}, className='container')], className='row'), dcc.Graph(id='my-graph'),
        html.Br(),
        html.Div([dcc.Graph(id='events-scatter', className='container')])
    ]
)

@app.callback(
    dash.dependencies.Output('matt-graph', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')]
)

def update_figure(selected):
    # county = [get_county(x) for x in [2611,2612]]
    county = copy.deepcopy(counties)
    county['features'] = [i for i in county['features'] if i['id'] in [2611,2612]]
    # name = df[df['geoid'] == county['id']]['GeoName'].values[:]
    newdf = df[df['geoid'].isin([2611,2612])]
    # county_id = df[df['geoid'].isin([2611,2612])]['GEOID']
    # county_index = county_id.index
    # opacity = df[selected][county_index] * .01
    opacity = newdf['happening'].values * .01
    # custom_df = df[df.index == county_index]
    # color=df[df.index == county_index]
    # print(name, '\n', county_id, '\n', county_index, '\n', opacity, '\n', custom_df)
    colorsIdx = {'Democratic': 'blue', 'Republican': 'red'}
    colorsNum = {'Democratic': 0, 'Republican': 1}
    cols = newdf['party'].map(colorsIdx)
    p_num = newdf['party'].map(colorsNum)
    my_text = [n + "<br>Happening: " + str(h) for n, h in zip(list(newdf['GeoName']),list(newdf['happening']))]
    fig = go.Choroplethmapbox(
        # colorscale = 'Reds',
        showscale=False,
        customdata=newdf,
        geojson=county, 
        locations=newdf['GEOID'],
        z=p_num,
        text=my_text,
        # text=newdf['GeoName'],
        # hovertemplate= "%{text}<br>Happening: %{customdata['happening']}",
        autocolorscale=False,
        marker_opacity=opacity,
        marker={
            'line': {
                'color': 'rgb(250,250,248)',
                'width': 1,
            },
        }, 

    )
    return {
        'data': [fig], 
        'layout': go.Layout(
            title="Congressional Districts 11 and 12 (115th Congress), Michigan",
            geo_scope='usa',
            mapbox_style='carto-positron', 
            mapbox_zoom=9, 
            mapbox_center = {
                'lat': 42.4602, 
                'lon': -83.5529}, 
                height=800
        ),
    }


# @app.callback(
#     dash.dependencies.Output('matt-graph2', 'figure'),
#     [dash.dependencies.Input('value-selected', 'value')]
# )

# def update_figure(selected):
#     county = get_county(2612)
#     name = df[df['geoid'] == county['id']]['GeoName'].values[0]
#     county_id = df[df['geoid'] == 2612]['GEOID']
#     county_index = county_id.index[0]
#     opacity = df[selected][county_index] * .01
#     custom_df = df[df.index == county_index]
#     color=df[df.index == county_index]
#     # print(name, '\n', county_id, '\n', county_index, '\n', opacity, '\n', custom_df)
#     fig = go.Choroplethmapbox(
#         colorscale = 'Blues',
#         showscale=False,
#         customdata=custom_df,
#         geojson=county, 
#         locations=county_id,
#         z=pd.Series(p_num[county_index]),
#         text=name,
#         autocolorscale=False,
#         marker_opacity=opacity,
#         marker={
#             'line': {
#                 'color': 'rgb(250,250,248)',
#                 'width': 1,
#             },
#         }, 
#         colorbar={
#             'thickness': 10,
#             'len': 0.3,
#             'x': 1,
#             'y': 1, 
#         }
#     )
#     return {
#         'data': [fig], 
#         'layout': go.Layout(
#             title=name,
#             geo_scope='usa',
#             mapbox_style='carto-positron', 
#             mapbox_zoom=9, 
#             mapbox_center = {
#                 'lat': 42.1702, 
#                 'lon': -83.4229}, 
#                 height=800
#         ),
#     }

@app.callback(
    dash.dependencies.Output('ben-graph', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')]
)

def update_figure(selected):
    county = get_county(101)
    # name = df[df['geoid'] == county['id']]['GeoName'].values[0]
    # county_id = df[df['geoid'] == 101]['GEOID']
    # county_index = county_id.index[0]
    # opacity = df[selected][county_index] * .01
    # custom_df = df[df.index == county_index]
    # color=df[df.index == county_index]
    
    newdf = df[df['geoid'].isin([101])]
    name = newdf['GeoName'].values[0]
    # county_id = df[df['geoid'].isin([2611,2612])]['GEOID']
    # county_index = county_id.index
    # opacity = df[selected][county_index] * .01
    opacity = newdf['happening'].values * .01
    # custom_df = df[df.index == county_index]
    # color=df[df.index == county_index]
    # print(name, '\n', county_id, '\n', county_index, '\n', opacity, '\n', custom_df)
    colorsIdx = {'Democratic': 'blue', 'Republican': 'red'}
    colorsNum = {'Democratic': 0, 'Republican': 1}
    cols = newdf['party'].map(colorsIdx)
    p_num = newdf['party'].map(colorsNum)
    # print(p_num)
    my_text = [n + "<br>Happening: " + str(h) for n, h in zip(list(newdf['GeoName']),list(newdf['happening']))]

    # print(name, '\n', county_id, '\n', county_index, '\n', opacity, '\n', custom_df)
    fig = go.Choroplethmapbox(
        # colorscale = 'RdBu',
        showscale=False,
        customdata=newdf,
        geojson=county, 
        locations=newdf['GEOID'],
        z=p_num,
        zmin=0,
        zmax=1,
        text=my_text,
        autocolorscale=False,
        marker_opacity=opacity,
        marker={
            'line': {
                'color': 'rgb(250,250,248)',
                'width': 1,
            },
        }, 

    )
    return {
        'data': [fig], 
        'layout': go.Layout(
            title=name,
            geo_scope='usa',
            mapbox_style='carto-positron', 
            mapbox_zoom=7, 
            mapbox_center = {
                'lat': 30.7902, 
                'lon': -88.0029}, 
                height=800
        ),
    }


@app.callback(
    dash.dependencies.Output('ben-graph2', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')]
)

def update_figure(selected):
    county = get_county(3610)
    # name = df[df['geoid'] == county['id']]['GeoName'].values[0]
    # county_id = df[df['geoid'] == 3610]['GEOID']
    # county_index = county_id.index[0]
    # opacity = df[selected][county_index] * .01
    # custom_df = df[df.index == county_index]
    # color=df[df.index == county_index]

    newdf = df[df['geoid'].isin([3610])]
    name = newdf['GeoName'].values[0]
    opacity = newdf['happening'].values * .01
    colorsIdx = {'Democratic': 'blue', 'Republican': 'red'}
    colorsNum = {'Democratic': 0, 'Republican': 1}
    cols = newdf['party'].map(colorsIdx)
    p_num = newdf['party'].map(colorsNum)
    my_text = [n + "<br>Happening: " + str(h) for n, h in zip(list(newdf['GeoName']),list(newdf['happening']))]

    # print(name, '\n', county_id, '\n', county_index, '\n', opacity, '\n', custom_df)
    fig = go.Choroplethmapbox(
        # colorscale = 'Blues',
        showscale=False,
        customdata=newdf,
        geojson=county, 
        locations=newdf['GEOID'],
        z=p_num,
        zmin=0,
        zmax=1,
        text=my_text,
        autocolorscale=False,
        marker_opacity=opacity,
        marker={
            'line': {
                'color': 'rgb(250,250,248)',
                'width': 1,
            },
        }, 
        colorbar={
            'thickness': 10,
            'len': 0.3,
            'x': 1,
            'y': 1, 
        }
    )
    return {
        'data': [fig], 
        'layout': go.Layout(
            title=name,
            geo_scope='usa',
            mapbox_style='carto-positron', 
            mapbox_zoom=10, 
            mapbox_center = {
                'lat': 40.7302, 
                'lon': -73.9729}, 
                height=800
        ),
    }

@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')]
)

def update_figure(selected):
    opacity = df[selected].values * .01
    fig = go.Choroplethmapbox(
        showscale=False,
        customdata=df,
        geojson=counties, 
        locations=df['geoid'],
        z=p_num,
        text=df['GeoName'], 
        autocolorscale=False,
        marker_opacity=opacity,
        marker={
            'line': {
                'color': 'rgb(250,250,248)',
                'width': 1,
            },
        }, 
        colorbar={
            'thickness': 10,
            'len': 0.3,
            'x': 1,
            'y': 1, 
        }
    )
    return {
        'data': [fig], 
        'layout': go.Layout(
            mapbox_style='carto-positron', 
            mapbox_zoom=3.3, 
            mapbox_center = {
                'lat': 37.0902, 
                'lon': -95.7129}, 
                height=800
        )
    }

@app.callback(
    dash.dependencies.Output('my-bars3', 'figure'),
    [dash.dependencies.Input('value-selected-region1', 'value')]
)

def update_bars(region1):
    dff = df_region.loc[df_region['region'] == region1][['happening', 'happeningOppose', 'affectweather', 'affectweatherOppose', 'harmUS', 'harmUSOppose', 'worried', 'worriedOppose']]
    values = dff.values[0]
    agree_vals = [values[0], values[2], values[4], values[6]]
    disagree_vals = [values[1], values[3], values[5], values[7]]
    opinions = ['Happening', 'Affects weather', 'Harmful to the US', 'Worrisome']

    bars = data=[
        go.Bar(name='Agree', x=opinions, y=agree_vals, marker_color='rgb(45,117,0)'),
        go.Bar(name='Disagree', x=opinions, y=disagree_vals, marker_color='rgb(80,182,0)'),
    ]
    return {
        'data': bars,
        'layout': go.Layout(
            title="Average Climate Opinion of the {}".format(region1),
            xaxis_title="Opinion",
            yaxis_title="Percent of People Who Share This Opinion"
        )
    }

@app.callback(
    dash.dependencies.Output('my-bars4', 'figure'),
    [dash.dependencies.Input('value-selected-region2', 'value')]
)

def update_bars(region2):
    dff = df_region.loc[df_region['region'] == region2][['happening', 'happeningOppose', 'affectweather', 'affectweatherOppose', 'harmUS', 'harmUSOppose', 'worried', 'worriedOppose']]
    values = dff.values[0]
    agree_vals = [values[0], values[2], values[4], values[6]]
    disagree_vals = [values[1], values[3], values[5], values[7]]
    opinions = ['Happening', 'Affects weather', 'Harmful to the US', 'Worrisome']

    bars = data=[
        go.Bar(name='Agree', x=opinions, y=agree_vals, marker_color='rgb(45,117,0)'),
        go.Bar(name='Disagree', x=opinions, y=disagree_vals, marker_color='rgb(80,182,0)'),
    ]
    return {
        'data': bars,
        'layout': go.Layout(
            title="Average Climate Opinion of the {}".format(region2),
            xaxis_title="Opinion",
            yaxis_title="Percent of People Who Share This Opinion",
        )
    }

@app.callback(
    dash.dependencies.Output('my-bars', 'figure'),
    [dash.dependencies.Input('value-selected2', 'value')]
)

def update_bars(selected2):
    dff = df.loc[df['GeoName'] == selected2][['happening', 'happeningOppose', 'affectweather', 'affectweatherOppose', 'harmUS', 'harmUSOppose', 'worried', 'worriedOppose']]
    values = dff.values[0]
    agree_vals = [values[0], values[2], values[4], values[6]]
    disagree_vals = [values[1], values[3], values[5], values[7]]
    opinions = ['Happening', 'Affects weather', 'Harmful to the US', 'Worrisome']

    bars = data=[
        go.Bar(name='Agree', x=opinions, y=agree_vals, marker_color='rgb(45,117,0)'),
        go.Bar(name='Disagree', x=opinions, y=disagree_vals, marker_color='rgb(80,182,0)'),
    ]
    return {
        'data': bars,
        'layout': go.Layout(
            title="Average Climate Opinion of the {}".format(selected2),
            xaxis_title="Opinion",
            yaxis_title="Percent of People Who Share This Opinion",
        )
    }

@app.callback(
    dash.dependencies.Output('my-bars2', 'figure'),
    [dash.dependencies.Input('value-selected3', 'value')]
)

def update_bars(selected3):
    dff = df.loc[df['GeoName'] == selected3][['happening', 'happeningOppose', 'affectweather', 'affectweatherOppose', 'harmUS', 'harmUSOppose', 'worried', 'worriedOppose']]
    values = dff.values[0]
    agree_vals = [values[0], values[2], values[4], values[6]]
    disagree_vals = [values[1], values[3], values[5], values[7]]
    opinions = ['Happening', 'Affects weather', 'Harmful to the US', 'Worrisome']

    bars = data=[
        go.Bar(name='Agree', x=opinions, y=agree_vals, marker_color='rgb(45,117,0)'),
        go.Bar(name='Disagree', x=opinions, y=disagree_vals, marker_color='rgb(80,182,0)'),
    ]
    return {
        'data': bars,
        'layout': go.Layout(
            title="Average Climate Opinion of the {}".format(selected3),
            xaxis_title="Opinion",
            yaxis_title="Percent of People Who Share This Opinion",
        )
    }


@app.callback(
    dash.dependencies.Output('northeast-scatter', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')])

def update_graph_northeast(selected):
    dff = df[df['region'] == 'Northeast'][['geoid', 'party', 'happening', 'happeningOppose', 'human', 'humanOppose', 'GeoName']]
    dff2 = df2[df2['region'] == 'Northeast']
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
        'layout': go.Layout(
            title="Opinions of People in the Northeast",
            xaxis_title="Number of Weather Alerts",
            yaxis_title='Percent of People Who Agree: {}'.format(selected),
        )
    }


@app.callback(
    dash.dependencies.Output('midwest-scatter', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')])

def update_graph_midwest(selected):
    dff = df[df['region'] == 'Midwest'][['geoid', 'party', 'happening', 'happeningOppose', 'human', 'humanOppose', 'GeoName']]
    dff2 = df2[df2['region'] == 'Midwest']
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
        'layout': go.Layout(
            title="Opinions of People in the Midwest",
            xaxis_title="Number of Weather Alerts",
            yaxis_title='Percent of People Who Agree: {}'.format(selected),
        )
    }

@app.callback(
    dash.dependencies.Output('south-scatter', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')])

def update_graph_south(selected):
    dff = df[df['region'] == 'South'][['geoid', 'party', 'happening', 'happeningOppose', 'human', 'humanOppose', 'GeoName']]
    dff2 = df2[df2['region'] == 'South']
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
        'layout': go.Layout(
            title="Opinions of People in the South",
            xaxis_title="Number of Weather Alerts",
            yaxis_title='Percent of People Who Agree: {}'.format(selected),
        )
    }



@app.callback(
    dash.dependencies.Output('west-scatter', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')])

def update_graph_west(selected):
    dff = df[df['region'] == 'West'][['geoid', 'party', 'happening', 'happeningOppose', 'human', 'humanOppose', 'GeoName']]
    dff2 = df2[df2['region'] == 'West']

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
        'layout': go.Layout(
            title="Opinions of People in the West",
            xaxis_title="Number of Weather Alerts",
            yaxis_title='Percent of People Who Agree: {}'.format(selected),
        )
    }

@app.callback(
    dash.dependencies.Output('events-scatter', 'figure'),
    [dash.dependencies.Input('value-selected2', 'value'), dash.dependencies.Input('value-selected3', 'value')])

def update_graph(selected2, selected3):
    df1 = list(pd.pivot_table(new.groupby('GeoName').get_group(selected2), values='alerts_total', columns='event').values[0])
    df2 = list(pd.pivot_table(new.groupby('GeoName').get_group(selected3), values='alerts_total', columns='event').values[0])
    max_1 = pd.pivot_table(new.groupby('GeoName').get_group(selected2), values='alerts_total', columns='event').values.max()
    # max_2 = pd.pivot_table(new.groupby('GeoName').get_group(selected3), values='alerts_total', columns='event').values
    # combined = np.concatenate(max_1, max_2)
    # maxed = combined.max()

    categories = list(pd.pivot_table(new.groupby('geoid').get_group(101), values='alerts_total', columns='event').columns)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=df1,
        theta=categories,
        fill='toself',
        name=selected2,
        marker_color='rgb(104,115,135)'
    ))

    fig.add_trace(go.Scatterpolar(
        r=df2,
        theta=categories,
        fill='toself',
        name=selected3,
        marker_color='rgb(136,171,184)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, max_1]
            )),
        showlegend=True
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)