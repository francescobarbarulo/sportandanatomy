# coding=utf-8

import datetime
import json

import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output
from util import get_exercises

from app import app

def serve_layout():
	exercises = get_exercises().fetchall()
	datasets = [{'Name': exercise['name'], 'Recommended sessions': exercise['recommended_sessions'], 'Threshold': exercise['threshold']} for exercise in exercises]

	return html.Div(children=[
		html.Header(children=[
			html.H1(children='Exercises'),

			html.Div(children=[
				dcc.Link('NEW EXERCISE', href='/new-exercise')
			], className='nav')
		]),

		dt.DataTable(
			rows=datasets,
			columns=['Name', 'Recommended sessions', 'Threshold'],
			editable=False,
			id='exercises-list'
		),
	])

layout = serve_layout