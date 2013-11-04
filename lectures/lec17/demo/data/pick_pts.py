import csv
import random
import pdb
import json
import scipy.stats
import numpy as np

from itertools import *
from collections import *
from datetime import *


twohrs = timedelta(hours=2)
dt2str = lambda dt: dt.strftime('%Y-%m-%d %H:%M')
dt2key = lambda n: (n.weekday(), n.hour)
sign = lambda n: (n < 0) and -1 or 1
td2hours = lambda td: td.total_seconds() / (60*60)

def chain(*args):
  ret = []
  return map(ret.extend, args)

def partition(items, keyf, value=lambda d:d):
  ret = defaultdict(list)
  for item in items:
    ret[keyf(item)].append(value(item))
  return ret

def groupby(items, keyf, agg=lambda ds: ds):
  ret = {}
  for key, vals in partition(items, keyf, lambda pair: pair[1]).iteritems():
    ret[key] = agg(vals)
  return ret

def max_max(stats):
  maxes = [stat[2] for stat in stats]
  return max(maxes)

def quartile_max(stats):
  maxes = [stat[2] for stat in stats]
  return np.mean(maxes) + 1.2 * np.std(maxes)

def min_min(stats):
  mins = [stat[3] for stat in stats]
  return min(mins)

def quartile_min(stats):
  mins = [stat[3] for stat in stats]
  return np.mean(mins) - 1.2 * np.std(mins)

def zero(stats):
  means, stds, mosts, leasts = zip(*stats)
  return np.mean(means) ** 2

def std(stats):
  return np.mean([stat[1] for stat in stats])

def valid_loc(d):
  valids = ['TD Gar', 'South Stat', 'Fenway', 'Convention', 'Children', 'Logan', 'Hynes']
  for valid in valids:
    if valid in d[0]:
      return True
  return False

edate = datetime(2012, 5, 6)
all_diffs = json.load(file('./all_diffs.txt','r'))
all_diffs = filter(valid_loc, all_diffs)
table = []
for i,t in enumerate(all_diffs):
  # name, lat, lon, dt, avgcount, diff
  dt = datetime(*t[2])
  if dt > edate: continue
  d = map(str,[t[0], t[1][0], t[1][1], dt2str(dt), t[3], t[4]] )

  row = {
      'name': d[0],
      'lat': d[1],
      'lon': d[2],
      'time': d[3],
      'count': d[4],
      'diff': d[5]
  }
  table.append(row)

with file("./data.csv", "w") as f:
  w = csv.DictWriter(f, ['name', 'lat', 'lon', 'time', 'count', 'diff'])
  w.writeheader()
  w.writerows(table)

print "done!"
exit()

print json.dumps(table)
exit()



locs = list(set([(d[0], tuple(d[1])) for d in all_diffs]))

minday = min(all_diffs, key=lambda diff: diff[2])[2].date()
minday = datetime(minday.year, minday.month, minday.day)
maxday = max(all_diffs, key=lambda diff: diff[2])[2].date()
maxday = datetime(maxday.year, maxday.month, maxday.day)

def pick_normal_slots():
  normal_slots = []
  curday = minday
  oneday = timedelta(days=1)
  while curday <= maxday:
    if curday.weekday() >= 0 and curday.weekday() <= 4:
      for hour in [8, 5+12, 8+12]:
        normal_slots.append(curday + timedelta(hours=hour))
    else:
      normal_slots.append(curday + timedelta(hours=random.randint(12, 18)))

    curday = curday + oneday

  return normal_slots

def pick_random_slots(n=30):
  nhours = int((maxday - minday).total_seconds() / (60 * 60))
  for hour in random.sample(range(nhours), n):
    yield minday + timedelta(hours=hour)

def pick_zeros(day):
  xs = range(24)
  latlons = set([tuple(d[1]) for d in all_diffs])
  diffs = [d for d in all_diffs if d[2].date() == day]
  zeros = filter(lambda d: abs(d[-1]) < 3, diffs)
  return zeros

def pick_tops(day):
  diffs = [d for d in all_diffs if d[2].date() == day]
  vals = [d[-1] for d in diffs]
  thresh = np.mean(vals) + 1.5*np.std(vals)
  tops = filter(lambda d: d[-1] > thresh, diffs)
  return tops

def pick_lows(day):
  diffs = [d for d in all_diffs if d[2].date() == day]
  vals = [d[-1] for d in diffs]
  thresh = np.mean(vals) - 1.5*np.std(vals)
  return filter(lambda d: d[-1] < thresh, diffs)

def pick_extreme(metrics=[]):
  def foo(vals):
    return [np.mean(*vals), np.std(*vals), max(*vals), min(*vals) ]

  expectation = groupby(all_diffs, lambda d: dt2key(d[2]), lambda ds: np.mean([d[-1] for d in ds]))
  hour_stats = partition(all_diffs, lambda d: d[2], lambda d: d[-1] - expectation.get(dt2key(d[2]),0))
  hour_stats = groupby(
    hour_stats.items(), 
    lambda (dt, vals): dt,
    foo
  )
  day_stats = partition(
      hour_stats.items(),
      lambda (dt, vals): dt.date(),
      lambda (key, stats): stats
  )


  votes = Counter()
  for metric in metrics:
    result = sorted(day_stats.items(), key=lambda (day, stats): metric(stats), reverse=True)
    votes.update([day for day, stats in result[:10]])

  extremes = []
  for day, count in votes.most_common():
    extremes.extend(pick_zeros(day))
    extremes.extend(pick_tops(day))
    extremes.extend(pick_lows(day))
  return extremes




def plot_day(day, subplot):
  xs = range(24)
  latlons = set([tuple(d[1]) for d in all_diffs])
  diffs = [d for d in all_diffs if d[2].date() == day]
  by_loc = partition(diffs, lambda d: d[0])#, value=lambda d: [-1])

  for loc, pts in by_loc.iteritems():
    hr2diff = { pt[2].hour: pt[-1] for pt in pts }
    ys = map(lambda hr: hr2diff.get(hr, 0), xs)
    ppl.plot(subplot, xs, ys, c='grey', alpha=0.2)

  subplot.set_xlim(xmin=0, xmax=24)
  subplot.set_title(str(day))
  yield list(latlons)[0], 0
  
def plot_days(days):
  nplots = len(days)
  fig, subplots = plt.subplots(nplots, figsize=(10, 50))
  for i, day in enumerate(days):
    subplot = subplots[i]
    plot_day(day, subplot)
  plt.tight_layout()
  plt.savefig('./plots/best.png')




normal_slots = random.sample(pick_normal_slots(), 20)
random_slots = list(pick_random_slots(20))
slots = []
map(slots.extend, [normal_slots, random_slots])
final_slots = []
for slot in slots:
  for (name, latlon) in locs:
    final_slots.append(( latlon, name,dt2str(slot-twohrs),dt2str(slot+twohrs)  ))

extreme_slots = []
for metric in [max_max, quartile_max, min_min, quartile_min, zero, std]:
  diffs = pick_extreme([metric])
  random.shuffle(diffs)

  ret = []
  for extreme in diffs:
    dt = extreme[2]
    if len(ret) == 0:
      ret.append(extreme)
    elif abs(td2hours(dt-min(ret, key=lambda d: abs(td2hours(d[2]-dt)))[2])) > 4:
      ret.append(extreme)
    if len(ret) > 30:
      break
  
  extreme_slots.extend(ret)
  #print '\n'.join(map(lambda d: str((d[0], dt2str(d[2]))), sorted(ret)))
  #print

extreme_slots = random.sample(extreme_slots, 30)
for d in extreme_slots:
  final_slots.append((d[1],d[0],dt2str(d[2]-twohrs), dt2str(d[2]+twohrs)))

print json.dumps(final_slots)
exit()


  

# std on a per-week hour basis
dist = defaultdict(list)
for tup in all_diffs:
  key = dt2key(tup[2])
  dist[key].append((tup[-2], tup[-1]))

avgs_dist = {}
diffs_dist = {}
for key in sorted(dist.keys()):
  avgs, diffs = zip(*dist[key])
  avgs_dist[key] = (np.mean(avgs), np.std(avgs))
  diffs_dist[key] = (np.mean(diffs), np.std(diffs))




#xs, ys = zip(*sorted(avgs_dist.items()))
#xs = [w*24+h for w, h in xs]
#means, stds = zip(*ys)
#highs = [m+s for (m,s) in ys]
#lows = [m-s for (m,s) in ys]
#
#
#fig = plt.figure(figsize=(20, 8))
#subplot = fig.add_subplot(211)
#subplot.plot(xs, means, c='grey')
#subplot.plot(xs, highs, c='green')
#subplot.plot(xs, lows, c='red')
#
#xs, ys = zip(*sorted(diffs_dist.items()))
#xs = [w*24+h for w, h in xs]
#means, stds = zip(*ys)
#highs = [m+s for (m,s) in ys]
#lows = [m-s for (m,s) in ys]
#
#
#subplot = fig.add_subplot(212)
#subplot.plot(xs, means, c='grey')
#subplot.plot(xs, highs, c='green')
#subplot.plot(xs, lows, c='red')
#plt.savefig('./plots/stddevs.png')


# As a location
# high, med, low stderr(avgcounts, avgs_dist)

def print_metric(metric):
  all_loc_points = defaultdict(list)
  for tup in all_diffs:
    all_loc_points[tup[0]].append(tup)

  errs = []
  for loc, pts in all_loc_points.iteritems():
    errs.append((loc, metric(pts, avgs_dist), pts))

  errs.sort(key=lambda p: p[1])
  errs = errs[4:]
  for l, m, pts in errs:
    print m, '\t', l
  return errs

def sqerr(pts, avgs_dist):
  return np.mean([(avgs_dist[key][0]-pt[-2])**2  for pt in pts])**.5

def diff(pts, avgs_dist):
  return np.mean([(avgs_dist[key][0]-pt[-2])  for pt in pts])

def skew(pts, _):
  _, counts = zip(*sorted([(dt2key(pt[2]), pt[-2]) for pt in pts]))
  return scipy.stats.skew(counts)

def kurtosis(pts, _):
  _, counts = zip(*sorted([(dt2key(pt[2]), pt[-2]) for pt in pts]))
  return scipy.stats.kurtosis(counts)

# more than expected
def red(pts, _):
  return np.mean([abs(pt[-1]) for pt in pts])

# different than expected
def red2(pts, _):
  return np.mean([abs(pt[-1])**2 for pt in pts])**.5



def top_hours(pts):
  pts = sorted(pts, key=lambda pt: pt[-1], reverse=True)
  leasts = sorted(pts, key=lambda pt: abs(pt[-1]))
  ret = []
  for pt in pts[:5] + pts[-5:] + leasts[:5]:
    hr = pt[2]
    if len([x for (x, c) in ret if abs((x-hr).total_seconds()) < (60*60*4)]):
      pass
    else:
      ret.append((hr, pt[-1]))

  return [((hr-twohrs, hr+twohrs), c) for hr, c in ret]


top_locs = {}
for metric in [red, red2]:
  print metric
  sorted_locs = print_metric(metric)[4:]
  high_locs = sorted_locs[-10:]
  low_locs = sorted_locs[:10]

  for name, score, pts in chain(high_locs, low_locs):
    top_locs[name] = pts


days = Counter()
for name, pts in top_locs.iteritems():
  latlon = pts[0][1]
  print name, latlon
  for (shr, ehr), c in top_hours(pts):
    print '\t', dt2str(shr), '\t', c
    days[shr.date()] += 1

print len(days)
for day in sorted(days.keys()):
  print day, days[day]


print


# avg: (high, med, low)

# diff: (high, med, low)
