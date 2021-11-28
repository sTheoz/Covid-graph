import pandas as pd
import pprint

# Datetime, String, Interger Example Dataframe 

listDate = ['2020-01-01 00:00:00','2020-01-01 00:01:00','2020-01-01 00:02:00', '2020-01-01 00:03:00']
listStrings = ['a','b','c','d']
listInterger = [1, 2, 3, 4 ]

df = pd.DataFrame([ x for x in zip(listDate,listStrings,listInterger)], columns=['date','string', 'interger'])
df['date'] = pd.to_datetime(df['date'])


df = pd.DataFrame(data = {'date' : df['date'],
                          'strings': df['string'],
                          'interger' : df['interger']})
 
test = df.to_dict(orient='records')
pprint.pprint(test)

df = pd.read_csv("/home/naveteur/Téléchargements/donnees-hospitalieres-covid19-2020-11-25-19h00.csv", delimiter=';')
test = df.to_dict(orient='records')
pprint.pprint(test[:2])