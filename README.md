## Bracecker
### Avoid setting your server on fire like a brace with bracecker!
Bracecker is a python script that checks the status of your services every 60 seconds. It uses a sqlite database to store statuses and response times, so you don't have to set up a MySQL server to use bracecker. Bracecker has also an integrated tornado server that shows a fancy page with the status of your services, uptimes and a response time graph.

## Requirements
- Python 3.5
- Requests
- sqlite3
- Tornado
- Jinja2
- Datadog _(optional)_

## Setting up
```
$ cd some_directory
$ git clone repo_url
$ cd bracecker
$ sudo pip install -r requirements.txt
$ cp services.sample.json services.json
$ nano services.json
...
```

### Web server only setup
If you want a simple web page that displays your uptime, run bracecker with:
```
$ python3 main.py
```

### Datadog + Web server
If you want bracecker to report response times and uptime to datadog and display the uptime on a web page, run bracecker with:
```
$ python3 main.py --datadog
```
_Make sure to create `datadog.json` if you want to use bracecker with datadog. Use `datadog.sample.json` as a sample._

### Datadog only setup
If you want bracecker to report response times and uptime to datadog, without the web page for that displays uptime, run:
```
$ python3 main.py --datadog --noweb
```
_Make sure to create `datadog.json` if you want to use bracecker with datadog. Use `datadog.sample.json` as a sample._

## Configuration files
### services.json
Bracecker will look for the services to check inside the `services.json` file. It's super easy to config, use `services.sample.json` as a sample.
Bracecker will consider a service as **UP** if the HTTP status code the service returns is between **200 and 226 (inclusive) or 404**, everything else or a timeout (5 secs) will mark the service as **DOWN**.

### datadog.json
If you want to use bracecker along with datadog (`--datadog` argument), make sure to create a `datadog.json` file with your datadog api key and app key. Use `datadog.sample.json` as a sample.
Bracecker will report response time and uptime to datadog as metrics (`bracecker.response_time.*` and `bracecker.uptime.*`). Keep in mind that it might take some minutes for the metrics to appear if it's the first time you're using bracecker with datadog.
Bracecker will also create custom checks on datadog (`bracecker.up.*`) that will automatically change if the service is up or down, so you can use them easily when creating monitors.

### announcement.txt
You can also create a file called `announcement.txt` in the same directory as bracecker and its message will be shown on the website as an announcement. Use it to alert your users about maintenance or technical issues. Bracecker will automatically reload announcement.txt's content every 60 seconds.

## CLI arguments
Bracecker supports some CLI arguments. Run `python3 main.py --help` to see the full list.

## Resetting
Bracecker doesn't reset response times and uptime automatically. If you want to reset your stats, close bracecker, remove `bracecker.db` and run bracecker again

## License
MIT
