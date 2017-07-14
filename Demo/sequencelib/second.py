import re
import json
import sys
from sequencelib.infix import expression, mapnum, builtin_func_list
from collections import Counter
from math import ceil,sqrt,sin,floor,cos,tan
from random import seed,randint,random
import ast
import traceback



mainJson = {}
mainepxr = ""
numberr = ""
index = 0
_timer = 0
tablerow = 0
__firstTime = 0
variable_store = dict()
builtin_functions_list = [ 'None', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield','abs','ascii','bin','bool','chr','float','hex','id','input','len','max','min','oct','ord','print','round','sorted','str','sum','type','sqrt','tan','cos','sin','cos','ceil','floor','random','seed','randint',  'and', 'or','int','float','str']
memoryAddress = ["0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100"]
import_builtins = ['ceil','sqrt','sin','floor','cos','cos','seed','randint','random']
allowed_builtins = {"abs":abs,"ascii":ascii,"bin":bin,"bool":bool,"chr":chr,"float":float,"hex":hex,"id":id,"input":input,"int":int,"len":len,"max":max,"min":min,"oct":oct,"ord":ord,"print":print,"round":round,"sorted":sorted,"str":str,"sum":sum,"type":type, "ceil":ceil,"floor":floor,"sqrt":sqrt,"cos":cos,"sin":sin,"tan":tan, "seed":seed,"randint":randint,"random":random}



def storing_values(name,value):
    variable_store.update({name:value})
    #print(variable_store)

def check_expression_execute_noerror(i,code):
    global mainJson
    origin_code = code
    code = code.split('\n')
    print(code)
    if mainJson['Details_with_linenum'][str(i)][0] == 'Assign':
        if mainJson['Details_with_linenum'][str(i)][1] == "Expression":
            #code split after = as the statement will assign some value to varibale
            resCode = code[i-1].split('=',1)[1]
            # Initial setup for find different Expression ex:(a=-(-4)),a=-(int(4)),a=-(-(a)) , a=-(-int(a))
            token = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|["\'a-z,A-Z,0-9,\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(resCode.strip().split()))
            counter_token = Counter(token)
            token1 = set(token).union(set(['(', ')','+','-','*','**','/','%','>','<=','>=','<','==','!=','and','or','not']+builtin_functions_list))
            check = set(token1).symmetric_difference(set(['(', ')','+','-','*','**','/','%','>','<=','>=','<','==','!=','and','or','not']+builtin_functions_list))
            #
            # print('Inside')
            # print(not check)


            # check if duplicates (number or varibale) available
            check_num = 0
            if len(check) == 1:
                check_num = counter_token[str(list(check)[0])]

            #This is for negation(UnaryOP) with only numbers supports with or without in-bulit function example(-4,-(-4),int(-4),-int(-4))
            if not any(i in ['+','*','**','/','%','>','<=','>=','<','==','!=','and','or'] for i in token) and (len(mainJson['Details_with_linenum'][str(i)][4]) == 1 or check_num == 1 or not check):
                if not check or (str(list(check)[0]).replace('.', '', 1).lstrip('-').isdigit() or str(list(check)[0]) in ['True','False']):
                    if  set(import_builtins).intersection(set(mainJson['Details_with_linenum'][str(i)][4])):
                        from math import ceil,sqrt,sin,floor,cos,tan
                        from random import seed,randint,random
                    res = eval(resCode,{"__builtins__":None},allowed_builtins)
                    storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res)
                    res1 = mainJson['Details_with_linenum'][str(i)]
                    res1[1] = 'UnaryOp'
                    replaceValue = res1+[str(resCode),str(res)]
                    mainJson['Details_with_linenum'].update({str(i):replaceValue})

                #This is for negation(UnaryOP) with only varibale names supports with or without in-bulit function example(-a,-(-a),int(-a),-int(-a))
                elif str(list(check)[0]) in [key for key in variable_store]:
                    Text_Before_fetching_bold = ''.join(list(map(lambda x:x if str(list(check)[0]) != x else '<b>'+(list(check)[0])+'</b>',token)))
                    Text_After_fetching = list(map(lambda x:x if str(list(check)[0]) != x else variable_store[str(list(check)[0])],token))
                    Text_After_fetching = ''.join(list(map(str,Text_After_fetching)))
                    data_mem_load_lis = [resCode,Text_Before_fetching_bold,Text_After_fetching]
                    if isinstance(variable_store[str(list(check)[0])],str):
                       res = Text_After_fetching
                    else:
                       if set(import_builtins).intersection(set(mainJson['Details_with_linenum'][str(i)][4])):
                           from math import ceil,sqrt,sin,floor,cos,tan
                           from random import seed,randint,random
                       res = eval(Text_After_fetching,{"__builtins__":None},allowed_builtins)
                    storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res)
                    res1 = mainJson['Details_with_linenum'][str(i)]
                    res1[1] = 'UnaryOp'
                    replaceValue = res1+data_mem_load_lis+[str(res)]
                    mainJson['Details_with_linenum'].update({str(i):replaceValue})
            else:
                #print(mainJson['Details_with_linenum'][str(i)][3],mainJson['Details_with_linenum'][str(i)][4])

                #
                # token = [x for x in token if x != '"']
                # token = [x for x in token if x != "'"]


                # This is Expression do not contain variable or function
                if not mainJson['Details_with_linenum'][str(i)][3] and not mainJson['Details_with_linenum'][str(i)][4]:
                    token1 = list(map(mapnum,token))
                    res1 = mainJson['Details_with_linenum'][str(i)]
                    res1[1] = 'Expression_normal'
                    mainJson['Details_with_linenum'].update({str(i):res1})
                    res = expression(token)
                    res1 = mainJson['Details_with_linenum'][str(i)]
                    res1.append(''.join(token1))
                    res1.append(res)
                    res1[1] = 'Expression_normal'
                    mainJson['Details_with_linenum'].update({str(i):res1})
                    if res[-1].replace('.', '', 1).lstrip('-').isdigit() or res[-1] in ['True','False']:
                        storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),ast.literal_eval(res[-1]))
                    else:
                        storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res[-1])
                    # print(variable_store)


                # This is Expression do not contain variable but contain functions
                elif not mainJson['Details_with_linenum'][str(i)][3] and mainJson['Details_with_linenum'][str(i)][4]:
                    token1 = list(map(mapnum,token))
                    res1 = mainJson['Details_with_linenum'][str(i)]
                    res1[1] = 'Expression_func'
                    mainJson['Details_with_linenum'].update({str(i):res1})
                    token_func = builtin_func_list(token1)
                    rendered_text = ''.join(token1)
                    for j in token_func:
                        if  set(import_builtins).intersection(set(mainJson['Details_with_linenum'][str(i)][4])):
                            from math import ceil,sqrt,sin,floor,cos,tan
                            from random import seed,randint,random
                        rendered_text = rendered_text.replace(j,str(eval(j,{"__builtins__":None},allowed_builtins)))
                    original_text = ''.join(token1)
                    token = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|[a-z,A-Z,0-9,\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(rendered_text.strip().split()))
                    res = expression(token)
                    res1 = mainJson['Details_with_linenum'][str(i)]
                    res1.append([original_text,rendered_text])
                    res1.append(res)
                    res1[1] = 'Expression_func'
                    mainJson['Details_with_linenum'].update({str(i):res1})
                    if res[-1].replace('.', '', 1).lstrip('-').isdigit() or res[-1] in ['True','False']:
                        storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),ast.literal_eval(res[-1]))
                    else:
                        storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res[-1])


                # This is Expression do not contain functions but contain variables
                elif mainJson['Details_with_linenum'][str(i)][3] and not mainJson['Details_with_linenum'][str(i)][4]:
                    token1 = list(map(mapnum,token))
                    res1 = mainJson['Details_with_linenum'][str(i)]
                    res1[1] = 'Expression_varibale'
                    mainJson['Details_with_linenum'].update({str(i):res1})
                    Text_Before_fetching_bold = ''.join(list(map(lambda x:x if not x in [key for key in variable_store] else '<b>'+x+'</b>',token1)))
                    Text_After_fetching = list(map(lambda x:x if not x in [key for key in variable_store] else variable_store[x],token1))
                    Text_After_fetching_lis = list(map(str,Text_After_fetching))
                    Text_After_fetching = ''.join(list(map(str,Text_After_fetching)))
                    res = expression(Text_After_fetching_lis)
                    data_mem_load_lis = [''.join(token1),Text_Before_fetching_bold,Text_After_fetching]
                    res1 = mainJson['Details_with_linenum'][str(i)]
                    res1.append(data_mem_load_lis)
                    res1.append(res)
                    res1[1] = 'Expression_varibale'
                    mainJson['Details_with_linenum'].update({str(i):res1})
                    if res[-1].replace('.', '', 1).lstrip('-').isdigit() or res[-1] in ['True','False']:
                        storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),ast.literal_eval(res[-1]))
                    else:
                        storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res[-1])



                # This is Expression contain both functions and variables
                elif mainJson['Details_with_linenum'][str(i)][3] and mainJson['Details_with_linenum'][str(i)][4]:
                    token1 = list(map(mapnum,token))
                    original_text_bold = ''.join(token1)
                    res1 = mainJson['Details_with_linenum'][str(i)]
                    res1[1] = 'Expression_variable_func'
                    mainJson['Details_with_linenum'].update({str(i):res1})
                    token2 = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|[a-zA-Z0-9\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(original_text_bold.strip().split()))
                    Text_Before_fetching_bold = ''.join(list(map(lambda x:x if not x in [key for key in variable_store] else '<b>'+x+'</b>',token2)))
                    Text_After_fetching_lis = list(map(lambda x:x if not x in [key for key in variable_store] else str(variable_store[x]),token2))
                    Text_After_fetching = ''.join(Text_After_fetching_lis)
                    token3 = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|[a-z,A-Z,0-9,\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(Text_After_fetching.strip().split()))
                    token_func = builtin_func_list(token3)
                    for j in range(len(token_func)):
                        if  set(import_builtins).intersection(set(mainJson['Details_with_linenum'][str(i)][4])):
                            from math import ceil,sqrt,sin,floor,cos,tan
                            from random import seed,randint,random
                        Text_After_fetching = Text_After_fetching.replace(token_func[j],str(eval(token_func[j],{"__builtins__":None},allowed_builtins)))
                    original_text = ''.join(token1)
                    rendered_text = Text_After_fetching
                    token4 = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|[a-z,A-Z,0-9,\#\@\$\^\&\_\~\`]+|[)(]{1}|.', ''.join(rendered_text.strip().split()))
                    res = expression(token4)
                    res1 = mainJson['Details_with_linenum'][str(i)]
                    res1.append([original_text,Text_Before_fetching_bold,''.join(Text_After_fetching_lis),rendered_text])
                    res1.append(res)
                    res1[1] = 'Expression_variable_func'
                    mainJson['Details_with_linenum'].update({str(i):res1})
                    if res[-1].replace('.', '', 1).lstrip('-').isdigit() or res[-1] in ['True','False']:
                        storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),ast.literal_eval(res[-1]))
                    else:
                        storing_values(str(mainJson['Details_with_linenum'][str(i)][2]),res[-1])


        elif mainJson['Details_with_linenum'][str(i)][1] == "Num":
            storing_values(str(mainJson['Details_with_linenum'][str(i)][3]),mainJson['Details_with_linenum'][str(i)][2])
        elif mainJson['Details_with_linenum'][str(i)][1] == "Str":
            storing_values(str(mainJson['Details_with_linenum'][str(i)][3]),mainJson['Details_with_linenum'][str(i)][2])

    elif mainJson['Details_with_linenum'][str(i)][0] == "Expr":
        print('inside')
        resCode = code[i-1]
        printCode = resCode.strip()
        if mainJson['Details_with_linenum'][str(i)][1] == "print":
            printCode = printCode.replace('print','sem')
            def sem(*args):
                return args
            from math import ceil,sqrt,sin,floor,cos,tan
            from random import seed,randint,random
            exec(origin_code)
            finalRes = eval(printCode)
            res1 = mainJson['Details_with_linenum'][str(i)]
            res1.append([' '.join(map(str,finalRes))])
            mainJson['Details_with_linenum'].update({str(i):res1})
        else:
            print('sss')
            res1 = mainJson['Details_with_linenum'][str(i)]
            res1[1] = 'others'
            mainJson['Details_with_linenum'].update({str(i):res1})
            from math import ceil,sqrt,sin,floor,cos,tan
            from random import seed,randint,random
            # exec(origin_code)
            # finalRes = eval(printCode)
            print(finalRes)
            res1 = mainJson['Details_with_linenum'][str(i)]
            res1.append([str(finalRes)])
            mainJson['Details_with_linenum'].update({str(i):res1})



def sequence_execute(mainJ,code):
    global mainJson
    mainJson = json.loads(json.dumps(mainJ))
    variable_store.clear()
    try:
        if mainJson['error'] == '0':
            for i in mainJson['resData']:
                check_expression_execute_noerror(i,code)
        elif mainJson['error'] == '1':
            for i in mainJson['resData']:
                check_expression_execute_noerror(i,code)
        return mainJson
    except Exception as ex:
        excepName = type(ex).__name__
        cl, exc, tb = sys.exc_info()
        line_number = traceback.extract_tb(tb)[-1][1]
        return mainJson
