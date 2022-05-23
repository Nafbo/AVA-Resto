from tracemalloc import stop
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import base64
import plotly.graph_objs as go
from dash import Dash, dash_table
from src.analysis.analysis import analysis_prix, analysis_quartier, analysis_type, set_up


# ------- INITIALISATION DATA --------------------------------------------------------

df = pd.read_csv('./src/analysis/LePetitFute.csv')
df1 = set_up(df)

#Pour les quartiers et le nombre de restos dans ces quartiers 

df_quartier = analysis_quartier(df)
liste_quartier = df_quartier['Quartier'].sort_values().unique()

#Pour le type de restos au total

df_type = analysis_type(df)
type_quartier=df_type['Type'].sort_values().unique()

#Pour le nombre de restaurants en fonction des prix

df_prix = analysis_prix(df)
prix_quartier=df_prix['Prix'].sort_values().unique()

# ------- APP -----------------------------------------------------------

app=dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL],  #dbc.themes.ZEPHIR
            meta_tags=[{'name': 'viewport',       # permet à l'app d'être responsive pour téléphone  
                     'content': 'width=device-width, initial-scale=1.0'}]
                     
            )

# ------- LAYOUT --------------------------------------------------------

app.layout= dbc.Container([    #dbc.Container mieux que html.div pour bootstrap

 #-------------- HEADER --------------#

    dbc.Row([   #divise la page en 3 ligne : le titres / dropdown / derniers bar chart
        html.H1("Quel est le meilleur restaurant de Paris")], 
        className="text-center mb-3"), 

    dbc.Row([
        dbc.Col([
            dbc.Card([

                dbc.CardHeader([
                    html.H4("Nombre de restaurants par quartier"),
                    dcc.Dropdown(id='dropdown_quartier', 
                        multi=True, 
                        value=liste_quartier,
                        options=liste_quartier,
                    )
                ]),

                dbc.CardBody([
                    dcc.Graph(id='pie_quartier', figure={})
                ]),
            
            ],className='card border-primary mb-3'),
        ], width=5),

        dbc.Col([
            
            dbc.Card([

                dbc.CardHeader([
                    html.H4("Total de restaurants par type"),
                    dcc.Dropdown(id='dropdown_type', 
                        multi=True, 
                        value=type_quartier[1],
                        options=type_quartier,
                    )
                ]),

                dbc.CardBody([
                    dcc.Graph(id='pie', figure={})
                ]),
            
            ],className='card border-success mb-3'),

        ], width = 5, ),
        
        dbc.Col([
            
            dbc.Card([

                dbc.CardHeader([
                    html.H4("Total de restaurants par prix"),
                    dcc.Dropdown(id='dropdown_prix', 
                        multi=True, 
                        value=prix_quartier,
                        options=prix_quartier,
                    )
                ]),

                dbc.CardBody([
                    dcc.Graph(id='pie_prix', figure={})
                ]),
            
            ],className='card border-info mb-3'),

        ], width = 5, )
        
    ],justify="around" ),

    

 #-------------- FOOTER --------------#    
],fluid = True) #permet d'étirer à la largeur de la page web

        

# ------- CALLBACK -------------------------------------------------------


# pie quartier
@app.callback(
    Output('pie_quartier', 'figure'),
    Input('dropdown_quartier', 'value')
)
def update_graph(value_slctd):
    df1_slct = df_quartier[df_quartier['Quartier'].isin(value_slctd)]
    figln2 = px.bar(df1_slct, x='Quartier', y='Valeur_Quartier', color='Quartier')
    return figln2

@app.callback(
    Output('pie', 'figure'),
    Input('dropdown_type', 'value')
)
def update_graph(value_slctd):
    df1_slct = df_type[df_type['Type'].isin(value_slctd)]
    figln3 = px.bar(df1_slct, x='Type', y='Valeur_Type', color='Type')
    return figln3


@app.callback(
    Output('pie_prix', 'figure'),
    Input('dropdown_prix', 'value')
)
def update_graph(value_slctd):
    df1_slct = df_prix[df_prix['Prix'].isin(value_slctd)]
    figln4 = px.pie(df1_slct, values='Valeur_Prix', names='Prix', hole=.3)
    #figln4 = px.bar(df1_slct, x='Prix', y='Valeur_Prix', color='Prix')
    return figln4


if __name__=='__main__':
    app.run_server(debug=True)   

