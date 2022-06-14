import requests, configparser, json

# Use configparser file
config=configparser.ConfigParser()
config.read('config.ini')

# Token save to variable
TOKEN=(config.get('TELEGRAM', 'ACCESS_TOKEN'))

# Telegram Bot Get status API
getINFO_URL=f'https://api.telegram.org/bot{TOKEN}/getUpdates'

# Get response save to {data}
res=requests.get(getINFO_URL)
data=json.loads(res.text)

data=data['result']

# Save filter data to file
with open('chatID_List.txt', 'a') as f:
    for d in data:
        if 'message' in d:
            d=d['message']
            if 'chat' in d:
                d=d['chat']
                key=d['title']
                value=d['id']
                f.write(str(key) + ' = ' + str(value) + '\n')