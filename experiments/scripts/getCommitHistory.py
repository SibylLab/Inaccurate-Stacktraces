import git
import os
g = git.Git("C:/Users/meher/spring-framework/")

#print(loginfo)

stacktrace_files = "D:/IS/infozilla-master/infozilla-master/demo/Spring/results/"


import csv
count = 0
with open('springFramework_commitHistory.csv', mode='w',newline='') as csv_file:
    fieldnames = ['Bug ID', 'Commit Files']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for filename in os.listdir(stacktrace_files):
        if filename.endswith(".xml"):
            try:
                bugID = filename[:filename.find('.')].strip()
                grep_cmd = "--grep=\<"+str(bugID)+"\>"
                commitFiles = g.log('--graph','--pretty=oneline','--name-only',grep_cmd)
                if commitFiles:
                    writer.writerow({'Bug ID': bugID, 'Commit Files': commitFiles})
            except:
                print("Something went wrong with filename: ",bugID)
