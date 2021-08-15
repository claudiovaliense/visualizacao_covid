import pandas as pd

import plotly.graph_objects as go

def pad_list(l, n):

    pad = [1] * (n - len(l))

    return l + pad

def stacked_area(df, x_column, y_column, filename, category):

    fig = go.Figure()

    categories = df[category].unique().tolist()

    df_total = df.groupby(x_column).apply(lambda e: pd.DataFrame({'Total (semana)': [sum(e['Total (semana)'].tolist())]})).reset_index()
    df_total.columns = [x_column, 'a', 'Total dia (semana)']

    df_total = df_total[[x_column, 'Total dia (semana)']]
    # unique_x_column = df_total[x_column].unique().tolist()
    # pad_df = {x_column: [], 'Total dia (semana)': []}
    # for i in range(len(unique_x_column)):
    #     pad_df[x_column].append(unique_x_column[i])
    #     pad_df['Total dia (semana)'].append(1)
    #
    # pad_df = pd.DataFrame(pad_df)
    #
    # df_total = pd.concat([df_total, pad_df], ignore_index=True)

    df = df.join(df_total.set_index(x_column), on=x_column)
    df['Total semana (%)'] = (df['Total (semana)'] / df['Total dia (semana)'])*100
    x = df[x_column].unique().tolist()

    semanas_unicas = len(df[x_column].unique().tolist())
    n = semanas_unicas

    azul = "rgb(0, 102, 255)"
    azul_escuro = "rgb(0, 102, 153)"
    laranja = "rgb(255, 153, 0)"
    verde = "rgb(0, 153, 51)"
    vermelho = "rgb(204, 0, 0)"
    roxo = "rgb(153, 51, 153)"
    rosa = "rgb(255, 0, 255)"
    marrom = "rgb(153, 102, 51)"
    color = [azul, laranja, azul_escuro, roxo, rosa, marrom]

    for i in range(len(categories)):
        y = df[df[category] == categories[i]][y_column].tolist()
        y = pad_list(y, n)
        if i == 0:
            fig.add_trace(go.Scatter(
                x=x, y=y,
                mode='lines',
                line=dict(width=0.5, color=color[i]),
                name=categories[i],
                stackgroup='one',
                groupnorm='percent'  # sets the normalization for the sum of the stackgroup
            ))
        else:
            fig.add_trace(go.Scatter(
                x=x, y=y,
                mode='lines',
                line=dict(width=0.5, color=color[i]),
                name=categories[i],
                stackgroup='one'  # sets the normalization for the sum of the stackgroup
            ))

    fig.update_layout(
        showlegend=True,
        xaxis_type='category',
        yaxis=dict(
            type='linear',
            range=[1, 100],
            ticksuffix='%'),
        xaxis_title="Semana - início em 17/01/2021 até 20/06/2021",
        yaxis_title="Vacinas (%)",
        font=dict(
            size=16)
        )

    #fig.write_html(filename)

    return fig