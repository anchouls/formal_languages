import sys

import parser

if len(sys.argv) != 2:
    print("Передайте в аргументы название файла с прологом")
else:
    file_name = sys.argv[1]
    with open(file_name, "r") as reader:
        data = reader.read()
        result = parser.parser.parse(data)
        print(result, sep='\n')

