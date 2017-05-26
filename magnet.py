magnet_format = "magnet:?xt=urn:btih:%s&dn=%s%s"

class Tracker(object):
    def __init__(self, method, url, port):
        self.method = method
        self.url = url
        self.port = port

    def __str__(self):
        return "&tr=%s%%3A%%2F%%2F%s%%3A%d" % (self.method, self.url, self.port)

trackers = [
    Tracker("udp", "trackers.leechers-paradise.org", 6969),
    Tracker("udp", "zer0day.ch", 6969),
    Tracker("udp", "open.demonii.com", 1337),
    Tracker("udp", "tracker.coppersurfer.tk", 6969),
    Tracker("udp", "exodus.desync.com", 6969)
]

class Magnet(object):
    def __init__(self, tpb_id, name, size, seeders, leechers, urn):
        self.tpb_id = tpb_id
        self.name = name
        self.size = size
        self.seeders = seeders
        self.leechers = leechers
        self.urn = urn.strip()
        self.link = self.generate_magnet_url()

    def generate_magnet_url(self):
        trackers_str = "".join([str(t) for t in trackers])
        magnet_url = magnet_format % (self.urn, self.name.replace(" ", "+"), trackers_str)

        return magnet_url