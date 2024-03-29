import os
from flask import Flask, send_file, request, render_template, jsonify
from tpb import TPB
from torrent import start_torrenting, incoming_dir

app = Flask(__name__)

tpb_db = TPB()

@app.route('/')
def hello_world():
    return send_file("templates/index.html")

@app.route('/search', methods=['POST','GET'])
def search():
    content = request.get_json()
    search_terms = str(content["search_term"]).upper().split(" ")
    results = tpb_db.search(search_terms)
    return jsonify({ "results": results })#, 200

@app.route('/download', methods=['POST'])
def download():
    content = request.get_json()
    url = str(content["url"])
    urn = str(content["urn"])

    magnet_file = open(incoming_dir + "/" + urn + ".magnet", "w")
    magnet_file.write(url)
    magnet_file.close()

if __name__ == '__main__':
    torrent_pid = os.fork()
    if torrent_pid == 0:
        start_torrenting()
    else:
        app.run(host="0.0.0.0")