from flask import Flask, send_file
from flask import request
from gevent.pywsgi import WSGIServer
from video import create_video
from tinydb import TinyDB, where
from utils import ipInfo
import shortuuid
import yaml
config = yaml.safe_load(open("config.yml"))

app = Flask(__name__)
db = TinyDB("db.json")


@app.route("/")
def index():
    client_ip = request.remote_addr

    query = db.search(where("query") == client_ip)
    if query:
        return send_file(f"storage/{query[0]['id']}.mp4")

    id = shortuuid.uuid()

    data = ipInfo(client_ip)
    data["id"] = id

    create_video(data)

    db.insert(data)

    return send_file(f"storage/{id}.mp4")


if __name__ == "__main__":
    print(f"⚡️[server]: Server is running at http://{config['host']}:{config['port']}")
    http_server = WSGIServer((config['host'], config['port']), app)
    http_server.serve_forever()
