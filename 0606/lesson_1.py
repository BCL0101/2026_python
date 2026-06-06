file = open("student.txt","r",encoding="utf-8")
print(type(file))
content = file.read()
print(content)
file.close()
file.closed

#=======================

with open("student.txt","r",encoding="utf-8") as file:
	content = file.read()

print(file.closed)

#==============
import csv

with open("考試分數_3年6班.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    # print(type(reader))
    for row in reader:   # for 自訂的變數 in reader:
        print(row)   # dict儲存在row