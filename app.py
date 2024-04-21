import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go

pokemon_data = pd.read_csv("pokemondashtrue2.csv")

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Div([
        html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pokémon_logo.svg/1200px-International_Pokémon_logo.svg.png',
                 style={'width': '50%', 'margin': 'auto', 'display': 'block'})
    ]),
    html.Div([
        html.Div([
            html.H3("Choisissez le type de Pokémon à adopter :"),
            dcc.RadioItems(
                id='type-selector',
                options=[
                    {'label': 'Plante', 'value': 'grass'},
                    {'label': 'Feu', 'value': 'fire'},
                    {'label': 'Eau', 'value': 'water'},
                    {'label': 'Électrique', 'value': 'electric'},
                    {'label': 'Dragon', 'value': 'dragon'},
                    {'label': 'Fée', 'value': 'fairy'},
                    {'label': 'Insecte', 'value': 'bug'},
                    {'label': 'Normale', 'value': 'normal'},
                    {'label': 'Poison', 'value': 'poison'},
                    {'label': 'Psy', 'value': 'psychic'},
                    {'label': 'Acier', 'value': 'steel'},
                    {'label': 'Tenebre', 'value': 'dark'},
                    {'label': 'Fantome', 'value': 'ghost'},
                    {'label': 'Sol', 'value': 'ground'},
                    {'label': 'Roche', 'value': 'rock'},
                    {'label': 'Combat', 'value': 'fighting'},
                    {'label': 'Glace', 'value': 'ice'}
                ],
                value='grass'
            )
        ], style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='pokemon-stats')
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),

    html.Div(id='pokemon-selector'),

    html.Div([
        dcc.Graph(id='pokemon-types')
    ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div([
        html.H3("Dataframe des Pokémon"),
        dcc.Textarea(
            id='pokemon-dataframe',
            value=pokemon_data.to_string(),
            style={'width': '100%', 'height': '300px', 'resize': 'none'}
        )
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'})
])

@app.callback(
    Output('pokemon-selector', 'children'),
    [Input('type-selector', 'value')]
)
def update_pokemon_selector(selected_type):
    pokemon_of_selected_type = pokemon_data[pokemon_data['type1'] == selected_type]

    pokemon_names = pokemon_of_selected_type['name'].unique()

    pokemon_dropdown = dcc.Dropdown(
        id='pokemon-dropdown',
        options=[{'label': name, 'value': name} for name in pokemon_names],
        value=pokemon_names[0] if len(pokemon_names) > 0 else None
    )

    return pokemon_dropdown

@app.callback(
    Output('pokemon-stats', 'figure'),
    [Input('pokemon-dropdown', 'value')]
)
def update_pokemon_stats(selected_pokemon):
    if selected_pokemon is not None:
        pokemon_stats = pokemon_data[pokemon_data['name'] == selected_pokemon]

        fig = go.Figure(data=[go.Pie(
            labels=['Attack', 'Defense', 'HP', 'Taille', 'Poid', 'Speed'],
            values=[pokemon_stats['attack'].values[0], pokemon_stats['defense'].values[0],
                    pokemon_stats['hp'].values[0], pokemon_stats['height_m'].values[0],
                    pokemon_stats['kg'].values[0], pokemon_stats['speed'].values[0]],
            textinfo='label+value'
        )])

        fig.update_layout(title=f"Statistiques de {selected_pokemon}")

        return fig
    else:
        return go.Figure()

@app.callback(
    Output('pokemon-types', 'figure'),
    [Input('pokemon-dropdown', 'value')]
)
def update_pokemon_types(selected_pokemon):
    pokemon_type_counts = pokemon_data['type1'].value_counts()

    fig = go.Figure(data=[go.Pie(
        labels=pokemon_type_counts.index,
        values=pokemon_type_counts.values,
        hoverinfo='label+value'
    )])

    fig.update_layout(title=f"Types de Pokémon présents")

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
