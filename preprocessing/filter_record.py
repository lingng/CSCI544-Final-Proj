# Filter Record

# Remove reviews without 3 rankings, and remove reviews without contents
# 4422474 records total
# 612543 records without 3 rankings & contents

# input: review.txt
# output: tmp.txt
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

# Filter Record

# Remove reviews without 3 rankings, and remove reviews without contents
# 4422474 records total
# 612543 records without 3 rankings & contents

# input: review.txt
# output: tmp.txt

urls = {}
fkeys = open('urls.txt')
while 1:
    line = fkeys.readline()
    if not line:
        break
    else:
        line = line.strip()
        urls[line] = 1
print urls

with open('o_0.txt') as fin:
    fout = open("filteered_0.txt", 'w')
    for line in fin:
        url = line.split(" ^ {")[0]
        if urls.has_key(url):
            fout.write(line)


