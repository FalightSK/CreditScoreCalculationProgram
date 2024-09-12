import numpy as np
from Script.customerInfo import PaymentInfo, FinancialInfo, extract_fin_info
import Script.databaseClient as db
from datetime import datetime

def cal_payment_his(payment_info, credit_term= 30, show= False):
    # Set initial value
    if payment_info.stat == 'FULL':
        S0 = 850
    elif payment_info.stat == 'PARTIAL':
        S0 = 680
    else:
        S0 = 300
        return S0
        
    # Late penalty
    late_days = (payment_info.paid_date - payment_info.order_date).days - credit_term
    late_days = 0 if late_days < 0 else late_days
    # print(late_days)
    
    # Final calculation
    if late_days > 15:
        Sf = 300
    else:
        Sf = S0 * np.power(0.95, late_days)
    
    return Sf

def cal_amount_owed(payment_info, show= False):
    # Set Initial value
    if payment_info.stat == 'FULL':
        S0 = 850
    elif payment_info.stat == 'PARTIAL':
        S0 = 700
    else:
        S0 = 300
        return S0
        
    # Delay penalty
    delay_time = (payment_info.paid_date - payment_info.order_date).days
    if payment_info.stat == 'FULL':
        S0 -= (delay_time * 10)
    else:
        S0 -= (delay_time * 15)
        
    # Adjustment vased on order size
    P = payment_info.amount
    if P > 10000:
        A = 18 * (np.exp(0.0001 * (P - 10000)) - 1)
    else:
        A = -100 * (np.exp(0.0003 * (P - 10000)) - 1)
    A = 100 if A > 100 else -100 if A < -100 else A
    S0 += A 
    
    # Multiplier
    M = payment_info.method
    if M == 'CASH':
        M = 1.05
    elif M == 'IN_STORE':
        M = 1.03
    elif M == 'OTHERS':
        M = 1.02
    else:
        M = 1
    S0 *= M
    
    # Final score cap
    Sf = np.max([np.min([S0, 850]), 300])
    if show: print(f'> Delay Time: {delay_time}\n> Adjustment: {A}\n> Multiplier: {M}\n')
    return Sf
        
def cal_credit_history_lenght(customer_id, show = False):
    n = db.get_number_of_order_by_id(customer_id)
    info = db.get_info_by_id(customer_id)
    
    # Freq
    customer_type = info['type']
    criteria = db.get_criteria_credit_history(customer_type)
    
    x = n//criteria[1]
    x = 12 if x > 12 else x
    if show: print('x->', x)
    
    Sf_freq = 300 + (x * 550/12)
    
    # Value
    val = 0
    for data in info['records']:
        val += data['amount']
    x = val//criteria[0]
    if show: print('x->', x)
    
    Sf_val = 300 + (x * 550/12)
    
    return min([Sf_freq, Sf_val])

def cal_credit_mix(customer_id, show= False):
    info = db.get_info_by_id(customer_id)['financial_info']
    # print(info)
    if len(info) == 0:
        return 0
    
    financial_info = FinancialInfo()
    financial_info.JSON_to_FinancialInfo(info[len(info) - 1])
    # financial_info.show()
    
    credit_mix_ratio = financial_info.current_assets / financial_info.total_liabilities
    debt_to_equity = 1 - (financial_info.total_liabilities / financial_info.shareholder_equity)
    debt_to_assets = 1 - (financial_info.total_liabilities / financial_info.total_assets)
    
    debt_to_equity = 1 if debt_to_equity > 1 else 0 if debt_to_equity < 0 else debt_to_equity
    debt_to_assets = 1 if debt_to_assets > 1 else 0 if debt_to_assets < 0 else debt_to_assets

    if show: print('>value:', credit_mix_ratio, debt_to_equity, debt_to_assets)
    credit_mix = (0.6 * credit_mix_ratio + 0.2 * debt_to_equity + 0.2 * debt_to_assets) * 550 + 300
    return credit_mix

def cal_new_credit(customer_id, requested_budget, show= False):
    customer_info = db.get_info_by_id(customer_id)
    
    if customer_info['record_summary']['n'] < 30:
        if show: print('order less than 30')
        n_fin_record = len(customer_info['financial_info'])
        if n_fin_record == 0:
            return 0
        
        new_credit_list = []
        all_fin_info = []
        for i in range(n_fin_record):
            fin_info = FinancialInfo()
            fin_info.JSON_to_FinancialInfo(customer_info['financial_info'][i])
            all_fin_info.append(fin_info)
            # fin_info.show()
            # print(new_credit_list)
            
            if i == 0:
                if show: print('first of list')
                continue
            ratio_of_liabilities_difference = (all_fin_info[i].total_liabilities - all_fin_info[i-1].total_liabilities) / all_fin_info[i-1].total_liabilities
            new_credit_list.append((550 / (1 + np.exp(5 * ratio_of_liabilities_difference))) + 300)
            
            if show: print(i, ratio_of_liabilities_difference, new_credit_list)
        
        Sf = np.mean(new_credit_list)
    
    else:
        if show: print('order more than 30')
        mean = db.get_mean_by_id(customer_id)
        std = db.get_std_by_id(customer_id)
        
        z = (requested_budget - mean) / std
        Sf = 850 - 20 * np.exp(1.65 * z)
        
    return Sf

def cal_FICO_current(payment_his, amoutn_owed, credit_his_len, credti_mix, new_credit):
    return 0.35 * payment_his + 0.3 * amoutn_owed + 0.15 * credit_his_len + 0.1 * credti_mix + 0.1 * new_credit

if __name__ == '__main__':
    customer_ID = '00007'
    requested_budget = 10000
    
    test_customer = db.get_info_by_id(customer_ID)
    
    P = PaymentInfo()
    P.JSON_to_PaymentInfo(test_customer['records'][0])
    # P.show()
    

    print('>> payment_his:', cal_payment_his(P))
    print('>> amount_owed:', cal_amount_owed(P))
    print('>> credit_mix:', cal_credit_mix(customer_ID))
    print('>> credit_his_len:', cal_credit_history_lenght(customer_ID))
    print('>> new_credit:', cal_new_credit(customer_ID, requested_budget))
    
    print('>>>>> FICO:', cal_FICO_current(cal_payment_his(P), cal_amount_owed(P), cal_credit_mix(customer_ID), cal_credit_history_lenght(customer_ID), cal_new_credit(customer_ID, requested_budget)), '<<<<<')
    
    # print('credit mix:', cal_credit_mix('00007'))



    