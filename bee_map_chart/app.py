#Import Libs 
import os
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go 
import dash 
import dash_core_components as dcc 
import dash_html_components as dhc 
from dash.dependencies import Input,Output 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


server = app.server

#--------------------------------------------------------
# Import and clean data from csv 

df=pd.read_csv('intro_bees.csv')

df=df.groupby(['State','ANSI','Affected by','Year','state_code'])[['Pct of Colonies Impacted']].mean()

df.reset_index(inplace=True)

print(df[:10])

#--------------------------------------------------------
#App Layout 

app.layout = dhc.Div([

    dhc.H1("Web Application With Dash",style={'text-align': 'center'}),

    dcc.Dropdown(id='Select_Year',
                options=[
                    {'label':'2015','value':2015},
                    {'label':'2016','value':2016},
                    {'label':'2017','value':2017},
                    {'label':'2018','value':2018}],
                multi=False,
                value=2015,
                style={'width':'40%'}
                ),

    dhc.Div(id='output_container',children=[]),
    dhc.Br(),

    dcc.Graph(id='my_plot',figure={})            

])

#-----------------------------------------------------------
# Connect the plotly graphs to HTML Components

@app.callback(
    [Output(component_id='output_container',component_property='children'),
    Output(component_id='my_plot',component_property='figure')],
    [Input(component_id='Select_Year',component_property='value')]
)

def update_graph(option_selct):
    print(option_selct)
    print(type(option_selct))


    container='The Year choosen is {}'.format(option_selct)

    final_df=df.copy()
    final_df = final_df[final_df['Year'] == option_selct]
    final_df=final_df[final_df['Affected by']== 'Varroa_mites']

    #Plotly Express
    fig=px.choropleth(
        data_frame=final_df,
        locationmode='USA-states',
        locations='state_code',
        scope='usa',
        color='Pct of Colonies Impacted',
        hover_data=['State','Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct Of Colonies Impacted':'% Of Bee Colonies'},
        template='plotly_dark'
    )    

    return container,fig

#-----------------------------------------------------------------
# Running the App 

if __name__ == "__main__":
    app.run_server(debug=True)
        