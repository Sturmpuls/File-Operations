#! for Python 3.7 or higher!

import codecs
import csv
import datetime
import os
from pathlib import Path


def fix_byte(csv_in):
    ''' Jedes Zeichen belegt 2 Bytes. Um das fehlerhafte Zeichen (\u0a0d)
    mit einem Zeilenumbruch (\r\n) ersetzen zu können, brauchen wir 4 Bytes.
    Die Zeilen sehen so aus: "...;Temperature\u0a0d0d 00:00:21..."
    Es gibt also kein Leerzeichen. Um zwei Bytes zu verändern können wir das
    "e" von "Temperature" mit dazunehmen. Die Spaltenbezeichnung bleibt damit
    noch verständlich ("Temperature" -> "Temperatur"). Das "0" Byte direkt hinter dem fehlerhaften Zeichen
    wollen wir auf jeden Fall nicht überschreiben.
    '''
    
    with codecs.open(csv_in, 'r+', encoding='utf_16_le') as f:
    
        while True:
            char = f.read(1)
            pos = f.tell()
            fixed = False
            
            if char == '\u0a0d':
                pos -= 4
                f.seek(pos)
                if f.read(1) == 'e': # reads 1 character but consumes 2 Bytes
                    f.seek(pos)
                    f.write('\r\n') # writes 2 characters on 4 Bytes
                    fixed = True
                else:
                    f.seek(pos-20)
                    string = f.read(20)
                    print(f'Character "\u0a0d" in unexpected position:\r\n...{string}...')
                break
                
            if pos > 2000:
                break

        return fixed
        

cwd = os.path.dirname(os.path.realpath(__file__))
p = Path(cwd)
files = p.glob('**/*.csv')

for csv_in in files:
    f = str(csv_in)
    fixed = fix_byte(f)
    if fixed:
        new_name = csv_in.parent / (csv_in.stem + '_fixed' + csv_in.suffix)
        csv_in.replace(new_name)
    print(f'>>> Fixed: {fixed} | {datetime.datetime.now().time()}: {csv_in.name}')