import unittest

import dash
import dash_html_components as html
from population_chart import PopulationChart, PopulationChartDash


class PopulationChartTest(unittest.TestCase):
    def test_population_chart(self):
        chart = PopulationChart()
        chart.show()

    def test_population_chart_dash(self):
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        chart = PopulationChartDash(app)
        components_html = [html.Div([html.H1("Visualizações sobre Covid-19"),
                                     html.H6(
                                         "Neste trabalho, são apresentadas visualizações sobre os casos de Covid-19 e as vacinas aplicadas no Brasil.")]),
                           chart.component_html]
        app.layout = html.Div(components_html)
        app.run_server(debug=True)


if __name__ == '__main__':
    unittest.main()
