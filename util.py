# coding=utf-8

import datetime
import time
import csv
import math
from settings import current_settings as cs
from database import Database
		
def get_week_sessions(patientId):
    db = Database()
    queryText = '''SELECT *
                   FROM session S
                   		INNER JOIN
                   		patient P ON S.patientId = P.patientId
                   WHERE WEEK(DATE(S.timestamp), 1) = WEEK(CURRENT_DATE, 1)
                   		AND P.patientId = %s''' % (patientId)
    cursor = db.performQuery(queryText)
    db.closeConnection()
    return cursor

def good_exercises(exercises):
    count = 0

    for exercise in exercises:
    	average_gap = 0
    	valid_datasets = 0

        for position in exercise:
        	if position['ideal'] > 0:
        		average_gap += abs(position['angle'] - position['ideal'])
        		valid_datasets += 1

        average_gap /= valid_datasets

        if average_gap < cs.threshold:
            count += 1

    return count

def get_patients():
	db = Database()
	queryText = 'SELECT * FROM patient'
	cursor = db.performQuery(queryText)
	db.closeConnection()
	return cursor

# inserimento dati

def insert_rows():
	db = Database()

	for i in range(4, 8):
		data = []
		with open('Soggetto'+str(i)+'.csv', 'rb') as csvfile:
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
			queryText = 'INSERT INTO session(angle, ideal, patientId, timestamp) VALUES(%.10f, %.10f, %d, "%s")' % (record['value'], record['ideal'], i, started_at)
			cursor = db.performQuery(queryText);

		time.sleep(5);

	db.closeConnection()

#insert_rows()

patients = get_patients().fetchall()

'''
i = 0

while i < len(result):

    start = result[i]
    positions = []
    
    while i < len(result) and result[i]['timestamp'] < start['timestamp'] + datetime.timedelta(seconds=150):
        positions.append(result[i])
        i += 1

    week_exercises.append(Exercise(positions))
'''





