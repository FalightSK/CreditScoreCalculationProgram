import numpy as np
from customerInfo import PaymentInfo, FinancialInfo
from newCustomer import extract_fin_info
import databaseClient as db


from datetime import datetime

def cal_payment_his(payment_info, credit_term= 30):
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
        
def cal_credit_history_lenght(customer_id):
    x = db.get_number_of_order_by_id(customer_id)
    customer_type = db.get_info_by_id(customer_id)['type']
    print(x)
    
    criteria = db.get_criteria_credit_history(customer_type)
    
    print(criteria[])
    Sf = 300 + (x/criteria * 550/12)
    return Sf

def cal_credit_mix(customer_id, show= False):
    info = db.get_info_by_id(customer_id)['financial_info']
    financial_info = FinancialInfo()
    financial_info.JSON_to_FinancialInfo(info[len(info) - 1])
    financial_info.show()
    
    if financial_info.total_assets is None:
        return 0
    
    credit_mix_ratio = financial_info.current_assets / financial_info.total_liabilities
    debt_to_equity = 1 - (financial_info.total_liabilities / financial_info.shareholder_equity)
    debt_to_assets = 1 - (financial_info.total_liabilities / financial_info.total_assets)
    
    debt_to_equity = 1 if debt_to_equity > 1 else 0 if debt_to_equity < 0 else debt_to_equity
    debt_to_assets = 1 if debt_to_assets > 1 else 0 if debt_to_assets < 0 else debt_to_assets

    if show: print('>value:', credit_mix_ratio, debt_to_equity, debt_to_assets)
    credit_mix = (0.6 * credit_mix_ratio + 0.2 * debt_to_equity + 0.2 * debt_to_assets) * 550 + 300
    return credit_mix

def cal_new_credit(customer_id, requested_budget):
    mean = db.get_mean_by_id(customer_id)
    std = db.get_std_by_id(customer_id)
    
    z = (requested_budget - mean) / std
    Sf = 850 - 20 * np.exp(1.65 * z)
    return Sf


if __name__ == '__main__':
    test_customer = db.read()['history']['00001']['records'][0]
    print(test_customer)
    
    P = PaymentInfo()
    P.JSON_to_PaymentInfo(test_customer)
    P.show()
    
    print('val:', cal_amount_owed(P))
    print('credit his len:', cal_credit_history_lenght('00001'))
    # print('credit mix:', cal_credit_mix('00007'))



    
    
    