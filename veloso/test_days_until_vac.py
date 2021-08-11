import unittest

import dash
import dash_html_components as html
from days_until_vac import DaysUntilVac, DaysUntilVacDash


class DaysUntilVacTest(unittest.TestCase):
    def test_days_until_vac(self):
        chart = DaysUntilVac()
        chart.show()

    def test_days_until_vac_dash(self):
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        chart = DaysUntilVacDash(app)
        components_html = [html.Div([html.H1("Visualizações sobre Covid-19"),
                                     html.H6(
                                         "Neste trabalho, são apresentadas visualizações sobre os casos de Covid-19 e as vacinas aplicadas no Brasil.")]),
                           chart.component_html]
        app.layout = html.Div(components_html)
        app.run_server(debug=True)


if __name__ == '__main__':
    unittest.main()
