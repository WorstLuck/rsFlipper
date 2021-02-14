import pandas as pd
import requests
from datetime import datetime

objects = pd.read_json('data/itemID.json',typ='series')
dfxp = pd.read_csv('data/dxp_weeks.csv')
for col in dfxp:
    dfxp[col] = dfxp[col].apply(lambda x: datetime.strptime(x, '%d %B %Y (%H:%M)').strftime('%Y-%m-%d'))

class get_item:
    def __init__(self,name,graph='False'):
        self.name = name
        self.graph = graph
        self.ID = self.get_ID(name)
        self.item = requests.get("https://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item={}".format(self.ID)).json()['item']
        self.type = self.item['type']
    def get_ID(self,name):
        for ID,item in objects.items():
            if item == name:
                return ID
    '''
    val can be:
        - current
        - today
        - day30 
        - day60
        - day90
        - day180
    '''
    def price(self,group,val='current',graph_period = 'daily'):
        prices = {}
        graphs = {}
        
        item_groups = []
        for ID,item in objects.items():
            if group in item:
                item_groups.append(item)
        if type(item_groups) == list:
            for item in item_groups:
                ID = self.get_ID(item)
                item_info = requests.get("https://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item={}".format(ID)).json()['item'][val]
                if eval(self.graph) == True:
                    graph_info = requests.get("https://services.runescape.com/m=itemdb_rs/api/graph/{}.json".format(ID)).json()
                    graphs[item + ' graph'] = graph_info
                prices[item] = item_info
        else:
            item_info = requests.get("https://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item={}".format(self.ID)).json()['item'][val]
        return prices,graphs