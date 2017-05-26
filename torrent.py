#!/usr/bin/python

import libtorrent as lt
import time
import os
import shutil

incoming_dir = "./incoming_torrents"
completed_dir = "./completed_torrents"
files_dir = "./files"
poll_interval_seconds = 2

def ensure_dir(dir_path):
    if os.path.exists(dir_path):
        if not os.path.isdir(dir_path):
            raise Exception("file %s exists but is not a directory" % (dir_path))
    else:
        os.mkdir(dir_path)

def grab_magnet(filename):
    ses = lt.session()
    ses.listen_on(6881, 6891)
    magnet_url = open(filename, 'rb').read().strip()
    params = {
        'save_path': files_dir,
        'storage_mode': lt.storage_mode_t.storage_mode_sparse,
    }

    h = lt.add_magnet_uri(ses, magnet_url, params)
    ses.start_dht()
    s = h.status()

    while (not s.is_seeding):
        s = h.status()
        print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %s) %s' % (
        s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)
        time.sleep(1)

# needs a refactor, it's a nasty copy-paste from the README
def grab_torrent(filename):
    ses = lt.session()
    ses.listen_on(6881, 6891)

    e = lt.bdecode(open(filename, 'rb').read())
    info = lt.torrent_info(e)

    params = {
        'save_path': files_dir, 
        'storage_mode': lt.storage_mode_t.storage_mode_sparse,
        'ti': info
    }

    h = ses.add_torrent(params)
    s = h.status()

    print "%s:" % (filename)
    
    while (not s.is_seeding):
        s = h.status()
        print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %s) %s' % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)
        time.sleep(1)

def start_torrenting():
    ensure_dir(incoming_dir)
    ensure_dir(completed_dir)

    while True:
        files = os.listdir(incoming_dir)

        for incoming_file in files:
            full_path = incoming_dir + "/" + incoming_file
            filename, file_extension = os.path.splitext(incoming_file)
            if file_extension == "torrent":
                grab_torrent(full_path)
            else:
                grab_magnet(full_path)
            shutil.move(full_path, completed_dir + "/" + incoming_file)

        time.sleep(poll_interval_seconds)