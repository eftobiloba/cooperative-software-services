from pymongo import MongoClient
import certifi
from config.config import MONGODB_URI

ca = certifi.where()

client = MongoClient(MONGODB_URI, tls=True, tlsCAFile=ca)

db = client.society_db

society_collection = db["society_collection"]
not_member_collection = db["not_member_collection"]
member_collection = db["member_collection"]
saving_products_collection = db["saving_products_collection"]
loan_products_collection = db["loan_products"]
savings_transactions_collection = db["savings_transactions_collection"]
loan_transaction_collection = db["loan_transaction_collection"]
admin_collection = db["admin_collection"]
balance_collection = db["balance_collection"]
repayments_collection = db["repayments_collection"]
forms_collection = db["forms_collection"]
form_submissions_collection = db["form_submissions_collection"]
actions_collection = db["actions_collection"]
dev_collection = db["dev_collection"]

member_collection.create_index('membership_no', unique=True)
society_collection.create_index('society_id', unique=True)
savings_transactions_collection.create_index('trans_ref', unique=True)
loan_transaction_collection.create_index('trans_ref', unique=True)