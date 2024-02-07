# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     * [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=int(min_payload),
                    max=int(max_payload),
                    step=1000,
                    marks={i: str(i) for i in range(int(min_payload), int(max_payload) + 1, 1000)},
                    value=[int(min_payload), int(max_payload)]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def update_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site != 'ALL':
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

    fig = px.pie(filtered_df, values='class', names='Launch Site', title='Success Launches by Site')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, selected_payload_range):
    filtered_df = spacex_df
    if selected_site != 'ALL':
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= selected_payload_range[0]) &
                              (filtered_df['Payload Mass (kg)'] <= selected_payload_range[1])]

    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category', title='Payload vs. Success',
                     labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Launch Outcome'})
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
