import ast
import json
from flask import Flask,jsonify
import sys
from collections import Counter
import re
import ast
from sequencelib import globalfile

with open('error.txt') as json_file:
    data = json.load(json_file)

keywords = ['AND', 'ANd', 'AnD', 'And', 'aND', 'aNd', 'anD', 'AS', 'As', 'aS', 'ASSERT', 'ASSERt', 'ASSErT', 'ASSErt', 'ASSeRT', 'ASSeRt', 'ASSerT', 'ASSert', 'ASsERT', 'ASsERt', 'ASsErT', 'ASsErt', 'ASseRT', 'ASseRt', 'ASserT', 'ASsert', 'AsSERT', 'AsSERt', 'AsSErT', 'AsSErt', 'AsSeRT', 'AsSeRt', 'AsSerT', 'AsSert', 'AssERT', 'AssERt', 'AssErT', 'AssErt', 'AsseRT', 'AsseRt', 'AsserT', 'Assert', 'aSSERT', 'aSSERt', 'aSSErT', 'aSSErt', 'aSSeRT', 'aSSeRt', 'aSSerT', 'aSSert', 'aSsERT', 'aSsERt', 'aSsErT', 'aSsErt', 'aSseRT', 'aSseRt', 'aSserT', 'aSsert', 'asSERT', 'asSERt', 'asSErT', 'asSErt', 'asSeRT', 'asSeRt', 'asSerT', 'asSert', 'assERT', 'assERt', 'assErT', 'assErt', 'asseRT', 'asseRt', 'asserT', 'BREAK', 'BREAk', 'BREaK', 'BREak', 'BReAK', 'BReAk', 'BReaK', 'BReak', 'BrEAK', 'BrEAk', 'BrEaK', 'BrEak', 'BreAK', 'BreAk', 'BreaK', 'Break', 'bREAK', 'bREAk', 'bREaK', 'bREak', 'bReAK', 'bReAk', 'bReaK', 'bReak', 'brEAK', 'brEAk', 'brEaK', 'brEak', 'breAK', 'breAk', 'breaK', 'CLASS', 'CLASs', 'CLAsS', 'CLAss', 'CLaSS', 'CLaSs', 'CLasS', 'CLass', 'ClASS', 'ClASs', 'ClAsS', 'ClAss', 'ClaSS', 'ClaSs', 'ClasS', 'Class', 'cLASS', 'cLASs', 'cLAsS', 'cLAss', 'cLaSS', 'cLaSs', 'cLasS', 'cLass', 'clASS', 'clASs', 'clAsS', 'clAss', 'claSS', 'claSs', 'clasS', 'CONTINUE', 'CONTINUe', 'CONTINuE', 'CONTINue', 'CONTInUE', 'CONTInUe', 'CONTInuE', 'CONTInue', 'CONTiNUE', 'CONTiNUe', 'CONTiNuE', 'CONTiNue', 'CONTinUE', 'CONTinUe', 'CONTinuE', 'CONTinue', 'CONtINUE', 'CONtINUe', 'CONtINuE', 'CONtINue', 'CONtInUE', 'CONtInUe', 'CONtInuE', 'CONtInue', 'CONtiNUE', 'CONtiNUe', 'CONtiNuE', 'CONtiNue', 'CONtinUE', 'CONtinUe', 'CONtinuE', 'CONtinue', 'COnTINUE', 'COnTINUe', 'COnTINuE', 'COnTINue', 'COnTInUE', 'COnTInUe', 'COnTInuE', 'COnTInue', 'COnTiNUE', 'COnTiNUe', 'COnTiNuE', 'COnTiNue', 'COnTinUE', 'COnTinUe', 'COnTinuE', 'COnTinue', 'COntINUE', 'COntINUe', 'COntINuE', 'COntINue', 'COntInUE', 'COntInUe', 'COntInuE', 'COntInue', 'COntiNUE', 'COntiNUe', 'COntiNuE', 'COntiNue', 'COntinUE', 'COntinUe', 'COntinuE', 'COntinue', 'CoNTINUE', 'CoNTINUe', 'CoNTINuE', 'CoNTINue', 'CoNTInUE', 'CoNTInUe', 'CoNTInuE', 'CoNTInue', 'CoNTiNUE', 'CoNTiNUe', 'CoNTiNuE', 'CoNTiNue', 'CoNTinUE', 'CoNTinUe', 'CoNTinuE', 'CoNTinue', 'CoNtINUE', 'CoNtINUe', 'CoNtINuE', 'CoNtINue', 'CoNtInUE', 'CoNtInUe', 'CoNtInuE', 'CoNtInue', 'CoNtiNUE', 'CoNtiNUe', 'CoNtiNuE', 'CoNtiNue', 'CoNtinUE', 'CoNtinUe', 'CoNtinuE', 'CoNtinue', 'ConTINUE', 'ConTINUe', 'ConTINuE', 'ConTINue', 'ConTInUE', 'ConTInUe', 'ConTInuE', 'ConTInue', 'ConTiNUE', 'ConTiNUe', 'ConTiNuE', 'ConTiNue', 'ConTinUE', 'ConTinUe', 'ConTinuE', 'ConTinue', 'ContINUE', 'ContINUe', 'ContINuE', 'ContINue', 'ContInUE', 'ContInUe', 'ContInuE', 'ContInue', 'ContiNUE', 'ContiNUe', 'ContiNuE', 'ContiNue', 'ContinUE', 'ContinUe', 'ContinuE', 'Continue', 'cONTINUE', 'cONTINUe', 'cONTINuE', 'cONTINue', 'cONTInUE', 'cONTInUe', 'cONTInuE', 'cONTInue', 'cONTiNUE', 'cONTiNUe', 'cONTiNuE', 'cONTiNue', 'cONTinUE', 'cONTinUe', 'cONTinuE', 'cONTinue', 'cONtINUE', 'cONtINUe', 'cONtINuE', 'cONtINue', 'cONtInUE', 'cONtInUe', 'cONtInuE', 'cONtInue', 'cONtiNUE', 'cONtiNUe', 'cONtiNuE', 'cONtiNue', 'cONtinUE', 'cONtinUe', 'cONtinuE', 'cONtinue', 'cOnTINUE', 'cOnTINUe', 'cOnTINuE', 'cOnTINue', 'cOnTInUE', 'cOnTInUe', 'cOnTInuE', 'cOnTInue', 'cOnTiNUE', 'cOnTiNUe', 'cOnTiNuE', 'cOnTiNue', 'cOnTinUE', 'cOnTinUe', 'cOnTinuE', 'cOnTinue', 'cOntINUE', 'cOntINUe', 'cOntINuE', 'cOntINue', 'cOntInUE', 'cOntInUe', 'cOntInuE', 'cOntInue', 'cOntiNUE', 'cOntiNUe', 'cOntiNuE', 'cOntiNue', 'cOntinUE', 'cOntinUe', 'cOntinuE', 'cOntinue', 'coNTINUE', 'coNTINUe', 'coNTINuE', 'coNTINue', 'coNTInUE', 'coNTInUe', 'coNTInuE', 'coNTInue', 'coNTiNUE', 'coNTiNUe', 'coNTiNuE', 'coNTiNue', 'coNTinUE', 'coNTinUe', 'coNTinuE', 'coNTinue', 'coNtINUE', 'coNtINUe', 'coNtINuE', 'coNtINue', 'coNtInUE', 'coNtInUe', 'coNtInuE', 'coNtInue', 'coNtiNUE', 'coNtiNUe', 'coNtiNuE', 'coNtiNue', 'coNtinUE', 'coNtinUe', 'coNtinuE', 'coNtinue', 'conTINUE', 'conTINUe', 'conTINuE', 'conTINue', 'conTInUE', 'conTInUe', 'conTInuE', 'conTInue', 'conTiNUE', 'conTiNUe', 'conTiNuE', 'conTiNue', 'conTinUE', 'conTinUe', 'conTinuE', 'conTinue', 'contINUE', 'contINUe', 'contINuE', 'contINue', 'contInUE', 'contInUe', 'contInuE', 'contInue', 'contiNUE', 'contiNUe', 'contiNuE', 'contiNue', 'continUE', 'continUe', 'continuE', 'DEF', 'DEf', 'DeF', 'Def', 'dEF', 'dEf', 'deF', 'DEL', 'DEl', 'DeL', 'Del', 'dEL', 'dEl', 'deL', 'ELIF', 'ELIf', 'ELiF', 'ELif', 'ElIF', 'ElIf', 'EliF', 'Elif', 'eLIF', 'eLIf', 'eLiF', 'eLif', 'elIF', 'elIf', 'eliF', 'ELSE', 'ELSe', 'ELsE', 'ELse', 'ElSE', 'ElSe', 'ElsE', 'Else', 'eLSE', 'eLSe', 'eLsE', 'eLse', 'elSE', 'elSe', 'elsE', 'EXCEPT', 'EXCEPt', 'EXCEpT', 'EXCEpt', 'EXCePT', 'EXCePt', 'EXCepT', 'EXCept', 'EXcEPT', 'EXcEPt', 'EXcEpT', 'EXcEpt', 'EXcePT', 'EXcePt', 'EXcepT', 'EXcept', 'ExCEPT', 'ExCEPt', 'ExCEpT', 'ExCEpt', 'ExCePT', 'ExCePt', 'ExCepT', 'ExCept', 'ExcEPT', 'ExcEPt', 'ExcEpT', 'ExcEpt', 'ExcePT', 'ExcePt', 'ExcepT', 'Except', 'eXCEPT', 'eXCEPt', 'eXCEpT', 'eXCEpt', 'eXCePT', 'eXCePt', 'eXCepT', 'eXCept', 'eXcEPT', 'eXcEPt', 'eXcEpT', 'eXcEpt', 'eXcePT', 'eXcePt', 'eXcepT', 'eXcept', 'exCEPT', 'exCEPt', 'exCEpT', 'exCEpt', 'exCePT', 'exCePt', 'exCepT', 'exCept', 'excEPT', 'excEPt', 'excEpT', 'excEpt', 'excePT', 'excePt', 'excepT', 'FINALLY', 'FINALLy', 'FINALlY', 'FINALly', 'FINAlLY', 'FINAlLy', 'FINAllY', 'FINAlly', 'FINaLLY', 'FINaLLy', 'FINaLlY', 'FINaLly', 'FINalLY', 'FINalLy', 'FINallY', 'FINally', 'FInALLY', 'FInALLy', 'FInALlY', 'FInALly', 'FInAlLY', 'FInAlLy', 'FInAllY', 'FInAlly', 'FInaLLY', 'FInaLLy', 'FInaLlY', 'FInaLly', 'FInalLY', 'FInalLy', 'FInallY', 'FInally', 'FiNALLY', 'FiNALLy', 'FiNALlY', 'FiNALly', 'FiNAlLY', 'FiNAlLy', 'FiNAllY', 'FiNAlly', 'FiNaLLY', 'FiNaLLy', 'FiNaLlY', 'FiNaLly', 'FiNalLY', 'FiNalLy', 'FiNallY', 'FiNally', 'FinALLY', 'FinALLy', 'FinALlY', 'FinALly', 'FinAlLY', 'FinAlLy', 'FinAllY', 'FinAlly', 'FinaLLY', 'FinaLLy', 'FinaLlY', 'FinaLly', 'FinalLY', 'FinalLy', 'FinallY', 'Finally', 'fINALLY', 'fINALLy', 'fINALlY', 'fINALly', 'fINAlLY', 'fINAlLy', 'fINAllY', 'fINAlly', 'fINaLLY', 'fINaLLy', 'fINaLlY', 'fINaLly', 'fINalLY', 'fINalLy', 'fINallY', 'fINally', 'fInALLY', 'fInALLy', 'fInALlY', 'fInALly', 'fInAlLY', 'fInAlLy', 'fInAllY', 'fInAlly', 'fInaLLY', 'fInaLLy', 'fInaLlY', 'fInaLly', 'fInalLY', 'fInalLy', 'fInallY', 'fInally', 'fiNALLY', 'fiNALLy', 'fiNALlY', 'fiNALly', 'fiNAlLY', 'fiNAlLy', 'fiNAllY', 'fiNAlly', 'fiNaLLY', 'fiNaLLy', 'fiNaLlY', 'fiNaLly', 'fiNalLY', 'fiNalLy', 'fiNallY', 'fiNally', 'finALLY', 'finALLy', 'finALlY', 'finALly', 'finAlLY', 'finAlLy', 'finAllY', 'finAlly', 'finaLLY', 'finaLLy', 'finaLlY', 'finaLly', 'finalLY', 'finalLy', 'finallY', 'FOR', 'FOr', 'FoR', 'For', 'fOR', 'fOr', 'foR', 'FROM', 'FROm', 'FRoM', 'FRom', 'FrOM', 'FrOm', 'FroM', 'From', 'fROM', 'fROm', 'fRoM', 'fRom', 'frOM', 'frOm', 'froM', 'GLOBAL', 'GLOBAl', 'GLOBaL', 'GLOBal', 'GLObAL', 'GLObAl', 'GLObaL', 'GLObal', 'GLoBAL', 'GLoBAl', 'GLoBaL', 'GLoBal', 'GLobAL', 'GLobAl', 'GLobaL', 'GLobal', 'GlOBAL', 'GlOBAl', 'GlOBaL', 'GlOBal', 'GlObAL', 'GlObAl', 'GlObaL', 'GlObal', 'GloBAL', 'GloBAl', 'GloBaL', 'GloBal', 'GlobAL', 'GlobAl', 'GlobaL', 'Global', 'gLOBAL', 'gLOBAl', 'gLOBaL', 'gLOBal', 'gLObAL', 'gLObAl', 'gLObaL', 'gLObal', 'gLoBAL', 'gLoBAl', 'gLoBaL', 'gLoBal', 'gLobAL', 'gLobAl', 'gLobaL', 'gLobal', 'glOBAL', 'glOBAl', 'glOBaL', 'glOBal', 'glObAL', 'glObAl', 'glObaL', 'glObal', 'gloBAL', 'gloBAl', 'gloBaL', 'gloBal', 'globAL', 'globAl', 'globaL', 'IF', 'If', 'iF', 'IMPORT', 'IMPORt', 'IMPOrT', 'IMPOrt', 'IMPoRT', 'IMPoRt', 'IMPorT', 'IMPort', 'IMpORT', 'IMpORt', 'IMpOrT', 'IMpOrt', 'IMpoRT', 'IMpoRt', 'IMporT', 'IMport', 'ImPORT', 'ImPORt', 'ImPOrT', 'ImPOrt', 'ImPoRT', 'ImPoRt', 'ImPorT', 'ImPort', 'ImpORT', 'ImpORt', 'ImpOrT', 'ImpOrt', 'ImpoRT', 'ImpoRt', 'ImporT', 'Import', 'iMPORT', 'iMPORt', 'iMPOrT', 'iMPOrt', 'iMPoRT', 'iMPoRt', 'iMPorT', 'iMPort', 'iMpORT', 'iMpORt', 'iMpOrT', 'iMpOrt', 'iMpoRT', 'iMpoRt', 'iMporT', 'iMport', 'imPORT', 'imPORt', 'imPOrT', 'imPOrt', 'imPoRT', 'imPoRt', 'imPorT', 'imPort', 'impORT', 'impORt', 'impOrT', 'impOrt', 'impoRT', 'impoRt', 'imporT', 'IN', 'In', 'iN', 'IS', 'Is', 'iS', 'LAMBDA', 'LAMBDa', 'LAMBdA', 'LAMBda', 'LAMbDA', 'LAMbDa', 'LAMbdA', 'LAMbda', 'LAmBDA', 'LAmBDa', 'LAmBdA', 'LAmBda', 'LAmbDA', 'LAmbDa', 'LAmbdA', 'LAmbda', 'LaMBDA', 'LaMBDa', 'LaMBdA', 'LaMBda', 'LaMbDA', 'LaMbDa', 'LaMbdA', 'LaMbda', 'LamBDA', 'LamBDa', 'LamBdA', 'LamBda', 'LambDA', 'LambDa', 'LambdA', 'Lambda', 'lAMBDA', 'lAMBDa', 'lAMBdA', 'lAMBda', 'lAMbDA', 'lAMbDa', 'lAMbdA', 'lAMbda', 'lAmBDA', 'lAmBDa', 'lAmBdA', 'lAmBda', 'lAmbDA', 'lAmbDa', 'lAmbdA', 'lAmbda', 'laMBDA', 'laMBDa', 'laMBdA', 'laMBda', 'laMbDA', 'laMbDa', 'laMbdA', 'laMbda', 'lamBDA', 'lamBDa', 'lamBdA', 'lamBda', 'lambDA', 'lambDa', 'lambdA', 'NOT', 'NOt', 'NoT', 'Not', 'nOT', 'nOt', 'noT', 'OR', 'Or', 'oR', 'PASS', 'PASs', 'PAsS', 'PAss', 'PaSS', 'PaSs', 'PasS', 'Pass', 'pASS', 'pASs', 'pAsS', 'pAss', 'paSS', 'paSs', 'pasS', 'PRINT', 'PRINt', 'PRInT', 'PRInt', 'PRiNT', 'PRiNt', 'PRinT', 'PRint', 'PrINT', 'PrINt', 'PrInT', 'PrInt', 'PriNT', 'PriNt', 'PrinT', 'Print', 'pRINT', 'pRINt', 'pRInT', 'pRInt', 'pRiNT', 'pRiNt', 'pRinT', 'pRint', 'prINT', 'prINt', 'prInT', 'prInt', 'priNT', 'priNt', 'prinT', 'RAISE', 'RAISe', 'RAIsE', 'RAIse', 'RAiSE', 'RAiSe', 'RAisE', 'RAise', 'RaISE', 'RaISe', 'RaIsE', 'RaIse', 'RaiSE', 'RaiSe', 'RaisE', 'Raise', 'rAISE', 'rAISe', 'rAIsE', 'rAIse', 'rAiSE', 'rAiSe', 'rAisE', 'rAise', 'raISE', 'raISe', 'raIsE', 'raIse', 'raiSE', 'raiSe', 'raisE', 'RETURN', 'RETURn', 'RETUrN', 'RETUrn', 'RETuRN', 'RETuRn', 'RETurN', 'RETurn', 'REtURN', 'REtURn', 'REtUrN', 'REtUrn', 'REtuRN', 'REtuRn', 'REturN', 'REturn', 'ReTURN', 'ReTURn', 'ReTUrN', 'ReTUrn', 'ReTuRN', 'ReTuRn', 'ReTurN', 'ReTurn', 'RetURN', 'RetURn', 'RetUrN', 'RetUrn', 'RetuRN', 'RetuRn', 'ReturN', 'Return', 'rETURN', 'rETURn', 'rETUrN', 'rETUrn', 'rETuRN', 'rETuRn', 'rETurN', 'rETurn', 'rEtURN', 'rEtURn', 'rEtUrN', 'rEtUrn', 'rEtuRN', 'rEtuRn', 'rEturN', 'rEturn', 'reTURN', 'reTURn', 'reTUrN', 'reTUrn', 'reTuRN', 'reTuRn', 'reTurN', 'reTurn', 'retURN', 'retURn', 'retUrN', 'retUrn', 'retuRN', 'retuRn', 'returN', 'TRY', 'TRy', 'TrY', 'Try', 'tRY', 'tRy', 'trY', 'WHILE', 'WHILe', 'WHIlE', 'WHIle', 'WHiLE', 'WHiLe', 'WHilE', 'WHile', 'WhILE', 'WhILe', 'WhIlE', 'WhIle', 'WhiLE', 'WhiLe', 'WhilE', 'While', 'wHILE', 'wHILe', 'wHIlE', 'wHIle', 'wHiLE', 'wHiLe', 'wHilE', 'wHile', 'whILE', 'whILe', 'whIlE', 'whIle', 'whiLE', 'whiLe', 'whilE', 'WITH', 'WITh', 'WItH', 'WIth', 'WiTH', 'WiTh', 'WitH', 'With', 'wITH', 'wITh', 'wItH', 'wIth', 'wiTH', 'wiTh', 'witH', 'YIELD', 'YIELd', 'YIElD', 'YIEld', 'YIeLD', 'YIeLd', 'YIelD', 'YIeld', 'YiELD', 'YiELd', 'YiElD', 'YiEld', 'YieLD', 'YieLd', 'YielD', 'Yield', 'yIELD', 'yIELd', 'yIElD', 'yIEld', 'yIeLD', 'yIeLd', 'yIelD', 'yIeld', 'yiELD', 'yiELd', 'yiElD', 'yiEld', 'yieLD', 'yieLd', 'yielD']

builtin_functions_list = [ 'None', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield','abs','ascii','bin','bool','chr','float','hex','id','input','len','max','min','oct','ord','print','round','sorted','str','sum','type','sqrt','tan','cos','sin','cos','ceil','floor','random','seed','randint',  'and', 'or','int','float','str']


class WrongNumArguError(Exception):
    pass

class NotSupportedError(Exception):
    pass

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
	    elif item in "%+-*/**==!=<=><>=andor" : operator += 1
	    elif item.replace('.', '', 1).lstrip('-').isdigit():operand += 1
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
        if item == "=": return True
        if item == "=>": return 0

def experssionErrorQuotation(token):
    if Counter(token)["'"] == 0 and Counter(token)['"'] == 0:
        return False
    elif Counter(token)["'"] == 2 or Counter(token)['"'] == 6:
        return False
    elif Counter(token)['"'] == 2 or Counter(token)['"'] == 6:
        return False
    elif Counter(token)["'"] != 2 or Counter(token)["'"] != 6:
        return True
    elif Counter(token)['"'] != 2 or Counter(token)['"'] != 6:
        return True





def compileFunction(e,code):
    excepName = type(e).__name__
    # Error which are not supported in the interactive P1
    if excepName == "NotSupportedError":
        res = {"error_name":"Not_Supported","error_message":str(e.args[0])+"'","error":"1","error_Type":"compile","line_no":e.args[1]}
        return jsonify(res)
    if excepName == "WrongNumArguError":
        res = {"error_name":"NumofArugments","error_message":str(data["NumofArugments"])+" '"+str(e.args[1])+"'","error":"1","error_Type":"compile","line_no":e.args[1]}
        return jsonify(res)

    # Indentation Error P2
    if str(excepName) == "IndentationError":
        res = {"error_name":"CodeBlockError","error_message":data["IndentationError"],"error":"1","error_Type":"compile","line_no":e.lineno}
        return jsonify(res)

    # Invalid keywords P3
    token = code.split('\n')
    if any(word in token[e.lineno-1] for word in keywords):
        res = {"error_name":"NameError","error_message":data["NameError_keywords"],"error":"1","error_Type":"compile","line_no":e.lineno}
        return jsonify(res)
    if any(word in token[e.lineno-1] for word in ['def','if','elif','else','while']):
        if not ':' in token[e.lineno-1]:
            res = {"error_name":"CodeBlockError","error_message":data["CodeBlockError"],"error":"1","error_Type":"compile","line_no":e.lineno}
            return jsonify(res)

    if not "=" in token[e.lineno-1]:
        token = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|[)(]{1}|.', ''.join(token[e.lineno-1].split()))
        if experssionErrorQuotation(token):
            res = {"error_name":"ExpressionError","error_message":data["experssionErrorQuotation"],"error":"1","error_Type":"compile","line_no":e.lineno}
            return jsonify(res)
        else:
            res = {"error_name":excepName,"error_message":str(e),"error":"1","error_Type":"compile","line_no":e.lineno}
            return jsonify(res)


    # Invalid expression for conditional statments (if elif while)
    if any(word in token[e.lineno-1] for word in ['if','elif','while']):
        token = token[e.lineno-1].split([i for i in ['if','elif','while'] if i in token[e.lineno-1]][-1])[1].split(':')[0]
        token = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|[)(]{1}|.', ''.join(token.split()))
        if experssionErrorEqual(token):
            res = {"error_name":"ExpressionError","error_message":data["experssionErrorEqual"],"error":"1","error_Type":"compile","line_no":e.lineno}
            return jsonify(res)
        elif experssionErrorEqual(token) == 0:
            res = {"error_name":"lambda_Not_Supported","error_message":data["lambda_Not_Supported"],"error":"1","error_Type":"compile","line_no":e.lineno}
            return jsonify(res)
        else:
            res = {"error_name":excepName,"error_message":str(e),"error":"1","error_Type":"compile","line_no":e.lineno}
            return jsonify(res)


    # Expression Errors P4
    token = code.split('\n')[e.lineno-1].strip().split('=')[1]
    if experssionErrorEqual(token):
        res = {"error_name":"ExpressionError","error_message":data["experssionErrorEqual"],"error":"1","error_Type":"compile","line_no":e.lineno}
        return jsonify(res)
    if len(token) == 0:
        res = {"error_name":excepName,"error_message":str(e),"error":"1","error_Type":"compile","line_no":e.lineno}
        return jsonify(res)
    token = re.findall(r'and?|or?|not?|True?|False?|\d*\.\d+|\d+|[-]{1}|[=><!]{1,2}|[*]+|[)(]{1}|.', ''.join(token.split()))
    if experssionErrorPar(token):
        res = {"error_name":"ExpressionError","error_message":data["experssionErrorPar"],"error":"1","error_Type":"compile","line_no":e.lineno}
        return jsonify(res)
    if experssionErrorQuotation(token):
        res = {"error_name":"ExpressionError","error_message":data["experssionErrorQuotation"],"error":"1","error_Type":"compile","line_no":e.lineno}
        return jsonify(res)
    if experssionErrorOperand(token):
        res = {"error_name":"ExpressionError","error_message":data["experssionErrorOperator"],"error":"1","error_Type":"compile","line_no":e.lineno}
        return jsonify(res)
    if experssionErrorOperator(token):
        res = {"error_name":"ExpressionError","error_message":data["experssionErrorOperator"],"error":"1","error_Type":"compile","line_no":e.lineno}
        return jsonify(res)
    else:
        res = {"error_name":excepName,"error_message":str(e),"error":"1","error_Type":"compile","line_no":e.lineno}
        return jsonify(res)




class nodevisitSeq(ast.NodeVisitor):
    # Supported nodes

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Num):
            globalfile.dict1.update({str(node.lineno):('Assign','Num',node.value.n,node.targets[0].id)})
        elif isinstance(node.value, ast.Str):
            globalfile.dict1.update({str(node.lineno):('Assign','Str',node.value.s,node.targets[0].id)})
        elif isinstance(node.value, ast.NameConstant):
            globalfile.dict1.update({str(node.lineno):('Assign','Str',str(node.value.value),node.targets[0].id)})
        else:
            var_names = [nodes.id for nodes in ast.walk(node) if isinstance(nodes, ast.Name)]
            var_names.pop(0)
            #variable name duplication removal example 1 a=-(-4) remove duplication of same varibale name as it is used to store and a=-(-a) will reatin variable name as it is used to load the value
            var_names = sorted(set(var_names))
            func_names = []
            for nodes in ast.walk(node):
                if 'func' in dir(nodes):
                    func_names.append(nodes.func.id)
                    var_names = [i for i in var_names if i != nodes.func.id]
            globalfile.dict1.update({str(node.lineno):('Assign','Expression',node.targets[0].id,var_names,func_names)})
            # if 'exec' in func_names or 'eval' in func_names:
            #     raise SyntaxError(data["evalExec"])
        self.generic_visit(node)
    def visit_Expr(self, node):
        try:
            if node.value.func.id in builtin_functions_list:
                var_names = [nodes.id for nodes in ast.walk(node) if isinstance(nodes, ast.Name)]
                var_names.pop(0)
                var_names = sorted(set(var_names))
                func_names = []
                for nodes in ast.walk(node):
                    if 'func' in dir(nodes):
                        func_names.append(nodes.func.id)
                        var_names = [i for i in var_names if i != nodes.func.id]
                globalfile.dict1.update({str(node.lineno):('Expr',node.value.func.id,node.value.func.id,var_names,func_names)})
            self.generic_visit(node)
        except:
            globalfile.dict1.update({str(node.lineno):('Expr','others','others','','',)})
            self.generic_visit(node)
    def visit_Call(self, node):
        if str(node.func.id) == "exec" or str(node.func.id) == "eval" or str(node.func.id) == "input":
            raise NotSupportedError(data["evalExec"],node.lineno,"Not Supported")
        # elif str(node.func.id) in ['math','random']:
        #     raise NotSupportedError(data["Warning"],node.lineno,"Warning")
        self.generic_visit(node)


   # Not Supported nodes
    def visit_Return(self,node):
       raise NotSupportedError(str('while ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_FunctionDef(self, node):
       raise NotSupportedError(str('function ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_If(self, node):
       raise NotSupportedError(str('if ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_While(self, node):
       raise NotSupportedError(str('while ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Import(self,node):
        raise NotSupportedError(str('import ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_ImportFrom(self,node):
        raise NotSupportedError(str('from ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Try(self,node):
        raise NotSupportedError(str('try ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Except(self,node):
        raise NotSupportedError(str('except ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Global(self,node):
        raise NotSupportedError(str('global ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Raise(self,node):
        raise NotSupportedError(str('raise ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_ClassDef(self,node):
        raise NotSupportedError(str('class ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_For(self,node):
        raise NotSupportedError(str('for ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_With(self,node):
        raise NotSupportedError(str('with ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_AsyncWith(self,node):
        raise NotSupportedError(str('asyncWith ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Assert(self,node):
        raise NotSupportedError(str('assert ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Dict(self,node):
        raise NotSupportedError(str('dict ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Set(self,node):
        raise NotSupportedError(str('set ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_ListComp(self,node):
        raise NotSupportedError(str('list_comprehension ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_SetComp(self,node):
        raise NotSupportedError(str('set_comprehension ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_DictComp(self,node):
        raise NotSupportedError(str('dict_comprehension ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_GeneratorExp(self,node):
        raise NotSupportedError(str('generator ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Await(self,node):
        raise NotSupportedError(str('await ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Yield(self,node):
        raise NotSupportedError(str('yield ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_JoinedStr(self,node):
        raise NotSupportedError(str('join ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Bytes(self,node):
        raise NotSupportedError(str('Bytes ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_List(self,node):
        raise NotSupportedError(str('list ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Tuple(self,node):
        raise NotSupportedError(str('tuple ')+str(data["Not_Supported"]),node.lineno,'Not Supported')

class nodevisit_func(ast.NodeVisitor):
    # Supported nodes
    def visit_Assign(self, node):
        if isinstance(node.value, ast.Num):
            globalfile.dict1.update({str(node.lineno):('Assign','Num',node.value.n,node.targets[0].id)})
        elif isinstance(node.value, ast.Str):
            globalfile.dict1.update({str(node.lineno):('Assign','Str',node.value.s,node.targets[0].id)})
        elif isinstance(node.value, ast.NameConstant):
            globalfile.dict1.update({str(node.lineno):('Assign','Str',str(node.value.value),node.targets[0].id)})
        else:
            var_names = [nodes.id for nodes in ast.walk(node) if isinstance(nodes, ast.Name)]
            var_names.pop(0)
            #variable name duplication removal example 1 a=-(-4) remove duplication of same varibale name as it is used to store and a=-(-a) will reatin variable name as it is used to load the value
            var_names = sorted(set(var_names))
            func_names = []
            for nodes in ast.walk(node):
                if 'func' in dir(nodes):
                    func_names.append(nodes.func.id)
                    var_names = [i for i in var_names if i != nodes.func.id]
            globalfile.dict1.update({str(node.lineno):('Assign','Expression',node.targets[0].id,var_names,func_names)})
            # if 'exec' in func_names or 'eval' in func_names:
            #     raise SyntaxError(data["evalExec"])
        self.generic_visit(node)
    def visit_Expr(self, node):
        # print(ast.dump(node))
        try:
            if node.value.func.id in builtin_functions_list:
                var_names = [nodes.id for nodes in ast.walk(node) if isinstance(nodes, ast.Name)]
                var_names.pop(0)
                var_names = sorted(set(var_names))
                func_names = []
                for nodes in ast.walk(node):
                    if 'func' in dir(nodes):
                        func_names.append(nodes.func.id)
                        var_names = [i for i in var_names if i != nodes.func.id]
                globalfile.dict1.update({str(node.lineno):('Expr',node.value.func.id,node.value.func.id,var_names,func_names)})
            self.generic_visit(node)
        except:
            globalfile.dict1.update({str(node.lineno):('Expr','others','others','','',)})
            self.generic_visit(node)
    def visit_Call(self, node):
        if str(node.func.id) == "exec" or str(node.func.id) == "eval" or str(node.func.id) == "input":
            raise NotSupportedError(data["evalExec"],node.lineno,"Not Supported")
        if not str(node.func.id) in builtin_functions_list:
            no_of_args = []
            no_of_args_values = []
            for nos in ast.walk(node):
                if isinstance(nos,ast.Str):
                   no_of_args.append(nos.s)
                elif isinstance(nos , ast.Num):
                   no_of_args.append(nos.n)
                elif isinstance(nos,ast.NameConstant):
                    no_of_args.append(nos.value)
                elif isinstance(nos,ast.Name):
                    no_of_args.append(nos.id)
            for nos in ast.walk(node):
                if isinstance(nos,ast.Str):
                   no_of_args_values.append(nos.s)
                elif isinstance(nos , ast.Num):
                   no_of_args_values.append(nos.n)
                elif isinstance(nos,ast.NameConstant):
                    no_of_args_values.append(nos.value)
            no_of_args.remove(str(node.func.id))
            var_names = [nodes1.id for nodes1 in ast.walk(node) if isinstance(nodes1, ast.Name)]
            var_names.pop(0)
            func_names = []
            for nodes in ast.walk(node):
                if 'func' in dir(nodes):
                    func_names.append(nodes.func.id)
                    var_names = [i for i in var_names if i != nodes.func.id]
            # values = [nodes1.id for nodes1 in ast.walk(nodes.test) if isinstance(nodes1, ast.s) or isinstance(nodes1,ast.n)]
            func_names.remove(str(node.func.id))
            # print(globalfile.dict1)
            globalfile.dict1.update({str(node.lineno):('FunctionCall','FunctionCall',[str(node.func.id)],no_of_args,no_of_args_values,var_names,func_names)})
            # print(globalfile.dict1)

        self.generic_visit(node)
    def visit_FunctionDef(self, node):
       no_of_args = [nos.arg for nos in ast.walk(node.args) if isinstance(nos,ast.arg)]
       if len(no_of_args) > 3:
           raise WrongNumArguError(data['NumofArugments'],node.lineno,"Not Supported")
       globalfile.dict1.update({str(node.lineno):('FunctionDef','FunctionDef',node.name,no_of_args,[])})
       self.generic_visit(node)
    def visit_Return(self,node):
    #    print(ast.dump(node))
       self.generic_visit(node)


    # Not Supported nodes
    # def visit_Return(self,node):
    #    raise NotSupportedError(str('while ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Import(self,node):
        raise NotSupportedError(str('import ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_ImportFrom(self,node):
        raise NotSupportedError(str('from ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Try(self,node):
        raise NotSupportedError(str('try ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Except(self,node):
        raise NotSupportedError(str('except ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Global(self,node):
        raise NotSupportedError(str('global ')+str(data["UnSupportedNodes"]),node.lineno,'Not Supported')
    def visit_Raise(self,node):
        raise NotSupportedError(str('raise ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_ClassDef(self,node):
        raise NotSupportedError(str('class ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_For(self,node):
        raise NotSupportedError(str('for ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_With(self,node):
        raise NotSupportedError(str('with ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_AsyncWith(self,node):
        raise NotSupportedError(str('asyncWith ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Assert(self,node):
        raise NotSupportedError(str('assert ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Dict(self,node):
        raise NotSupportedError(str('dict ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Set(self,node):
        raise NotSupportedError(str('set ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_ListComp(self,node):
        raise NotSupportedError(str('list_comprehension ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_SetComp(self,node):
        raise NotSupportedError(str('set_comprehension ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_DictComp(self,node):
        raise NotSupportedError(str('dict_comprehension ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_GeneratorExp(self,node):
        raise NotSupportedError(str('generator ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Await(self,node):
        raise NotSupportedError(str('await ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Yield(self,node):
        raise NotSupportedError(str('yield ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_JoinedStr(self,node):
        raise NotSupportedError(str('join ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Bytes(self,node):
        raise NotSupportedError(str('Bytes ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_List(self,node):
        raise NotSupportedError(str('list ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Tuple(self,node):
        raise NotSupportedError(str('tuple ')+str(data["Not_Supported"]),node.lineno,'Not Supported')

class nodevisit_cond(ast.NodeVisitor):
    # Supported nodes
    def visit_Assign(self, node):
        if isinstance(node.value, ast.Num):
            globalfile.dict1.update({str(node.lineno):('Assign','Num',node.value.n,node.targets[0].id)})
        elif isinstance(node.value, ast.Str):
            globalfile.dict1.update({str(node.lineno):('Assign','Str',node.value.s,node.targets[0].id)})
        elif isinstance(node.value, ast.NameConstant):
            globalfile.dict1.update({str(node.lineno):('Assign','Str',str(node.value.value),node.targets[0].id)})
        else:
            var_names = [nodes.id for nodes in ast.walk(node) if isinstance(nodes, ast.Name)]
            var_names.pop(0)
            #variable name duplication removal example 1 a=-(-4) remove duplication of same varibale name as it is used to store and a=-(-a) will reatin variable name as it is used to load the value
            var_names = sorted(set(var_names))
            func_names = []
            for nodes in ast.walk(node):
                if 'func' in dir(nodes):
                    func_names.append(nodes.func.id)
                    var_names = [i for i in var_names if i != nodes.func.id]
            globalfile.dict1.update({str(node.lineno):('Assign','Expression',node.targets[0].id,var_names,func_names)})
            # if 'exec' in func_names or 'eval' in func_names:
            #     raise SyntaxError(data["evalExec"])
        self.generic_visit(node)
    def visit_Expr(self, node):
        # print(ast.dump(node))
        try:
            if node.value.func.id in builtin_functions_list:
                var_names = [nodes.id for nodes in ast.walk(node) if isinstance(nodes, ast.Name)]
                var_names.pop(0)
                var_names = sorted(set(var_names))
                func_names = []
                for nodes in ast.walk(node):
                    if 'func' in dir(nodes):
                        func_names.append(nodes.func.id)
                        var_names = [i for i in var_names if i != nodes.func.id]
                globalfile.dict1.update({str(node.lineno):('Expr',node.value.func.id,node.value.func.id,var_names,func_names)})
            self.generic_visit(node)
        except:
            globalfile.dict1.update({str(node.lineno):('Expr','others','others','','',)})
            self.generic_visit(node)
    def visit_Call(self, node):
        if str(node.func.id) == "exec" or str(node.func.id) == "eval" or str(node.func.id) == "input":
            raise NotSupportedError(data["evalExec"],node.lineno,"Not Supported")
        if not str(node.func.id) in builtin_functions_list:
            no_of_args = []
            no_of_args_values = []
            for nos in ast.walk(node):
                if isinstance(nos,ast.Str):
                   no_of_args.append(nos.s)
                elif isinstance(nos , ast.Num):
                   no_of_args.append(nos.n)
                elif isinstance(nos,ast.NameConstant):
                    no_of_args.append(nos.value)
                elif isinstance(nos,ast.Name):
                    no_of_args.append(nos.id)
            for nos in ast.walk(node):
                if isinstance(nos,ast.Str):
                   no_of_args_values.append(nos.s)
                elif isinstance(nos , ast.Num):
                   no_of_args_values.append(nos.n)
                elif isinstance(nos,ast.NameConstant):
                    no_of_args_values.append(nos.value)
            no_of_args.remove(str(node.func.id))
            var_names = [nodes1.id for nodes1 in ast.walk(node) if isinstance(nodes1, ast.Name)]
            var_names.pop(0)
            func_names = []
            for nodes in ast.walk(node):
                if 'func' in dir(nodes):
                    func_names.append(nodes.func.id)
                    var_names = [i for i in var_names if i != nodes.func.id]
            # values = [nodes1.id for nodes1 in ast.walk(nodes.test) if isinstance(nodes1, ast.s) or isinstance(nodes1,ast.n)]
            func_names.remove(str(node.func.id))
            # print(globalfile.dict1)
            globalfile.dict1.update({str(node.lineno):('FunctionCall','FunctionCall',[str(node.func.id)],no_of_args,no_of_args_values,var_names,func_names)})
            # print(globalfile.dict1)

        self.generic_visit(node)
    def visit_FunctionDef(self, node):
       no_of_args = [nos.arg for nos in ast.walk(node.args) if isinstance(nos,ast.arg)]
       if len(no_of_args) > 3:
           raise WrongNumArguError(data['NumofArugments'],node.lineno,"Not Supported")
       globalfile.dict1.update({str(node.lineno):('FunctionDef','FunctionDef',node.name,no_of_args,[])})
       self.generic_visit(node)
    def visit_If(self, node):
        for nodes in ast.walk(node):
            if isinstance(nodes, ast.If):
                if 'value' in dir(nodes.test):
                    globalfile.dict1.update({str(node.lineno):('If','NameConstant','others',str(nodes.test.value),'',)})
                    break
                elif 'id' in dir(nodes.test):
                    globalfile.dict1.update({str(node.lineno):('If','Name','others',[nodes.test.id],'',)})
                    break
                else:
                    var_names = [nodes1.id for nodes1 in ast.walk(nodes.test) if isinstance(nodes1, ast.Name)]
                    var_names = sorted(set(var_names))
                    func_names = []
                    for nodes1 in ast.walk(nodes.test):
                        if 'func' in dir(nodes1):
                            func_names.append(nodes1.func.id)
                            var_names = [i for i in var_names if i != nodes1.func.id]
                    globalfile.dict1.update({str(node.lineno):('If','Expression','others',var_names,func_names)})
                    break
        self.generic_visit(node)
    def visit_Return(self,node):
    #    print(ast.dump(node))
       self.generic_visit(node)
    def visit_While(self, node):
        for nodes in ast.walk(node):
            if isinstance(nodes, ast.While):
                if 'value' in dir(nodes.test):
                    globalfile.dict1.update({str(node.lineno):('While','Name','others',str(nodes.test.value),'',)})
                    break
                elif 'id' in dir(nodes.test):
                    globalfile.dict1.update({str(node.lineno):('While','NameConstant','others',[nodes.test.id],'',)})
                    break
                else:
                    var_names = [nodes1.id for nodes1 in ast.walk(nodes.test) if isinstance(nodes1, ast.Name)]
                    var_names = sorted(set(var_names))
                    func_names = []
                    for nodes1 in ast.walk(nodes.test):
                        if 'func' in dir(nodes1):
                            func_names.append(nodes1.func.id)
                            var_names = [i for i in var_names if i != nodes1.func.id]
                    globalfile.dict1.update({str(node.lineno):('While','Expression','others',var_names,func_names)})
                    break
        self.generic_visit(node)


   # Not Supported nodes
    # def visit_Return(self,node):
    #    raise NotSupportedError(str('while ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Import(self,node):
        raise NotSupportedError(str('import ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_ImportFrom(self,node):
        raise NotSupportedError(str('from ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Try(self,node):
        raise NotSupportedError(str('try ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Except(self,node):
        raise NotSupportedError(str('except ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    # def visit_Global(self,node):
    #     raise NotSupportedError(str('global ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Raise(self,node):
        raise NotSupportedError(str('raise ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_ClassDef(self,node):
        raise NotSupportedError(str('class ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_For(self,node):
        raise NotSupportedError(str('for ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_With(self,node):
        raise NotSupportedError(str('with ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_AsyncWith(self,node):
        raise NotSupportedError(str('asyncWith ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Assert(self,node):
        raise NotSupportedError(str('assert ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Dict(self,node):
        raise NotSupportedError(str('dict ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Set(self,node):
        raise NotSupportedError(str('set ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_ListComp(self,node):
        raise NotSupportedError(str('list_comprehension ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_SetComp(self,node):
        raise NotSupportedError(str('set_comprehension ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_DictComp(self,node):
        raise NotSupportedError(str('dict_comprehension ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_GeneratorExp(self,node):
        raise NotSupportedError(str('generator ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Await(self,node):
        raise NotSupportedError(str('await ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Yield(self,node):
        raise NotSupportedError(str('yield ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_JoinedStr(self,node):
        raise NotSupportedError(str('join ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Bytes(self,node):
        raise NotSupportedError(str('Bytes ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_List(self,node):
        raise NotSupportedError(str('list ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
    def visit_Tuple(self,node):
        raise NotSupportedError(str('tuple ')+str(data["Not_Supported"]),node.lineno,'Not Supported')
