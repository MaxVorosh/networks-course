import datetime
from email.utils import format_datetime
import requests
from flask import Flask, request
from http import HTTPStatus
from Cache import Cache

app = Flask(__name__)


def reroute(request, subpath):
    if request.method == 'GET':
        return requests.get(subpath)
    return requests.post(subpath, json=request.json)


def check_blocked(path):
    global bad_adresses
    if path in bad_adresses:
        return True
    for item in bad_adresses:
        if item[0] == '.':
            if item in path:
                return True
    return False


@app.route("/<path:subpath>", methods=['GET', 'POST'])
def handle_adress(subpath):
    global cache
    try:
        if request.referrer:
            subpath = '/'.join(request.referrer.split('/')[3:]) + '/' + subpath
        subpath = "http://" + subpath
        if check_blocked(subpath):
            return "Blocked", HTTPStatus.FORBIDDEN
        if cache.check(subpath):
            time = cache.lastModified(subpath)
            headers = {'If-Modified-Since': format_datetime(time)}
            resp = requests.get(subpath, headers=headers)
            if resp.status_code == HTTPStatus.NOT_MODIFIED:
                return cache.read(subpath), HTTPStatus.ACCEPTED
        resp = reroute(request, subpath)
        time = datetime.datetime.now()
        cache.write(subpath, time, resp.content)
        status = resp.status_code
        with open("journal.txt", "a") as f:
            f.write(f'{subpath} {status}\n')
        return resp.content, status
    except Exception as err:
        return str(err), HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == "__main__":
    open('journal.txt', 'w').close()
    f = open('server/config.txt')
    bad_adresses = list(map(lambda s: s.strip(), f.readlines()))
    f.close()
    cache = Cache()
    app.run(host="127.0.0.1", port=5000)