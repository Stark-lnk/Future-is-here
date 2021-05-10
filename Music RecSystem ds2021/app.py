import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
from dash.dependencies import Output, Input
import random

table_greeting = ['Смотри что мы тебе подобрали!', 'А мне нравится твой вкус!', 'Бомбические песни строкой ниже ;)',
                  'Это точно поднимет настроение😉', 'Лучшие треки только у нас🤩', 'Прекрасный выбор))0)',
                  "Мне тоже нравится❤"]

data = pd.read_csv("data/tracks3.csv").sample(30000).reset_index(drop=True)
data['artists'] = data['artists'].map(lambda x: ', '.join(x[1:-1].replace("'", '').split(',')))
# all_artists = pd.read_csv("data/artists.csv")['0']
# song_names = pd.read_csv("data/song_names.csv")['name']

try:
    data['release_date'] = data['release_date'].map(lambda x: int(x[:4]))
    data.dropna(inplace=True)
except:
    pass


# ________________________________-functions-________________________________
# get list of artists
def get_all_artists(artist_col):
    all_artists = []
    for artist_block in artist_col:
        artists = artist_block.split(',')
        for artist in artists:
            if artist not in all_artists:
                all_artists.append(artist)
    return all_artists


# generate html table
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


# transform table into readable view
def show_final_df(df):
    df = df.loc[:, ['name', 'popularity', 'artists', 'release_date']]
    df.rename(columns={'name': 'Название песни', 'popularity': 'Популярность', 'artists': 'Исполнитель',
                       'release_date': 'Год выпуска'}, inplace=True)
    # df['Исполнитель'] = df['Исполнитель'].map(lambda x: ', '.join(x[1:-1].replace("'", '').split(',')))
    return df


# ________________________________ # ________________________________
# ccs styles
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        {
                            "href": "https://fonts.googleapis.com/css2?"
                                    "family=Lato:wght@400;700&display=swap",
                            "rel": "stylesheet",
                        },
                        ]
# initialization
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Music filters for everyone"

# ________________________________ # ________________________________
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🎵", className="header-emoji"),
                html.H1(
                    children="Продвинутые музыкальные фильтры", className="header-title"
                ),
                html.P(
                    children="С нашей системой можно найти подборку под любую ситуацию и настроение!"
                             " Вы сможете настроить все необходимые для этого фильтры, выбрать год релиза, танцевальность, "
                             "акустичность и многое другое! От вас потребуется лишь пара минут и подборка готова!",
                    className="header-description",
                ),
            ],
            className="header", ),

        # ________________________________Menu Block 1______________________________________
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Исполнитель", className="menu-title"),
                        dcc.Dropdown(
                            id="artist-filter",
                            options=[
                                # {"label": artist0, "value": artist0}
                                # for artist0 in list(all_artists)
                                {"label": artist, "value": artist}
                                for artist in get_all_artists(data['artists'].unique())
                            ],
                            value="Выбери название песни",
                            clearable=False,
                            className="dropdown",
                            multi=True,
                            placeholder="Выбери любимого испольнителя"
                        ),
                    ]
                ), ],
            className="menu", ),

        # ________________________________-Sliders-________________________________
        html.Div(
            children=[
                # 1
                html.Div(
                    children="Год релиза",
                    className="menu-title"),

                dcc.RangeSlider(
                    id='year-slider',
                    min=1900,
                    max=2021,
                    step=1,
                    value=[1900, 2021],
                    marks={'1900': '1900', '2021': '2021'}
                ),
                html.Div(id='output-year-slider', className='output-style'),
                # 2
                html.Div(
                    children="Уровень танцевальности",
                    className="menu-title"),

                dcc.RangeSlider(
                    id='danceability-slider',
                    min=0,
                    max=1,
                    step=0.01,
                    value=[0, 1],
                    marks={'0': '0%', '1': '100%'}
                ),
                html.Div(id='output-danceability-slider', className='output-style'),
                # 3
                html.Div(
                    children="Энергичность",
                    className="menu-title"),

                dcc.RangeSlider(
                    id='energy-slider',
                    min=0,
                    max=1,
                    step=0.01,
                    value=[0, 1],
                    marks={'0': '0%', '1': '100%'}
                ),
                html.Div(id='output-energy-slider', className='output-style'),

            ],
            className="sliders"),

        html.Div(
            children=[
                # 1
                html.Div(
                    children="Живость",
                    className="menu-title"),

                dcc.RangeSlider(
                    id='liveness-slider',
                    min=0,
                    max=1,
                    step=0.01,
                    value=[0, 1],
                    marks={'0': '0%', '1': '100%'}
                ),
                html.Div(id='output-liveness-slider', className='output-style'),
                # 2
                html.Div(
                    children="Насыщенность словами",
                    className="menu-title"),

                dcc.RangeSlider(
                    id='speechiness-slider',
                    min=0,
                    max=1,
                    step=0.01,
                    value=[0, 1],
                    marks={'0': '0%', '1': '100%'}
                ),
                html.Div(id='output-speechiness-slider', className='output-style'),
                # 3
                html.Div(
                    children="Акустичность",
                    className="menu-title"),

                dcc.RangeSlider(
                    id='acousticness-slider',
                    min=0,
                    max=1,
                    step=0.01,
                    value=[0, 1],
                    marks={'0': '0%', '1': '100%'}
                ),
                html.Div(id='output-acousticness-slider', className='output-style'),

            ],
            className="sliders"),

        # ________________________________-Table with results-________________________________
        html.Div(children=[
            html.H5(children=random.choice(table_greeting)),
            dcc.Interval(id='main-table-interval', interval=1000),
            dash_table.DataTable(
                id='main-table',
                data=[],
                editable=False,
                style_cell_conditional=[
                    {'if': {'column_id': 'Название песни'}, 'width': '40%'},
                    {'if': {'column_id': 'Исполнитель'}, 'width': '40%'},
                    {'if': {'column_id': 'Популярность'}, 'width': '10%'},
                    {'if': {'column_id': 'Год выпуска'}, 'width': '10%'},
                ],
                style_header={'backgroundColor': 'rgb(230, 230, 230)',
                              'fontWeight': 'bold'},
                style_data_conditional=[
                    {'if': {'row_index': 'odd'},
                     'backgroundColor': 'rgb(248, 248, 248)'}
                ],
                style_table={'table-layout': 'fixed'},
                style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0
                }
            )
        ], className="table-top"),

        # ________________________________-Menu Block 2-________________________________
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Название песни", className="menu-title"),
                        dcc.Dropdown(
                            id="song-name-filter",
                            options=[
                                {"label": song_name, "value": song_name}
                                for song_name in data.name.unique()
                            ],
                            value="Выбери название песни",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ), ],
            className="menu", ),
        # ________________________________-Table 2 with results-________________________________
        html.Div(children=[
            html.H5(children=random.choice(table_greeting)),
            dcc.Interval(id='rec-system-interval', interval=1000),
            dash_table.DataTable(
                id='rec-system-table',
                data=[],
                editable=False,
                style_cell_conditional=[
                    {'if': {'column_id': 'Название песни'}, 'width': '40%'},
                    {'if': {'column_id': 'Исполнитель'}, 'width': '40%'},
                    {'if': {'column_id': 'Популярность'}, 'width': '10%'},
                    {'if': {'column_id': 'Год выпуска'}, 'width': '10%'},
                ],
                style_header={'backgroundColor': 'rgb(230, 230, 230)',
                              'fontWeight': 'bold'},
                style_data_conditional=[
                    {'if': {'row_index': 'odd'},
                     'backgroundColor': 'rgb(248, 248, 248)'}
                ],
                style_table={'table-layout': 'fixed'},
                style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0
                }
            )
        ], className="table-top"),

    ]
)


# ________________________________-Updater-________________________________
@app.callback(
    [Output('output-year-slider', 'children'),
     Output('output-danceability-slider', 'children'),
     Output('output-energy-slider', 'children'),
     Output('output-liveness-slider', 'children'),
     Output('output-speechiness-slider', 'children'),
     Output('output-acousticness-slider', 'children'), ],

    [Input('year-slider', 'value'),
     Input('danceability-slider', 'value'),
     Input('energy-slider', 'value'),
     Input('liveness-slider', 'value'),
     Input('speechiness-slider', 'value'),
     Input('acousticness-slider', 'value')]
)
def update_output(value_year, value_dance, value_energy, value_loud, value_speech, value_acous):
    return f'Песни с {value_year[0]} по {value_year[1]} уже ждут тебя ниже!', \
           f'Вы выбрали с {value_dance[0] * 100:0.0f}% по {value_dance[1] * 100:0.0f}%', \
           f'Вы выбрали с {value_energy[0] * 100:0.0f}% по {value_energy[1] * 100:0.0f}%', \
           f'Вы выбрали с {value_loud[0] * 100:0.0f}% по {value_loud[1] * 100:0.0f}%', \
           f'Вы выбрали с {value_speech[0] * 100:0.0f}% по {value_speech[1] * 100:0.0f}%', \
           f'Вы выбрали с {value_acous[0] * 100:0.0f}% по {value_acous[1] * 100:0.0f}%',


# __________________-Main-__________________
@app.callback(
    [Output('main-table', 'data'), Output('main-table', 'columns')],
    [
        Input("artist-filter", 'value'),
        Input('year-slider', 'value'),
        Input('danceability-slider', 'value'),
        Input('energy-slider', 'value'),
        Input('liveness-slider', 'value'),
        Input('speechiness-slider', 'value'),
        Input('acousticness-slider', 'value')
    ]
)
def update_output(artists, year, danceability, energy, liveness, speechiness, acousticness):
    if len(artists) > 0:
        filtered_data = pd.DataFrame()
        for artist in artists:
            mask = (data.artists.str.contains(artist))
            filtered_data = filtered_data.append(data.loc[mask, :])
    else:
        filtered_data = data.copy()

    mask = (
            (filtered_data.release_date >= year[0]) & (filtered_data.release_date <= year[1])
            & (filtered_data.danceability >= danceability[0]) & (filtered_data.danceability <= danceability[1])
            & (filtered_data.energy >= energy[0]) & (filtered_data.energy <= energy[1])
            & (filtered_data.liveness >= liveness[0]) & (filtered_data.liveness <= liveness[1])
            & (filtered_data.speechiness >= speechiness[0]) & (filtered_data.speechiness <= speechiness[1])
            & (filtered_data.acousticness >= acousticness[0]) & (filtered_data.acousticness <= acousticness[1])
    )
    filtered_data = filtered_data.loc[mask, :]
    filtered_data = show_final_df(filtered_data)
    if len(filtered_data) == 0:
        filtered_data.loc[1] = ['Я не смог((', "Не получилось", "Нет ни одной походящей песни;(",
                                "Попробуй изменить фильтры"]
    else:
        if len(filtered_data) > 10:
            filtered_data = filtered_data.sample(10)
    return filtered_data.to_dict('records'), [{"name": i, "id": i} for i in filtered_data.columns]


# Table 2
@app.callback(
    [Output('rec-system-table', 'data'), Output('rec-system-table', 'columns')],
    [Input("song-name-filter", 'value'), ]
)
def update_output(song_name):
    mask = (data.name == song_name)
    filtered_data = data.loc[mask, :]
    if len(filtered_data) > 10:
        filtered_data = filtered_data.sample(10)

    filtered_data = show_final_df(filtered_data)
    return filtered_data.to_dict('records'), [{"name": i, "id": i} for i in filtered_data.columns]


# ________________________________-start-________________________________
# this is needed for the procfile to deploy to heroku
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True,
                   host='127.0.0.1')
