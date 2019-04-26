import json 

class Tweet():

    def __init__(self,in_json):
        
        #in_json = json.loads(in_json)
        #self.tweet_id = in_json.id
        #self.dateTime = in_json.created_at
        #self.geo = in_json.geo
        #self.coordinates= in_json.coordinates
        #self.search_text = in_json.text
        #self.text = in_json.text
        pass   
    @staticmethod		
    def parse_from_log_line(in_json):
        new = {}
        new["tweet_id"] = in_json["id"]
        new["dataTime"] = in_json["created_at"]
        new["geo"] = in_json["geo"]
        new["coordinates"] = in_json["coordinates"] 
        new["text"] = in_json["text"] 
        return new      
#        return json.loads(new)
    def __repr__(self):
        return "{} {} {} [{}] \"{} {} {}\" {} {}".format(self.tweet_id, self.dateTime,self.geo, self.coordinates, self.search_text,self.text, self.sentiment_value, self.sentiment_polarity)


di = {"id":1,"created_at":123,"geo":123,"coordinates":12,"search_text":"abc","text":"xyz"}
t = Tweet.parse_from_log_line(di)
print("val:", t)
