# coding=utf-8

import datetime
import time
import csv
import math
from database import Database
		
def get_week_sessions(patientId, exerciseId):
    db = Database()
    queryText = '''SELECT *
                   FROM position P
                   		INNER JOIN
                   		session S ON S.sessionId = P.sessionId
                   WHERE WEEK(DATE(P.timestamp), 1) = WEEK(CURRENT_DATE, 1)
                   		AND S.patientId = %d AND S.exerciseId = %d''' % (patientId, exerciseId)
    cursor = db.performQuery(queryText)
    db.closeConnection()
    return cursor

def good_exercises(exercises, threshold):
    count = 0

    for exercise in exercises:
    	average_gap = 0
    	valid_datasets = 0

        for position in exercise:
        	if position['ideal'] > 0:
        		average_gap += abs(position['angle'] - position['ideal'])
        		valid_datasets += 1

        average_gap /= valid_datasets

        if average_gap < threshold:
            count += 1

    return count

def get_patients():
	db = Database()
	queryText = 'SELECT * FROM patient'
	cursor = db.performQuery(queryText)
	db.closeConnection()
	return cursor

def get_exercises():
	db = Database()
	queryText = 'SELECT * FROM exercise'
	cursor = db.performQuery(queryText)
	db.closeConnection()
	return cursor

def new_session(patientId, exerciseId):
	db = Database()
	queryText = 'INSERT INTO session(patientId, exerciseId) VALUES (%d, %d)' % (patientId, exerciseId)
	cursor = db.performQuery(queryText)
	db.closeConnection()
	return cursor.lastrowid

def new_exercise(name, sessions, threshold):
	db = Database()
	queryText = 'INSERT INTO exercise(name, recommended_sessions, threshold) VALUES ("%s", %d, %.2f)' % (name, sessions, threshold)
	cursor = db.performQuery(queryText)
	db.closeConnection()
	return cursor.lastrowid

def new_patient(name, birthday):
	db = Database()
	queryText = 'INSERT INTO patient(name, birthday) VALUES ("%s", "%s")' % (name, birthday)
	cursor = db.performQuery(queryText)
	db.closeConnection()
	return cursor.lastrowid

# inserimento dati

def insert_rows():
	db = Database()

	for i in range(1, 8):
		data = []
		with open('Soggetto'+str(i)+'.csv', 'rb') as csvfile:
			sessionId = new_session(i, 1)
			lines = csv.reader(csvfile, delimiter=',', quotechar='"')
			for row in lines: 
				timestamp = row[0].replace(",",".")
				value = row[1].replace(",",".")
				ideal = row[10].replace(",",".")

				try:
					value = float(value)
					ideal = float(ideal)
					value = math.acos(value)
					ideal = math.acos(ideal)
					data.append({'timestamp': timestamp, 'value': value, 'ideal': ideal})

				except ValueError:
					continue

		started_at = datetime.datetime.now()
		for record in data:
			started_at = started_at + datetime.timedelta(microseconds=50000)
			queryText = 'INSERT INTO position (angle, ideal, sessionId, timestamp) VALUES (%.10f, %.10f, %d, "%s")' % (record['value'], record['ideal'], sessionId, started_at)
			cursor = db.performQuery(queryText);

		time.sleep(5);

	db.closeConnection()

#insert_rows()





