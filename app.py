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

def get_league_data(api_key, region='na1'):
    urls = {
        "challenger": f"https://{region}.api.riotgames.com/tft/league/v1/challenger?api_key={api_key}",
        "grandmaster": f"https://{region}.api.riotgames.com/tft/league/v1/grandmaster?api_key={api_key}",
        "master": f"https://{region}.api.riotgames.com/tft/league/v1/master?api_key={api_key}"
    }

    combined_entries = []

    # Fetch and combine entries from Challenger, Grandmaster, and Master tiers
    for tier, url in urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            combined_entries += data['entries']  # Combine entries from all tiers
        else:
            print(f"Error fetching data from {url}")

    # Sort by LP in descending order
    combined_entries.sort(key=lambda x: x['leaguePoints'], reverse=True)

    # Calculate cutoffs with default values for insufficient player count
    total_players = len(combined_entries)
    challenger_cutoff = combined_entries[249]['leaguePoints'] if total_players > 249 else 500
    grandmaster_cutoff = combined_entries[749]['leaguePoints'] if total_players > 749 else 250

    cutoffs = {
        "challenger": challenger_cutoff,
        "grandmaster": grandmaster_cutoff
    }

    return cutoffs

def get_tier_data(api_key, region='na1', tier='challenger'):
    url = f"https://{region}.api.riotgames.com/tft/league/v1/{tier}?api_key={api_key}"
    response = requests.get(url)
    tier_list = []

    if response.status_code == 200:
        data = response.json()
        for entry in data['entries']:
            tier_list.append((entry['summonerName'], entry['leaguePoints']))

    # Sort the list by LP in descending order
    tier_list.sort(key=lambda x: x[1], reverse=True)
    
    return tier_list

@app.route('/')
def home():
    api_key = 'RGAPI-70a43f21-2961-483a-93a6-a2626550801a' # Replace with a valid Riot Developer API
    region = 'na1' 
    cutoffs = get_league_data(api_key, region)
    challenger_list = get_tier_data(api_key, region, 'challenger')
    grandmaster_list = get_tier_data(api_key, region, 'grandmaster')
    
    try:
        with open('historical_data.json', 'r') as file:
            historical_data = json.load(file)
    except FileNotFoundError:
        historical_data = {"challenger": [], "grandmaster": []}

    return render_template('index.html', cutoffs=cutoffs, historical_data=historical_data, challenger_list=challenger_list, grandmaster_list=grandmaster_list)

if __name__ == '__main__':
    app.run(debug=True)