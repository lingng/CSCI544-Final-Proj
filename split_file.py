count = 0
with open('reviews.txt') as fin:
    for line in fin:
        if "flavor\":-1" in line:
            print line
            count += 1
            continue
        if "environment\":-1" in line:
            print line
            count += 1
            continue
        if "service\":-1" in line:
            print line
            count += 1
            continue
        if "content\":\"\"" in line:
            print line
            count += 1
            continue
print count

# 4422474 records total
# 346253 records without 3 rankings
# 612543 records without 3 rankings & contents
