# TODO: this takes > 6 seconds to parse the file and searching is slow - so we should really use postgresql

from magnet import Magnet
from util import sizeof_fmt
failures = []


def matches_all(search_terms, magnet):
    all_good = True
    magnet_name = magnet.name.upper()

    for search_term in search_terms:
        all_good = all_good and search_term in magnet_name

    return all_good

class TPB(object):
    def __init__(self):
        self.tpb_data = []
        self.failures = []

        raw_data_file = "./db/tpb.txt"

        for line in open(raw_data_file, "r").readlines():
            self.process_line(line)

    def process_line(self, line):
        cols = line.split("|")

        try:
            tpb_id = int(cols[0])
            name = cols[1]
            size = sizeof_fmt(int(cols[2]))
            seeders = int(cols[3])
            leechers = int(cols[4])
            urn = cols[5]

            self.tpb_data.append(Magnet(tpb_id, name, size, seeders, leechers, urn))
        except:
            self.failures.append(line)

    def search(self, search_terms):
        raw_results = [ m for m in self.tpb_data if matches_all(search_terms, m) ]
        return [d.__dict__ for d in sorted(raw_results, key=lambda x: -(x.seeders))]