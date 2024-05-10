import csv
import os.path
import re

data = dict()


def combineResults(resultDirectory):
    for file in os.listdir(resultDirectory):
        if file.endswith(".csv"):
            questionNumber = int(re.findall("Q(\\d)_Tes.*", file)[0])
            with open(os.path.join(resultDirectory, file)) as f:
                reader = csv.reader(f)
                header = next(reader)  # to skip the header
                for line in reader:
                    rollNumber = line[0]
                    passed = line[1]
                    total = line[2]
                    try:
                        qdata = data[rollNumber]
                        qdata[questionNumber - 1][0] = passed
                        qdata[questionNumber - 1][1] = total
                        data[rollNumber] = qdata
                    except KeyError:
                        qdata = [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1]]
                        qdata[questionNumber - 1][0] = passed
                        qdata[questionNumber - 1][1] = total
                        data[rollNumber] = qdata
    fields = ['Roll Number', 'Q1P', 'Q1T', 'Q2P', 'Q2T', 'Q3P', 'Q3T', 'Q4P', 'Q4T', 'Q5P', 'Q5T']
    with open("FinalResult.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

        for key, value in data.items():
            rowData = [key, ]
            for rows in data[key]:
                rowData.extend(rows)
            writer.writerow(rowData)
