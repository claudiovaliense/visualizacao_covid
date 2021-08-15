import unittest

import dash
import dash_html_components as html

from days_until_vac import DaysUntilVacDash
from population_chart import PopulationChartDash


class IntegratedTest(unittest.TestCase):
    def test_two_charts(self):
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        c1 = DaysUntilVacDash(app)
        c2 = PopulationChartDash(app)
        components_html = [html.Div([html.H1("Visualizações sobre Covid-19"),
                                     html.H6(
                                         "Neste trabalho, são apresentadas visualizações sobre os casos de Covid-19 e as vacinas aplicadas no Brasil.")]),
                           c1.component_html]

        components_html += [c2.component_html]

        # print(components_html)

        app.layout = html.Div(components_html)

        app.run_server(debug=True)


if __name__ == '__main__':
    unittest.main()
