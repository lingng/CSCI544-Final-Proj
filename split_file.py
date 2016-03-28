fin = open("tmp.txt", 'r')

for i in range(0, 100):
    out = "o_"+str(i)+".txt"
    fout = open(out, 'w')
    count = 0
    while 1:
        if count >= 38100:
            break
        line = fin.readline()
        if not line:
            break
        count += 1
        fout.write(line)