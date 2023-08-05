#Provide Unified API in here
from .qrcode import saleQR,voidSaleQR,refundQR,retrievalQR,checkTypeQR,setReceiptLang
from .terminal import openPortTerminal, closePortTerminal,saleTerminal,refundTerminal,voidSaleTerminal,retrievalTerminal,membershipTerminal
from .terminalUtils import formatTransReceiptTerminal
from .Octopus import openOCTCom,closeOCTCom,polling,getDeviceInfo,topUp,settleOCT,saleOCT,initSubsidy,RMS_Update,membershipOCT,topUpRetry,subsidyRetry
from .OctopusUtils import formatTransReceiptOctopus,packRespMsg
from .generalUtils import *
from .logUtils import *
from .project_dict_and_list import *
import pkg_resources


class UnifiedAPI():
	props = {}

	#Default Constructor
	def __init__(self):
		#get all the properties in the file
		with open("eftsolutions.properties", "r") as f:
				l = f.read()
		f.close()
		prop_list = l.split("\n")

		for item in prop_list:
			try:
				item_list = item.split("=")
				self.props[item_list[0]] = item_list[1]
			except:
				#empty line caused exception
				pass
		#Set the log file path
		if "LogLocation" in self.props:
			setLogPath(self.props["LogLocation"])
			writeLogString("API","API VERSION:"+str(pkg_resources.require("unified_api_pkg")[0].version))
			writeLogDictionary("PROPERTIES",self.props)
		
	#Dictonary for transData,List for printOut
	def SaleQR(self,payment_type, qr_code, ecr_ref, amount, additional_amount,transData,printOut):
		printOut.clear()

		writeLogString("SALEQR INPUT","TYPE:"+payment_type+"||"+"QR:"+qr_code+"||"+"ECR:"+ecr_ref+"||"+"AMT:"+str(amount))

		amount = inputAmountStringToLong(amount)

		writeLogString("SALEQR","CONVERTED AMT:"+str(amount))

		result = saleQR(qr_code,ecr_ref,amount,transData,printOut,self.props)

		writeLogString("SALEQR RETURN",str(result))
		writeLogDictionary("SALEQR RESPONSE DATA",transData)
		writeLogReceipt(printOut)

		return result

	def Sale(self,payment_type,ecr_ref,amount,additional_amount,payment_option,transData,printOut):
		printOut.clear()

		writeLogString("SALE INPUT","TYPE:"+payment_type+"||"+"ECR:"+ecr_ref+"||"+"AMT:"+str(amount)+"||"+"ADD AMT:"+str(additional_amount)+"||"+"OPTION:"+payment_option)

		amount = inputAmountStringToLong(amount)
		additional_amount = inputAmountStringToLong(additional_amount)

		writeLogString("SALE","CONVERTED AMT:"+str(amount))

		if payment_type == "EDC" or payment_type == "UPI" or payment_type == "EPS":
			result = saleTerminal(payment_type,ecr_ref,amount,additional_amount,payment_option,transData,printOut,self.props)

			isInt = False

			try:
				#Integer is approve in EDC or online transaction in EPS (print receipt when online)
				int(result)
				isInt = True
			except:
				isInt = False


			if result == "000" or (isInt and payment_type == "EPS"):
				formatTransReceiptTerminal(transData,printOut,self.props)

			writeLogString("SALE RETURN",str(result))
			writeLogDictionary("SALE RESPONSE DATA",transData)
			writeLogReceipt(printOut)
			return result

		elif payment_type == "OCT" or payment_type == "OCT_REWARDS":
			result = saleOCT(payment_type,ecr_ref,amount,additional_amount,payment_option,transData,printOut)

			if result < 100000:
				formatTransReceiptOctopus(transData,printOut,self.props,payment_option)
			
			packRespMsg(self.props["DisplayLanguage"],transData)
			writeLogString("SALE RETURN",str(result))
			writeLogDictionary("SALE RESPONSE DATA",transData)
			writeLogReceipt(printOut)

			return result

		else:
			transData["RESP"] = "A12"
			packAPIReject(transData,"A12",self.props["DisplayLanguage"])
			return transData["RESP"]

	def Void(self,payment_type,invoice,originalECRREF,transData,printOut):
		printOut.clear()

		writeLogString("VOID INPUT","TYPE:"+payment_type+"||"+"INVOICE:"+str(invoice)+"||"+"ORIECR:"+originalECRREF)

		if payment_type == "QR":
			result = voidSaleQR(invoice,transData,printOut,self.props)

			writeLogString("VOID RETURN",str(result))
			writeLogDictionary("VOID RESPONSE DATA",transData)
			writeLogReceipt(printOut)
			
			return result

		elif payment_type == "EDC" or payment_type == "UPI" or payment_type == "VAC":
			result = voidSaleTerminal(payment_type,invoice,originalECRREF,transData,printOut,self.props)

			if result == "000":
				formatTransReceiptTerminal(transData,printOut,self.props)
			
			writeLogString("VOID RETURN",str(result))
			writeLogDictionary("VOID RESPONSE DATA",transData)
			writeLogReceipt(printOut)

			return result
		else:
			transData["RESP"] = "A12"
			packAPIReject(transData,"A12",self.props["DisplayLanguage"])
			return transData["RESP"]
			
	def Refund(self,payment_type,ecr_ref,amount,originalTransRef,transData,printOut):
		printOut.clear()

		writeLogString("REFUND INPUT","TYPE:"+payment_type+"||"+"ECR:"+ecr_ref+"||"+"AMT:"+str(amount)+"||"+"ORI TRANS REF:"+str(originalTransRef))

		amount = inputAmountStringToLong(amount)

		writeLogString("REFUND","CONVERTED AMT:"+str(amount))

		if payment_type == "QR":
			result = refundQR(ecr_ref,amount,originalTransRef,transData,printOut,self.props)

			writeLogString("REFUND RETURN",str(result))
			writeLogDictionary("REFUND RESPONSE DATA",transData)
			writeLogReceipt(printOut)

			return result
		elif payment_type == "EDC":
			result = refundTerminal(payment_type,ecr_ref,amount,transData,printOut,self.props)

			if result == "000":
				formatTransReceiptTerminal(transData,printOut,self.props)

			writeLogString("REFUND RETURN",str(result))
			writeLogDictionary("REFUND RESPONSE DATA",transData)
			writeLogReceipt(printOut)

			return result
		else:
			transData["RESP"] = "A12"
			packAPIReject(transData,"A12",self.props["DisplayLanguage"])
			return transData["RESP"]

	def Retrieval(self,payment_type,invoice,ecr_ref,transData,printOut):
		printOut.clear()

		writeLogString("RETRIV INPUT","TYPE:"+payment_type+"||"+"INVOICE:"+invoice+"||"+"ECRREF:"+ecr_ref)

		if payment_type == "QR":
			result = retrievalQR(invoice,ecr_ref,transData,printOut,self.props)

			writeLogString("RETRIV RETURN",str(result))
			writeLogDictionary("RETRIV RESPONSE DATA",transData)
			writeLogReceipt(printOut)

			return result
		elif payment_type == "EDC" or payment_type == "EPS":
			result = retrievalTerminal(payment_type,invoice,transData,printOut,self.props)

			if result == "000":
				formatTransReceiptTerminal(transData,printOut,self.props)

			writeLogString("RETRIV RETURN",str(result))
			writeLogDictionary("RETRIV RESPONSE DATA",transData)
			writeLogReceipt(printOut)

			return result
		else:
			transData["RESP"] = "A12"
			packAPIReject(transData,"A12",self.props["DisplayLanguage"])
			return transData["RESP"]
	
	def Membership(self,payment_type,ecr_ref,option,amount,ciamID,transData,printOut):
		printOut.clear()

		writeLogString("MEMBER INPUT","TYPE:"+payment_type+"||"+"ECRREF:"+ecr_ref+"||"+"OPTION:"+option+"||"+"AMT:"+str(amount)+"||"+"ciamID:"+ciamID+"||")

		amount = inputAmountStringToLong(amount)

		writeLogString("MEMBER","CONVERTED AMT:"+str(amount))

		if payment_type == "EDC" or payment_type == "VAC":
			result = membershipTerminal(payment_type,ecr_ref,option,amount,ciamID,transData,printOut,self.props)

			writeLogString("MEMBER RETURN",str(result))
			writeLogDictionary("MEMBER RESPONSE DATA",transData)
			writeLogReceipt(printOut)

			return result
		elif payment_type == "OCT" or payment_type == "OCT_REWARDS":
			result = membershipOCT(transData,printOut)
			packRespMsg(self.props["DisplayLanguage"],transData)
			writeLogString("MEMBER RETURN",str(result))
			writeLogDictionary("MEMBER RESPONSE DATA",transData)
			writeLogReceipt(printOut)

			return result
		else:
			transData["RESP"] = "A12"
			packAPIReject(transData,"A12",self.props["DisplayLanguage"])
			return transData["RESP"]

	def CardEnquiry(self,payment_type,option,transData,printOut):
		printOut.clear()

		writeLogString("CARD ENQ INPUT","TYPE:"+payment_type+"||"+"OPTION:"+option)

		if payment_type == "OCT" or payment_type == "OCT_REWARDS":
			result = polling(option,transData,2)
			packRespMsg(self.props["DisplayLanguage"],transData)

			writeLogString("CARD ENQ RETURN",str(result))
			writeLogDictionary("CARD ENQ RESPONSE DATA",transData)
			
			return result
		else:
			transData["RESP"] = "A12"
			packAPIReject(transData,"A12",self.props["DisplayLanguage"])
			return transData["RESP"]

	def QRCodeEnquiry(self,payment_type,option,qrCode,transData,printOut):

		writeLogString("QR ENQ INPUT","TYPE:"+payment_type+"||"+"OPTION:"+option +"||"+"QR:"+qrCode)

		result = checkTypeQR(qrCode,transData)

		writeLogString("QR ENQ RETURN",str(result))
		writeLogDictionary("QR ENQ RESPONSE DATA",transData)

		return result

	def TopUp(self,payment_type,ecr_ref,Type,amount,transData,printOut):
		printOut.clear()
		writeLogString("TOPUP INPUT","TYPE:"+payment_type+"||"+"ECR REF:"+ecr_ref+"||"+"AMT:"+str(amount)+"||"+"TYPE:"+Type)
		amount = inputAmountStringToLongOCT(amount)
		writeLogString("TOPUP","CONVERTED AMT:"+str(amount))

		if payment_type == "OCT" or payment_type == "OCT_REWARDS":
			result = topUp(ecr_ref,Type,amount,transData)
			if result <100000:
				formatTransReceiptOctopus(transData,printOut,self.props,Type)
			packRespMsg(self.props["DisplayLanguage"],transData)

			writeLogString("TOPUP RETURN",str(result))
			writeLogDictionary("TOPUP RESPONSE DATA",transData)
			writeLogReceipt(printOut)
			return result
		else:
			transData["RESP"] = "A12"
			packAPIReject(transData,"A12",self.props["DisplayLanguage"])
			return transData["RESP"]

	def Settlement(self,payment_type,batchesData,printOut):
		#printOut.clear()

		writeLogString("SETTLE INPUT","TYPE:"+payment_type)

		if payment_type == "OCT" or payment_type == "OCT_REWARDS":
			result = settleOCT()

			writeLogString("SETTLE RETURN",str(result))

			return result
		else:
			batchesData["RESP"] = "A12"
			packAPIReject(batchesData,"A12",self.props["DisplayLanguage"])
			return batchesData["RESP"]

	def OpenEDCCom(self):
		model = 0
		if self.props["EdcModel"] == "PAX_S60":
			model = 2
		elif self.props["EdcModel"] == "SPECTRA_T300":
			model = 1
		else:
			model = 0
		result = openPortTerminal(self.props["EdcCom"],self.props["LogLocation"],model,self.props["EdcComTimeout"])

		writeLogString("OPEN EDC PORT RETURN",str(result))

		return result

	def CloseEDCCom(self):
		result = closePortTerminal()
		writeLogString("CLOSE EDC PORT RETURN",str(result))
		return result
	
	def OpenOCTCom(self):
		result = openOCTCom(self.props["OctCom"],self.props["OctOutletID"],self.props["OctPollTimeOut"])
		#101015 is RMS INIT failed. It can still do payment, but no RMS function
		if result == 0 or result == 101015:
			result = getDeviceInfo()
			self.props["OCTTID"] = result[1]
			self.props["OCTMID"] = result[2]

		writeLogString("OPEN OCT PORT RETURN",str(result))

		return result

	def CloseOCTCom(self):
		result = closeOCTCom()

		writeLogString("CLOSE OCT PORT RETURN",str(result))
		return result

	def InitTransportSubsidy(self,transData):
		result = initSubsidy()
		writeLogString("INIT SUBSIDY RETURN",str(result))
		transData["RESP"] = result
		transData["REMINBAL"] = 0 #for packRespMsg use
		packRespMsg(self.props["DisplayLanguage"],transData)
		return result
	
	def OctRetry(self, cmd, timeInterval,transData, printOut):
		writeLogString("OCTRETRY INPUT","CMD:"+str(cmd)+"||"+"TimeInterval:"+str(timeInterval))
		writeLogDictionary("OCTRETRY INPUT",transData)

		if "CMD" in transData:
			if transData["CMD"] == "TOPUP" and transData["AMT"] > 0:
				result = topUpRetry(timeInterval,transData,printOut)
			elif transData["CMD"] == "TOPUP" and transData["AMT"] == 0:
				result = subsidyRetry(timeInterval,transData,printOut)
			else:
				result = RMS_Update(cmd,timeInterval,transData)

			if result < 100000:
				formatTransReceiptOctopus(transData,printOut,self.props,"")
				packRespMsg(self.props["DisplayLanguage"],transData)
			# elif result == 100022:
			# 	#Special Case: pack 2 times
			# 	if self.props["language"] == "E":
			# 		transData["RESPMSG"] = transData["RESPMSG"] + "\nPlease Tap card no.:" + transData["PAN"]
			# 	else:
			# 		transData["RESPMSG"] = transData["RESPMSG"] + "\n請拍卡號:" + transData["PAN"]
			else:
				packRespMsg(self.props["DisplayLanguage"],transData)
				#Special Case: pack 2 times
				if self.props["language"] == "E":
					transData["RESPMSG"] = transData["RESPMSG"] + "\nRetry please (Octopus no. {0}".format(transData["PAN"])
				else:
					transData["RESPMSG"] = transData["RESPMSG"] + "\n請重試(八達通號碼 {0})".format(transData["PAN"])

			writeLogString("OCTRETRY RETURN",str(result))
			writeLogDictionary("OCTRETRY RESPONSE DATA",transData)	
			writeLogReceipt(printOut)

			return result
		else:
			transData["RESP"] = "A12"
			packAPIReject(transData,"A12",self.props["DisplayLanguage"])
			return transData["RESP"]

	def UpdateConfig(self, propName, value):
		if propName in self.props:
			self.props[propName] = value
			#qr receipt need specific set via dll
			if propName == "language":
				if value == "C" or value == "c":
					setReceiptLang(True)
				else:
					setReceiptLang(False)
			return True
		else:
			return False