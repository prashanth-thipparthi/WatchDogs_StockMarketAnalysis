import dash
import dash_html_components as html
import dash_core_components as dcc
from WatchDogs_MongoWrapper import MongoWrapper

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
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
            {'label': 'Uber', 'value': 'Uber'},
            {'label': 'Lyft', 'value': 'Lyft'},
            {'label': '3D Systems Corporation', 'value': '3D Systems Corporation'},
        ]
    ),
    
    dcc.Graph(id='live-update-graph'),

    dcc.Interval(
        id='interval-update',
        interval=1*1000, # in milliseconds
        # n_intervals=0
    )
])

@app.callback(dash.dependencies.Output('live-update-graph', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')],
              events=[dash.dependencies.Event('intervalComp', 'n_intervals')])


def update_graph_live(value, n_intervals):

    mongo = MongoWrapper()

    neg_sentiment, neutral_sentiment, pos_sentiment = mongo.get_polarity_tweets_of_stock(value)
    
    negs = neg_sentiment.count()
    poss = pos_sentiment.count()
    neuu = neutral_sentiment.count()
    tots = negs+poss+neuu

    posPercentage = (poss/(tots))*100
    neuPercentage = (neuu/(tots))*100
    negPercentage = (negs/(tots))*100

    fig=({
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
        })

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)