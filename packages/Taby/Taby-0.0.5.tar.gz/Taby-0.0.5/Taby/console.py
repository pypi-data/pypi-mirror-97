def console(outfile,highlighter):
  with open(outfile, 'r') as fin: 
    for line in fin:
        print(line)
        for word in line.split():
          if 'TAB' in word: 
          
            highlighter
            