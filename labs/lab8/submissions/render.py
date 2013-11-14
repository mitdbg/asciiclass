import os

def render(url, outfile):
  cmd = './slimerjs rasterize.js %s %s' % (url, outfile)
  print cmd
  os.system(cmd)

with file('data.csv', 'r') as f:
  f.readline()
  for line in f:
    (name, url) = tuple(line.strip().split(','))
    fname = './imgs/%s.png' % '_'.join(name.split())
    render(url, fname)
