import dash
import dash_html_components as html
#import dash_bootstrap_components as dbc
import os
from capanema.graficos_capanema import GraficosCapanema
from luiz_viana.graficos_luiz_viana import graficos_luiz_viana
from veloso.days_until_vac import DaysUntilVacDash
from veloso.population_chart import PopulationChartDash
from chaves.graficos_chaves import GraficoChaves

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

components_html = []
# # luiz viana
components_html += [html.Div([html.H1("Visualizações sobre Covid-19 - Vacinação"),
                             html.H6(
                                 "Neste trabalho, são apresentadas visualizações sobre os casos de Covid-19 e as vacinas aplicadas o Brasil.")])]
components_html += graficos_luiz_viana(app)

# capanema
components_html += [html.H6("Neste trabalho, são apresentadas visualizações sobre os casos de Covid-19 e as vacinas aplicadas o Brasil.")]


components_html += GraficosCapanema().start(app)

# veloso
c1 = DaysUntilVacDash(app)
c2 = PopulationChartDash(app)
components_html += [c1.component_html, c2.component_html]

# chaves
components_html += GraficoChaves().comparativo_casos(app)

app.layout = html.Div(components_html)

if __name__ == '__main__':
    app.run_server(debug=True)
