import dash
import dash_html_components as html
#import dash_bootstrap_components as dbc

from graficos_capanema import graficos_capanema


if __name__ == '__main__':
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    components_html = [html.Div([html.H1("Visualizações sobre Covid-19"),
                                 html.H6("Neste trabalho, são apresentadas visualizações sobre os casos de Covid-19 e as vacinas aplicadas o Brasil.")])]
    components_html += graficos_capanema(app)

    app.layout = html.Div(components_html)

    app.run_server(debug=True)