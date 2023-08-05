from datetime import datetime 
import os


def setLogPath(path):
    global log_path
    log_path = path
    #if path not exist, create
    if not os.path.isdir(log_path):
        os.makedirs(log_path)

def __formLogFileName():
    logFileName = "API"+datetime.today().strftime('%Y%m%d')+".log"
    return logFileName

def __fromReceiptFileName():
    logFileName = "RECEIPT"+datetime.today().strftime('%Y%m%d')+".log"
    return logFileName

def __fromOCTLogFileName():
    logFileName = "OCT"+datetime.today().strftime('%Y%m%d')+".log"
    return logFileName


#log file content format
#<YYYY-MM-DD HH:MM:SS>[PAYMENT TYPE]:{Content to display}
def writeLogString(prefix,content):
    with open(log_path+__formLogFileName(), "a", encoding='utf8') as f:
        f.write(datetime.today().strftime('<%Y-%m-%d %H:%M:%S>') + "[" + prefix + "]:"+content+"\n")
        f.close()

#log file content format
#<YYYY-MM-DD HH:MM:SS>[PAYMENT TYPE]:{KEY:VALUE}
def writeLogDictionary(prefix,dictionary):
    with open(log_path+__formLogFileName(), "a", encoding='utf8') as f:
        for x in dictionary:
            f.write( datetime.today().strftime('<%Y-%m-%d %H:%M:%S>') + "[" + prefix + "]:"+str(x) + ':' + str(dictionary[x])+ "\n")
        f.close()

#Store the receipt
def writeLogReceipt(receipt):
    with open(log_path+__fromReceiptFileName(), "a", encoding='utf8') as f:
        f.write("-"*50+"\n")
        for x in receipt:
            f.write(x+"\n")
        f.write("-"*50+"\n")
        f.close()

#Store OCT required LOG
def writeOCTLogString(prefix,content):
    with open(log_path+__fromOCTLogFileName(), "a", encoding='utf8') as f:
        f.write(datetime.today().strftime('<%d/%m/%Y %H:%M:%S>') + "[" + prefix + "]:"+content+"\n")
        f.close()
