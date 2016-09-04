import glob
import requests
import time
import threading
import json

class checker:
	"""Single checker instance"""
	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.uptime = 0	# cache
		self.up = False	# cache
		self.responseTimesJson = "" #cache

class checkers:
	def __init__(self, interval = 60, timeout = 5, allowedCodes = [404]):
		"""Initialize a list of checkers"""
		self.checkers = []
		self.interval = interval
		self.timeout = timeout
		self.allowedCodes = allowedCodes

	def addChecker(self, name, url):
		"""Register a new checker"""
		self.checkers.append(checker(name, url))

	def start(self):
		"""Start check look"""
		self.check()

	def save(self, data):
		"""Save content of data list in db [{"name", "time"}]"""
		t = int(time.time())
		query = "INSERT INTO status (id, service, time, response_time) VALUES"
		for i,v in enumerate(data):
			if i > 0:
				query += ","
			query += "(NULL, '{}', '{}', '{}')".format(v["name"], t, v["time"])
		glob.db.execute(query)

	def updateUptime(self):
		"""Update up status and uptime for every checker"""
		for i in self.checkers:
			upCount = int(glob.db.fetch("SELECT COUNT(*) AS count FROM status WHERE service = ? AND response_time > -1", [i.name])["count"])
			total = glob.db.fetchAll("SELECT response_time FROM status WHERE service = ? ORDER BY time ASC", [i.name])
			i.up = True if total[len(total)-1]["response_time"] > -1 else False
			i.uptime = float("{:.2f}".format((100*upCount)/len(total)))

	def cacheResponseTimes(self):
		"""Cache response times from db"""
		print("Saving json response in memory...")
		for i in self.checkers:
			data = []
			query = glob.db.fetchAll("SELECT response_time, time FROM status WHERE service = ? AND time >= ? ORDER BY time ASC", [i.name, int(time.time())-3600])
			for j in query:
				data.append([int(j["time"])*1000, float(j["response_time"])])
			i.responseTimesJson = json.dumps(data)
		print("Done")

	def check(self):
		"""Check loop. Call only once"""
		data = []
		for i in self.checkers:
			try:
				# Ping the service
				print("Checking {}... ".format(i.name), end="")
				response = requests.get(i.url, timeout=self.timeout)
				print(" ({}) ".format(response.status_code), end="")
				if (response.status_code < 200 or response.status_code > 226) and response.status_code not in self.allowedCodes:
					raise
				print("UP!")

				# No errors, service is up
				data.append({"name": i.name, "time": response.elapsed.total_seconds()})
			except:
				# Error, service is down
				print("DOWN!")
				data.append({"name": i.name, "time": -1})

		# Save new data in sqlite db and update uptime
		self.save(data)
		self.updateUptime()
		self.cacheResponseTimes()

		# Schedule a new check
		print("Next check in {} seconds\n".format(self.interval))
		threading.Timer(self.interval, self.check).start()
