import dash
import dash_html_components as html
import dash_core_components as dcc
from WatchDogs_MongoWrapper import MongoWrapper
import requests
import json
import pandas as pd
from geopy.geocoders import Nominatim

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        placeholder='Select a stock',
        # value='Microsoft',
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
    html.Div(id='output-container')
])        

@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')]
    )
def api(value):
    
    response = requests.get(
         "http://104.154.230.56/api/get_tweets_with_lat_long/{}".format(value))
    data = response.json()
    pretty = pd.DataFrame()

    df_sent = pd.DataFrame.from_dict(json_normalize(data['Sentiment_Value']), orient='columns')
    df_lat = pd.DataFrame.from_dict(json_normalize(data['Latitude']), orient='columns')
    df_long = pd.DataFrame.from_dict(json_normalize(data['Longitude']), orient='columns')
    df_tweet = pd.DataFrame.from_dict(json_normalize(data['Tweet_Text']), orient='columns')

    sent_list = df_sent.iloc[0].tolist()
    lat_list = df_lat.iloc[0].tolist()
    long_list = df_lat.iloc[0].tolist()
    tweet_list = df_lat.iloc[0].tolist()

    pretty['Sentiment'] = sent_list
    pretty['Latitude'] = lat_list
    pretty['Longitude'] = long_list
    pretty['Tweet'] = tweet_list

    print(pretty)

def mainFunction(value):

    mongo = MongoWrapper()

  
    neg_sentiment, neutral_sentiment, pos_sentiment = mongo.get_polarity_tweets_of_stock(value)

    negs = neg_sentiment.count()
    poss = pos_sentiment.count()
    neuu = neutral_sentiment.count()
    tots = negs+poss+neuu

    posPercentage = (poss/(tots))*100
    neuPercentage = (neuu/(tots))*100
    negPercentage = (negs/(tots))*100

    return dcc.Graph(
        animate=False,
        figure={
        'data': [{
                'type': 'pie',
                'labels': ['Positive', 'Neutral' ,'Negative'],
                'values': [posPercentage, neuPercentage, negPercentage],
                'marker': {'colors': ['#32C85A', '#4C93B1', '#FA4632'],
                # 'values': [posPercentage, negPercentage],
                # 'marker': {'colors': ['#32C85A', '#FA4632'],
                    },
            }],

            'layout':{
                'title':"Twitter Sentiment for {}\n".format(value)
            }
        }
    ), html.Div('Total Tweets pulled for searchword: {}.\n'.format(tots))
       
if __name__ == '__main__':
    app.run_server(debug=True)
