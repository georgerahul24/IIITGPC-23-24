import re
import shutil
import subprocess
import os
import csv

zeroErrorFolder = "ZeroErrors"


def getErrorsAndWarnings(foldername):
    data = dict()

    i = 1
    for file in os.listdir(foldername):
        if file.endswith(".c"):
            output = subprocess.run(["gcc", os.path.join(foldername, file)], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            outputString = str(output.stderr)

            rollNumber = int(re.findall("(\\d{7}).*[Qq].*", file)[0])
            questionNumber = int(re.findall("\\d{7}.*[Qq](\\d).*", file)[0])

            errors = re.findall("([0-9]+) error", outputString)
            warnings = re.findall("([0-9]+) warning", outputString)

            numberOfErrors = 0 if len(errors) == 0 else int(errors[0])
            numberOfWarnings = 0 if len(warnings) == 0 else int(warnings[0])

            print(f"Sl. No: {i} | Filename: {file} | Roll Number: {rollNumber} | Q No: {questionNumber}")
            print("Errors: ", numberOfErrors)
            print("Warnings: ", numberOfWarnings)
            try:
                qdata = data[rollNumber]
                qdata[questionNumber - 1][0] = numberOfWarnings
                qdata[questionNumber - 1][1] = numberOfErrors
                data[rollNumber] = qdata
            except KeyError:
                qdata = [[1000, 1000], [1000, 1000], [1000, 1000], [1000, 1000], [1000, 1000]]
                qdata[questionNumber - 1][0] = numberOfWarnings
                qdata[questionNumber - 1][1] = numberOfErrors
                data[rollNumber] = qdata
            finally:
                if (numberOfErrors == 0):
                    shutil.copy(os.path.join(foldername, file), zeroErrorFolder)

            i += 1

    fields = ['Roll Number', 'Q1W', 'Q1E', 'Q2W', 'Q2E', 'Q3W', 'Q3E', 'Q4W', 'Q4E', 'Q5W', 'Q5E']
    with open("NumberOfErrorsAndWarnings.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

        for key, value in data.items():
            rowData = [key, ]
            for rows in data[key]:
                rowData.extend(rows)
            writer.writerow(rowData)
