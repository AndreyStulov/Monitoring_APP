# Alt+Ctrl+L format code in pep-8
from urllib import request
import re
import requests

myUrl = "http://www.cbr.ru/scripts/XML_daily.asp"
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 YaBrowser/19.3.2.177 Yowser/2.5 Safari/537.36'
}

def CBR_Parse(myUrl, headers):

    arr_Nominal = []
    final_Nominal = []
    arr_Names = []
    final_Names = []

    arr_Value = []
    temp_Value = []
    temp2_Value = []
    final_Value = []

    Nominal_Value = []
    Uno_Cost = []

    ValuteDict = dict()

    COUNTER_OF_ITERATION = 0
    SIZE_OF_ARRAYS = len(final_Names)

    session = requests.Session()
    thisRequest = session.get(myUrl, headers=headers)
    if thisRequest.status_code == 200:
        with request.urlopen(myUrl) as webpage:
            for line in webpage:
                line = line.strip()
                line = line.decode('windows-1251')
                #print(line)
    else:
        print('ERROR')

    tegsNominal = r"<Nominal>\d+</Nominal>"
    tegsName = r"<CharCode>\w+</CharCode>"
    tegsValue = r"<Value>\d+,\d+</Value>"

    def result(tegs):
        return re.findall(tegs, line)

    arr_Nominal.extend(result(tegsNominal))
    arr_Names.extend(result(tegsName))
    arr_Value.extend(result(tegsValue))
### Information without tags #################################################################################################################################

    for i in arr_Nominal:
        final_Nominal.append(i[9:-10])

    for i in arr_Names:
        final_Names.append(i[10:-11])

    for i in arr_Value:
        temp_Value.append(i[7:-8])

# print(final_Nominal)
# print(final_Names)
# print(temp_Value)

# Swap to point for float values ####################################################################################

    arr_Value.clear()
    for i in temp_Value:
        for j in str(i):
            if j == ',':
                j = '.'
            temp2_Value.append(j)
        final_Value = ''.join(temp2_Value)
        temp2_Value.clear()
        arr_Value.append(final_Value)
    # print(arr_Value)

#####################################################################################
    Nominal_Value.insert(0, final_Nominal)
    Nominal_Value.insert(1, arr_Value)

# Uno cost of valutes ####################################################################################

    for i in Nominal_Value[0]:
        if i == '10':
            Uno_Cost.append((float(Nominal_Value[1][COUNTER_OF_ITERATION])) / 10)
        elif i == '100':
            Uno_Cost.append((float(Nominal_Value[1][COUNTER_OF_ITERATION])) / 100)
        elif i == '1000':
            Uno_Cost.append((float(Nominal_Value[1][COUNTER_OF_ITERATION])) / 1000)
        elif i == '10000':
            Uno_Cost.append((float(Nominal_Value[1][COUNTER_OF_ITERATION])) / 10000)
        else:
            Uno_Cost.append(float(Nominal_Value[1][COUNTER_OF_ITERATION]))

        COUNTER_OF_ITERATION = COUNTER_OF_ITERATION + 1

# print(Uno_Cost)

# Use Round() for Values ####################################################################################
    arr_Value.clear()
    for i in Uno_Cost:
        arr_Value.append((round(i, 3)))
    COUNTER_OF_ITERATION = 0
# print(arr_Value)

# Append of dict ####################################################################################
    for i in arr_Value:
        ValuteDict[i] = final_Names[COUNTER_OF_ITERATION]
        COUNTER_OF_ITERATION = COUNTER_OF_ITERATION + 1

    arr_Value.sort()
    MIN_course = arr_Value[0]
    MAX_course = arr_Value[SIZE_OF_ARRAYS - 1]

    return (ValuteDict[MIN_course], MIN_course), (ValuteDict[MAX_course], MAX_course)

    # print(ValuteDict[MIN_course], ' = ', MIN_course, 'RU')
    # print(ValuteDict[MAX_course], ' = ', MAX_course, 'RU')
    # print(Uno_Cost)
    # print(final_Names)
    # print(arr_Value[SIZE_OF_ARRAYS - 1])
a = CBR_Parse(myUrl, headers)
print(a[0])
print(a[1])