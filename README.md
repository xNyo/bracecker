## Bracecker
### Avoid setting your server on fire like a brace with bracecker!
Bracecker is a python script that checks the status of your services every 60 seconds. It uses a sqlite database to store statuses and response times, so you don't have to set up a MySQL server to use bracecker. Bracecker has also an integrated tornado server that shows a fancy page with the status of your services, uptimes and a response time graph.

## Requirements
- Python 3.5
- Tornado
- Jinja2

## Installing
```
$ git clone ...
$ cd bracecker
$ sudo pip install tornado jinja2
$ cp services.sample.json services.json
$ nano services.json
...
$ python3 main.py
```

## Configuring
Bracecker will look for the services to check inside the `services.json` file. It's super easy to config, use `services.sample.json` as a sample. You can also create a file called `announcement.txt` in the same directory as bracecker and its message will be shown on the website as an announcement. Use it to alert your users about maintenance or technical issues. Remember to restart bracecker whenever you edit `services.json` or `announcement.txt`

## License
MIT
