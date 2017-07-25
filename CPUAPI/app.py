import itertools
from flask import Flask,jsonify
from flask import request
from flask_cors import CORS, cross_origin
import json
import sys
from collections import Counter
import re
import traceback
import ast
import inspect
from sequencelib import globalfile
import functionsLevel
from math import ceil,sqrt,sin,floor,cos,tan
from random import seed,randint,random
from sequencelib.second import sequence_execute

with open('error.txt') as json_file:
    data = json.load(json_file)

globalfile.dict1 = {}


app = Flask(__name__, static_url_path='')
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route('/error/')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def root():
    return app.send_static_file('error.txt')

@app.route("/api",methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def serve_api():
    code = request.json['Data']
    l_execution_path = []
    def f_execution_path(code):
        program = code.split('\n')
        def tracefunc(frame, event, arg):
            if event == "line":
               if frame.f_lineno <= len(program):
                  if len(l_execution_path) > 0:
                      lis = sorted(Counter(l_execution_path).values())
                  else:
                      lis = [0]
                  if lis[-1] < data['While_loop_limition']:
                     l_execution_path.append(frame.f_lineno)
                  else:
                     raise Exception(data['whileLoopLimit'],frame.f_lineno-1)
            return tracefunc
        try:
            sys.settrace(tracefunc)
            exec(code)
            return 1
        except Exception as e:
            sys.settrace(None)
            return e
    try:
       global i
       tree = ast.parse(code)
       if request.json['Level'] == "sequence":
            functionsLevel.nodevisitSeq().visit(tree)
       elif request.json['Level'] == "functions":
            functionsLevel.nodevisit_func().visit(tree)
       elif request.json['Level'] == "conditions":
            functionsLevel.nodevisit_cond().visit(tree)
       compile(code,'<string>','exec')
    except Exception as e:
        excepName = type(e).__name__
        cl, exc, tb = sys.exc_info()
        line_number = traceback.extract_tb(tb)[-1][1]
        print(e,line_number)
        i = 0
        globalfile.dict1 = {}
        return functionsLevel.compileFunction(e,code)
    try:
       ans = f_execution_path(code)
       if ans != 1:
           raise ans
    except Exception as e:
        excepName = type(e).__name__
        cl, exc, tb = sys.exc_info()
        line_number = traceback.extract_tb(tb)[-1][1]
        print(e,line_number)
        if excepName == "NameError":
           name = str(e).split("'")[1].split("'")[0]
           res = {"resData":l_execution_path,"error_name":excepName,"error_message":"'"+name+"' "+data['NameError'],"error":"1","error_Type":"run-time","line_no":line_number,'Details_with_linenum':globalfile.dict1}
           i = 0
           globalfile.dict1 = {}
           mainRes = sequence_execute(res,code)
           return jsonify(mainRes)
        if e.args[0] == "While loop limit exceeed":
           name = str(e).split("'")[1].split("'")[0]
           res = {"resData":l_execution_path,"error_name":excepName,"error_message":"'"+name+"'","error":"1","error_Type":"run-time","line_no":e.args[1],'Details_with_linenum':globalfile.dict1}
           i = 0
           globalfile.dict1 = {}
           mainRes = sequence_execute(res,code)
           return jsonify(mainRes)
        res = {"resData":l_execution_path,"error_name":excepName,"error_message":str(e),"error":"1","error_Type":"run-time","line_no":line_number,'Details_with_linenum':globalfile.dict1}
        i = 0
        globalfile.dict1 = {}
        mainRes = sequence_execute(res,code)
        return jsonify(mainRes)
    res = {"resData":l_execution_path,"error":"0",'Details_with_linenum':globalfile.dict1}
    mainRes = sequence_execute(res,code)
    i = 0
    globalfile.dict1 = {}
    return jsonify(mainRes)


if __name__ == "__main__":
   app.config['name'] = '172.16.32.27'
   app.run(host=app.config['name'],port=5003, debug=True)
