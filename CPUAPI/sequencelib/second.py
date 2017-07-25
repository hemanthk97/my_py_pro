import re
import json
import sys
from sequencelib.infix import expression, mapnum, builtin_func_list
from collections import Counter
from math import ceil,sqrt,sin,floor,cos,tan
from random import seed,randint,random
import ast
import traceback



global_store = dict()
current_flag = False
mainJson = {}
resOfallLines = []
mainepxr = ""
numberr = ""
index = 0
_timer = 0
tablerow = 0
__firstTime = 0
InsideFunctionCall = 0
current_line = 0
variable_store = dict()
builtin_functions_list = [ 'None', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield','abs','ascii','bin','bool','chr','float','hex','id','input','len','max','min','oct','ord','print','round','sorted','str','sum','type','sqrt','tan','cos','sin','cos','ceil','floor','random','seed','randint',  'and', 'or','int','float','str1']
memoryAddress = ["0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100"]
import_builtins = ['ceil','sqrt','sin','floor','cos','cos','seed','randint','random']

def str1(x):
    return "'"+str(x)+"'"

allowed_builtins = {"abs":abs,"ascii":ascii,"bin":bin,"bool":bool,"chr":chr,"float":float,"hex":hex,"id":id,"input":input,"int":int,"len":len,"max":max,"min":min,"oct":oct,"ord":ord,"print":print,"round":round,"sorted":sorted,"str":str1,"sum":sum,"type":type, "ceil":ceil,"floor":floor,"sqrt":sqrt,"cos":cos,"sin":sin,"tan":tan, "seed":seed,"randint":randint,"random":random}

def storing_values(name,value):
    variable_store.update({name:value})



def ExpressionEval(token,resCode,i,resStatement,index):
    global mainJson
    global resOfallLines
    global variable_store
    # This is Expression do not contain variable or function
    if not mainJson['Details_with_linenum'][str(i)][3] and not mainJson['Details_with_linenum'][str(i)][4]:
        token1 = list(map(mapnum,token))
        res1 = list(mainJson['Details_with_linenum'][str(i)])
        res1[1] = resStatement+'Expression_normal'
        resOfallLines[index] = res1
        if ''.join(token1) == 'notTrue':
            res = 'False'
            send = "not True"
        elif ''.join(token1) == 'notFalse':
            res = 'True'
            send = "not False"
        else:
            res = expression(token)
            send = ''.join(token1)
        res1 = list(mainJson['Details_with_linenum'][str(i)])
        res1.append(send)
        res1.append(res)
        res1[1] = resStatement+'Expression_normal'
        finalRes = res1
        resOfallLines[index] = finalRes
        if res and not resStatement:
            if res[-1].replace('.', '', 1).lstrip('-').isdigit() or res[-1] in ['True','False']:
                storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),ast.literal_eval(res[-1]))
            else:
                storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res[-1])
        elif not resStatement:
            storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),ast.literal_eval(res))


    # This is Expression do not contain variable but contain functions
    elif not mainJson['Details_with_linenum'][str(i)][3] and mainJson['Details_with_linenum'][str(i)][4]:
        token1 = list(map(mapnum,token))
        res1 = list(mainJson['Details_with_linenum'][str(i)])
        res1[1] = resStatement+'Expression_func'
        resOfallLines[index] = res1
        token_func = builtin_func_list(token1)
        rendered_text = ''.join(token1)
        for j in token_func:
            if  set(import_builtins).intersection(set(mainJson['Details_with_linenum'][str(i)][4])):
                from math import ceil,sqrt,sin,floor,cos,tan
                from random import seed,randint,random
            rendered_text = rendered_text.replace(j,str(eval(j,{"__builtins__":None},allowed_builtins)))
        original_text = ''.join(token1)
        token4 = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|["\'a-z,A-Z,0-9,\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(rendered_text.strip().split()))
        res = []
        if len(token_func) > 1:
            res = expression(token4)
        res1 = list(mainJson['Details_with_linenum'][str(i)])
        res1.append([original_text,rendered_text])
        res1.append(res)
        res1[1] = resStatement+'Expression_func'
        finalRes = res1
        resOfallLines[index] = finalRes
        if res and not resStatement:
            if res[-1].replace('.', '', 1).lstrip('-').isdigit() or res[-1] in ['True','False']:
                storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),ast.literal_eval(res[-1]))
            else:
                storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res[-1])
        elif not resStatement:
            storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),ast.literal_eval(rendered_text))


    # This is Expression do not contain functions but contain variables
    elif mainJson['Details_with_linenum'][str(i)][3] and not mainJson['Details_with_linenum'][str(i)][4]:
        token1 = list(map(mapnum,token))
        res1 = mainJson['Details_with_linenum'][str(i)]
        res1[1] = resStatement+'Expression_variable'
        resOfallLines[index] = res1
        Text_Before_fetching_bold = ''.join(list(map(lambda x:x if not x in [key for key in variable_store] else '<b>'+x+'</b>',token1)))
        Text_After_fetching = list(map(lambda x:x if not x in [key for key in variable_store] else variable_store[x],token1))
        Text_After_fetching_lis = list(map(str,Text_After_fetching))
        Text_After_fetching = ''.join(list(map(str,Text_After_fetching)))
        if Text_After_fetching == 'notTrue':
            res = 'False'
            send = 'not True'
        elif Text_After_fetching == 'notFalse':
            res = 'True'
            send = 'not False'
        else:
            res = expression(Text_After_fetching_lis)
            send = Text_After_fetching
        data_mem_load_lis = [''.join(token1),Text_Before_fetching_bold,send]
        res1 = list(mainJson['Details_with_linenum'][str(i)])
        res1.append(data_mem_load_lis)
        res1.append(res)
        res1[1] = resStatement+'Expression_variable'
        finalRes = res1
        resOfallLines[index] = finalRes
        if res and not resStatement:
            if res[-1].replace('.', '', 1).lstrip('-').isdigit() or res[-1] in ['True','False']:
                storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),ast.literal_eval(res[-1]))
            else:
                storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res[-1])
        elif not resStatement:
            storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),ast.literal_eval(rendered_text))


    # This is Expression contain both functions and variables
    elif mainJson['Details_with_linenum'][str(i)][3] and mainJson['Details_with_linenum'][str(i)][4]:
        token1 = list(map(mapnum,token))
        original_text_bold = ''.join(token1)
        res1 = mainJson['Details_with_linenum'][str(i)]
        res1[1] = resStatement+'Expression_variable_func'
        resOfallLines[index] = res1
        token2 = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|["\'a-zA-Z0-9\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(original_text_bold.strip().split()))
        Text_Before_fetching_bold = ''.join(list(map(lambda x:x if not x in [key for key in variable_store] else '<b>'+x+'</b>',token2)))
        Text_After_fetching_lis = list(map(lambda x:x if not x in [key for key in variable_store] else str(variable_store[x]),token2))
        Text_After_fetching = ''.join(Text_After_fetching_lis)
        token3 = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|["\'a-z,A-Z,0-9,\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(Text_After_fetching.strip().split()))
        token_func = builtin_func_list(token3)
        for j in range(len(token_func)):
            if  set(import_builtins).intersection(set(mainJson['Details_with_linenum'][str(i)][4])):
                from math import ceil,sqrt,sin,floor,cos,tan
                from random import seed,randint,random
            Text_After_fetching = Text_After_fetching.replace(token_func[j],str(eval(token_func[j],{"__builtins__":None},allowed_builtins)))
        original_text = ''.join(token1)
        rendered_text = Text_After_fetching
        token4 = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|["\'a-z,A-Z,0-9,\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(rendered_text.strip().split()))
        res = []
        res = expression(token4)
        res1 = list(mainJson['Details_with_linenum'][str(i)])
        res1.append([original_text,Text_Before_fetching_bold,''.join(Text_After_fetching_lis),rendered_text])
        res1.append(res)
        res1[1] = resStatement+'Expression_variable_func'
        finalRes = res1
        resOfallLines[index] = finalRes
        if res and not resStatement:
            if res[-1].replace('.', '', 1).lstrip('-').isdigit() or res[-1] in ['True','False']:
                storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),ast.literal_eval(res[-1]))
            else:
                storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res[-1])
        elif not resStatement:
            storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),ast.literal_eval(rendered_text))





def check_expression_execute_noerror(i,code,index):
    global mainJson
    global resOfallLines
    global variable_store
    global current_line
    global InsideFunctionCall
    global global_store
    global current_flag
    origin_code = code
    code = code.split('\n')
    if current_flag:
        if current_line < i:
            InsideFunctionCall = InsideFunctionCall - 1
            if InsideFunctionCall == 0:
                variable_store = dict()
                variable_store = dict(global_store)
                global_store = dict()
                current_flag = False
            elif InsideFunctionCall > 0:
                variable_store = dict()
                variable_store = dict(global_store["func_"+str(InsideFunctionCall+1)])
                del global_store["func_"+str(InsideFunctionCall+1)]

    if mainJson['Details_with_linenum'][str(i)][0] == 'Assign':
        if mainJson['Details_with_linenum'][str(i)][1] in ["Expression","Expression_normal","Expression_variable","Expression_variable_func","Expression_func","UnaryOP"]:
            #code split after = as the statement will assign some value to varibale
            resCode = code[i-1].split('=',1)[1]
            # Initial setup for find different Expression ex:(a=-(-4)),a=-(int(4)),a=-(-(a)) , a=-(-int(a))
            token = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|["\'a-z,A-Z,0-9,\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(resCode.strip().split()))
            counter_token = Counter(token)
            token1 = set(token).union(set(['(', ')','+','-','*','**','/','%','>','<=','>=','<','==','!=','and','or','not']+builtin_functions_list))
            check = set(token1).symmetric_difference(set(['(', ')','+','-','*','**','/','%','>','<=','>=','<','==','!=','and','or','not']+builtin_functions_list))




            # check if duplicates (number or varibale) available
            check_num = 0
            if len(check) == 1:
                check_num = counter_token[str(list(check)[0])]



            #This is for negation(UnaryOP) with only numbers supports with or without in-bulit function example(-4,-(-4),int(-4),-int(-4))
            if not any(i in ['+','*','**','/','%','>','<=','>=','<','==','!=','and','or'] for i in token) and (len(mainJson['Details_with_linenum'][str(i)][4]) == 1 or check_num == 1 or not check):
                if not check or (str(list(check)[0]).replace('.', '', 1).lstrip('-').isdigit() or str(list(check)[0]) in ['True','False']) or isinstance(list(check)[0],str) and (not str(list(check)[0]) in [key for key in variable_store]):
                    if  set(import_builtins).intersection(set(mainJson['Details_with_linenum'][str(i)][4])):
                        from math import ceil,sqrt,sin,floor,cos,tan
                        from random import seed,randint,random
                    res = eval(resCode,{"__builtins__":None},allowed_builtins)
                    storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res)
                    res1 = list(mainJson['Details_with_linenum'][str(i)])
                    res1[1] = 'UnaryOp'
                    replaceValue = res1+[str(resCode),str(res)]
                    resOfallLines[index] = replaceValue

                #This is for negation(UnaryOP) with only varibale names supports with or without in-bulit function example(-a,-(-a),int(-a),-int(-a))
                elif str(list(check)[0]) in [key for key in variable_store]:
                    Text_Before_fetching_bold = ''.join(list(map(lambda x:x if str(list(check)[0]) != x else '<b>'+(list(check)[0])+'</b>',token)))
                    Text_After_fetching_lis = list(map(lambda x:x if str(list(check)[0]) != x else variable_store[str(list(check)[0])],token))
                    Text_After_fetching = ''.join(list(map(str,Text_After_fetching_lis)))
                    data_mem_load_lis = [resCode,Text_Before_fetching_bold,Text_After_fetching]
                    if isinstance(variable_store[str(list(check)[0])],str):
                      if any(word in Text_After_fetching for word in allowed_builtins):
                          res =  eval(Text_After_fetching,{"__builtins__":None},allowed_builtins)
                      else:
                          res =  Text_After_fetching
                    else:
                       if set(import_builtins).intersection(set(mainJson['Details_with_linenum'][str(i)][4])):
                           from math import ceil,sqrt,sin,floor,cos,tan
                           from random import seed,randint,random
                       res = eval(Text_After_fetching,{"__builtins__":None},allowed_builtins)
                    storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res)
                    res1 = list(mainJson['Details_with_linenum'][str(i)])
                    res1[1] = 'UnaryOp'
                    replaceValue = res1+data_mem_load_lis+[str(res)]
                    resOfallLines[index] = replaceValue
            else:
                ExpressionEval(token,resCode,i,'',index)

        elif mainJson['Details_with_linenum'][str(i)][1] == "Num":
            storing_values(str(mainJson['Details_with_linenum'][str(i)][3]),mainJson['Details_with_linenum'][str(i)][2])
            finalResnum = list(map(str,mainJson['Details_with_linenum'][str(i)]))
            resOfallLines[index] = finalResnum
        elif mainJson['Details_with_linenum'][str(i)][1] == "Str":
            if mainJson['Details_with_linenum'][str(i)][2] in ['True','False']:
                storing_values(str(mainJson['Details_with_linenum'][str(i)][3]),str(mainJson['Details_with_linenum'][str(i)][2]))
                finalResbool = list(map(str,mainJson['Details_with_linenum'][str(i)]))
                resOfallLines[index] = finalResbool
            else:
                storing_values(str(mainJson['Details_with_linenum'][str(i)][3]),"'"+mainJson['Details_with_linenum'][str(i)][2]+"'")
                finalResstr = list(map(str,mainJson['Details_with_linenum'][str(i)]))
                resOfallLines[index] = finalResstr
    elif mainJson['Details_with_linenum'][str(i)][0] == "Expr":
        resCode = code[i-1]
        printCode = resCode.strip()
        if mainJson['Details_with_linenum'][str(i)][1] == "print":
            printCode = printCode.replace('print','sem')
            res1 = list(mainJson['Details_with_linenum'][str(i)])
            resOfallLines[index] = res1
            # print('Hello')
            def sem(*args):
                return args
            from math import ceil,sqrt,sin,floor,cos,tan
            from random import seed,randint,random
            exec_var = ""
            for keys,values in variable_store.items():
                if keys in [key for key in variable_store]:
                    # print(keys)
                    if not isinstance(values,str):
                        exec_var = exec_var + str(keys)+" = "+str(values)+"\n"
                    else:
                        if values in ["True","False"]:
                            exec_var = exec_var + str(keys)+" = "+str(bool(values))+"\n"
                        else:
                            exec_var = exec_var + str(keys)+" = "+str(values)+"\n"
            exec(exec_var)

            finalRes = eval(printCode)
            res1 = list(mainJson['Details_with_linenum'][str(i)])
            res1.append([' '.join(map(str,finalRes))])
            resOfallLines[index] = res1
        else:
            res1 = mainJson['Details_with_linenum'][str(i)]
            res1[1] = 'others'
            resOfallLines[index] = res1
            from math import ceil,sqrt,sin,floor,cos,tan
            from random import seed,randint,random
            exec_var = ""
            for keys,values in variable_store.items():
                if keys in [key for key in variable_store]:
                    if not isinstance(values,str):
                        exec_var = exec_var + str(keys)+" = "+str(values)+"\n"
                    else:
                        exec_var = exec_var +str(keys)+" = "+str(values)+"\n"
            exec(exec_var)
            finalRes = eval(printCode)
            res1 = list(mainJson['Details_with_linenum'][str(i)])
            res1.append([str(finalRes)])
            resOfallLines[index] = res1
    elif mainJson['Details_with_linenum'][str(i)][0] == "FunctionDef":
         res1 = list(mainJson['Details_with_linenum'][str(i)])
         res1.append('<function Def>')
         resOfallLines[index] = res1
         storing_values(mainJson['Details_with_linenum'][str(i)][2],mainJson['Details_with_linenum'][str(i)][3])
    elif mainJson['Details_with_linenum'][str(i)][0] == "If":
         resCode = code[i-1].split('if',1)[1]
         resCode = resCode.split(':')[0]
         token = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|["\'a-z,A-Z,0-9,\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(resCode.strip().split()))
         if mainJson['Details_with_linenum'][str(i)][1] in ['Name','NameConstant','Expression']:
            if mainJson['Details_with_linenum'][str(i)][1] == "Name":
                # counter_token = Counter(token)
                # token1 = set(token).union(set(['(', ')','+','-','*','**','/','%','>','<=','>=','<','==','!=','and','or','not']+builtin_functions_list))
                res1 = list(mainJson['Details_with_linenum'][str(i)])
                resOfallLines[index] = res1
                Text_Before_fetching_bold = ''.join(list(map(lambda x:x if str(list(mainJson['Details_with_linenum'][str(i)][3])[0]) != x else '<b>'+(list(mainJson['Details_with_linenum'][str(i)][3])[0])+'</b>',token)))
                Text_After_fetching = list(map(lambda x:x if str(list(mainJson['Details_with_linenum'][str(i)][3])[0]) != x else variable_store[str(list(mainJson['Details_with_linenum'][str(i)][3])[0])],token))
                Text_After_fetching = ''.join(list(map(str,Text_After_fetching)))
                data_mem_load_lis = [resCode,Text_Before_fetching_bold,Text_After_fetching]
                if isinstance(variable_store[str(list(mainJson['Details_with_linenum'][str(i)][3])[0])],str):
                    res = eval(Text_After_fetching,{"__builtins__":None},allowed_builtins)
                else:
                    res = eval(Text_After_fetching,{"__builtins__":None},allowed_builtins)
                res1 = list(mainJson['Details_with_linenum'][str(i)])
                replaceValue = res1+data_mem_load_lis+[str(res)]
                resOfallLines[index] = replaceValue
                # check = set(token1).symmetric_difference(set(['(', ')','+','-','*','**','/','%','>','<=','>=','<','==','!=','and','or','not']+builtin_functions_list))
                #  # check if duplicates (number or varibale) available
                # check_num = 0
                # if len(check) == 1:
                #     check_num = counter_token[str(list(check)[0])]
            elif mainJson['Details_with_linenum'][str(i)][1] == "NameConstant":
                 res1 = list(mainJson['Details_with_linenum'][str(i)])
                 resOfallLines[index] = res1
            elif mainJson['Details_with_linenum'][str(i)][1] == "Expression":
                 ExpressionEval(token,resCode,i,'If_',index)
    elif mainJson['Details_with_linenum'][str(i)][0] == "While":
         resCode = code[i-1].split('while')[1]
         resCode = resCode.split(':')[0]
         token = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|["\'a-z,A-Z,0-9,\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(resCode.strip().split()))
         if str(mainJson['Details_with_linenum'][str(i)][1]) in ['Name','NameConstant','Expression','while_Expression_normal','while_Expression_func','while_Expression_variable','while_Expression_variable_func']:
            if mainJson['Details_with_linenum'][str(i)][1] == "Name":
                res1 = list(mainJson['Details_with_linenum'][str(i)])
                resOfallLines[index] = res1
                Text_Before_fetching_bold = ''.join(list(map(lambda x:x if str(list(check)[0]) != x else '<b>'+(list(mainJson['Details_with_linenum'][str(i)][3]))+'</b>',token)))
                Text_After_fetching = list(map(lambda x:x if str(list(check)[0]) != x else variable_store[str(list(mainJson['Details_with_linenum'][str(i)][3]))],token))
                Text_After_fetching = ''.join(list(map(str,Text_After_fetching)))
                data_mem_load_lis = [resCode,Text_Before_fetching_bold,Text_After_fetching]
                if isinstance(variable_store[str(list(mainJson['Details_with_linenum'][str(i)][3]))],str):
                    res = eval(Text_After_fetching,{"__builtins__":None},allowed_builtins)
                else:
                    res = eval(Text_After_fetching,{"__builtins__":None},allowed_builtins)
                res1 = list(mainJson['Details_with_linenum'][str(i)])
                replaceValue = res1+data_mem_load_lis+[str(res)]
                resOfallLines[index] = replaceValue
            elif str(mainJson['Details_with_linenum'][str(i)][1]) in ['Expression','while_Expression_normal','while_Expression_func','while_Expression_variable','while_Expression_variable_func']:
                 ExpressionEval(token,resCode,i,'while_',index)
    elif mainJson['Details_with_linenum'][str(i)][0] == "FunctionCall":
        global_store1 = dict()
        InsideFunctionCall = InsideFunctionCall + 1
        if InsideFunctionCall == 1:
            global_store = dict()
            global_store = dict(variable_store)
            global_store1 = dict(variable_store)
            variable_store = dict()
        elif InsideFunctionCall > 1:
            global_store["func_"+str(InsideFunctionCall)] = dict(variable_store)
            global_store1 = dict(global_store["func_"+str(InsideFunctionCall)])
            variable_store = dict()

        current_line = i
        current_flag = True
        res1 = list(mainJson['Details_with_linenum'][str(i)])
        replaceValue = res1
        resOfallLines[index] = replaceValue
        # Function call without args


        # Parameters with only values no varibales
        if mainJson['Details_with_linenum'][str(i)][4] and not mainJson['Details_with_linenum'][str(i)][5]:
            ind = 0
            Parameters_Names = list(global_store1[str(mainJson['Details_with_linenum'][str(i)][2][0])])
            for keyss in Parameters_Names:
                if isinstance(mainJson['Details_with_linenum'][str(i)][3][ind],str):
                    str_value = "'"+mainJson['Details_with_linenum'][str(i)][3][ind]+"'"
                else:
                    str_value = mainJson['Details_with_linenum'][str(i)][3][ind]
                storing_values(keyss,str_value)
                ind=ind+1
            res1 = list(mainJson['Details_with_linenum'][str(i)])
            res1.append(Parameters_Names)
            finalres = ["'"+x+"'"  if isinstance(x,str) else x for x in mainJson['Details_with_linenum'][str(i)][3]]
            finalres = [str(x)  if isinstance(x,bool) else x for x in finalres]
            res1.append(finalres)
            resOfallLines[index] = res1

        elif mainJson['Details_with_linenum'][str(i)][4] or mainJson['Details_with_linenum'][str(i)][5]:
            firstSplit = str(mainJson['Details_with_linenum'][str(i)][2][0])+'('
            resCode = code[i-1].split(str(mainJson['Details_with_linenum'][str(i)][2][0])+'(',1)[1]
            token = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|["\'a-zA-Z0-9\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(resCode.strip().split()))
            if token[-1] == ")":
                lastSplit = token.pop()
            token1 = list(map(mapnum,token))
            Text_Before_fetching_bold = ''.join(list(map(lambda x:x if not x in [key for key in global_store1] else '<b>'+x+'</b>',token1)))
            Text_After_fetching_lis = list(map(lambda x:x if not x in [key for key in global_store1] else global_store1[x],token1))
            Text_After_fetching = list(map(str,Text_After_fetching_lis))
            Text_After_fetching = ''.join(list(map(str,Text_After_fetching)))
            print(global_store)
            Parameters_Names = list(global_store1[str(mainJson['Details_with_linenum'][str(i)][2][0])])
            print(Parameters_Names)
            ind = 0
            Text_After_fetching_lis = [x for x in Text_After_fetching_lis if x != ',']
            for keyss in Parameters_Names:
                if isinstance(Text_After_fetching_lis[ind],str):
                    str_value = Text_After_fetching_lis[ind]
                else:
                    str_value = Text_After_fetching_lis[ind]
                storing_values(keyss,str_value)
                ind=ind+1
            res1 = list(mainJson['Details_with_linenum'][str(i)])
            res1.append([firstSplit+Text_Before_fetching_bold+lastSplit,firstSplit+Text_After_fetching+lastSplit])
            res1.append(Parameters_Names)
            # Text_After_fetching_lis = ["'"+x+"'" if isinstance(x,str) else x for x in Text_After_fetching_lis]
            Text_After_fetching_lis = [str(x) if isinstance(x,bool) else x for x in Text_After_fetching_lis ]
            # print(Text_After_fetching_lis)
            res1.append(Text_After_fetching_lis)
            resOfallLines[index] = res1




def sequence_execute(mainJ,code):
    global mainJson
    global resOfallLines
    global variable_store
    global global_store
    global current_line
    global current_flag
    global InsideFunctionCall
    mainJson = json.loads(json.dumps(mainJ))
    # print(mainJson)
    variable_store = dict()
    global_store = dict()
    current_line = None
    current_flag = False
    InsideFunctionCall = 0
    resOfallLines = [0]*len(mainJson['resData'])
    resDataArr = mainJson['resData']
    try:
        index = 0
        for i in resDataArr:
            check_expression_execute_noerror(i,code,index)
            index = index + 1
        del mainJson['Details_with_linenum']
        mainJson['program_data'] = resOfallLines
        return mainJson
    except Exception as ex:
        print(ex)
        excepName = type(ex).__name__
        cl, exc, tb = sys.exc_info()
        line_number = traceback.extract_tb(tb)[-1][1]
        print(line_number,ex)
        del mainJson['Details_with_linenum']
        mainJson['program_data'] = resOfallLines
        return mainJson
