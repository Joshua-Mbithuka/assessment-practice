import sys
import io
import pandas as pd

# Force UTF-8 so special characters print correctly on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ── Load Data ─────────────────────────────────────────────────────────────────

def load_data():
    file_path = r"C:\Users\JoshuaMutua\Downloads\bank_transactions\transactions.csv"
    df = pd.read_csv(file_path)
    return df


# ── Question 1: Total deposit amount per branch ───────────────────────────────

def deposits_per_branch(df):
    # Filter rows where transaction type is Deposit
    deposits_df = df[df["transaction_type"] == "Deposit"]

    # Step 1: Group the deposits data by branch
    grouped = deposits_df.groupby("branch")

    # Step 2: From each group, pick the amount column and add them up
    branch_totals = grouped["amount"].sum()

    # Step 3: Sort the totals from highest to lowest
    branch_totals = branch_totals.sort_values(ascending=False)

    return branch_totals


# ── Question 2: Customer with the highest net balance ─────────────────────────

def net_balance_per_customer(df):
    # Sum all deposits per customer
    total_deposits = df[df["transaction_type"] == "Deposit"].groupby("customer_name")["amount"].sum()

    # Sum all withdrawals per customer
    total_withdrawals = df[df["transaction_type"] == "Withdrawal"].groupby("customer_name")["amount"].sum()

    # Combine into one table, fill 0 where a customer has no deposits or withdrawals
    summary = pd.DataFrame({
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals
    }).fillna(0)

    # Calculate net balance
    summary["net_balance"] = summary["total_deposits"] - summary["total_withdrawals"]

    # Sort by net balance highest to lowest
    summary = summary.sort_values("net_balance", ascending=False)

    return summary


# ── Question 3: Number of transactions per account type ──────────────────────

def transactions_per_account_type(df):
    # Group by account type and count the number of transactions
    counts = df.groupby("account_type")["transaction_id"].count()
    return counts


# ── Main: Run all functions and print results ─────────────────────────────────

def main():
    df = load_data()
    print(f"Data loaded successfully. Here is a preview:\n{df}\n")

    print(f"1. Total Deposit Amount per Branch:\n{deposits_per_branch(df)}\n")

    net_balances = net_balance_per_customer(df)
    print(f"2. Customer Net Balances:\n{net_balances}\nCustomer with highest net balance: {net_balances['net_balance'].idxmax()}\n")

    print(f"3. Number of Transactions per Account Type:\n{transactions_per_account_type(df)}")


main()
