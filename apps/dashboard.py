# coding=utf-8

import datetime
import json

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from settings import get_exercise_settings
from util import get_week_sessions, good_exercises, get_patients, get_exercises

from app import app

colors = ['#76D7C4', '#EC7063']

def serve_layout():
    patients = get_patients().fetchall()
    exercises = get_exercises().fetchall()

    print patients

    return html.Div(children=[
    html.Header(children=[
        html.H1(children='Sport and Anatomy'),

        html.Div(children=[
            dcc.Link('PATIENTS', href="/patients"),
            dcc.Link('EXERCISES', href="/exercises")
        ], className='nav'),
    ]),

    html.Div(children=[
        html.Div(children=[

            html.Div(children=[
                dcc.Dropdown(
                    id='select-patient',
                    options=[{'label': x['name'], 'value': x['patientId']} for x in patients],
                    placeholder='Select patient...'
                ),

                dcc.Dropdown(
                    id='select-exercise',
                    options=[{'label': x['name'], 'value': x['id']} for x in exercises],
                    placeholder='Select exercise...'
                )
            ]),

            html.Div(children=[

                dcc.Graph(
                    id='frequency-graph',
                    figure={
                        'data': [go.Pie()],
                        'layout': {
                            'title': 'Frequency',
                            'plot_bgcolor': '#24292e',
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
                        'data': [go.Pie()],
                        'layout': {
                            'title': 'Goodness',
                            'plot_bgcolor': '#24292e',
                            'paper_bgcolor': '#24292e',
                            'font': {
                                'color': '#ccc'
                            }
                        }
                    }
                )
            ], className="table", style={'columnCount': 2}),
        ], className="section"),

        html.Div(children=[

            dcc.Dropdown(
                id='session-select',
                placeholder='Select session...'
            ),

            dcc.Graph(
                id='diff-graph',
                figure={
                    'data': [go.Scatter()],
                    'layout': {
                        'paper_bgcolor': '#24292e',
                        'plot_bgcolor': '#24292e',
                        'font': {
                            'color': '#ccc'
                        }
                    }
                }
            )
        ], className="section")
    ], className='overview'),

    html.Div(children='Università di Pisa', className="footer"),

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'})
])

layout = serve_layout

@app.callback(Output('intermediate-value', 'children'), 
    [Input('select-patient', 'value'), Input('select-exercise', 'value')])
def get_data(patientId, exerciseId):
    if patientId is None or exerciseId is None:
        return None

    exercise_settings = get_exercise_settings(exerciseId)
    result = get_week_sessions(patientId, exerciseId).fetchall()

    week_exercises =[]
    i = 0
    while i < len(result):
        start = result[i]
        positions = []

        while i < len(result) and result[i]['timestamp'] < start['timestamp'] + datetime.timedelta(seconds=150):
            positions.append({'timestamp': str(result[i]['timestamp']), 'angle': result[i]['angle'], 'ideal': result[i]['ideal']})
            i += 1

        week_exercises.append(positions)

    return json.dumps({'data': week_exercises, 'settings': {'recommended_sessions': exercise_settings.recommended_sessions, 'threshold': exercise_settings.threshold}})

@app.callback(
    Output('frequency-graph', 'figure'),
    [Input('intermediate-value', 'children')])
def set_frequency_graph(jsonified_data):
    if jsonified_data is None:
        return {
            'data': [go.Pie()],
            'layout': {
                'title': 'Frequency',
                'plot_bgcolor': '#24292e',
                'paper_bgcolor': '#24292e',
                'font': {
                    'color': '#ccc'
                }
            }
        }

    datasets = json.loads(jsonified_data)

    # numero di sessioni
    f_labels = ['Done', 'Missing']
    f_values = [len(datasets['data']), datasets['settings']['recommended_sessions'] - len(datasets['data'])] # da inserire quanti esercizi alla settimana
    f_trace = go.Pie(labels=f_labels, values=f_values, textinfo='value', textfont=dict(color='#fff'), hole=0.5, sort=False, marker=dict(colors=colors))

    return {
        'data': [f_trace],
        'layout': {
            'title': 'Frequency',
            'plot_bgcolor': '#24292e',
            'paper_bgcolor': '#24292e',
            'font': {
                'color': '#ccc'
            }
        }

    }


@app.callback(
    Output('goodness-graph', 'figure'),
    [Input('intermediate-value', 'children')])
def set_goodness_graph(jsonified_data):
    if jsonified_data is None:
        return {
            'data': [go.Pie()],
            'layout': {
                'title': 'Goodness',
                'plot_bgcolor': '#24292e',
                'paper_bgcolor': '#24292e',
                'font': {
                    'color': '#ccc'
                }
            }
        }

    datasets = json.loads(jsonified_data)
    # bontà esercizi
    num_good_exercises = good_exercises(datasets['data'], datasets['settings']['threshold'])
    labels = ['Good', 'Bad']
    values = [num_good_exercises, len(datasets['data']) - num_good_exercises]
    trace = go.Pie(labels=labels, values=values, textinfo='value', textfont=dict(color='#fff'), hole=0.5, marker=dict(colors=colors))
 
    return {
        'data': [trace],
        'layout': {
            'title': 'Goodness',
            'plot_bgcolor': '#24292e',
            'paper_bgcolor': '#24292e',
            'font': {
                'color': '#ccc'
            }
        }

    }

@app.callback(
    Output('session-select', 'options'),
    [Input('intermediate-value', 'children')])
def set_session_select(jsonified_data):
    if jsonified_data is None:
        return []

    datasets = json.loads(jsonified_data)
    # opzioni per dropdown menu
    return [{'label': 'Session '+str(i+1), 'value': datasets['data'][i][0]['timestamp']} for i in range(0, len(datasets['data']))]

@app.callback(
    Output('diff-graph', 'figure'),
    [Input('intermediate-value', 'children'), Input('session-select', 'value')])
def update_figure(jsonified_data, selected_session):
    if jsonified_data is None:
        return {
        'data': [],
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

    datasets = json.loads(jsonified_data)

    session_to_show = None
    for session in datasets['data']:
        if str(session[0]['timestamp']) == selected_session:
            session_to_show = session
            break

    time_x = []
    real_angle_y = []
    ideal_angle_y = []

    if session_to_show:
        for exercise in session_to_show:
            time_x.append(exercise['timestamp'])
            real_angle_y.append(exercise['angle'])
            ideal_angle_y.append(exercise['ideal'])

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
