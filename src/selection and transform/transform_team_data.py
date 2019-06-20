import pandas as pd

matchs = pd.DataFrame()
team_dict = pd.DataFrame()
scouts = pd.DataFrame()


def replace_slug_by_name(slug):
    name = team_dict[team_dict['Slug'] == slug]['Nome'].values
    return name[0]


def match_result(team, round):
    match = matchs[((matchs['home_team'] == team) |
                    (matchs['away_team'] == team)) &
                   (matchs['round'] == round)]['score'].values[0].split('x')

    is_home = matchs[(matchs['home_team'] == team) & (matchs['round'] == round)].shape[0]

    if is_home == 1:
        if int(match[0]) > int(match[1]):
            return 3

        elif int(match[0]) < int(match[1]):
            return 0

        return 1

    if int(match[0]) > int(match[1]):
        return 0

    elif int(match[0]) < int(match[1]):
        return 3

    return 1


def cs_per_round(row, data):
    team = row['team']
    round = row['round']

    data = data[data['team'] == team]
    data = data[data['round'] <= round]

    score = data['result_match'].sum()

    return score


def is_home_team(team, round):
    is_home = matchs[(matchs['home_team'] == team) &
                     (matchs['round'] == round)].shape[0]
    return is_home


def goals_conceded(team, round):  # only current GKs

    data = scouts[scouts['Rodada'] == round]

    team = data[data['atletas.clube.id.full.name'] == team]

    return team['GS'].sum()


def goals_scored(team, round):  # only current players

    data = scouts[scouts['Rodada'] == round]

    team = data[data['atletas.clube.id.full.name'] == team]

    return team['G'].sum()


def wcg(team, round):  # only current GKs

    data = scouts[scouts['Rodada'] == round]

    team = data[(data['atletas.clube.id.full.name'] == team)
                & (data['atletas.posicao_id'] == 'gol')]

    return team['SG'].sum()


def ag_scored(team, round):
    goals = goals_scored(team, round)
    avg = goals / round

    return avg


def ag_conceded(team, round):
    goals = goals_conceded(team, round)
    avg = goals / round

    return avg


def generate(year):
    year = str(year)
    print('- - - ' + year + ' - - -')
    print('Loading data...')

    sep = ';' if year == '2017' else ','

    matchs = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/' + year + '/' + year + '_partidas.csv')
    team_dict = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/' + year + '/' + year + '_times.csv',
                            sep=sep)
    scouts = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/' + year + '/' + year + '_scouts_raw.csv')

    team_names = team_dict['Nome'].values

    tr = pd.DataFrame({'team': [], 'round': []})

    for i in range(1, 39):
        df = pd.DataFrame({'team': team_names,
                           'round': [i] * 20})
        tr = tr.append(df, sort=False)

    tr['round'] = tr['round'].astype(int)

    print('Processing...')

    matchs['home_team'] = matchs.apply(lambda row: replace_slug_by_name(row['home_team']), axis=1)
    matchs['away_team'] = matchs.apply(lambda row: replace_slug_by_name(row['away_team']), axis=1)

    tr['result_match'] = tr.apply(lambda row: match_result(row['team'], row['round']), axis=1)
    tr['championship_score'] = tr.apply(lambda row: cs_per_round(row, tr), axis=1)
    tr['home_team'] = tr.apply(lambda row: is_home_team(row['team'], row['round']), axis=1)
    tr['goals_conceded'] = tr.apply(lambda row: goals_conceded(row['team'], row['round']), axis=1)
    tr['goals_scored'] = tr.apply(lambda row: goals_scored(row['team'], row['round']), axis=1)
    tr['ag_scored'] = tr.apply(lambda row: ag_scored(row['team'], row['round']), axis=1)  # goal average scored
    tr['ag_conceded'] = tr.apply(lambda row: ag_conceded(row['team'], row['round']), axis=1)  # goal average conceded
    tr['wcg'] = tr.apply(lambda row: wcg(row['team'], row['round']), axis=1)  # without conceding a goal

    print('Writing csv')
    tr.to_csv('/content/gdrive/My Drive/Data Science/Cartola/transformed/tr_' + year + '.csv')
