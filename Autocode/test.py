from datetime import datetime

fmt = '%Y-%m-%d %H:%M:%S'
tstamp1 = datetime.strptime('2016-04-06 21:26:27', fmt)
tstamp2 = datetime.strptime('2016-04-07 09:06:02', fmt)

if tstamp1 > tstamp2:
    td = tstamp1 - tstamp2
else:
    td = tstamp2 - tstamp1
td_mins = int(round(td.total_seconds() / 60))

print('The difference is approx. %s minutes' % td_mins)