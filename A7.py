import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Creating world cup winners/runnerups dataset
data = {
    'Year': [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022],
    'Winner': ['Uruguay', 'Italy', 'Italy', 'Uruguay', 'Germany', 'Brazil', 'Brazil', 'England', 'Brazil', 'Germany', 'Argentina', 'Italy', 'Argentina', 'Germany', 'Brazil', 'France', 'Brazil', 'Italy', 'Spain', 'Germany', 'France', 'Argentina'],
    'Runner_Up': ['Argentina', 'Czechoslovakia', 'Hungary', 'Brazil', 'Hungary', 'Sweden', 'Czechoslovakia', 'Germany', 'Italy', 'Netherlands', 'Netherlands', 'Germany', 'Germany', 'Argentina', 'Italy', 'Brazil', 'Germany', 'France', 'Netherlands', 'Argentina', 'Croatia', 'France']
}
df = pd.DataFrame(data)
# Aggregate wins by country
win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']
# Create Choropleth map data
map_data = px.data.gapminder().query("year == 2007")
map_data = map_data[['country', 'iso_alpha']]  # Country and ISO code
map_data = map_data.merge(win_counts, left_on='country', right_on='Country', how='left').fillna(0)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1('FIFA World Cup Winners Dashboard'),
    
    dcc.Graph(id='choropleth-map'),

    html.H4('Select a country to view total wins:'),
    dcc.Dropdown(
        id='country-dropdown',
        
        options=[{'label': c, 'value': c} for c in map_data['country'].unique()],
        value='Brazil'
    ),
    html.Div(id='country-wins-output', style={'fontSize': '32px', 'textAlign': 'center'}),

    html.H4('Select a year to view winner and runner-up:'),
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        marks={year: str(year) for year in df['Year']},
        value=2022,
        step=None
    ),
    html.Div(id='year-result-output', style={'fontSize': '32px', 'textAlign': 'center'}),

    
])

# Callbacks

# Update Choropleth map
@app.callback(
    Output('choropleth-map', 'figure'),
    Input('country-dropdown', 'value')
)
def update_map(selected_country):
    fig = px.choropleth(map_data, locations="iso_alpha", color="Wins",
                         hover_name="country", color_continuous_scale='Oranges')
    return fig

# Update country wins output
@app.callback(
    Output('country-wins-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_wins(selected_country):
    
    wins = win_counts.loc[win_counts['Country'] == selected_country, 'Wins'].values[0] if selected_country in win_counts['Country'].values else 0
    return f'{selected_country} has won the World Cup {wins} times.'

# Update year result output
@app.callback(
    Output('year-result-output', 'children'),
    Input('year-slider', 'value')
)
def update_year_result(selected_year):
    row = df[df['Year'] == selected_year].iloc[0]
    return f'In {selected_year}, {row.Winner} defeated {row.Runner_Up} in the finals.'

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
