import pandas as pd
import numpy as np
import re
def preprocess(data):
    pattern = "\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ')
    df['message_date'] = df['message_date'].str.rstrip(' -')
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p', errors='coerce')
    df['time'] = df['message_date'].dt.strftime('%I:%M %p')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    user = []
    message = []
    for i in df['user_message']:
        entry = re.split('([\w\W]+?):\s', i)
        if entry[1:]:  # username
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append('Group_notification')
            message.append(entry[0])
    df['user'] = user
    df['message'] = message

    df.drop(columns=['user_message'], inplace=True)
    df['Year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day_Name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day.astype(int)
    df['hour'] = df['date'].dt.strftime('%I').astype(int)
    df['minute'] = df['date'].dt.strftime('%M').astype(int)

    df['hour'] = pd.to_datetime(df['time'], format='%I:%M %p').dt.hour

    # Create the 'period' column
    df['period'] = (
            (df['hour'] % 12).replace(0, 12).astype(str) +  # Start hour in 12-hour format
            np.where(df['hour'] < 12, ' AM', ' PM') +  # Add AM/PM for the start hour
            ' - ' +
            ((df['hour'] + 1) % 12).replace(0, 12).astype(str) +  # End hour in 12-hour format
            np.where((df['hour'] + 1) % 24 < 12, ' AM', ' PM')  # Add AM/PM for the end hour
    )

    return df

