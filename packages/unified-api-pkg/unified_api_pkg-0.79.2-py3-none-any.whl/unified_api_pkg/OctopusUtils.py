from datetime import datetime
from .generalUtils import *
from .project_dict_and_list import *

OCT_BASCI_TIMESTAMP = 946684800
UD_AUTO_TOPUP = 4

def packRespMsg(language,transData):
    if language == "E":
        if int(transData["RESP"]) < 100000:
            transData["STATUS"] = "APPROVE"
            transData["RESPMSG"] = "REMIND BALANCE: ${0}".format(transData["REMINBAL"])
        elif int(transData["RESP"]) in OCT_RESPONSE_ENGLISH_MAP:
            if int(transData["RESP"]) == 101005 or int(transData["RESP"]) == 1000222:
                transData["STATUS"] = "ERROR"
                transData["RESPMSG"] = OCT_RESPONSE_ENGLISH_MAP[transData["RESP"]].format(transData["PAN"])
            else:
                transData["STATUS"] = "ERROR"
                transData["RESPMSG"] = OCT_RESPONSE_ENGLISH_MAP[transData["RESP"]]
        else:
            transData["STATUS"] = "ERROR"
            transData["RESPMSG"] = "ERROR {0}".format(transData["RESP"])
    else:
        if int(transData["RESP"]) < 100000:
            transData["STATUS"] = "APPROVE"
            transData["RESPMSG"] = "餘額: ${0}".format(transData["REMINBAL"])
        elif int(transData["RESP"]) in OCT_RESPONSE_CHINESE_MAP:
            if int(transData["RESP"]) == 101005 or int(transData["RESP"]) == 1000222:
                transData["STATUS"] = "ERROR"
                transData["RESPMSG"] = OCT_RESPONSE_CHINESE_MAP[transData["RESP"]].format(transData["PAN"])
            else:
                transData["STATUS"] = "ERROR"
                transData["RESPMSG"] = OCT_RESPONSE_CHINESE_MAP[transData["RESP"]]
        else:
            transData["STATUS"] = "ERROR"
            transData["RESPMSG"] = "錯誤 {0}".format(transData["RESP"])

def ecrRefToBCDByte(input, ecrRef, isSale):

    #Standard checking

    length = len(ecrRef)
    #Spec required at least 4 digit ecr ref. add "0" if not enough
    if length < 4:
        if(length % 2) == 0:
            ecrRef = ecrRef + "0000"
        else:
            ecrRef = ecrRef + "00000"
            
    length = len(ecrRef)
    last_4 = str(ecrRef[(length-4):])

    if isSale:
        #Do Sale format
        #c_int buffer
        input[22] = int(last_4[0:1],16)<<12|int(last_4[1:2],16)<<8|int(last_4[2:3],16)<<4|int(last_4[3:4],16)
        input[23] = int(last_4[0:1],16)<<20|int(last_4[1:2],16)<<16|int(last_4[2:3],16)<<12|int(last_4[3:4],16)<<8

        
    else:
        #TopUp format

        #c_char buffer
        #1st byte of AI must be 0
        input[0] = 0

        input[1] = int(last_4[0:1],16)<<4|int(last_4[1:2],16)
        input[2] = int(last_4[2:3],16)<<4|int(last_4[3:4],16)
        
def packResponseCode(resp,transData):
    transData["RESP"]=resp
        
def __add_minus(cmd):
    if cmd == "TOPUP":
        return ""
    else:
        return "-"

def formatTransDataOctopus(UD_list,transData):
    idx = 0
    
    if len(UD_list) <= 0:
        return

    idx = 1
    for x in range(0,int(UD_list[0])):

        #Normal UD
        if int(UD_list[idx]) == 0:
            idx = idx + 1

            #Wellcome request remove auto topup UD. check at the beginning. skip if hit this type of UD
            #idx + 8 for going to next UD: 7 + 1
            if int(UD_list[idx+4]) == UD_AUTO_TOPUP:
                idx = idx + 8
                continue

            transData["CARD"] = "OCTOPUS"
            if "UDSN" not in transData:
                transData["UDSN"] = str(UD_list[idx])
            else:
                transData["UDSN"] = transData["UDSN"] + "|" + str(UD_list[idx])
            txn_datetime = datetime.fromtimestamp(OCT_BASCI_TIMESTAMP+int(UD_list[idx+1]))
            transData["DATE"] = txn_datetime.strftime("%Y%m%d")
            transData["TIME"] = txn_datetime.strftime("%H%M%S")
            
            transData["TXNSEQ"] = str(UD_list[idx+5])
            
            if "AMT" not in transData:
                transData["AMT"] = float(UD_list[idx+6])/10
            else:
                if transData["AMT"] < float(UD_list[idx+6])/10:
                    transData["AMT"] = float(UD_list[idx+6])/10

            
            #String to int -> signed int -> float
            transData["REMINBAL"] = float(  unsignedIntToRealValue( int(UD_list[idx+7]) ) )/10
            transData["RESP"] = str(unsignedIntToRealValue( int(UD_list[idx+7]) ))
            #Go though normal UD.
            idx = idx + 7

            #Next UD type
            idx = idx + 1
        
        #RMS UD
        elif int(UD_list[idx]) == 1:
            idx = idx + 1
            #the UD contain RMS information
            transData["CARD"] = "OCTOPUS"

            if "RDSN" not in transData:
                transData["RDSN"] = str(UD_list[idx])
            else:
                transData["RDSN"] = transData["RDSN"] + "|" + str(UD_list[idx])
            
            txn_datetime = datetime.fromtimestamp(OCT_BASCI_TIMESTAMP+int(UD_list[idx+1]))
            transData["DATE"] = txn_datetime.strftime("%Y%m%d")
            transData["TIME"] = txn_datetime.strftime("%H%M%S")

            if "RMSTXNSEQ" not in transData:
                transData["RMSTXNSEQ"] = str(UD_list[idx+6])
            else:
                transData["RMSTXNSEQ"] = transData["RMSTXNSEQ"] + "|" + str(UD_list[idx+6])

            if "AMT" not in transData:
                transData["AMT"] = float(UD_list[idx+8])/10
            else:
                if transData["AMT"] < float(UD_list[idx+8])/10:
                    transData["AMT"] = float(UD_list[idx+8])/10
            #Go though RMS UD
            idx = idx + 10

            #Next UD type
            idx = idx + 1

        #Subsidy UD
        elif int(UD_list[idx]) == 2:
            idx = idx + 1
            transData["CARD"] = "OCTOPUS"
            if "UDSN" not in transData:
                transData["UDSN"] = str(UD_list[idx])
            else:
                transData["UDSN"] = transData["UDSN"] + "|" + str(UD_list[idx])
            txn_datetime = datetime.fromtimestamp(OCT_BASCI_TIMESTAMP+int(UD_list[idx+1]))
            transData["DATE"] = txn_datetime.strftime("%Y%m%d")
            transData["TIME"] = txn_datetime.strftime("%H%M%S")

            transData["TXNSEQ"] = str(UD_list[idx+5])

            #Next UD type
            idx = idx + 1

def formatTransReceiptOctopus(transData,printOut,props,receiptType):

    if receiptType == "REDEEM_COMP" or receiptType == "ISSUE":
        #Partial Receipt
        printOut.append("")
        #if props["language"] == "C":
            #printOut.append(print_at_middle(OCT_CHINESE_MAP["R_TITLE"],False))
        #else:
            #printOut.append(print_at_middle("Octopus Rewards",True))
        print_at_middle(OCT_CHINESE_MAP["R_TITLE"],"Octopus Rewards",props["language"],printOut)

        #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["TID"],"Device no.",props["OCTTID"]))
        #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["OUTLET"],"Shop no.",props["OctOutletID"]))
        mix_1_column(OCT_CHINESE_MAP["TID"],"Device no.",props["OCTTID"],props["language"],printOut)
        mix_1_column(OCT_CHINESE_MAP["OUTLET"],"Shop no.",props["OctOutletID"],props["language"],printOut)

        #printOut.append(mix_2_column_b(OCT_CHINESE_MAP["TID"],"Device no.",props["OCTTID"],OCT_CHINESE_MAP["OUTLET"],"Shop no.",props["OUTLET"]))
        #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["PAN"],"Octopus no.",transData["PAN"]))
        #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["ECRREF"],"Receipt no.",transData["ECRREF"]))
        mix_1_column(OCT_CHINESE_MAP["PAN"],"Octopus no.",transData["PAN"],props["language"],printOut)
        mix_1_column(OCT_CHINESE_MAP["ECRREF"],"Receipt no.",transData["ECRREF"],props["language"],printOut)


        #Special Case, must ignore "B", Chinese header use old function
        if "R_REDEEMED" in transData:
            if props["language"] == "C" or props["language"] == "c" or props["language"] == "B" or props["language"] == "b":
                printOut.append(mix_1_column_c(OCT_CHINESE_MAP["REDEEMED"],"R$"+'%.1f' % transData["R_REDEEMED"]+__add_minus(transData["CMD"])))
                #mix_1_column(OCT_CHINESE_MAP["REDEEMED"],"","R$"+'%.1f' % transData["R_REDEEMED"]+__add_minus(transData["CMD"]),"C",printOut)
            else:
                #printOut.append(mix_1_column("Redeem Reward$","R$"+__add_minus(transData["CMD"])+'%.1f' % transData["R_REDEEMED"]))
                mix_1_column("","Redeem Reward$","R$"+'%.1f' % transData["R_REDEEMED"]+__add_minus(transData["CMD"]),"E",printOut)

        #Special Case, must ignore "B", Chinese header use old function
        if "R_EARN" in transData:
            if props["language"] == "C" or props["language"] == "c" or props["language"] == "B" or props["language"] == "b":
                printOut.append(mix_1_column_c(OCT_CHINESE_MAP["EARN"],"R$"+'%.1f' % transData["R_EARN"]))
                #mix_1_column(OCT_CHINESE_MAP["EARN"],"","R$"+'%.1f' % transData["R_EARN"],"C",printOut)
            else:
                #printOut.append(mix_1_column("Earn Reward$","R$"+'%.1f' % transData["R_EARN"]))
                mix_1_column("","Earn Reward$","R$"+'%.1f' % transData["R_EARN"],"E",printOut)

        #Special Case, must ignore "B", Chinese header use old function
        if "R_BALANCE" in transData:
            if props["language"] == "C" or props["language"] == "c" or props["language"] == "B" or props["language"] == "b":
                printOut.append(mix_1_column_c(OCT_CHINESE_MAP["R_BAL"],"R$"+'%.1f' % transData["R_BALANCE"]))
                #mix_1_column(OCT_CHINESE_MAP["R_BAL"],"","R$"+'%.1f' % transData["R_BALANCE"],"C",printOut)
            else:
                #printOut.append(mix_1_column("Reward$ Balance","R$"+'%.1f' % transData["R_BALANCE"]))
                mix_1_column("","Reward$ Balance","R$"+'%.1f' % transData["R_BALANCE"],"E",printOut)

    elif receiptType == "CHANGE":
        printOut.append("")
        #if props["language"] == "C":
            #printOut.append(print_at_middle(OCT_CHINESE_MAP["CHANGE_TITLE"],False))
        #else:
            #printOut.append(print_at_middle("Octopus Top Up with Change Service",True))
        print_at_middle(OCT_CHINESE_MAP["CHANGE_TITLE"],"Octopus Top Up with Change Service",props["language"],printOut)
    
        #printOut.append(mix_2_column_b(OCT_CHINESE_MAP["DATE"],"DATE",formatDateTimeInReceipt(True,transData["DATE"]),OCT_CHINESE_MAP["TIME"],"TIME",formatDateTimeInReceipt(False,transData["TIME"])))
        
        mix_2_column(
            OCT_CHINESE_MAP["DATE"],
            "DATE",
            formatDateTimeInReceipt(True,transData["DATE"]),
            OCT_CHINESE_MAP["TIME"],
            "TIME",
            formatDateTimeInReceipt(False,transData["TIME"]),
            props["language"],
            printOut
        )        
        
        #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["PAN"],"Octopus no.",transData["PAN"]))
        mix_1_column(OCT_CHINESE_MAP["PAN"],"Octopus no.",transData["PAN"],props["language"],printOut)

        #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["REMINBAL"],"Remaining value","$"+'%.1f' % transData["REMINBAL"]))
        mix_1_column(OCT_CHINESE_MAP["REMINBAL"],"Remaining value","$"+'%.1f' % transData["REMINBAL"],props["language"],printOut)

    else:
        #Normal receipt

        if receiptType == "" or receiptType == None:
            #Treat as normal sale, remove RMS info
            if "R_REDEEMED" in transData:
                transData.pop("R_REDEEMED")
            if "R_EARN" in transData:
                transData.pop("R_EARN")
            if "R_BALANCE" in transData:
                transData.pop("R_BALANCE")
            if "NETAMT" in transData:
                transData.pop("NETAMT")
            
        #printOut.append(OCT_CHINESE_MAP[transData["CMD"]])
        #printOut.append(OCT_ENGLISH_MAP[transData["CMD"]])
        print_at_middle(OCT_CHINESE_MAP[transData["CMD"]],OCT_ENGLISH_MAP[transData["CMD"]],props["language"],printOut)
        printOut.append("")

        #printOut.append(mix_2_column_b(OCT_CHINESE_MAP["DATE"],"DATE",formatDateTimeInReceipt(True,transData["DATE"]),OCT_CHINESE_MAP["TIME"],"TIME",formatDateTimeInReceipt(False,transData["TIME"])))
        mix_2_column(
            OCT_CHINESE_MAP["DATE"],
            "DATE",
            formatDateTimeInReceipt(True,transData["DATE"]),
            OCT_CHINESE_MAP["TIME"],
            "TIME",
            formatDateTimeInReceipt(False,transData["TIME"]),
            props["language"],
            printOut
        )          
        #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["MID"],"MID",props["OCTMID"]))
        #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["TID"],"Device no.",props["OCTTID"]))
        #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["OUTLET"],"Shop no.",props["OctOutletID"]))
        mix_1_column(OCT_CHINESE_MAP["TID"],"Device no.",props["OCTTID"],props["language"],printOut)
        mix_1_column(OCT_CHINESE_MAP["OUTLET"],"Shop no.",props["OctOutletID"],props["language"],printOut)

        #printOut.append(mix_2_column_b(OCT_CHINESE_MAP["TID"],"Device no.",props["OCTTID"],OCT_CHINESE_MAP["OUTLET"],"Shop no.",props["OUTLET"]))
        #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["PAN"],"Octopus no.",transData["PAN"]))
        #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["ECRREF"],"Receipt no.",transData["ECRREF"]))
        mix_1_column(OCT_CHINESE_MAP["PAN"],"Octopus no.",transData["PAN"],props["language"],printOut)
        mix_1_column(OCT_CHINESE_MAP["ECRREF"],"Receipt no.",transData["ECRREF"],props["language"],printOut)
        #printOut.append(transData["CARD"])
        printOut.append("")

        if transData["CMD"] == "TOPUP" and transData["AMT"] != 0:
            #normal add value
            #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["TOPUPVALUE"],"Add value amount",__add_minus(transData["CMD"])+"$"+'%.1f' % transData["AMT"]))
            mix_1_column(OCT_CHINESE_MAP["TOPUPVALUE"],"Add value amount",__add_minus(transData["CMD"])+"$"+'%.1f' % transData["AMT"],props["language"],printOut)

            if transData["OCTTYPE"] != str(1):
                #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["REMINBAL"],"Remaining value","$"+'%.1f' % transData["REMINBAL"]))
                mix_1_column(OCT_CHINESE_MAP["REMINBAL"],"Remaining value","$"+'%.1f' % transData["REMINBAL"],props["language"],printOut)
        elif transData["CMD"] == "SUBSIDY" and transData["AMT"] == 0:
            #transport subsidy
            #pass in CMD is SUBSIDY, change back to TOPUP after print receipt
            #ignore "B"
            transData["CMD"] = "TOPUP"       

            if props["language"] == "C" or props["language"] == "c" or props["language"] == "B" or props["language"] == "b":
                #printOut.append(mix_1_column_c2(OCT_CHINESE_MAP["SUB_AMT"],__add_minus(transData["CMD"])+"$"+'%.1f' % transData["SUBSIDY_COLLECT"]))
                mix_1_column(OCT_CHINESE_MAP["SUB_AMT"],"",__add_minus(transData["CMD"])+"$"+'%.1f' % transData["SUBSIDY_COLLECT"],"C",printOut)
            else:
                #printOut.append(mix_1_column(OCT_ENGLISH_MAP["SUB_AMT"],__add_minus(transData["CMD"])+"$"+'%.1f' % transData["SUBSIDY_COLLECT"]))
                mix_1_column("",OCT_ENGLISH_MAP["SUB_AMT"],__add_minus(transData["CMD"])+"$"+'%.1f' % transData["SUBSIDY_COLLECT"],"E",printOut)


            if transData["OCTTYPE"] != str(1):
                #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["REMINBAL"],"Remaining value","$"+'%.1f' % transData["REMINBAL"]))
                mix_1_column(OCT_CHINESE_MAP["REMINBAL"],"Remaining value","$"+'%.1f' % transData["REMINBAL"],props["language"],printOut)


            #ignore "B"
            if props["language"] == "C" or props["language"] == "c" or props["language"] == "B" or props["language"] == "b":
                #No subsidy collected
                if transData["SUBSIDY_COLLECT"] == 0:
                    printOut.append("")
                    printOut.append(OCT_CHINESE_MAP["NO_SUB1"])
                    printOut.append(OCT_CHINESE_MAP["NO_SUB2"])
                else:
                    if transData["SUBSIDY_REASON"] == 1:
                        printOut.append("")
                        printOut.append(OCT_CHINESE_MAP["MAX_SUB1"])
                        printOut.append(OCT_CHINESE_MAP["MAX_SUB2"]+"$"+str(transData["SUBSIDY_OUTSTAND"]))
                        printOut.append(OCT_CHINESE_MAP["MAX_SUB3"])
                        printOut.append(OCT_CHINESE_MAP["MAX_SUB4"])
                        printOut.append(OCT_CHINESE_MAP["MAX_SUB5"])
                    elif transData["SUBSIDY_REASON"] > 1:
                        printOut.append("")
                        printOut.append(OCT_CHINESE_MAP["REMAIN_SUB1"]+"$"+str(transData["SUBSIDY_OUTSTAND"]))
                        printOut.append(OCT_CHINESE_MAP["REMAIN_SUB2"])
                        printOut.append(OCT_CHINESE_MAP["REMAIN_SUB3"])
            else:
                if transData["SUBSIDY_COLLECT"] == 0:
                    printOut.append("")
                    printOut.append(OCT_ENGLISH_MAP["NO_SUB1"])
                    printOut.append(OCT_ENGLISH_MAP["NO_SUB2"])
                    printOut.append(OCT_ENGLISH_MAP["NO_SUB3"])
                else:
                    if transData["SUBSIDY_REASON"] == 1:
                        printOut.append("")
                        printOut.append(OCT_ENGLISH_MAP["MAX_SUB1"])
                        printOut.append(OCT_ENGLISH_MAP["MAX_SUB2"])
                        printOut.append(OCT_ENGLISH_MAP["MAX_SUB3"]+"$"+str(transData["SUBSIDY_OUTSTAND"]))
                        printOut.append(OCT_ENGLISH_MAP["MAX_SUB4"])
                        printOut.append(OCT_ENGLISH_MAP["MAX_SUB5"])
                        printOut.append(OCT_ENGLISH_MAP["MAX_SUB6"])
                        printOut.append(OCT_ENGLISH_MAP["MAX_SUB7"])  
                    elif transData["SUBSIDY_REASON"] > 1:
                        printOut.append("")
                        printOut.append(OCT_ENGLISH_MAP["REMAIN_SUB1"])
                        printOut.append(OCT_ENGLISH_MAP["REMAIN_SUB2"]+"$"+str(transData["SUBSIDY_OUTSTAND"]))
                        printOut.append(OCT_ENGLISH_MAP["REMAIN_SUB3"])
                        printOut.append(OCT_ENGLISH_MAP["REMAIN_SUB4"])
                        printOut.append(OCT_ENGLISH_MAP["REMAIN_SUB5"])
                        printOut.append(OCT_ENGLISH_MAP["REMAIN_SUB6"])
                        
        elif transData["CMD"] == "SALE":
            #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["TOTAL"],OCT_ENGLISH_MAP["TOTAL"],__add_minus(transData["CMD"])+"$"+'%.1f' % transData["AMT"]))
            mix_1_column(OCT_CHINESE_MAP["TOTAL"],OCT_ENGLISH_MAP["TOTAL"],__add_minus(transData["CMD"])+"$"+'%.1f' % transData["AMT"],props["language"],printOut)

            if "R_REDEEMED" in transData:
                if props["language"] == "C" or props["language"] == "c" or props["language"] == "B" or props["language"] == "b":
                    printOut.append(mix_1_column_c(OCT_CHINESE_MAP["REDEEMED"],"R$"+'%.1f' % transData["R_REDEEMED"]+__add_minus(transData["CMD"])))
                    #mix_1_column(OCT_CHINESE_MAP["REDEEMED"],"","R$"+'%.1f' % transData["R_REDEEMED"]+__add_minus(transData["CMD"]),"C",printOut)
                else:
                    #printOut.append(mix_1_column("Redeem Reward$","R$"+'%.1f' % transData["R_REDEEMED"]+__add_minus(transData["CMD"])))
                    mix_1_column("","Redeem Reward$","R$"+'%.1f' % transData["R_REDEEMED"]+__add_minus(transData["CMD"]),"E",printOut)
                printOut.append("-"*LINE_LENGTH)

                #Not required
                transData.pop("R_REDEEMED")

            if "NETAMT" in transData:
                #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["NET"],"NET",__add_minus(transData["CMD"])+"$"+'%.1f' % transData["NETAMT"]))
                mix_1_column(OCT_CHINESE_MAP["NET"],"NET",__add_minus(transData["CMD"])+"$"+'%.1f' % transData["NETAMT"],props["language"],printOut)

            if transData["OCTTYPE"] != str(1):
                #printOut.append(mix_1_column_b(OCT_CHINESE_MAP["REMINBAL"],"Remaining value","$"+'%.1f' % transData["REMINBAL"]))
                mix_1_column(OCT_CHINESE_MAP["REMINBAL"],"Remaining value","$"+'%.1f' % transData["REMINBAL"],props["language"],printOut)

            printOut.append("")

            if "LAST_ADD" in transData:
                list_last_topup = transData["LAST_ADD"].split(",")
                #transData.pop("LAST_ADD")
                if int(list_last_topup[1]) < 4:
                    if props["language"] == "C" or props["language"] == "c" or props["language"] == "B" or props["language"] == "b":
                        printOut.append("上一次於 "+ list_last_topup[0] +" "+ OCT_LAST_TOPUP_CHINESE_LIST[int(list_last_topup[1])])
                    else:
                        printOut.append("LAST ADD VALUE BY " + OCT_LAST_TOPUP_ENGLISH_LIST[int(list_last_topup[1])]+ " ON "+list_last_topup[0])
                    printOut.append("")
            #Special Case, must ignore "B", Chinese header use old function
            if "R_EARN" in transData:
                print_at_middle(OCT_CHINESE_MAP["R_TITLE"],"Octopus Rewards",props["language"],printOut)
                if props["language"] == "C" or props["language"] == "c" or props["language"] == "B" or props["language"] == "b":
                    printOut.append(mix_1_column_c(OCT_CHINESE_MAP["EARN"],"R$"+'%.1f' % transData["R_EARN"]))
                    #mix_1_column(OCT_CHINESE_MAP["EARN"],"","R$"+'%.1f' % transData["R_EARN"],"C",printOut)
                else:
                    #printOut.append(mix_1_column("Earn Reward$","R$"+'%.1f' % transData["R_EARN"]))
                    mix_1_column("","Earn Reward$","R$"+'%.1f' % transData["R_EARN"],"E",printOut)
                
            #Special Case, must ignore "B", Chinese header use old function
            if "R_BALANCE" in transData:
                if props["language"] == "C" or props["language"] == "c" or props["language"] == "B" or props["language"] == "b":
                    printOut.append(mix_1_column_c(OCT_CHINESE_MAP["R_BAL"],"R$"+'%.1f' % transData["R_BALANCE"]))
                    #mix_1_column(OCT_CHINESE_MAP["R_BAL"],"","R$"+'%.1f' % transData["R_BALANCE"],"C",printOut)
                else:
                    #printOut.append(mix_1_column("Reward$ Balance","R$"+'%.1f' % transData["R_BALANCE"]))
                    mix_1_column("","Reward$ Balance","R$"+'%.1f' % transData["R_BALANCE"],"E",printOut)

            # if "NON_REWARDS" in transData:
            #     transData.pop("NON_REWARDS")
            #     if props["language"] == "C" or props["language"] == "c" or props["language"] == "B" or props["language"] == "b":
            #         #printOut.append(print_at_middle(OCT_CHINESE_MAP["REG_R"],False))
            #         print_at_middle(OCT_CHINESE_MAP["REG_R"],"","C",printOut)
            #         printOut.append(print_at_middle_ce("www.octopusrewards.com.hk",True))
            #     else:
            #         #printOut.append(print_at_middle(OCT_ENGLISH_MAP["REG_R"],True))
            #         print_at_middle("",OCT_ENGLISH_MAP["REG_R"],"E",printOut)
            #         printOut.append(print_at_middle_ce("www.octopusrewards.com.hk",True))
