# coding=utf-8

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from util import week_exercises, good_exercises

app = dash.Dash()

colors = ['#76D7C4', '#EC7063']

# numero di sessioni
f_labels = ['Sessioni eseguite', 'Sessioni mancanti']
f_values = [len(week_exercises), 7 - len(week_exercises)] # da inserire quanti esercizi alla settimana
f_trace = go.Pie(labels=f_labels, values=f_values, textinfo='value', textfont=dict(color='#fff'), hole=0.5, sort=False, marker=dict(colors=colors))

# bontà esercizi
num_good_exercises = good_exercises(week_exercises)
g_labels = ['Sessioni buone', 'Sessioni non buone']
g_values = [num_good_exercises, len(week_exercises) - num_good_exercises]
g_trace = go.Pie(labels=g_labels, values=g_values, textinfo='value', textfont=dict(color='#fff'), hole=0.5, marker=dict(colors=colors))

app.layout = html.Div(style={'backgroundColor': '#24292e'}, children=[
    html.Header(children=[
        html.H1(children='Sport and Anatomy'),
    ]),

    html.Div(children=[
        dcc.Graph(
            id='frequence-graph',
            figure={
                'data': [f_trace],
                'layout': {
                    'title': 'Frequenza',
                    'paper_bgcolor': '#24292e',
                    'display': 'inline',
                    'font': {
                        'color': '#ccc'
                    }
                }
            }
        ),

        dcc.Graph(
            id='goodness-graph',
            figure={
                'data': [g_trace],
                'layout': {
                    'title': u'Bontà',
                    'paper_bgcolor': '#24292e',
                    'display': 'inline',
                    'font': {
                        'color': '#ccc'
                    }
                }
            }
        )
    ],
    className='flex-container')
])

if __name__ == '__main__':
    app.run_server(debug=True)