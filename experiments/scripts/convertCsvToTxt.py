import csv
import io

FILEPATH = "C:/Users/meher/Downloads/Spring/"

with io.open(r'C:\Users\meher\Downloads\Spring_v8.csv', mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    try:
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            path = FILEPATH+str(row["Issue key"])+".txt"
            file = open(path,"w+",encoding="utf-8")
            file.write(row["Summary"])
            file.write("\n")
            file.write(row["Issue key"])
            file.write("\n")
            file.write(row["Issue Type"])
            file.write("\n")
            file.write(row["Status"])
            file.write("\n")
            file.write(row["Project key"])
            file.write("\n")
            file.write(row["Priority"])
            file.write("\n")
            file.write(row["Description"])
            file.write("\n")
            for i in range(1,26):
                if row["Comment_"+str(i)] is not None:
                    file.write(row["Comment_"+str(i)])
    except BaseException as error:
        print(row["Issue key"])
        print('An exception occurred: {}'.format(error))
    file.close()
