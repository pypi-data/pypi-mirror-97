# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 21:46:15 2021

@author: Sangoi
"""
import requests
import json
import pandas as pd

class EquityApi(object):
    """
        This class hold all methods to access equity data
      
    """
    
    def __init__(self, key):
        """ 
        Initialize the class
        Keyword Arguments:
            key:  RDUAccess api key

        """
        
        self.key = key
        #self.all_column_list = ["ct_exchCd","ct_lstngCycleTp","ct_omic","ct_segTp","ct_smic","ct_tckSz","ct_tckVal","ct_trdStsTp","ct_vndrExchCd","ct_ticker","ct_bbgIdBBGlobal","ct_rduSecId","ct_rduSegId","ct_bbgCompositeIdBbGlobal","ct_rduSecIdExp","ct_rduSegIdExp","ct_gmiFullPrdCd","p_name","p_roundLotSz","p_clrngCd","p_name","p_roundLotSz","p_trdCtyCd","p_trdCcyMajorFl","p_trdCcyCd","p_dayNum","p_maxOrdSz","p_tckSzDnmntr","p_prdTp","p_flexElgblFl","p_clrngCcyCd","p_msrmntUntCd","p_tckSzNmrtr","p_spotMnthPosLmt","p_mnthPosLmt","p_allMnthPosLmt","p_blckTrdElgblFl","p_actFl","p_exchCd","p_wkNum","p_exchRptngLvl","p_cftcRptngLvl","p_trdStsTp","p_cftcRegFl","p_undlRltnsTp","p_clrngCd","p_rduPrdId","c_name","c_assetTp","c_expDt","c_lstTrdDt","c_settleDt","c_frstDlvryDt","c_frstNtcDt","c_lstDlvryDt","c_name","c_vndrAssetTp","c_prntAssetTp","c_strikePx","c_cfi","c_yrCd","c_settleTp","c_ctrSz","c_frstTrdDt","c_settleFixDt","c_numOfLegs","c_accrlStrtDt","c_accrlEndDt","c_mnthCd","c_dayNum","c_pntVal","c_flexFl","c_actFl","c_wkNum","c_lstNtcDt","c_trdStsTp","c_cfiCd","c_isin","c_bbgTicker","c_bbgIdBbUnique","c_aiiCode"] 

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

    def __convert_json_to_df(self, input_key,json_data, columnList=[]):
        df = pd.json_normalize(json_data) 
        content =  df.get('content')
        msg = df.get('responseCode')
        
        isSuccess = msg[0][0].startswith('S')
        contract_dict = {}
        instrument_dict = {}

        if(isSuccess):
            ins = content.iloc[0][0].get('instrument')
            
            securities = ins.get('securities')
            
            for security in securities:
            
                contract_dict = {}
                contract_dict['success'] = True
                
                #contract_dict['australiaInstrumentId'] = ins.get('australiaInstrumentId')[0].get('value')
                contract_dict['bbgIdBbGlobalShareClassLevel'] = ins.get('bbgIdBbGlobalShareClassLevel')[0].get('value')
                contract_dict['bbgMarketSectorDes'] = ins.get('bbgMarketSectorDes')[0].get('value')
                contract_dict['bbgSecurityTyp'] = ins.get('bbgSecurityTyp')[0].get('value')
                contract_dict['bbgSecurityTyp2'] = ins.get('bbgSecurityTyp2')[0].get('value')
                contract_dict['nameLong'] = ins.get('nameLong')[0].get('value')
                contract_dict['shareClass'] = ins.get('shareClass')[0].get('value')
                contract_dict['countryOfTaxationCode'] = ins.get('countryOfTaxationCode')[0].get('value')
                contract_dict['countryOfTaxationName'] = ins.get('countryOfTaxationName')[0].get('value')
                contract_dict['instrumentTypeCode'] = ins.get('instrumentTypeCode')[0].get('value')
                contract_dict['instrumentTypeName'] = ins.get('instrumentTypeName')[0].get('value')
                contract_dict['issueCountryCode'] = ins.get('issueCountryCode')[0].get('value')
                contract_dict['issueCountryName'] = ins.get('issueCountryName')[0].get('value')
                if(security.get('bbgCompositeExchangeCode') is not None) : contract_dict['bbgCompositeExchangeCode'] = security.get('bbgCompositeExchangeCode')[0].get('value')
                if(security.get('bbgCompositeIdBbGlobal') is not None) : contract_dict['bbgCompositeIdBbGlobal'] = security.get('bbgCompositeIdBbGlobal')[0].get('value')
                if(security.get('bbgCompositeTicker') is not None) : contract_dict['bbgCompositeTicker'] = security.get('bbgCompositeTicker')[0].get('value')
                if(security.get('bbgIdBbGlobal') is not None) : contract_dict['bbgIdBbGlobal'] = security.get('bbgIdBbGlobal')[0].get('value')
                if(security.get('bbgSecurityDes') is not None) : contract_dict['bbgSecurityDes'] = security.get('bbgSecurityDes')[0].get('value')
                if(security.get('bbgIdBbUnique') is not None) : contract_dict['bbgIdBbUnique'] = security.get('bbgIdBbUnique')[0].get('value')

                
                contract_dict['exchangeTicker'] = security.get('exchangeTicker')[0].get('value')
                contract_dict['listingStatus'] = security.get('listingStatus')[0].get('value')
                contract_dict['rduSecurityId'] = security.get('rduSecurityId')[0].get('value')
                contract_dict['ric'] = security.get('ric')[0].get('value')
                contract_dict['ticker'] = security.get('ticker')[0].get('value')
                contract_dict['tradingSymbol'] = security.get('tradingSymbol')[0].get('value')
                contract_dict['trConsolidatedRic'] = security.get('trConsolidatedRic')[0].get('value')
                contract_dict['trQuoteId'] = security.get('trQuoteId')[0].get('value')
                contract_dict['vendorExchangeCode'] = security.get('vendorExchangeCode')[0].get('value')
                contract_dict['exchangeCode'] = security.get('exchangeCode')[0].get('value')
                contract_dict['exchangeName'] = security.get('exchangeName')[0].get('value')
                contract_dict['officialPlaceOfListingMic'] = security.get('officialPlaceOfListingMic')[0].get('value')
                contract_dict['officialPlaceOfListingMicName'] = security.get('officialPlaceOfListingMicName')[0].get('value')
                contract_dict['operatingMic'] = security.get('operatingMic')[0].get('value')
                #contract_dict['operatingMicName'] = security.get('operatingMicName')[0].get('value')
                contract_dict['periodicCallAuctionFlag'] = security.get('periodicCallAuctionFlag')[0].get('value')
                contract_dict['primaryRicFlag'] = security.get('primaryRicFlag')[0].get('value')
                contract_dict['ptmLevyEligibleFlag'] = security.get('ptmLevyEligibleFlag')[0].get('value')
                contract_dict['securityStatus'] = security.get('securityStatus')[0].get('value')
                contract_dict['securityStatusName'] = security.get('securityStatusName')[0].get('value')
                contract_dict['segmentMic'] = security.get('segmentMic')[0].get('value')
                #contract_dict['segmentMicName'] = security.get('segmentMicName')[0].get('value')
                contract_dict['shHkStockConnectEligibleFlag'] = security.get('shHkStockConnectEligibleFlag')[0].get('value')
                contract_dict['shortSellEligibleFlag'] = security.get('shortSellEligibleFlag')[0].get('value')
                contract_dict['stampDutyReserveTaxFlag'] = security.get('stampDutyReserveTaxFlag')[0].get('value')
                contract_dict['suspendedFlag'] = security.get('suspendedFlag')[0].get('value')
                #contract_dict['tradeCountryCode'] = security.get('tradeCountryCode')[0].get('value')
                contract_dict['tradeCountryName'] = security.get('tradeCountryName')[0].get('value')
                contract_dict['tradeCurrencyCode'] = security.get('tradeCurrencyCode')[0].get('value')
                contract_dict['tradeCurrencyName'] = security.get('tradeCurrencyName')[0].get('value')
                contract_dict['whenDistributedFlag'] = security.get('whenDistributedFlag')[0].get('value')
                contract_dict['whenIssuedFlag'] = security.get('whenIssuedFlag')[0].get('value')
                contract_dict['listingDate'] = security.get('listingDate')[0].get('value')
                contract_dict['numberOfDaysToSettle'] = security.get('numberOfDaysToSettle')[0].get('value')
                contract_dict['roundLotSize'] = security.get('roundLotSize')[0].get('value')



                
                exchCd = security.get('exchangeCode')[0].get('value')
                instrument_dict[input_key+"_"+exchCd] = contract_dict
                
        else:
            contract_dict = {}
            contract_dict['success'] = False
            contract_dict['failed_message'] = df.get('responseString')[0][0]
            instrument_dict[input_key] = contract_dict

            
        data = pd.DataFrame.from_dict(instrument_dict, orient='index')
        
        return data       



    def get_by_isin(self, isin):
        """
        
        This will return the equity data given the isin
        Parameters
        ----------
        isin : String
            The ISIN code.

        Returns
        -------
        data : dataframe
            this will return a dataframe with key as isin+exchange.

        """
        #print("Calling getByIsin with isin "+isin)
        query = {'isin':isin}
        json_data = self.__call_api(query, 'https://65stvtuo0h.execute-api.eu-west-2.amazonaws.com/FreeTrial/equity/search/v1/getByISIN')
            
        data = self.__convert_json_to_df(isin,json_data)
        return data

    def get_by_isin_exchange(self, isin, exchange):
        """
        
        This will return the equity data given the isin
        Parameters
        ----------
        isin : String
            The ISIN code.
        exchange : String
            exchange code 
        Returns
        -------
        data : dataframe
            this will return a dataframe with key as isin+exchange.

        """
        #print("Calling getByIsin with isin "+isin)
        query = {'isin':isin,'mic':exchange}
        json_data = self.__call_api(query, 'https://65stvtuo0h.execute-api.eu-west-2.amazonaws.com/FreeTrial/equity/search/v1/getByISINMIC')
            
        data = self.__convert_json_to_df(isin,json_data)
        return data
    