import plotly.graph_objects as go

def pad_list(l, n):

    pad = [1] * (n - len(l))

    return l + pad

def overlaid_area(df, x_column, y_column, filename, category):

    df = df.sort_values(x_column)
    dose_1 = df[df[category] == 'Primeira dose']
    x_dose_1 = dose_1[x_column].tolist()
    y_dose_1 = dose_1[y_column].cumsum()
    completa = df[df[category] == 'Vacinação completa']
    x_completa = completa[x_column].tolist()
    y_completa = completa[y_column].cumsum()

    azul_escuro = "rgb(0, 102, 255)"
    azul = "rgb(102, 204, 255)"

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_dose_1, y=y_dose_1, fill='tozeroy', legendgroup='a', name='Primeira dose', fillcolor=azul))  # fill down to xaxis
    fig.add_trace(go.Scatter(x=x_completa, y=y_completa, fill='tozeroy', legendgroup='a', name='Vacinação completa', fillcolor=azul_escuro))  # fill to trace0 y

    fig.update_layout(
        showlegend=True,
        xaxis_type='category',
        xaxis_title="Semana - início em 17/01/2021 até 20/06/2021",
        yaxis_title="Total de vacinas aplicadas",
        font=dict(
            size=25))

    return fig

