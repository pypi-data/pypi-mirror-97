import clr
import json
import datetime
clr.AddReference("System.Collections")
clr.AddReference(r"EFTECRCOMDLL")

from .EFTECRCOMDLL import ComPortController
from .terminalUtils import *
from .generalUtils import *
from .logUtils import *
from .project_dict_and_list import *

comPort = None

modelType = 0

TxnTimeout = 120
def openPortTerminal(EdcCom,logPath,EdcType,TxnTimeOut):

    global comPort
    global modelType
    global TxnTimeout
    modelType = EdcType
    TxnTimeout = TxnTimeOut

    if comPort is None:
        comPort = ComPortController(True,logPath,EdcType)
    else:
        return "PF"
    Result = comPort.portOpen(EdcCom,0)

    writeLogString("TERMINAL","OPEN COM:"+str(Result))

    return Result

def closePortTerminal():
    Result = comPort.portClose()

    writeLogString("TERMINAL","CLOSE COM:"+str(Result))

    return Result

def __connection(request_cmd,TxnTimeout,transData,modelType,props):
    comPort.SerialClearBuffer()

    writeLogString("TERMINAL","REQUEST CMD:"+request_cmd)

    result = comPort.SerialWrite(request_cmd)

    writeLogString("TERMINAL","REQUEST SENT:"+str(result))

    if result:
        diff_txn_time = datetime.now()
        result = comPort.SerialRead(TxnTimeout)
        diff_txn_time = datetime.now() - diff_txn_time
        if result != None:
            formatTransDataTerminal(result,transData,modelType)
            packEDCResponseMsg(transData["RESP"],transData,props)
            writeLogString("TERMINAL","RESPONSE:"+result)

            return transData["RESP"]
        else:
            diff_in_second = diff_txn_time.total_seconds()
            if int(diff_in_second) < int(TxnTimeout):
                writeLogString("TERMINAL","POLLING NOT RECEIVED, COM DISCONNECTED")
                transData["RESP"] = "A14"
                packAPIReject(transData,"A14",props["DisplayLanguage"])
                return transData["RESP"]
            else:
                writeLogString("TERMINAL","RESPONSE: ECR TIMEOUT")
                transData["RESP"] = "A10"
                packAPIReject(transData,"A10",props["DisplayLanguage"])
                return transData["RESP"]
    else:
        writeLogString("TERMINAL","REQUEST TERMINAL FAILURE")
        transData["RESP"] = "A11"
        packAPIReject(transData,"A11",props["DisplayLanguage"])
        return transData["RESP"]

def saleTerminal(payment_type,ecr_ref,amount,additional_amount,payment_option,transData,printOut,props):
    request_cmd = ""
    if modelType == PAX_S60:
        if payment_type == "EDC":
            request_cmd += "0"
            if len(ecr_ref) > 16:
                request_cmd += ecr_ref[:16]
            else:
                request_cmd += ecr_ref.ljust(16)
            request_cmd += "{:012d}".format(amount)
            #6-digit VOID trace and 6-digit instal
            request_cmd += "000000000000"
            if payment_option == "NORMAL_REDEEM":
                request_cmd += "03"
            else:
                request_cmd += "00"
        elif payment_type == "EPS":
            total = amount + additional_amount
            request_cmd += "5"
            if len(ecr_ref) > 16:
                request_cmd += ecr_ref[:16]
            else:
                request_cmd += ecr_ref.ljust(16)
            request_cmd += "{:012d}".format(total)
            request_cmd += "000000000000"
            request_cmd += "000000"
            request_cmd += "EE"
            request_cmd += "{:012d}".format(amount)
            request_cmd += "{:012d}".format(additional_amount)
        elif payment_type == "UPI":
            request_cmd += "@"
            if len(ecr_ref) > 16:
                request_cmd += ecr_ref[:16]
            else:
                request_cmd += ecr_ref.ljust(16)
            request_cmd += "{:012d}".format(amount)
            request_cmd += "CU"
            request_cmd += "000000"

        return __connection(request_cmd,TxnTimeout,transData,modelType,props)
    else:
        writeLogString("TERMINAL","INVALID TERMINAL TYPE")
        transData["RESP"] = "A13"
        packAPIReject(transData,"A13",props["DisplayLanguage"])
        return transData["RESP"]

def refundTerminal(payment_type,ecr_ref,amount,transData,printOut,props):
    request_cmd = ""
    if modelType == PAX_S60:
        #PAX only EDC refund
        request_cmd += "2"
        if len(ecr_ref) > 16:
            request_cmd += ecr_ref[:16]
        else:
            request_cmd += ecr_ref.ljust(16)
        request_cmd += "{:012d}".format(amount)
        #6-digit VOID trace and 6-digit instal, 2-digit redeem
        request_cmd += "000000000000"
        request_cmd += "00"
        
        return __connection(request_cmd,TxnTimeout,transData,modelType,props)
    else:
        writeLogString("TERMINAL","INVALID TERMINAL TYPE")
        transData["RESP"] = "A13"
        packAPIReject(transData,"A13",props["DisplayLanguage"])
        return transData["RESP"]

def voidSaleTerminal(payment_type,invoice,originalECRREF,transData,printOut,props):
    request_cmd = ""
    if modelType == PAX_S60:
        if payment_type == "EDC":
            request_cmd += "3"

            #ECRREF is the search key
            if len(originalECRREF) > 16:
                request_cmd += originalECRREF[:16]
            else:
                request_cmd += originalECRREF.ljust(16)

            #Invoice and amount are dont-care
            request_cmd += "{:012d}".format(0)
            request_cmd += "{:06d}".format(int(invoice))

            #6-digit instal and redeem
            request_cmd += "000000"
            request_cmd += "00"

        elif payment_type == "UPI":
            request_cmd += "A"

            #ECRREF is the search key
            if len(originalECRREF) > 16:
                request_cmd += originalECRREF[:16]
            else:
                request_cmd += originalECRREF.ljust(16)

            # VOID amount cannot use $0.00
            request_cmd += "{:012d}".format(1)
            request_cmd += "CU"
            request_cmd += "{:06d}".format(int(invoice))
        elif payment_type == "VAC":
            request_cmd += "Q"
            #ECRREF is the search key
            if len(originalECRREF) > 16:
                request_cmd += originalECRREF[:16]
            else:
                request_cmd += originalECRREF.ljust(16)
            #Invoice and amount are dont-care
            request_cmd += "{:012d}".format(0)
            request_cmd += "{:06d}".format(int(invoice))

        return __connection(request_cmd,TxnTimeout,transData,modelType,props)
    else:
        writeLogString("TERMINAL","INVALID TERMINAL TYPE")
        transData["RESP"] = "A13"
        packAPIReject(transData,"A13",props["DisplayLanguage"])
        return transData["RESP"]

def retrievalTerminal(payment_type,invoice,transData,printOut,props):
    request_cmd = ""
    invoice_2_retrieve = 0
    try:
        invoice_2_retrieve = "{:06d}".format(int(invoice))
    except:
        invoice_2_retrieve = "******"

    if modelType == PAX_S60:
        if payment_type == "EDC":
            request_cmd += "4"
            request_cmd += invoice_2_retrieve
        elif payment_type == "UPI":
            request_cmd += "D"
            request_cmd += invoice_2_retrieve
        elif payment_type == "EPS":
            request_cmd += "6"
            request_cmd += invoice_2_retrieve

        return __connection(request_cmd,TxnTimeout,transData,modelType,props)
    else:
        writeLogString("TERMINAL","INVALID TERMINAL TYPE")
        transData["RESP"] = "A13"
        packAPIReject(transData,"A13",props["DisplayLanguage"])
        return transData["RESP"]

def membershipTerminal(payment_type,ecr_ref,option,amount,ciamID,transData,printOut,props):
    request_cmd = ""
    invoice_2_retrieve = 0
    try:
        invoice_2_retrieve = "{:06d}".format(int(ecr_ref))
    except:
        invoice_2_retrieve = "******"

    if modelType == PAX_S60:
        if payment_type == "EDC":
            if option == "MEMRET":
                request_cmd += "K"
                request_cmd += "******"
            else:
                if option == "MEMLINK":
                    request_cmd += "I"
                elif option == "MEMENQ":
                    request_cmd += "J"
                    
                if len(ecr_ref) > 16:
                    request_cmd += ecr_ref[:16]
                else:
                    request_cmd += ecr_ref.ljust(16)

                if len(ciamID) > 20:
                    request_cmd += ciamID[:20]
                else:
                    request_cmd += ciamID.ljust(20)
        elif payment_type == "VAC":
            request_cmd += "P"
            if len(ecr_ref) > 16:
                request_cmd += ecr_ref[:16]
            else:
                request_cmd += ecr_ref.ljust(16)
            request_cmd += "{:012d}".format(amount)
            request_cmd += "000000"

        return __connection(request_cmd,TxnTimeout,transData,modelType,props)
    else:
        writeLogString("TERMINAL","INVALID TERMINAL TYPE")
        transData["RESP"] = "A13"
        packAPIReject(transData,"A13",props["DisplayLanguage"])
        return transData["RESP"]


    
