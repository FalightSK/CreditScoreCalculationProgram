import json
import os

Dir = os.getcwd()
path = 'Script\\database.json'
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
    n = read()['history'][customer_id]['record_summary']['n']
    n = n if n is not None else 0
    return n

def get_info_by_id(customer_id):
    data = read()['history']
    if customer_id not in data: return None
    else: return data[customer_id]



# Update database
def update_credit_score(customer_id, score):
    database = read()
    database['history'][customer_id]['credit_score'] = score
    save(database)

def add_new_user(customer_info):
    database = read()
    
    if customer_info['customer_id'] in database['history']: print(f'ERROR: user {customer_info["customer_id"]} already existed')
    else: update_customer_info(customer_info)

def update_customer_info(customer_info):
    database = read()
    database['history'][customer_info['customer_id']] = customer_info
    save(database)
    

if __name__ == '__main__':
    pass
    # save({'test': 'helloworld!!!'})
    # print(get_mean_by_id('00001'))
    
    # with open('Script/database.json', 'w') as file:
    #     json_file = {
    #         'micket': 1,
    #         'test': {
    #             'local': 1,
    #             'not local': 2}
    #         }
    #     json.dump(json_file, file)
        
        
    # with open('Script\database.json', 'r') as file:
    #     local_file = json.load(file)
    #     print(local_file['test'])
    # print('save success')