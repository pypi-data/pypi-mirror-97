def reader(infile, outfile,highlighter):
  with open(infile) as fin, open(outfile, 'w') as fout:
    for line in fin:
        fout.write(line.replace('  ', highlighter))