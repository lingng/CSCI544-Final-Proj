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

# 4422474 records total
# 346253 records without 3 rankings
# 612543 records without 3 rankings & contents
