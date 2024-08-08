from models.savings import *
from models.loans import *
from models.repayments import *

def savings_transaction_serial(transaction: SavingsTransaction) -> dict:
    return {
        "membership_no": transaction.membership_no,
        "email": transaction.email,
        "transref": transaction.transref,
        "product_id": transaction.product_id,
        "society_id": transaction.society_id,
        "timestamp": transaction.timestamp.isoformat(),
        "description": transaction.description,
        "type": transaction.type,
        "amount": transaction.amount,
        "status": transaction.status,
        "formonth": transaction.formonth
    }

def list_savings_transaction_serial(transactions: list) -> list:
    return [savings_transaction_serial(transaction) for transaction in transactions]

def savings_product_serial(product: SavingsProduct) -> dict:
    return {
        "product_id": product.product_id,
        "product_name": product.product_name,
        "description": product.description,
        "society_id": product.society_id,
        "minimum_saveable": product.minimum_saveable,
        "minimum_untouchable": product.minimum_untouchable,
        "interest_return": product.interest_return,
        "required_info": product.required_info
    }

def list_savings_product_serial(products: list) -> list:
    return [savings_product_serial(product) for product in products]

def savings_balance_serial(balance: SavingsBalance) -> dict:
    return {
        "membership_no": balance.membership_no,
        "product_id": balance.product_id,
        "balance": balance.balance
    }

def list_savings_balance_serial(balances: list) -> list:
    return [savings_balance_serial(balance) for balance in balances]


# --------------------- LOANS ----------------------
def loan_transaction_serial(transaction: LoanTransaction) -> dict:
    return {
        "membership_no": transaction.membership_no if transaction.membership_no else None,
        "non_member_id": transaction.non_member_id if transaction.non_member_id else None,
        "email": transaction.email,
        "transref": transaction.transref,
        "product_id": transaction.product_id,
        "society_id": transaction.society_id,
        "timestamp": transaction.timestamp.isoformat(),
        "calculation_method": transaction.calculation_method,
        "loantype": transaction.loantype,
        "interest": transaction.interest,
        "amount": transaction.amount,
        "period": transaction.period,
        "status": transaction.status,
        "completed": transaction.completed,
        "date_approved": transaction.date_approved.isoformat()
    }

def list_loan_transaction_serial(transactions: list) -> list:
    return [loan_transaction_serial(transaction) for transaction in transactions]

def loan_product_serial(product: LoanProduct) -> dict:
    return {
        "product_id": product.product_id,
        "product_name": product.product_name,
        "description": product.description,
        "society_id": product.society_id,
        "interest": product.interest,
        "form_id": product.form_id if product.form_id else None,
        "calculation_method": product.calculation_method
    }

def list_loan_product_serial(products: list) -> list:
    return [loan_product_serial(product) for product in products]


# -------------------------- Savings Balance -------------------------------
def savings_balance_serial(savings_balance: SavingsBalance) -> dict:
    return {
        "id": str(savings_balance["_id"]),
        "membership_no": savings_balance["membership_no"],
        "society_id": savings_balance["society_id"],
        "product_id": savings_balance["product_id"],
        "balance": savings_balance["balance"]
    }

def list_savings_balance_serial(savings_balances) -> list:
    return [savings_balance_serial(savings_balance) for savings_balance in savings_balances]


#---------------------------- Repayments -----------------------------------
def repayments_serial(repayment: Repayment) -> dict:
    return {
        "loan_transaction_id": repayment.loan_transaction_id,
        "amount": repayment.amount,
        "date": repayment.date
    }