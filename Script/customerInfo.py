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
            'total_asstotal_liabilitiesets': self.total_liabilities,
            'total_revenue': self.total_revenue,
            'shareholder_equity': self.shareholder_equity
        }
        return JSON
    
    def copy(self):
        return copy.copy(self)
        
class PaymentInfo():
    method_list = ['CASH', 'IN_STORE', 'OTHERS', 'CREDIT_CARD']
    stat_list = ['FULL', 'PARTIAL', 'OVERDUE']
    
    def __inti__(self):
        self.stat = None
        self.order_date = None
        self.paid_date = None
        self.amount = None
        self.method = None
        
    def JSON_to_PaymentInfo(self, JSON):
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
            'stat': self.stat,
            'amount': self.amount,
            'method': self.method,
            'order_date': [self.order_date.day, self.order_date.month, self.order_date.year],
            'paid_date': [self.paid_date.day, self.paid_date.month, self.paid_date.year]
        }
        
        return JSON
        
    
    def show(self):
        print(f'stat: {self.stat}\norder date: {self.order_date}\npaid_date: {self.paid_date}\namount: {self.amount}\nmethod: {self.method}')


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


# Data Structure
order = {
    'ID': None,
    'order_date': None,
    'amount': None,
    'stat': None,
    'paid_date': None,
    'method': None
}

user = {
    'customer_id': None,
    'type': None,
    'credit_score': None,
    'credit_budget': None,
    'credit_terms': None,
    'financial_info': {
        'total_assets': None,
        'current_assets': None,
        'total_liabilities': None,
        'total_revenue': None,
        'shareholder_equity': None
    },
    'record_summary': {
        'mean': None,
        'std': None,
        'n': None
    }, 
    'records': [order]
}

summary = {
    'type': {
        'mean': None,
        'std': None
    }
}


        