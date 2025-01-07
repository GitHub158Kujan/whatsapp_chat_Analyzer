import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    #total messages
    num_mess=df.shape[0]
    words=[]
   #total words
    for messages in df['message']:
      if not messages.startswith('<') or not messages.startswith('Messages and calls are end-to-end encrypted.'):
          words.extend(messages.split())
    #media shared
    media = df[df['message']=='<Media omitted>\n'].shape[0]

    #links
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_mess, len(words) ,media, len(links)

def most_busy_users(df):
    df = df[df['user'] != 'Group_notification']
    x = df['user'].value_counts().head()
    new_df = round(df['user'].value_counts() / df['user'].shape[0] * 100, 2).reset_index().rename(
        columns={'count': 'percentage'})

    return x,new_df

def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    temp_df = df[df['user'] != 'Group_notification']
    temp_df = temp_df[temp_df['message'] != '<Media omitted>\n']
    wc=WordCloud(width=300,height=300,min_font_size=10,background_color='white')
    df_wc=wc.generate(temp_df['message'].str.cat(sep=' '))
    return df_wc


def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'Group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return_df=pd.DataFrame(Counter(words).most_common(20),columns=['word', 'count'])
    return_df = return_df.sort_values(by='count', ascending=True)
    return return_df

def most_common_emoji(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    emojis=[]
    for message in df['message']:
            emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['Year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['Year'][i]))
    timeline['time'] = time
    return timeline

def day_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    day_time=df['day_Name'].value_counts()
    return day_time

def month_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    month_time=df['month'].value_counts()
    return month_time

def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    heatmap=df.pivot_table(index='day_Name', columns='period', values='message', aggfunc='count').fillna(0)
    return heatmap

