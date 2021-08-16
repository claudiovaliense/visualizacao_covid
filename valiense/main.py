import dash
import dash_html_components as html
import dash_core_components as dcc

#from graficos_luiz_viana import graficos_luiz_viana
from graficos_valiense import graficos_valiense

if __name__ == '__main__':
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    #components_html = [html.Div([html.H6("Visualizações sobre idade dos vacinados")])]
    #components_html += graficos_valiense(app)
    components_html = graficos_valiense(app)
    
    
    app.layout = html.Div([
        dcc.Graph(figure=components_html)
    ])

    #app.layout = html.Div(components_html)

    app.run_server(debug=True)