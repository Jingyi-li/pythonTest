def txt2csv(filename_tp):

    import numpy as np
    import matplotlib.pyplot as plt
    import csv
    filename = filename_tp+'.txt'
    rawData = np.loadtxt(filename, dtype=np.str)

    Lable = ['accx', 'accy', 'accz', 'grox', 'groy', 'groz', 'magx', 'magy', 'magz', 'count']
    tempDataDec = []
    # tempDataHex = []
    arrayDataDec = {}
    # arrayDataHex = {}

    #save the data to arrayData
    for i in range(len(Lable)):
        for j in range(len(rawData)):
            # low number
            temp = int(rawData[j][(i + 1) * 4 - 2:(i + 1) * 4], 16) * 256 + int(rawData[j][i * 4:i * 4 + 2], 16)
            # tempDataHex.append(rawData[j][(i) * 4:(i + 1) * 4])
            if temp > 32768:
                temp = temp-65536
                # continue
            tempDataDec.append(temp)

        arrayDataDec[Lable[i]] = tempDataDec
        # arrayDataHex[Lable[i]] = tempDataHex
        tempDataDec = []
        # tempDataHex = []

    with open(filename[0:len(filename)-4]+'.csv', 'w', newline='') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f,fieldnames = Lable)
        w.writeheader()
        tempDict={}

        for i in range(len(rawData)):
            for j in range(len(Lable)):
                tempDict[Lable[j]]=arrayDataDec[Lable[j]][i]
            w.writerow(tempDict)
            tempDict = {}
        f.close()

    return;


print('This is an exe convert the .txt file to .csv file\n ')
filename_tp = input('please type the file name:')

txt2csv(filename_tp)