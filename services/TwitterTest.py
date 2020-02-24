# -*- coding: utf-8 -*-
"""TwitterParcial2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hhj8LmsaE69l4zl6n2zpYSO7pSnpMnfa

#Manejo de información con la librería de Twitter
---
#Librerias
---
"""

import tweepy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""#Autenticación con la librería
----
"""

api_key = "J7goYmTliL5SN6JxNBcTnaV9P"
api_secret_key = "mECQnrsacSIHIlWYBW8NlkQQKiqMKO5WBtFQQZWJIitfauOvPP"
access_token = "870273825769959424-r85QoXzCVHpNk03vOyqP2FikIj6F9uA"
access_token_secret = "uqOBdmbCYhXyIwjllSZmu5nmlMl2yNn9xL9u086TF6tG0"

aut = tweepy.OAuthHandler(api_key, api_secret_key)
aut.set_access_token(access_token, access_token_secret)

api = tweepy.API(aut, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

"""#Tweets del home del usuario 
---
"""

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

"""#Seguidos por la cuenta
---
"""

for friend in tweepy.Cursor(api.friends).items():
    print(friend.name)

"""#Datos a trabajar
---
Teniendo en cuenta lo que nos brinda el modulo de tweepy, conseguimos los últimos 100 twits que contengan la palabra mascota para hacer un análisis correspodiente a ellos:
"""

#Ingresando datos
datosMascotas = pd.read_csv("result.csv", names = ["fechaTweet", "tweet", "numeroLikes", "numeroRetweets", "longitud"])
datosMascotas

"""#Datos sobre mascotas
---

## Analisis de relacion entre likes y retweets con la longitud de los Tweets
___

Se realiza un analizis de relacion entre likes y retweets con respecto a la longitud de los tweets y se ve una pequeña tendencia a tener mas Likes o Retweets si la longitud de estos es mas grande
"""

datosMascotas.plot(kind='scatter',x='numeroLikes',y='numeroRetweets',c='longitud', colormap='viridis')
plt.show()

"""#Análisis de relación entre las mascotas
---
Se realiza un análisis con relación a las máscotas para ver en los datos que se obtuvieron las mascotas nombradas, teniendo en cuenta que en su mayoría pueden ser perros o gatos.
"""

perros = []
gatos = []
otros = []

for i in range(0, 1000):
  if('perro' in datosMascotas[['tweet']][i:i+1].to_string()):
    perros.append(datosMascotas[['tweet']][i:i+1].to_string())
  elif('gato' in datosMascotas[['tweet']][i:i+1].to_string()):
    gatos.append(datosMascotas[['tweet']][i:i+1].to_string())
  else:
    otros.append(datosMascotas[['tweet']][i:i+1].to_string())

names = ['gatos', 'perros']
values = [len(gatos), len(perros)]

plt.bar(names, values)
plt.title('Grafica comparativa entre gatos y perros')
plt.show()

"""## Analisis con estadistica discreta
___

Se aplican diferentes medidas de tendencia central en este caso para las variables de likes, longitud y retweets
las medidas usadas son:
* Media
* Mediana
* Sesgo Estadistico
* Varianza
* Error Estandar
"""

dataLikes=pd.DataFrame(datosMascotas['numeroLikes'])
dataRetweets=pd.DataFrame(datosMascotas['numeroRetweets'])
dataLongitud=pd.DataFrame(datosMascotas['longitud'])
frames1=[dataLikes,dataRetweets]
dataLikesRetweets=pd.concat(frames1, ignore_index = False, sort = False)
frames2=[dataLikesRetweets,dataLongitud]
dataLikesRetweetsLongitud=pd.concat(frames2, ignore_index = False, sort = False)
print(dataLikesRetweetsLongitud.agg(['mean', 'median','skew','var','std']))

"""#Maltrato animal

---
"""

msgs = []
msg =[]

for tweet in tweepy.Cursor(api.search, q='maltrato mascotas', rpp=2000).items():
    msg = [tweet.user.name,tweet.text, tweet.source, tweet.created_at,tweet.user.location] 
    msg = tuple(msg)                    
    msgs.append(msg)

dataframeMaltratoMascotas = pd.DataFrame(msgs,columns=['Usuario','Texto', 'Dispositivo', 'Fecha Creacion','Ubicacion'])

msgs = []
msg =[]

for tweet in tweepy.Cursor(api.search, q='violencia mascotas', rpp=2000).items():
    msg = [tweet.user.name,tweet.text, tweet.source, tweet.created_at, tweet.user.location] 
    msg = tuple(msg)                    
    msgs.append(msg)

dataframeViolenciaMascotas = pd.DataFrame(msgs,columns=['Usuario','Texto', 'Dispositivo', 'Fecha Creacion','Ubicacion'])

frames1=[dataframeMaltratoMascotas,dataframeViolenciaMascotas]
dataFrameMaltrato=pd.concat(frames1, ignore_index = True)
dataFrameMaltrato

"""#Análisis dispositvos
---
Dispositivos desde los que se hicieron estos tipos de twits
"""

def Porcentaje(Series):
    return (Series*100)/150
    
    
serieDispositivos=dataFrameMaltrato['Dispositivo'].value_counts()
serieDispositivos=serieDispositivos.pipe(Porcentaje)
dataDispositivos= pd.DataFrame(serieDispositivos)
dataDispositivos

fig, ax = plt.subplots(figsize=(7, 7))

size = 0.4
cmap = plt.get_cmap("tab20c")
explode = (0.1,0.1,0.1, 0.1, 0.1, 0.1,0.1,0.1)
outer_colors = cmap(np.arange(7))
ax.pie(dataDispositivos['Dispositivo'],autopct='%1.1f%%',radius=1.3,startangle=10,explode=explode,labels="Dispositivo: " +dataDispositivos.index,colors=outer_colors)