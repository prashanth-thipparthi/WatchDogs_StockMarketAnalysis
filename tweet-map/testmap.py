import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly
import plotly.graph_objs as go
from WatchDogs_MongoWrapper import MongoWrapper
from dash.dependencies import Input, Output
import pandas as pd


df = pd.read_csv('/Users/iankresyman/Desktop/2011_february_us_airport_traffic2.csv')
df.head()

df['text'] = df['airport'] + '' + df['city'] + ', ' + df['state'] + '' + 'Arrivals: ' + df['cnt'].astype(str)

scl = [ [0,"rgb(39,174,96)"],[0.35,"rgb(46,204,113)"],[0.5,"rgb(241,196,15)"],\
    [0.6,"rgb(243,156,18)"],[0.7,"rgb(231,76,60)"],[1,"rgb(192,57,43)"] ]

mongo = MongoWrapper()

negCoord, neuCoord, posCoord = mongo.get_lat_long('Microsoft')

print('\n')
print(negCoord[0])
print('\n')

app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Graph(
        style={'height': '800px'},
        figure={
            'data' :[{
                'type':'scattergeo',
                'locationmode':'USA-states',
                'lon' : df['long'],
                'lat' : df['lat'],
                'text' : df['text'],
                # 'lon':df['longitude'],
                # 'lat':df['latitude'],
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
                    'color' : df['cnt'],
                    'cmax' : 1,
                    'colorbar':{
                        'title':"Polarity Scale"
                    }
                }
            }],

            'layout' :{
                'title':{
                    'text': 'Tweet locations with sentiment ratings', 
                },
                'font':{
                    'size':15,
                },
                'geo' :{
                    'scope':'usa',
                    # 'projection':dict( 'type'='albers usa' ),
                    'showland' : True,
                    'landcolor' : "rgb(250, 250, 250)",
                    'subunitcolor' : "rgb(217, 217, 217)",
                    'countrycolor' : "rgb(217, 217, 217)",
                    'countrywidth' : 0.5,
                    'subunitwidth' : 0.5        
                },
            }  
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
