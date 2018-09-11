# coding=utf-8

import datetime
import json

import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output
from util import get_patients

from app import app

def serve_layout():
	patients = get_patients().fetchall()
	datasets = [{'Id': patient['patientId'], 'Name': patient['name'], 'Birthday': patient['birthday']} for patient in patients]

	return html.Div(children=[
		html.Header(children=[
			html.H1(children='Patients'),

			html.Div(children=[
				dcc.Link('NEW PATIENT', href='/new-patient')
			], className='nav')
		]),

		dt.DataTable(
			rows=datasets,
			columns=['Id', 'Name', 'Birthday'],
			editable=False,
			id='patients-list'
		),
	])

layout = serve_layout