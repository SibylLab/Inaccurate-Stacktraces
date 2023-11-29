import pandas as pd
df = pd.read_json (r'C:\Users\meher\Downloads\infozilla-master\infozilla-master\demo\bug418384.json')
df.to_csv (r'C:\Users\meher\Downloads\infozilla-master\infozilla-master\demo\bug418384.txt', index = False)

"""with open("C:/Users/meher/Downloads/infozilla-master/infozilla-master/demo/bug418384.txt") as f:
    for each in f:
        text+=str(each).replace("\n"," ")
print(text)"""
fin = open("C:/Users/meher/Downloads/infozilla-master/infozilla-master/demo/bug418384.txt", "rt")
fout = open("C:/Users/meher/Downloads/infozilla-master/infozilla-master/demo/bug418384_out.txt", "wt")
fin_2 = open("C:/Users/meher/Downloads/infozilla-master/infozilla-master/demo/bug418384_out.txt", "rt")
fout_2 = open("C:/Users/meher/Downloads/infozilla-master/infozilla-master/demo/bug418384_out_2.txt", "wt")
for line in fin:
	#fout.write(line.replace('\\n', ' '))
    fout.write(line.replace("'", ""))
for line in fin_2:
	fout_2.write(line.replace('\\n', ' '))
fin.close()
fin_2.close()
fout.close()
fout_2.close()
