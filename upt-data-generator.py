import os
import random
import csv
import shutil
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(20260903)
np.random.seed(20260903)

# Create output directories
os.makedirs("/workspace/scratch/mock_data", exist_ok=True)

# 1. GENERATE EMPLOYER GROUPS (EGP)
# Fictional representation of Employer Group Profile (EGP)
group_data = [
    {
        "Group_ID": 101,
        "Group_Name": "Maple Valley School District",
        "Sponsor_Number": 33,
        "Location_Number": "0001",
        "Funding_Type": "Fully-Insured",
        "COBRA_Admin_Flag": "UPT-Admin",
        "Bank_Routing_Number": "031000053",
        "Bank_Name": "Trust National Bank",
        "Lines_Of_Business": "Dental,Vision,Prescription"
    },
    {
        "Group_ID": 102,
        "Group_Name": "Pine Creek Township",
        "Sponsor_Number": 33,
        "Location_Number": "0002",
        "Funding_Type": "Fully-Insured",
        "COBRA_Admin_Flag": "UPT-Admin",
        "Bank_Routing_Number": "031000503",
        "Bank_Name": "Keystone Federal",
        "Lines_Of_Business": "Dental,Vision"
    },
    {
        "Group_ID": 103,
        "Group_Name": "Oakridge Transit Authority",
        "Sponsor_Number": 35,
        "Location_Number": "0001",
        "Funding_Type": "Fully-Insured",
        "COBRA_Admin_Flag": "Group-Admin",
        "Bank_Routing_Number": "031201509",
        "Bank_Name": "Fidelity Union Bank",
        "Lines_Of_Business": "Dental,Vision,Prescription"
    },
    {
        "Group_ID": 104,
        "Group_Name": "River Valley School District",
        "Sponsor_Number": 103,
        "Location_Number": "0001",
        "Funding_Type": "Fully-Insured",
        "COBRA_Admin_Flag": "UPT-Admin",
        "Bank_Routing_Number": "031100121",
        "Bank_Name": "Pinnacle Bank",
        "Lines_Of_Business": "Vision"
    },
    {
        "Group_ID": 105,
        "Group_Name": "Blue Ridge Transit Consortium",
        "Sponsor_Number": 50,
        "Location_Number": "0001",
        "Funding_Type": "Self-Funded",
        "COBRA_Admin_Flag": "Group-Admin",
        "Bank_Routing_Number": "031302804",
        "Bank_Name": "Summit Bank",
        "Lines_Of_Business": "Dental,Vision"
    },
    {
        "Group_ID": 106,
        "Group_Name": "Summit Municipal Water",
        "Sponsor_Number": 60,
        "Location_Number": "0001",
        "Funding_Type": "Self-Billed",
        "COBRA_Admin_Flag": "Group-Admin",
        "Bank_Routing_Number": "031000011",
        "Bank_Name": "Metro Commerce Bank",
        "Lines_Of_Business": "Dental"
    },
    {
        "Group_ID": 107,
        "Group_Name": "Valley View Public Library",
        "Sponsor_Number": 33,
        "Location_Number": "0003",
        "Funding_Type": "Fully-Insured",
        "COBRA_Admin_Flag": "UPT-Admin",
        "Bank_Routing_Number": "031200155",
        "Bank_Name": "Citizens Trust",
        "Lines_Of_Business": "Dental,Vision"
    }
]

df_egp = pd.DataFrame(group_data)
df_egp.to_csv("/workspace/scratch/mock_data/employer-groups.csv", index=False)

# Fictionalized Name generation pools
first_names_m = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"]
first_names_f = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson", 
              "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White"]

# 2. GENERATE BENEFIT SUBSCRIBERS (BSE)
subscribers = []
sub_id_counter = 10001

for group in group_data:
    g_id = group["Group_ID"]
    g_type = group["Funding_Type"]
    
    # Valley View Library is small (10 subs); others have 20-30 subs
    num_subs = 12 if g_id == 107 else random.randint(20, 35)
    
    for i in range(num_subs):
        gender = random.choice(["M", "F"])
        first_name = random.choice(first_names_m if gender == "M" else first_names_f)
        last_name = random.choice(last_names)
        
        # 10% COBRA probability
        is_cobra = "N"
        cobra_type = ""
        elig_end_date = ""
        elig_start_date = ""
        
        if random.random() < 0.10:
            is_cobra = "Y"
            cobra_type = random.choice(["Employee", "Spouse", "Dependent"])
            elig_start_date = (datetime(2026, 1, 1) + timedelta(days=random.randint(1, 150))).strftime("%Y-%m-%d")
            elig_end_date = (datetime.strptime(elig_start_date, "%Y-%m-%d") + timedelta(days=540)).strftime("%Y-%m-%d")
            
        status = "Active"
        # Valley View library has 2 terminated members to show delinquency termination
        if g_id == 107 and i < 2:
            status = "Terminated"
            
        ssn = f"999-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
        dob = (datetime(1960, 1, 1) + timedelta(days=random.randint(0, 15000))).strftime("%Y-%m-%d")
        effective_date = (datetime(2020, 1, 1) + timedelta(days=random.randint(1, 1500))).strftime("%Y-%m-%d")
        
        # Paid through to date
        if g_id == 107:
            # Valley View library is delinquent, paid up to June 30, 2026
            paid_to_date = "2026-06-30"
        else:
            paid_to_date = "2026-09-30"
            
        subscribers.append({
            "Subscriber_ID": sub_id_counter,
            "Group_ID": g_id,
            "Last_Name": last_name,
            "First_Name": first_name,
            "Fake_SSN": ssn,
            "Date_of_Birth": dob,
            "Status": status,
            "Is_COBRA": is_cobra,
            "COBRA_Sub_Type": cobra_type,
            "COBRA_Elig_Date": elig_start_date,
            "COBRA_Elig_End_Date": elig_end_date,
            "Paid_To_Date": paid_to_date,
            "Coverage_Effective_Date": effective_date,
            "Gender": gender
        })
        sub_id_counter += 1

df_bse = pd.DataFrame(subscribers)
df_bse.to_csv("/workspace/scratch/mock_data/benefit-subscribers.csv", index=False)


# 3. GENERATE DEPENDENTS (SDR)
dependents = []
dep_id_counter = 50001

for sub in subscribers:
    sub_id = sub["Subscriber_ID"]
    sub_dob = datetime.strptime(sub["Date_of_Birth"], "%Y-%m-%d")
    sub_age = (datetime(2026, 9, 3) - sub_dob).days // 365
    
    # Subscribers over age 28 have a chance of dependents
    if sub_age > 28:
        # 1. Spouse probability (60%)
        if random.random() < 0.60:
            spouse_gender = "F" if sub["Gender"] == "M" else "M"
            spouse_first = random.choice(first_names_f if spouse_gender == "F" else first_names_m)
            spouse_last = sub["Last_Name"]
            spouse_dob = (sub_dob + timedelta(days=random.randint(-1500, 1500))).strftime("%Y-%m-%d")
            
            # Same-sex spouse check (5% chance)
            relationship = "Spouse"
            if random.random() < 0.05:
                spouse_gender = sub["Gender"]
                relationship = "Same-Sex Spouse"
                
            dependents.append({
                "Dependent_ID": dep_id_counter,
                "Subscriber_ID": sub_id,
                "Relationship": relationship,
                "Last_Name": spouse_last,
                "First_Name": spouse_first,
                "Date_of_Birth": spouse_dob,
                "Student_Cert_Expiry": "",
                "Is_Eligible": "Y"
            })
            dep_id_counter += 1
            
        # 2. Children probability (70%)
        if random.random() < 0.70:
            num_children = random.randint(1, 3)
            for c in range(num_children):
                child_gender = random.choice(["M", "F"])
                child_first = random.choice(first_names_m if child_gender == "M" else first_names_f)
                child_last = sub["Last_Name"]
                
                # Dynamic child age relative to parent (sub)
                child_age = random.randint(1, min(26, sub_age - 18))
                child_dob_dt = datetime(2026, 9, 3) - timedelta(days=child_age * 365 + random.randint(1, 300))
                child_dob = child_dob_dt.strftime("%Y-%m-%d")
                
                relationship = "Child"
                student_cert_expiry = ""
                is_eligible = "Y"
                
                # Check for Full-Time Higher Education Student Cert rules (Age 19 - 25)
                if 19 <= child_age < 26:
                    relationship = "FT Student"
                    # 10% chance of expired or missing cert -> ineligible
                    if random.random() < 0.10:
                        student_cert_expiry = (datetime(2026, 6, 30)).strftime("%Y-%m-%d")
                        is_eligible = "N"
                    else:
                        student_cert_expiry = (datetime(2027, 6, 30)).strftime("%Y-%m-%d")
                elif child_age >= 26:
                    # Ineligible by age unless disabled
                    if random.random() < 0.05:
                        relationship = "Disabled Dependent"
                    else:
                        is_eligible = "N"
                        
                dependents.append({
                    "Dependent_ID": dep_id_counter,
                    "Subscriber_ID": sub_id,
                    "Relationship": relationship,
                    "Last_Name": child_last,
                    "First_Name": child_first,
                    "Date_of_Birth": child_dob,
                    "Student_Cert_Expiry": student_cert_expiry,
                    "Is_Eligible": is_eligible
                })
                dep_id_counter += 1

df_sdr = pd.DataFrame(dependents)
df_sdr.to_csv("/workspace/scratch/mock_data/subscriber-dependents.csv", index=False)


# 4. RULES ENGINE FOR BILLING TIER CALCULATION
# Helper function to dynamically map tier based on active dependents
def calculate_billing_tier(sub_row, dep_rows):
    if len(dep_rows) == 0:
        return 3, "Single Coverage"  # Single
        
    has_spouse = any(d["Relationship"] in ["Spouse", "Same-Sex Spouse"] and d["Is_Eligible"] == "Y" for d in dep_rows)
    active_child_count = sum(1 for d in dep_rows if d["Relationship"] in ["Child", "FT Student", "Disabled Dependent"] and d["Is_Eligible"] == "Y")
    
    if not has_spouse:
        if active_child_count == 0:
            return 3, "Single Coverage"
        elif active_child_count == 1:
            return 4, "Single w/ 1 Dependent"
        else:
            return 1, "Family Coverage"
    else:
        if active_child_count == 0:
            return 2, "Member & Spouse"
        else:
            return 1, "Family Coverage"

# Map calculated tiers back into subscriber dataset
sub_tiers = []
for idx, sub in df_bse.iterrows():
    sub_id = sub["Subscriber_ID"]
    sub_deps = df_sdr[df_sdr["Subscriber_ID"] == sub_id].to_dict("records")
    tier_code, tier_label = calculate_billing_tier(sub, sub_deps)
    sub_tiers.append({"Subscriber_ID": sub_id, "Billing_Tier_Code": tier_code, "Billing_Tier_Label": tier_label})

df_tiers = pd.DataFrame(sub_tiers)
df_bse = df_bse.merge(df_tiers, on="Subscriber_ID")
# Re-save updated subscriber directory containing dynamic billing tier assignments
df_bse.to_csv("/workspace/scratch/mock_data/benefit-subscribers.csv", index=False)


# 5. GENERATE GROUP PREMIUM RECEIPTS LEDGER (GPRR)
# Generate monthly ledger records for the past 12 billing periods (Oct 2025 - Sep 2026)
billing_periods = [
    "2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", 
    "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"
]

# Set rates for fully-insured lines of business
TIER_RATES = {
    "Dental": {1: 120.00, 2: 90.00, 3: 45.00, 4: 75.00},
    "Vision": {1: 40.00, 2: 30.00, 3: 15.00, 4: 25.00},
    "Prescription": {1: 400.00, 2: 300.00, 3: 150.00, 4: 250.00}
}

ledger_rows = []
ledger_id_counter = 200001

for period in billing_periods:
    year_str, month_str = period.split("-")
    
    for group in group_data:
        g_id = group["Group_ID"]
        g_funding = group["Funding_Type"]
        g_lobs = group["Lines_Of_Business"].split(",")
        
        # Get active subscribers for this group in this period
        gp_subs = df_bse[(df_bse["Group_ID"] == g_id) & (df_bse["Status"] == "Active")]
        headcount = len(gp_subs)
        
        for lob in g_lobs:
            calc_premium = 0.00
            
            # Calculate premium based on funding type
            if g_funding == "Fully-Insured" or g_funding == "Self-Billed":
                # Aggregate counts per tier
                for idx, sub in gp_subs.iterrows():
                    tier = sub["Billing_Tier_Code"]
                    rate = TIER_RATES[lob][tier]
                    calc_premium += rate
            elif g_funding == "Self-Funded":
                # Self-Funded (ASO): Claims Expense + Admin Fee (headcount * contracted rate)
                # Contracted admin rate is $5.50 for Dental, $2.50 for Vision
                admin_rate = 5.50 if lob == "Dental" else 2.50
                claims_expense = float(np.random.normal(5000, 1200)) # random claims variance
                claims_expense = max(1500, claims_expense) # non-negative limit
                admin_fee = headcount * admin_rate
                calc_premium = claims_expense + admin_fee
            
            # Default payment behavior
            premium_paid = calc_premium
            balance_due = 0.00
            deposit_date = f"{period}-15"
            status = "Fully Paid"
            
            # Scenario deviations for delinquency & aging reporting demo:
            if g_id == 107: # Valley View Public Library (Delinquent)
                if period in ["2026-07", "2026-08", "2026-09"]:
                    # Paid 0.00 for past 3 months
                    premium_paid = 0.00
                    balance_due = calc_premium
                    deposit_date = ""
                    status = "Delinquent"
            elif g_id == 103 and period == "2026-08": # Oakridge Transit (Underpaid Balance due)
                premium_paid = round(calc_premium * 0.90, 2)
                balance_due = round(calc_premium - premium_paid, 2)
                deposit_date = "2026-08-20"
                status = "Underpaid"
            elif g_id == 102 and period == "2026-09": # Pine Creek (Paid in Advance)
                premium_paid = calc_premium
                balance_due = 0.00
                deposit_date = "2026-08-28" # Paid prior month
                status = "Advance"
                
            ledger_rows.append({
                "Ledger_ID": ledger_id_counter,
                "Group_ID": g_id,
                "Group_Name": group["Group_Name"],
                "Billing_Period": period,
                "Line_of_Business": lob,
                "Calculated_Premium": round(calc_premium, 2),
                "Premium_Paid": round(premium_paid, 2),
                "Deposit_Date": deposit_date,
                "Balance_Due": round(balance_due, 2),
                "Reconciliation_Status": status
            })
            ledger_id_counter += 1

df_gprr = pd.DataFrame(ledger_rows)
df_gprr.to_csv("/workspace/scratch/mock_data/group-premium-ledger.csv", index=False)


# 6. GENERATE ACH BANK STATEMENT UPLOAD (ACH)
# Represent bank output containing matched transactions and messy text strings
ach_records = []
ach_id_counter = 800001

# Filter Aug-Sep 2026 ledger items to reconcile via bank statement
recent_ledger = df_gprr[df_gprr["Billing_Period"].isin(["2026-08", "2026-09"])]

for idx, row in recent_ledger.iterrows():
    if row["Premium_Paid"] == 0:
        continue  # skip delinquent items with no deposits
        
    g_id = row["Group_ID"]
    g_profile = next(item for item in group_data if item["Group_ID"] == g_id)
    
    # 1. Rank 1: Exact matches for PSEA-initiated groups (Sponsor 33, 35)
    if g_profile["Sponsor_Number"] in [33, 35] and row["Reconciliation_Status"] == "Fully Paid":
        depositor_string = f"UPT-BATCH-{g_profile['Sponsor_Number']}-{g_profile['Location_Number']}"
        ach_records.append({
            "Transaction_ID": ach_id_counter,
            "Deposit_Date": row["Deposit_Date"],
            "Amount": row["Premium_Paid"],
            "ACH_Transit_Route_No": g_profile["Bank_Routing_Number"],
            "ACH_Originating_Bank": g_profile["Bank_Name"],
            "Depositor_Name_String": depositor_string,
            "Reconciliation_Rank_Match": "Rank 1 (Route & Amount Match)"
        })
        ach_id_counter += 1
        
    # 2. Rank 2: Exact matches for self-initiated or underpaid items using bank name
    elif row["Reconciliation_Status"] in ["Underpaid", "Fully Paid", "Advance"]:
        # Messy depositor string
        abbrev_name = "".join([w[0:4].upper() for w in g_profile["Group_Name"].split()])
        depositor_string = f"{abbrev_name} ACH DISB PMT"
        
        ach_records.append({
            "Transaction_ID": ach_id_counter,
            "Deposit_Date": row["Deposit_Date"],
            "Amount": row["Premium_Paid"],
            "ACH_Transit_Route_No": g_profile["Bank_Routing_Number"],
            "ACH_Originating_Bank": g_profile["Bank_Name"],
            "Depositor_Name_String": depositor_string,
            "Reconciliation_Rank_Match": "Rank 2 (Bank Name & Amount Match)"
        })
        ach_id_counter += 1

# 3. Add Rank 3: Messy COBRA individual payees
cobra_subs = df_bse[df_bse["Is_COBRA"] == "Y"].head(10)
for idx, sub in cobra_subs.iterrows():
    # Individual billing amount for Dental + Vision
    amt = TIER_RATES["Dental"][sub["Billing_Tier_Code"]] + TIER_RATES["Vision"][sub["Billing_Tier_Code"]]
    messy_name = f"{sub['Last_Name'].upper()}, {sub['First_Name'][0]} COBRA PMT"
    
    ach_records.append({
        "Transaction_ID": ach_id_counter,
        "Deposit_Date": "2026-08-15",
        "Amount": amt,
        "ACH_Transit_Route_No": "031000216",
        "ACH_Originating_Bank": "State Employees CU",
        "Depositor_Name_String": messy_name,
        "Reconciliation_Rank_Match": "Rank 3 (Edit-Distance Name Match)"
    })
    ach_id_counter += 1

df_ach = pd.DataFrame(ach_records)
df_ach.to_csv("/workspace/scratch/mock_data/ach-bank-statement.csv", index=False)

# Save a copy of this generation script into the target folder so the user has the source code
shutil.copy(__file__, "/workspace/scratch/mock_data/upt-data-generator.py")

# Publish all verified files to out directory
target_files = [
    "employer-groups.csv",
    "benefit-subscribers.csv",
    "subscriber-dependents.csv",
    "group-premium-ledger.csv",
    "ach-bank-statement.csv",
    "upt-data-generator.py"
]

for filename in target_files:
    shutil.copy(f"/workspace/scratch/mock_data/{filename}", f"/workspace/out/{filename}")

print("All mock database files and python generator successfully published to outbox.")
