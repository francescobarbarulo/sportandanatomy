import MySQLdb

class Database:
	def __init__(self):
		self.db = 'sportandanatomy'
		self.host = 'localhost'
		self.user = 'root'
		self.passwd = ''

		self.cursor = None

		print 'Connecting to %s on %s...' % (self.db, self.host)
		self.conn = MySQLdb.connect(db=self.db, host=self.host, user=self.user, passwd=self.passwd)

	def performQuery(self, query):
		if self.cursor is None:
			self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
		# execute query
		print(query);
		self.cursor.execute(query)
		self.conn.commit()

		print '%d rows affected' % (self.cursor.rowcount)
		return self.cursor

	def closeConnection(self):
		self.conn.close()
		print 'Closing db connection...'