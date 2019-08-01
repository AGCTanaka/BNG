import re
import sys

arg = sys.argv[1]
sub_strings = 'token = "' + arg + '"'
with open("hello.py") as f:
    s = f.read()

s = re.sub("token = .*",sub_strings,s)
print(s)
'''
with open("hello.py","w",encoding="UTF-8") as f:
    f.write(s)
'''
