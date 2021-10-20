#Парсинг JMS.LOG
#определение тредов, резка на файлы по тредам
#читаем лог сверху вниз, при появлении нового треда создаём отдельный файл лога и выбрасываем в него нужные данные 

import sys, os, re   #os + regexp
import shutil   #copy/move files
import glob #file exists with wildcard

print('\nSiebel Log Utils: Parse JMS.LOG into threads , 18.10.2021, ZAS\n')

logList = []; #список результирующих логов
logObj  = {};

#открыть новый лог
def openLog(thNum):
    logObj[thNum] = open(pathName + '_' + thNum + extension, 'wb')
    logList.append(thNum)

#записать строку в лог
def writeLog(thNum, content):
    if not thNum in logList:
        openLog(thNum)
    logObj[thNum].write(content.encode('utf8'))

#закрывает все открытые файлы
def closeLog():
    for x in logObj:
       logObj[x].close()

#проверка на наличие аргумента - путь к папке с XML
if len(sys.argv) < 2:
    print('\nUsage: ' + sys.argv[0] + ' <file path>\n')
    exit()

#заготовка по именованию файлов
srcPath = sys.argv[1]
pathName, extension = os.path.splitext(srcPath)

#сообщение при наличии результирующих файлов
#file_exists = os.path.exists(pathName + '_*.*')
#print(pathName);
#if file_exists:

if glob.glob(pathName + '_*.*'):
    print('Result file exists, delete it before start')
    exit()

#чтение файла
currThreadNum = ''
pattern = 'http-nio-9080-exec-([0-9]+)'

fh = open(srcPath, 'r', encoding='utf8')
for line in fh:
    res = re.search(pattern, line)
    if res:
        currThreadNum = res.group(1)
    print('\n>>' + currThreadNum + '\n')

    writeLog(currThreadNum, line)


closeLog()
               
fh.close()
