import random as r
userpip = input('Do you have pip or pip3?: ')
try:
  import pygame
  import pygame.locals as GUI_keys
except ModuleNotFoundError:
  __import__('os').system(userpip +  ' install pygame')
try:
  import pyfiglet
except ModuleNotFoundError:
  __import__('os').system(userpip + ' install pyfiglet')
try:
  from replit import db
except ModuleNotFoundError:
  __import__('os').system(userpip + ' install replit')
try:
  import requests
except ModuleNotFoundError:
  __import__('os').system(userpip + ' install requests')
import time
clock = time
try:
  import ShdwDB as DB
except ModuleNotFoundError:
  __import__('os').system(userpip + ' install ShdwDB')
#print('Type "view()" to view all the functions.')
zero = 0
one = 1
two = 2
three = 3
four = 4
five = 5
six = 6
seven = 7
eight = 8
nine = 9
nums = [zero, one, two, three, four, five, six, seven, eight, nine]
pygame.init()
def init_pygame(width, height, title):
  screen = pygame.display.set_mode((width, height))
  pygame.display.set_caption(title)
  return screen
GUI = pygame
GUI_events = pygame.event
GUI_out = GUI.draw
GUI_clock = GUI.time
def chattify(word):
  if len(word) >= 3:
    word = word.split()[0]
    if word == 'why' or word == 'you':
      word = word[-1]
    elif 'h' == word[0]:
      word = word.strip('h')
    elif 'ing' == word.strip(word[:-3]):
      word = word.strip(word[-1])
    else:
      vowels = ['a', 'e', 'i', 'o', 'u']
      word = list(word)
      for i in vowels:
        if i in word:
          word.remove(i)
      word = ''.join(word)
  return word

class sublist:
  def example():
    print('All of list2\'s elements will be removed from list1.')
def sublists(list1=[], list2=[]):
  for i in list1:
    for j in list2:
      if i == j:
        list1.remove(i)
  return sublist

def requester():
  """
  Do not use. This is only for Shdw.
  """
  r = requests.get("https://client.shivankchhaya.repl.co/requests", data={'update':'\x1b[0;32mUpdate Alert! Please go to the original repl for update.'})
  print(r.text)
  #u = requests.head('http://192.168.86.38/Users/deepchhaya1/Documents/flask_web_app/flaskr.py')
  #print(u.text)


def empty(what):
  if what == str:
    return ''
  elif what == int:
    return 0
  elif what == list:
    return []
  elif what == dict:
    return {}
  elif what == tuple:
    return ()
  elif what == bool:
    return False
  elif what == set:
    return set()
  elif what == 'function':
    def i():
      pass
    return i
  elif what == 'any':
    return None


class replitdb:
  """
  Use this for the repl.it database
  """
  def store(key, value):
    db[key] = value
  def get(key):
    return db[key]
  def delit(key):
    del db[key]
  def allkeys():
    return db.keys()
  def allvalues():
    return db.values()


#Make a color pattern. Use the ANSI escape codes for colors, and you have to use four colors.
def flashcol(text, col1, col2, col3, col4):
  lentxt = 0
  while lentxt < len(text):
    lentxt += 1
    if lentxt % 4 == 0:
      color = col1
    elif lentxt % 4 == 1:
      color = col2
    elif lentxt % 4 == 2:
      color = col3
    elif lentxt % 4 == 3:
      color = col4
    print(color + text[lentxt - 1], end='')
  print()
#Find how many lines in a file
def linesinfile(file):
    fillo = open(file)
    lenger = fillo.readlines()
    return len(lenger)
#Make a two-digit number
def twodigit(num1, num2):
    num3 = str(num1) + str(num2)
    return int(num3)
#Make a three-digit number
def threedigit(num1, num2, num3):
    num4 = str(num1) + str(num2) + str(num3)
    return int(num4)
#Make a four-digit number
def fourdigit(num1, num2, num3, num4):
    num5 = str(num1) + str(num2) + str(num3) + str(num4)
    return int(num5)
#Save some text in a file. Have mode='a' for appending text, mode='w' for overwriting the file, and mode='x' for creating a new file
def save_to_file(file, whattosave, mode):
  filo = open(file, mode)
  filo.write(whattosave)
#Delete files
def clearfiles(f1, f2=None, f3=None, f4=None, f5=None, f6=None):
  a = [f1]
  if f2 != None:
    a.append(f2)
  if f3 != None:
    a.append(f3)
  if f4 != None:
    a.append(f4)
  if f5 != None:
    a.append(f5)
  if f6 != None:
    a.append(f6)
  lena = len(a)
  while lena > 0:
    lena -= 1
    import os
    os.remove(a[lena])
#Some useless functions
class randoms:
  """
  The class where I put all my useless but usefull functions.
  """
  def series(st):
    a = st + 1
    b = a * 2
    c = b + 3
    d = c * 4
    e = d + 5
    f = e * 6
    g = f + 7
    h = g * 8
    i = h + 9
    j = i * 10
    return j
  def wrdnums(num):
      import random as r
      for n in range(1, num+1):
        print(r.randint(1, n), end=', ')
      print(num)
#Replace the first item in a list, replace all with mode='all'
def replace(list, element, put_in, mode='first'):
  if mode == 'first':
    eleinde = list.index(element)
    list.insert(eleinde, put_in)
    list.remove(element)
    return list
  elif mode == 'all':
    while element in list:
      eleinde = list.index(element)
      list.insert(eleinde, put_in)
      list.remove(element)
    return list
#Length of something
def length():
    ace = input("Type Something: ")
    print("The length of that is {0}.".format(len(ace)))
#Division
def div(num1, num2):
    bdf = num1/num2
    print("Your first number divided by your second is {0}. As a fraction it is {1}/{2}.".format(bdf, num1, num2))
#Multiplication
def mult(num1, num2):
    ceg = num1*num2
    print("Your first number multiplied by your second is {0}.".format(ceg))
#Addition
def add(num1, num2):
    dfh = num1+num2
    print("Your first number added to your second is {0}.".format(dfh))
#Subtraction
def sub(num1, num2):
    egi = num2-num1
    print("Your first number subtacted from your second is {0}.".format(egi))
#Modulus
def mod(num1, num2):
    hub = num1 % num2
    print('Your first number divided by your second\'s remainder is {0}.'.format(hub))
#Math function Chooser
def mathypleep():
    hjl = input('[1]Divide, [2]Multiply, [3]Add, [4]Subtract, [5]Exponent, [6]Modulus: ')
    num1 = float(input('First number: '))
    num2 = float(input('Second number: '))
    if int(hjl) == 1:
        div(num1, num2)
    if int(hjl) == 2:
        mult(num1, num2)
    if int(hjl) == 3:
        add(num1, num2)
    if int(hjl) == 4:
        sub(num1, num2)
    if int(hjl) == 5:
        exponent(num1, num2)
    if int(hjl) == 6:
        mod(num1, num2)
#Outputs to the console
def text(str):
    print(str)
#Asks a question
def question(str):
    fhj = input(str)
    print("You said, \"{0}\"".format(fhj))
#Exponent
def exponent(num1, num2):
    gik = num1**num2
    print("Your first number to the power of your second number is {0}.".format(gik))
#Smiley face
def imhappy():
    print("   |     |    ")
    print("   |     |    ")
    print("   |     |    ")
    print("   |     |    ")
    print("_            _")
    print(" _          _ ")
    print("  _        _  ")
    print("   _     _    ")
    print("    _   _     ")
    print("      _       ")
#Greeting
def hi():
    print('Hi! I hope you are having a really good day! If not, I hope this cheers you up.')
    imhappy()
#Clear terminal
def clear():
    import os
    os.system('clear')
#Ascii
def ascii(str, font='stantard', mode='print'):
    b = pyfiglet.Figlet(font=font)
    c = b.renderText(str)
    if mode == 'print':
      print(c)
    elif mode =='return':
      return c
#Function chooser
def pleep():
    print('[1]Length')
    print('[2]Text')
    print('[3]Question')
    print('[4]Imhappy')
    print('[5]Hi')
    print('[6]Math Pleep')
    print('[7]Clear The terminal')
    print('[8]Ascii')
    ree = int(input('Which one?: '))
    if ree == 1:
        length()
    if ree == 2:
        mee = input('What text?: ')
        text(mee)
    if ree == 3:
        AHH = input('What question?: ')
        question(AHH)
    if ree == 4:
        imhappy()
    if ree == 5:
        hi()
    if ree == 6:
        mathypleep()
    if ree == 7:
        clear()
    if ree == 8:
        hii = input('Text: ')
        ffont = input('Font?: ')
        ascii(hii, font=ffont)
#View functions
def view():
    print('These are not all the functions, but these include some of them.')
    print('1. Pleep(Type \"pleep()\")')
    print('2. Math Pleep(Type \"mathypleep()\")')

#Unicode, Hexadecimal, Octal, Binary
class funfuncs:
    """
    Fun functions.
    """
    def uniques(uni):
        print('Unicode: ' + chr(uni))
    def hexques(hexa):
        print('Hexadecimal: ' + hex(hexa).strip('0x'))
    def octques(octa):
        print('Octal: ' + oct(octa).strip('0o'))
    def binques(bina):
        print('Binary: ' + bin(bina).strip('0b'))
    def unirand(fromm, to):
        uni = r.randint(fromm, to)
        print('Random Unicode: ' + chr(uni))
    def hexrand(fromm, to):
        hexa = r.randint(fromm, to)
        print('Random Hexadecimal: ' + hex(hexa).strip('0x'))
    def octrand(fromm, to):
        octa = r.randint(fromm, to)
        print('Random Octal: ' + oct(octa.strip('0o')))
    def binrand(fromm, to):
        bina = r.randint(fromm, to)
        print('Random Binary: ' + bin(bina).strip('0b'))
__import__('os').system('clear')