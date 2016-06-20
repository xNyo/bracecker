import tornado.web
import glob
import json

# Index handler
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		# Get services info
		noIncidents = True
		services = []
		for i, v in enumerate(glob.brace.checkers):
			services.append({})
			services[i]["name"] = v.name.title()
			services[i]["up"] = v.up
			services[i]["uptime"] = v.uptime

			if services[i]["up"] == False:
				noIncidents=False

		# Render and output template
		template = glob.templateEnv.get_template("index.html")
		htmlOutput = template.render(
			noIncidents = noIncidents,
			services = services,
			announcement = glob.announcement
		)
		self.write(htmlOutput)

# Response times API handler
class ResponseTimeHandler(tornado.web.RequestHandler):
	def get(self):
		# Return a json list with all responses times
		service = self.get_argument("service")
		data = []
		query = glob.db.fetchAll("SELECT response_time, time FROM status WHERE service = ? ORDER BY time ASC", [service])
		for i in query:
			data.append([int(i["time"])*1000, float(i["response_time"])])
		self.write(json.dumps(data))
