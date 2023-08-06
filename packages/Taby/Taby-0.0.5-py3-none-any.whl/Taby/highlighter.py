def highlighter(color, text):
      if color == 'yellow':
        return "\033[1;43m" + text + "\033[1;m"
      if color == "red":
        return "\033[1;41m" + text + "\033[1;m"
      if color == "green":
        return "\033[1;42m" + text + "\033[1;m"
      if color == "blue":
        return "\033[1;44m" + text + "\033[1;m"