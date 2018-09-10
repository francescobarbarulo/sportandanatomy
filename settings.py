from database import Database

class Settings:
	def __init__(self, recommended_sessions, threshold):
		self. recommended_sessions = recommended_sessions
		self.threshold = threshold

def get_exercise_settings(exerciseId):
	db = Database()

	queryText = 'SELECT * FROM exercise WHERE id = (%d)' % (exerciseId)
	cursor = db.performQuery(queryText)
	db.closeConnection()

	result = cursor.fetchone()
	return Settings(result['recommended_sessions'], result['threshold'])