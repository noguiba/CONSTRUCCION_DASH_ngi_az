import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


data_agricola = pd.read_excel('data_final_agr.xlsx')
list_ciudad = list(data_agricola['ciudad'].unique())

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.H3('CONTRATOS SECTOR AGRICULTURA - COLOMBIA', style = {'margin-bottom': '5px', 'color': 'aqua'}),
            ])
        ], className = "create_container1 four columns", id = "title"),

    ], id = "header", className = "row flex-display", style = {"margin-bottom": "10px"}),


    html.Div([
        html.Div([
            html.P('Ciudad', className = 'fix_label', style = {'color': 'red'}),
            dcc.Dropdown(id = 'select_ciudad',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Colombia, Bogotá, Bogotá',
                         placeholder = 'Select Ciudad',
                         options = [{'label': c, 'value': c}
                                    for c in list_ciudad], className = 'dcc_compon'),

            html.P('Seleccionar el año', className = 'fix_label', style = {'color': 'red', 'margin-top': '30px'}),
            dcc.Slider(id = 'slider_year',
                       included = True,
                       updatemode='drag',
                       tooltip={'always_visible': True},
                       min = 2000,
                       max = 2021,
                       step = 1,
                       value = 2000,
                       marks = {str(yr): str(yr) for yr in range(2000, 2022, 5)},
                       className = 'dcc_compon'),

            html.P('Nombre de la Entidad', className = 'fix_label', style = {'color': 'red', 'margin-top': '30px'}),
            dcc.Checklist(id = 'radio_items',
                          options = [{'label': d, 'value': d} for d in sorted(data_agricola['entidad'].unique())],
                          value=["ICA_NAL"],
                          style = {'color': 'white'}, className = 'dcc_compon'),

            ], className = "create_container2 four columns"),


        html.Div([
            dcc.Graph(id = 'bubble_chart',
                      config = {'displayModeBar': 'hover'}),

        ], className = "create_container2 eight columns"),

    ], className = "row flex-display"),

], id= "mainContainer", style={"display": "flex", "flex-direction": "column"})


@app.callback(Output('bubble_chart', 'figure'),
              [Input('select_ciudad', 'value')],
              [Input('slider_year', 'value')],
              [Input('radio_items', 'value')])
def update_graph(select_ciudad, slider_year, radio_items):
    data_agricola1 = data_agricola.groupby(['entidad', 'ciudad', 'destino_gasto', 'año', 'poblacion', 'No_contratos/100k pop'])['No_contratos'].sum().reset_index()
    data_agricola2 = data_agricola1[(data_agricola1['ciudad'] == select_ciudad) & (data_agricola1['año'] >= slider_year) & (data_agricola1['entidad'].isin(radio_items))]

    return {
        'data':[go.Scatter(
                    x=data_agricola2['año'],
                    y=data_agricola2['No_contratos'],
                    text = data_agricola2['destino_gasto'],
                    textposition = 'top center',
                    mode = 'markers + text',
                    marker = dict(
                        size = data_agricola2['No_contratos'] / 10,
                        color = data_agricola2['No_contratos'],
                        colorscale = 'HSV',
                        showscale = False,
                        line = dict(
                            color = 'MediumPurple',
                            width = 2
                        )),
                    hoverinfo='text',
                    hovertext=
                    '<b>Country</b>: ' + data_agricola2['ciudad'].astype(str) + '<br>' +
                    '<b>Age</b>: ' + data_agricola2['entidad'].astype(str) + '<br>' +
                    '<b>Sex</b>: ' + data_agricola2['destino_gasto'].astype(str) + '<br>' +
                    '<b>Year</b>: ' + data_agricola2['año'].astype(str) + '<br>' +
                    '<b>Population</b>: ' + [f'{x:,.0f}' for x in data_agricola2['poblacion']] + '<br>' +
                    '<b>Suicides/100k pop</b>: ' + [f'{x:,.0f}' for x in data_agricola2['No_contratos/100k pop']] + '<br>' +
                    '<b>Suicides</b>: ' + [f'{x:,.0f}' for x in data_agricola2['No_contratos']] + '<br>'


              )],


        'layout': go.Layout(
             plot_bgcolor='#010915',
             paper_bgcolor='#010915',
             title={
                'text': 'Contratos (fun: funcionamiento - Inv: Inversión - ND: No Disponible): ' + (select_ciudad),

                'y': 0.96,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'yellow',
                        'size': 20},

             hovermode='x',
             xaxis=dict(title='<b>Año</b>',
                        tick0=0,
                        dtick=1,
                        color='silver',
                        showline=True,
                        showgrid=False,
                        linecolor='white',
                        linewidth=1,


                ),

             yaxis=dict(title='<b>No. de contratos</b>',
                        color='silver',
                        showline=False,
                        showgrid=True,
                        linecolor='white',

                ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#010915',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},
            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white',


                 )
        )

    }


if __name__ == '__main__':
    app.run_server()