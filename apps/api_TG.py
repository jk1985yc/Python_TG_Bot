import requests, configparser, json

# Use configparser file
config=configparser.ConfigParser()
config.read('config.ini')

url='https://api.telegram.org'

# Token save to variable
TOKEN=(config.get('TELEGRAM', 'ACCESS_TOKEN'))

# Telegram Bot Get status API
getINFO_URL=f'{url}/bot{TOKEN}/getUpdates'

# Get response save to {data}
res=requests.get(getINFO_URL)
data=json.loads(res.text)
data=data['result']

def offset_updates():
    # Offset updates queue
    try:
        last_id = data[-1]['update_id']
        response=requests.post(f'{url}/bot{TOKEN}/getUpdates', data={'offset':{last_id+1}})
        return response
    except:
        print('No DATA!!')

def get_chatID():
    result={}
    # Save filter data to file
    try:
        for d in data:
            if 'message' in d:
                d=d['message']
                if 'chat' in d:
                    d=d['chat']
                    keys=d['title']
                    values=d['id']
                    result[keys]=values
    except:
        print('NoDATA')

    # write data in file
    with open('chatID_List.txt', 'a', encoding='UTF-8') as f:
        for key, val in result.items():
            f.write(str(key) + ' = ' + str(val) + '\n')

get_chatID()