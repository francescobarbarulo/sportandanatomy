# coding=utf-8

import datetime

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from util import new_patient

from app import app

layout = html.Div(children=[
	html.Div(children=[
		dcc.Link(u'⟵ Back to dashboard', href='/')
	], className='new-header'),

	html.Div(children=[
		html.H1(children='New patient'),

		html.Div(children=[
			html.Label(children="Name"),
			dcc.Input(id='name', type='text', autocomplete='off'),

			html.Label(children="Birthday"),
		    dcc.Input(id='birthday', type='date'),

		    html.Div(id='patient-response', className='response'),

		    html.Button(id='submit-button', n_clicks=0, children='CREATE PATIENT'),
		], className='form')
	], className='new')
])

@app.callback(Output('patient-response', 'children'),
			[Input('submit-button', 'n_clicks')],
			[State('name', 'value'),
            State('birthday', 'value')])
def create_patient(n_clicks, name, birthday):
	if n_clicks == 0:
		return None

	if name is None or birthday is None:
		return html.Div(children='Enter name and birthday', className="error")

	if not new_patient(name, birthday):
		return html.Div(children='Something went wrong', className="error")

	return html.Div(children='New patient created', className="success")