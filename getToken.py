import re
with open("tokentest.txt") as f:
    s = f.readlines()
for line in s:
    if "access_token" in line:
        acc = re.sub('\"access_token\": \"',"",line)
        acc = re.sub('\",',"",acc)
        acc = re.sub(" *","",acc)
        acc = re.sub("\n","",acc)
        print (acc.replace("\n",""))

