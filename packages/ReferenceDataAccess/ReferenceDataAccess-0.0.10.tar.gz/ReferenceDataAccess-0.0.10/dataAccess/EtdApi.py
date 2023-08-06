# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:44:00 2020

@author: Sangoi
"""

import requests
import json
import pandas as pd
from dataAccess.EquityApi import EquityApi


class EtdApi(object):
    
    """
    This class hold all methods to access etd (derivatives - futures/options/strategies) data
      
    """
    
    def __init__(self, key):
        """ 
        Initialize the class
        Keyword Arguments:
            key:  RDUAccess api key

        """
        
        self.key = key
        self.all_column_list = ["exchCd","lstngCycleTp","omic","segTp","smic","tckSz","tckVal","trdStsTp","vndrExchCd","ticker","bbgIdBBGlobal","rduSecId","rduSegId","bbgCompositeIdBbGlobal","rduSecIdExp","rduSegIdExp","gmiFullPrdCd","name","roundLotSz","clrngCd","name","roundLotSz","trdCtyCd","trdCcyMajorFl","trdCcyCd","dayNum","maxOrdSz","tckSzDnmntr","prdTp","flexElgblFl","clrngCcyCd","msrmntUntCd","tckSzNmrtr","spotMnthPosLmt","mnthPosLmt","allMnthPosLmt","blckTrdElgblFl","actFl","exchCd","wkNum","exchRptngLvl","cftcRptngLvl","trdStsTp","cftcRegFl","undlRltnsTp","clrngCd","rduPrdId","name","assetTp","expDt","lstTrdDt","settleDt","frstDlvryDt","frstNtcDt","lstDlvryDt","name","vndrAssetTp","prntAssetTp","strikePx","cfi","yrCd","settleTp","ctrSz","frstTrdDt","settleFixDt","numOfLegs","accrlStrtDt","accrlEndDt","mnthCd","dayNum","pntVal","flexFl","actFl","wkNum","lstNtcDt","trdStsTp","cfiCd","isin","bbgTicker","bbgIdBbUnique","aiiCode","ric","trAssetId","trQuoteId","ricRoot","ult_under_name","ult_under_ric","ult_under_ticker","ult_under_isin","ult_under_rduSecId","exchPrfx","immed_under_name","immed_under_ric","immed_under_ticker","immed_under_isin","immed_under_rduSecId"] 

    def _fetch_underlying_data(self, isin, smic, omic):
        
        underlyingData = None
        if(not isin):
            return underlyingData
        if(not smic and not omic):
            return underlyingData
        if(smic):
            underlyingData = self.__get_underlying_data(isin, smic)
            if(not underlyingData['success'][0] and omic):
                underlyingData = self.__get_underlying_data(isin, omic)
                   
        return underlyingData

    def __get_underlying_data(self, isin, exchange):
        equity = EquityApi(key=self.key)
        underlyingData = equity.get_by_isin_exchange(isin, exchange)
        
        return underlyingData
           


    def __convert_json_to_df(self, input_key,json_data, fetchUnderlying:False, columnList=[]):
        df = pd.json_normalize(json_data)        
        msg = df.get('message')
        product_dict = {}
        if(not columnList):
            columnList.extend(self.all_column_list)
        if (isinstance(msg, pd.Series)):
            message = msg.loc[0]
            contract_dict = {}
            contract_dict['sucess'] = False
            contract_dict['failed_message'] = message
            product_dict[input_key] = contract_dict
        else:
            for index, row in df.iterrows():
                """product_list.append(row['basics.name'])
                product_list.append(row['basics.roundLotSz'])
                product_list.append(row['ids.clrngCd'])
                """
                underlier_df = pd.DataFrame()
                etdunderliers = row.get('underliers.underlier')
                p_u_name_list = []
                p_u_ric_list = []
                p_u_ticker_list = []
                p_u_isin_list = []
                p_u_rduSecId_list = []
                
                for prd_underlier in etdunderliers:
                    index = index+1
                    p_u_name_list.append(prd_underlier.get('basics').get('name'))   
                    p_u_ric_list.append(prd_underlier.get('ids').get('ric'))   
                    p_u_ticker_list.append(prd_underlier.get('ids').get('ticker'))   
                    p_u_isin_list.append(prd_underlier.get('ids').get('isin'))   
                    p_u_rduSecId_list.append(prd_underlier.get('ids').get('rduSecId'))   

                    underlyingIsin = prd_underlier.get('ids').get('isin')
                    #print(underlyingIsin)
                    smic = prd_underlier.get('basics').get('smic')
                    omic = prd_underlier.get('basics').get('omic')
                    if(fetchUnderlying):
                        
                        underlyingData = self._fetch_underlying_data(underlyingIsin, smic, omic)
                        
                            
                        #print(underlyingData)
                        if(underlyingData is  not None):
                            underlier_df = underlier_df.append(underlyingData)
                        
                       
                underlier_df = underlier_df.add_prefix('ult_under_eq_')        
            
                #print(underlier_df)
                contracts = row.get('contracts')
                for contract in contracts :
                    
                    c_u_name_list = []
                    c_u_ric_list = []
                    c_u_ticker_list = []
                    c_u_isin_list = []
                    c_u_rduSecId_list = []
                    c_underlier_df = pd.DataFrame()
                    imm_underliers = contract.get('underliers')
                    
                    if(imm_underliers is not None):
                        im_underlier = imm_underliers.get('underlier')
                        for uu_un in im_underlier:
                            
                            c_u_name_list.append(uu_un.get('basics').get('name'))   
                            c_u_ric_list.append(uu_un.get('ids').get('ric'))   
                            c_u_ticker_list.append(uu_un.get('ids').get('ticker'))   
                            c_u_isin_list.append(uu_un.get('ids').get('isin'))   
                            c_u_rduSecId_list.append(uu_un.get('ids').get('rduSecId'))   

                            
                            smic = uu_un.get('basics').get('smic')
                            omic = uu_un.get('basics').get('omic')
                            cuisin = uu_un.get('ids').get('isin')
                            #print(cuisin)
                            if(fetchUnderlying):
                                
                                cunderlyingData = self._fetch_underlying_data(cuisin, smic, omic)
                                #print(cunderlyingData)
                                if(cunderlyingData is  not None):
                                    c_underlier_df = underlier_df.append(underlyingData)
                        
                        c_underlier_df = c_underlier_df.add_prefix('ult_under_eq_')        
    
                    
                    c_tradelines = contract['tradeLines']['tradeLine']
                    
                          
                    for c_tradeline in c_tradelines :
                        contract_dict = {}

                        ct_basics = c_tradeline['basics']
                        
                        contract_dict['sucess'] = True
                        #print(ct_basics.get('segTp'))
                        if(	'exchCd'	in	columnList):	contract_dict['exchCd'] =ct_basics.get('exchCd')
                        if(	'lstngCycleTp'	in	columnList):	contract_dict['lstngCycleTp'] =ct_basics.get('lstngCycleTp')
                        if(	'omic'	in	columnList):	contract_dict['omic'] =ct_basics.get('omic')
                        if(	'segTp'	in	columnList):	contract_dict['segTp'] =ct_basics.get('segTp')
                        if(	'smic'	in	columnList):	contract_dict['smic'] =ct_basics.get('smic')
                        if(	'tckSz'	in	columnList):	contract_dict['tckSz'] =ct_basics.get('tckSz')
                        if(	'tckVal'	in	columnList):	contract_dict['tckVal'] =ct_basics.get('tckVal')
                        if(	'trdStsTp'	in	columnList):	contract_dict['trdStsTp'] =ct_basics.get('trdStsTp')
                     
                        ct_sessions = c_tradeline['sessions'].get('session')
                        ct_session = ct_sessions[0]
                        ct_session_id = ct_session.get('ids')
                        #print(type(ct_session_id))
                        #print(ct_session_id)
                        if(	'ric'	in	columnList):	contract_dict['ric'] =ct_session_id.get('ric')
                        if(	'trAssetId'	in	columnList):	contract_dict['trAssetId'] =ct_session_id.get('trAssetId')
                        if(	'trQuoteId'	in	columnList):	contract_dict['trQuoteId'] =ct_session_id.get('trQuoteId')                        

                        #contract_dict['ct_vndrExchCd'] =ct_basics.get('vndrExchCd')
    
                        ct_ids = c_tradeline['ids']
                        
                        if(	'ticker'	in	columnList):	contract_dict['ticker']=ct_ids.get('ticker')
                        if(	'bbgIdBBGlobal'	in	columnList):	contract_dict['bbgIdBBGlobal']=ct_ids.get('bbgIdBbGlobal')
                        if(	'rduSecId'	in	columnList):	contract_dict['rduSecId']=ct_ids.get('rduSecId')
                        if(	'rduSegId'	in	columnList):	contract_dict['rduSegId']=ct_ids.get('rduSegId')
                        if(	'bbgCompositeIdBbGlobal'	in	columnList):	contract_dict['bbgCompositeIdBbGlobal']=ct_ids.get('bbgCompositeIdBbGlobal')
                        if(	'rduSecIdExp'	in	columnList):	contract_dict['rduSecIdExp']=ct_ids.get('rduSecIdExp')
                        if(	'rduSegIdExp'	in	columnList):	contract_dict['rduSegIdExp']=ct_ids.get('rduSegIdExp')
                        if(	'gmiFullPrdCd'	in	columnList):	contract_dict['gmiFullPrdCd']=ct_ids.get('gmiFullPrdCd')
 
#                        if(	'name'	in	columnList):	contract_dict['name'] = row.get('basics.name')
                        if(	'roundLotSz'	in	columnList):	contract_dict['roundLotSz'] = row.get('basics.roundLotSz')
                        if(	'clrngCd'	in	columnList):	contract_dict['clrngCd'] = row.get('ids.clrngCd')
                        if(	'roundLotSz'	in	columnList):	contract_dict['roundLotSz'] =row.get('basics.roundLotSz')
                        if(	'trdCtyCd'	in	columnList):	contract_dict['trdCtyCd'] =row.get('basics.trdCtyCd')
                        if(	'trdCcyMajorFl'	in	columnList):	contract_dict['trdCcyMajorFl'] =row.get('basics.trdCcyMajorFl')
                        if(	'trdCcyCd'	in	columnList):	contract_dict['trdCcyCd'] =row.get('basics.trdCcyCd')
                        if(	'dayNum'	in	columnList):	contract_dict['dayNum'] =row.get('basics.dayNum')
                        if(	'maxOrdSz'	in	columnList):	contract_dict['maxOrdSz'] =row.get('basics.maxOrdSz')
                        if(	'tckSzDnmntr'	in	columnList):	contract_dict['tckSzDnmntr'] =row.get('basics.tckSzDnmntr')
                        if(	'prdTp'	in	columnList):	contract_dict['prdTp'] =row.get('basics.prdTp')
                        if(	'flexElgblFl'	in	columnList):	contract_dict['flexElgblFl'] =row.get('basics.flexElgblFl')
                        if(	'clrngCcyCd'	in	columnList):	contract_dict['clrngCcyCd'] =row.get('basics.clrngCcyCd')
                        if(	'msrmntUntCd'	in	columnList):	contract_dict['msrmntUntCd'] =row.get('basics.msrmntUntCd')
                        if(	'tckSzNmrtr'	in	columnList):	contract_dict['tckSzNmrtr'] =row.get('basics.tckSzNmrtr')
                        if(	'spotMnthPosLmt'	in	columnList):	contract_dict['spotMnthPosLmt'] =row.get('basics.spotMnthPosLmt')
                        if(	'mnthPosLmt'	in	columnList):	contract_dict['mnthPosLmt'] =row.get('basics.mnthPosLmt')
                        if(	'allMnthPosLmt'	in	columnList):	contract_dict['allMnthPosLmt'] =row.get('basics.allMnthPosLmt')
                        if(	'blckTrdElgblFl'	in	columnList):	contract_dict['blckTrdElgblFl'] =row.get('basics.blckTrdElgblFl')
                        if(	'actFl'	in	columnList):	contract_dict['actFl'] =row.get('basics.actFl')
                        if(	'exchCd'	in	columnList):	contract_dict['exchCd'] =row.get('basics.exchCd')
                        if(	'wkNum'	in	columnList):	contract_dict['wkNum'] =row.get('basics.wkNum')
                        if(	'exchRptngLvl'	in	columnList):	contract_dict['exchRptngLvl'] =row.get('basics.exchRptngLvl')
                        if(	'cftcRptngLvl'	in	columnList):	contract_dict['cftcRptngLvl'] =row.get('basics.cftcRptngLvl')
                        if(	'trdStsTp'	in	columnList):	contract_dict['trdStsTp'] =row.get('basics.trdStsTp')
                        if(	'cftcRegFl'	in	columnList):	contract_dict['cftcRegFl'] =row.get('basics.cftcRegFl')
                        if(	'undlRltnsTp'	in	columnList):	contract_dict['undlRltnsTp'] =row.get('basics.undlRltnsTp')
                        if(	'clrngCd'	in	columnList):	contract_dict['clrngCd'] =row.get('ids.clrngCd')
                        if(	'rduPrdId'	in	columnList):	contract_dict['rduPrdId'] =row.get('ids.rduPrdId')
                             
                        prd_tradeline = row.get('tradeLines.tradeLine')
                        if(	'exchPrfx'	in	columnList):	contract_dict['exchPrfx'] = prd_tradeline[0].get('ids').get('exchPrfx')

                       
                        prd_session = prd_tradeline[0].get('sessions').get('session')[0]
                        prd_session_id = prd_session.get('ids')
                        if(prd_session_id is not None):
                            #print(prd_session_id.get('ricRoot'))
                            
                            if(	'ricRoot'	in	columnList):contract_dict['ricRoot'] =prd_session_id.get('ricRoot')
                        

                        
                        #print(type(prd_underlier))
                        #print(prd_underlier)    
                            
                        #print(prd_session)
                        
                        #print(type(prd_session))
                        
                        #contract_dict['p_tradeLine'] =row.get('tradeLines.tradeLine')
                        #contract_dict['p_underlier'] =row.get('underliers.underlier')
        
                        
                        c_basics = contract.get('basics')

                        if(	'name'	in	columnList):	contract_dict['name'] = c_basics.get('name')
                        if(	'assetTp'	in	columnList):	contract_dict['assetTp'] =c_basics.get('assetTp')
                        if(	'expDt'	in	columnList):	contract_dict['expDt'] =c_basics.get('expDt')
                        if(	'lstTrdDt'	in	columnList):	contract_dict['lstTrdDt'] =c_basics.get('lstTrdDt')
                        if(	'settleDt'	in	columnList):	contract_dict['settleDt'] =c_basics.get('settleDt')
                        if(	'frstDlvryDt'	in	columnList):	contract_dict['frstDlvryDt'] =c_basics.get('frstDlvryDt')
                        if(	'frstNtcDt'	in	columnList):	contract_dict['frstNtcDt'] =c_basics.get('frstNtcDt')
                        if(	'lstDlvryDt'	in	columnList):	contract_dict['lstDlvryDt'] =c_basics.get('lstDlvryDt')
                        if(	'name'	in	columnList):	contract_dict['name'] =c_basics.get('name')
                        if(	'vndrAssetTp'	in	columnList):	contract_dict['vndrAssetTp'] =c_basics.get('vndrAssetTp')
                        if(	'prntAssetTp'	in	columnList):	contract_dict['prntAssetTp'] =c_basics.get('prntAssetTp')
                        if(	'strikePx'	in	columnList):	contract_dict['strikePx'] =c_basics.get('strikePx')
                        if(	'cfi'	in	columnList):	contract_dict['cfi'] =c_basics.get('cfi')
                        if(	'yrCd'	in	columnList):	contract_dict['yrCd'] =c_basics.get('yrCd')
                        if(	'settleTp'	in	columnList):	contract_dict['settleTp'] =c_basics.get('settleTp')
                        if(	'ctrSz'	in	columnList):	contract_dict['ctrSz'] =c_basics.get('ctrSz')
                        if(	'frstTrdDt'	in	columnList):	contract_dict['frstTrdDt'] =c_basics.get('frstTrdDt')
                        if(	'settleFixDt'	in	columnList):	contract_dict['settleFixDt'] =c_basics.get('settleFixDt')
                        if(	'numOfLegs'	in	columnList):	contract_dict['numOfLegs'] =c_basics.get('numOfLegs')
                        if(	'accrlStrtDt'	in	columnList):	contract_dict['accrlStrtDt'] =c_basics.get('accrlStrtDt')
                        if(	'accrlEndDt'	in	columnList):	contract_dict['accrlEndDt'] =c_basics.get('accrlEndDt')
                        if(	'mnthCd'	in	columnList):	contract_dict['mnthCd'] =c_basics.get('mnthCd')
                        if(	'dayNum'	in	columnList):	contract_dict['dayNum'] =c_basics.get('dayNum')
                        if(	'pntVal'	in	columnList):	contract_dict['pntVal'] =c_basics.get('pntVal')
                        if(	'flexFl'	in	columnList):	contract_dict['flexFl'] =c_basics.get('flexFl')
                        if(	'actFl'	in	columnList):	contract_dict['actFl'] =c_basics.get('actFl')
                        if(	'wkNum'	in	columnList):	contract_dict['wkNum'] =c_basics.get('wkNum')
                        if(	'lstNtcDt'	in	columnList):	contract_dict['lstNtcDt'] =c_basics.get('lstNtcDt')
                        if(	'trdStsTp'	in	columnList):	contract_dict['trdStsTp'] =c_basics.get('trdStsTp')
                        if(	'cfiCd'	in	columnList):	contract_dict['cfiCd'] =c_basics.get('cfiCd')

                        
        
                        c_ids = contract.get('ids')

                        if(	'isin'	in	columnList):	contract_dict['isin'] =c_ids.get('isin')
                        if(	'bbgTicker'	in	columnList):	contract_dict['bbgTicker'] =c_ids.get('bbgTicker')
                        if(	'bbgIdBbUnique'	in	columnList):	contract_dict['bbgIdBbUnique'] =c_ids.get('bbgIdBbUnique')
                        if(	'aiiCode'	in	columnList):	contract_dict['aiiCode'] =c_ids.get('aiiCode')

        
        
                        
                        """contract_list.append(c_basics['name'])
                        rows_list = product_list + contract_list
                                                
                        data.loc[i] = rows_list
                        i = i+1
                        """
                        
                        #print(type(etdunderliers))
                        #print(etdunderliers)
                        
                        if(	'ult_under_name'	in	columnList):	
                            contract_dict['ult_under_name_1'] =p_u_name_list[0]
                            if(len(p_u_name_list)>1):
                                contract_dict['ult_under_name_2'] =p_u_name_list[1]
                            if(len(p_u_name_list)>2):
                                contract_dict['ult_under_name_3'] =p_u_name_list[2]
                                
                        if(	'ult_under_ric'	in	columnList):	
                            contract_dict['ult_under_ric_1'] =p_u_ric_list[0]
                            if(len(p_u_ric_list)>1):
                                contract_dict['ult_under_ric_2'] =p_u_ric_list[1]
                            if(len(p_u_ric_list)>2):
                                contract_dict['ult_under_ric_3'] =p_u_ric_list[2]

                        if(	'ult_under_ticker'	in	columnList):	
                            contract_dict['ult_under_ticker_1'] =p_u_ticker_list[0]
                            if(len(p_u_ticker_list)>1):
                                contract_dict['ult_under_ticker_2'] =p_u_ticker_list[1]
                            if(len(p_u_ticker_list)>2):
                                contract_dict['ult_under_ticker_3'] =p_u_ticker_list[2]


                        if(	'ult_under_isin'	in	columnList):	
                            contract_dict['ult_under_isin_1']  = p_u_isin_list[0]
                            if(len(p_u_isin_list)>1):
                                contract_dict['ult_under_isin_2'] =p_u_isin_list[1]
                            if(len(p_u_isin_list)>2):
                                contract_dict['ult_under_isin_3'] =p_u_isin_list[2]

                        if(	'ult_under_rduSecId'	in	columnList):	
                            contract_dict['ult_under_rduSecId_1'] = p_u_rduSecId_list[0]
                            if(len(p_u_rduSecId_list)>1):
                                contract_dict['ult_under_rduSecId_2'] =p_u_rduSecId_list[1]
                            if(len(p_u_rduSecId_list)>2):
                                contract_dict['ult_under_rduSecId_3'] =p_u_rduSecId_list[2]
 
                        if(fetchUnderlying and underlier_df is not None):
                            for uc in underlier_df.columns:
                                ls = underlier_df[uc].tolist()
                                contract_dict[uc+"_1"] =  ls[0]
                                if(len(ls)>1):
                                    contract_dict[uc+"_2"] =  ls[1]
                                if(len(ls)>2):
                                    contract_dict[uc+"_3"] =  ls[2]

                        if(	'immed_under_name'	in	columnList):	
                            if(len(c_u_name_list)>0):
                                contract_dict['immed_under_name_1'] =c_u_name_list[0]
                            if(len(c_u_name_list)>1):
                                contract_dict['immed_under_name_2'] =c_u_name_list[1]
                            if(len(c_u_name_list)>2):
                                contract_dict['immed_under_name_3'] =c_u_name_list[2]
                                
                        if(	'immed_under_ric'	in	columnList):	
                            if(len(c_u_ric_list)>0):
                                contract_dict['immed_under_ric_1'] =c_u_ric_list[0]
                            if(len(c_u_ric_list)>1):
                                contract_dict['immed_under_ric_2'] =c_u_ric_list[1]
                            if(len(c_u_ric_list)>2):
                                contract_dict['immed_under_ric_3'] =c_u_ric_list[2]

                        if(	'immed_under_ticker'	in	columnList):	
                            if(len(c_u_ticker_list)>0):
                                contract_dict['immed_under_ticker_1'] =c_u_ticker_list[0]
                            if(len(c_u_ticker_list)>1):
                                contract_dict['immed_under_ticker_2'] =c_u_ticker_list[1]
                            if(len(c_u_ticker_list)>2):
                                contract_dict['immed_under_ticker_3'] =c_u_ticker_list[2]


                        if(	'immed_under_isin'	in	columnList):	
                            if(len(c_u_isin_list)>0):
                                contract_dict['immed_under_isin_1']  = c_u_isin_list[0]
                            if(len(c_u_isin_list)>1):
                                contract_dict['immed_under_isin_2'] =c_u_isin_list[1]
                            if(len(c_u_isin_list)>2):
                                contract_dict['immed_under_isin_3'] =c_u_isin_list[2]

                        if(	'immed_under_rduSecId'	in	columnList):	
                            if(len(c_u_rduSecId_list)>0):
                                contract_dict['immed_under_rduSecId_1'] = c_u_rduSecId_list[0]
                            if(len(c_u_rduSecId_list)>1):
                                contract_dict['immed_under_rduSecId_2'] =c_u_rduSecId_list[1]
                            if(len(c_u_rduSecId_list)>2):
                                contract_dict['immed_under_rduSecId_3'] =c_u_rduSecId_list[2]

                        if(fetchUnderlying and c_underlier_df is not None):
                            for uc in c_underlier_df.columns:
                                ls = c_underlier_df[uc].tolist()
                                contract_dict[uc+"_1"] =  ls[0]
                                if(len(ls)>1):
                                    contract_dict[uc+"_2"] =  ls[1]
                                if(len(ls)>2):
                                    contract_dict[uc+"_3"] =  ls[2]
                                
                                
                                
                        product_dict[input_key+"_"+ct_basics['exchCd']] = contract_dict
                        #print(product_dict)
                    
                        
                            
                
                
        data = pd.DataFrame.from_dict(product_dict, orient='index')
#        if(fetchUnderlying):
#            series = underlier_df.iloc[0]
#            for col in underlyingData:
#                data[col] = series[col]
        return data
    
    """
    This method calls the resp api.
    """
    
    def __call_api(self, query, url):
        headers = {'x-api-key' : self.key,'accept':'application/json'}
        response = requests.get(url, params=query,headers=headers)
        data = response.text
        if not data:
            data = "{\"message\":\"No Data Found\"}"
        json_data = json.loads(data)
        return json_data
    
    def get_by_isin_with_underlier_data(self, isin, columnList=[]):
        """
        
        This will return the etd data given the isin
        Parameters
        ----------
        isin : String
            The ISIN code.
        columnList : List    
            Specify the list of column's that needs to be returned in output. 
            If no column's are specified, then it will return all the columns
        Returns
        -------
        data : dataframe
            this will return a dataframe with key as isin+exchange.
            To get description on the columns of dataframe, call get_output_attributes_doc.
        """
        print("Calling getByIsin with isin "+isin)
        query = {'isin':isin}
        json_data = self.__call_api(query, 'https://sfbrekezl8.execute-api.eu-west-2.amazonaws.com/FreeTrial/etd/standard/getByIsin')
            
        data = self.__convert_json_to_df(isin,json_data,fetchUnderlying=True, columnList= columnList)
        columnList = []
        return data


    
    def get_by_isin(self, isin, columnList=[]):
        """
        
        This will return the etd data given the isin
        Parameters
        ----------
        isin : String
            The ISIN code.
        columnList : List    
            Specify the list of column's that needs to be returned in output. 
            If no column's are specified, then it will return all the columns
        Returns
        -------
        data : dataframe
            this will return a dataframe with key as isin+exchange.
            To get description on the columns of dataframe, call get_output_attributes_doc.
        """
        print("Calling getByIsin with isin "+isin)
        query = {'isin':isin}
        json_data = self.__call_api(query, 'https://sfbrekezl8.execute-api.eu-west-2.amazonaws.com/FreeTrial/etd/standard/getByIsin')
            
        data = self.__convert_json_to_df(isin,json_data, fetchUnderlying=False, columnList=columnList)
        columnList = []
        return data


    def get_by_isins(self, isins = [], columnList=[]):
        """
        This will return the etd data given the isins
        Keyword Arguments:

        Parameters
        ----------
        isins : TYPE, optional
            DESCRIPTION. The default is [].

        Returns
        -------
        data : dataframe
            this will return a dataframe with key as isin+exchange.

        """
        data = []            
        for isin in isins:
            t_data = self.get_by_isin(isin,columnList)
            data.append(t_data)
        data = pd.concat(data)
        return data   

    def get_by_ticker_with_underlier_data(self, ticker, exchangeCode,columnList=[]):
        """
        This will return the etd data given the ticker and echange code
       

        Parameters
        ----------
        ticker : String
            Exchange symbol (also known as Ticker or Trade Symbol) of contract.
        exchangeCode : String
            Exchange code of the session where the security is trading.

        Returns
        -------
        data : dataframe
            This will return a dataframe with key as ticker+exchange.
            To get description on the columns of dataframe, call get_output_attributes_doc.

        """
        print("Calling get_by_exchange_symbol with isin "+ticker+" exchangeCode-"+exchangeCode)
        query = {'ticker':ticker, 'exchangeCode':exchangeCode}
        json_data = self.__call_api(query, 'https://sfbrekezl8.execute-api.eu-west-2.amazonaws.com/FreeTrial/etd/standard/getByExchangeSymbol')
        data = self.__convert_json_to_df(ticker,json_data, fetchUnderlying=True)
       
        return data

    
    def get_by_ticker(self, ticker, exchangeCode,columnList=[]):
        """
        This will return the etd data given the ticker and echange code
       

        Parameters
        ----------
        ticker : String
            Exchange symbol (also known as Ticker or Trade Symbol) of contract.
        exchangeCode : String
            Exchange code of the session where the security is trading.

        Returns
        -------
        data : dataframe
            This will return a dataframe with key as ticker+exchange.
            To get description on the columns of dataframe, call get_output_attributes_doc.

        """
        print("Calling get_by_exchange_symbol with isin "+ticker+" exchangeCode-"+exchangeCode)
        query = {'ticker':ticker, 'exchangeCode':exchangeCode}
        json_data = self.__call_api(query, 'https://sfbrekezl8.execute-api.eu-west-2.amazonaws.com/FreeTrial/etd/standard/getByExchangeSymbol')
        data = self.__convert_json_to_df(ticker,json_data, fetchUnderlying=False)
       
        return data
    
