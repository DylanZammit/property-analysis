# visit http://127.0.0.1:8050/ in your web browser.

import argparse
import webbrowser
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

from app import app
from analysis.anova import ANOVA
from apps import analysis, main, anova

wpage = None

intro = 'Do you want to get a quote, or rough estimate of how much your property is worth in the current market in Malta? Or maybe do you want to do an in depth analysis on the current housing market? Press the options below to test out different stuff and try. Enjoy!'

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    #html.Script(src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"),
    html.Div('Property Analysis', id='header'),
    main.layout,
    html.Div(id='page-content'),
    html.Div(id='HIDDEN', style={'display': 'none'})
], id='backest')

def search_prop_url( form, locality):
    townid = townmap[locality]
    formid = 2 or formmap[form]
    return 'https://remax-malta.com/listings?Residential=true&Commercial=false&ForSale=true&ForRent=false&TownIds={}&SelectedPropertyTypes={}&page=1'.format(townid,formid)

###########################################
df = pd.read_csv('data/remax_properties.csv')

qtile = 0.99
qprice = df.price.quantile(qtile)
qintarea = df.int_area.quantile(qtile)
qarea = df.area.quantile(qtile)

n = len(df)

min_locs_by_type = 20
B = df.groupby('type').count()
types = B[B>=min_locs_by_type].dropna().index
df = df[df.type.isin(types)]
df = df[(df.price<qprice)&(df.int_area<qintarea)&(df.area<qarea)] # too much?
###########################################
townmap = df.groupby('locality').last()['locality_id']
model = ANOVA(df)

#@app.callback(Output('HIDDEN', 'children'),
#              [Input('url', 'pathname')])
#def display_page(pathname):
#    import pdb; pdb.set_trace()
#    return None
#    #if pathname == '/page-1':
#    #    return page_1_layout
#    #elif pathname == '/page-2':
#    #    return page_2_layout
#    #else:
#    #    return index_page

@app.callback(
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

#@app.callback(
#    Output('scroll-container', 'style'),
#    Input('main-quote-link', 'pathname'),
#)

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
                             height=900,trendline='ols', trendline_color_override='orange')
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
    Input('area-quote-slider', 'value'),
    Input('beds-quote-slider', 'value'),
    Input('loc-quote-dd', 'value'),
    Input('type-quote-dd', 'value')
)
def quote_button(area, beds, loc, type):
    if area and beds and loc and type:
        X = {'area': area, 'bedrooms': beds, 'locality': loc, 'type': type}
        out = model.predict(X)
        return f'Estimate is €{int(out//1000*1000):,}'
    return ''

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
