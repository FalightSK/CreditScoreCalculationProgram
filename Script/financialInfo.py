import copy

class FinancialInfo():
    def __init__(self):
        self.total_assets = None
        self.current_assets = None
        self.total_liabilities = None
        self.total_revenue = None
        self.shareholder_equity = None
    
    def show(self):
        print(f'total assets: {self.total_assets}\ntotal current assets: {self.current_assets}\ntotal liabilities: {self.total_liabilities}\ntoal revenue: {self.total_revenue}\nshareholder equity: {self.shareholder_equity}')
    
    def copy(self):
        return copy.copy(self)
# class CumulativeInfo():
#     def    