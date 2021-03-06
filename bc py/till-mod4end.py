mining_reward = 10
genesis_block = {'previous_hash': '','index' : 0, 'transactions': [] }
blockchain= [genesis_block]
open_transactions =[]
owner = 'Harkirat'
participants = {'Harkirat'}

def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx)>0:
            amount_sent += tx[0]
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = 0
    for tx in tx_recipient:
        if len(tx)>0:
            amount_recieved += tx[0]
    return amount_recieved - amount_sent

def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None 
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']
       

def add_transaction(recipient, sender= owner, amount=1.0):
    transaction = {'sender':sender, 'recipient':recipient, 'amount': amount}
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False
    

def mine_block():
    last_block= blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'Mining',
        'recipient': owner,
        'amount': mining_reward
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {'previous_hash': hashed_block,'index' : len(blockchain), 'transactions': copied_transactions }
    blockchain.append(block)
    return True    

def get_transaction_value():
    tx_recipient= input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your Transaction amount please : '))
    return tx_recipient, tx_amount

def get_user_choice():
    return input('Your Choice: ')


def print_blockchain_elements():
    for block in blockchain:
        print ('Outputting Block')
        print (block)
    else:
        print('-'*20)

def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash']!= hash_block(blockchain[index-1]):
            return False
    return True
waiting_for_input = True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])
# something is wrong

while waiting_for_input:
    print ('Please Choose')
    print ('1: Add a new transaction value')
    print ('2: Mine a new block')
    print ('3: Output the blockchain blocks')
    print ('4: Output Participants')
    print ('5: Check Transaction Validity')
    print ('H: Manipulate the chain')
    print ('Q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1' :
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Added transaction')
        else:
            print('Transaction Failed')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
           open_transactions = [] 
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print ('All transaction are valid')
        else:
            print ('There are invalid transactions')
    elif user_choice == 'H':
        if len(blockchain) >= 1:
            blockchain [0] = { 'transaction': 100}
    elif user_choice == 'Q':
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid Blockchain')
        break
    print (get_balance('Harkirat'))
else:
    print ('User left')
print ('done')