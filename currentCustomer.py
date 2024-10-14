import numpy as np
from Script.customerInfo import *
import Script.databaseClient as db
# from Script.databaseClient import *
from Script.credit_cal import cal_credit_values ,budget_round
from datetime import datetime
import pandas as pd

# Score calculation
def cal_payment_his(payment_info, credit_term= 15, show= False):
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
    
    if show: print(f'cal_payment_his >> S0: {S0} - LP: {late_days}')
    
    return max(min(Sf, 850), 300)

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
    # delay_time = 0 if delay_time < 0 else delay_time
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
    Sf = max(min(S0, 850), 300)
    if show: print(f'cal_amount_owed >> Delay Time: {delay_time} | Adjustment: {int(A)} | Multiplier: {M}')
    return Sf
        
def cal_credit_history_length(customer_id, show= False):
    info = db.get_info_by_id(customer_id)
    
    customer_type = info['type']
    if customer_type == 'UNKNOWN':
        return 300
    criteria = db.get_criteria_credit_history(customer_type)
    
    this_month = datetime.now().month
    
    n = 0
    x = 0
    prev_month = -1
    for order in info['records'].values():
        
        order_month = order['order_date'][1]
        if this_month == order_month:
            continue
        
        if prev_month != order_month:
            prev_month = order_month
            try:
                if show: print(f' | (M{order_month}, {monthly_n}, {int(monthly_order/monthly_n)})', end= '')
                if monthly_n >= criteria[1] or monthly_order/monthly_n >= criteria[0]:
                    x+=1
            except:
                if show: print('first time', end= '')
                pass
            monthly_order = 0
            monthly_n = 0
            n+=1
            
        if n > 6: break    
        
        monthly_order += order['amount']
        monthly_n += 1

            
    
    # # Freq
    # customer_type = info['type']
    # # print(customer_type)
    # if customer_type == 'UNKNOWN':
    #     return 0
    # criteria = db.get_criteria_credit_history(customer_type)
    
    # x = n//criteria[1]
    # x = 12 if x > 12 else x
    
    # Sf_freq = 300 + (x * 550/12)
    # if show: print(f'cal_credit_history_length >> x_freq-> {x}, {Sf_freq}', end= ' | ')
    
    # # Value
    # val = 0
    # for data_id, data in info['records'].items():
    #     val += data['amount']
    # x = val//criteria[0]
    
    # Sf_val = 300 + (x * 550/12)
    # if show: print(f'x_val -> {x}, {Sf_val}')
    
    if show: print(f' >>>>> x: {x}, n: {n}')
    try:
        Sf = 300 + (x * 550/(n-1))
        Sf = max(min(Sf, 850), 300)
    except:
        Sf = 300
    return Sf

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

    if show: print('cal_credit_mix >> value:', credit_mix_ratio, debt_to_equity, debt_to_assets)
    credit_mix = (0.6 * credit_mix_ratio + 0.2 * debt_to_equity + 0.2 * debt_to_assets) * 550 + 300
    return credit_mix

def cal_new_credit(customer_id, requested_budget, payment_stat= "OVERDUE", set_n= 100, show= False):
    customer_info = db.get_info_by_id(customer_id)
    if show: print('cal_new_credit >> ', end= '')
    
    if customer_info['record_summary']['n'] < 30 or set_n < 30:
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
        
        if len(new_credit_list) != 0: Sf = np.mean(new_credit_list)
        else: Sf = 0
            
    else:
        mean = db.get_mean_by_id(customer_id)
        std = db.get_std_by_id(customer_id)
        
        z = (requested_budget - mean) / std
        Sf = 850 - 20 * np.exp(1.65 * z)
        
        if show: print(f'order more than 30 | mean: {mean}, std: {std}, z: {z}')
        Sf = min(max(Sf, 300), 850)
    
    if payment_stat == 'FULL':
        # P = requested_budget
        # if P > mean: A = 18 * (np.exp(0.0001 * (P - mean)) - 1)
        # A = 100 if A > 100 else A
        # Sf += A 
        Sf *= 1.5
        
    return max(min(Sf, 850), 300)

def cal_FICO_current(customer_id, payment_info, requested_budget, set_n= 100, show= False):
    print(customer_id, requested_budget)
    info = db.get_info_by_id(customer_id)
    Score = 0.35 * (payment_his := cal_payment_his(payment_info, credit_term= info['credit_terms'], show= show)) + 0.3 * (amount_owed := cal_amount_owed(payment_info, show= show)) + 0.2 * (credit_history_length := cal_credit_history_length(customer_id, show= show)) + 0.15 * (new_credit := cal_new_credit(customer_id, requested_budget, payment_stat= payment_info.stat, set_n= set_n, show= show))

    if show:
        print('>>>> Score:', Score)
        print('>> payment_his:', payment_his)
        print('>> amount_owed:', amount_owed)
        print('>> credit_his_len:', credit_history_length)
        # print('>> credit_mix:', credit_mix)
        print('>> new_credit:', new_credit)
        
    return int(min(max(Score, 300), 850)), {'payment_his': payment_his, 'amount_owed': amount_owed, 'credit_his_len': credit_history_length, 'credit_mix': None, 'new_credit': new_credit}

# Score retrieve -> 185
def cal_final_FICO_score(customer_id, cal_duration= 185, show= True):
    info = db.get_info_by_id(customer_id)
    orders = info['records']
    
    FICO = []
        
    for i, (order_id, order) in enumerate(orders.items()):
        today = datetime.now()
        order_date = datetime(order['order_date'][2], order['order_date'][1], order['order_date'][0])
        day_dif = today - order_date
        
        if show: print(i, order_id, day_dif, f'D: {cal_duration}',sep=' | ')
        if day_dif.days < cal_duration:
            FICO.append(order['local_credit_score'])
        else:
            break

    if len(FICO) == 0: 
        score = 300
    else:
        score = int(min(max(np.mean(FICO), 300), 850))
        
    if show: print(f'{customer_id}: [{len(FICO)}] -> {FICO} >>>>> {score} ', end='')
    return score
        
def update_FICO_score(customer_id, cal_duration= 185, score= None, score_info= None, show= False):
    if score is None:
        score = cal_final_FICO_score(customer_id, cal_duration, show)
    
    db.update_credit_score(customer_id, score)

def get_FICO_score(customer_id):
    try:
        score = db.get_info_by_id(customer_id)['credit_score']
        return score
    except:
        return 'User Does Not Exist'

# Data base manipulation
def add_new_order(customer_id, payment_info, show= False):
    ### Add record
    customer_info = db.get_info_by_id(customer_id)
    if customer_info is None:
        return None
        # credit_budget, credit_terms = cal_credit_values(customer_id, credit_score, True)
        # new_user = {
        #     'customer_id': customer_id,
        #     'type': customer_type,
        #     'credit_score': credit_score,
        #     'credit_budget': credit_budget,
        #     'credit_terms': credit_terms,
        #     'financial_info': fin_info_list,
        #     'record_summary': {'mean': None, 'std': None, 'n': 0 }, 
        #     'records': {}
        # }
        
        # db.add_new_user(new_user)
        # customer_info = db.get_info_by_id(customer_id)
    # payment_info.show()
    order = payment_info.PaymentInfo_to_JSON()
    # print('order:', order)
    
    credit_score, credit_score_info = cal_FICO_current(customer_id, payment_info, payment_info.amount, show= show)
    order['local_credit_score'] = credit_score
    order['local_credit_score_info'] = credit_score_info
    # print('credit score', credit_score)
    
    is_new_data = False
    prev_stat = ''
    if payment_info.ID in customer_info['records']:
        prev_stat = customer_info['records'][payment_info.ID]['stat']
        customer_info['records'][payment_info.ID] = order
    else:
        customer_info['records'] = {**{payment_info.ID: order}, **customer_info['records']}
        is_new_data = True
    # print(customer_info)
        
    ###  Update summary
    if payment_info.stat == 'FULL':
        # print('FULL', payment_info.ID in customer_info['records'])
        if not (not is_new_data and prev_stat == 'FULL'):
            if show: print('summary updated')
            data_list = []
            for local_order in customer_info['records'].values():
                if local_order['stat'] == 'FULL': data_list.append(local_order['amount'])
            
            customer_info['record_summary'] = {
                "mean": np.mean(data_list),
                "std": np.std(data_list),
                "n": len(data_list)
            }
      
    ### Save new record to database
    db.update_customer_info(customer_info)
    update_FICO_score(customer_id)
    customer_info = db.get_info_by_id(customer_id)
    
    ### Update credit budget & terms  
    print('update credit budget')        
    credit_budget, credit_terms, n_per_month = cal_credit_values(customer_id, show= True)
    customer_info['credit_budget']: credit_budget
    customer_info['credit_budget_per_month'] = budget_round(credit_budget * n_per_month)
    customer_info['credit_terms'] = credit_terms
    
    ### Record update time
    customer_info['last_update'] = str(datetime.now()).split('.')[0]
    
    ### Save data to database
    db.update_customer_info(customer_info)

def add_list_new_order(order_list, show= False):
    # for customer_id, order in order_list:
    sz = len(order_list) - 1
    for i in range(sz-1, 0, -1):
        customer_id, order = order_list[i]
        
        # if customer_id != '00001': return
        if show:
            print(f'\n{customer_id} -> {order.ID} ---------------------------------------- {sz-i}/{sz}')
        add_new_order(customer_id, order)

def request_new_budget(customer_id, requested_budget, cal_duration= 185, show= False):
    info = db.get_info_by_id(customer_id)
    if info is None:
        return 'ERROR: User Does Not Exist'
    
    new_credit = cal_new_credit(customer_id, requested_budget)
    print(new_credit)
    
    score = {'payment_his': [], 'amount_owed': [], 'credit_his_len': [], 'credit_mix': [], 'new_credit': []}
    for order_id, order in info['records'].items():
        today = datetime.now()
        order_date = datetime(order['order_date'][2], order['order_date'][1], order['order_date'][0])
        day_dif = today - order_date
        
        if show: print(order_id, day_dif, sep=' | ')
        if day_dif.days < cal_duration:
            score['payment_his'].append(order['local_credit_score_info']['payment_his'])
            score['amount_owed'].append(order['local_credit_score_info']['amount_owed'])
            score['credit_his_len'].append(order['local_credit_score_info']['credit_his_len'])
            # score['credit_mix'].append(order['local_credit_score_info']['credit_mix'])
            score['new_credit'].append(order['local_credit_score_info']['new_credit'])
        else:
            break
        
        
    if len(score['payment_his']) == 0:
        Score = 0.15 * new_credit + 0.9 * info['credit_score']
    else:
        Score = 0.35 * np.mean(score['payment_his']) + 0.3 * np.mean(score['amount_owed']) + 0.2 * np.mean(score['credit_his_len']) + 0.15 * new_credit

    return int(min(max(Score, 300), 850))

if __name__ == '__main__':
    customer_ID = '00005'
    
    #TS0002
    
    # test_customer = db.get_info_by_id(customer_ID)
    # P = PaymentInfo()
    # P.JSON_to_PaymentInfo(test_customer['records'][list(test_customer['records'].keys())[0]])
    # P.show()
    
    
    ### Calculation test
    # requested_budget = 10000
    # print('>>>>> FICO:', cal_FICO_current(customer_ID, P, requested_budget, show = True), '<<<<<')
    # print(f'Credit History: {cal_credit_history_length(customer_ID, True)}')

    
    ### Data retrival test
    # print('FICO Score:', cal_final_FICO_score(customer_ID, cal_duration=365, show= True))
    # update_FICO_score(customer_ID, cal_duration= 185, show= True)
    
    
    ### Add order
    # P = PaymentInfo()
    # P.ID = 'UND-675-2024-10-05 209811'
    # P.amount = 4620
    # P.stat = "FULL"
    # P.paid_date = datetime(2024, 9, 5)
    # P.order_date = datetime(2024, 8, 7)
    # add_new_order(customer_ID, P, show= True)
    
    
    ### Add multiple orders
    # path = r'D:\KMITL\KMITL\Year 03 - 01\Prompt Engineer\Work\08_08_2024_Project\Script\CreditScoreCalculationProgram\Script\testData\raw_data_for_third_test.xlsx'
    # doc = read_order_file(path)
    # payment_list = extract_order_info(doc)
    # add_list_new_order(payment_list, show= True)

    
    ### Request new budget
    requested_budget = 40000
    print(f'Credit Score for requested {requested_budget} is {request_new_budget(customer_ID, requested_budget, show = True)}')
    
    
    ### Check score
    print(f'FICO socre of {customer_ID} is {get_FICO_score(customer_ID)}')
    
    
    
    


    