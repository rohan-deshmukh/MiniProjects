import MySQLdb

def connection():
	conn = MySQLdb.connect(host="localhost",
						   user="",
							passwd="",
							db="")
	c = conn.cursor()

	return c, conn