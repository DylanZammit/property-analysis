# visit http://127.0.0.1:8050/ in your web browser.

import argparse
import webbrowser
import pdb
import numpy as np
import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State

class App:

    wpage = None

    def search_prop_url(self, form, locality):
        townid = self.townmap[locality]
        formid = 2 or self.formmap[form]
        return 'https://remax-malta.com/listings?Residential=true&Commercial=false&ForSale=true&ForRent=false&TownIds={}&SelectedPropertyTypes={}&page=1'.format(townid,formid)


    def __init__(self, df):
        qtile = 0.99
        qprice = df.price.quantile(qtile)
        qintarea = df.int_area.quantile(qtile)
        qarea = df.area.quantile(qtile)

        self.n = len(df)

        min_locs_by_type = 20
        B = df.groupby('type').count()
        types = B[B>=min_locs_by_type].dropna().index
        df = df[df.type.isin(types)]
        df = df[(df.price<qprice)&(df.int_area<qintarea)&(df.area<qarea)] # too much?
        self.df = df
        self.townmap = df.groupby('locality').last()['locality_id']

        app = dash.Dash(__name__)

        app.layout = html.Div([
            html.H1('Property Analysis', style={'text-align': 'center'}),
            html.Hr(),
            html.Div([
                dcc.Graph(id='price-by-area', style={'float': 'left','margin': 'auto', 'width':'60%'}, config={'displayModeBar': False}),
                html.Div([
                    html.H2('Filters ', style={'padding': '20px', 'float': 'center','margin': 'auto', 'width': '100%',
                                               'text-align': 'center'}),
                html.Div([
                html.Div('Locality: ', style={'float': 'left','margin': 'auto', 'width': '20%'}),
                dcc.Dropdown(id='loc-dd',
                             placeholder='Any',
                             multi=True,
                             options=[
                                 {'label': k, 'value': k} for k in np.unique(df.locality)
                             ], style={'float': 'left','margin': 'auto', 'width': '80%'}
                            )], style={'overflow': 'visible', 'padding': '8px'}),
                html.Div([
                html.Div('Region: ', style={'float': 'left','margin': 'auto', 'width': '20%'}),
                dcc.Dropdown(id='region-dd',
                             placeholder='Any',
                             multi=True,
                             options=[
                                 {'label': k, 'value': k} for k in np.unique(df.region)
                             ], style={'float': 'left','margin': 'auto', 'width': '80%'}
                            )], style={'overflow': 'visible', 'padding': '8px'}),
                html.Div([
                html.Div('# Bedrooms: ', style={'float': 'left','margin': 'auto', 'width': '20%'}),
                dcc.Dropdown(id='beds-dd',
                             placeholder='Any',
                             multi=True,
                             options=[
                                 {'label': k, 'value': k} for k in np.unique(df.bedrooms)
                             ], style={'float': 'left','margin': 'auto', 'width': '80%'}
                            )], style={'overflow': 'visible', 'padding': '8px'}),
                html.Div([
                html.Div('Property Type: ', style={'float': 'left','margin': 'auto', 'width': '20%'}),
                dcc.Dropdown(id='scatter-type-dd',
                             placeholder='Any',
                             multi=True, 
                             options=[
                                 {'label': k, 'value': k} for k in np.unique(df.type)
                             ], style={'float': 'left','margin': 'auto', 'width': '80%'}
                            )], style={'overflow': 'visible', 'padding': '8px'}),
                ], className='filters', style={'float': 'left','margin': 'auto', 'width': '40%'}),
                html.Table([
                    html.Tr([html.Td('Locality'), html.Td(id='locality-output')]),
                    html.Tr([html.Td('Region'), html.Td(id='region-output')]),
                    html.Tr([html.Td('Price (EUR)'), html.Td(id='price-output')]),
                    html.Tr([html.Td('# Rooms'), html.Td(id='rooms-output')]),
                    html.Tr([html.Td('# Bedrooms'), html.Td(id='beds-output')]),
                    html.Tr([html.Td('# Bathrooms'), html.Td(id='baths-output')]),
                    html.Tr([html.Td(['Area (m', html.Sup(2), ')']), html.Td(id='area-output')]),
                    html.Tr([html.Td(['Interior Area (m', html.Sup(2), ')']), html.Td(id='intarea-output')]),
                    html.Tr([html.Td(['Exterior Area (m', html.Sup(2), ')']), html.Td(id='extarea-output')]),
                    html.Tr([html.Td('Property Type'), html.Td(id='type-output')]),
                ], style={'padding-top': '30px'}),
                html.Button('View Property', className='button', id='prop-link'),
                #dcc.Link(html.Button('View Property', style={'margin-top': '10px'}), id='prop-link', style={'margin-top': '10px'}, href=''),
            ], style={'overflow': 'hidden'}),
            #html.Hr(),
            html.Div([
            dcc.Dropdown(id='type-dd',
                         multi=True,
                         placeholder='All property types',
                         options=[
                             {'label': k, 'value': k} for k in np.unique(df.type)
                         ],
                         value=['Apartment']
                        ),
                dcc.Graph(id='bar-by-type', config={'displayModeBar': False})]),
            html.Div(id='hidden-div', style={'display':'none'}),
            html.Div(id='hidden-div2', style={'display':'none'}),
        ])

        self.app = app

        @app.callback(
            Output(component_id='price-by-area', component_property='figure'),
            Input(component_id='loc-dd', component_property='value'),
            Input(component_id='region-dd', component_property='value'),
            Input(component_id='beds-dd', component_property='value'),
            Input(component_id='scatter-type-dd', component_property='value'),
        )
        def update_scatter_by_type(loc, region, beds, form):
            fdf = df.copy()
            fdf = fdf if not loc else fdf[fdf.locality.isin(loc)]
            fdf = fdf if not region else fdf[fdf.region.isin(region)]
            fdf = fdf if not beds else fdf[fdf.bedrooms.isin([int(b) for b in beds])]
            fdf = fdf if not form else fdf[fdf.type.isin(form)]
            fig_scatter = px.scatter(fdf, x='int_area', y='price', custom_data=['locality', 'region', 'price','rooms',
                                                                                'bedrooms', 'bathrooms', 'area',
                                                                                'int_area', 'ext_area', 'type',
                                                                                'webpage'],
                                     height=800,trendline='ols', trendline_color_override='orange')
            fig_scatter.update_layout(transition_duration=500, clickmode='event+select')
            return fig_scatter

        @app.callback(
            Output(component_id='hidden-div', component_property='children'),
            Input(component_id='bar-by-type', component_property='clickData'),
            Input(component_id='type-dd', component_property='value'),
        )
        def search_loc_form(data, form):
            if data: 
                loc = data['points'][0]['x']
                form = 1
                wpage = self.search_prop_url(form, loc)
                webbrowser.open_new_tab(wpage)
            return None

        @app.callback(
            Output(component_id='bar-by-type', component_property='figure'),
            Input(component_id='type-dd', component_property='value')
        )
        def update_bar_by_type(prop_type):
            min_properties = 1
            if prop_type:
                fdf_grouped = df[df.type.isin(prop_type)].groupby('locality')
            else:
                fdf_grouped = df.groupby('locality')

            A = fdf_grouped.count()
            locs = A[A>=min_properties].dropna().index
            fdf = fdf_grouped.median()
            fdf = fdf.loc[locs]
            fdf = fdf[['price']]
            fdf = fdf.sort_values('price')
            fig_bar = px.bar(fdf, x=fdf.index, y='price', labels={'price': 'Price EUR'}, height=500)
            fig_bar.update_layout(transition_duration=500, clickmode='event+select')

            return fig_bar


        @app.callback(
            Output(component_id='locality-output', component_property='children'),
            Output(component_id='region-output', component_property='children'),
            Output(component_id='price-output', component_property='children'),
            Output(component_id='beds-output', component_property='children'),
            Output(component_id='baths-output', component_property='children'),
            Output(component_id='rooms-output', component_property='children'),
            Output(component_id='area-output', component_property='children'),
            Output(component_id='intarea-output', component_property='children'),
            Output(component_id='extarea-output', component_property='children'),
            Output(component_id='type-output', component_property='children'),
            #Output(component_id='prop-link', component_property='href'),
            Input(component_id='price-by-area', component_property='clickData')
        )
        def search_prop_scatter(data):
            if data: 
                output = data['points'][0]['customdata']
                output[2] = '€{:,}'.format(output[2])
                self.wpage = output[-1]
                return tuple(output[:-1])
            return tuple(['']*10)

        @app.callback(
            Output(component_id='hidden-div2', component_property='children'),
            #Input(component_id='prop-link', component_property='value')
            Input('prop-link', 'n_clicks')
        )
        def button_click(data):
            if data and self.wpage:
                webbrowser.open_new_tab(self.wpage)
            return None

    def run_server(self, **kwargs):
        self.app.run_server(**kwargs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-debug', action='store_true')
    args = parser.parse_args()

    debug = not args.no_debug

    df = pd.read_csv('remax_properties.csv')
    app = App(df)
    app.run_server(debug=debug)
