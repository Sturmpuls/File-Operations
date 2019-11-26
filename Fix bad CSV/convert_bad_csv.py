import os
import sys
import glob
from pathlib import Path

def convert(csv_in, csv_out):
    with open(csv_in, 'rb') as bytestring, open(csv_out, 'wb') as out:
        for i, row in enumerate(bytestring, 1):
            row = row.replace(b'\x00', b'')
            if i != 2:
                print(f'{csv_in.name[:8]}...:', row)
                out.write(row)


version = sys.version_info
if not version.major >= 3 and version.minor >= 7:
    raise Exception("Please use Python 3.7 or newer!")

cwd = os.path.dirname(os.path.realpath(__file__))
suffix = '_fixed'
p = Path(cwd)
files = p.glob('*.csv')

for csv_in in files:
    if not csv_in.stem.endswith(suffix):
        print('=' * 70, f'>>> {csv_in.name}', sep='\r\n')
        csv_out = csv_in.parent / (csv_in.stem + suffix + csv_in.suffix)
        convert(csv_in, csv_out)