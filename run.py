# !/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import os
import utils.send as send
import unittest
import  utils.responsibility as res
import logging
import pyexcel as py
import requests
import json
import pdb
import copy
# from utils import send
import datetime
import time

import utils.excelUtil as ex
# import utils.plan

proDir =  r"C:\Users\Administrator\Documents\lejianyisheng"
# print os.getcwd()
# print os.path.join(os.getcwd())
# print proDir
xlsxPath = os.path.join(proDir, "data", "fee.xlsx")
resultPath = os.path.join(proDir,'data')
log_path = r"C:\Users\Administrator\Documents\lejianyisheng\sys.log"
print(xlsxPath)

# class Logger(object):
#     def __init__(self, logFile='Default.log'):
#         self.terminal = sys.stdout
#         self.log = open(logFile,'a')
#
#     def write(self,message):
#         self.terminal.write(message)
#         self.log.write(message)
#
#     def flush(self):
#         pass



class TestUnderwriting(unittest.TestCase):
    """测试趸交"""

    def setUp(self):
        # sys.stdout = Logger("log.log")

        logPath = os.path.join(resultPath, str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        if not os.path.exists(logPath):
            os.mkdir(logPath)


        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler(os.path.join(logPath, "my.log"))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.logger.info("开始了")
        self.num = 0
        # self.gender = ['M', 'F']
        self.productCode1 =  ['10270831']
        # 赔付比例
        self.Compensation_proportion = [1,0.9,0.8,0.7,0.6,0.5]
        # self.Compensation_proportion = [0.9]
        # 日津贴
        self.Daily_allowance = {'1':100,'2':100,'3':150,'4':150,'5':150,'6':200,'7':200,'8':300}
        # self.Daily_allowance = {'1': 100}
        self.social = ['0','1']
        #门急诊免赔额方式,0按年，1按照次数
        self.way = ["year","time"]
        #住院年免赔额：调整因子
        self.hospital = {'0':1,'5000':0.7,'10000':0.6,'15000':0.55,'20000':0.5}
        # self.hospital = {'0': 1}
        #门急诊年免赔额：调整因子
        self.emergency_year = {'0':1,'200':0.96,'500':0.92,'1300':0.8}
        # self.emergency_year = {'0': 1}
        self.optional =  [0,1]
        # 门急诊年免赔额：门诊普通部次免赔额调整因子,门诊特需部次免赔额调整因子
        self.emergency_time = {'0':[1,1],'50':[0.89,0.95],'100':[0.79,0.9],'200':[0.62,0.8],'500':[0.35,0.65]}
        # self.emergency_time = {'500': [0.35, 0.65]}
        # 套餐
        # self.set_meal = [1,2,3,4]
        self.plan = [1,2,3,4,5,6,7,8]
        self.productCode=["10270982","10270983","10270984","10270985","10270986","10270987","10270988","10270989"]
        self.age = range(0,55,1)
        self.has_optional=[1,0]

        print('test start1')

    def test_a(self):
        """测试含有可选计划时的保费"""
        # gole_payment = []

            # for g in self.gender:
            #     print("性别:%s" %g)
        for a in self.age:
            print ("年龄：%d" %a )
            print ("*****************************************************")
            for p in self.plan:
                if p == 1:
                    pcode = "10270982"
                if p == 2:
                    self.logger.info(pcode)
                    pcode = "10270983"
                    self.logger.info("now:" + pcode)
                if p == 3:
                    pcode = "10270984"
                if p == 4:
                    pcode = "10270985"
                if p == 5:
                    pcode = "10270986"
                if p == 6:
                    pcode = "10270987"
                if p == 7:
                    pcode = "10270988"
                if p == 8:
                    pcode = "10270989"
                self.logger.info("计划%d" % p)
                print ("计划%d" % p)
                if p in [1, 2, 3, 4]:
                    # set_meal = [1, 2]
                    set_meal = [1]
                if p in [5, 6, 7, 8]:
                    # set_meal = [1, 2, 3, 4]
                    set_meal = [1]
                # print set_meal
                for (k,v) in self.Daily_allowance.items():
                    if p == int(k):
                        print("津贴：%s" %(v))
                        mainfee1 = ex.get_mainfee1(xlsxPath, u'津贴', start_row=2, age=a)
                        tumor_fee = res.get_tumor_fee(mainfee1,v)
                        # print tumor_fee
                        print("恶性肿瘤住院津贴主险费:%f" % tumor_fee)
                    else:
                        continue


                    for so in self.social:
                        if so == '1':
                            print"有社保"
                        else:
                            print"无社保"

                        mainfee = ex.get_mainfee(xlsxPath, u'住院', start_row=2, plan=p, age=a, so=so)
                        # print mainfee
                        for C_p in self.Compensation_proportion:
                            print("*****************")
                            print("赔付比例：%f" % C_p)
                            print("*****************")

                            for (key, val) in self.hospital.items():
                                print("住院年免赔额: %s" % key)
                                hospital_fee = res.get_hospital_fee(C_p=C_p, mainfee=mainfee, val=val)
                                print("一般住院医疗保险金责任费用:%f" % hospital_fee)
                                print("*******************************")

                                for se in set_meal:
                                    print("套餐:%d" % se)
                                    optional_fee = ex.get_option_fee(xlsxPath, u'门诊', start_row=2, se=se, age=a, so=so)
                                    for w in self.way:
                                        if w == "year":
                                        # print("门急诊按照年免赔")
                                            facor = self.emergency_year
                                            for (k, va) in facor.items():
                                                print("门急诊年免赔额：%s,调整比例：%f" % (k, va))
                                                emergency_fee = res.get_emergency_fee(optional_fee, facor=va, C_p=C_p)
                                                print("门急诊按年免赔，费用：%f" % emergency_fee)
                                                respct_total_fee = emergency_fee + tumor_fee + hospital_fee
                                                print("总保费：%f" % respct_total_fee)
                                                print("########")
                                                data = {
                                                # // 被保人年龄
                                                "age": a,
                                                # // 保障期限
                                                "insurePeriod": "1",
                                                # // 保障期限类型，3：年
                                                "insurePeriodType": "3",
                                                # // 产品编码
                                                "productCode": pcode,
                                                # // 一般住院年免赔额
                                                "hospitalizationDeductiblePerYear": key,
                                                # // 赔付比例因子
                                                "compensationProportion": C_p,
                                                # // 门急诊 【0：不投保 | 1：套餐一 | | 2：套餐二 | | 3：套餐三 | | 4：套餐四 |】
                                                "outpatientAndEmergency": se,
                                                # // 门急诊免赔额方式【year：按年 | time：按次】
                                                "outpatientAndEmergencyDeductibleWay": w,
                                                # // 年免赔额（二选一）
                                                "outpatientAndEmergencyDeductiblePerYear": k,

                                                # // 社保标识【0：无 | 1：有】
                                                "social": so,
                                                # // 缴费期限，1000：趸交
                                                "paymentPeriod": "1000"
                                            }
                                                print (json.dumps(data, encoding="UTF-8", ensure_ascii=False, sort_keys=False,indent=1))
                                                retext = send.senddatas(data)
                                            # print (retext.text)
                                                outputdata = json.loads(retext.text)["body"]["payment"]
                                                times = str(datetime.datetime.now().hour) + ":" + str(
                                                        datetime.datetime.now().minute) + ":" + str(
                                                        datetime.datetime.now().second)
                                                retval = os.getcwd()
                                                fileDay = time.strftime("%Y%m%d", time.localtime())
                                                file = open(retval + '/logs/' + fileDay + '.txt', 'a+')
                                                file.write("\n\n----------%s----------有可选计划"
                                                            "\n计划:%d    套餐：%d    年龄：%d    社保：%s\n"
                                                            "住院免赔额：%s   门诊免赔方式：%s   门诊免赔额：%s   赔付比例：%f\n"
                                                            "接口返回结果：%s    计算结果：%f\n" % (times, p, se, a,so,key,w,k,C_p,outputdata,respct_total_fee))
                                                file.close()
                                                if (respct_total_fee != outputdata):
                                                    print (respct_total_fee, outputdata)
                                                    print(float(outputdata))
                                                # with self.subTest():
                                                # print (str(float(respect_total_fee)).split('.')[1])
                                                    number = len(str(float(respct_total_fee)).split('.')[1])
                                                    if number == 1:
                                                        finalfee = str(float(respct_total_fee)) + "0"
                                                    else:
                                                        finalfee = str(float(respct_total_fee))
                                                    self.assertEqual(finalfee, outputdata, msg="222")



                                        else:
                                            print("门急诊按照次免赔")
                                            facor = self.emergency_time
                                            for (k, va) in facor.items():
                                                # print se
                                                # print k,va
                                                if (se == 1 or se == 2):
                                                    factor = va[0]
                                                    print factor
                                                if (se == 3 or se == 4):
                                                    factor = va[1]
                                                    print factor
                                                print("门急诊次免赔额：%s,调整比例：%f" % (k, factor))
                                                emergency_fee = res.get_emergency_fee(optional_fee, facor=factor, C_p=C_p)
                                                print("门急诊按次免赔，费用：%f" % emergency_fee)
                                                respct_total_fee = emergency_fee + tumor_fee + hospital_fee
                                                print("总保费：%f" % respct_total_fee)
                                                print("###############")
                                                data = {
                                                # // 被保人年龄
                                                "age": a,
                                                # // 保障期限
                                                "insurePeriod": "1",
                                                # // 保障期限类型，3：年
                                                "insurePeriodType": "3",
                                                # // 产品编码
                                                "productCode": pcode,
                                                # // 一般住院年免赔额
                                                "hospitalizationDeductiblePerYear": key,
                                                # // 赔付比例因子
                                                "compensationProportion": C_p,
                                                # // 门急诊 【0：不投保 | 1：套餐一 | | 2：套餐二 | | 3：套餐三 | | 4：套餐四 |】
                                                "outpatientAndEmergency": se,
                                                   # // 门急诊免赔额方式【year：按年 | time：按次】
                                                "outpatientAndEmergencyDeductibleWay": w,

                                            # // 次免赔额
                                                "outpatientAndEmergencyDeductiblePerTime": k,
                                                # // 社保标识【0：无 | 1：有】
                                                "social": so,
                                                # // 缴费期限，1000：趸交
                                                "paymentPeriod": "1000"
                                            }
                                                print (json.dumps(data, encoding="UTF-8", ensure_ascii=False, sort_keys=False,indent=1))
                                                retext = send.senddatas(data)
                                            # print (retext.text)
                                                outputdata = json.loads(retext.text)["body"]["payment"]
                                                times = str(datetime.datetime.now().hour) + ":" + str(
                                                        datetime.datetime.now().minute) + ":" + str(
                                                        datetime.datetime.now().second)
                                                retval = os.getcwd()
                                                fileDay = time.strftime("%Y%m%d", time.localtime())
                                                file = open(retval + '/logs/' + fileDay + '.txt', 'a+')
                                                file.write("\n\n----------%s----------"
                                                            "\n计划:%d    套餐：%d    年龄：%d    社保：%s\n"
                                                            "住院免赔额：%s   门诊免赔方式：%s   门诊免赔额：%s   赔付比例：%f\n"
                                                            "接口返回结果：%s    计算结果：%f\n" % (times, p, se, a,so,key,w,k,C_p,outputdata,respct_total_fee))
                                                file.close()
                                                if (respct_total_fee != outputdata):
                                                    print (respct_total_fee, outputdata)
                                                    print(float(outputdata))
                                                # with self.subTest():
                                                # print (str(float(respect_total_fee)).split('.')[1])
                                                    number = len(str(float(respct_total_fee)).split('.')[1])
                                                    if number == 1:
                                                        finalfee = str(float(respct_total_fee)) + "0"
                                                    else:
                                                        finalfee = str(float(respct_total_fee))
                                                    self.assertEqual(finalfee, outputdata, msg="222")

    def test_b(self):
        """测试不含可选计划的保费"""
        for a in self.age:
            print ("年龄：%d" %a )
            print ("*****************************************************")
            for p in self.plan:
                if p == 1:
                    pcode = "10270982"
                if p == 2:
                    pcode = "10270983"
                if p == 3:
                    pcode = "10270984"
                if p == 4:
                    pcode = "10270985"
                if p == 5:
                    pcode = "10270986"
                if p == 6:
                    pcode = "10270987"
                if p == 7:
                    pcode = "10270988"
                if p == 8:
                    pcode = "10270989"



                print ("计划%d" % p)
                if p in [1,2,3,4]:
                    set_meal=[1,2]
                if p in [5,6,7,8]:
                    set_meal=[1,2,3,4]
                # print set_meal
                for (k,v) in self.Daily_allowance.items():
                #     print p
                #     print k
                    if p == int(k):
                        print("津贴：%s" %(self.Daily_allowance[str(p)]))
                        mainfee1 = ex.get_mainfee1(xlsxPath, u'津贴', start_row=2, age=a)
                        tumor_fee = res.get_tumor_fee(mainfee1,v=self.Daily_allowance[str(p)])
                        # print tumor_fee
                        print("恶性肿瘤住院津贴主险费:%f" % tumor_fee)
                    else:
                        continue
                    for so in self.social:
                        if so == '1':
                            print"有社保"
                        else:
                            print"无社保"

                        mainfee = ex.get_mainfee(xlsxPath, u'住院', start_row=2, plan=p, age=a, so=so)
                        for C_p in self.Compensation_proportion:
                            print("*****************")
                            print("赔付比例：%f" % C_p)
                            print("*****************")

                            for (key, val) in self.hospital.items():
                                print("住院年免赔额: %s" % key)
                                hospital_fee = res.get_hospital_fee(C_p=C_p, mainfee=mainfee, val=val)
                                print("一般住院医疗保险金责任费用:%f" % hospital_fee)
                                respect_total_fee = tumor_fee + hospital_fee
                                print("预期总保费:%s" % respect_total_fee)
                                print("******************")
                            # print("*******************************")

                                data = {
	                                # // 被保人年龄
	                            "age": a,
	                                # // 保障期限
	                            "insurePeriod": "1",
	# // 保障期限类型，3：年
	                            "insurePeriodType": "3",
	# // 产品编码
	                            "productCode": pcode,
	# // 一般住院年免赔额
	                            "hospitalizationDeductiblePerYear": key,
	# // 赔付比例因子
	                            "compensationProportion": C_p,
	# // 门急诊 【0：不投保 | 1：套餐一 | | 2：套餐二 | | 3：套餐三 | | 4：套餐四 |】
	                            "outpatientAndEmergency": 0,
	# // 社保标识【0：无 | 1：有】
	                            "social": so,
	# // 缴费期限，1000：趸交
	                            "paymentPeriod": "1000"
                                }
                                print (json.dumps(data,encoding="UTF-8", ensure_ascii=False, sort_keys=False, indent=1))
                                retext = send.senddatas(data)
                                # print (retext.text)
                                outputdata = json.loads(retext.text)["body"]["payment"]
                                times = str(datetime.datetime.now().hour) + ":" + str(
                                    datetime.datetime.now().minute) + ":" + str(
                                    datetime.datetime.now().second)
                                retval = os.getcwd()
                                fileDay = time.strftime("%Y%m%d", time.localtime())
                                file = open(retval + '/logs/' + fileDay + '.txt', 'a+')
                                file.write("\n\n----------%s----------"
                                           "\n计划:%d       年龄：%d    社保：%s\n"
                                           "住院免赔额：%s   赔付比例：%f\n"
                                           "接口返回结果：%s   计算结果：%f\n" % (
                                           times, p, a, so, key, C_p, outputdata,respect_total_fee))
                                file.close()
                                if (respect_total_fee != outputdata):
                                    print (respect_total_fee, outputdata)
                                    print(float(outputdata))
                                    # with self.subTest():
                                    # print (str(float(respect_total_fee)).split('.')[1])
                                    number = len(str(float(respect_total_fee)).split('.')[1])
                                    if number == 1:
                                        finalfee = str(float(respect_total_fee)) + "0"
                                    else:
                                        finalfee = str(float(respect_total_fee))
                                    self.assertEqual(finalfee, outputdata, msg="222")

                    # for c_p in self.Compensation_proportion:
                    #     print("")
                    #
                    # # print ('\n')
                    # respect_optional2fee =  ex.get_option_fee(xlsxPath=xlsxPath,sheetname=u'少儿意外住院津贴责任费率',start_row=1,gender=g,g_p=gu_period,p_p=int(go),age=a)
                    # respect_optional3fee = ex.get_option_fee(xlsxPath=xlsxPath, sheetname=u'少儿意外医疗责任费率',
                    #                                          start_row=1, gender=g, g_p=gu_period, p_p=int(go),
                    #  age=a)
                    # print("少儿意外住院津贴责任费率:%f"%respect_optional2fee)
                    #
                    # # if go=="1":
                    # #     for amount in self.insured_amount:
                    # #         if gole_payment == 1:
                    # #             print("当前保额:%f,当前总保费:%f" % (amount, respect_optional2fee + respect_optional3fee))
                    # #     continue
                    # if go!='1000':
                    #     respect_optional1fee = ex.get_option_fee(xlsxPath=xlsxPath,sheetname='optional1',start_row=1,gender=g,g_p=str(int(go)-1),p_p=int(go)-1,age=a+18)
                    # else:
                    #     respect_optional1fee = 0
                    #
                    # print("投保人豁免费率：%f" %respect_optional1fee)
                    #     for amount in self.insured_amount:
                    #         if go=='1000':
                    #             data = {
                    #                 "age": 17,
                    #                 "insurePeriod": gu_period,
                    #                 "insuredPaperNo": "513436199501011042",
                    #                 "orgCode": "sxdg",
                    #                 "paymentPeriod":go ,
                    #                 "insureAmount":amount,
                    #                 "productCode": '10270893',
                    #                 "responsibilityCodes": "B10016,B10017",
                    #                 "holderAge": a + 18,
                    #                 "holderGender": g,
                    #                 "gender": g,
                    #                 "dieResidual":dieResidual,
                    #                 "secondDiseases":secondDiseases,
                    #                 "malignant":malignant,
                    #                 "majorDiseaseImmunity":majorDiseaseImmunity
                    #             }
                    #             respect_tolfee =  respect_mainfee*(amount*10)+respect_optional2fee + respect_optional3fee
                    #             # if(respect_tolfee>=200000):
                    #             print("当前保额:%f,当前总保费:%f" % (amount, respect_mainfee*(amount*10)+respect_optional2fee + respect_optional3fee))
                    #             retext = send.senddatas(data)
                    #
                    #             # print (retext.text)
                    #             # print (a)
                    #             outputdata = json.loads(retext.text)["body"]["payment"]
                    #             if (str(respect_tolfee) != outputdata):
                    #                 print (respect_tolfee, outputdata)
                    #             # with self.subTest():
                    #             # print (str(float(respect_tolfee)).split('.')[1])
                    #             number = len(str(float(respect_tolfee)).split('.')[1])
                    #             if number == 1:
                    #                 finalfee = str(float(respect_tolfee)) + "0"
                    #             else:
                    #                 finalfee = str(float(respect_tolfee))
                    #             self.assertEqual(finalfee, outputdata, msg="222")
                    #         else:
                    #             resps = res.getResponsibility()
                    #             for resp in resps:
                    #                 if(resp==[]):
                    #                     cc = ""
                    #                 else:
                    #
                    #                     # for i in resp:
                    #                     #
                    #                     #     if(len(i)==1):
                    #                     #         cc = i
                    #                     #         continue
                    #                     #     else:
                    #                     cc = ",".join(resp)
                    #
                    #
                    #
                    #                 print resp
                    #                     # c = str(resp).split('[')[1].split(']')
                    #                 # print c[0]
                    #                 # cc = str(c[0])
                    #                 data = {
                    #                     "age": 17,
                    #                     "insureAmount":amount,
                    #                     "insurePeriod": gu_period,
                    #                     "insuredPaperNo": "513436199501011042",
                    #                     "orgCode": "sxdg",
                    #                     "paymentPeriod": go,
                    #                     "insureAmount": amount,
                    #                     "productCode": '10270893',
                    #                     "responsibilityCodes":cc,
                    #                     "holderAge": a + 18,
                    #                     "holderGender": g,
                    #                     "gender": g,
                    #                     "dieResidual":dieResidual,
                    #                     "secondDiseases":secondDiseases,
                    #                     "malignant":malignant,
                    #                     "majorDiseaseImmunity":majorDiseaseImmunity
                    #                 }
                    #                 resp,respect_tolfee = res.get_totalfee(resp=resp,amount=amount,mainfee=respect_mainfee*(amount*10), optional1fee=respect_optional1fee, optional2fee=respect_optional2fee, optional3fee=respect_optional3fee)
                    #
                    #                 print("当前保额:%f,当前总保费:%f" %(amount, respect_tolfee))
                    #                 print  json.dumps(data,encoding="UTF-8", ensure_ascii=False, sort_keys=False, indent=1)

                    #                 if (respect_tolfee != outputdata):
                    #                     print (respect_tolfee, outputdata)
                    #                 print(float(outputdata))
                    #                 # with self.subTest():
                    #                 print (str(float(respect_tolfee)).split('.')[1])
                    #                 number = len(str(float(respect_tolfee)).split('.')[1])
                    #                 if number == 1:
                    #                     finalfee = str(float(respect_tolfee)) + "0"
                    #                 else:
                    #                     finalfee = str(float(respect_tolfee))
                    #                 self.assertEqual(finalfee, outputdata, msg="222")
                    #


    def tearDown(self):
        # sys.stdout = open(log_path,mode='w')
        print("test  end")

if __name__ == '__main__':
    unittest.main()
