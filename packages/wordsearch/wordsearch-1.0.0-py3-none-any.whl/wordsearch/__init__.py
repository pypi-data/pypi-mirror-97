from requests import get as __get

__version__ = '1.0.0'

WORDS = __get('https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt')
WORDS = WORDS.text.splitlines()

def has(string):
  l = []

  for word in WORDS:
    if string in word:
      l.append(word)

  return l

def has_patterns(patterns):
  l = []

  for word in WORDS:
    yes = True
    done = []

    for pattern in patterns:
      if pattern in done:
        continue

      if not pattern in word:
        yes = False
      
      done.append(pattern)

    if yes:
      l.append(word)

  return l

def length(length):
  l = []

  for word in WORDS:
    if len(word) - 1 == length:
      l.append(word)

  return l

def starts_with(string):
  l = []

  for word in WORDS:
    if word.startswith(string):
      l.append(word)

  return l

def ends_with(string):
  l = []

  for word in WORDS:
    if word.endswith(string):
      l.append(word)

  return l

def in_middle(string):
  l = []

  for word in WORDS:
    if not word.startswith(string) and not word.endswith(string) and string in word:
      l.append(word)

  return l

def in_specific(string, start):
  l = []

  for word in WORDS:
    try:
      if word[start:start + len(string)] == string:
        l.append(word)
    except NameError:
      continue

  return l

def is_palindrome():
  l = []

  for word in WORDS:
    if word == word[::-1]:
      l.append(word)

  return l

def is_word(string):
  if string in WORDS:
    return True
  else:
    return False

def starts_and_ends_with(string):
  l = []

  for word in WORDS:
    if word.startswith(string) and word.endswith(string):
      l.append(word)

  return l
