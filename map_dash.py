# -*- coding: utf-8 -*-
import dash
from urllib.request import urlopen
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import plotly.graph_objects as go

with urlopen('https://raw.githubusercontent.com/SophieNiu/infovisfinal/master/dataset/CleanedData/cleaned-us-115th-congress.geojson') as response:
    counties = json.load(response)
df = pd.read_csv("https://raw.githubusercontent.com/SophieNiu/infovisfinal/master/dataset/CleanedData/Congress_YCOM_2019_Data.csv", dtype={"geoid": int})

for i in range(0, len(counties['features'])):
    counties["features"][i]['id'] = counties["features"][i]['properties']['geoid']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.Div(
            [html.H1("Climate Change")],
            style={
                'text-align': "center", 
                "padding-bottom": "30"
            }
        ),
        html.Div(
            [
                html.Span(
                    "Display: ", 
                    className="six columns", 
                    style={
                        "text-align": "right", 
                        "width": "40%", 
                        "padding-top": 10
                    }
                ), 
            dcc.Dropdown(
                id="value-selected", 
                value='happening', 
                options=[
                    {
                        'label': "Happening", 
                        'value': 'happening'
                    }, 
                    {
                        'label': "HappeningOppose", 
                        'value': 'happeningOppose'
                    }, 
                    {
                        'label': "Human", 
                        'value': 'human'
                    }
                ], 
                style={
                    "display": "block", 
                    "margin-left": "auto", 
                    "margin-right": "auto", 
                    "width": "70%"
                }, 
                className="six columns"
            )
        ], 
        className="row"
    ), 
    dcc.Graph(id="my-graph")
    ], 
    className="container"
)


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("value-selected", "value")]
)

def update_figure(selected):
    def title(text):
        if text == "happening":
            return "Percent believe Happening"
        elif text == "happeningOppose":
            return "Percent believe not Happening"
        else:
            return "Percent believe Human imposed"
    fig = go.Choroplethmapbox(
        geojson=counties, 
        locations=df['geoid'],
        z=df[selected],
        text=df['GeoName'], 
        autocolorscale=False, 
        colorscale="YlGnBu",
        marker={
            'line': {
                'color': 'rgb(180,180,180)',
                'width': 0.5
            }
        }, 
        colorbar={
            "thickness": 10,
            "len": 0.3,
            "x": 0.9,
            "y": 0.7, 
            'title': {
                "text": title(selected),
                "side": "bottom"
            }
        }
    )
    return {
        "data": [fig], 
        "layout": go.Layout(
            mapbox_style='carto-positron', 
            mapbox_zoom=3, 
            mapbox_center = {
                "lat": 37.0902, 
                "lon": -95.7129}, 
                title=title(selected), 
                height=800
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)