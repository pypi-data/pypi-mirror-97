from decimal import Decimal

#2 decimal place int
def inputAmountStringToLong(amount):
    amount = "{:.2f}".format(float(amount))
    amount = Decimal(amount) * Decimal('100')
    return int(amount)

#1 decimal place int
def inputAmountStringToLongOCT(amount):
    amount = "{:.1f}".format(float(amount))
    amount = Decimal(amount) * Decimal('10')
    return int(amount)

#Unsigned int to signed int
def unsignedIntToRealValue(value):
    isPositive = 1
    bit = "{0:016b}".format(value)
    if bit[0:1] == "1":
        isPositive = -1
    else:
        #if positive value, no need to check
        isPositive = 1
        return value
        
    not_bit = ""
    for x in range(0,len(bit)):
        if bit[x] == "1":
            not_bit += "0"
        else:
            not_bit += "1"
    
    signed_value = int(not_bit,2) + 1
    signed_value = signed_value * isPositive
    return signed_value

def decimalTypeToInt(value):
    list_d = str(value).split('.')

    if len(list_d) == 2:
        exponent = -len(list_d[1])
        integer = int(list_d[0] + list_d[1])
    else:
        str_dec = list_d[0].rstrip('0')
        exponent = len(list_d[0]) - len(str_dec)
        integer = int(str_dec)
    
    return integer

def formatDateTimeInReceipt(isDate,content):
    if isDate:
        #using date format "/"
        return content[0:4] + "/" + content[4:6] + "/" + content[6:]
    else:
        #using time format ":"
        return content[0:2] + ":" + content[2:4] + ":" + content[4:]

#Maximum character per line = 38 
#1 chinese = 2 English/number

LINE_LENGTH = 38
HALF_LINE_LENGTH = 18


#bilingu 2 column  
def mix_2_column_b(column1_header_chinese,column1_header_english,value1,column2_header_chinese,column2_header_english,value2):
    finial_content = ""
    col_content = column1_header_chinese + " " + column1_header_english
    length = len(column1_header_chinese)*2 + 1 + len(column1_header_english)
    space = HALF_LINE_LENGTH - length - len(value1)

    finial_content = col_content + " "*space + value1 +"  "

    col_content = column2_header_chinese + " " + column2_header_english
    length = len(column2_header_chinese)*2 + 1 + len(column2_header_english)
    space = HALF_LINE_LENGTH - length - len(value2)

    finial_content = finial_content + col_content + " "*space + value2

    return finial_content

#Chinese only, 2 column
def mix_2_column_c(column1_header_chinese,value1,column2_header_chinese,value2):
    finial_content = ""
    col_content = column1_header_chinese
    length = len(column1_header_chinese)*2
    space = HALF_LINE_LENGTH - length - len(value1)

    finial_content = col_content + " "*space + value1 +"  "

    col_content = column2_header_chinese
    length = len(column2_header_chinese)*2
    space = HALF_LINE_LENGTH - length - len(value2)

    finial_content = finial_content + col_content + " "*space + value2

    return finial_content
#English only, 2 column
def mix_2_column_e(column1_header_english,value1,column2_header_english,value2):
    finial_content = ""
    col_content = column1_header_english
    length = len(column1_header_english)
    space = HALF_LINE_LENGTH - length - len(value1)

    finial_content = col_content + " "*space + value1 +"  "

    col_content = column2_header_english
    length = len(column2_header_english)
    space = HALF_LINE_LENGTH - length - len(value2)

    finial_content = finial_content + col_content + " "*space + value2

    return finial_content

#bilingu 1 column
def mix_1_column_b(header_chinese,header_english,value):
    finial_content = ""
    col_content = header_chinese + " " + header_english
    length = len(header_chinese)*2 + 1 + len(header_english)
    space = LINE_LENGTH - length - len(value)
    finial_content = col_content + " "*space + value

    return finial_content

#English header , 1 column
def mix_1_column_e(header_english,value):
    finial_content = ""
    length = len(header_english)
    space = LINE_LENGTH - length - len(value)
    finial_content = header_english + " "*space + value

    return finial_content

#Rewards$ header
#Chinese header , 1 column
def mix_1_column_c(header_chinese,value):
    finial_content = ""
    #-1 for '$'
    length = len(header_chinese) * 2 - 1 
    space = LINE_LENGTH - length - len(value)
    finial_content = header_chinese + " "*space + value

    return finial_content

#Pure Chinese header
#Chinese header , 1 column
def mix_1_column_c2(header_chinese,value):
    finial_content = ""

    length = len(header_chinese) * 2
    space = LINE_LENGTH - length - len(value)
    finial_content = header_chinese + " "*space + value

    return finial_content

#Print at middle, Chinese or English only
def print_at_middle_ce(content,isEnglish):
    content_length = 0
    line_length = 0 
    if isEnglish:
        content_length = len(content)
        line_length = LINE_LENGTH
    else:
        content_length = len(content) * 2
        line_length = LINE_LENGTH
    
    space = (int)((line_length - content_length) / 2)
    
    return " "*space + content + " "*space

#Print at middle, bilingual
def print_at_middle_b(content_chinese,content_english):
    content_length = len(content_chinese)*2 + 1 + len(content_english)

    content = content_chinese + " " + content_english
    space = int((LINE_LENGTH - content_length) / 2)

    return " "*space + content + " "*space
        

#Print at both end, not chinese
def print_at_both_end(content1,content2):
    content_length = len(content1) + len(content2)

    space = LINE_LENGTH - content_length

    return content1 + " "*space + content2

#Print 2 column, switch
def mix_2_column(column1_header_chinese,column1_header_english,value1,column2_header_chinese,column2_header_english,value2,languageType,printOut):
    if languageType == "C" or languageType == "c":
        printOut.append( mix_2_column_c(column1_header_chinese,value1,column2_header_chinese,value2))
    if languageType == "E" or languageType == "e":
        printOut.append( mix_2_column_e(column1_header_english,value1,column2_header_english,value2))
    if languageType == "B" or languageType == "b":
        printOut.append( mix_1_column_b( column1_header_chinese,column1_header_english,value1 ))
        printOut.append( mix_1_column_b( column2_header_chinese,column2_header_english,value2 ))

#Print 1 column, switch
def mix_1_column(header_chinese,header_english,value,languageType,printOut):
    if languageType == "C" or languageType == "c":
        printOut.append( mix_1_column_c2(header_chinese,value))
    if languageType == "E" or languageType == "e":
        printOut.append( mix_1_column_e(header_english,value))
    if languageType == "B" or languageType == "b":
        printOut.append( mix_1_column_b( header_chinese,header_english,value))

#Print at middle switch
def print_at_middle(content_chinese,content_english,languageType,printOut):
    if languageType == "C" or languageType == "c":
        printOut.append( print_at_middle_ce(content_chinese,False))
    if languageType == "E" or languageType == "e":
        printOut.append( print_at_middle_ce(content_english,True))
    if languageType == "B" or languageType == "b":
        printOut.append( print_at_middle_ce(content_chinese,False))
        printOut.append( print_at_middle_ce(content_english,True))