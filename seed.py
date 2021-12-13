import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trade.settings')
django.setup()

from trading_outpost.models import Card

def get_teams():
  url = 'http://lookup-service-prod.mlb.com/json/named.team_all_season.bam'
  paramaters = {
    'sport_code': '\'mlb\'',
    'season' : 2021
  }
  r = requests.get(url, headers={'Content-Type': 'application/json'}, params = paramaters)
  teams = r.json()
  return teams['team_all_season']['queryResults']['row']


def players_by_team(team_id):
  url = 'http://lookup-service-prod.mlb.com/json/named.roster_40.bam'
  paramaters = {
    'sport_code': '\'mlb\'',
    'team_id' : team_id
  }
  r = requests.get(url, headers={'Content-Type': 'application/json'}, params = paramaters)
  players = r.json()
  if players['roster_40']['queryResults']['totalSize'] == '0':
    return []
  return players['roster_40']['queryResults']['row']

def player_detail(player_id):
  if not player_id:
    return None
  url = 'http://lookup-service-prod.mlb.com/json/named.player_info.bam'
  paramaters = {
    'sport_code': '\'mlb\'',
    'player_id' : f'\'{player_id}\''
  }
  r = requests.get(url, headers={'Content-Type': 'application/json'}, params = paramaters)
  if r.text == 'There was a problem with your request.':
    return None
  details = r.json()
  return details ['player_info']['queryResults']['row']


# def populate_database():
teams = get_teams()
for team in teams:
  team_id = team['team_id']
  players = players_by_team(team_id)
  for player in players:
    player_id = player['player_id']
    details = player_detail(player_id)
    print(json.dumps(details, indent =2))
    if details:
      print('Creating card')
      cards = Card.objects.create(name = details['name_full'], position = details['primary_position_txt'])
      print(cards)
# populate_database()