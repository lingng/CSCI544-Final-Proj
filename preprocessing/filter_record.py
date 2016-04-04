# Filter Record

# Remove reviews without 3 rankings, and remove reviews without contents
# 4422474 records total
# 612543 records without 3 rankings & contents

# input: review.txt
# output: tmp.txt

with open('reviews.txt') as fin:
    fout = open("tmp.txt", 'w')
    for line in fin:
        if "flavor\":-1" in line:
            continue
        if "environment\":-1" in line:
            continue
        if "service\":-1" in line:
            continue
        if "content\":\"\"" in line:
            continue
        fout.write(line)


