import codecs
import csv
import datetime
import os
import sys
from pathlib import Path

def convert(csv_in, csv_out):
    with codecs.open(csv_in, 'r', encoding='utf_16_le', errors='ignore') as f, open(csv_out, 'w', newline='') as out:
        r = csv.reader(f)
        c = csv.writer(out)
        
        # write first two lines and fix problematic line 2
        for i in range(2):
            row = next(r)
            try:
                row = row[0].split('\u0a0d')
                c.writerow([row[0]])
                c.writerow([row[1]])
            except:
                c.writerow(row)			
		# c.writerow(next(r))
        # c.writerow([next(r)[0].replace('\u0a0d', '')])
        
        for line in r:
            c.writerow(line)


version = sys.version_info
if not version.major >= 3 and version.minor >= 7:
    raise Exception("Please use Python 3.7 or newer!")

cwd = os.path.dirname(os.path.realpath(__file__))
suffix = '_fixed'
p = Path(cwd)
files = p.glob('**/*.csv')

for csv_in in files:
    if not csv_in.stem.endswith(suffix):
        #print('=' * 70)
        print(f'>>> {datetime.datetime.now().time()}: {csv_in.name} ---> {csv_in.stem + suffix + csv_in.suffix}')#, sep='\r\n')
        csv_out = csv_in.parent / (csv_in.stem + suffix + csv_in.suffix)
        convert(csv_in, csv_out)