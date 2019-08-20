import os
import dash
import dash_html_components as html
import dash_core_components as dcc
# from dash.dependencies import Output, Event, Input
from WatchDogs_MongoWrapper import MongoWrapper
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
# from geopy.geocoders import Nominatim

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(style={'background':'#2f3239'}, children=[
    dcc.Dropdown(
        style={
            'backgroundColor':'#f8f8f8', 'borderColor':'#2f3239', 'borderRadius':'5px', 'fontFamily':'Roboto', 'height':'35px', 'width':'150px'
        },
        value='Microsoft',
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
    ),
    
    html.Div(id='output-container', style={'backgroundColor':'transparent'}),

])

@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('my_dropdown', 'value')]
    )


def update_graph_live(value):

    # response = requests.get("http://104.154.230.56/api/get_tweets_with_lat_long/{}".format(value))
    # data = response.json()
    # pretty = pd.DataFrame()

    # df_sent = pd.DataFrame.from_dict(json_normalize(data['Sentiment_Value']), orient='columns')
    # df_lat = pd.DataFrame.from_dict(json_normalize(data['Latitude']), orient='columns')
    # df_long = pd.DataFrame.from_dict(json_normalize(data['Longitude']), orient='columns')
    # df_tweet = pd.DataFrame.from_dict(json_normalize(data['Tweet_Text']), orient='columns')

    # sent_list = df_sent.iloc[0].tolist()
    # lat_list = df_lat.iloc[0].tolist()
    # long_list = df_long.iloc[0].tolist()
    # tweet_list = df_tweet.iloc[0].tolist()

    # pretty['Sentiment'] = sent_list
    # pretty['Latitude'] = lat_list
    # pretty['Longitude'] = long_list
    # pretty['Tweet'] = tweet_list
    
    response_latlong = requests.get("http://104.154.230.56/api/get_tweets_with_lat_long/{}".format(value))
    data = response_latlong.json()
    pretty = json_normalize(data)

    totalSentiment = pretty['Sentiment_Value']
    totalLongitude = pretty['Longitude']
    totalLatitude = pretty['Latitude']
    totalTweet = pretty['Tweet_Text']

    tots2 = totalSentiment.count()

    scl = [ [0,"rgb(39,174,96)"],[0.35,"rgb(46,204,113)"],[0.5,"rgb(241,196,15)"],\
    [0.6,"rgb(243,156,18)"],[0.7,"rgb(231,76,60)"],[1,"rgb(192,57,43)"] ]

    return dcc.Graph(
        style={'height': '900px'},
        figure={
            'data' :[{
                'type':'scattergeo',
                # 'locationmode':'USA-states',
                'lon' : totalLongitude,
                'lat' : totalLatitude,
                'text' : totalTweet,
                'mode':'markers',
                'marker':{ 
                    'size':10, 
                    # 'opacity':1,
                    'reversescale':True,
                    'autocolorscale':False,
                    'symbol':'circle-open',
                    'line':{
                        'width':1.5,
                        'color':'rgba(150, 150, 150)'
                    },
                    'colorscale' : scl,
                    'cmin' : -1,
                    'color' : totalSentiment,
                    'cmax' : 1,
                    'colorbar':{
                        'title':{
                            'text':"Polarity Scale",
                            'font':{
                                'size':14,
                            },
                        },
                        'thickness':20,
                        'titleside' : "right",
                        'ticks' : "outside",
                        'ticklen' : 3,
                        'tickfont':{
                            'size':10,
                        },
                        # 'showticksuffix' : "last",
                        # 'ticksuffix' : " inches",
                        'dtick' : 0.1
                    }
                }
            }],

                'layout' :{
                    # 'legend':{
                    #     'orientation': 'h',
                    # },
                    'paper_bgcolor':'#2f3239',
                    'plot_bgcolor':'#2f3239',
                    'title': "Twitter Sentiment for {}\n".format(value), 
                    'font':{
                        'size':15,
                        'color': '#f8f8f8',
                    },
                    'geo' :{
                        # 'scope':'usa',
                        # 'projection':dict( 'type'='albers usa' ),
                        'showland' : True,
                        'bgcolor': '#2f3239',       
                        'landcolor' : "#2f3239",
                        'subunitcolor' : "#2f3239",
                        'countrycolor' : "#f8f8f8",
                        'coastlinewidth': 0.5,
                        'countrywidth' : 0.5,
                        'subunitwidth' : 1,
                        'showsubunits': True,
                        'showcountries':True,
                        'showcoastlines':True,
                        'coastlinecolor':"#f8f8f8",
                        'showframe':False,
                        # 'framecolor': "rgb(155, 155, 155)"
                        'showocean':True,
                        'oceancolor':"#2f3239"
                        # 'showlakes':True        
                    },
                }  
        }
    ), 
    # html.Div(children='Total Tweets pulled for searchword: {}.\n'.format(tots2))
       
if __name__ == '__main__':
    app.run_server(debug=True)
