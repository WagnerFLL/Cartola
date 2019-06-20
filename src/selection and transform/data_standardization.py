import pandas as pd

team_dict = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/times_ids.csv')

scouts_2014 = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/2014/2014_scouts_raw.csv')
scouts_2015 = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/2015/2015_scouts_raw.csv')
scouts_2016 = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/2016/2016_scouts_raw.csv')
scouts_2017 = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/2017/2017_scouts_raw.csv')

players_2016 = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/2016/2016_jogadores.csv')
players_2015 = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/2015/2015_jogadores.csv')
players_2014 = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/2014/2014_jogadores.csv')
positions = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/posicoes_ids.csv')
teams_2017 = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/2017/2017_times.csv', sep=';')

dict_2014 = {'Atleta': 'atleta_id','Rodada':'rodada','Clube':'clube_id','Posicao':'atleta_posicao_id',
             'Pontos':'pontuacao','PontosMedia':'pontuacao_media','Preco':'preco','PrecoVariacao':'preco_variacao'}
dict_2015 = {"Rodada":'rodada',"ClubeID":'clube_id',"AtletaID":'atleta_id',"Pontos":'pontuacao',
             "PontosMedia":'pontuacao_media',"Preco":'preco',"PrecoVariacao":'preco_variacao'}
dict_2016 = {"Rodada":'rodada',"ClubeID":'clube_id',"AtletaID":'atleta_id',"Pontos":'pontuacao',
             "PontosMedia":'pontuacao_media',"Preco":'preco',"PrecoVariacao":'preco_variacao'}
dict_2017 = {'atletas.apelido':'atleta_apelido','atletas.atleta_id':'atleta_id','atletas.clube.id.full.name':'clube_nome',
             'atletas.clube_id':'clube_id','atletas.media_num':'pontuacao_media','atletas.nome':'atleta_nome',
             'atletas.pontos_num':'pontuacao','atletas.posicao_id':'posicao','atletas.preco_num':'preco','Rodada':'rodada',
             'atletas.variacao_num':'preco_variacao'}
dict_2018 = {"atletas.nome":'atleta_nome',"atletas.slug":'atleta_slug',"atletas.apelido":'atleta_apelido',
             "atletas.atleta_id":'atleta_id',"atletas.rodada_id":'rodada',"atletas.clube_id":'clube_id',
             "atletas.posicao_id":'posicao',"atletas.pontos_num":'pontuacao',"atletas.preco_num":'preco',
             "atletas.variacao_num":'preco_variacao',"atletas.media_num":'pontuacao_media',
             "atletas.clube.id.full.name":'clube_nome'}

scouts_2014.rename(columns=dict_2014, inplace=True)
scouts_2015.rename(columns=dict_2015, inplace=True)
scouts_2016.rename(columns=dict_2016, inplace=True)
scouts_2017.rename(columns=dict_2017, inplace=True)


def get_round(round, year=2018):
    data = pd.read_csv('/content/gdrive/My Drive/Data Science/Cartola/' + str(year) + '/rodada-' + str(round) + '.csv')
    return data


scouts_2018 = pd.DataFrame()
all_rounds = []
for i in range(1, 39):
    all_rounds.append(get_round(i))

scouts_2018 = pd.concat(all_rounds, ignore_index=True, sort=False)
scouts_2018.rename(columns=dict_2018, inplace=True)


def position_abbr_2016(id):
    pos_id = players_2016[players_2016['ID'] == id]['PosicaoID'].values[0]
    pos = positions[positions['Cod'] == pos_id]['abbr'].values[0]

    return pos


def position_abbr_2015(id):
    pos_id = players_2015[players_2015['ID'] == id]['PosicaoID'].values[0]
    pos = positions[positions['Cod'] == pos_id]['abbr'].values[0]

    return pos


def position_abbr_2014(id):
    pos_id = players_2014[players_2014['ID'] == id]['PosicaoID'].values[0]
    pos = positions[positions['Cod'] == pos_id]['abbr'].values[0]

    return pos


def clube_id_2017(abbr):
    id = teams_2017[teams_2017['Abreviacao'] == abbr]['ID'].values[0]

    return id


def clube_id_2014(atleta_id):
    id = players_2014[players_2014['ID'] == atleta_id]['ClubeID'].values[0]

    return id


def clube_id_2016(atleta_id):
    id = players_2016[players_2016['ID'] == atleta_id]['ClubeID'].values[0]

    return id


def clube_id_2018(abbr):
    id = team_dict[team_dict['abreviacao'] == abbr]['id'].values[0]

    return id


scouts_2015['posicao'] = scouts_2015.apply(lambda  row: position_abbr_2015(row['atleta_id']), axis=1)
scouts_2016['posicao'] = scouts_2016.apply(lambda  row: position_abbr_2016(row['atleta_id']), axis=1)
scouts_2014['posicao'] = scouts_2014.apply(lambda  row: position_abbr_2014(row['atleta_id']), axis=1)
scouts_2017['clube_id'] = scouts_2017.apply(lambda  row: clube_id_2017(row['clube_id']), axis=1)
scouts_2014['clube_id'] = scouts_2014.apply(lambda  row: clube_id_2014(row['atleta_id']), axis=1)
scouts_2016['clube_id'] = scouts_2016.apply(lambda  row: clube_id_2016(row['atleta_id']), axis=1)
scouts_2018['clube_id'] = scouts_2018.apply(lambda  row: clube_id_2018(row['clube_id']), axis=1)

columns = ['rodada', 'atleta_id', 'clube_id', 'pontuacao', 'pontuacao_media', 'preco', 'preco_variacao', 'posicao',
           'FS', 'PE', 'A', 'FT', 'FD', 'FF', 'G', 'I', 'PP', 'RB', 'FC', 'GC', 'CA', 'CV', 'SG', 'DD', 'DP', 'GS']

scouts_2014 = scouts_2014[columns]
scouts_2015 = scouts_2015[columns]
scouts_2016 = scouts_2016[columns]
scouts_2017 = scouts_2017[columns]
scouts_2018 = scouts_2018[columns]

scouts_2014.to_csv('/content/gdrive/My Drive/Data Science/Cartola/Standardized/scouts_2014.csv', index=False)
scouts_2015.to_csv('/content/gdrive/My Drive/Data Science/Cartola/Standardized/scouts_2015.csv', index=False)
scouts_2016.to_csv('/content/gdrive/My Drive/Data Science/Cartola/Standardized/scouts_2016.csv', index=False)
scouts_2017.to_csv('/content/gdrive/My Drive/Data Science/Cartola/Standardized/scouts_2017.csv', index=False)
scouts_2018.to_csv('/content/gdrive/My Drive/Data Science/Cartola/Standardized/scouts_2018.csv', index=False)
