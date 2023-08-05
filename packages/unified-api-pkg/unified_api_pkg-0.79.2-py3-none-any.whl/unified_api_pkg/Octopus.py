from ctypes import *
from .OctopusUtils import *
from datetime import datetime
from .generalUtils import *
from .logUtils import *
import time

dll_path = 'C:\\RML\\lib\\rml.dll'

dll = windll.LoadLibrary(dll_path)

device_TID = None
company_MID = None
TimeOut = None

OCT_BASCI_TIMESTAMP = 946684800

def __checkSameCard(transData,pollPan):
    if "PAN" in transData:
        if transData["PAN"] == pollPan:
            #Same PAN, perform retry
            return True
        else:
            #Not the same PAN, reject and prompt retap correct card
            return False
    else:#Expect no a retry call
        return True

def openOCTCom(octCOM,octOutID,octTimeOut):
    global TimeOut
    TimeOut = int(octTimeOut)
    result = dll.InitComm(int(octCOM),115200)

    writeLogString("OCT","OPEN COM:"+str(result))
    writeOCTLogString("InitComm",str(result))

    output = (c_char *1024)()
    if result == 0:
        result = dll.RMS_Init(int(octOutID),output)

        writeLogString("OCT","RMS INIT:"+str(result))
        writeOCTLogString("RMS_Init",str(result))
    return result

def closeOCTCom():
    result = dll.PortClose()

    writeLogString("OCT","CLOSE COM:"+str(result))
    return result

def getDeviceInfo():
    device_info = []
    global device_TID
    global company_MID
    output = (c_uint * 56)()
    result = dll.TimeVer(output)

    writeLogString("OCT","GET DEVICE INFO:"+str(result))

    device_info.append(result)

    if result == 0:
        device_TID = hex(output[0])[2:].upper()
        company_MID = str(output[3])

        device_info.append(device_TID)
        device_info.append(company_MID)
        
        writeLogString("OCT","DEVICE ID:"+str(device_TID))
        writeLogString("OCT","COMPANY ID:"+str(company_MID))

    return device_info

def polling(option,transData,pollType):

    writeLogString("OCT POLL","OPTION:"+option+"||"+"POLLTYPE:"+str(pollType))

    output = (c_char * 1024)()
    #RMS polling require 128
    if option == "REWARDBAL":
        pollType = 128

    for t in range(0,int(TimeOut)):
        result = dll.PollEx(pollType,10,output)
        if result == 100032:
            pass
        else:
            break
    
    writeLogString("OCT POLL","POLL:"+str(result))

    if result  < 100000:
        list_output_string = output.value.decode("utf-8").split(",")
        if pollType == 2:
            list_customer_info = list_output_string[3].split("-")

            if __checkSameCard(transData,list_output_string[2]):
                transData["OCTTYPE"] = list_customer_info[0]
                transData["OCTOLDPAN"] = list_output_string[0]
                transData["PAN"] = list_output_string[2]
            else:
                writeOCTLogString("PollEx", "Present false card, API handle reject as 101005")
                return 101005

        elif pollType == 128:
            list_customer_info = list_output_string[2].split("-")

            if __checkSameCard(transData,list_output_string[1]):
                transData["OCTTYPE"] = list_customer_info[0]
                transData["OCTOLDPAN"] = list_output_string[0]
                transData["PAN"] = list_output_string[1]
            else:
                writeOCTLogString("PollEx", "Present false card, API handle reject as 101005")
                return 101005

        #less than 100000 is valid
        transData["CMD"] = "ENQ"
        transData["TYPE"] = "OCT_REWARDS"

        
        transData["TID"] = device_TID
        transData["DEVICENO"] = device_TID
        transData["MID"] = company_MID

        now = datetime.now()
        transData["DATE"] = now.strftime("%Y%m%d")
        transData["TIME"] = now.strftime("%H%M%S")
        transData["ACQNAME"] = "OCT_REWARDS"
        transData["CARD"] = "OCT_REWARDS"
        transData["STATUS"] = "APPROVE"
        transData["RESP"] = str(result)
        transData["REMINBAL"] = float(result)/10

        writeOCTLogString("PollEx",transData["PAN"]+","+transData["OCTOLDPAN"]+","+transData["OCTTYPE"]+","+str(result))

        if option == "HISTORY":
            #from index 5 - 10 record, each record has 5 elements
            list_history = []
            for x in range(5, 55, 5):
                try:
                    dict_history = {}
                    txn_datetime = datetime.fromtimestamp(OCT_BASCI_TIMESTAMP+int(list_output_string[x+2]))
                    dict_history["DATE"] = txn_datetime.strftime("%Y%m%d")
                    dict_history["TIME"] = txn_datetime.strftime("%H%M%S")
                    dict_history["AMT"] = float(list_output_string[x+1])/10
                    dict_history["DEVICEID"] = hex(int(list_output_string[x+3]))[2:].upper()
                    dict_history["ECRREF"] = str(list_output_string[x+4])
                    list_history.append(dict_history)
                except:
                    #skip this record
                    pass
            transData["HISTORY"] = list_history
        elif option == "REWARDBAL":
            result = __RMS_get()
            writeLogString("OCT","RMS GET:"+str(result))
            if result < 10000:
                transData["REWARDBAL"] = result/100
            else:
                packResponseCode(result,transData)
    else:
        packResponseCode(result,transData)
        writeOCTLogString("PollEx",str(result))
    return result

def pollingForRetry(option,transData,pollType,time):

    writeLogString("OCT POLL","OPTION:"+option+"||"+"POLLTYPE:"+str(pollType))

    output = (c_char * 1024)()
    #RMS polling require 128
    if option == "REWARDBAL":
        pollType = 128

    for t in range(0,int(time)):
        result = dll.PollEx(pollType,10,output)
        if result == 100032:
            pass
        else:
            break
    
    writeLogString("OCT POLL","POLL:"+str(result))

    if result  < 100000:
        list_output_string = output.value.decode("utf-8").split(",")
        if pollType == 2:
            list_customer_info = list_output_string[3].split("-")

            if __checkSameCard(transData,list_output_string[2]):
                transData["OCTTYPE"] = list_customer_info[0]
                transData["OCTOLDPAN"] = list_output_string[0]
                transData["PAN"] = list_output_string[2]
            else:
                writeOCTLogString("PollEx", "Present false card, API handle reject as 101005")
                return 101005

        elif pollType == 128:
            list_customer_info = list_output_string[2].split("-")

            if __checkSameCard(transData,list_output_string[1]):
                transData["OCTTYPE"] = list_customer_info[0]
                transData["OCTOLDPAN"] = list_output_string[0]
                transData["PAN"] = list_output_string[1]
            else:
                writeOCTLogString("PollEx", "Present false card, API handle reject as 101005")
                return 101005

        #less than 100000 is valid
        transData["CMD"] = "ENQ"
        transData["TYPE"] = "OCT_REWARDS"

        
        transData["TID"] = device_TID
        transData["DEVICENO"] = device_TID
        transData["MID"] = company_MID

        now = datetime.now()
        transData["DATE"] = now.strftime("%Y%m%d")
        transData["TIME"] = now.strftime("%H%M%S")
        transData["ACQNAME"] = "OCT_REWARDS"
        transData["CARD"] = "OCT_REWARDS"
        transData["STATUS"] = "APPROVE"
        transData["RESP"] = str(result)
        transData["REMINBAL"] = float(result)/10

        writeOCTLogString("PollEx",transData["PAN"]+","+transData["OCTOLDPAN"]+","+transData["OCTTYPE"]+","+str(result))

        if option == "HISTORY":
            #from index 5 - 10 record, each record has 5 elements
            list_history = []
            for x in range(5, 55, 5):
                try:
                    dict_history = {}
                    txn_datetime = datetime.fromtimestamp(OCT_BASCI_TIMESTAMP+int(list_output_string[x+2]))
                    dict_history["DATE"] = txn_datetime.strftime("%Y%m%d")
                    dict_history["TIME"] = txn_datetime.strftime("%H%M%S")
                    dict_history["AMT"] = float(list_output_string[x+1])/10
                    dict_history["DEVICEID"] = hex(int(list_output_string[x+3]))[2:].upper()
                    dict_history["ECRREF"] = str(list_output_string[x+4])
                    list_history.append(dict_history)
                except:
                    #skip this record
                    pass
            transData["HISTORY"] = list_history
        elif option == "REWARDBAL":
            result = __RMS_get()
            writeLogString("OCT","RMS GET:"+str(result))
            if result < 10000:
                transData["REWARDBAL"] = result/100
            else:
                packResponseCode(result,transData)
    else:
        packResponseCode(result,transData)
        writeOCTLogString("PollEx",str(result))
    return result

def topUp(ecr_ref,Type,amount,transData):
    UD_list = []
    transData["ECRREF"] = ecr_ref
    if amount == 0 and Type == "SUBSIDY":
        list_subsidy = []
        transData["AMT"] = 0
        #Transport subsidy
        result = polling("SUBSIDY",transData,2)

        writeLogString("OCT","POLL:"+str(result))

        if result < 100000:
            int_ecr = int(ecr_ref)

            writeLogString("OCT","ECR REF CHECK:"+str(int_ecr))

            if int_ecr >= 65535:
                #too large for Octopus device
                result = [101102]
                packResponseCode(101102,transData)
                return result[0]
            else:
                result =  __CollectSubsidy(int_ecr,list_subsidy)

                writeLogString("OCT","COLLECT SUBSIDY:"+str(result))

                if result[0] < 100000:
                    transData["CMD"] = "SUBSIDY"
                    transData["REMINBAL"] = float(result[0])/10
                    #Subsidy data
                    transData["SUBSIDY_TOTAL"] = float(result[1])/10
                    transData["SUBSIDY_COLLECT"] = float(result[2])/10
                    transData["SUBSIDY_OUTSTAND"] = float(result[3])/10
                    transData["SUBSIDY_REASON"] = int(result[4])
                    #NO of sub collect ignore
                    
                    writeLogDictionary("OCT SUBSIDY",transData)
                    __GetExtraInfo(transData)
                    if __getInstantUD(UD_list) == 0:
                        formatTransDataOctopus(UD_list,transData)
                        packResponseCode(result[0],transData)
                    return result[0]
                else:
                    packResponseCode(result[0],transData)
                return result[0]
        else:
            transData["CMD"] = "TOPUP"
            packResponseCode(result,transData)
            return result
    else:
        #do a Poll

        #Default a value avoid 100022
        transData["AMT"] = float(amount)/10

        result = polling("TOPUP",transData,2)

        writeLogString("OCT","POLL:"+str(result))
        
        if result < 100000:

            #Poll success
            output = (c_char * 1024)()

            # if len(ecr_ref) > 5:
            #     temp_ecr_ref = '0'+ecr_ref[0:5]
            #     b_ecr = temp_ecr_ref.encode('utf-8')
            #     memmove(output,b_ecr,6)

            ecrRefToBCDByte(output,ecr_ref,False)
            if Type == "TOPUP":
                result = dll.AddValue(amount,1,output)
            elif Type == "CHANGE":
                input_char = (c_char)()
                input_char.value = 1
                result = dll.AddValue(amount,input_char,output)

            writeLogString("OCT","TOPUP:"+str(result))
            transData["CMD"] = "TOPUP"

            if result < 100000:
                __GetExtraInfo(transData)
                if __getInstantUD(UD_list) == 0:
                    formatTransDataOctopus(UD_list,transData)
                    packResponseCode(result,transData)
                
                writeOCTLogString("AddValue",transData["PAN"]+","+transData["ECRREF"]+","+str(amount)+","+str(result))
                return result
            else:
                writeOCTLogString("AddValue", str(result))
                packResponseCode(result,transData)
                return result
        else:
            transData["CMD"] = "TOPUP"
            transData["AMT"] = float(amount)/10
            packResponseCode(result,transData)
            return result

def topUpForRetry(ecr_ref,Type,amount,time,transData):
    UD_list = []
    transData["ECRREF"] = ecr_ref
    if amount == 0 and Type == "SUBSIDY":
        list_subsidy = []
        transData["AMT"] = 0
        #Transport subsidy
        result = pollingForRetry("SUBSIDY",transData,2,time)

        writeLogString("OCT","POLL:"+str(result))

        if result < 100000:
            int_ecr = int(ecr_ref)

            writeLogString("OCT","ECR REF CHECK:"+str(int_ecr))

            if int_ecr >= 65535:
                #too large for Octopus device
                result = [101102]
                packResponseCode(101102,transData)
                return result[0]
            else:
                result =  __CollectSubsidy(int_ecr,list_subsidy)

                writeLogString("OCT","COLLECT SUBSIDY:"+str(result))

                if result[0] < 100000:
                    transData["CMD"] = "SUBSIDY"
                    transData["REMINBAL"] = float(result[0])/10
                    #Subsidy data
                    transData["SUBSIDY_TOTAL"] = float(result[1])/10
                    transData["SUBSIDY_COLLECT"] = float(result[2])/10
                    transData["SUBSIDY_OUTSTAND"] = float(result[3])/10
                    transData["SUBSIDY_REASON"] = int(result[4])
                    #NO of sub collect ignore
                    
                    writeLogDictionary("OCT SUBSIDY",transData)
                    __GetExtraInfo(transData)
                    if __getInstantUD(UD_list) == 0:
                        formatTransDataOctopus(UD_list,transData)
                        packResponseCode(result[0],transData)
                    return result[0]
                else:
                    packResponseCode(result[0],transData)
                return result[0]
        else:
            transData["CMD"] = "TOPUP"
            packResponseCode(result,transData)
            return result
    else:
        #do a Poll

        #Default a value avoid 100022
        transData["AMT"] = float(amount)/10

        result = pollingForRetry("TOPUP",transData,2,time)

        writeLogString("OCT","POLL:"+str(result))
        
        if result < 100000:

            #Poll success
            output = (c_char * 1024)()

            # if len(ecr_ref) > 5:
            #     temp_ecr_ref = '0'+ecr_ref[0:5]
            #     b_ecr = temp_ecr_ref.encode('utf-8')
            #     memmove(output,b_ecr,6)

            ecrRefToBCDByte(output,ecr_ref,False)
            if Type == "TOPUP":
                result = dll.AddValue(amount,1,output)
            elif Type == "CHANGE":
                input_char = (c_char)()
                input_char.value = 1
                result = dll.AddValue(amount,input_char,output)

            writeLogString("OCT","TOPUP:"+str(result))
            transData["CMD"] = "TOPUP"

            if result < 100000:
                __GetExtraInfo(transData)
                if __getInstantUD(UD_list) == 0:
                    formatTransDataOctopus(UD_list,transData)
                    packResponseCode(result,transData)
                
                writeOCTLogString("AddValue",transData["PAN"]+","+transData["ECRREF"]+","+str(amount)+","+str(result))
                return result
            else:
                writeOCTLogString("AddValue", str(result))
                packResponseCode(result,transData)
                return result
        else:
            transData["CMD"] = "TOPUP"
            transData["AMT"] = float(amount)/10
            packResponseCode(result,transData)
            return result

def saleOCT(payment_type,ecr_ref,amount,additional_amount,payment_option,transData,printOut):
    list_last_txn = []
    transData["ECRREF"] = ecr_ref
    if "OCT_LAST" in transData:
        list_last_txn = transData["OCT_LAST"]
        #shift the octopus payment to the last
        list_last_txn.append(list_last_txn.pop(0))

        writeLogString("OCT","OCT LAST:"+str(list_last_txn))
    
    if payment_option != "REDEEM_COMP":
        result = polling("SALE",transData,128)

        writeLogString("OCT","POLL:"+str(result))

        if result < 100000:
            if payment_option == "" or payment_option == None: 
                result = __RMS_TXN(0,list_last_txn,amount,ecr_ref,transData)

                transData["NON_REWARDS"] = "Y"
                return result
            else:
                result = __RMS_get()
                if result < 100000:
                    if payment_option == "DO_NOT_REDEEM" or payment_option == "ISSUE":
                        #issue R$ only, settle by Octopus
                        result = __RMS_TXN(1,list_last_txn,amount,ecr_ref,transData)

                        return result
                    elif payment_option == "NORMAL_REDEEM":
                        #redeem and issue, by Octopus only
                        result = __RMS_TXN(3,list_last_txn,amount,ecr_ref,transData)

                        return result
                    elif payment_option == "REDEEM_CHECK":
                        #Redeem Check, return eligble R$
                        result =__RMS_Redeem_Check(amount,amount)

                        writeLogString("OCT","RMS_REDEEM_CHECK:"+str(result))

                        transData["REWARDBAL"] = result/100
                        return result
                else:
                    packResponseCode(result,transData)
                    return result
        else:
            packResponseCode(result,transData)
            return result
    else:
        #Complete the transaction by previous REDEEM_CHECK command
        result = __RMS_TXN(3,list_last_txn,amount,ecr_ref,transData)

        writeLogString("OCT","RMS_TXN:"+str(result))

        return result

def __RMS_get():
    buf = (c_int * 1)()
    result = dll.RMS_Get(0,1,buf)

    writeLogString("OCT","RMS_GET:"+str(result))

    if result < 100000:
        writeLogString("OCT","RMS_REWARDS BAL:"+str(buf[0]))
        writeOCTLogString("RMS_Get",str(result)+","+"0"+","+"1"+","+str(buf[0]))
        return buf[0]
    else:
        writeOCTLogString("RMS_Get",str(result))
        return result

def __RMS_TXN(option,list_lastTxn,amount,ecr_ref,transData):
    input = (c_int32*26)()
    output = (c_int*6)()

    #extra_issue;redeem;redeem_off
    #should be provided as setting
    input[0] = 0
    input[1] = 0
    input[2] = 0

    #total amount 
    input[3] = amount
    #redeem or not; bit 1 issue ;bit 2 redeem; bit 3 RMS register; 0 normal deduct
    input[4] = option
    #split payment

    if option > 0:
        if len(list_lastTxn) == 0:
            input[5] = 2
            input[6] = 0
            input[7] = amount
            input[8] = 128
            input[9] = 0
        else:
            input[5] = len(list_lastTxn) *2
            for x in range(0,len(list_lastTxn)):
                input[6+(4*x)] = x
                input[7+(4*x)] = inputAmountStringToLong(list_lastTxn[x])
                input[8+(4*x)] = x + 128
                input[9+(4*x)] = 0
    else:
        input[5] = 1
        input[6] = 0
        input[7] = amount

    ecrRefToBCDByte(input,ecr_ref,True)

    for x in range(0,24):
        writeLogString("OCT","RMS_TXN INPUT:"+ str(x)+":"+str(input[x]))

    result = dll.RMS_TXN(input,output)
    
    writeLogString("OCT","RMS_TXN:"+ str(result))

    for x in range(0,6):
        writeLogString("OCT","RMS_TXN OUTPUT:"+ str(x)+":"+str(output[x]))
    #success
    if result == 0:
        if option >0:
            writeOCTLogString("RMS_TXN","0,0,0,"+str(amount)+","+str(option)+","+str(input[5])+","+str( input[8+(4*len(list_lastTxn))] )+",0,"+str(output[0])+","+str(output[1])+","+str(output[2])+","+str(output[3])+","+str(output[4]))
        else:
            writeOCTLogString("RMS_TXN","0,0,0,"+str(amount)+","+str(option)+",1,0,"+str(amount)+","+str(output[0])+","+str(output[1])+","+str(output[2])+","+str(output[3])+","+str(output[4]))

        result = dll.RMS_Update(0)
        writeOCTLogString("RMS_Update",str(result)+","+"0")

        writeLogString("OCT","RMS_UPDATE:"+ str(result))

        #get data from output.  
        transData["R_EARN"] = output[0]/100
        transData["NETAMT"] = output[3]/100
        transData["R_REDEEMED"] = output[1]/100
        transData["R_BALANCE"] = output[5]/100

        if result == 0:
            __GetExtraInfo(transData)
            UD_list = []
            if __getInstantUD(UD_list) == 0:
                transData["CMD"] = "SALE"
                formatTransDataOctopus(UD_list,transData)
                packResponseCode(result,transData)
            return result
        else:
            transData["CMD"] = "SALE"
            packResponseCode(result,transData)
            return result
    else:
        packResponseCode(result,transData)
        writeOCTLogString("RMS_TXN",str(result))
        return result

    return result

def __getInstantUD(ud_content):
    UD_length = c_int32()
    UD = c_void_p() 

    result = dll.GetInstantUD(byref(UD),byref(UD_length))

    writeLogString("OCT","GETINSTANCEUD:"+str(result))

    ptrt = POINTER(c_char * UD_length.value) 
    mydblPtr = cast(UD, POINTER(c_char * UD_length.value)) 

    indexes = ptrt(mydblPtr.contents)

    writeOCTLogString("GetInstantUD",str(list(indexes.contents))+","+str(UD_length.value))

    if UD_length.value <= 0:
        return result


    #Get total number of UD contained.
    ud_content.append(str(int.from_bytes(indexes.contents[0],'big')))

    idx = 1

    #get thet UD info 1 by 1
    for no_UD in range(0,int.from_bytes(indexes.contents[0],'big')):

        # The size of this UD
        size = int.from_bytes(indexes.contents[idx],'big')

        #the type
        idx = idx + 1

        # UD Type
        ud_content.append(str(int.from_bytes(indexes.contents[idx],'big')))

        #The starting idx of content
        idx = idx + 1

        for x in range(idx,size + idx,4):
            b1 = int.from_bytes(indexes.contents[x],'big')
            b2 = int.from_bytes(indexes.contents[x+1],'big')
            b3 = int.from_bytes(indexes.contents[x+2],'big')
            b4 = int.from_bytes(indexes.contents[x+3],'big')
            y = 0
            y = (y|b4)<<8
            y = (y|b3)<<8
            y = (y|b2)<<8
            y = (y|b1)
            ud_content.append(str(y))

        idx = idx + size
    
    for x in ud_content:
        writeLogString("OCT","GETINSTANCEUD:"+str(x))

    return result

def __GetExtraInfo(transData):
    output = (c_char *1024)()
    result = dll.GetExtraInfo(0,1,output)

    writeLogString("OCT","GETEXTRAINFO:"+str(result))
    writeOCTLogString("GetExtraInfo",str(result)+",0,1,"+output.value.decode("utf-8"))

    if result == 0:
        transData["LAST_ADD"] = output.value.decode("utf-8")
    else:
        packResponseCode(result,transData)
        return result

def settleOCT():
    output = (c_char * 1024)()
    result = dll.XFile(output)

    writeLogString("OCT","SETTLE:"+str(result))
    writeLogString("OCT","SETTLE FILE:"+str(output.value))
    writeOCTLogString("XFile",str(result)+","+str(output.value))

    return result

def __RMS_Redeem_Check(totalAmt,netAmt):
    result = dll.RMS_RedeemCheck(totalAmt,netAmt)

    writeLogString("OCT","REDEEM CHECK:"+str(result))
    writeOCTLogString("RMS_RedeemCheck",str(result)+","+str(totalAmt)+","+str(netAmt))

    return result

def initSubsidy():
    result = dll.InitSubsidyList()

    writeLogString("OCT","SUBSIDY INIT:"+str(result))
    writeOCTLogString("InitSubsidyList",str(result))

    return result

def __CollectSubsidy(int_ecr,list_subsidy):
    output = (c_char * 1024)()
    result = dll.CollectSubsidy(int_ecr,output)

    list_subsidy.append(result)
    if result < 100000:
        for x in range(0,20,4):
            b1 = int.from_bytes(output[x],'big')
            b2 = int.from_bytes(output[x+1],'big')
            b3 = int.from_bytes(output[x+2],'big')
            b4 = int.from_bytes(output[x+3],'big')
            y = 0
            y = (y|b4)<<8
            y = (y|b3)<<8
            y = (y|b2)<<8
            y = (y|b1)

            list_subsidy.append(str(y))

        for x in list_subsidy:
            writeLogString("OCT","COLLECTSUBSIDY:"+str(x))
        
        writeOCTLogString("CollectSubsidy",str(result)+","+list_subsidy[1]+","+list_subsidy[2]+","+list_subsidy[3]+","+list_subsidy[4]+","+list_subsidy[5]+",")
    else:
        writeOCTLogString("CollectSubsidy",str(result))
    return list_subsidy

#For Retry
def RMS_Update(cmd, timeInterval , transData):
    for x in range(0,timeInterval):
        result = dll.RMS_Update(cmd)
        writeOCTLogString("RMS_Update",str(result))
        # completed
        if result < 100000:
            writeLogString("OCT","RMS UPDATE:"+str(result))
            UD_List = []
            __getInstantUD(UD_List)
            __GetExtraInfo(transData)
            transData["CMD"] = "SALE"
            formatTransDataOctopus(UD_List,transData)
            packResponseCode(result,transData)
            return result
        elif result != 100032:
            writeLogString("OCT","RMS UPDATE:"+str(result))
            packResponseCode(result,transData)
            return result
        time.sleep(1)
    else:
        writeLogString("OCT","RMS UPDATE:"+str(result))
        packResponseCode(result,transData)
        return result

def membershipOCT(transData,printOut):
    result = polling("DUMMY",transData,2)
    if result >= 100000:
        packResponseCode(result,transData)
    writeLogString("OCT","MEMBERSHIP:"+str(result))
    return result

#No poll
def topUpRetry(timeInterval,transData,printOut):
    result = topUpForRetry(transData["ECRREF"],"TOPUP",inputAmountStringToLongOCT(transData["AMT"]),timeInterval,transData)
    return result

#No poll
def subsidyRetry(timeInterval,transData,printOut):
    result = topUpForRetry(transData["ECRREF"],"SUBSIDY",0,timeInterval,transData)
    return result
