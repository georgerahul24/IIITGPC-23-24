import os.path
import shutil
import threading

import BlindCodingEvaluationNumberofErrors
import RunTestCases
import CombineResults

codeFolder = "./Code"
testCasesFolder = "./TestCases"
resultFolder = RunTestCases.resultDirectory
zeroErrorsFolder = BlindCodingEvaluationNumberofErrors.zeroErrorFolder

for file in os.listdir(testCasesFolder):
    if file.endswith(".txt"):
        RunTestCases.RunTestCases(os.path.join(testCasesFolder, file), "./ZeroErrors")


