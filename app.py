import dash
from dash import html
from dash import dcc 

print(dcc.__version__) # 0.6.0 or above is required

app = dash.Dash(__name__, update_title=None)

server = app.server
app.config.suppress_callback_exceptions = True

if __name__=='__main__':
    app.run_server()
