import IEXTools
from IEXTools import Parser

fname = "/c/Users/Victor Frazao/Dropbox/Personal/Python/Programs/IEX_Examples/IEX_data/20161212_IEXTP1_TOPS1.5.pcap"

p = Parser(fname, tops=True, tops_version=1.5)

i = 0
with p as lines:
    for line in lines:
        print(line)
        i += 1
