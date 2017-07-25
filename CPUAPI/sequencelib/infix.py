#!/usr/bin/python
# Infix Expression Evaluation

import re
import json
import ast
import sys
import traceback

maintoken = list()
toggle = False

with open('error.txt') as json_file:
    data = json.load(json_file)

builtin_functions_list = [ 'None', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield','abs','ascii','bin','bool','chr','float','hex','id','input','len','max','min','oct','ord','print','round','sorted','str','sum','type','sqrt','tan','cos','sin','cos','ceil','floor','random','seed','randint',  'and', 'or','int','float','str']

def builtin_func_list(token):
    add = []
    str1 = ""
    tot = 0
    flag = False
    for i in token:
        if i in builtin_functions_list and not flag:
            flag = True
            tot = tot + 1
            str1 = str1 + i
            continue


        if flag:
            if i == ")":
                tot = tot - 1
                str1 = str1 + i
            elif i == "(":
                tot = tot + 1
                str1 = str1 + i
            elif i != "int":
                str1 = str1 + i

            if tot == 1:
                flag = False
                add.append(str1)
                str1 = ""
                tot = 0
    return add



def isOp(c):
	if c != '':
		return c in ['%', '*', '+', '-', '/', '**', '==', '!=', '<=', '>', '<', '>=', 'and', 'or']
	else:
		return False

def isOpCheck(c):
	if c != '':
		return c in ['%', '*', '+', '-', '/', '**', '==', '!=', '<=', '>', '<', '>=', 'and', 'or','(',')','-(']
	else:
		return False


def pri(c):  # operator priority
	if c in ['and','or']:
	   return 0
	if c in ['==','!=','<','>','>=','<=']:
	   return 1
	if c in ['+','-']:
	   return 2
	if c == '%':
	   return 3
	if c == '*':
	   return 4
	if c == '/':
	   return 5
	if c == '**':
	   return 6

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
		elif not isOpCheck(c):
		   return True
	else:
		 return  False

def isNum1(c):
	if c != '':
		if c.replace('.', '', 1).lstrip('-').isdigit():
		   return True
	else:
		 return  False


def stringOperation(str1,op,str2):
    try:
        str1 = ast.literal_eval(str(str1))
        str2 = ast.literal_eval(str(str2))
    except:
        str1 = str1
        str2 = str2
    if op == "-":
        res = str1 - str2
        return "'"+str(res)+"'"
    elif op == "+":
        res = str1 + str2
        return "'"+str(res)+"'"
    elif op == "*":
        res = str1 * str2
        return "'"+str(res)+"'"
    elif op == "/":
        res = str1 / str2
        return "'"+str(res)+"'"
    elif op == "%":
        res = str1 % str2
        return "'"+str(res)+"'"
    elif op == "**":
        res = str1 % str2
        return "'"+str(res)+"'"
    elif op == ">":
        res = str1 > str2
        return str(res)
    elif op == "<":
        res = str1 < str2
        return str(res)
    elif op == ">=":
        res = str1 >= str2
        return str(res)
    elif op == "<=":
        res = str1 <= str2
        return str(res)
    elif op == "==":
        res = str1 == str2
        return str(res)
    elif op == "!=":
        res = str1 != str2
        return str(res)
    elif op == "and":
        res = str1 and str2
        return "'"+str(res)+"'"
    elif op == "or":
        res = str1 or str2
        return "'"+str(res)+"'"


def addTolist(num1,op,num2):
	global maintoken
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
	elif num1.replace('.', '', 1).lstrip('-').isdigit():
	   num1 = float(num1)

	if num2.lstrip('-').isdigit():
	   num2 = int(num2)
	elif num2.replace('.', '', 1).lstrip('-').isdigit():
	   num2 = float(num2)
	#end

	if isinstance(num1, (int, float)) and isinstance(num2, str):
		maintoken.append(str(num1))
		maintoken.append(str(op))
		maintoken.append(str(num2))
		temp_str = stringOperation(str(num1),op,str(num2))
		maintoken.append(str(temp_str))
		return maintoken[-1]
	elif isinstance(num1, str) and isinstance(num2, (int,float)):
		maintoken.append(str(num1))
		maintoken.append(str(op))
		maintoken.append(str(num2))
		temp_str = stringOperation(str(num1),op,str(num2))
		maintoken.append(str(temp_str))
		return maintoken[-1]
	elif isinstance(num1, str) and isinstance(num2, str):
		maintoken.append(str(num1))
		maintoken.append(str(op))
		maintoken.append(str(num2))
		temp_str = stringOperation(str(num1),op,str(num2))
		maintoken.append(str(temp_str))
		return maintoken[-1]

	#population token array which has infix Evaluation results
	if op == "/" and num2 == 0:
		 temp = "0"
		 maintoken.append(str(num1))
		 maintoken.append(str(op))
		 maintoken.append(str(num2))
		 raise ZeroDivisionError('error')
	else:
	   temp = str(eval(str(num1) + op + str(num2),{"__builtins__":None}))
	   if temp =="inf":
		   maintoken.append(str(num1))
		   maintoken.append(str(op))
		   maintoken.append(str(num2))
		   raise SyntaxError(data["experssionErrorInf"])
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
	return maintoken[-1]

def addTolistRel(num1,op,num2):
	global maintoken
	orig_num1 = num1
	orig_num2 = num2
	temp1 = num1
	temp2 = num2
	if num1 == "not True":
	   temp1 = False
	elif num1 == "not False":
	   temp1 = True

	if num2 == "not True":
	   temp2 = False
	elif num2 == "not False":
	   temp2 = True


	if num1.lstrip('-').isdigit():
		num1 = int(num1)
	elif num1.replace('.', '', 1).lstrip('-').isdigit():
		num1 = float(num1)
	elif num1 == "not True":
		num1 = False
	elif num1 == "not False":
	    num1 = True
	elif num1 == "True":
		num1 = True
	elif num1 == "False":
	    num1 = False

	if num2.lstrip('-').isdigit():
		num2 = int(num2)
	elif num2.replace('.', '', 1).lstrip('-').isdigit():
		num2 = float(num2)
	elif num2 == "not True":
	    num2 = False
	elif num2 == "not False":
	    num2 = True
	elif num2 == "True":
	    num2 = True
	elif num2 == "False":
	    num2 = False

	if isinstance(num1, (int,bool)) and isinstance(num2, str):
		maintoken.append(str(orig_num1))
		maintoken.append(str(op))
		maintoken.append(str(orig_num2))
		temp_str = stringOperation(orig_num1,op,orig_num1)
		maintoken.append(str(temp_str))
		return maintoken[-1]
	elif isinstance(num1, str) and isinstance(num2, (int,float,bool)):
		maintoken.append(str(orig_num1))
		maintoken.append(str(op))
		maintoken.append(str(orig_num2))
		temp_str = stringOperation(orig_num1,op,orig_num2)
		maintoken.append(str(temp_str))
		return maintoken[-1]
	elif isinstance(num1, str) and isinstance(num2, str):
		maintoken.append(str(orig_num1))
		maintoken.append(str(op))
		maintoken.append(str(orig_num2))
		temp_str = stringOperation(orig_num1,op,orig_num2)
		maintoken.append(str(temp_str))
		return maintoken[-1]



	if op == ">=" or op == "<=":
		if str(num1) in ['True','False','not True','not False'] and str(num2) in ['True','False','not True','not False']:
		   raise SyntaxError(data["expressionErrorDoesNotMakeSense"])
	maintoken.append(str(orig_num1))
	maintoken.append(str(op))
	maintoken.append(str(orig_num2))
	maintoken.append(str(eval(str(temp1)+ " "+op+" " + str(temp2),{"__builtins__":None})))
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
	   #x = "1"
	   return x
	elif x == "not True":
	   x = "not True"
	   #x = "0"
	   return x
	elif x.replace('.', '', 1).lstrip('-').isdigit():
	   x = str(float(x))
	   return x
	elif not isOpCheck(x):
	   x = str(x)
	   return x

def calc(op, num1, num2):
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



def expression(token):
	global maintoken
	try:
		maintoken = []
		if token[0] == '-':
			token[0] = str(token[0] + token[1])
			token.pop(1)
		# for (index, tok) in enumerate(token, start=0):
		# 	if tok == "not":
		# 		if isNum1(token[index + 1]) or isOpCheck(token[index + 1]):
		# 				raise SyntaxError(data["notintfloat"]);
		for (index, tok) in enumerate(token, start=0):
			if tok == '-' or tok == "not":
				if token[index - 1] in '*-+/**==!=<=><>=%(-(':
					if token[index + 1] in ['True','False'] and token[index] == "not":
					   token[index] = str(token[index] +" "+ token[index + 1])
					   token.pop(index + 1)
					else:
					  token[index] = str(token[index] + token[index + 1])
					  token.pop(index + 1)
				elif token[index + 1] in ['True','False']  and token[index] == "not":
					token[index] = str(token[index] +" "+ token[index + 1])
					token.pop(index + 1)
		token1 = list(map(mapnum,token))
		expr = token1
		stackChr = list()  # character stack
		stackNum = list()  # number stack
		num = ''
		while len(expr) > 0:
			c = expr.pop(0)
			if len(expr) > 0:
				d = expr[0]
			else:
				d = ''
			if isNum(c):
				num = c
				if not isNum(d):
					stackNum.append(num)
					num = ''
			elif isOp(c):
				while True:
					if len(stackChr) > 0:
						top = stackChr[-1]
					else:
						top = ''
					if isOp(top):
						if not pri(c) > pri(top):
							num2 = stackNum.pop()
							op = stackChr.pop()
							num1 = stackNum.pop()
							stackNum.append(calc(op, num1, num2))
						else:
							stackChr.append(c)
							break
					else:
						stackChr.append(c)
						break
			elif c == '(' or c == "-(":
				stackChr.append(c)
			elif c == ')':
				while len(stackChr) > 0:
					c = stackChr.pop()
					if c == "(":
					    break
					elif c == "-(":
						if len(maintoken) == 0:
							stackNum[-1] = str(eval("-"+str(stackNum[-1]),{"__builtins__":None}))
						elif stackNum[-1] != maintoken[-1] :
							stackNum[-1] = str(eval("-"+str(stackNum[-1]),{"__builtins__":None}))
						else:
							stackNum[-1] = str(eval("-"+str(stackNum[-1]),{"__builtins__":None}))
							maintoken[-1] = str(eval(str(stackNum[-1]),{"__builtins__":None}))
						break
					elif isOp(c):
						num2 = stackNum.pop()
						num1 = stackNum.pop()
						stackNum.append(calc(c, num1, num2))
		while len(stackChr) > 0:
			c = stackChr.pop()
			if c == '(':
				break
			elif isOp(c):
				num2 = stackNum.pop()
				num1 = stackNum.pop()
				stackNum.append(calc(c, num1, num2))
		if 'not(' in ''.join(token):
			lastres = maintoken.pop()
			textt = 'not '+lastres
			ress = str(eval(str(textt),{"__builtins__":None}))
			maintoken.append(ress)
		return maintoken
	except SyntaxError as ex:
		excepName = type(ex).__name__
		cl, exc, tb = sys.exc_info()
		line_number = traceback.extract_tb(tb)[-1][1]
		print(ex,line_number)
		return maintoken
	except Exception as ex:
		excepName = type(ex).__name__
		cl, exc, tb = sys.exc_info()
		line_number = traceback.extract_tb(tb)[-1][1]
		print(ex,line_number)
		return maintoken
