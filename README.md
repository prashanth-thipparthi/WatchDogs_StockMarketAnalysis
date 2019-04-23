## WatchDogs_Visualization
This repo contains the visualization elements to our project.
There are two main apps inside the newApps folder:
1. **PieChart.py** which is a sentiment calculator visualizaed as a pie chart. This app reads tweets from our database, assigns sentiment to each tweet, and then calulates how many tweets are considered 'positive' or 'negative' for every search word. It constantly updates when new data is added to the database.
2. **Map.py** which is a map that shows where the tweets were for each search word and then color codes the dot location from red to yellow to green if tweets are overall 'positive', 'negative', or 'neutral' sentiment rating. In order to use this app, make sure you have installed these versions of dash:

- dash==0.30.0
- dash-core-components==0.38.0
- dash-html-components==0.13.2
- dash-renderer==0.15.0

Along with...

pip install --upgrade git+https://github.com/CUBigDataClass/WatchDogs_MongoWrapper.git

### To create an use a virtual environment:
$ virtualenv venv # creates a virtualenv called "venv"

$ source venv/bin/activate # uses the virtualenv
