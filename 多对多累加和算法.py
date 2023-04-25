import copy
import numpy as np
import pandas as pd
# from partial_deduction import PartialDeduction


class DeductionSplit:

    def split_pack(self, fields, invoices):
        if fields.deductible_amount.sum() == sum(invoices):
            max_deductible_amount = fields.deductible_amount.max()
            max_invoices = max(invoices)

            if max_deductible_amount > max_invoices:
                residue_deductible_amount = max_deductible_amount - max_invoices
                invoices.remove(max_invoices)   # 删除发票金额
                del_index = fields[fields.deductible_amount == max_deductible_amount].index[0]
                accident_no_ = fields.loc[del_index, 'accident_no']
                paid_amount_ = fields.loc[del_index, 'paid_amount']

                fields.drop(del_index, inplace=True)    # 删除事故号金额
                fields.loc[max(fields.index) + 1] = [None, accident_no_, paid_amount_, residue_deductible_amount]   # 添加 事故号减发票金额
                print(f'{max_deductible_amount}-{max_invoices}')
                self.invoice_s = invoices
                self.split_pack(fields, invoices)
                pass
            else:
                for invoice in sorted(self.invoice_s, reverse=True):
                    fields.sort_values(by='deductible_amount', ascending=False, inplace=True)
                    fields['cum_sum'] = fields.deductible_amount.cumsum()
                    # 获取拆分的项事故号
                    split_fields = fields[fields.cum_sum >= invoice].head(1)
                    accident_no_ = split_fields.accident_no.values.tolist()[0]
                    paid_amount_ = split_fields.paid_amount.values.tolist()[0]
                    residue_deductible_amount = split_fields.cum_sum.values.tolist()[0] - invoice

                    # 删除待打包的objectID
                    fields.drop(fields[~(fields.cum_sum > invoice)].index, inplace=True)

                    if residue_deductible_amount:
                        fields.drop(split_fields.index, inplace=True)
                        fields.loc[max(fields.index) + 1] = [None, accident_no_, paid_amount_, residue_deductible_amount, None]   # 添加 事故号减发票金额
                    else:
                        pass
                    print(fields.deductible_amount.sum())
                    invoices.remove(invoice)
                    print(sum(invoices))

                    # 获取打包的objectID
                    # pack_fields = fields[~(fields.cum_sum > invoice)]
                # self.split_pack(fields, invoices)

                pass

        else:
            print('打包总金额不等于发票总金额')
            pass




        return fields, invoices
        pass

    def invoice_split_pack(self, fields, invoices):
        if fields.deductible_amount.sum() == sum(invoices):
            for invoice in sorted(self.invoice_s, reverse=True):
                # print(fields.deductible_amount.sum())
                # print(f'当前打包发票金额为：{invoice}，剩余总金额{sum(invoices)}')
                fields.sort_values(by='deductible_amount', ascending=False, inplace=True)
                fields['cum_sum'] = fields.deductible_amount.cumsum()
                # 获取拆分的项事故号
                split_fields = fields[fields.cum_sum >= invoice].head(1)
                accident_no_ = split_fields.accident_no.values.tolist()[0]
                paid_amount_ = split_fields.paid_amount.values.tolist()[0]
                deductible_amount_ = split_fields.deductible_amount.values.tolist()[0]
                residue_deductible_amount = split_fields.cum_sum.values.tolist()[0] - invoice

                print('*' * 100)

                print(f'\n打包objectID信息：\n{pd.concat([fields[~(fields.cum_sum >= invoice)], split_fields])}\n待打包objectID剩余总金额：{fields.deductible_amount.sum()}')

                print(f'\n当前打包发票金额为：{invoice}，发票剩余总金额：{sum(invoices)}')

                # print('*' * 100)

                # obj_deduction = PartialDeduction(invoice_info=datasets, accident_no=accident_no_, deduction_amount=deductible_amount_)
                # obj_deduction.partial_deduction()

                # 删除待打包的objectID
                object_id_list = fields[~(fields.cum_sum > invoice)].object_id.values.tolist()
                # object_id_list.append(拆分后的objectID)
                fields.drop(fields[~(fields.cum_sum > invoice)].index, inplace=True)

                if residue_deductible_amount:
                    print('拆分。。。')
                    fields.drop(split_fields.index, inplace=True)
                    fields.loc[max(fields.index) + 1] = [None, accident_no_, paid_amount_, residue_deductible_amount, None]  # 添加 事故号减发票金额
                else:
                    pass
                # print(fields.deductible_amount.sum())
                invoices.remove(invoice)
                # print(sum(invoices))
        else:
            print('打包总金额不等于发票总金额')
        return fields, invoices
        pass
            
datasets = {
    "data$": [
        {
            "objectId": 15153200106,
            "objectIdPlan": 15153200104,
            "accidentNo": "80052022220000023102",
            "registNo": "8605212022220000019706",
            "certiNo": "8505212022220000016271",
            "accountCode": "0804221109001082076",
            "accountName": "公主岭市吉洋名车维修服务中心",
            "certiTypeCode": "C",
            "paidAmount": 445.0,
            "deductibleAmount": 445.0,
            "invoiceAmount": 12.96,
            "underWriteDate": "2022-06-10",
            "payConfirmTime": "2022-06-10 17:37:22",
            "lowCarbonFlag": "0",
            "fromRepairFlag": "1",
            "repairOrderno": "10322872",
            "repairOrganizationCode": "220106600014607",
            "repairFactoryName": "绿园区篮扳手汽车服务部",
            "repairTaxRate": "1",
            "repairQualification": "二类",
            "sameAccountFlag": "不一致",
            "comCode": "2201848003",
            "comName": "长春公主岭支公司个代咨询服务团队三部",
            "branchComCode": "22000000",
            "branchComName": "吉林省分公司",
            "taxPayerNoInsurer": "91220101333846872H",
            "taxPayerNameInsurer": "长春中心支公司",
            "bankInsurer": "中国农业银行股份有限公司长春人民广场支行",
            "accountNoInsurer": "07195901040015285",
            "addressInsurer": "吉林省长春市净月经济开发区乙十四路伟峰生态新城8办公楼102号",
            "phoneNumberInsurer": "043181105388",
            "dealComCode": "22010035",
            "dealComName": "长春市理赔/客服分中心",
            "lossType": "车",
            "insuredCarFlag": "1",
            "lossName": "吉CYR382",
            "itemNo": "19407451",
            "certainDeptCode": "22010035",
            "certainDeptName": "长春市理赔/客服分中心",
            "certainCode": "220381198801011634",
            "certainName": "马亮",
            "state": "待开票",
            "topId": 14052207024,
            "batchAmount": 0,
            "repairInvoiceAmount": 4.41,
            "repairDeptCode": "22000036",
            "repairDeptName": "吉林省分公司理赔管理部",
            "compensateRemark": "吉CYR382和公主岭市吉洋名车维修服务中心",
            "prplInvoiceReadyKindEOList": []
        },
        {
            "objectId": 15153039878,
            "objectIdPlan": 15153039877,
            "accidentNo": "80052022220000023102",
            "registNo": "8605072022220000018652",
            "certiNo": "8505072022220000013882",
            "accountCode": "0804221109001082076",
            "accountName": "公主岭市吉洋名车维修服务中心",
            "certiTypeCode": "C",
            "paidAmount": 100.0,
            "deductibleAmount": 100.0,
            "invoiceAmount": 2.91,
            "underWriteDate": "2022-06-10",
            "payConfirmTime": "2022-06-10 17:33:24",
            "lowCarbonFlag": "0",
            "fromRepairFlag": "1",
            "repairOrderno": "10322872",
            "repairOrganizationCode": "220106600014607",
            "repairFactoryName": "绿园区篮扳手汽车服务部",
            "repairTaxRate": "1",
            "repairQualification": "二类",
            "sameAccountFlag": "不一致",
            "comCode": "2201848006",
            "comName": "长春公主岭支公司个代咨询服务团队六部",
            "branchComCode": "22000000",
            "branchComName": "吉林省分公司",
            "taxPayerNoInsurer": "91220101333846872H",
            "taxPayerNameInsurer": "长春中心支公司",
            "bankInsurer": "中国农业银行股份有限公司长春人民广场支行",
            "accountNoInsurer": "07195901040015285",
            "addressInsurer": "吉林省长春市净月经济开发区乙十四路伟峰生态新城8办公楼102号",
            "phoneNumberInsurer": "043181105388",
            "dealComCode": "22010035",
            "dealComName": "长春市理赔/客服分中心",
            "lossType": "车",
            "insuredCarFlag": "1",
            "lossName": "吉CYR382",
            "itemNo": "19407451",
            "certainDeptCode": "22010035",
            "certainDeptName": "长春市理赔/客服分中心",
            "certainCode": "220381198801011634",
            "certainName": "马亮",
            "state": "待开票",
            "topId": 14052207024,
            "batchAmount": 0,
            "repairInvoiceAmount": 0.99,
            "repairDeptCode": "22000036",
            "repairDeptName": "吉林省分公司理赔管理部",
            "compensateRemark": "吉CYR382和公主岭市吉洋名车维修服务中心",
            "prplInvoiceReadyKindEOList": []
        },
        {
            "objectId": 15283877185,
            "objectIdPlan": 15283877184,
            "accidentNo": "80052022220000023283",
            "registNo": "8605212022220000019792",
            "certiNo": "8505212022220000017179",
            "accountCode": "0804221109001082076",
            "accountName": "公主岭市吉洋名车维修服务中心",
            "certiTypeCode": "C",
            "paidAmount": 1000.0,
            "deductibleAmount": 1000.0,
            "invoiceAmount": 29.15,
            "underWriteDate": "2022-06-17",
            "payConfirmTime": "2022-06-17 09:59:24",
            "lowCarbonFlag": "0",
            "fromRepairFlag": "1",
            "repairOrderno": "10322872",
            "repairOrganizationCode": "220106600014607",
            "repairFactoryName": "绿园区篮扳手汽车服务部",
            "repairTaxRate": "1",
            "repairQualification": "二类",
            "sameAccountFlag": "不一致",
            "comCode": "2201158009",
            "comName": "长春解放支公司个代咨询服务团队九部",
            "branchComCode": "22000000",
            "branchComName": "吉林省分公司",
            "taxPayerNoInsurer": "91220101333846872H",
            "taxPayerNameInsurer": "长春中心支公司",
            "bankInsurer": "中国农业银行股份有限公司长春人民广场支行",
            "accountNoInsurer": "07195901040015285",
            "addressInsurer": "吉林省长春市净月经济开发区乙十四路伟峰生态新城8办公楼102号",
            "phoneNumberInsurer": "043181105388",
            "dealComCode": "22010035",
            "dealComName": "长春市理赔/客服分中心",
            "lossType": "车",
            "insuredCarFlag": "1",
            "lossName": "吉A2TU29",
            "itemNo": "19435826",
            "certainDeptCode": "22010035",
            "certainDeptName": "长春市理赔/客服分中心",
            "certainCode": "220381198801011634",
            "certainName": "马亮",
            "state": "待开票",
            "topId": 14075833859,
            "batchAmount": 0,
            "repairInvoiceAmount": 9.9,
            "repairDeptCode": "22000036",
            "repairDeptName": "吉林省分公司理赔管理部",
            "compensateRemark": "吉A2TU29和公主岭市吉洋名车维修服务中心",
            "prplInvoiceReadyKindEOList": []
        },
        {
            "objectId": 15260291133,
            "objectIdPlan": 15260291131,
            "accidentNo": "80052022220000024370",
            "registNo": "8605072022220000019464",
            "certiNo": "8505072022220000014516",
            "accountCode": "0804221109001082076",
            "accountName": "公主岭市吉洋名车维修服务中心",
            "certiTypeCode": "C",
            "paidAmount": 376.0,
            "deductibleAmount": 376.0,
            "invoiceAmount": 10.95,
            "underWriteDate": "2022-06-16",
            "payConfirmTime": "2022-06-16 09:44:48",
            "lowCarbonFlag": "0",
            "fromRepairFlag": "1",
            "repairOrderno": "10322872",
            "repairOrganizationCode": "220106600014607",
            "repairFactoryName": "绿园区篮扳手汽车服务部",
            "repairTaxRate": "1",
            "repairQualification": "二类",
            "sameAccountFlag": "不一致",
            "comCode": "2201841101",
            "comName": "长春公主岭支公司农村业务部一部",
            "branchComCode": "22000000",
            "branchComName": "吉林省分公司",
            "taxPayerNoInsurer": "91220101333846872H",
            "taxPayerNameInsurer": "长春中心支公司",
            "bankInsurer": "中国农业银行股份有限公司长春人民广场支行",
            "accountNoInsurer": "07195901040015285",
            "addressInsurer": "吉林省长春市净月经济开发区乙十四路伟峰生态新城8办公楼102号",
            "phoneNumberInsurer": "043181105388",
            "dealComCode": "22010035",
            "dealComName": "长春市理赔/客服分中心",
            "lossType": "车",
            "insuredCarFlag": "2",
            "lossName": "吉CWQ596",
            "itemNo": "19593884",
            "certainDeptCode": "22010035",
            "certainDeptName": "长春市理赔/客服分中心",
            "certainCode": "220381198801011634",
            "certainName": "马亮",
            "state": "待开票",
            "topId": 14190913433,
            "batchAmount": 0,
            "repairInvoiceAmount": 3.72,
            "repairDeptCode": "22000036",
            "repairDeptName": "吉林省分公司理赔管理部",
            "compensateRemark": "吉C5D32G和公主岭市吉洋名车维修服务中心",
            "prplInvoiceReadyKindEOList": []
        },
        {
            "objectId": 15439376271,
            "objectIdPlan": 15439376268,
            "accidentNo": "80052022220000025860",
            "registNo": "8605072022220000020349",
            "certiNo": "8505072022220000015465",
            "accountCode": "0804221109001082076",
            "accountName": "公主岭市吉洋名车维修服务中心",
            "certiTypeCode": "C",
            "paidAmount": 1950.0,
            "deductibleAmount": 500.0,
            "invoiceAmount": 14.56,
            "underWriteDate": "2022-06-24",
            "payConfirmTime": "2022-06-24 13:10:49",
            "lowCarbonFlag": "0",
            "fromRepairFlag": "1",
            "repairOrderno": "10322872",
            "repairOrganizationCode": "220106600014607",
            "repairFactoryName": "绿园区篮扳手汽车服务部",
            "repairTaxRate": "1",
            "repairQualification": "二类",
            "sameAccountFlag": "不一致",
            "comCode": "2201848006",
            "comName": "长春公主岭支公司个代咨询服务团队六部",
            "branchComCode": "22000000",
            "branchComName": "吉林省分公司",
            "taxPayerNoInsurer": "91220101333846872H",
            "taxPayerNameInsurer": "长春中心支公司",
            "bankInsurer": "中国农业银行股份有限公司长春人民广场支行",
            "accountNoInsurer": "07195901040015285",
            "addressInsurer": "吉林省长春市净月经济开发区乙十四路伟峰生态新城8办公楼102号",
            "phoneNumberInsurer": "043181105388",
            "dealComCode": "22010035",
            "dealComName": "长春市理赔/客服分中心",
            "lossType": "车",
            "insuredCarFlag": "2",
            "lossName": "吉CZA848",
            "itemNo": "19807819",
            "certainDeptCode": "22010035",
            "certainDeptName": "长春市理赔/客服分中心",
            "certainCode": "220381198801011634",
            "certainName": "马亮",
            "state": "待开票",
            "topId": 14355549695,
            "spiltDate": "2023-04-19T16:04:40.929+0800",
            "spiltOperatorCode": "220183198910225617",
            "spiltOperatorName": "李君冶",
            "batchAmount": 0,
            "repairInvoiceAmount": 4.95,
            "repairDeptCode": "22000036",
            "repairDeptName": "吉林省分公司理赔管理部",
            "compensateRemark": "吉AJ309J和公主岭市吉洋名车维修服务中心",
            "prplInvoiceReadyKindEOList": []
        },
        {
            "objectId": 23921928601,
            "objectIdPlan": 15439376268,
            "accidentNo": "80052022220000025860",
            "registNo": "8605072022220000020349",
            "certiNo": "8505072022220000015465",
            "accountCode": "0804221109001082076",
            "accountName": "公主岭市吉洋名车维修服务中心",
            "certiTypeCode": "C",
            "paidAmount": 1950.0,
            "deductibleAmount": 475.0,
            "invoiceAmount": 13.83,
            "underWriteDate": "2022-06-24",
            "payConfirmTime": "2022-06-24 13:10:49",
            "lowCarbonFlag": "0",
            "fromRepairFlag": "1",
            "repairOrderno": "10322872",
            "repairOrganizationCode": "220106600014607",
            "repairFactoryName": "绿园区篮扳手汽车服务部",
            "repairTaxRate": "1",
            "repairQualification": "二类",
            "sameAccountFlag": "不一致",
            "comCode": "2201848006",
            "comName": "长春公主岭支公司个代咨询服务团队六部",
            "branchComCode": "22000000",
            "branchComName": "吉林省分公司",
            "taxPayerNoInsurer": "91220101333846872H",
            "taxPayerNameInsurer": "长春中心支公司",
            "bankInsurer": "中国农业银行股份有限公司长春人民广场支行",
            "accountNoInsurer": "07195901040015285",
            "addressInsurer": "吉林省长春市净月经济开发区乙十四路伟峰生态新城8办公楼102号",
            "phoneNumberInsurer": "043181105388",
            "dealComCode": "22010035",
            "dealComName": "长春市理赔/客服分中心",
            "lossType": "车",
            "insuredCarFlag": "2",
            "lossName": "吉CZA848",
            "itemNo": "19807819",
            "certainDeptCode": "22010035",
            "certainDeptName": "长春市理赔/客服分中心",
            "certainCode": "220381198801011634",
            "certainName": "马亮",
            "state": "待开票",
            "topId": 14355549695,
            "spiltDate": "2023-04-20T18:27:03.196+0800",
            "spiltOperatorCode": "220183198910225617",
            "spiltOperatorName": "李君冶",
            "batchAmount": 0,
            "repairInvoiceAmount": 4.7,
            "repairDeptCode": "22000036",
            "repairDeptName": "吉林省分公司理赔管理部",
            "compensateRemark": "吉AJ309J和公主岭市吉洋名车维修服务中心",
            "prplInvoiceReadyKindEOList": []
        },
        {
            "objectId": 23872734000,
            "objectIdPlan": 15439376268,
            "accidentNo": "80052022220000025860",
            "registNo": "8605072022220000020349",
            "certiNo": "8505072022220000015465",
            "accountCode": "0804221109001082076",
            "accountName": "公主岭市吉洋名车维修服务中心",
            "certiTypeCode": "C",
            "paidAmount": 1950.0,
            "deductibleAmount": 500.0,
            "invoiceAmount": 14.56,
            "underWriteDate": "2022-06-24",
            "payConfirmTime": "2022-06-24 13:10:49",
            "lowCarbonFlag": "0",
            "fromRepairFlag": "1",
            "repairOrderno": "10322872",
            "repairOrganizationCode": "220106600014607",
            "repairFactoryName": "绿园区篮扳手汽车服务部",
            "repairTaxRate": "1",
            "repairQualification": "二类",
            "sameAccountFlag": "不一致",
            "comCode": "2201848006",
            "comName": "长春公主岭支公司个代咨询服务团队六部",
            "branchComCode": "22000000",
            "branchComName": "吉林省分公司",
            "taxPayerNoInsurer": "91220101333846872H",
            "taxPayerNameInsurer": "长春中心支公司",
            "bankInsurer": "中国农业银行股份有限公司长春人民广场支行",
            "accountNoInsurer": "07195901040015285",
            "addressInsurer": "吉林省长春市净月经济开发区乙十四路伟峰生态新城8办公楼102号",
            "phoneNumberInsurer": "043181105388",
            "dealComCode": "22010035",
            "dealComName": "长春市理赔/客服分中心",
            "lossType": "车",
            "insuredCarFlag": "2",
            "lossName": "吉CZA848",
            "itemNo": "19807819",
            "certainDeptCode": "22010035",
            "certainDeptName": "长春市理赔/客服分中心",
            "certainCode": "220381198801011634",
            "certainName": "马亮",
            "state": "待开票",
            "topId": 14355549695,
            "spiltDate": "2023-04-19T16:04:40.930+0800",
            "spiltOperatorCode": "220183198910225617",
            "spiltOperatorName": "李君冶",
            "batchAmount": 0,
            "repairInvoiceAmount": 4.95,
            "repairDeptCode": "22000036",
            "repairDeptName": "吉林省分公司理赔管理部",
            "compensateRemark": "吉AJ309J和公主岭市吉洋名车维修服务中心",
            "prplInvoiceReadyKindEOList": []
        },
        {
            "objectId": 23872318044,
            "objectIdPlan": 15439376268,
            "accidentNo": "80052022220000025860",
            "registNo": "8605072022220000020349",
            "certiNo": "8505072022220000015465",
            "accountCode": "0804221109001082076",
            "accountName": "公主岭市吉洋名车维修服务中心",
            "certiTypeCode": "C",
            "paidAmount": 1950.0,
            "deductibleAmount": 475.0,
            "invoiceAmount": 13.83,
            "underWriteDate": "2022-06-24",
            "payConfirmTime": "2022-06-24 13:10:49",
            "lowCarbonFlag": "0",
            "fromRepairFlag": "1",
            "repairOrderno": "10322872",
            "repairOrganizationCode": "220106600014607",
            "repairFactoryName": "绿园区篮扳手汽车服务部",
            "repairTaxRate": "1",
            "repairQualification": "二类",
            "sameAccountFlag": "不一致",
            "comCode": "2201848006",
            "comName": "长春公主岭支公司个代咨询服务团队六部",
            "branchComCode": "22000000",
            "branchComName": "吉林省分公司",
            "taxPayerNoInsurer": "91220101333846872H",
            "taxPayerNameInsurer": "长春中心支公司",
            "bankInsurer": "中国农业银行股份有限公司长春人民广场支行",
            "accountNoInsurer": "07195901040015285",
            "addressInsurer": "吉林省长春市净月经济开发区乙十四路伟峰生态新城8办公楼102号",
            "phoneNumberInsurer": "043181105388",
            "dealComCode": "22010035",
            "dealComName": "长春市理赔/客服分中心",
            "lossType": "车",
            "insuredCarFlag": "2",
            "lossName": "吉CZA848",
            "itemNo": "19807819",
            "certainDeptCode": "22010035",
            "certainDeptName": "长春市理赔/客服分中心",
            "certainCode": "220381198801011634",
            "certainName": "马亮",
            "state": "待开票",
            "topId": 14355549695,
            "spiltDate": "2023-04-20T18:27:03.193+0800",
            "spiltOperatorCode": "220183198910225617",
            "spiltOperatorName": "李君冶",
            "batchAmount": 0,
            "repairInvoiceAmount": 4.7,
            "repairDeptCode": "22000036",
            "repairDeptName": "吉林省分公司理赔管理部",
            "compensateRemark": "吉AJ309J和公主岭市吉洋名车维修服务中心",
            "prplInvoiceReadyKindEOList": []
        },
        {
            "objectId": 15459430807,
            "objectIdPlan": 15459430805,
            "accidentNo": "80052022220000026020",
            "registNo": "8605212022220000021719",
            "certiNo": "8505212022220000018201",
            "accountCode": "0804221109001082076",
            "accountName": "公主岭市吉洋名车维修服务中心",
            "certiTypeCode": "C",
            "paidAmount": 845.0,
            "deductibleAmount": 845.0,
            "invoiceAmount": 24.61,
            "underWriteDate": "2022-06-25",
            "payConfirmTime": "2022-06-25 12:10:44",
            "lowCarbonFlag": "0",
            "fromRepairFlag": "1",
            "repairOrderno": "10322872",
            "repairOrganizationCode": "220106600014607",
            "repairFactoryName": "绿园区篮扳手汽车服务部",
            "repairTaxRate": "1",
            "repairQualification": "二类",
            "sameAccountFlag": "不一致",
            "comCode": "2201972002",
            "comName": "长春中心支公司业务数字渠道支持团队一部",
            "branchComCode": "22000000",
            "branchComName": "吉林省分公司",
            "taxPayerNoInsurer": "91220101333846872H",
            "taxPayerNameInsurer": "长春中心支公司",
            "bankInsurer": "中国农业银行股份有限公司长春人民广场支行",
            "accountNoInsurer": "07195901040015285",
            "addressInsurer": "吉林省长春市净月经济开发区乙十四路伟峰生态新城8办公楼102号",
            "phoneNumberInsurer": "043181105388",
            "dealComCode": "22010035",
            "dealComName": "长春市理赔/客服分中心",
            "lossType": "车",
            "insuredCarFlag": "1",
            "lossName": "吉C9398D",
            "itemNo": "19830530",
            "certainDeptCode": "22010035",
            "certainDeptName": "长春市理赔/客服分中心",
            "certainCode": "220381198801011634",
            "certainName": "马亮",
            "state": "待开票",
            "topId": 14373036947,
            "batchAmount": 0,
            "repairInvoiceAmount": 8.37,
            "repairDeptCode": "22000036",
            "repairDeptName": "吉林省分公司理赔管理部",
            "compensateRemark": "吉C9398D和公主岭市吉洋名车维修服务中心",
            "prplInvoiceReadyKindEOList": []
        },
        {
            "objectId": 15459430874,
            "objectIdPlan": 15459430873,
            "accidentNo": "80052022220000026020",
            "registNo": "8605072022220000020447",
            "certiNo": "8505072022220000015554",
            "accountCode": "0804221109001082076",
            "accountName": "公主岭市吉洋名车维修服务中心",
            "certiTypeCode": "C",
            "paidAmount": 100.0,
            "deductibleAmount": 100.0,
            "invoiceAmount": 2.91,
            "underWriteDate": "2022-06-25",
            "payConfirmTime": "2022-06-25 12:10:59",
            "lowCarbonFlag": "0",
            "fromRepairFlag": "1",
            "repairOrderno": "10322872",
            "repairOrganizationCode": "220106600014607",
            "repairFactoryName": "绿园区篮扳手汽车服务部",
            "repairTaxRate": "1",
            "repairQualification": "二类",
            "sameAccountFlag": "不一致",
            "comCode": "2201972002",
            "comName": "长春中心支公司业务数字渠道支持团队一部",
            "branchComCode": "22000000",
            "branchComName": "吉林省分公司",
            "taxPayerNoInsurer": "91220101333846872H",
            "taxPayerNameInsurer": "长春中心支公司",
            "bankInsurer": "中国农业银行股份有限公司长春人民广场支行",
            "accountNoInsurer": "07195901040015285",
            "addressInsurer": "吉林省长春市净月经济开发区乙十四路伟峰生态新城8办公楼102号",
            "phoneNumberInsurer": "043181105388",
            "dealComCode": "22010035",
            "dealComName": "长春市理赔/客服分中心",
            "lossType": "车",
            "insuredCarFlag": "1",
            "lossName": "吉C9398D",
            "itemNo": "19830530",
            "certainDeptCode": "22010035",
            "certainDeptName": "长春市理赔/客服分中心",
            "certainCode": "220381198801011634",
            "certainName": "马亮",
            "state": "待开票",
            "topId": 14373036947,
            "batchAmount": 0,
            "repairInvoiceAmount": 0.99,
            "repairDeptCode": "22000036",
            "repairDeptName": "吉林省分公司理赔管理部",
            "compensateRemark": "吉C9398D和公主岭市吉洋名车维修服务中心",
            "prplInvoiceReadyKindEOList": []
        }
    ],
    "entityCount$": 10,
    "from": 0,
    "limit": 50
}
object_id = []
accident_no = []
paid_amount = []
deductible_amount = []
for dataset in datasets['data$']:
    object_id.append(dataset.get('objectId'))
    accident_no.append(dataset.get('accidentNo'))
    paid_amount.append(dataset.get('paidAmount'))
    deductible_amount.append(dataset.get('deductibleAmount'))
    pass


# deductible_amount = [2000, 316, 500, 1000, 4500, 684, 4000, 10000, 3500, 2500]
deductible_amount = [188.3, 226.7, 445.8, 339.2, 8800, 3500, 1500, 1000, 2600, 1400]
# invoice_number_s = [416, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400]
# invoice_number_s = [1000, 1200, 800, 1816, 284, 5000, 4000, 2000, 1000, 1500, 1500, 1000, 2000, 3000, 2900]
invoice_number_s = [6400, 3600, 5537, 4463]
obj_deduction_split = DeductionSplit(copy.deepcopy(invoice_number_s))

df_deduction = pd.DataFrame(data={
    'object_id': object_id,
    'accident_no': accident_no,
    'paid_amount': paid_amount,
    'deductible_amount': deductible_amount,
})
df = df_deduction.copy()

fields, invoices = obj_deduction_split.invoice_split_pack(df_deduction, invoices=sorted(invoice_number_s, reverse=True))
# fields, invoices = obj_deduction_split.split_pack(df_deduction, invoices=sorted(invoice_number_s, reverse=True))

fields = obj_deduction_split.split_pack(np.asarray(
    [
        object_id,
        accident_no,
        paid_amount,
        deductible_amount,
    ],

).T)
invoices, deduction = obj_deduction_split.split_deductible_amount(list(zip(object_id, accident_no, paid_amount, deductible_amount)), invoice_number_s)
print(list(zip(object_id, accident_no, paid_amount, deductible_amount)))



