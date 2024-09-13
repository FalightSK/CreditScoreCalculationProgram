import copy
import datetime
import pandas as pd
#181146

# Data Classes
class FinancialInfo():
    def __init__(self):
        self.total_assets = None
        self.current_assets = None
        self.total_liabilities = None
        self.total_revenue = None
        self.shareholder_equity = None
    
    def show(self):
        print(f'total assets: {self.total_assets}\ntotal current assets: {self.current_assets}\ntotal liabilities: {self.total_liabilities}\ntoal revenue: {self.total_revenue}\nshareholder equity: {self.shareholder_equity}')
    
    def JSON_to_FinancialInfo(self, JSON):
        self.total_assets = JSON['total_assets']
        self.current_assets = JSON['current_assets']
        self.total_liabilities = JSON['total_liabilities']
        self.total_revenue = JSON['total_revenue']
        self.shareholder_equity = JSON['shareholder_equity']
        
    def FinancialInfo_to_JSON(self):
        JSON = {
            'total_assets': self.total_assets,
            'current_assets': self.current_assets,
            'total_liabilities': self.total_liabilities,
            'total_revenue': self.total_revenue,
            'shareholder_equity': self.shareholder_equity
        }
        return JSON
    
    def copy(self):
        return copy.copy(self)
        
class PaymentInfo():
    method_list = ['CASH', 'IN_STORE', 'OTHERS', 'CREDIT_CARD']
    stat_list = ['FULL', 'PARTIAL', 'OVERDUE']
    
    def __init__(self):
        self.ID = None
        self.stat = None
        self.order_date = None
        self.paid_date = None
        self.amount = None
        self.method = None
        
    def JSON_to_PaymentInfo(self, JSON):
        self.ID = JSON['ID']
        self.stat = JSON['stat']
        self.amount = JSON['amount']
        self.method = JSON['method']
        
        date01 = JSON['order_date']
        self.order_date = datetime.datetime(date01[2], date01[1], date01[0])
        
        date02 = JSON['paid_date']
        if date02 is None:
            self.paid_date = None
        else:
            self.paid_date = datetime.datetime(date02[2], date02[1], date02[0])
        
    def PaymentInfo_to_JSON(self):
        JSON = {
            'ID': self.ID,
            'order_date': [self.order_date.day, self.order_date.month, self.order_date.year],
            'amount': self.amount,
            'stat': self.stat,
            'paid_date': None,
            'method': self.method,
            'local_credit_score': None
        }
        
        if self.paid_date is not None:
            JSON['paid_date'] = [self.paid_date.day, self.paid_date.month, self.paid_date.year]
        
        return JSON
        
    def show(self):
        print(f'>> {self.ID}:\nstat: {self.stat}\norder date: {self.order_date}\npaid_date: {self.paid_date}\namount: {self.amount}\nmethod: {self.method}')
        
    def copy(self):
        return copy.copy(self)


# Util Functions 
def read_financial_file(path):
    doc = pd.read_excel(path, header= 2)
    return doc

def extract_fin_info(doc_position, doc_income):
    
    # an empty list to contain financial info throughout the years
    fin_info = []
    
    col = doc_position.columns
    for i in range(2, len(col), 2):
        local_fin_info = FinancialInfo()
        
        try:
            local_fin_info.total_assets = float(str(doc_position[col[i]][6]).replace(',', ''))
            local_fin_info.current_assets = float(str(doc_position[col[i]][3]).replace(',', ''))
            local_fin_info.total_liabilities = float(str(doc_position[col[i]][9]).replace(',', ''))
            local_fin_info.shareholder_equity = float(str(doc_position[col[i]][10]).replace(',', ''))
            
            local_fin_info.total_revenue = float(str(doc_income[col[i]][2]).replace(',', ''))
            
            # print('\n')
            # local_fin_info.show()
            fin_info.append(local_fin_info.copy())
        
        except:
            print('found NONE value')
        
        
    return fin_info

def read_order_file(path):
    doc = pd.read_excel(path, header= 1)
    doc.fillna('UNKNOWN', inplace= True)
    return doc

def extract_order_info(doc):
    payment_list = []
    
    prev_order_id = ''
    for order in doc.iloc():
        order_id = order['รายการ']
        if prev_order_id == order_id or order['สถานะรายการ'] != 'สำเร็จ' or order['มูลค่า'] in [0, 'UNKNOWN']:
            continue
        
        
        prev_order_id = order_id
            
        local_payment = PaymentInfo()
        local_payment.ID = order_id
        local_payment.amount = order['มูลค่า']
        order_date = [int(j) for j in order['วันที่ทำรายการ'].split('/')]
        local_payment.order_date = datetime.datetime(order_date[2], order_date[1], order_date[0])
        
        try:
            paid_date = [int(j) for j in order['วันที่ชำระเงิน'].split()[0].split('/')]
            local_payment.paid_date = datetime.datetime(paid_date[2], paid_date[1], paid_date[0])
        except:
            local_payment.paid_date = None
        
        local_stat = order['สถานะการชำระเงิน']
        if local_stat == 'ชำระครบ':
            local_stat = 'FULL'
        elif local_stat == 'ชำระบางส่วน':
            local_stat = 'PARTIAL'
        elif local_stat == 'รอการชำระเงิน':
            local_stat = 'OVERDUE'
        else:
            continue
        local_payment.stat = local_stat
        
        local_method = order['ช่องทางการชำระเงิน'] 
        local_payment.method = 'CASH' if local_method == 'เงินสด' else 'IN_STORE' if local_method == 'หน้าร้าน' else 'CREDIT_CARD' if local_method == "รอตัด" or local_method == "เครื่องรูดบัตร" else 'OTHERS'
        
        payment_list.append((order['รหัสลูกค้า'], local_payment.copy()))
          
    return payment_list


# Data Structure
order = {
    'ID': None,
    'order_date': None,
    'amount': None,
    'stat': None,
    'paid_date': None,
    'method': None,
    'local_credit_score': None,
    'local_credit_score_info': None
}

user = {
    'customer_id': None,
    'type': None,
    'credit_score': None,
    'credit_budget': 17000,
    'credit_terms': 15,
    'financial_info': [{
        'total_assets': None,
        'current_assets': None,
        'total_liabilities': None,
        'total_revenue': None,
        'shareholder_equity': None
    }],
    'record_summary': {
        'mean': None,
        'std': None,
        'n': None
    }, 
    'records': order
}

summary = {
    'type': {
        'mean': None,
        'std': None
    }
}


        