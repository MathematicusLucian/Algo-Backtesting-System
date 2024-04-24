import pandas as pd
import matplotlib.pyplot as plt
import requests
from pytube import YouTube
from transformers import pipeline
from src.utils.utils import get_envar

key = get_envar('YouTube_API_key')

def yt_id(url):
  yt = YouTube(url)
  channel_id = yt.channel_id
  return channel_id

def get_channel_data(key, id):
  channel_data = []
  res = f'https://www.googleapis.com/youtube/v3/search?key={key}&channelId={id}&part=snippet,id&order=date&maxResults=25'
  r = requests.get(res)
  data = r.json()

  for x in range(len(data['items'])):

    publish = data['items'][x]['snippet']['publishedAt']
    title = data['items'][x]['snippet']['title']
    description = data['items'][x]['snippet']['description']
    channel_name = data['items'][x]['snippet']['channelTitle']

    video_info = {
        'publish':publish,
        'title':title,
        'description':description,
        'channel_name':channel_name
    }

    channel_data.append(video_info)
    df = pd.DataFrame(channel_data)
  return df

videos = [
    'https://www.youtube.com/watch?v=RKFxWzJuQTw',
    'https://www.youtube.com/watch?v=Xa5cc8mgczc',
    'https://www.youtube.com/watch?v=EP6JqpjtUjM'
    ]

channel_ids = []
for video in videos:
  id = yt_id(video)
  channel_ids.append(id)

yahoo = get_channel_data(key, channel_ids[0])
cnbc = get_channel_data(key, channel_ids[1])
bloomberg = get_channel_data(key, channel_ids[2])
df = pd.concat([yahoo,cnbc,bloomberg])
df = df.reset_index(drop=True)
df.sample(7)

pipe = pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

df['sentiment_label'] = ''
df['sentiment_score'] = ''
for x in df.index:
  results = pipe(df.title[x] + df.description[x])
  df['sentiment_label'][x] = results[0]['label']
  df['sentiment_score'][x] = results[0]['score']

yf_sentiment = df[df['channel_name'] == 'Yahoo Finance']['sentiment_label'].value_counts()
plt.pie(yf_sentiment, labels=yf_sentiment.index)
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('Yahoo Finance Sentiment Details')
plt.show()

cnbc_sentiment = df[df['channel_name'] == 'CNBC Television']['sentiment_label'].value_counts()
plt.pie(yf_sentiment, labels=yf_sentiment.index)
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('CNBC Sentiment Details')
plt.show()

bloomberg_sentiment = df[df['channel_name'] == 'Bloomberg Television']['sentiment_label'].value_counts()
plt.pie(yf_sentiment, labels=yf_sentiment.index)
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('Bloomberg Television Sentiment Details')
plt.show()

df['publish'] = pd.to_datetime(df['publish'])
df['date'] = df['publish'].dt.date
date_grouped = df.groupby(['date'])['sentiment_label'].value_counts()
date_grouped = date_grouped.unstack(level=1)
date_grouped.plot.bar()