# visit http://127.0.0.1:8050/ in your web browser.

import argparse
import webbrowser
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State

intro = 'The perfect place to research properties across Malta & Gozo.'

layout = html.Div([
    html.Div(intro, className='fade-in-text'),
    #html.Img(src='assets/kampanja.JPG', id='main-banner'),
    html.Div([
    html.A(html.Button('Estimate Price', id='main-quote-btn'), href='#HIDDEN', id='main-quote-link'),
    html.A(html.Button('View Properties', id='main-analysis-btn'), href='#HIDDEN')
    ],id='main-buttons-div'),
    html.A(html.Img(src='assets/scroll-down.png', id='scroll-down'), id='scroll-container', href='#page-content'),
], id='main-area')




    #dcc.Link(html.Button('Get Quote', className='button-main-1'), href='/quote', className='main-link'),
    #dcc.Link(html.Button('View Properties', className='button-main-2'), href='/analysis', className='main-link')],
