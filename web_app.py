# visit http://127.0.0.1:8050/ in your web browser.

import pdb
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

class App:

    def __init__(self, df):
        self.n = len(df)

        min_locs_by_type = 10
        B = df.groupby('type').count()
        types = B[B>=min_locs_by_type].dropna().index
        df = df[df.type.isin(types)]
        self.df = df

        app = dash.Dash(__name__)

        app.layout = html.Div([
            
            dcc.Dropdown(id='type-dd',
                         options=[
                             {'label': k, 'value': k} for k in np.unique(df.type)
                         ],
                         value='Apartment'
                        ),
            dcc.Graph(id='bar-by-type'),
            dcc.Dropdown(id='loc-dd',
                         options=[
                             {'label': k, 'value': k} for k in np.unique(df.locality)
                         ],
                         value='Qawra'
                        ),
            dcc.Graph(id='price-by-area')
        ])

        self.app = app

        @app.callback(
            Output(component_id='bar-by-type', component_property='figure'),
            Input(component_id='type-dd', component_property='value')
        )
        def update_bar_by_type(prop_type):

            min_properties = 10
            filtered_df_grouped = df[df.type==prop_type].groupby('locality')

            A = filtered_df_grouped.count()
            locs = A[A>=min_properties].dropna().index
            filtered_df = filtered_df_grouped.median()
            filtered_df = filtered_df.loc[locs]
            filtered_df = filtered_df[['price']]
            filtered_df = filtered_df.sort_values('price')
            fig_bar = px.bar(filtered_df, x=filtered_df.index, y='price', labels={'price': 'Price EUR'})
            fig_bar.update_layout(transition_duration=500)

            return fig_bar

        @app.callback(
            Output(component_id='price-by-area', component_property='figure'),
            Input(component_id='loc-dd', component_property='value')
        )
        def update_scatter_by_type(prop_loc):
            filtered_df = df[df.locality==prop_loc]
            filtered_df = filtered_df[['price', 'area']]
            fig_scatter = px.scatter(filtered_df, x='area', y='price')
            fig_scatter.update_layout(transition_duration=500)
            return fig_scatter

    def run_server(self, **kwargs):
        self.app.run_server(**kwargs)

if __name__ == '__main__':
    df = pd.read_csv('remax_properties.csv')
    app = App(df)
    app.run_server(debug=True)
