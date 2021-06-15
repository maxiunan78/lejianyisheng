#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os
from decimal import *
inputlist = []

option_responsibility1 = ['0','1']
option_responsibility2 = ['0','1']
option_responsibility3 = ['0','1']

inputlist = []

def get_tumor_fee(mainfee1,v):
	# print v
	# fee  = mainfee1*v/100*0.95
	# print fee
	rumor_fee = Decimal(str(mainfee1))*Decimal(str(v))/Decimal(str(100))*Decimal(str(0.95))
	tumor_fee = Decimal(rumor_fee).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
	print rumor_fee
	return tumor_fee
	# print type(tumor_fee)

def get_hospital_fee(mainfee,C_p,val):
	hospital_fee = Decimal(str(mainfee))*Decimal(str(C_p))*Decimal(str(val))*Decimal(str(0.95))
	hospital_fee = hospital_fee.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
	return hospital_fee

def get_emergency_fee(optional_fee, facor, C_p):
	emergency_fee = Decimal(str(optional_fee))*Decimal(str(facor))*Decimal(str(C_p))*Decimal(str(0.95))
	emergency_fee = emergency_fee.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
	return emergency_fee



# def get_optional_fee(opfee,)
# def get_totalfee(resp,amount,mainfee,optional1fee,optional2fee,optional3fee):
#
#
# 		if (resp == []):
# 			respect_fee = mainfee
# 			# print mainfee
# 			print(resp)
# 			respect_fee = Decimal(str(respect_fee)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
# 			# print("当前保额:%f,当前总保费:%f" % (amount, respect_fee))
# 			return resp,respect_fee
#
#
# 		if (resp == ["B10018"]):
# 			respect_fee = mainfee + optional1fee*mainfee*0.001
# 			print(resp)
# 			print(mainfee)
# 			print (optional1fee*mainfee*0.001)
# 			print("111111111当前保额:%f,当前总保费:%f" % (amount, respect_fee))
# 			respect_fee = Decimal(str(respect_fee)).quantize(Decimal('0.00'),rounding=ROUND_HALF_UP)
# 			return resp,respect_fee
#
#
# 		if (resp == ["B10016"]):
# 			respect_fee = mainfee + optional2fee
# 			print(resp)
# 			respect_fee = Decimal(str(respect_fee)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
# 			# print("当前保额:%f,当前总保费:%f" % (amount, respect_fee))
# 			return resp,respect_fee
#
#
# 		if (resp == ["B10017"]):
# 			respect_fee = mainfee + optional3fee
# 			print(resp)
# 			respect_fee = Decimal(str(respect_fee)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
# 			# print("当前保额:%f,当前总保费:%f" % (amount, respect_fee))
# 			return resp,respect_fee
#
#
#
# 		if (resp == ["B10018", "B10016"]):
# 			respect_fee = mainfee + optional2fee + optional1fee*(mainfee + optional2fee)*0.001
# 			print(resp)
# 			# print("当前保额:%f,当前总保费:%f" % (amount, respect_fee))
# 			respect_fee = Decimal(str(respect_fee)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
# 			return resp, respect_fee
#
#
# 		if (resp == ["B10018", "B10017"]):
# 			respect_fee = mainfee + optional1fee*(mainfee + optional3fee)*0.001 +  optional3fee
# 			print(resp)
# 			respect_fee = Decimal(str(respect_fee)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
# 			# print("当前保额:%f,当前总保费:%f" % (amount, respect_fee))
# 			return resp, respect_fee
#
#
# 		if (resp == ["B10016", "B10017"]):
# 			respect_fee = mainfee + optional2fee +  optional3fee
# 			print(resp)
# 			# print("当前保额:%f,当前总保费:%f" % (amount, respect_fee))
# 			return resp,round(respect_fee,2)
#
#
#
# 		if (resp == ["B10018", "B10016", "B10017"]):
# 			respect_fee = mainfee + optional2fee +  optional3fee + optional1fee*(mainfee + optional2fee + optional3fee)*0.001
# 			print(resp)
# 			# print("当前保额:%f,当前总保费:%f" % (amount, respect_fee))
# 			return resp,round(respect_fee,2)


# if __name__ == '__main__':
# 	getResponsibility()