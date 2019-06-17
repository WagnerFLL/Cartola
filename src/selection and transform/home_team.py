import pandas as pd


def match_at_home(team):
    home = matchs[matchs['home_team'] == team]['round']
    home = list(home)
    total = [1 if i in home else 0 for i in range(1, 39)]

    return total


matchs = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/2018/2018_partidas.csv')

team_dict = {'Cruzeiro': 'Cruzeiro - MG', 'Atlético-PR': 'Atlético - PR',
             'América-MG': 'América - MG', 'Vitória': 'Vitória - BA',
             'Vasco': 'Vasco da Gama - RJ', 'Botafogo': 'Botafogo - RJ',
             'São Paulo': 'São Paulo - SP', 'Santos': 'Santos - SP',
             'Corinthians': 'Corinthians - SP', 'Internacional': 'Internacional - RS',
             'Atlético-MG': 'Atlético - MG', 'Paraná': 'Paraná - PR',
             'Chapecoense': 'Chapecoense - SC', 'Bahia': 'Bahia - BA',
             'Fluminense': 'Fluminense - RJ', 'Flamengo': 'Flamengo - RJ',
             'Ceará': 'Ceará - CE', 'Sport': 'Sport - PE',
             'Palmeiras': 'Palmeiras - SP', 'Grêmio': 'Grêmio - RS'}

team_dict = {v: k for k, v in team_dict.items()}

matchs.replace({'home_team': team_dict, 'away_team': team_dict}, inplace=True)
teams = matchs['home_team'].unique()

data = pd.DataFrame(columns=['team'] + list(range(1, 39)))
data['team'] = teams

for i, row in data.iterrows():
    home_list = match_at_home(row['team'])

    for x in range(1, 39):
        data.loc[i, x] = home_list[x - 1]

data.to_csv('/content/gdrive/My Drive/Data Science/Cartola/2018/mandantes.csv', index=False)
