import unittest

import dash
import dash_html_components as html

from stacked_area import StackedAreaDash, StackedArea, StackedAreaDataset


class StackedAreaTest(unittest.TestCase):
    def test_stacked_area(self):
        df = StackedAreaDataset.update("Todos")
        chart = StackedArea(df, "Nome da vacina", 'Semana de aplicação', 'Total (semana)')
        chart.show()

    def test_stacked_area_dash(self):
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        pop = StackedAreaDash(app)
        components_html = [html.Div([html.H1("Visualizações sobre Covid-19"),
                                     html.H6(
                                         "Neste trabalho, são apresentadas visualizações sobre os casos de Covid-19 e as vacinas aplicadas no Brasil.")]),
                           pop.component_html]
        app.layout = html.Div(components_html)
        app.run_server(debug=True)


if __name__ == '__main__':
    unittest.main()
