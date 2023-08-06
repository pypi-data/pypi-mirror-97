import time, sys
def sp(text):
  for char in text:
    print(char, end = "")
    time.sleep(0.05)
    sys.stdout.flush()
def hello():
  print("Hello")
