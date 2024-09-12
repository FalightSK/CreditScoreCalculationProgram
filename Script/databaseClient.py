import json
import os

Dir = os.getcwd()
path = 'Script/database.txt'
path = os.path.join(Dir, path)

# JSON utilities
def save(json_file, path= path):
    with open(path, 'w') as file:
        json.dump(json_file, file)
    print('save success')
    
def read(path= path):
    with open(path, 'r') as file:
        data = json.load(file)
        return data
    
# Get general infomation
def get_criteria_credit_history(shop_type):
    return read()['credit_history_criteria'][shop_type]
    
    

# Get customer infomation by ID
def get_std_by_id(customer_id):
    return read()['history'][customer_id]['record_summary']['std']

def get_mean_by_id(customer_id):
    return read()['history'][customer_id]['record_summary']['mean']

def get_number_of_order_by_id(customer_id):
    return read()['history'][customer_id]['record_summary']['n']

def get_info_by_id(customer_id):
    return read()['history'][customer_id]


if __name__ == '__main__':
    print(get_mean_by_id('00001'))