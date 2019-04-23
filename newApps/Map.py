import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Event, Input
import plotly
import plotly.graph_objs as go
from WatchDogs_MongoWrapper import MongoWrapper
import pandas as pd

app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div(children=[
        html.Div(
            dcc.Dropdown(
                id='my_dropdown',
                placeholder='Select a stock',
                options=[
                    {'label': 'Microsoft', 'value': 'Microsoft'},
                    {'label': 'Facebook', 'value': 'Facebook'},
                    {'label': 'Visa', 'value': 'Visa'},
                    {'label': 'Nvidia', 'value': 'Nvidia'},
                    {'label': 'Google', 'value': 'Google'},
                    {'label': 'Nike', 'value': 'Nike'},
                    {'label': 'Alibaba', 'value': 'Alibaba'},
                    {'label': 'Netflix', 'value': 'Netflix'},
                    {'label': 'PayPal', 'value': 'PayPal'},
                    {'label': 'Ebay', 'value': 'Ebay'},
                    {'label': 'Tesla', 'value': 'Tesla'},
                    {'label': 'Twitter', 'value': 'Twitter'},
                    {'label': 'Disney', 'value': 'Disney'},
                    {'label': 'Pepsi', 'value': 'Pepsi'},
                    {'label': 'Lyft', 'value': 'Lyft'},
                    {'label': 'Chevron', 'value': 'Chevron'},
                    {'label': 'Cisco', 'value': 'Cisco'},
                    {'label': 'Intel', 'value': 'Intel'},
                    {'label': 'Verizon', 'value': 'Verizon'},
                    {'label': 'AT&T', 'value': 'AT&T'},
                    {'label': 'Nokia', 'value': 'Nokia'},
                    {'label': 'Comcast', 'value': 'Comcast'},
                    {'label': 'Kroger', 'value': 'Kroger'},
                    {'label': 'Boeing', 'value': 'Boeing'},
                    {'label': 'Starbucks', 'value': 'Starbucks'},
                    {'label': 'Walmart', 'value': 'Walmart'},
                    {'label': 'Adobe', 'value': 'Adobe'},
                    {'label': 'Dell', 'value': 'Dell'},
                    {'label': 'Ford', 'value': 'Ford'},
                    {'label': 'Samsung', 'value': 'Samsung'},
                ]
            )
        )
    ]),        

    html.Div(id='live-update-graph'),

    dcc.Interval(
        id='interval-update',
        interval=10000
    )

])

@app.callback(Output('live-update-graph', 'children'),
              [Input('my_dropdown', 'value')],
              events=[Event('interval-update', 'interval')])

def update_graph_live(value):

    mongo = MongoWrapper()

    getTweets =  mongo.get_tweets_with_lat_long(value)
    allLatitude = getTweets['Latitude']
    allLongitude = getTweets['Longitude']
    allSentiment = getTweets['Sentiment_Value']

    tots = allSentiment.count()

    scl = [ [0,"rgb(39,174,96)"],[0.35,"rgb(46,204,113)"],[0.5,"rgb(241,196,15)"],\
    [0.6,"rgb(243,156,18)"],[0.7,"rgb(231,76,60)"],[1,"rgb(192,57,43)"] ]

    bigGraph = dcc.Graph(
        style={'height': '800px'},
        figure={
            'data' :[{
                'type':'scattergeo',
                'locationmode':'USA-states',
                'lon' : allLongitude,
                'lat' : allLatitude,
                'text' : allSentiment,
                'mode':'markers',
                'marker':{ 
                    'size':8, 
                    'opacity':0.8,
                    'reversescale':True,
                    'autocolorscale':False,
                    'symbol':'circle',
                    'line':{
                        'width':1,
                        'color':'rgba(102, 102, 102)'
                    },
                    'colorscale' : scl,
                    'cmin' : -1,
                    'color' : allSentiment,
                    'cmax' : 1,
                    'colorbar':{
                        'title':"Polarity Scale",
                        'thickness':20,
                        'titleside' : "right",
                        # 'outlinecolor' : "rgba(68, 68, 68, 0)",
                        'ticks' : "outside",
                        'ticklen' : 3,
                        # 'showticksuffix' : "last",
                        # 'ticksuffix' : " inches",
                        'dtick' : 0.1
                    }
                }
            }],

                'layout' :{
                    'title': "Twitter Sentiment for {}\n".format(value), 
                    'font':{
                        'size':15,
                    },
                    'geo' :{
                        # 'scope':'usa',
                        # 'projection':dict( 'type'='albers usa' ),
                        'showland' : True,
                        'landcolor' : "rgb(250, 250, 250)",
                        'subunitcolor' : "rgb(217, 217, 217)",
                        'countrycolor' : "rgb(217, 217, 217)",
                        'countrywidth' : 0.5,
                        'subunitwidth' : 1,
                        'showsubunits': True,
                        'showcountries':True,
                        'showcoastlines':True,
                        'coastlinecolor':"rgb(155, 155, 155)",
                        'showframe':True,
                        'framecolor': "rgb(155, 155, 155)"
                        # 'showocean':True
                        # 'showlakes':True        
                    },
                }  
        }
    ), html.Div(children='Total Tweets pulled for searchword: {}.\n'.format(tots)),

    return (bigGraph)
       
if __name__ == '__main__':
    app.run_server(debug=True)