import os
import re
import json
import pandas as pd
import time
import xml.etree.ElementTree as ET
from urllib.request import urlopen
import csv

SLEEP_TIMELIMIT = 3 #TIME IN SECONDS
FILES_LIMIT = 3000
PROJECTS = ['AspectJ','Birt','Eclipse_Platform_UI','JDT','SWT','Tomcat']
EXCELSHEET_FILENAME = "D:/IS/dataset/dataset/Eclipse_Platform_UI.xlsx"
INFOZILLA_PATH = "D:/IS/infozilla-master/infozilla-master"
JSONSTORE_FILEPATH = INFOZILLA_PATH + "/demo/Hbase/"
RESULTS_PATH = JSONSTORE_FILEPATH + "results/"
FILENAMES_PATH = JSONSTORE_FILEPATH + "st_filenames/"
GRADLE_CMD = "gradle run --args='demo/Haddop/"
HELPFUL_TAG = "Helpful"
MISLEADING_TAG = "Misleading"
CH_CSV_FILE =  "D:/IS/stracktraces/CommitHistory/hbase_commitHistory.csv"
ST_FN_CSV_FILE = "D:/IS/stracktraces/hbase_st_full.csv"
ST_FILENAMES_COUNT = 200
st_filenames,complete_list = [],[]

commitHistory_details = pd.read_csv(CH_CSV_FILE,encoding='unicode_escape')
stracktraces_details = pd.read_csv(ST_FN_CSV_FILE,encoding='unicode_escape')
commiyhistory_bugids = []
for bug in commitHistory_details['Bug ID'].unique():
    commiyhistory_bugids.append(str(bug).strip())
print("length :",commiyhistory_bugids)

def getBRJsonRpc():
    count=0
    df = pd.read_excel(EXCELSHEET_FILENAME)
    print("Getting JSON Response from Bugzilla Rest Services \n")
    for bugid in df['bug_id']:
        path = JSONSTORE_FILEPATH+str(bugid)+".json"
        file = open(path,"w+")
        url = "https://bugs.eclipse.org/bugs/rest/bug/"+str(bugid)+"/comment"
        response = urlopen(url)
        data_json = json.loads(response.read())
        try:
            for element in data_json['bugs'][str(bugid)]['comments']:
                element.pop('text', None)
            file.write(str(data_json).replace('\\n','\n').replace('\\t','\t'))
        except:
            print("Something went wrong with id:",bugid)
        file.close()
        count+=1
        if count == FILES_LIMIT:
            break
        time.sleep(SLEEP_TIMELIMIT)

def executeInfozilla():
    print("Executing Infozilla on Bug reports \n")
    os.chdir(INFOZILLA_PATH)
    file_count=0
    for filename in os.listdir(JSONSTORE_FILEPATH):
        if filename.endswith(".txt"):
            try:
                file_count+=1
                command = GRADLE_CMD+filename+"'"
                print("Current File Count: ",file_count)
                print(command)
                os.system(command)
            except BaseException as error:
                #print("Something went wrong with filename: ",filename)
                print('An exception occurred: {}'.format(error))

def extractFileNames():
    print("Extracting Filenames from Strack Traces \n")
    for filename in os.listdir(RESULTS_PATH):
        if filename.endswith(".xml"):
            try:
                bugID = filename[:filename.find('.')]
                tree = ET.parse(RESULTS_PATH+filename)
                root = tree.getroot()
                commitHistory = []
                filesList =[]
                st_filenames = []
                misleading_flag = True
                for child in root:
                    for subchild in child.iter('Frame'):
                        frame = subchild.text
                        filesList.append(frame[frame.find('(')+1:frame.find(':')])
            except:
                print("Something went wrong with filename: ",filename)
            for file in filesList:
                if file not in st_filenames:
                    st_filenames.append(file)
            commitHistory = getCommitHistory(bugID)
            if commitHistory:
                for commitfile in commitHistory:
                    if commitfile in st_filenames[:min(len(st_filenames),ST_FILENAMES_COUNT)]:
                        misleading_flag = False
                        path = FILENAMES_PATH + "/"+ HELPFUL_TAG + "/"+str(bugID)+".txt"
                        file = open(path,"w+")
                        for st_file in st_filenames[:min(len(st_filenames),ST_FILENAMES_COUNT)]:
                            file.write(st_file+","+HELPFUL_TAG+"\n")
                if misleading_flag:
                    path = FILENAMES_PATH +"/"+ MISLEADING_TAG +  "/"+ str(bugID)+".txt"
                    file = open(path,"w+")
                    for st_file in st_filenames[:min(len(st_filenames),ST_FILENAMES_COUNT)]:
                        file.write(st_file+","+MISLEADING_TAG+"\n")

def extractFeatures():
    print("Extracting Filenames,Method names, Exception from Strack Traces \n")
    with open('hbase_st_full.csv', mode='w',newline='') as csv_file:
        header = ['Project','BugID', 'Filename','Method name', 'Path', 'Exception','Label']
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        for filename in os.listdir(RESULTS_PATH):
            if filename.endswith(".xml"):
                try:
                    bugID = filename[:filename.find('.')]
                    if bugID.strip() in commiyhistory_bugids:
                        tree = ET.parse(RESULTS_PATH+filename)
                        root = tree.getroot()
                        commitHistory,filesList,st_filenames = [],[],[]
                        misleading_flag = True
                        file_name,method_name,path,exception='','','',''
                        for child in root:
                            for subchild in child.iter('Exception'):
                                exception = subchild.text
                                if exception:
                                    exception = exception[exception.rindex('.')+1:] if '.' in exception else exception
                            for subchild in child.iter('Frame'):
                                frame = subchild.text
                                file_name = frame[frame.find('(')+1:frame.find(':')]
                                filesList.append(file_name)
                                features = frame[:frame.find('(')]
                                method_name = features[features.rindex('.')+1:]
                                path = features[:features.rindex('.')]
                                if removingDuplicates(file_name,method_name,bugID):
                                    writer.writerow({'Project': "Hbase", 'BugID':bugID,'Filename':file_name,'Method name': method_name,'Path':path,'Exception':exception})
                except BaseException as error:
                    print("Something went wrong with filename: ",filename,exception,error)


def removingDuplicates(fn,mn,bi):
    if fn+mn+bi not in complete_list:
        complete_list.append(fn+mn+bi)
        return True
    else:
        return False

def getCommitHistory(bugID):
    df = pd.read_excel(EXCELSHEET_FILENAME)
    pattern = r"(\w+\.java){1}"
    for file in df[df["bug_id"]== int(bugID)]['files']:
        return re.findall(pattern,file)

def getCommitFiles(bugID):
    pattern = r"(\w+\.java){1}"
    for file in commitHistory_details[commitHistory_details["Bug ID"] == (bugID)]['Commit Files']:
        return re.findall(pattern,file)

def detectLabels():
    helpfulBugIds = []
    for bugid in commitHistory_details['Bug ID']:
        unique_files = []
        ch_files = getCommitFiles(bugid)
        st_filenames = stracktraces_details[stracktraces_details["BugID"] == bugid]["Filename"]
        for file in st_filenames:
            if file not in unique_files:
                unique_files.append(file)
        for commitfile in ch_files:
            if commitfile in unique_files[:min(len(unique_files),ST_FILENAMES_COUNT)]:
                helpfulBugIds.append(bugid)
    print(len(helpfulBugIds))
    stracktraces_details["Label"] =  stracktraces_details.BugID.map(lambda p : HELPFUL_TAG if p in helpfulBugIds else MISLEADING_TAG)
    stracktraces_details.to_csv("hbase_top_all.csv", index=False)


def main():
    print("STRACK TRACES EXTRACTION!!!")
    #getBRJsonRpc()
    #executeInfozilla()
    #extractFileNames()
    #extractFeatures()
    detectLabels()

#if __name__ == "__main__":
main()
