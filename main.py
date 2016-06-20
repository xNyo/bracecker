import db
import os
import glob
import brace
import tornado.ioloop
import tornado.web
import os
import sys
import json
import jinja2
import handlers

if __name__ == "__main__":
	# Load template
	glob.templateLoader = jinja2.FileSystemLoader(searchpath="html")
	glob.templateEnv = jinja2.Environment(loader=glob.templateLoader)

	# Connect/create DB
	newDB = True if not os.path.isfile("bracecker.db") else False
	glob.db = db.db("bracecker.db")
	if newDB == True:
		glob.db.execute("CREATE TABLE `status` (`id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, `service` INTEGER, `time` INTEGER, `response_time` INTEGER);")

	# Load announcement
	if os.path.isfile("announcement.txt"):
		with open("announcement.txt") as f:
			glob.announcement = f.read()

	# Load and create services
	glob.brace = brace.checkers()
	if os.path.isfile("services.json"):
		with open("services.json") as f:
			try:
				content = f.read()
				data = json.loads(content)
				for i in data:
					glob.brace.addChecker(i["name"], i["url"])
			except:
				print("Error while loading services.json")
				raise
	else:
		print("services.json doesn't exist")
		sys.exit()

	# Set the brace on fire
	glob.brace.start()

	# Create and start tornado server
	app = tornado.web.Application([
			(r"/", handlers.MainHandler),
			(r"/api/response_time", handlers.ResponseTimeHandler)
		], **{
			"static_path": os.path.join(os.path.dirname(__file__), "static"),
		})
	app.listen(6996)
	tornado.ioloop.IOLoop.current().start()
