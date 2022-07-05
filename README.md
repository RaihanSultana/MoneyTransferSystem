# MoneyTransferSystem
A person can send money from their account to one or many user's account now or in a scheduled time.


Requirements: Celery, Redis(in order to reun celery)
Steps:
1. pip install -r requirements.txt - This will install all the required packages that are required to run the project
2. After installing the packages, and migrating, Create test users using registration api : '127.0.0.0:800/api/register/'
3. Login using : '127.0.0.0:800/api/login/'. This is necessary as only authenticated user can send money and view transaction history.
4. Send money api: 127.0.0.0:800/api/send_money/ [User must be authenticated]

    In order to request this api, the following parameters must be given. 
    
    amount:int, to_account_id:list(example: ["3", "4"]), time:%Y-%m-%d %H:%M:%S(example: 2022-07-05 12:42:00), set_time: boolean(example: true)
    
    json_parameters_sample: {
                            "amount": "10.00",
                            "to_account_id": ["3", "4"],
                            "time": "2022-07-05 12:42:00",
                            "set_time": true   
                        }
                        
      set_time: If set_time is true, That means  time is schedulled. It will then check time and run task to send money on the scheduled time.
                If set_time is false, then it will check if sender has sufficient amount in account, if yes, it will send money now. 
       
      to_account_id: This should be a list. So user can send to one or more user money at the same time. However separate transaction object will be created fr each            transaction.
      
5. transaction history api: 127.0.0.0:800/api/transaction_history/ [User must be authenticated]
    Returns list of transaction for authenticated user
       
                    