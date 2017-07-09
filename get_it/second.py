from browser import document,alert, window, html
import re
import json
import sys
from browser import timer
from browser.html import TABLE, TR, TH, TD



with open('../data/error.txt') as json_file:
    data = json.load(json_file)
mainstack = list()
maintoken = list()
mainJson = {}
toggle = False
mainepxr = ""
numberr = ""
index = 0
_timer = 0
tablerow = 0
__firstTime = 0
variable_store = dict()
builtin_functions_list = ['False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield','abs','ascii','bin','bool','chr','float','hex','id','input','len','max','min','oct','ord','print','round','sorted','str','sum','type','sqrt','tan','cos','sin','cos','ceil','floor','random','seed','randint', 'True', 'False', 'and', 'or', 'not', 'notTrue', 'notFalse','int','float','str']
memoryAddress = ["0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100"]


def isOp(c):
    if c != "": return (c in "%+-*/**==!=<=><>=andor")
    else: return False

def isOpCheck(c):
	if c != '':
		return c in '%+-*/**==!=<=><>=andor()-('
	else:
		return False


def pri(c):  # operator priority
	if c in 'andor':
		return 0
	if c in '==!=<=<>>=':
		return 1
	if c in '+':
		return 2
	if c in '-':
		return 3
	if c in '%':
		return 4
	if c in '*':
		return 5
	if c in '/':
		return 6
	if c in '**':
		return 7

def isNum(c):
	if c != '':
		if str(c) == "False":
			return True
		elif str(c) == "True":
			return True
		if str(c) == "not False":
		    return True
		elif str(c) == "not True":
		    return True
		elif c.replace('.', '', 1).lstrip('-').isdigit():
			return True
	else:
		return  False

def isNum1(c):
	if c != '':
		if c.replace('.', '', 1).lstrip('-').isdigit():
		   return True
	else:
		 return  False

def addTolist(num1,op,num2):
	if num1 == "True":
		num1 = True
	elif num1 == "False":
		num1 = False
	if num2 == "True":
		num2 = True
	elif num2 == "False":
		num2 = False
	temp1 = False
	temp2 = False
	temp3 = False
	temp4 = False
	#conversion of bool values if any in the expresssion while execution
	if num1 == True:
		num1 = "1"
		temp1 = True
	elif num1 == False:
		num1= "0"
		temp2 = True
	if num2 == True:
		num2 = "1"
		temp3 = True
	elif num2 == False:
		num2= "0"
		temp4 = True
	  #end
	#conversion of string to int or float
	if num1.lstrip('-').isdigit():
		num1 = int(num1)
	else:
		num1 = float(num1)
	if num2.lstrip('-').isdigit():
		num2 = int(num2)
	else:
		num2 = float(num2)
	#end
	#population token array which has infix Evaluation results
	if op == "/" and num2 == 0:
		temp = "0"
	else:
		temp = str(eval(str(num1) + op + str(num2)))
		if temp =="inf":
			raise SyntaxError(data["experssionErrorInf"])
	#a = np.int16(temp)
	#print(a)
	   #changing binary 0 and 1 to bool value True and False
	if temp1:
		num1 = True
	elif temp2:
		num1 = False
	if temp3:
		num2 = True
	elif temp4:
		num2 = False
	   #end

	maintoken.append(str(num1))
	maintoken.append(str(op))
	maintoken.append(str(num2))
	if temp.lstrip('-').isdigit():
	   maintoken.append(str(temp))
	else:
	   maintoken.append(str(round(float(temp),2)))
	#print(maintoken[-1]);
	return maintoken[-1]

def addTolistRel(num1,op,num2):
	if num1 == "not True":
		temp1 = 0
	elif num1 == "not False":
		temp1 = 1
	else:
		temp1 = num1
	if num2 == "not True":
		temp2 = 0
	elif num2 == "not False":
		temp2 = 1
	else:
		temp2 = num2
	#print(op)
	if op == ">=" or op == "<=":
		if str(num1) in "TrueFalsenot Truenot False" and str(num2) in "TrueFalsenot Truenot False":
			raise SyntaxError(data["notintfloat"])
	maintoken.append(str(num1))
	maintoken.append(str(op))
	maintoken.append(str(num2))
	maintoken.append(eval(str(num1)+ " "+op+" " + str(num2)))
	#print(eval(str(num1)+ op + str(num2)))
	return maintoken[-1]

def mapnum(x):
	if isOpCheck(x):
		return x
	elif x.lstrip('-').isdigit():
		x = str(int(x))
		return x
	elif x == "True":
		x = "True"
		return x
	elif x == "False":
		x = "False"
		return x
	elif x == "not False":
		x = "not False"
		return x
	elif x == "not True":
		x = "not True"
		return x
	elif x.lstrip('-').isdigit() == False:
		x = str(float(x))
		return x

def calc(op, num1, num2, expres):
    if op == '+':
       return addTolist(num1,op,num2)
    if op == '-':
       return addTolist(num1,op,num2)
    if op == '*':
       return addTolist(num1,op,num2)
    if op == '/':
       return addTolist(num1,op,num2)
    if op == '**':
       return addTolist(num1,op,num2)
    if op == '<=':
       return addTolistRel(num1,op,num2)
    if op == '<':
		return addTolistRel(num1,op,num2)
    if op == '>':
       return addTolistRel(num1,op,num2)
    if op == '>=':
       return addTolistRel(num1,op,num2)
    if op == '==':
       return addTolistRel(num1,op,num2)
    if op == '!=':
       return addTolistRel(num1,op,num2)
    if op == '%':
       return addTolist(num1,op,num2)
    if op == 'and':
       return addTolistRel(num1,op,num2)
    if op == 'or':
       return addTolistRel(num1,op,num2)

def experssionErrorPar(token):
    openPar = 0
    closePar = 0
    for item in token:
        if item == "(" or item == "-(": openPar += 1
        elif item == ")" : closePar += 1
    if openPar != closePar:
          return True

def experssionErrorOperator(token):
    operand = 0
    operator = 0
    for item in token:
		if item == "True" or item == "-True" or item == "not True":
			operand += 1
		elif item == "False" or item == "-False" or item == "not False":
			operand += 1
		elif item.replace('.', '', 1).lstrip('-').isdigit(): operand += 1
		elif item in "+-*/**==!=<=><>=%andor" : operator += 1
    if operator != operand-1 : return True
    elif operator >= operand : return True

def experssionErrorOperand(token):
    for item in token:
		if not item in "-True-Falsenot Truenot False" :
			if not item.replace('.', '', 1).lstrip('-').isdigit():
			   if not item in "%+-*/**==!=<=><>=andor)(-(" :
				  return True

def experssionErrorEqual(token):
    for item in token:
        if item == "=" : return True


def spacerem(x):
	if x == "and" or x == "or":
		return str(" "+x+" ")
	else:
		return x


def Infix(token):
		maintoken = []
		orig = token
		# #print(orig)
		# #token = re.findall(r'and?|or?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|[a-z,A-Z,0-9,\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(expr.strip().split()))
		# token = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|[a-z,A-Z,0-9,\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(expr.strip().split()))
		# token = get_stored_variables(token)
		# #print(token)
		# temp = [x for x in token if isNum1(x)]
		# #if len(temp) == 1:
		# 	#evalNum = str(eval(''.join(token)))
		# 	#token = []
		# 	#token.append(evalNum)
		# print(token)
		# token = list_validate(token)
		if token[0] == "-":
			if not token[1] == "(":
				token[0] = str(eval(str(token[0] + token[1])))
				token.pop(1)
			else:
				token[0] = str(token[0] + token[1])
				token.pop(1)
		for (index, tok) in enumerate(token, start=0):
			if tok == "not":
				if isNum1(token[index + 1]) or isOpCheck(token[index + 1]):
					raise SyntaxError(data["notintfloat"]);
		for (index, tok) in enumerate(token, start=0):
			if tok == '-' or tok == 'not':
				if token[index-1] in '*-+/**==!=<=><>=%(-(':
					if token[index+1] in 'TrueFalse':
						token[index] = str(token[index] +" "+ token[index + 1])
						token.pop(index + 1)
					else:
						if token[index] == '-' and token[index + 1] == '(':
						    token[index] = str(token[index] + token[index + 1])
						else:
						    token[index] = str(eval(str(token[index] + token[index + 1])))
						#token[index] = str(token[index] + token[index + 1])
						token.pop(index + 1)
				elif token[index + 1] in 'TrueFalse':
					token[index] = str(token[index] +" "+ token[index + 1])
					token.pop(index + 1)
		#print(orig)
		#if 'not' in orig or 'true' in orig or 'True' or 'False' in orig:
			#eval(expression1[1])
		#print(token)
		# if experssionErrorPar(token):
		# 	raise SyntaxError(data["experssionErrorPar"])
		# if experssionErrorOperand(token):
		# 	raise SyntaxError(data["experssionErrorOperand"])
		# if experssionErrorOperator(token):
		# 	raise SyntaxError(data["experssionErrorOperator"])
		# if experssionErrorEqual(token):
		# 	raise SyntaxError(data["experssionErrorEqual"])
		#if 'not' in orig or 'true' in orig or 'True' or 'False' in orig:
			#eval(orig)
		token1 = list(map(mapnum,token))
		token2 = list(map(spacerem, token1))
		#document['textBox_0'].value =  document['textBox_0'].value.split("=")[0] + "= "+ ''.join(token2)
		expr = token1
		stackChr = list() # character stack
		stackNum = list() # number stack
		num = ""
		while len(expr) > 0:
			c = expr.pop(0)
			if len(expr) > 0: d = expr[0]
			else: d = ""
			if isNum(c):
				num = c
				if not isNum(d):
					stackNum.append(num)
					num = ""
			elif isOp(c):
				while True:
					if 'nan' in stackNum:
						document['errorCond'].text = ''
						document['errorCond'] <= 'false'
						document['myTextArea'] <= "\n>>> Equation cannot be calculated "
						document['myTextAreaHistory'] <= "\n>>> Equation cannot be calculated "
					if len(stackChr) > 0: top = stackChr[-1]
					else: top = ""
					if isOp(top):
						if not pri(c) > pri(top):
							num2 = stackNum.pop()
							op = stackChr.pop()
							num1 = stackNum.pop()
							stackNum.append(calc(op, num1, num2, expr))
						else:
							stackChr.append(c)
							break
					else:
						stackChr.append(c)

						break
			elif c == "(" or c == "-(":
				stackChr.append(c)
			elif c == ")":
				while len(stackChr) > 0:
					c = stackChr.pop()
					if c == "(":
						break
					elif c == "-(":
						#print("Stack "+stackNum[-1])
						#print(maintoken)
						#toggle = True
						#stackNum[-1] = str(eval("-"+str(stackNum[-1])))
						if len(maintoken) == 0:
							stackNum[-1] = str(eval("-"+str(stackNum[-1])))
						elif stackNum[-1] != maintoken[-1] :
							stackNum[-1] = str(eval("-"+str(stackNum[-1])))
						else:
							stackNum[-1] = str(eval("-"+str(stackNum[-1])))
							maintoken[-1] = str(eval(str(stackNum[-1])))
						break
					elif isOp(c):
						num2 = stackNum.pop()
						num1 = stackNum.pop()
						stackNum.append(calc(c, num1, num2, orig))

		while len(stackChr) > 0:
			c = stackChr.pop()
			if c == "(":
				break
			elif isOp(c):
				num2 = stackNum.pop()
				num1 = stackNum.pop()
				stackNum.append(calc(c, num1, num2, orig))
		return maintoken



def storing_values(name,value):
    variable_store.update({name:value})
    #print(variable_store)

def check_expression_execute_noerror(i):
    global mainJson
    code = document['programMemory'].value.split('\n')
    if mainJson['Details_with_linenum'][str(i)][0] == 'Assign':
        if mainJson['Details_with_linenum'][str(i)][1] == "Expression":
            # Initial setup for find different Expression ex:(a=-(-4)),a=-(int(4)),a=-(-(a)) , a=-(-int(a))
            token = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|[a-z,A-Z,0-9,\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(code[i-1].split('=')[1].strip().split()))
            token1 = set(token).union(set(['(', ')','+','-','*','**','/','%','>','<=','>=','<','==','!=','and','or','not']+builtin_functions_list))
            check = set(token1).symmetric_difference(set(['(', ')','+','-','*','**','/','%','>','<=','>=','<','==','!=','and','or','not']+builtin_functions_list))

            #This is for negation(UnaryOP) with only varibale names supports with or without in-bulit function example(-4,-(-4),int(-4),-int(-4))
            if len(list(check)) == 1:
                if str(list(check)[0]).replace('.', '', 1).lstrip('-').isdigit():
                    res = eval(code[i-1].split('=')[1])
                    storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res)
                    res1 = mainJson['Details_with_linenum'][str(i)]
                    res1[1] = 'UnaryOp'
                    replaceValue = res1+[str(code[i-1].split('=')[1]),str(res)]
                    mainJson['Details_with_linenum'].update({str(i):replaceValue})

                #This is for negation(UnaryOP) with only varibale names supports with or without in-bulit function example(-a,-(-a),int(-a),-int(-a))
                elif str(list(check)[0]) in [key for key in variable_store]:
                    Text_After_fetching = list(map(lambda x:x if str(list(check)[0]) != x else variable_store[str(list(check)[0])],token))
                    Text_After_fetching = ''.join(list(map(str,Text_After_fetching)))
                    data_mem_load_lis = [code[i-1].split('=')[1],Text_After_fetching]
                    res = eval(Text_After_fetching)
                    storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res)
                    res1 = mainJson['Details_with_linenum'][str(i)]
                    res1[1] = 'UnaryOp'
                    replaceValue = res1+data_mem_load_lis+[str(res)]
                    mainJson['Details_with_linenum'].update({str(i):replaceValue})
            else:
                #print(mainJson['Details_with_linenum'][str(i)][3],mainJson['Details_with_linenum'][str(i)][4])
                # This is Expression do not contain variable or function
                if not mainJson['Details_with_linenum'][str(i)][3] and not mainJson['Details_with_linenum'][str(i)][4]:
                    print(Infix(token))

                # This is Expression do not contain variable but contain functions
                elif not mainJson['Details_with_linenum'][str(i)][3] and mainJson['Details_with_linenum'][str(i)][3]:
                    pass

                # This is Expression do not contain functions but contain variables
                elif mainJson['Details_with_linenum'][str(i)][3] and not mainJson['Details_with_linenum'][str(i)][3]:
                    pass

                # This is Expression contain both functions and variables
                elif mainJson['Details_with_linenum'][str(i)][3] and not mainJson['Details_with_linenum'][str(i)][3]:
                    pass



        elif mainJson['Details_with_linenum'][str(i)][1] == "Num":
            storing_values(str(mainJson['Details_with_linenum'][str(i)][3]),mainJson['Details_with_linenum'][str(i)][2])
        elif mainJson['Details_with_linenum'][str(i)][1] == "Str":
            storing_values(str(mainJson['Details_with_linenum'][str(i)][3]),mainJson['Details_with_linenum'][str(i)][2])

    else:
        pass



def check_expression_execute_runtime(i):
    global mainJson
    code = document['programMemory'].value.split('\n')
    if mainJson['Details_with_linenum'][str(i)][1] == "Expression":
        if not '+/*%><==!=>=<=andor**' in code and ('0123456789' in code or 'notTruenotFalseTrueFalse' in code):
            res = eval(code[i-1].split('=')[1])
            res1 = mainJson["Details_with_linenum"][str(i)]
            res1[1] = 'UnaryOp'
            replaceValue = res1+[str(code[i-1].split('=')[1]),str(res)]
            storing_values(str(mainJson["Details_with_linenum"][str(i)][3]),mainJson['Details_with_linenum'][str(i)][2])
            mainJson['Details_with_linenum'].update({str(i):replaceValue})
            #print(mainJson)
        elif not '+/*%><==!=>=<=andor**' in code and (any(word in code for word in [key for key in variable_store]) or len(mainJson['Details_with_linenum'][str(i)][3])>0):
            print('Unary with variable or function or both')
    elif mainJson['Details_with_linenum'][str(i)][1] == "Num":
        storing_values(str(mainJson["Details_with_linenum"][str(i)][3]),mainJson["Details_with_linenum"][str(i)][2])
    elif mainJson['Details_with_linenum'][str(i)][1] == "Str":
        storing_values(str(mainJson["Details_with_linenum"][str(i)][3]),mainJson["Details_with_linenum"][str(i)][2])



def sequence_execute():
    global mainJson
    mainJson = json.loads(document['jsonValArray'].text)
    print(mainJson)
    if mainJson['error'] == '0':
        for i in mainJson['resData']:
            check_expression_execute_noerror(i)
    elif mainJson['error'] == '1':
        for i in mainJson['resData']:
            check_expression_execute_runtime(i)
