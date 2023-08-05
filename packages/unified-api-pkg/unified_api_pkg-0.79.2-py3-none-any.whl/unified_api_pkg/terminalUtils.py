from .generalUtils import *
from .project_dict_and_list import *

PAX_S60 = 2
SPECTRA_T300 = 1
LANDI_A8 = 0

def __packEPSResponseCodeMsg(respCode,transData,printOut,props):
    if props["DisplayLanguage"] == "E":
        #English display, in the table 
        if respCode in EPS_CHINESE_MAP:
            if respCode == "000":
                return
            else:
                printOut.append(print_at_middle_ce(EPS_CHINESE_MAP[transData["RESP"]],False))
                printOut.append(print_at_middle_ce(transData["RESPMSG"],True))
                #matched the resp code, return 
                return
        try:
            int_respCode = int(respCode)
            #check range
            if int_respCode >= 918 and int_respCode <= 959:
                printOut.append(print_at_middle_ce("請聯絡卡中心",False))
                printOut.append(print_at_middle_ce(transData["RESPMSG"],True))
                #Chinese + nextline + English
            elif int_respCode >= 960 and int_respCode <= 999:
                printOut.append(print_at_middle_ce("請聯絡銀行",False))
                printOut.append(print_at_middle_ce(transData["RESPMSG"],True))
                #Chinese + nextline + English
            else:
                printOut.append(print_at_middle_ce("其他原因",False))
                printOut.append(print_at_middle_ce(transData["RESPMSG"],True))
                #Chinese + nextline + English
        except:
            printOut.append(print_at_middle_ce("其他原因",False))
            printOut.append(print_at_middle_ce(transData["RESPMSG"],True))
            #Chinese + nextline + English
    else:
        if respCode in EPS_CHINESE_MAP:
            if respCode == "000":
                transData["RESPMSG"] = EPS_CHINESE_MAP[transData["RESP"]]
                return
            else:
                printOut.append(print_at_middle_ce(EPS_CHINESE_MAP[transData["RESP"]],False))
                printOut.append(print_at_middle_ce(transData["RESPMSG"],True))
                transData["RESPMSG"] = EPS_CHINESE_MAP[transData["RESP"]]
                #matched the resp code, return 
                return
        try:
            int_respCode = int(respCode)
            #check range
            if int_respCode >= 918 and int_respCode <= 959:
                printOut.append(print_at_middle_ce("請聯絡卡中心",False))
                printOut.append(print_at_middle_ce(transData["RESPMSG"],True))
                transData["RESPMSG"] = "請聯絡卡中心"

            elif int_respCode >= 960 and int_respCode <= 999:
                printOut.append(print_at_middle_ce("請聯絡銀行",False))
                printOut.append(print_at_middle_ce(transData["RESPMSG"],True))
                transData["RESPMSG"] = "請聯絡銀行"
            else:
                printOut.append(print_at_middle_ce("其他原因",False))
                printOut.append(print_at_middle_ce(transData["RESPMSG"],True))
                transData["RESPMSG"] = "其他原因"
        except:
            printOut.append(print_at_middle_ce("其他原因",False))
            printOut.append(print_at_middle_ce(transData["RESPMSG"],True))
            transData["RESPMSG"] = "其他原因"

def packEDCResponseMsg(respCode,transData,props):
    if props["DisplayLanguage"] == "C":
        if respCode in EDC_RESPONSE_CHINESE_MAP:
            transData["RESPMSG"] = EDC_RESPONSE_CHINESE_MAP[respCode]
        elif respCode in API_CHINESE_MAP:
            transData["RESPMSG"] = API_CHINESE_MAP[respCode]
        else:
            transData["RESPMSG"] = '交易失敗'
    else:
        if respCode in EDC_RESPONSE_ENGLISH_MAP:
            transData["RESPMSG"] = EDC_RESPONSE_ENGLISH_MAP[respCode]
        elif respCode in API_ENGLISH_MAP:
            transData["RESPMSG"] = API_ENGLISH_MAP[respCode]
        else:
            transData["RESPMSG"] = 'TRANS REJECTED'
        
        
def __add_minus(cmd):
    if cmd == "VOID" or cmd == "REFUND":
        return "-"
    else:
        return ""

#Pack transData
def formatTransDataTerminal(rawData,transData,modelType):
    if modelType == PAX_S60:
        #CMD and TYPE
        if rawData[0:1] == "0":
            transData["CMD"] = "SALE"
            transData["TYPE"] = "EDC"
        elif rawData[0:1] == "2":
            transData["CMD"] = "REFUND"
            transData["TYPE"] = "EDC"
        elif rawData[0:1] == "3":
            transData["CMD"] = "VOID"
            transData["TYPE"] = "EDC"
        elif rawData[0:1] == "4":
            transData["CMD"] = "RETRIEVAL"
            transData["TYPE"] = "EDC"
        elif rawData[0:1] == "5":
            transData["CMD"] = "SALE"
            transData["TYPE"] = "EPS"
        elif rawData[0:1] == "6":
            transData["CMD"] = "RETRIEVAL"
            transData["TYPE"] = "EPS"
        elif rawData[0:1] == "@":
            transData["CMD"] = "SALE"
            transData["TYPE"] = "UPI"
        elif rawData[0:1] == "A":
            transData["CMD"] = "VOID"
            transData["TYPE"] = "UPI"
        elif rawData[0:1] == "D":
            transData["CMD"] = "RETRIEVAL"
            transData["TYPE"] = "UPI"
        elif rawData[0:1] == "I" or rawData[0:1] == "J" or rawData[0:1] == "K":
            transData["CMD"] = "MEMBER"
            transData["TYPE"] = "EDC"
        elif rawData[0:1] == "P":
            transData["CMD"] = "MEMBER"
            transData["TYPE"] = "VAC"
        elif rawData[0:1] == "Q":
            transData["CMD"] = "VOID"
            transData["TYPE"] = "VAC"

        
        #discard the MessageType
        rawData = rawData[1:]
        if transData["TYPE"] == "EDC":
            if transData["CMD"] != "MEMBER":
                transData["RESP"] = rawData[0:3]
                rawData = rawData[3:]
                transData["RESPMSG"] = rawData[0:20]
                rawData = rawData[20:]
                #ignore 1 byte original trans type
                rawData = rawData[1:]
                transData["ECRREF"] = rawData[0:16]
                rawData = rawData[16:]
                try:
                    transData["AMT"] = float(rawData[0:12])/100
                    rawData = rawData[12:]
                    transData["TIPS"] = float(rawData[0:12])/100
                    rawData = rawData[12:]
                except:
                    transData["AMT"] = 0.00
                    transData["TIPS"] = 0.00
                    rawData = rawData[12:]
                    rawData = rawData[12:]

                transData["DATE"] = rawData[0:8]
                rawData = rawData[8:]
                transData["TIME"] = rawData[0:6]
                rawData = rawData[6:]
                transData["CARD"] = rawData[0:10]
                rawData = rawData[10:]
                transData["PAN"] = rawData[0:19]
                rawData = rawData[19:]
                transData["EXPDATE"] = rawData[0:4]
                rawData = rawData[4:]
                transData["TERMINALID"] = rawData[0:8]
                rawData = rawData[8:]
                transData["MERCHANTID"] = rawData[0:15]
                rawData = rawData[15:]
                transData["TRACE"] = rawData[0:6]
                transData["INVOICE"] = rawData[0:6]
                rawData = rawData[6:]
                transData["BATCHNO"] = rawData[0:6]
                rawData = rawData[6:]
                transData["APPCODE"] = rawData[0:6]
                rawData = rawData[6:]
                transData["REFNUM"] = rawData[0:12]
                rawData = rawData[12:]

                #DCC
                if rawData[0:3] != "   ":
                    transData["CURRCODE"] = rawData[0:3]
                    rawData = rawData[3:]
                    transData["FXRATE"] = float(rawData[1:8])/(10 ** int(rawData[0:1]))
                    rawData = rawData[8:]
                    transData["FOREIGNAMT"] = float(rawData[0:12])/100
                    rawData = rawData[12:]
                else:
                    rawData = rawData[3:]
                    rawData = rawData[8:]
                    rawData = rawData[12:]

                #Entry Mode
                transData["ENTRYMODE"] = rawData[0:1]
                rawData = rawData[1:]

                if transData["ENTRYMODE"] in SIGN_LIST:
                    transData["SIGNBLOCK"] = "N"
                else:
                    transData["SIGNBLOCK"] = "Y"

                #Loyalty
                #if the HASE is completely new. It may treat as normal card also. 
                if rawData[0:60] != "{:060d}".format(0) and rawData[0:60] != "".ljust(60):

                    #Cash Dollar
                    hsd_dict = {}

                    #enjoy Dollar
                    enjoy_dict = {}

                    enjoy_dict["REDEEMED"] = float(rawData[0:12])
                    rawData = rawData[12:]
                    hsd_dict["REDEEMED"] = float(rawData[0:12])
                    rawData = rawData[12:]

                    transData["NETAMT"] = float(rawData[0:12])/100
                    rawData = rawData[12:]
                    
                    enjoy_dict["BAL"] = float(rawData[0:12])
                    rawData = rawData[12:]
                    hsd_dict["BAL"] = float(rawData[0:12])
                    rawData = rawData[12:]

                    full_loy_dict = {
                        "HSD":hsd_dict,
                        "JDD":enjoy_dict
                    }
                    transData["LOYALTY"] = full_loy_dict
            else:
                #Membership function
                transData["RESP"] = rawData[0:3]
                rawData = rawData[3:]
                transData["RESPMSG"] = rawData[0:20]
                rawData = rawData[20:]
                transData["ECRREF"] = rawData[0:16]
                rawData = rawData[16:]
                transData["DATE"] = rawData[0:8]
                rawData = rawData[8:]
                transData["TIME"] = rawData[0:6]
                rawData = rawData[6:]
                transData["CARD"] = rawData[0:10]
                rawData = rawData[10:]
                transData["PAN"] = rawData[0:19]
                rawData = rawData[19:]
                transData["EXPDATE"] = rawData[0:4]
                rawData = rawData[4:]
                transData["TERMINALID"] = rawData[0:8]
                rawData = rawData[8:]
                transData["MERCHANTID"] = rawData[0:15]
                rawData = rawData[15:]
                transData["ENTRYMODE"] = rawData[0:1]
                rawData = rawData[1:]
                transData["CIAMID"] = rawData[0:20]
                rawData = rawData[20:]
                transData["PROGRAMID"] = rawData[0:20]
                rawData = rawData[20:]
                #ignore rest

        elif transData["TYPE"] == "EPS":
            transData["RESP"] = rawData[0:3]
            rawData = rawData[3:]
            transData["RESPMSG"] = rawData[0:20]
            rawData = rawData[20:]
            transData["ECRREF"] = rawData[0:16]
            rawData = rawData[16:]
            #ignore 12-digit total amount and 12-digit other amount
            rawData = rawData[12:]
            rawData = rawData[12:]
            transData["DATE"] = rawData[0:8]
            rawData = rawData[8:]
            transData["TIME"] = rawData[0:6]
            rawData = rawData[6:]
            transData["PAN"] = rawData[0:19]
            rawData = rawData[19:]
            transData["TERMINALID"] = rawData[0:8]
            rawData = rawData[8:]
            transData["MERCHANTID"] = rawData[0:15]
            rawData = rawData[15:]
            transData["TRACE"] = rawData[0:6]
            transData["INVOICE"] = rawData[0:6]
            rawData = rawData[6:]
            transData["BANKINVALUEDAY"] = rawData[0:4]
            rawData = rawData[4:]

            #Avoid 0x00 string
            if rawData[0:28] == '\x00'*28:
                transData["DEBITACCOUNTNO"] = ""
            else:
                transData["DEBITACCOUNTNO"] = rawData[0:28]
            rawData = rawData[28:]
            
            if rawData[0:20] == '\x00'*20:
                transData["BANKADDITIONALRESP"] = ""
            else:
                transData["BANKADDITIONALRESP"] = rawData[0:20]
            rawData = rawData[20:]

            transData["CARD"] = rawData[0:10]
            rawData = rawData[10:]
            #ignore 3-digit brand name
            rawData = rawData[3:]
            #ignore 6-digit billing currency
            rawData = rawData[6:]
            try:
                transData["AMT"] = float(rawData[0:12])/100
                rawData = rawData[12:]
                transData["CASHBACKAMT"] = float(rawData[0:12])/100
                rawData = rawData[12:]
            except:
                transData["AMT"] = 0.00
                transData["CASHBACKAMT"] = 0.00
                rawData = rawData[12:]
                rawData = rawData[12:]            
            transData["ACINDICATOR"] = rawData[0:3]
            rawData = rawData[3:]
            transData["REFNUM"] = rawData[0:6]
            rawData = rawData[6:]
            transData["SIGNBLOCK"] = "N"
            #ignore the Filler

        elif transData["TYPE"] == "UPI":
            transData["RESP"] = rawData[0:3]
            rawData = rawData[3:]
            transData["RESPMSG"] = rawData[0:20]
            rawData = rawData[20:]
            #ignore 1 byte original trans type
            rawData = rawData[1:]
            transData["ECRREF"] = rawData[0:16]
            rawData = rawData[16:]
            try:
                transData["AMT"] = float(rawData[0:12])/100
                rawData = rawData[12:]
                rawData = rawData[12:]
            except:
                transData["AMT"] = 0.00
                rawData = rawData[12:]
                rawData = rawData[12:]
            transData["DATE"] = rawData[0:8]
            rawData = rawData[8:]
            transData["TIME"] = rawData[0:6]
            rawData = rawData[6:]
            transData["CARD"] = rawData[0:10]
            rawData = rawData[10:]
            transData["PAN"] = rawData[0:19]
            rawData = rawData[19:]
            transData["EXPDATE"] = rawData[0:4]
            rawData = rawData[4:]
            transData["TERMINALID"] = rawData[0:8]
            rawData = rawData[8:]
            transData["MERCHANTID"] = rawData[0:15]
            rawData = rawData[15:]
            transData["TRACE"] = rawData[0:6]
            transData["INVOICE"] = rawData[0:6]
            rawData = rawData[6:]
            transData["BATCHNO"] = rawData[0:6]
            rawData = rawData[6:]
            transData["APPCODE"] = rawData[0:6]
            rawData = rawData[6:]
            transData["REFNUM"] = rawData[0:12]
            rawData = rawData[12:]
            transData["SIGNBLOCK"] = rawData[0:1]

            #"U" is default value, no meaning
            transData["ENTRYMODE"] = "U"

            #ignore the rest      
        elif transData["TYPE"] == "VAC":
            transData["RESP"] = rawData[0:3]
            rawData = rawData[3:]
            transData["RESPMSG"] = rawData[0:20]
            rawData = rawData[20:]
            #ignore 1 byte original trans type
            rawData = rawData[1:]
            transData["ECRREF"] = rawData[0:16]
            rawData = rawData[16:]
            try:
                transData["AMT"] = float(rawData[0:12])/100
                rawData = rawData[12:]
                rawData = rawData[12:]
            except:
                transData["AMT"] = 0.00
                rawData = rawData[12:]
                rawData = rawData[12:]

            transData["DATE"] = rawData[0:8]
            rawData = rawData[8:]
            transData["TIME"] = rawData[0:6]
            rawData = rawData[6:]
            transData["CARD"] = rawData[0:10]
            rawData = rawData[10:]
            transData["PAN"] = rawData[0:19]
            rawData = rawData[19:]
            transData["EXPDATE"] = rawData[0:4]
            rawData = rawData[4:]
            transData["TERMINALID"] = rawData[0:8]
            rawData = rawData[8:]
            transData["MERCHANTID"] = rawData[0:15]
            rawData = rawData[15:]
            transData["TRACE"] = rawData[0:6]
            transData["INVOICE"] = rawData[0:6]
            rawData = rawData[6:]
            transData["BATCHNO"] = rawData[0:6]
            rawData = rawData[6:]
            transData["APPCODE"] = rawData[0:6]
            rawData = rawData[6:]
            transData["REFNUM"] = rawData[0:12]
            rawData = rawData[12:]
            try:
                transData["VACBALANCE"] = float(rawData[0:12])/100
                rawData = rawData[12:]
            except:
                transData["VACBALANCE"] = 0.00
                rawData = rawData[12:]
            transData["VACEXPDATE"] = rawData[0:8]
            rawData = rawData[8:]
            #ignore the rest

#Pack receipt
def formatTransReceiptTerminal(transData,printOut,props):
    if transData["TYPE"] == "EDC" or transData["TYPE"] == "UPI" or transData["TYPE"] == "VAC":
        #Anfield should not has receipt
        if (transData["TYPE"] != "EDC" or transData["TYPE"] != "MEMBER"):
            print_at_middle(EDC_RECEIPT_MAP[transData["CMD"]],transData["CMD"],props["language"],printOut)

            printOut.append("")

            mix_2_column(
                EDC_RECEIPT_MAP["DATE"],
                "DATE",
                formatDateTimeInReceipt(True,transData["DATE"]),
                EDC_RECEIPT_MAP["TIME"],
                "TIME",
                formatDateTimeInReceipt(False,transData["TIME"]),
                props["language"],
                printOut
            )
            
            mix_2_column(
                EDC_RECEIPT_MAP["BATCH"],
                "BATCH",
                transData["BATCHNO"],
                EDC_RECEIPT_MAP["TRACE"],
                "TRACE",
                transData["TRACE"],
                props["language"],
                printOut
            )

            mix_1_column(EDC_RECEIPT_MAP["MID"],"MID",transData["MERCHANTID"],props["language"],printOut)
            mix_1_column(EDC_RECEIPT_MAP["TID"],"TID",transData["TERMINALID"],props["language"],printOut)
            mix_1_column(EDC_RECEIPT_MAP["PAN"],"PAN",transData["PAN"] + " " + transData["ENTRYMODE"],props["language"],printOut)
            mix_1_column(EDC_RECEIPT_MAP["EXPDATE"],"EXPDATE",transData["EXPDATE"][0:2] + "/"+ transData["EXPDATE"][2:4],props["language"],printOut)
            printOut.append(transData["CARD"][2:])
            mix_1_column(EDC_RECEIPT_MAP["APPCODE"],"APPCODE",transData["APPCODE"],props["language"],printOut)
            mix_1_column(EDC_RECEIPT_MAP["REFNUM"],"REFNUM",transData["REFNUM"],props["language"],printOut)
            mix_1_column("","ECRREF",transData["ECRREF"],"E",printOut)
            printOut.append("")            

            if "LOYALTY" in transData:
                mix_1_column(EDC_RECEIPT_MAP["TOTAL"],"TOTAL",props["region"]+" "+__add_minus(transData["CMD"])+'%.2f' % transData["AMT"],props["language"],printOut)
                loy = transData["LOYALTY"]
                for looping in loy:
                    dollar = loy[looping]
                    mix_1_column("",HASE_LOYALTY_MAP[looping],props["region"]+" "+__add_minus(transData["CMD"])+'%.2f' % dollar["REDEEMED"],"E",printOut)
                printOut.append("-"*LINE_LENGTH)
                mix_1_column(EDC_RECEIPT_MAP["NET"],"NET",props["region"]+" "+__add_minus(transData["CMD"])+'%.2f' % transData["NETAMT"],props["language"],printOut)
                
                if transData["CMD"] == "SALE":
                    printOut.append("")
                    printOut.append("")

                    printOut.append(" "*32 + "BAL")
                    for looping in loy:
                        dollar = loy[looping]
                        printOut.append(mix_1_column_e(HASE_LOYALTY_MAP[looping],'%.2f' % dollar["BAL"]))
            elif "CURRCODE" in transData:
                #DCC section
                printOut.append("FX RATE: "+ str(transData["FXRATE"]))
                printOut.append(print_at_middle_b(EDC_RECEIPT_MAP["TOTAL"],"TOTAL"))
                printOut.append(print_at_both_end("HKD []",DCC_CURR_CODE_MAP[transData["CURRCODE"]]+" [X]"))
                printOut.append(print_at_both_end(str(transData["AMT"]),str(transData["FOREIGNAMT"])))
            else:
                #normal section
                mix_1_column(EDC_RECEIPT_MAP["TOTAL"],"TOTAL",props["region"]+" "+__add_minus(transData["CMD"])+'%.2f' % transData["AMT"],props["language"],printOut)

    elif transData["TYPE"] == "EPS":
        if transData["RESP"] == "000":
            #approve transaction
            printOut.append(EDC_RECEIPT_MAP[transData["CMD"]] +" "+ transData["CMD"])
            printOut.append("")
            
            mix_2_column(
                EDC_RECEIPT_MAP["DATE"],
                "DATE",
                formatDateTimeInReceipt(True,transData["DATE"]),
                EDC_RECEIPT_MAP["TIME"],
                "TIME",
                formatDateTimeInReceipt(False,transData["TIME"]),
                props["language"],
                printOut
            )

            mix_1_column(EDC_RECEIPT_MAP["MID"],"MID",transData["MERCHANTID"],props["language"],printOut)
            mix_1_column(EDC_RECEIPT_MAP["TID"],"TID",transData["TERMINALID"],props["language"],printOut)
            mix_1_column(EDC_RECEIPT_MAP["PAN"],"PAN",transData["PAN"],props["language"],printOut)

            mix_1_column("","ISN",transData["TRACE"],"E",printOut)
            mix_1_column("","A/C",transData["DEBITACCOUNTNO"],"E",printOut)
            mix_1_column("","A/C INDICATOR",transData["ACINDICATOR"],"E",printOut)
            mix_1_column("","PURCHASE",props["region"]+" "+str(transData["AMT"]),"E",printOut)
            mix_1_column("","CASHBACK",props["region"]+" "+str(transData["CASHBACKAMT"]),"E",printOut)
            printOut.append("-"*LINE_LENGTH)
            mix_1_column("","TOTAL",props["region"]+" "+str(transData["AMT"]+transData["CASHBACKAMT"]),"E",printOut)

            printOut.append("")
            #need to test pure chinese position
            printOut.append("*"*LINE_LENGTH)
            printOut.append("")

            printOut.append(print_at_middle_ce(EDC_RECEIPT_MAP["ACCEPTED"],False))
            printOut.append(print_at_middle_ce("ACCEPTED",True))
            printOut.append("")
            printOut.append("*"*LINE_LENGTH)

            #this will only override the RESPMSG, 000 will return as once
            __packEPSResponseCodeMsg(transData["RESP"],transData,printOut,props)

            if "BANKADDITIONALRESP" in transData and transData["BANKADDITIONALRESP"]:
                printOut.append("")
                printOut.append(print_at_middle_ce(transData["BANKADDITIONALRESP"],True))

        elif "E" in transData["RESP"]:
            #internal reject
            #nothing to print
            printOut.append("")
        else:
            #online reject
            printOut.append("X"*LINE_LENGTH)
            printOut.append("X"*LINE_LENGTH)

            printOut.append(print_at_middle_ce(EDC_RECEIPT_MAP["REJECTED"],False))
            printOut.append(print_at_middle_ce("REJECTED",True))

            printOut.append("X"*LINE_LENGTH)
            printOut.append("X"*LINE_LENGTH)

            printOut.append(EDC_RECEIPT_MAP[transData["CMD"]] +" "+ transData["CMD"])
            printOut.append("")

            mix_2_column(
                EDC_RECEIPT_MAP["DATE"],
                "DATE",
                formatDateTimeInReceipt(True,transData["DATE"]),
                EDC_RECEIPT_MAP["TIME"],
                "TIME",
                formatDateTimeInReceipt(False,transData["TIME"]),
                props["language"],
                printOut
            )

            mix_1_column(EDC_RECEIPT_MAP["MID"],"MID",transData["MERCHANTID"],props["language"],printOut)
            mix_1_column(EDC_RECEIPT_MAP["TID"],"TID",transData["TERMINALID"],props["language"],printOut)
            mix_1_column(EDC_RECEIPT_MAP["PAN"],"PAN",transData["PAN"],props["language"],printOut)
            mix_1_column("","ISN",transData["TRACE"],"E",printOut)
            mix_1_column("","A/C",transData["DEBITACCOUNTNO"],"E",printOut)
            mix_1_column("","A/C INDICATOR",transData["ACINDICATOR"],"E",printOut)
            mix_1_column("","TOTAL",props["region"]+" "+str(transData["AMT"]+transData["CASHBACKAMT"]),"E",printOut)


            printOut.append("")
            #Print the Reason
            __packEPSResponseCodeMsg(transData["RESP"],transData,printOut,props)

            if "BANKADDITIONALRESP" in transData and transData["BANKADDITIONALRESP"]:
                printOut.append("")
                printOut.append(print_at_middle_ce(transData["BANKADDITIONALRESP"],True))