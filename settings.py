from database import Database

class Settings:
	def __init__(self, session_number, threshold):
		self.session_number = session_number
		self.threshold = threshold

def get_settings():
	db = Database()

	queryText = 'SELECT * FROM settings'
	cursor = db.performQuery(queryText)
	db.closeConnection()

	result = cursor.fetchone()
	return Settings(result['session_number'], result['threshold'])


current_settings = get_settings()