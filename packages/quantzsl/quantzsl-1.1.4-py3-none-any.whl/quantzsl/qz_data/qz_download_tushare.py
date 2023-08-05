# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 13:09:04 2019

@author: ZSL
"""
import pandas as pd
import numpy as np
import time
import datetime
import warnings
import json
warnings.filterwarnings("ignore")
import tushare as ts
import quantzsl as qz
def qz_download_stock_day_data_from_tushare(trade_date='20190102'):   
    trade_date = trade_date.replace('-', '') #兼容设置以防日期格式为2001-10-20格式
    lastEx = None
    retry = 10
    for _ in range(retry):
        try:
            pro=qz.qz_ts_pro()
            df_daily=pro.query('daily',trade_date=trade_date)
            df_daily_basic=pro.query('daily_basic',trade_date=trade_date)
            df_factor=pro.query('adj_factor',trade_date=trade_date) 
#            df_daily_basic=df_daily_basic.fillna(0)            
#            if df_daily.isnull().sum().sum()>0  or df_daily_basic.isnull().sum().sum()>0  or df_factor.isnull().sum().sum() > 0:
            break 
        except Exception as ex:
            lastEx = ex
            print("[{}]TuSharePro数据异常: {}, retrying...".format(trade_date, ex))
    else:
        print("[{}]TuSharePro异常: {}, retried {} times".format(trade_date,lastEx, retry))
        return None   
    df=pd.merge(df_daily,df_factor,how='left')
    res=pd.merge(df,df_daily_basic,how='left').sort_values(by = 'ts_code')
    res['code']=res['ts_code'].apply(lambda x:x[:6]) #x[7:9].lower()
    res.rename(columns={'trade_date':'date'}, inplace=True)
    res['amount']=res['amount']/10
    res['date'] =[ i[0:4]+'-'+i[4:6]+'-'+i[6:8]  for i in res['date']]    
    #res['datetime'] = pd.to_datetime(res['date'], format='%Y-%m-%d')
    return res 

def qz_download_index_day_data_from_tushare(code,trade_date='20190102'):  
    '''
    等tushare 出了 类似股票那样的指数获取方式在弄
    '''
    trade_date = trade_date.replace('-', '') #兼容设置以防日期格式为2001-10-20格式
    lastEx = None
    retry = 10
    for _ in range(retry):
        try:
            pro=qz.qz_ts_pro()
            pro.index_daily(ts_code='399300.SZ', trade_date=trade_date)
            pro.index_daily(ts_code=['399300.SZ','000001.SH'],trade_date=trade_date)
            df_daily_basic=pro.query('daily_basic',trade_date=trade_date)
            df_factor=pro.query('adj_factor',trade_date=trade_date) 
#            df_daily_basic=df_daily_basic.fillna(0)            
#            if df_daily.isnull().sum().sum()>0  or df_daily_basic.isnull().sum().sum()>0  or df_factor.isnull().sum().sum() > 0:
            break 
        except Exception as ex:
            lastEx = ex
            print("[{}]TuSharePro数据异常: {}, retrying...".format(trade_date, ex))
    else:
        print("[{}]TuSharePro异常: {}, retried {} times".format(trade_date,lastEx, retry))
        return None   
    df=pd.merge(df_daily,df_factor,how='left')
    res=pd.merge(df,df_daily_basic,how='left').sort_values(by = 'ts_code')
    res['code']=res['ts_code'].apply(lambda x:x[:6]) #x[7:9].lower()
    res.rename(columns={'trade_date':'date'}, inplace=True)
    res['amount']=res['amount']/10
    res['date'] =[ i[0:4]+'-'+i[4:6]+'-'+i[6:8]  for i in res['date']]    
    #res['datetime'] = pd.to_datetime(res['date'], format='%Y-%m-%d')
    return res       
def qz_download_stock_list_from_tushare():   
    pro=qz.qz_ts_pro()
    stock_list_l= pro.stock_basic(exchange_id='', is_hs='',list_status='L' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    stock_list_D= pro.stock_basic(exchange_id='', is_hs='',list_status='D' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    stock_list_P= pro.stock_basic(exchange_id='', is_hs='',list_status='P' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')          
    stock_list=pd.concat([stock_list_l,stock_list_D],axis=0)
    stock_list=pd.concat([stock_list,stock_list_P],axis=0)
    stock_list['list_date'] =[ i[0:4]+'-'+i[4:6]+'-'+i[6:8]  for i in stock_list['list_date']]     
    return stock_list

def qz_download_index_list_from_tushare():   
    pro=qz.qz_ts_pro()
    申万指数= pro.index_basic(market='SW') 
    中证指数 = pro.index_basic(market='CSI') 
    上交所指数 = pro.index_basic(market='SSE')     
    深交所指数 = pro.index_basic(market='SZSE') 
#    MSCI指数 = pro.index_basic(market='MSCI')       
#    中金所指数 = pro.index_basic(market='CICC') 
#    国证指数 = pro.index_basic(market='CNI') 
#    其他指数 = pro.index_basic(market='OTH')
    df=pd.concat([申万指数,中证指数],axis=0) 
    df=pd.concat([df,上交所指数],axis=0)  
    df=pd.concat([df,深交所指数],axis=0)
    df['symbol']=df.ts_code.apply(lambda x:x[:6])
    df=df.set_index(np.arange(len(df)))
    #df['list_date'] =[ i[0:4]+'-'+i[4:6]+'-'+i[6:8]  for i in df['list_date']]         
    return df

def qz_download_stock_moneyflow_from_tushare(trade_date='20190102'):   
    trade_date = trade_date.replace('-', '') #兼容设置以防日期格式为2001-10-20格式
    lastEx = None
    retry = 10
    for _ in range(retry):
        try:
            pro =qz.QZ_ts_pro()
            list_=['ts_code','trade_date','buy_sm_vol','buy_sm_amount','sell_sm_vol','sell_sm_amount','buy_md_vol',
                   'buy_md_amount','sell_md_vol','sell_md_amount','buy_lg_vol','buy_lg_amount','sell_lg_vol','sell_lg_amount',
                   'buy_elg_vol','buy_elg_amount','sell_elg_vol','sell_elg_amount','net_mf_vol','net_mf_amount']
            df = pro.moneyflow(trade_date=trade_date,fields=list_)
            break 
        except Exception as ex:
            lastEx = ex
            print("[{}]TuSharePro数据异常: {}, retrying...".format(trade_date, ex))
    else:
        print("[{}]TuSharePro异常: {}, retried {} times".format(trade_date,lastEx, retry))
        return None   
    res=df.sort_values(by = 'ts_code')
    res['code']=res['ts_code'].apply(lambda x:x[:6]) #x[7:9].lower()
    res.rename(columns={'trade_date':'date'}, inplace=True)
    res['date'] =[ i[0:4]+'-'+i[4:6]+'-'+i[6:8]  for i in res['date']]    
    #res['datetime'] = pd.to_datetime(res['date'], format='%Y-%m-%d')
    return res 

def QZ_download_finance_income_from_tushare(period='20181231'): 
    #token='e0eeb08befd1f07516df2cbf9cbd58663f77fd72f92a04f290291c9d'
    #pro = ts.pro_api(token)
    period = period.replace('-', '') #兼容设置以防日期格式为2001-10-20格式    
    pro=QZ.QZ_ts_pro()
    #利润表
    list_income=['ts_code','ann_date','f_ann_date','end_date','report_type','comp_type','basic_eps','diluted_eps',
'total_revenue','revenue','int_income','prem_earned','comm_income','n_commis_income','n_oth_income','n_oth_b_income',
'prem_income','out_prem','une_prem_reser','reins_income','n_sec_tb_income','n_sec_uw_income','n_asset_mg_income',
'oth_b_income','fv_value_chg_gain','invest_income','ass_invest_income','forex_gain','total_cogs','oper_cost',
'int_exp','comm_exp','biz_tax_surchg','sell_exp','admin_exp','fin_exp','assets_impair_loss','prem_refund',
'compens_payout','reser_insur_liab','div_payt','reins_exp','oper_exp','compens_payout_refu','insur_reser_refu',
'reins_cost_refund','other_bus_cost','operate_profit','non_oper_income','non_oper_exp','nca_disploss','total_profit',
'income_tax','n_income','n_income_attr_p','minority_gain','oth_compr_income','t_compr_income','compr_inc_attr_p',
'compr_inc_attr_m_s','ebit','ebitda','insurance_exp','undist_profit','distable_profit']
    df_income = pro.income_vip(period=period,fields=list_income)     
    return df_income
def qz_download_finance_balancesheet_from_tushare(period='20181231'): 
    period = period.replace('-', '') #兼容设置以防日期格式为2001-10-20格式    
    pro=qz.qz_ts_pro()
    #资产股债表  
    list_balancesheet=['ts_code','ann_date','f_ann_date','end_date','report_type','comp_type','total_share',
'cap_rese','undistr_porfit','surplus_rese','special_rese','money_cap','trad_asset','notes_receiv','accounts_receiv',
'oth_receiv','prepayment','div_receiv','int_receiv','inventories','amor_exp','nca_within_1y','sett_rsrv',
'loanto_oth_bank_fi','premium_receiv','reinsur_receiv','reinsur_res_receiv','pur_resale_fa','oth_cur_assets',
'total_cur_assets','fa_avail_for_sale','htm_invest','lt_eqt_invest','invest_real_estate','time_deposits','oth_assets',
'lt_rec','fix_assets','cip','const_materials','fixed_assets_disp','produc_bio_assets','oil_and_gas_assets','intan_assets',
'r_and_d','goodwill','lt_amor_exp','defer_tax_assets','decr_in_disbur','oth_nca','total_nca','cash_reser_cb',
'depos_in_oth_bfi','prec_metals','deriv_assets','rr_reins_une_prem','rr_reins_outstd_cla','rr_reins_lins_liab','rr_reins_lthins_liab',
'refund_depos','ph_pledge_loans','refund_cap_depos','indep_acct_assets','client_depos','client_prov','transac_seat_fee',
'invest_as_receiv','total_assets','lt_borr','st_borr','cb_borr','depos_ib_deposits','loan_oth_bank','trading_fl',
'notes_payable','acct_payable','adv_receipts','sold_for_repur_fa','comm_payable','payroll_payable','taxes_payable',
'int_payable','div_payable','oth_payable','acc_exp','deferred_inc','st_bonds_payable','payable_to_reinsurer','rsrv_insur_cont',
'acting_trading_sec','acting_uw_sec','non_cur_liab_due_1y','oth_cur_liab','total_cur_liab','bond_payable',
'lt_payable','specific_payables','estimated_liab','defer_tax_liab','defer_inc_non_cur_liab','oth_ncl',
'total_ncl','depos_oth_bfi','deriv_liab','depos','agency_bus_liab','oth_liab','prem_receiv_adva','depos_received',
'ph_invest','reser_une_prem','reser_outstd_claims','reser_lins_liab','reser_lthins_liab','indept_acc_liab','pledge_borr',
'indem_payable','policy_div_payable','total_liab','treasury_share','ordin_risk_reser','forex_differ','invest_loss_unconf',
'minority_int','total_hldr_eqy_exc_min_int','total_hldr_eqy_inc_min_int','total_liab_hldr_eqy','lt_payroll_payable',
'oth_comp_income','oth_eqt_tools','oth_eqt_tools_p_shr','lending_funds','acc_receivable','st_fin_payable','payables',
'hfs_assets','hfs_sales']
    df_balancesheet = pro.balancesheet_vip(period=period,fields=list_balancesheet)
    return df_balancesheet
def qz_download_finance_cashflow_from_tushare(period='20181231'): 
    period = period.replace('-', '') #兼容设置以防日期格式为2001-10-20格式    
    pro=qz.qz_ts_pro()
    #现金流量表    
    list_cashflow=['ts_code','ann_date','f_ann_date','end_date','comp_type','report_type','net_profit',
'finan_exp','c_fr_sale_sg','recp_tax_rends','n_depos_incr_fi','n_incr_loans_cb','n_inc_borr_oth_fi','prem_fr_orig_contr',
'n_incr_insured_dep','n_reinsur_prem','n_incr_disp_tfa','ifc_cash_incr','n_incr_disp_faas','n_incr_loans_oth_bank',
'n_cap_incr_repur','c_fr_oth_operate_a','c_inf_fr_operate_a','c_paid_goods_s','c_paid_to_for_empl','c_paid_for_taxes',
'n_incr_clt_loan_adv','n_incr_dep_cbob','c_pay_claims_orig_inco','pay_handling_chrg','pay_comm_insur_plcy','oth_cash_pay_oper_act',
'st_cash_out_act','n_cashflow_act','oth_recp_ral_inv_act','c_disp_withdrwl_invest','c_recp_return_invest','n_recp_disp_fiolta',
'n_recp_disp_sobu','stot_inflows_inv_act','c_pay_acq_const_fiolta','c_paid_invest','n_disp_subs_oth_biz','oth_pay_ral_inv_act',
'n_incr_pledge_loan','stot_out_inv_act','n_cashflow_inv_act','c_recp_borrow','proc_issue_bonds','oth_cash_recp_ral_fnc_act',
'stot_cash_in_fnc_act','free_cashflow','c_prepay_amt_borr','c_pay_dist_dpcp_int_exp','incl_dvd_profit_paid_sc_ms','oth_cashpay_ral_fnc_act',
'stot_cashout_fnc_act','n_cash_flows_fnc_act','eff_fx_flu_cash','n_incr_cash_cash_equ','c_cash_equ_beg_period','c_cash_equ_end_period',
'c_recp_cap_contrib','incl_cash_rec_saims','uncon_invest_loss','prov_depr_assets','depr_fa_coga_dpba','amort_intang_assets',
'lt_amort_deferred_exp','decr_deferred_exp','incr_acc_exp','loss_disp_fiolta','loss_scr_fa','loss_fv_chg',
'invest_loss','decr_def_inc_tax_assets','incr_def_inc_tax_liab','decr_inventories','decr_oper_payable','incr_oper_payable',
'others','im_net_cashflow_oper_act','conv_debt_into_cap','conv_copbonds_due_within_1y','fa_fnc_leases','end_bal_cash',
'beg_bal_cash','end_bal_cash_equ','beg_bal_cash_equ','im_n_incr_cash_equ']
    df_cashflow = pro.cashflow_vip(end_date=period,fields=list_cashflow)
    return df_cashflow
def qz_download_finance_forecast_from_tushare(period='20181231'): 
    period = period.replace('-', '') #兼容设置以防日期格式为2001-10-20格式    
    pro=qz.qz_ts_pro()   
    #业绩预告表    
    list_forecast=['ts_code','ann_date','end_date','type','p_change_min','p_change_max','net_profit_min','net_profit_max',
'last_parent_net','first_ann_date','summary','change_reason']
    df_forecast = pro.forecast_vip(end_date=period,fields=list_forecast) 
    return df_forecast 
def qz_download_finance_express_from_tushare(period='20181231'): 
    period = period.replace('-', '') #兼容设置以防日期格式为2001-10-20格式    
    pro=qz.qz_ts_pro()            
    #业绩快报表      
    list_express=['ts_code','ann_date','end_date','revenue','operate_profit','total_profit','n_income',
'total_assets','total_hldr_eqy_exc_min_int','diluted_eps','diluted_roe','yoy_net_profit','bps','yoy_sales',
'yoy_op','yoy_tp','yoy_dedu_np','yoy_eps','yoy_roe','growth_assets','yoy_equity','growth_bps','or_last_year',
'op_last_year','tp_last_year','np_last_year','eps_last_year','open_net_assets','open_bps','perf_summary','is_audit',
'remark']
    df_express = pro.express_vip(end_date=period,fields=list_express)
    return df_express    
#分红送股好像没有批量方式 先不下
#    list_dividend=['ts_code','end_date','ann_date','div_proc','stk_div','stk_bo_rate','stk_co_rate','cash_div',
#'cash_div_tax','record_date','ex_date','pay_date','div_listdate','imp_ann_date','base_date','base_share']
#    df_dividend = pro.dividend_vip(end_date='20181231',fields=list_dividend)
def qz_download_finance_fina_indicator_from_tushare(period='20181231'): 
    period = period.replace('-', '') #兼容设置以防日期格式为2001-10-20格式    
    pro=qz.qz_ts_pro()         
    #财务指标数据表
    list_fina_indicator=['ts_code','ann_date','end_date','eps','dt_eps','total_revenue_ps','revenue_ps','capital_rese_ps','surplus_rese_ps',
'undist_profit_ps','extra_item','profit_dedt','gross_margin','current_ratio','quick_ratio','cash_ratio',
'invturn_days','arturn_days','inv_turn','ar_turn','ca_turn','fa_turn','assets_turn','op_income','valuechange_income',
'interst_income','daa','ebit','ebitda','fcff','fcfe','current_exint','noncurrent_exint','interestdebt','netdebt',
'tangible_asset','working_capital','networking_capital','invest_capital','retained_earnings','diluted2_eps',
'bps','ocfps','retainedps','cfps','ebit_ps','fcff_ps','fcfe_ps','netprofit_margin','grossprofit_margin','cogs_of_sales',
'expense_of_sales','profit_to_gr','saleexp_to_gr','adminexp_of_gr','finaexp_of_gr','impai_ttm','gc_of_gr',
'op_of_gr','ebit_of_gr','roe','roe_waa','roe_dt','roa','npta','roic','roe_yearly','roa2_yearly','roe_avg',
'opincome_of_ebt','investincome_of_ebt','n_op_profit_of_ebt','tax_to_ebt','dtprofit_to_profit','salescash_to_or',
'ocf_to_or','ocf_to_opincome','capitalized_to_da','debt_to_assets','assets_to_eqt','dp_assets_to_eqt','ca_to_assets',
'nca_to_assets','tbassets_to_totalassets','int_to_talcap','eqt_to_talcapital','currentdebt_to_debt','longdeb_to_debt',
'ocf_to_shortdebt','debt_to_eqt','eqt_to_debt','eqt_to_interestdebt','tangibleasset_to_debt','tangasset_to_intdebt',
'tangibleasset_to_netdebt','ocf_to_debt','ocf_to_interestdebt','ocf_to_netdebt','ebit_to_interest','longdebt_to_workingcapital',
'ebitda_to_debt','turn_days','roa_yearly','roa_dp','fixed_assets','profit_prefin_exp','non_op_profit','op_to_ebt',
'nop_to_ebt','ocf_to_profit','cash_to_liqdebt','cash_to_liqdebt_withinterest','op_to_liqdebt','op_to_debt',
'roic_yearly','profit_to_op','q_opincome','q_investincome','q_dtprofit','q_eps','q_netprofit_margin','q_gsprofit_margin',
'q_exp_to_sales','q_profit_to_gr','q_saleexp_to_gr','q_adminexp_to_gr','q_finaexp_to_gr','q_impair_to_gr_ttm','q_gc_to_gr',
'q_op_to_gr','q_roe','q_dt_roe','q_npta','q_opincome_to_ebt','q_investincome_to_ebt','q_dtprofit_to_profit','q_salescash_to_or',
'q_ocf_to_sales','q_ocf_to_or','basic_eps_yoy','dt_eps_yoy','cfps_yoy','op_yoy','ebt_yoy','netprofit_yoy','dt_netprofit_yoy',
'ocf_yoy','roe_yoy','bps_yoy','assets_yoy','eqt_yoy','tr_yoy','or_yoy','q_gr_yoy','q_gr_qoq','q_sales_yoy',
'q_sales_qoq','q_op_yoy','q_op_qoq','q_profit_yoy','q_profit_qoq','q_netprofit_yoy','q_netprofit_qoq','equity_yoy',
'rd_exp']
    df_fina_indicator = pro.fina_indicator_vip(end_date=period,fields=list_fina_indicator)
    return df_fina_indicator 
#主营业务构成  此部分感觉应该分开获取 目前用不到 先不弄    
#    list_fina_mainbz=['ts_code','end_date','bz_item','bz_sales','bz_profit','bz_cost','curr_type','update_flag']           
#    df_fina_mainbz = pro.fina_mainbz_vip(end_date=period,fields=list_fina_mainbz)
def qz_download_finance_disclosure_date_from_tushare(period='20181231'): 
    period = period.replace('-', '') #兼容设置以防日期格式为2001-10-20格式    
    pro=qz.qz_ts_pro()
    #财报披露计划表
    list_disclosure_date=['ts_code','ann_date','end_date','pre_date','actual_date','modify_date']
    df_disclosure_date= pro.disclosure_date(end_date=period,fields=list_disclosure_date) 
          #利润 知产负债 现金流 业绩预告 业绩快报 财务指标 财务审计意见 财务披露日期           
    return df_disclosure_date

if __name__ == '__main__': 
    data=qz_download_day_data_from_tushare()
    """需要对于datetime 和date 进行转换, 以免直接被变成了时间戳"""
    if 'datetime' in data.columns:
        data.datetime = data.datetime.apply(str)
    if 'date' in data.columns:
        data.date = data.date.apply(str)
    json_data = json.loads(data.reset_index().to_json(orient='records')) 
    pro=qz.qz_ts_pro()
    aa=ts.pro_bar(pro_api=pro, ts_code='600000.SH', adj='qfq', start_date='20110101', end_date='20181011')
    aa_bfq=ts.pro_bar(pro_api=pro, ts_code='000001.SZ', adj=None, start_date='20110101', end_date='20181011')
    data=qz_download_finance_from_tushare(period='20181231')
    #
        