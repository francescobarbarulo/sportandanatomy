# coding=utf-8

import datetime

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from util import new_exercise

from app import app

layout = html.Div(children=[
	html.Div(children=[
		dcc.Link(u'⟵ Back to dashboard', href='/')
	], className='new-header'),

	html.Div(children=[
		html.H1(children='New exercise'),

		html.Div(children=[
			html.Label(children="Name"),
			dcc.Input(id='name', type='text', autocomplete='off'),

			html.Label(children="Recommended sessions"),
		    dcc.Input(id='sessions', type='number', min=1),

		    html.Label(children="Threshold"),
		    dcc.Slider(id='threshold',
			    min=0,
			    max=10,
			    marks={i: '{}'.format(i*0.1) for i in range(0, 11)},
			    value=5
			),

		    html.Div(id='exercise-response', className='response'),

		    html.Button(id='submit-button', n_clicks=0, children='CREATE EXERCISE'),
		], className='form')
	], className='new')
])

@app.callback(Output('exercise-response', 'children'),
			[Input('submit-button', 'n_clicks')],
			[State('name', 'value'),
            State('sessions', 'value'),
            State('threshold', 'value')])
def create_exercise(n_clicks, name, sessions, threshold):
	print threshold

	if n_clicks == 0:
		return None

	if name is None or sessions is None or threshold is None:
		return html.Div(children='Enter name, recommended sessions and threshold', className="error")

	if not new_exercise(name, sessions, threshold*0.1):
		return html.Div(children='Something went wrong', className="error")

	return html.Div(children='New exercise created', className="success")