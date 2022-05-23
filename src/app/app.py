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

# print(liste_quartier[:-1])

df_quartier = analysis_quartier(df)
print(df_quartier)

liste_quartier = df_quartier['Valeur_Quartier'].sort_values().unique()


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
                    html.H4("Nombre de resaurants par quartier"),
                    dcc.Dropdown(id='dropdown_quartier', 
                        multi=True, 
                        value=liste_quartier[0],
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
                    html.H4("Nombre de restaurants par quartier"),
                    dcc.Dropdown(id='dropdown', 
                        multi=True, 
                        value=liste_quartier[0],
                        options=liste_quartier,
                    )
                ]),

                dbc.CardBody([
                    dcc.Graph(id='pie', figure={})
                ]),
            
            ],className='card border-primary mb-3'),

        ], width = 5, )
        
    ],justify="around" ),

    

 #-------------- FOOTER --------------#    
],fluid = True) #permet d'étirer à la largeur de la page web



# width={'size':5, 'offset':0, 'order':2}, #offset decale de 2 colonnes à gauche
# no_gutters= False,  l'espace entre les 2 éléments / True = pas d'espace ; False = espace
# width={'size':5, 'order':1},), #premières 5 colonnes à partir de la gauche, order permet de choisir l'ordre des éléments dans la ligne
# ),
# ], className='card border-light mb-3', style={"margin" : "6px"} ),
            

# ------- CALLBACK -------------------------------------------------------

# @app.callback(
#     Output('line-fig', 'figure'),
#     Input('dropdown', 'value')
# )
# def update_graph(stock_slctd):
#     dff = wallet[wallet['Name']==stock_slctd]
#     figln = px.bar(dff, x='Name', y='Balance')
#     return figln


# pie quartier
@app.callback(
    Output('pie_quartier', 'figure'),
    Input('dropdown_quartier', 'value')
)
def update_graph(value_slctd):
    
    df1_slct = df_quartier[df_quartier['Valeur_Quartier'].isin(value_slctd)]
    figln2 = px.bar(df1_slct, x='Quartier', y='Valeur_Quartier')
    return figln2


# # Barchart - Balance - Crypto
# @app.callback(
#     Output('bar_chart', 'figure'),
#     Input('checklist_bar', 'value')
# )
# def update_graph(value_slctd):
#     wallet_slctd = wallet[wallet['Name'].isin(value_slctd)]
#     fighist = px.histogram(wallet_slctd, x='Name', y='Balance', color="Name",  hover_name='Name')
#     return fighist

# #Add wallet



# # details_crypto
# @app.callback(
#     Output("details_output", "children"),
#     Input('dropdown_details', 'value')
# )
# def update_output_details(value_slctd):
#     dff = wallet[wallet['Name']==value_slctd]
#     balance = "{}".format(dff['Balance']).split('\n',1)[0].split('    ',1)[1]
#     holdings = "{}".format(dff['Holdings (en USD)']).split('\n',1)[0].split('    ',1)[1]
#     profit = "{}".format(dff['Profit/Loss']).split('\n',1)[0].split('    ',1)[1]
#     return "Balance : ",balance,"\n"," Holdings (en USD) : ",holdings, "\n", "Profit/Loss : " , profit

# #temps_reel_output
# @app.callback(
#     Output("temps_reel_output","children"),
#     Input("dropdown_temps_reel","value")
# )

# def update_output_temps_reel(value_slctd):
#     price_tps = price(value_slctd)
#     return "Price : {}".format(price_tps[0])

# #temps_reel_couleur   
# @app.callback(
#     Output("temps_reel_couleur","children"),
#     Input("dropdown_temps_reel","value")
# )

# def update_output_temps_couleurs(value_slctd):
#     price_tps = price(value_slctd)
#     return "Price : {}".format(price_tps[0])
# ------- RUN APP --------------------------------------------------------
# def launch_app():
#     return app.run_server(debug=True)  

if __name__=='__main__':
    app.run_server(debug=True)   

