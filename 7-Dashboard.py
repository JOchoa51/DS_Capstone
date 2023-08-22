import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")   
spacex_df['success'] = ['Success' if clas == 1 else 'Failure' for clas in spacex_df['class']]
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("SpaceX Launch Record Dashboard", style={'textAlign': 'left'}),
    html.P("Launch Site:", style={'textAlign':'center'}),
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='CCAFS LC-40',
        multi=False,
        style={'width': '50%', 'margin': 'auto'}
    ),
    
    dcc.Graph(id='success-pie-chart'),
    html.P("Payload range (Kg):", style={'textAlign': 'center'}),
    dcc.Slider(
        id='payload-slider',
        min=0,
        max=spacex_df['Payload Mass (kg)'].max(),
        step=1000,
        value=spacex_df['Payload Mass (kg)'].max(),
        marks={i: str(i) for i in range(0, (spacex_df['Payload Mass (kg)']).astype(int).max() + 1, 5000)},
        tooltip={'placement': 'top'}
    ),
    
    dcc.Graph(id='success-payload-scatter-chart'),
])

# Callback for the success pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site:
        if selected_site == 'All Sites':
            data_filtered = spacex_df
        else:
            data_filtered = spacex_df[spacex_df['Launch Site'] == selected_site]
        
        success_counts = data_filtered['class'].value_counts()
        
        fig = px.pie(success_counts, names=success_counts.index, values=success_counts.values, title='Launch Success Distribution')
        return fig

# Callback for the success vs. payload scatter chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_value):
    if selected_site:
        if selected_site == 'All Sites':
            data_filtered = spacex_df
        else:
            data_filtered = spacex_df[spacex_df['Launch Site'] == selected_site]
        
        data_filtered = data_filtered[data_filtered['Payload Mass (kg)'] <= payload_value]
        
        fig = px.scatter(data_filtered, x='Payload Mass (kg)', y='class', color_discrete_sequence=px.colors.qualitative.Dark2, title='Correlation between Payload and Launch Success')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
