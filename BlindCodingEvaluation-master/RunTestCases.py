import csv
import os
import re
import subprocess

resultDirectory = "ResultsForTestCase"
try:
    os.makedirs(resultDirectory)
except FileExistsError:
    pass


def RunTestCases(testcasefile, codeDirectory):
    data = dict()
    questionNumberForTheTestCase = int(re.findall("[Qq](.)_Tes.*", testcasefile)[0])

    for file in os.listdir(codeDirectory):
       if(file.endswith(".c")):
            print("Procesing File"+file)
            rollNumber = int(re.findall("(\\d{7}).*[qQ].*", file)[0])
            questionNumber = int(re.findall("\\d{7}.*[qQ](\\d).*", file)[0])

            if questionNumber == questionNumberForTheTestCase:
                numberOfTestCasesPassed = 0
                totalTestCases = 0
                with open(testcasefile) as f:
                    for line in f:
                        inputToPass, expectedOutput = line.split("||")
                        subprocess.Popen(["gcc", os.path.join(codeDirectory, file)],
                                         stderr=subprocess.PIPE).communicate()  # To reset the stdout
                        subprocess.Popen(["chmod", "+x", "a.out"])
                        p = subprocess.Popen("./a.out", stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                        stdout = p.communicate(input=bytes(inputToPass, 'utf-8'))[0]
                        stdout = stdout.decode()

                        print(f"Expected Output: {expectedOutput} | Output: {stdout}")
                        if len(re.findall(expectedOutput.strip(), stdout.strip())):
                            numberOfTestCasesPassed += 1
                        totalTestCases += 1



                    print(
                        f"Filename: {file} | TestCases Passed: {numberOfTestCasesPassed}/{totalTestCases} | Roll Number: {rollNumber}")

                    data[rollNumber] = [numberOfTestCasesPassed, totalTestCases]

    fields = ["Roll Number", "Passed", "Total"]
    with open(os.path.join(resultDirectory, f"Q{questionNumberForTheTestCase}_TestCaseResult.csv"), 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(fields)

        for key in data.keys():
            row = [key, ]
            row.extend(data[key])
            csv_writer.writerow(row)
