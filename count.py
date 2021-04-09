import csv
import copy


def count():

    # count total numbers
    strtg = ["", "s", 0, 110, 120, 140, 210, 220]
    
    max = []
    score = []
    list = []
    list.append('all')
    for j in strtg:
        list.append(0)
    max.append(list)
    
    i = 16
    while i < 4100:
        list = []
        list.append(i)
        for j in strtg:
            list.append(0)
        max.append(list)
        i = i * 2
    score = copy.deepcopy(max)
    
    f1 = 'detail.csv'
    f2 = 'total.csv'
    with open(f1,'r') as f:
        result = csv.reader(f)
        for line in result:
            n = 0
            for m in line[:3]:
                n = n * 10 + int(m)
            i = 0
            while True:
                if max[i][0] == int(line[3]):
                    max[i][strtg.index(n)] += 1
                    max[0][strtg.index(n)] += 1
                    max[i][1] += 1
                    max[0][1] += 1
                    score[i][strtg.index(n)] += int(line[4])
                    score[0][strtg.index(n)] += int(line[4])
                    score[i][1] += int(line[4])
                    score[0][1] += int(line[4])
                    break
                i += 1
                
    
    with open(f2, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(strtg)
        i = 0
        while i < len(max):
            csv_writer.writerow(max[i])
            l1 = []
            l2 = []
            l1.append(str(max[i][0]) + '%up')
            l2.append('avg' + str(max[i][0]))
            j = 1
            while j < len(max[i]):
                if max[i][j] == 0:
                    l1.append(0)
                    l2.append(0)
                    j += 1
                    continue
                l1.append(max[i][j] / max[0][j])
                l2.append(score[i][j] / max[i][j])
                j += 1
            csv_writer.writerow(l1)
            csv_writer.writerow(l2)
            i += 1
        f.close()
        
        
count()
print("done")
