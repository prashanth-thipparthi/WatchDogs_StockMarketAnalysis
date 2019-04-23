import dash
# from dash.dependencies import Output, Event
import dash_html_components as html
import dash_core_components as dcc
from WatchDogs_MongoWrapper import MongoWrapper

app = dash.Dash(__name__)
app.layout = html.Div([
    # html.Div('Select a stock'),
    dcc.Dropdown(
        id='my-dropdown',
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
            {'label': 'Uber', 'value': 'Uber'},
            {'label': 'Lyft', 'value': 'Lyft'},
            {'label': '3D Systems Corporation', 'value': '3D Systems Corporation'},
        ],
        # value='NYC'
        placeholder='Select a stock',
    ),
    html.Div(id='output-container')
])


@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')]
    )

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

    # print(posPercentage, neuPercentage, negPercentage)

    return dcc.Graph(
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
                'title':{
                    'text':"Twitter Sentiment for {}\n".format(value),
                },

            }
        }
    ), html.Div(children='Total Tweets pulled for searchword: {}.\n'.format(tots)),
        
if __name__ == '__main__':
    app.run_server(debug=True)
