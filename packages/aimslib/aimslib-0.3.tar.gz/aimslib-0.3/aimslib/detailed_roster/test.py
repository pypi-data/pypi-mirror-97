#!/usr/bin/python3

import datetime as dt
import aimslib.detailed_roster.process as dr
from aimslib.detailed_roster.process import DStr, Break, SectorFormatException

#filename = "/home/intranet/rosters/roster-201908.htm"
filename = "/home/jon/tmp/DW401_1333717754.htm"
s = open(filename).read()
l = dr.lines(s)
c = dr.columns(l)
bstream = dr.basic_stream(dr.extract_date(l), c)


dstream = bstream[:]

#Remove single DStr surrounded by Breaks
for c in range(1, len(dstream) - 1):
    if (isinstance(dstream[c], DStr) and
        isinstance(dstream[c - 1], Break) and
        isinstance(dstream[c + 1], Break)):
        dstream[c] = None
        dstream[c - 1] = None
dstream = [X for X in dstream if X]

#if a dt.datetime follows a column break, remove the break
for c in range(1, len(dstream) - 1):
    if dstream[c] == Break.COLUMN and isinstance(dstream[c + 1], dt.datetime):
        dstream[c] = None
dstream = [X for X in dstream if X]

#clean up sector blocks, including column break removal
in_sector = False
for c in range(1, len(dstream) - 1):
    if in_sector:
        if (isinstance(dstream[c], DStr) and
            isinstance(dstream[c + 1], dt.datetime)): #"from" found
            in_sector = False
            #remove any DStr up to next Break object
            i = c + 2
            while not isinstance(dstream[i], Break):
                if isinstance(dstream[i], DStr):
                    dstream[i] = None
                i += 1
        else:
            dstream[c] = None #remove column breaks and extra DStrs
    else: #not in sector
        if isinstance(dstream[c], DStr):
            if isinstance(dstream[c - 1], dt.datetime): #"to" found
                in_sector = True
            elif isinstance(dstream[c - 1], DStr):
                dstream[c - 1] = None #remove extra DStrs at start of block
dstream = [X for X in dstream if X]

#remaining Break objects are either duty breaks if separated by more
#than 8 hours, else they are sector breaks
for c in range(1, len(dstream) - 2):
    if dstream[c] in (Break.LINE, Break.COLUMN):
        if (not isinstance(dstream[c - 1], dt.datetime) or
            not isinstance(dstream[c + 2], dt.datetime)):
            raise SectorFormatException
        tdiff = (dstream[c + 2] - dstream[c - 1]).total_seconds()
        if tdiff >= 8 * 3600:
            dstream[c] = Break.DUTY
        else:
            dstream[c] = Break.SECTOR
for e in dstream[1:-1]:
    print(e)
