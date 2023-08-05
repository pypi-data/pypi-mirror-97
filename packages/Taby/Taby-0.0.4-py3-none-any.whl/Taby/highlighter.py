def highlighter(color, text):
      if color == 'yellow':
        return "\033[1;43m" + text + "\033[1;m"