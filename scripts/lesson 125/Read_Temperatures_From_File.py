'''
-There is a file which contains temperatures in Celsius or Fahrenheit, one string per line. 
The strings are expected to look like this: 10F or -15C. 
-Write a Python program which asks: 
    -the user for an input value for the file location 
    -reads the file line by line 
    -converts each temperature to Fahrenheit if it is in Celsius  
    -writes the converted values in a new file 
-The input and output values should be floating-point numbers. 
'''
import os
import sys

class Temperature:
    temp = 0
    degree_symbol = ''

    def __init__(self, temp, degree_symbol):
        self.temp = temp
        self.degree_symbol = degree_symbol

    def to_string(self):
        return str(self.temp) + self.degree_symbol


def convert_to_fahrenheit(temp):
    try:
        temp_float = float(temp)
    except:
        temp_float = 0

    return (temp_float * 1.8) + 32


print("Enter path to file:")
path_to_file = input().replace('\\', '/')

try:
    file = open(path_to_file)
except:
    print('Invalid path')
    sys.exit(0)

path = path_to_file.split('/')
new_path = ''
for i in range(len(path) - 1):
    new_path += path[i] + '/'

raw_data = str(file.read()).replace(',', '').split('\n')
file.close()

temps = []

for i in raw_data:
    i.replace(',', '')
    symbol = i[-1]
    temp = i[0 : len(i)-1]

    try:
        t = Temperature(int(temp) * 1.0, symbol)
        temps.append(t)
    except:
        print("Invalid Data at row ")
        continue

f = open(new_path + "Result.txt", "w")

for i in range(len(temps)):
    comma = ','
    if i == len(temps) - 1:
        comma = ''

    if(temps[i].degree_symbol == 'C'):
        temps[i].temp = round(convert_to_fahrenheit(temps[i].temp), 1)
        temps[i].degree_symbol = 'F'

    f.write(temps[i].to_string().strip() + comma + '\n')

print("Done")
f.close()
