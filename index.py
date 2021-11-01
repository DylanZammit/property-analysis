# visit http://127.0.0.1:8050/ in your web browser.

import os
import argparse
import webbrowser
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from app import app
from analysis.anova import ANOVA
from apps import analysis, main, anova, regression, malta, compare
import dash_daq as daq
from read_data import df, region2loc, loc2region, region2img

wpage = None

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='header', children=[
        html.Div('Malta Properties', id='title'),
        #daq.BooleanSwitch(
        #    on=True,
        #    id='asd')
    ]),
    html.Div(html.Img(src='assets/island.jpg', id='main-img-really'), id='main-img', className='box-shadow'),
    main.layout,
    html.Div(id='page-content'),
    html.Div(id='HIDDEN', style={'visibility': 'hidden'})
], id='backest')

def search_prop_url( form, locality):
    townid = townmap[locality]
    formid = 2 or formmap[form]
    return 'https://remax-malta.com/listings?Residential=true&Commercial=false&ForSale=true&ForRent=false&TownIds={}&SelectedPropertyTypes={}&page=1'.format(townid,formid)

townmap = df.groupby('locality').last()['locality_id']
model = ANOVA(df)

@app.callback(
    Output('analysis-content', 'children'),
    Input('analysis-tabs', 'value')
)
def render_analysis_content(tab):
    if tab == 'malta-tab':
        return malta.layout
    elif tab == 'regression-tab':
        return regression.layout
    elif tab == 'compare-tab':
        return compare.layout

@app.callback(
    #Output('page-content', 'style'),
    Output('page-content', 'children'),
    Output('scroll-container', 'style'),
    #Input('main-quote-link', 'pathname'),
    Input('main-quote-btn', 'n_clicks'),
    Input('main-analysis-btn', 'n_clicks')
)
def main_button_click(btn1, btn2):
    visible = {'visibility': 'unset'}
    hidden = {'visibility': 'hidden'}

    ctx = dash.callback_context
    if not ctx.triggered:
        return None, hidden

    button = ctx.triggered[0]['prop_id'].split('.')[0].split('-')[1]

    if button == 'analysis':
        return analysis.layout, visible
    elif button == 'quote':
        return anova.layout, visible

@app.callback(
    Output(component_id='compare-bar', component_property='figure'),
    Input(component_id='compare-loc1-dd', component_property='value'),
    Input(component_id='compare-loc2-dd', component_property='value'),
)
def update_compare_bar(loc1, loc2):
    fdf = df.copy()
    fdf = fdf[fdf.locality.isin([loc1, loc2])]
    fdf = fdf['type price locality'.split()]

    loc_type = fdf.groupby(['locality', 'type']).mean()
    types = list(loc_type.loc[loc1].index)
    data1 = np.floor(loc_type.loc[loc1].values).flatten()
    data2 = np.floor(loc_type.loc[loc2].values).flatten()
    
    fig_bar = go.Figure(data=[
        go.Bar(name=loc1, x=types, y=data1),
        go.Bar(name=loc2, x=types, y=data2)
    ])
    fig_bar.update_layout(transition_duration=500, clickmode='event+select', barmode='group')
    return fig_bar

@app.callback(
    Output(component_id='price-by-area', component_property='figure'),
    Output(component_id='price-range-text', component_property='children'),
    Input(component_id='loc-dd', component_property='value'),
    Input(component_id='region-dd', component_property='value'),
    Input(component_id='beds-dd', component_property='value'),
    Input(component_id='scatter-type-dd', component_property='value'),
    Input(component_id='price-range', component_property='value'),
)
def update_scatter_by_type(loc, region, beds, form, price_range):
    fdf = df.copy()
    fdf = fdf if not loc else fdf[fdf.locality.isin(loc)]
    fdf = fdf if not region else fdf[fdf.region.isin(region)]
    fdf = fdf if not beds else fdf[fdf.bedrooms.isin([int(b) for b in beds])]
    fdf = fdf if not form else fdf[fdf.type.isin(form)]
    fdf = fdf[fdf.price.between(price_range[0], price_range[1])]
    fig_scatter = px.scatter(fdf, x='int_area', y='price', custom_data=['locality', 'region', 'price','rooms',
                                                                        'bedrooms', 'bathrooms', 'area',
                                                                        'int_area', 'ext_area', 'type',
                                                                        'webpage'],
                             height=900,trendline='ols', trendline_color_override='orange')
    fig_scatter.update_layout(transition_duration=500, clickmode='event+select')
    return fig_scatter, f'Price is between €{price_range[0]:,} and €{price_range[1]:,}'

@app.callback(
    Output(component_id='hidden-div', component_property='children'),
    Input(component_id='bar-by-type', component_property='clickData'),
    Input(component_id='type-dd', component_property='value'),
)
def search_loc_form(data, form):
    if data: 
        loc = data['points'][0]['x']
        form = 1
        wpage = search_prop_url(form, loc)
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
    fig_bar = px.bar(fdf, x=fdf.index, y='price', labels={'price': 'Price EUR'}, height=500,
                     color_continuous_scale=px.colors.sequential.Bluered, color='price')
    fig_bar.update_layout(transition_duration=500, clickmode='event+select')

    return fig_bar


@app.callback(
    Output(component_id='locality-output', component_property='children'),
    Output(component_id='region-output', component_property='children'),
    Output(component_id='price-output', component_property='children'),
    Output(component_id='rooms-output', component_property='children'),
    Output(component_id='beds-output', component_property='children'),
    Output(component_id='baths-output', component_property='children'),
    Output(component_id='area-output', component_property='children'),
    Output(component_id='intarea-output', component_property='children'),
    Output(component_id='extarea-output', component_property='children'),
    Output(component_id='type-output', component_property='children'),
    #Output(component_id='prop-link', component_property='href'),
    Input(component_id='price-by-area', component_property='clickData')
)
def search_prop_scatter(data):
    global wpage
    if data and 'customdata' in data['points'][0]: 
        output = data['points'][0]['customdata']
        output[2] = '€{:,}'.format(output[2])
        for i in range(3, 6):
            output[i] = ['{}'.format(output[i]), ' rooms']
        for i in range(6, 9):
            output[i] = ['{}m'.format(output[i]), html.Sup(2)]
        wpage = output[-1]
        return tuple(output[:-1])
    return tuple(['']*10)

@app.callback(
    Output(component_id='hidden-div2', component_property='children'),
    #Input(component_id='prop-link', component_property='value')
    Input('prop-link', 'n_clicks')
)
def button_click(data):
    if data and wpage:
        webbrowser.open_new_tab(wpage)
    return None

@app.callback(
    Output('quote-output', 'children'),
    Output('quote-image-container', 'children'),
    Input('area-quote-slider', 'value'),
    Input('beds-quote-slider', 'value'),
    Input('loc-quote-dd', 'value'),
    Input('type-quote-dd', 'value')
)
def quote_button(area, beds, loc, type):
    global prev_reg

    img_out = html.Img(id='quote-image', src=os.path.join('assets', region2img[loc2region[loc]]))
    if area and beds and loc and type:
        X = {'area': area, 'bedrooms': beds, 'locality': loc, 'type': type}
        out = model.predict(X)

        return f'Estimate is €{int(out//1000*1000):,}', img_out
    return '', img_out

@app.callback(
    Output('beds-quote-output', 'children'),
    [Input('beds-quote-slider', 'value')])
def update_beds_quote(value):
    return f'{value} bedroom'

@app.callback(
    Output('area-quote-output', 'children'),
    [Input('area-quote-slider', 'value')])
def update_area_quote(value):
    return f'Total area = {value}m\u00b2'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-debug', action='store_true')
    args = parser.parse_args()

    debug = not args.no_debug
    app.run_server(debug=debug)
