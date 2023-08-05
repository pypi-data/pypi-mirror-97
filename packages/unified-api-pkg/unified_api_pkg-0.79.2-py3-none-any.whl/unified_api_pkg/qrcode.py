import clr
import json
clr.AddReference("System.Collections")
clr.AddReference(r"paymentQR")

from System.Collections import ArrayList
from System import String
from .paymentQR import TransRecord
from .paymentQR import paymentQRAPI
from .project_dict_and_list import *

qrAPI=paymentQRAPI(38,18)
testdata = TransRecord()
arraylist = ArrayList()
result = -1

def __packRespMsg(result, transData, displayLanguage):
    if displayLanguage == 'E':
        if result in QR_ENGLISH_MAP:
            transData["RESPMSG"] = QR_ENGLISH_MAP[result]
        else:
            transData["RESPMSG"] = UNKNOWN_ERROR_ENGLISH
    else:
        if result in QR_CHINESE_MAP:
            transData["RESPMSG"] = QR_CHINESE_MAP[result]
        else:
            transData["RESPMSG"] = UNKNOWN_ERROR_CHINESE

def saleQR(code, ecrRef, amount, transData, stringList,props):
    result = qrAPI.SaleQR(code,ecrRef,amount,testdata,arraylist)
    jsonString = testdata.toJSONString()
    tempDict = json.loads(jsonString)
    for val in tempDict:
        transData[val] = tempDict[val]
    for val in arraylist:
        stringList.append(val)
    __packRespMsg(result,transData,props["DisplayLanguage"])
    return result

def voidSaleQR(invoice,transData,stringList,props):
    result = qrAPI.Void(invoice,"",testdata,arraylist)
    jsonString = testdata.toJSONString()
    tempDict = json.loads(jsonString)

    for val in tempDict:
        transData[val] = tempDict[val]
    for val in arraylist:
        stringList.append(val)
    __packRespMsg(result,transData,props["DisplayLanguage"])
    return result

def refundQR(EcrRef,Amount,originalData,transData,stringList,props):
    if "QRTYPE" in originalData and "APPV" in originalData and "REFNUM" in originalData:
        oriDataString = originalData["QRTYPE"]+originalData["APPV"]+originalData["REFNUM"]
    else:
        transData["RESP"] = "A12"
        if props["DisplayLanguage"] == 'E':
            transData["RESPMSG"] = API_ENGLISH_MAP["A12"]
        else:
            transData["RESPMSG"] = API_CHINESE_MAP["A12"]
        return transData["RESP"]
    result = qrAPI.Refund(EcrRef,Amount,oriDataString,testdata,arraylist)
    jsonString = testdata.toJSONString()
    tempDict = json.loads(jsonString)
    for val in tempDict:
        transData[val] = tempDict[val]
    for val in arraylist:
        stringList.append(val)
    
    __packRespMsg(result,transData,props["DisplayLanguage"])
    return result

def retrievalQR(invoice,ecrRef,transData,stringList,props):
    result = qrAPI.Retrieval(invoice,ecrRef,testdata,arraylist)
    jsonString = testdata.toJSONString()
    tempDict = json.loads(jsonString)
    for val in tempDict:
        transData[val] = tempDict[val]
    for val in arraylist:
        stringList.append(val)
    __packRespMsg(result,transData,props["DisplayLanguage"])
    return result
	
def checkTypeQR(qr_code,transData):
    result = qrAPI.GetQRType(qr_code)

    transData["CMD"] = "ENQ"
    transData["TYPE"] = "QR"
    transData["PAN"] = qr_code
    transData["RESP"] = result
    if result < 0:
        transData["RESPMSG"] = "INVALID CODE"
        transData['STATUS'] = "ERROR"
    else:
        transData["RESPMSG"] = "APPROVED"
        transData["STATUS"] = "APPROVED"
        transData["CARD"] = QR_TYPE_LIST[result]

    return result
        
def setReceiptLang(isChineseOnly):
    qrAPI.setlang(isChineseOnly)