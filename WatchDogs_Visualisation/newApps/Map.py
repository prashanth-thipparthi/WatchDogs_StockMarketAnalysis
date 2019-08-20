import os
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Event, Input
from WatchDogs_MongoWrapper import MongoWrapper
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
from geopy.geocoders import Nominatim
# from urllib2 import urlopen
# import json

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.Div(style={'backgroundColor':'transparent'}, children=[
        html.Div(
            dcc.Dropdown(
                style={
                    'backgroundColor':'transparent', 'borderColor':'rgb(101, 101, 101)'
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
            )
        )
    ]),        

    html.Div(id='live-update-graph', style={'backgroundColor':'transparent'}),

    dcc.Interval(
        id='interval-update',
        interval=10000
    )

])

@app.callback(Output('live-update-graph', 'children'),
              [Input('my_dropdown', 'value')],
              events=[Event('interval-update', 'interval')])

# def api(value):

    
#     data = response.json()
#     pretty = pd.DataFrame()



# def api(value):
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

    # print(pretty)
    # print(pretty)

def update_graph_live(value):

    # mongo = MongoWrapper()

    # getTweets =  mongo.get_tweets_with_lat_long(value)


    # response = requests.get("http://104.154.230.56/api/get_tweets_with_lat_long/{}".format(value))
    # data = response.json()
    # print(data['Latitude'])


    # logs = mongo.get_logger(__name__)
    # logs.info('test log from ian')


    # allLatitude = getTweets['Latitude']
    # allLongitude = getTweets['Longitude']
    # allText = getTweets['Tweet_Text']



    # allTweets = getTweets['Location']

    # latty = allLatitude.tolist()
    # longy = allLongitude.tolist()

    # allSentiment = getTweets['Sentiment_Value']






    # geolocator = Nominatim(user_agent="map")

    # df = pd.DataFrame()

    # stringLatty = str(latty)


    # loc =[]
    # for i,j in zip(latty,longy):

        # location = geolocator.reverse(str(i)+','+str(j))
        # nlocation = list(location)
        # print(nlocation)
        # print(type(location))
        # df['issaLocation'] = location

        # Newlocation = location.tolist()
        # df['location'] = location
        # loc.append(location)
        # print(Newlocation)

    # print(loc)
    # print(df.location)


    # response = requests.get("http://104.154.230.56/api/get_tweets_with_lat_long/{}".format(value))
    # data = response.json()
    # print(data['Latitude'])






    # tots = allSentiment.count()














    response = requests.get("http://104.154.230.56/api/get_tweets_with_lat_long/{}".format(value))
    data = response.json()
    pretty = pd.DataFrame()

    df_sent = pd.DataFrame.from_dict(json_normalize(data['Sentiment_Value']), orient='columns')
    df_lat = pd.DataFrame.from_dict(json_normalize(data['Latitude']), orient='columns')
    df_long = pd.DataFrame.from_dict(json_normalize(data['Longitude']), orient='columns')
    df_tweet = pd.DataFrame.from_dict(json_normalize(data['Tweet_Text']), orient='columns')


    sent_list = df_sent.iloc[0].tolist()
    lat_list = df_lat.iloc[0].tolist()
    long_list = df_long.iloc[0].tolist()
    tweet_list = df_tweet.iloc[0].tolist()

    pretty['Sentiment'] = sent_list
    pretty['Latitude'] = lat_list
    pretty['Longitude'] = long_list
    pretty['Tweet'] = tweet_list













    totalSentiment = pretty['Sentiment']
    tots2 = totalSentiment.count()

    scl = [ [0,"rgb(39,174,96)"],[0.35,"rgb(46,204,113)"],[0.5,"rgb(241,196,15)"],\
    [0.6,"rgb(243,156,18)"],[0.7,"rgb(231,76,60)"],[1,"rgb(192,57,43)"] ]

    bigGraph = dcc.Graph(
        style={'height': '800px'},
        figure={
            'data' :[{
                'type':'scattergeo',
                'locationmode':'USA-states',
                'lon' : pretty['Longitude'],
                'lat' : pretty['Latitude'],
                'text' : pretty['Tweet'],
                'mode':'markers',
                'marker':{ 
                    'size':8, 
                    # 'opacity':0.8,
                    'reversescale':True,
                    'autocolorscale':False,
                    'symbol':'circle',
                    'line':{
                        'width':1,
                        'color':'rgba(102, 102, 102)'
                    },
                    'colorscale' : scl,
                    'cmin' : -1,
                    'color' : pretty['Sentiment'],
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
                    'paper_bgcolor':'rgb(201, 201, 201)',
                    'plot_bgcolor':'rgb(201, 201, 201)',
                    'title': "Twitter Sentiment for {}\n".format(value), 
                    'font':{
                        'size':15,
                    },
                    'geo' :{
                        # 'scope':'usa',
                        # 'projection':dict( 'type'='albers usa' ),
                        'showland' : True,
                        'landcolor' : "rgb(201, 201, 201)",
                        'subunitcolor' : "rgb(151, 151, 151)",
                        'countrycolor' : "rgb(151, 151, 151)",
                        'countrywidth' : 1.5,
                        'subunitwidth' : 1,
                        'showsubunits': True,
                        'showcountries':True,
                        'showcoastlines':True,
                        'coastlinecolor':"rgb(101, 101, 101)",
                        'showframe':False,
                        # 'framecolor': "rgb(155, 155, 155)"
                        'showocean':True,
                        'oceancolor':"rgb(201, 201, 201)"
                        # 'showlakes':True        
                    },
                }  
        }
    ), html.Div(children='Total Tweets pulled for searchword: {}.\n'.format(tots2)),

    return (bigGraph)
       
if __name__ == '__main__':
    app.run_server(debug=True)