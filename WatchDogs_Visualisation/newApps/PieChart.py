import dash
import dash_html_components as html
import dash_core_components as dcc
from WatchDogs_MongoWrapper import MongoWrapper
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
# from geopy.geocoders import Nominatim

app = dash.Dash(__name__)
app.layout = html.Div(style={'background':'#2f3239'}, children=[
    dcc.Dropdown(
        style={
            'backgroundColor':'#f8f8f8', 'borderColor':'#2f3239', 'borderRadius':'5px', 'fontFamily':'Roboto', 'height':'35px', 'width':'150px'
        },
        id='my-dropdown',
        placeholder='Select a stock',
        value='Microsoft',
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
    html.Div(id='output-container', style={'backgroundColor':'transparent'})
])        

@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')]
    )
    
# def api(value):
    
#     response = requests.get("http://104.154.230.56/api/get_polarity_tweets_of_stock/{}".format(value))
#     data = response.json()
#     pretty = pd.DataFrame()

#     df_sent = pd.DataFrame.from_dict(json_normalize(data['neg_tweets']), orient='columns')
#     df_lat = pd.DataFrame.from_dict(json_normalize(data['neu_tweets']), orient='columns')
#     df_long = pd.DataFrame.from_dict(json_normalize(data['pos_tweets']), orient='columns')
#     # df_tweet = pd.DataFrame.from_dict(json_normalize(data['Tweet_Text']), orient='columns')

#     pos_list = df_sent.iloc[0].tolist()
#     neu_list = df_lat.iloc[0].tolist()
#     neg_list = df_lat.iloc[0].tolist()

#     pretty['Negative'] = pos_list
#     pretty['Neutral'] = neu_list
#     pretty['Positive'] = neg_list
#     # pretty['Tweet'] = tweet_list

def mainFunction(value):

    # mongo = MongoWrapper()
  
    # neg_sentiment, neutral_sentiment, pos_sentiment = mongo.get_polarity_tweets_of_stock(value)

    # negs = neg_sentiment.count()
    # poss = pos_sentiment.count()
    # neuu = neutral_sentiment.count()
    # tots = negs+poss+neuu

    # posPercentage = (poss/(tots))*100
    # neuPercentage = (neuu/(tots))*100
    # negPercentage = (negs/(tots))*100


    # response = requests.get("http://104.154.230.56/api/get_polarity_tweets_of_stock/{}".format(value))
    # data = response.json()
    # pretty = pd.DataFrame()

    # dataNeg = data['neg_tweets']
    # dataNeu = data['neu_tweets']
    # dataPos = data['pos_tweets']

    # df_neg = pd.DataFrame.from_dict(json_normalize(dataNeg['Text\\']), orient='columns')
    # df_neu = pd.DataFrame.from_dict(json_normalize(dataNeu['Text\\']), orient='columns')
    # df_pos = pd.DataFrame.from_dict(json_normalize(dataPos['Text\\']), orient='columns')
    # # df_tweet = pd.DataFrame.from_dict(json_normalize(data['Tweet_Text']), orient='columns')

    # pos_list = df_pos.iloc[0].tolist()
    # neu_list = df_neu.iloc[0].tolist()
    # neg_list = df_neg.iloc[0].tolist()

    # pretty['Negative'] = pos_list
    # pretty['Neutral'] = neu_list
    # pretty['Positive'] = neg_list
    # pretty['Tweet'] = tweet_list
    response_polarity = requests.get(
        "http://104.154.230.56/api/get_polarity_tweets_of_stock/{}".format(value))


    data2 = response_polarity.json()
    neg_tweets = data2['Negative_Tweets']
    pos_tweets = data2['Positive_Tweets']
    neutral_tweets = data2['Neutral_Tweets']
    negative = json_normalize(neg_tweets)
    positive = json_normalize(pos_tweets)
    neutral = json_normalize(neutral_tweets)

    sumPos = len(positive)
    sumNeg = len(negative)
    sumNeu = len(neutral)
    

    # totalNeg = pretty['Negative']
    # totalNeu = pretty['Neutral']
    # totalPos = pretty['Positive']

    # sumNeg = totalNeg.count()
    # sumNeu = totalNeu.count()
    # sumPos = totalPos.count()

    tots = sumNeg+sumPos+sumNeu
    posPercentage = (sumPos/(tots))*100
    neuPercentage = (sumNeu/(tots))*100
    negPercentage = (sumNeg/(tots))*100

    # print(posPercentage)


    return dcc.Graph(
        animate=False,
        figure={
        'data': [{
                'type': 'pie',
                'labels': ['Positive', 'Neutral' ,'Negative'],
                'values': [posPercentage, neuPercentage, negPercentage],
                'marker': {
                    'colors': ['rgb(39,174,96)', 'rgb(242,176,17)', 'rgb(192,57,43)'],
                    'line':{
                        'color':'#2f3239',
                        'width':3,
                    },
                # 'values': [posPercentage, negPercentage],
                # 'marker': {'colors': ['#32C85A', '#FA4632'],
                    },
                'opacity':0.9,
                'hole':0.7,
                # 'pull':0.05,
            }],

            'layout':{
                'paper_bgcolor':'#2f3239',
                'plot_bgcolor':'#2f3239',
                'title':"Twitter Sentiment for {}\n".format(value),
                'font':{
                    'size':15,
                    'color': '#f8f8f8',
                },
                'legend':{
                    'font':{
                        'size':12,
                        'color': '#f8f8f8',
                    },
                }
            }
        }
    )
       
if __name__ == '__main__':
    app.run_server(debug=True)
