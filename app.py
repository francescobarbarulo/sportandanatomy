# coding=utf-8

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import datetime
import math
from util import week_exercises, good_exercises

app = dash.Dash()

colors = ['#76D7C4', '#EC7063']

# numero di sessioni
f_labels = ['Done', 'Missing']
f_values = [len(week_exercises), 7 - len(week_exercises)] # da inserire quanti esercizi alla settimana
f_trace = go.Pie(labels=f_labels, values=f_values, textinfo='value', textfont=dict(color='#fff'), hole=0.5, sort=False, marker=dict(colors=colors))

# bontà esercizi
num_good_exercises = good_exercises(week_exercises)
g_labels = ['Good', 'Bad']
g_values = [num_good_exercises, len(week_exercises) - num_good_exercises]
g_trace = go.Pie(labels=g_labels, values=g_values, textinfo='value', textfont=dict(color='#fff'), hole=0.5, marker=dict(colors=colors))

# opzioni per dropdown menu
options = []
for i in range(0, len(week_exercises)):
    options.append({'label': 'Session '+str(i+1)+' started at '+week_exercises[i].data[0]['timestamp'].strftime('%H:%M')+' on '+week_exercises[i].data[0]['timestamp'].strftime('%b %d, %Y'), 'value': week_exercises[i].data[0]['timestamp']})

# andamento
time_x = []
real_angle_y = []
ideal_angle_y = []

if len(week_exercises) > 0:
    for exercise in week_exercises[0].data:
        time_x.append(exercise['timestamp'])
        real_angle_y.append(math.degrees(np.arccos(exercise['move'])))
        ideal_angle_y.append(math.degrees(np.arccos(exercise['ideal'])))

real_d_trace = go.Scatter(
    x = time_x,
    y = real_angle_y,
    name = 'Real',
    line = dict(
        color = ('#F9E79F')
    )
)

ideal_d_trace = go.Scatter(
    x = time_x,
    y = ideal_angle_y,
    name = 'Ideal',
    line = dict(
        color = ('#A569BD')
    )
)

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
                    'title': 'Frequency',
                    'paper_bgcolor': '#24292e',
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
                    'title': 'Goodness',
                    'paper_bgcolor': '#24292e',
                    'font': {
                        'color': '#ccc'
                    }
                }
            }
        )
    ], style={'columnCount': 2}),

    html.Div(children=[

        dcc.Dropdown(
            id='session-select',
            options=options,
            value=week_exercises[0].data[0]['timestamp']
        ),

        dcc.Graph(id='diff-graph')
    ])
])

@app.callback(
    dash.dependencies.Output('diff-graph', 'figure'),
    [dash.dependencies.Input('session-select', 'value')])
def update_figure(selected_session):
    session_to_show = None
    for session in week_exercises:
        if str(session.data[0]['timestamp']) == selected_session:
            session_to_show = session
            break

    time_x = []
    real_angle_y = []
    ideal_angle_y = []

    if session_to_show:
        for exercise in session_to_show.data:
            time_x.append(exercise['timestamp'])
            real_angle_y.append(math.degrees(np.arccos(exercise['move'])))
            ideal_angle_y.append(math.degrees(np.arccos(exercise['ideal'])))

    real_d_trace = go.Scatter(
        x = time_x,
        y = real_angle_y,
        name = 'Real',
        line = dict(
            color = ('#F9E79F')
        )
    )

    ideal_d_trace = go.Scatter(
        x = time_x,
        y = ideal_angle_y,
        name = 'Ideal',
        line = dict(
            color = ('#A569BD')
        )
    )

    return {
        'data': [real_d_trace, ideal_d_trace],
        'layout': go.Layout(
            xaxis=dict(
                showgrid=False
            ),
            yaxis=dict(
                showgrid=False
            ),
            paper_bgcolor='#24292e',
            plot_bgcolor='#24292e',
            font=dict(
                color='#ccc'
            )
        )
    }



if __name__ == '__main__':
    app.run_server(debug=True)