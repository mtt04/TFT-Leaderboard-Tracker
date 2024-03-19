from flask import Flask, render_template
import requests
import json
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)

def update_historical_data(new_challenger, new_grandmaster):
    try:
        with open('historical_data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"challenger": [], "grandmaster": []}
    
    data['challenger'] = data['challenger'][1:] + [new_challenger]
    data['grandmaster'] = data['grandmaster'][1:] + [new_grandmaster]

    with open('historical_data.json', 'w') as file:
        json.dump(data, file)

def fetch_and_update_data():
    api_key = 'RGAPI-5a9bf1ee-4416-4c5c-9402-39456dfda31a'
    region = 'na1'
    cutoffs = get_league_data(api_key, region)
    
    update_historical_data(cutoffs['challenger'], cutoffs['grandmaster'])
    print("Historical data updated")

scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_and_update_data, trigger="interval", minutes=1440) # Run daily
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

def get_league_data(api_key, region='na1'):
    urls = {
        "challenger": f"https://{region}.api.riotgames.com/tft/league/v1/challenger?api_key={api_key}",
        "grandmaster": f"https://{region}.api.riotgames.com/tft/league/v1/grandmaster?api_key={api_key}",
        "master": f"https://{region}.api.riotgames.com/tft/league/v1/master?api_key={api_key}"
    }

    combined_entries = []

    for url in urls.values():
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            combined_entries += data['entries']
        else:
            print(f"Error fetching data from {url}")

    # Sort by LP in descending order
    combined_entries.sort(key=lambda x: x['leaguePoints'], reverse=True)

    # Calculate cutoffs
    cutoffs = {
        "challenger": combined_entries[249]['leaguePoints'] if len(combined_entries) > 249 else "N/A",
        "grandmaster": combined_entries[749]['leaguePoints'] if len(combined_entries) > 749 else "N/A"
    }

    return cutoffs

@app.route('/')
def home():
    api_key = 'RGAPI-5a9bf1ee-4416-4c5c-9402-39456dfda31a'
    region = 'na1' 
    cutoffs = get_league_data(api_key, region)
    
    try:
        with open('historical_data.json', 'r') as file:
            historical_data = json.load(file)
    except FileNotFoundError:
        historical_data = {"challenger": [], "grandmaster": []}

    return render_template('index.html', cutoffs=cutoffs, historical_data=historical_data)

if __name__ == '__main__':
    app.run(debug=True)