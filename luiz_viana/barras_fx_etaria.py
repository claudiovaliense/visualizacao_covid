import plotly.express as px
from plotly.subplots import make_subplots

def barras_fx_etaria(df, r_min, r_max):



    #fig = go.Figure()
    
    fig = px.bar(df, x="vacina_dataaplicacao", y="quantidade", 
                    color='faixa_etaria',
                    labels={'vacina_dataaplicacao':'Data de Aplicação',
                            'quantidade': 'Doses Aplicadas',
                            'faixa_etaria': 'Faixa Etária'})
    
    
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(
            size=16)
    ))
    
    fig.update_yaxes(
        range=[r_min, r_max]
    )
    
  

    return fig

def barras_sub_plot_vacina(df, r_min, r_max):
    
    corona = df[df['vacina_nome'] == 'Covid-19-Coronavac-Sinovac/Butantan'] 
    corona = corona.groupby(['vacina_dataaplicacao', 'faixa_etaria'], 
                                        as_index=False)['quantidade'].sum()
    
    astrazeneca = df[df['vacina_nome'] == 'Covid-19-AstraZeneca' ]
    astrazeneca = astrazeneca.append(
                    df[df['vacina_nome'] == 'Vacina Covid-19 - Covishield' ],
                    ignore_index=True)
    
    astrazeneca = astrazeneca.groupby(['vacina_dataaplicacao', 
                                        'faixa_etaria'], 
                                        as_index=False)['quantidade'].sum()
    
    pfizer = df[df['vacina_nome'] 
            == 'Vacina covid-19 - BNT162b2 - BioNTech/Fosun Pharma/Pfizer'] 
    pfizer = pfizer.groupby(['vacina_dataaplicacao', 'faixa_etaria'], 
                                        as_index=False)['quantidade'].sum()
    
    jansen = df[df['vacina_nome'] 
                        == 'Vacina covid-19 - Ad26.COV2.S - Janssen-Cilag'] 
    jansen = jansen.groupby(['vacina_dataaplicacao', 'faixa_etaria'], 
                                        as_index=False)['quantidade'].sum()
    

    df = df.groupby(['vacina_dataaplicacao', 'faixa_etaria'], 
                                        as_index=False)['quantidade'].sum()
    
    
    fig1 = px.bar(corona, x="vacina_dataaplicacao", y="quantidade", 
                color='faixa_etaria')
    fig1_traces = []
    for trace in range(len(fig1["data"])):
        fig1_traces.append(fig1["data"][trace])
    

    fig2 = px.bar(astrazeneca, x="vacina_dataaplicacao", y="quantidade", 
                color='faixa_etaria')
    fig2_traces = []
    for trace in range(len(fig2["data"])):
        fig2_traces.append(fig2["data"][trace])


    fig3 = px.bar(pfizer, x="vacina_dataaplicacao", y="quantidade", 
                color='faixa_etaria')
    fig3_traces = []
    for trace in range(len(fig3["data"])):
        fig3_traces.append(fig3["data"][trace])

    
    fig4 = px.bar(jansen, x="vacina_dataaplicacao", y="quantidade", 
                color='faixa_etaria')    
    fig4_traces = []
    for trace in range(len(fig4["data"])):
        fig4_traces.append(fig4["data"][trace])

    
    fig5 = px.bar(df, x="vacina_dataaplicacao", y="quantidade", 
                color='faixa_etaria')    
    fig5_traces = []
    for trace in range(len(fig5["data"])):
        fig5_traces.append(fig5["data"][trace])
    

    fig = make_subplots(
        rows=3, cols=2,
        specs=[[{}, {}],
                [{}, {}]
                ,[{"colspan": 2}, None]
                ],
        subplot_titles=("Coronavac","Astrazeneca" 
                        , "PFizer", "Jansen",
                        "Total"
                        ),
        horizontal_spacing = 0.05,
        vertical_spacing=0.15)        

    for traces in fig1_traces:
        fig.append_trace(traces, row=1, col=1)
    
    for traces in fig2_traces:
        fig.append_trace(traces, row=1, col=2)
        
    for traces in fig3_traces:
        fig.append_trace(traces, row=2, col=1)

    for traces in fig4_traces:
        fig.append_trace(traces, row=2, col=2)        

    for traces in fig5_traces:
        fig.append_trace(traces, row=3, col=1)     
        
    fig.update_layout(height=550, 
                      margin=dict(t=50),
                      font=dict(
                          size=16)
                      )
    #, margin=dict(l=0.1,r=0.1,b=0,t=50)
    fig.update_xaxes(title_text="Data de Aplicação", row=3, col=1)
    fig.update_xaxes(range=['2021-01-10','2021-06-30'])
    
    fig.update_yaxes(range=[r_min, r_max])
    fig.update_yaxes(title_text="Doses Aplicadas", row=3, col=1)
    fig.update_layout(coloraxis=dict(cmin=0, cmax=100))
    fig.update_coloraxes(colorbar_title=dict(text="Faixa Etária",
                                             side="bottom"))
 
    return fig