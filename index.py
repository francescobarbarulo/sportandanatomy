import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output
import datetime

from app import app
from apps import dashboard, new_exercise, new_patient, exercises, patients

def serve_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
        #html.Div(children=datetime.datetime.now()),
        html.Div(id='page-content')
    ])

app.layout = serve_layout


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return dashboard.layout()
    elif pathname == '/exercises':
        return exercises.layout()
    elif pathname == '/patients':
        return patients.layout()
    elif pathname == '/new-exercise':
    	return new_exercise.layout
    elif pathname == '/new-patient':
    	return new_patient.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)