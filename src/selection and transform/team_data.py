import pandas as pd
import numpy as np

def get_round(round, year=2018):
  data = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/' + str(year) + '/rodada-' + str(round) + '.csv')
  return data

round1 = get_round(1)
team_names = round1['atletas.clube.id.full.name'].unique() 
team_names

"""## Create team-round dataframe"""

tr = pd.DataFrame({'team':[], 'round':[]})

tr['goals_conceded'] = []
tr['goals_scored'] = []
tr['play_home'] = []
tr['ga_scored'] = [] # goal average scored
tr['ga_conceded'] = [] # goal average conceded
tr['wcg'] = [] # without conceding a goal
tr['last_match'] = [] # points obtained in the last match.

for i in range(2,21):
  df = pd.DataFrame({'team': team_names,
                  'round': [i]*20})
  tr = tr.append(df, sort=False)

tr['round'] = tr['round'].astype(int) 
tr['round'].unique()

tr.head()

all_rounds = []

for i in range(1, 39):
  all_rounds.append(get_round(i))

len(all_rounds)

def goals_conceded(team, round): # only current GKs
  round -= 1
  data = all_rounds[round]
  
  team = data[data['atletas.clube.id.full.name'] == team]
  
  return team['GS'].sum()


def goals_scored(team, round): # only current players
  round -= 1
  data = all_rounds[round]
  
  team = data[data['atletas.clube.id.full.name'] == team]
  
  return team['G'].sum()


def wcg	(team, round): # only current GKs
  round -= 1
  data = all_rounds[round]
  
  team = data[(data['atletas.clube.id.full.name'] == team) 
             & (data['atletas.posicao_id'] == 'gol')]
  
  return team['SG'].sum()


def ag_scored(team, round):
  
  goals = goals_scored(team, round)
  avg = goals/round
  
  return avg


def ag_conceded(team, round):
  
  goals = goals_conceded(team, round)
  avg = goals/round
  
  return avg

final_table = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/tabela_final_2018.csv')

def last_match_score(team, round):
  
  if round == 1:
    return 0
    
  current = final_table[final_table['time'] == team][str(round - 1)].sum()
  last = 0
  
  if round != 2:
    last = final_table[final_table['time'] == team][str(round - 2)].sum()
  
  return current - last

