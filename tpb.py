# TODO: this takes > 6 seconds to parse the file and searching is slow - so we should really use postgresql

from magnet import Magnet

failures = []

def process_line(line):
    cols = line.split("|")

    try:
        tpb_id = int(cols[0])
        name = cols[1]
        size = int(cols[2])
        seeders = int(cols[3])
        leechers = int(cols[4])
        urn = cols[5]
        return Magnet(tpb_id, name, size, seeders, leechers, urn)
    except:
        failures.append(line)
        return None

def load_data():
    raw_data_file = "./db/tpb.txt"
    tpb_data = [ process_line(line) for line in open(raw_data_file, "r").readlines() ]
    print "%d failures" % (len(failures))
    return tpb_data


