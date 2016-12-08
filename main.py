import db
import glob
import tornado.web
import os
import json
import jinja2
import handlers
import argparse
import threading

if __name__ == "__main__":
	# CLI arguments
	parser = argparse.ArgumentParser(description="Check uptime and response times of your services")
	parser.add_argument("-d", "--datadog", dest="datadog",
						help="If present, report data to datadog.",
						action="store_true")
	parser.add_argument("-n", "--noweb", dest="noWeb",
						help="If present, don't start the bracecker web server. Use it along with --datadog if you just want to report response times and uptime to datadog.",
						action="store_true")
	parser.add_argument("-p", "--port", dest="port", help="Webserver port", default=6996, type=int)
	parser.add_argument("-c", "--check-every", dest="interval", help="Number of seconds to wait between checks", default=60, type=int)
	args = parser.parse_args()

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

	# Set up datadog agent
	if args.datadog:
		import datadog
		# Load datadog api and app key=
		with open("datadog.json", "r") as f:
			try:
				content = f.read()
				data = json.loads(content)
				glob.datadogConfig["apiKey"] = data["api_key"]
				glob.datadogConfig["appKey"] = data["app_key"]
			except:
				print("error while loading datadog.json")
				raise

		# Initialize datadog agent
		datadog.initialize(api_key=glob.datadogConfig["apiKey"], app_key=glob.datadogConfig["appKey"])
		glob.datadog = datadog.ThreadStats()
		glob.datadog.start()

	# Load and create services
	import brace
	glob.brace = brace.checkers(interval=args.interval, datadog=glob.datadog, webServer=True if args.noWeb is None else False)
	with open("services.json", "r") as f:
		try:
			content = f.read()
			data = json.loads(content)
			for i in data:
				glob.brace.addChecker(i["name"], i["url"])
		except:
			print("Error while loading services.json")
			raise

	# Set the brace on fire
	glob.brace.start()

	# Create and start tornado server
	# if we are not in datadog mode
	if not args.noWeb:
		app = tornado.web.Application([
				(r"/", handlers.MainHandler),
				(r"/api/response_time", handlers.ResponseTimeHandler)
			], **{
				"static_path": os.path.join(os.path.dirname(__file__), "static"),
			})
		app.listen(args.port)
		print("Starting tornado on port {}".format(args.port))
		tornado.ioloop.IOLoop.current().start()