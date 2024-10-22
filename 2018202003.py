import copy as cp
import sys

headerDict = {}
operatorDict = {}

def printData(header, data):
    # header = headerDict[tableName]
    print(*header, sep='\t')
    print("----------------------------------")
    for row in data:
        print(*row, sep="\t")

def printDataDistinct(header, data):
    print(*header, sep='\t')
    print("----------------------------------")
    toPrint = []
    for row in data:
        if (row in toPrint):
            continue
        print(*row, sep="\t")
        toPrint.append(row)

def prepareHeaderDict(fileName):
    global headerDict
    flag = False
    key = ''
    temp = []
    try:
        fp = open(fileName)
        while (True):
            line = fp.readline()
            # print("current line is: ", line)
            if line == '':
                break
            if line[-1] == '\n':
                line = line[:-1]    
            if flag == False and line == '<begin_table>':
                line = fp.readline()
                if line[-1] == '\n':
                    line = line[:-1]
                key = line
                flag = True
                continue
            if flag == True:
                if line != '<end_table>':
                    temp.append(line.lower())   # key+"."+
                else:
                    # print("Key is: ", key, " & value is: ", temp)
                    headerDict[key] = temp
                    temp = []
                    flag = False
                    key = ''             
    except FileExistsError:
        print("Error: File '", fileName, "' does not exist")
    except FileNotFoundError:
        print("Error: File '", fileName, "' does not found")
    finally:
        fp.close()

def readFileIn2DList(fileName):
    tableData = []
    s = "\""
    with open(fileName) as f:
        for line in f:
            # Removing the double quotes if occurs
            if s in line:
                line = line.replace(s, '')
            if(line[-1] == '\n'):
                line = line[:-1]
            row = line.split(',')
            row = list(map(int, row))       # Converting all elements in row to integers
            tableData.append(row)    
    return tableData

def selectAllFromTable(tableName):
    tableFileName = tableName + '.csv'
    data = readFileIn2DList(tableFileName)
    print(*headerDict[tableName], sep='\t')
    print("----------------------------------")
    for row in data:
        print(*row, sep='\t')

def sumColumn(columnName, data, header):
    # tableFileName = tableName + '.csv'
    # data = readFileIn2DList(tableFileName)
    # header = headerDict[tableName]
    index = header.index(columnName)
    # print("Index of column: ", columnName, " is: ", index)
    sum = 0
    print("SUM(", columnName, ")")
    print("---------------------")
    for row in data:
        sum += row[index]
        # sum += int(row[index])
    print(sum)
    # return sum

def averageColumn(columnName, data, header):
    # tableFileName = tableName + '.csv'
    # data = readFileIn2DList(tableFileName)
    # header = headerDict[tableName]
    index = header.index(columnName)
    sum = 0
    n = 0
    print("AVG(", columnName, ")")
    print("---------------------")
    for row in data:
        n += 1
        sum += row[index] 
        # sum += int(row[index])
    print(sum/n)    
    # return sum/n

def maxColumn(columnName, data, header):
    # tableFileName = tableName + '.csv'
    # data = readFileIn2DList(tableFileName)
    # header = headerDict[tableName]
    index = header.index(columnName)
    print("MAX(", columnName, ")")
    print("---------------------")
    max = int(data[0][index])
    for i in range(1, len(data)):
        # temp = int(data[i][index])
        temp = data[i][index]
        if  (temp > max):
            max = temp   
    print(max)
    # return max

def minColumn(columnName, data, header):
    # tableFileName = tableName + '.csv'
    # data = readFileIn2DList(tableFileName)
    # header = headerDict[tableName]
    index = header.index(columnName)
    print("MIN(", columnName, ")")
    print("---------------------")
    min = int(data[0][index])
    for i in range(1, len(data)):
        # temp = int(data[i][index])
        temp = data[i][index]
        if  (temp < min):
            min = temp   
    print(min)        
    # return min

def projectColumns(columnList, data, header):
    # tableFileName = tableName + '.csv'
    # data = readFileIn2DList(tableFileName)
    indexList = []
    # header = headerDict[tableName]
    
    for col in columnList:
        indexList.append(header.index(col))
    # print("Index list is: ", indexList)
    
    # Printing Header
    for i in indexList:
        print(header[i], end="\t")
    print("\n----------------------------------")

    # Printing Data
    for row in data:
        for i in indexList:
            print(row[i], end="\t")
        print()        

def projectColumnsDistinct(columnList, data, header):
    # tableFileName = tableName + '.csv'
    # data = readFileIn2DList(tableFileName)
    # header = headerDict[tableName]
    
    indexList = []
    for col in columnList:
        indexList.append(header.index(col))
    
    # Printing Header
    for i in indexList:
        print(header[i], end="\t")
    print("\n----------------------------------")
    toPrint = []
    # Accumulating distinct Data
    for row in data:
        temp = []
        for i in indexList:
            temp.append(row[i])
        try:
            toPrint.index(temp)
        except ValueError:
            toPrint.append(temp)
            print(*temp, sep="\t")    
    toPrint = []

def trimListElements(strList):
    for i in range(len(strList)):
        strList[i] = strList[i].strip()
    return strList

def splitCondition(cond):
    # print("Cond is: ", cond)
    op = None
    if cond.find("<=") != -1:
        op = "<="
    elif cond.find("<") != -1:
        op = "<"
    elif cond.find(">=") != -1:
        op = ">="
    elif cond.find(">") != -1:
        op = ">"
    elif cond.find("=") != -1:
        op = "="
    # print("operator is:", op)    
    index = cond.index(op)        
    colName = cond[: index]
    value = cond[index+len(op):]
    colName = colName.strip()
    value = value.strip()
    # print("col, op, value are:", colName, ",",op, ",",value)
    return colName, op, value

# Filter rows for a column, operator and value
def filterRowsByCond(data, header, colName, op, value):
    index = header.index(colName)

    returnData = []
    for row in data:
        if op == "<=" and row[index] <= value:
            returnData.append(row)
        elif op == "<" and row[index] < value:
            returnData.append(row)
        elif op == ">=" and row[index] >= value:
            returnData.append(row)
        elif op == ">" and row[index] > value:
            returnData.append(row)
        elif op == "=" and row[index] == value:
            returnData.append(row)    
    return returnData           

# Filter rows only by equality of columns
def filterRowsJoinCond(data, header, col1, col2):
    index1 = header.index(col1)
    index2 = header.index(col2)
    returnData = []
    
    for row in data:
        if row[index1] == row[index2]:
            returnData.append(row)
    
    return returnData        

# Deletes a particular column from list of Lists 
def deleteColumnFrom2DList(data, colIndex):
    for row in data:
        try :
            del row[colIndex]
        except IndexError:
            print("Index: ",colIndex, " Out of Range")
    return data        

# Returns header and data of the cartesian product
def prepareCartesianProduct(tableName1, tableName2):
    header1 = headerDict[tableName1]
    header2 = headerDict[tableName2]
    tableData1 = readFileIn2DList(tableName1 + ".csv")
    tableData2 = readFileIn2DList(tableName2 + ".csv")

    # Preparing header
    newHeader = []
    for col in header1:
        newHeader.append(tableName1 + "." + col)

    for col in header2:
        newHeader.append(tableName2 + "." + col)
    
    catesianProd = []

    for outerRow in tableData1:
        for innerRow in tableData2:
            newRow = cp.deepcopy(outerRow)
            newRow.extend(innerRow)
            # print(*newRow, sep="\t")
            catesianProd.append(newRow)
    return newHeader, catesianProd

def checkColumnValidity(col, table1, table2):
    print("")
    err = None
    if (col.startswith(table1+".") == False) and (col.startswith(table2+".") == False):
        if ((col in headerDict[table1]) == True) and ((col in headerDict[table2]) == False):
            col = table1 + "." + col
        elif ((col in headerDict[table1]) == False) and ((col in headerDict[table2]) == True):    
            col = table2 + "." + col
        elif ((col in headerDict[table1]) == False) and ((col in headerDict[table2]) == False):
            err = "Column '"+ col +"' does not belongs to any table.."
        else:
            err = "Column '"+col+"' is ambiguous. Please provide table name.."
    
    else:
        # This section contains bug
        if (col.startswith(table1+".")):
            temp = col[len(table1+"."):]
        elif (col.startswith(table2+".")):
            temp = col[len(table2+"."):]

        if ((temp in headerDict[table1]) == False) and ((temp in headerDict[table2]) == False):
            err = "Column '"+ col +"' does not belongs to any table.."
    
    return err, col   

def performUnion(data1, data2):
    for row in data2:
        if (row in data1) == False:
            data1.append(row)
    return data1        

def validateCondOnJoinedTables(data, header, col, op, value, table1, table2):
    err, col = checkColumnValidity(col, table1, table2)
    if err != None:
        print(err)
        quit()
    try:
        value = int(value)
        tempData = filterRowsByCond(data, header, col, op, value)
    except ValueError:
        # Checking if the value is also a column for join condition
        err, col2 = checkColumnValidity(value, table1, table2)
        if err != None:
            print(err)
            quit()
        tempData = filterRowsJoinCond(data, header, col, col2)
    return tempData    

def validateSingleTableCond(data, header, col, op, value):
    if (col in header) == False:
        print("Column '", col ,"' does not belong to table..")
        quit()
    value = int(value)    
    tempData = filterRowsByCond(data, header, col, op, value)
    return tempData


def parseSQL(sql):
    # sql = input("Enter the query: ")
    sql = sql.lower()
    # selectIndex = sql.index("SELECT ")
    if (("select ") in sql) == False:    # selectIndex == -1
        print("Error: 'select' keyword missing..")
        quit()
    selectIndex = sql.index("select ")
    if selectIndex != -1 and selectIndex != 0:
        print("Error: 'select' keyword misplaced..")
        quit()
    # fromIndex = sql.index(" FROM ")
    fromIndex = -1
    if ((" from ") in sql) == False:
        print("Error: 'from' keyword missing..")
        quit()
    if sql[-1] != ';':
        print("Error: semicolon missing..")
        quit()
    else:
        fromIndex = sql.index(" from ")
        sql = sql[:-1]
    # whereIndex = sql.index(" WHERE ")
    whereIndex = -1
    if ((" where ") in sql) == False:    # whereIndex == -1
        tables = sql[fromIndex+len(" from "):]
    else:
        whereIndex = sql.index(" where ")
        tables = sql[fromIndex+len(" from "): whereIndex]
    tables = tables.strip()
    tables = tables.lower()  # As the csv files are named in lowercase letters
    
    # Checking for join
    comaCount = tables.count(',')
    if comaCount > 1:
        print("Error: Joining more than 2 tables not supported..")
        quit()
    if comaCount == 0:
        table1 = tables
        if (table1 in headerDict) == False:
            print("Error: Table '",table1, "' does not exist..")
            quit()
        table1 = table1.strip()    
        header = headerDict[table1]
        data = readFileIn2DList(table1+".csv")
    else:   # comaCount == 1        
        comaIndex = tables.index(',')
        table1 = tables[:comaIndex]
        table1 = table1.strip()
        if (table1 in headerDict) == False:
            print("Error: Table : '",table1, "' does not exist..")
            quit()
         
        table2 = tables[comaIndex+1:]
        table2 = table2.strip()
        if (table1 in headerDict) == False:
            print("Error: Table : '",table1, "' does not exist..")
            quit()
        header, data = prepareCartesianProduct(table1, table2)
    
    # Processing where clause/s
    if whereIndex != -1:
        # processWhere(sql, data, header)
        clause = sql[whereIndex+len(" where "):]
        
        if clause.find(" or ") != -1:
            orIndex = clause.index(" or ") 
            cond1 = clause[:orIndex]
            cond1 = cond1.strip()
            cond2 = clause[orIndex+len(" or "):]
            cond2 = cond2.strip()
            
            # Checking first condition
            col, op, value = splitCondition(cond1)
            if comaCount == 1:
                data1 = validateCondOnJoinedTables(data, header, col, op, value, table1, table2)
            elif comaCount == 0:
                data1 = validateSingleTableCond(data, header, col, op, value)
                
            # Checking second condition
            col, op, value = splitCondition(cond2)
            if comaCount == 1:
                data2 = validateCondOnJoinedTables(data, header, col, op, value, table1, table2) 
            elif comaCount == 0:
                data2 = validateSingleTableCond(data, header, col, op, value)
                
            # Performing union due to OR condition
            data = performUnion(data1, data2)
        
        elif clause.find(" and ") != -1:
            andIndex = clause.index(" and ")
            cond1 = clause[:andIndex]
            cond1 = cond1.strip()
            cond2 = clause[andIndex+len(" and "):]
            cond2 = cond2.strip()

            # Checking first condition
            col, op, value = splitCondition(cond1)
            if comaCount == 1:
                data = validateCondOnJoinedTables(data, header, col, op, value, table1, table2)
            elif comaCount == 0:
                data = validateSingleTableCond(data, header, col, op, value)
                
            # Checking second condition
            col, op, value = splitCondition(cond2)
            if comaCount == 1:
                data = validateCondOnJoinedTables(data, header, col, op, value, table1, table2)
            elif comaCount == 0:
                data = validateSingleTableCond(data, header, col, op, value)
            
            # No need to perform intersection as already passing filtered data based on first condition
            # data = filterRowsByCond(data, header, col, op, value)       
        
        # Single condition
        else:
            cond = clause
            cond = cond.strip()
            col, op, value = splitCondition(cond)
            if comaCount == 1:
                data = validateCondOnJoinedTables(data, header, col, op, value, table1, table2)
            elif comaCount == 0:
                data = validateSingleTableCond(data, header, col, op, value)
    # Processing of where clause completed here
    
    # Projecting columns on above filtered data
    toSelect = sql[selectIndex+len("select "): fromIndex]
    toSelect = toSelect.strip()
    distinctFlag = False
    if toSelect.startswith("distinct "):
        distinctFlag = True
        toSelect = toSelect[len("distinct "):]
    if toSelect == "*":
        if distinctFlag:
            printDataDistinct(header, data)
        else:
            printData(header, data)
    elif toSelect.startswith("sum(") and toSelect.endswith(")"):
            col = toSelect[len("SUM("):-1]
            if comaCount == 0:
                if (col in header) == False:
                    print("Column '", col ,"' does not belong to table..")
                    quit()
            elif comaCount == 1:
                err, col = checkColumnValidity(col, table1, table2)
                if err != None:
                    print(err)
                    quit()
            sumColumn(col, data, header)
    
    elif toSelect.startswith("avg(") and toSelect.endswith(")"):
            col = toSelect[len("AVG("):-1]
            if comaCount == 0:
                if (col in header) == False:
                    print("Column '", col ,"' does not belong to table..")
                    quit()
            elif comaCount == 1:
                err, col = checkColumnValidity(col, table1, table2)
                if err != None:
                    print(err)
                    quit()
            averageColumn(col, data, header)            
    
    elif toSelect.startswith("max(") and toSelect.endswith(")"):
            col = toSelect[len("MAX("):-1]
            if comaCount == 0:
                if (col in header) == False:
                    print("Column '", col ,"' does not belong to table..")
                    quit()
            elif comaCount == 1:
                err, col = checkColumnValidity(col, table1, table2)
                if err != None:
                    print(err)
                    quit()
            maxColumn(col, data, header)            
    
    elif toSelect.startswith("min(") and toSelect.endswith(")"):
            col = toSelect[len("MIN("):-1]
            if comaCount == 0:
                if (col in header) == False:
                    print("Column '", col ,"' does not belong to table..")
                    quit()
            elif comaCount == 1:
                err, col = checkColumnValidity(col, table1, table2)
                if err != None:
                    print(err)
                    quit()
            minColumn(col, data, header)            
    
    else:
        # Projecting columns
        columns = toSelect.split(",")
        colToIterate = []
        flag = False
        # Checking all the columns to be projected are valid
        for col in columns:
            col = col.strip()
            if comaCount == 0:
                if (col in header) == False:
                    print("Column '", col ,"' does not belong to table..")
                    flag = True
                    break
                else:
                    colToIterate.append(col)
            elif comaCount == 1:
                err, col = checkColumnValidity(col, table1, table2)
                if err != None:
                    print(err)
                    flag = True
                    break
                else:
                    colToIterate.append(col)    
        if flag:
            quit()
        else:
            # Projecting the columns
            if distinctFlag:
                projectColumnsDistinct(colToIterate, data, header)
            else:    
                projectColumns(colToIterate, data, header)

if __name__ == '__main__':    
    prepareHeaderDict('metadata.txt')
    sql = str(sys.argv[1])
    if sql == None or sql == '':
        print("No SQL query provided as arguement..")
    else:    
        parseSQL(sql)