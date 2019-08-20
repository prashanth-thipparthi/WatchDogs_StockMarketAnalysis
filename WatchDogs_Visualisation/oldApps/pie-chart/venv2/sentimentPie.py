import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Event, Input
import plotly
import plotly.graph_objs as go
from WatchDogs_MongoWrapper import MongoWrapper

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

    neg_sentiment, neutral_sentiment, pos_sentiment = mongo.get_polarity_tweets_of_stock(value)
    
    negs = neg_sentiment.count()
    poss = pos_sentiment.count()
    neuu = neutral_sentiment.count()
    tots = negs+poss+neuu

    posPercentage = (poss/(tots))*100
    neuPercentage = (neuu/(tots))*100
    negPercentage = (negs/(tots))*100

    bigGraph = dcc.Graph(
        # animate=True,
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
    )

    afterText = html.Div(children='Total Tweets pulled for searchword: {}.\n'.format(tots))

    return (bigGraph, afterText)
       
if __name__ == '__main__':
    app.run_server(debug=True)