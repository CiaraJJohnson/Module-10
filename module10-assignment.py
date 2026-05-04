# Module 10 Assignment: Data Manipulation and Cleaning with Pandas
# UrbanStyle Customer Data Cleaning

# Import required libraries
import pandas as pd
import numpy as np
from datetime import datetime

# Welcome message
print("=" * 60)
print("URBANSTYLE CUSTOMER DATA CLEANING")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO SIMULATE A CSV FILE (DO NOT MODIFY) -----
from io import StringIO

# Simulated CSV content with intentional data issues
csv_content = """customer_id,first_name,last_name,email,phone,join_date,last_purchase,total_purchases,total_spent,preferred_category,satisfaction_rating,age,city,state,loyalty_status
CS001,John,Smith,johnsmith@email.com,(555) 123-4567,2023-01-15,2023-12-01,12,"1,250.99",Menswear,4.5,35,Tampa,FL,Gold
CS002,Emily,Johnson,emily.j@email.com,555.987.6543,01/25/2023,10/15/2023,8,$875.50,Womenswear,4,28,Miami,FL,Silver
CS003,Michael,Williams,mw@email.com,(555)456-7890,2023-02-10,2023-11-20,15,"2,100.75",Footwear,5,42,Orlando,FL,Gold
CS004,JESSICA,BROWN,jess.brown@email.com,5551234567,2023-03-05,2023-12-10,6,659.25,Womenswear,3.5,31,Tampa,FL,Bronze
CS005,David,jones,djones@email.com,555-789-1234,2023-03-20,2023-09-18,4,350.00,Menswear,,45,Jacksonville,FL,Bronze
CS006,Sarah,Miller,sarah_miller@email.com,(555) 234-5678,2023-04-12,2023-12-05,10,1450.30,Accessories,4,29,Tampa,FL,Silver
CS007,Robert,Davis,robert.davis@email.com,555.444.7777,04/30/2023,11/25/2023,7,$725.80,Footwear,4.5,38,Miami,FL,Silver
CS008,Jennifer,Garcia,jen.garcia@email.com,(555)876-5432,2023-05-15,2023-10-30,3,280.50,ACCESSORIES,3,25,Orlando,FL,Bronze
CS009,Michael,Williams,m.williams@email.com,5558889999,2023-06-01,2023-12-07,9,1100.00,Menswear,4,39,Jacksonville,FL,Silver
CS010,Emily,Johnson,emilyjohnson@email.com,555-321-6547,2023-06-15,2023-12-15,14,"1,875.25",Womenswear,4.5,27,Miami,FL,Gold
CS006,Sarah,Miller,sarah_miller@email.com,(555) 234-5678,2023-04-12,2023-12-05,10,1450.30,Accessories,4,29,Tampa,FL,Silver
CS011,Amanda,,amanda.p@email.com,(555) 741-8529,2023-07-10,,2,180.00,womenswear,3,32,Tampa,FL,Bronze
CS012,Thomas,Wilson,thomas.w@email.com,,2023-07-25,2023-11-02,5,450.75,menswear,4,44,Orlando,FL,Bronze
CS013,Lisa,Anderson,lisa.a@email.com,555.159.7530,08/05/2023,,0,0.00,Womenswear,,30,Miami,FL,
CS014,James,Taylor,jtaylor@email.com,555-951-7530,2023-08-20,2023-10-10,11,"1,520.65",Footwear,4.5,,Jacksonville,FL,Gold
CS015,Karen,Thomas,karen.t@email.com,(555) 357-9512,2023-09-05,2023-12-12,6,685.30,Womenswear,4,36,Tampa,FL,Silver
"""

# Create a StringIO object (simulates a file)
customer_data_csv = StringIO(csv_content)

# Now you can load this as if it was a CSV file:
# raw_df = pd.read_csv(customer_data_csv)
# ----- END OF SIMULATION CODE -----

# TODO 1: Load and Explore the Dataset
# 1.1 Load the dataset and display basic information
# REQUIRED: Store DataFrame in variable 'raw_df'

raw_df = pd.read_csv(customer_data_csv)

print(raw_df.head()) #looks at the first few rows
print(raw_df.info()) # checks column types and shows the missing values


# 1.2 Assess the data quality issues (missing values, incorrect formats, duplicates)
# REQUIRED: Store initial missing value counts in 'initial_missing_counts' (pandas Series)
# REQUIRED: Store duplicate count in variable 'initial_duplicate_count' (int)

initial_missing_counts = raw_df.isnull().sum() 
initial_duplicate_count = raw_df.duplicated().sum()  # this checks for any duplicated rows


# TODO 2: Handle Missing Values
# 2.1 Identify and count missing values
# REQUIRED: Store in variable 'missing_value_report' (pandas Series)
missing_value_report = raw_df.isnull().sum()  #stores the data into the variable


# 2.2 Fill missing satisfaction_rating with the median value
# REQUIRED: Store median value used in variable 'satisfaction_median' (float)
satisfaction_median = raw_df['satisfaction_rating'].median()  # we store the value into the  variable and uses median
raw_df['satisfaction_rating'] = raw_df['satisfaction_rating'].fillna(satisfaction_median)


# 2.3 Fill missing last_purchase dates appropriately
# REQUIRED: Store strategy used in variable 'date_fill_strategy'
date_fill_strategy = 'forward_fill'  # This stores the stragedy an uses forward fill so that it uses the previous valid date
raw_df['last_purchase'] = raw_df['last_purchase'].fillna(method='ffill')


# 2.4 Handle other missing values as needed
# REQUIRED: Store cleaned DataFrame in variable 'df_no_missing'  
df_no_missing = raw_df.copy()   

df_no_missing['last_name'] = df_no_missing['last_name'].fillna('Unknown') #If the last name is missing this fills it in a placehholder 
df_no_missing['phone'] = df_no_missing['phone'].fillna('0000000000')  #If its missing any phone numbers it fills it 
df_no_missing['loyalty_status'] = df_no_missing['loyalty_status'].fillna('Unknown') # if there is a missing loyalty status it fills it with "unknown"
df_no_missing['age'] = df_no_missing['age'].fillna(df_no_missing['age'].median()) # This fills any missing age with just the median age


# TODO 3: Correct Data Types
# 3.1 Convert join_date and last_purchase to datetime
# REQUIRED: Work with 'df_no_missing' and store result in 'df_typed'
df_typed = df_no_missing.copy()

#Converts the different date formats into standard daytime
df_typed['join_date'] = pd.to_datetime(df_typed['join_date'], errors='coerce')
df_typed['last_purchase'] = pd.to_datetime(df_typed['last_purchase'], errors='coerce')


# 3.2 Convert total_spent to numeric (handle currency symbols and commas)
# REQUIRED: Continue working with 'df_typed'   @
df_typed['total_spent'] = df_typed['total_spent'].replace('[\$,]', '', regex=True) #removes any $ signs and commas before it converts 
df_typed['total_spent'] = pd.to_numeric(df_typed['total_spent'])


# 3.3 Ensure other numeric fields (total_purchases, age) are correct types
# REQUIRED: Store final typed DataFrame in 'df_typed'
df_typed['total_purchases'] = pd.to_numeric(df_typed['total_purchases']) # Makes sure that the columns are numbers for calculations
df_typed['age'] = pd.to_numeric(df_typed['age'])


# TODO 4: Clean and Standardize Text Data
# 4.1 Standardize case for first_name and last_name (proper case)
# REQUIRED: Work with 'df_typed' and store result in 'df_text_cleaned'
df_text_cleaned = df_typed.copy()


# Converts names to be upper case rather then lowerr
df_text_cleaned['first_name'] = df_text_cleaned['first_name'].str.title()
df_text_cleaned['last_name'] = df_text_cleaned['last_name'].str.title()


# 4.2 Standardize category names (consistent capitalization)
# REQUIRED: Continue working with 'df_text_cleaned'
df_text_cleaned['preferred_category'] = df_text_cleaned['preferred_category'].str.title()  #Makes the categories consistent


# 4.3 Standardize phone numbers to a consistent format
# REQUIRED: Store standardized phone format used in variable 'phone_format' (string)
phone_format = "(XXX) XXX-XXXX"

def fix_phone(x):
    nums = ''.join(filter(str.isdigit, str(x)))
    if len(nums) == 10:
        return "(" + nums[:3] + ") " + nums[3:6] + "-" + nums[6:]
    else:
        return "(000) 000-0000"

df_text_cleaned['phone'] = df_text_cleaned['phone'].apply(fix_phone)
#formats the numbers properly 

# TODO 5: Remove Duplicates
# 5.1 Identify duplicate records
# REQUIRED: Store duplicate count in variable 'duplicate_count' (int)
duplicate_count = df_text_cleaned.duplicated().sum()


# 5.2 Remove duplicates while keeping the appropriate record
# REQUIRED: Work with 'df_text_cleaned' and store result in 'df_no_duplicates'
df_no_duplicates = df_text_cleaned.drop_duplicates(subset='customer_id')


# TODO 6: Add Derived Features
# 6.1 Calculate days_since_last_purchase
# REQUIRED: Work with 'df_no_duplicates' and add column
df_no_duplicates['days_since_last_purchase'] = (
    pd.Timestamp.today() - df_no_duplicates['last_purchase']
).dt.days # this helps understand customers purchase activity


# 6.2 Calculate average_purchase_value (total_spent / total_purchases)
# REQUIRED: Add column
df_no_duplicates['average_purchase_value'] = (
    df_no_duplicates['total_spent'] / df_no_duplicates['total_purchases']
) #Shows how much/ the average each customer spends per every purchse
 

# 6.3 Create a purchase_frequency_category (High, Medium, Low)
# REQUIRED: Add column #Classifies custoers based on the number of purchases
def get_category(x):
    if x >= 10:
        return "High"
    elif x >= 5:
        return "Medium"
    else:
        return "Low"

df_no_duplicates['purchase_frequency_category'] = df_no_duplicates['total_purchases'].apply(get_category)
#this classifies the customers based on their purchase history

# TODO 7: Clean Up the DataFrame
# 7.1 Rename columns to more readable formats
# REQUIRED: Store renamed DataFrame in 'df_renamed'
df_renamed = df_no_duplicates.rename(columns={
    'customer_id': 'CustomerID',
    'first_name': 'FirstName',
    'last_name': 'LastName',
    'total_spent': 'TotalSpent'
})
#Makes the columns cleaner, more professional, and easier to read


# 7.2 Remove any unnecessary columns
# REQUIRED: Store cleaned DataFrame in 'df_final'
df_final = df_renamed.drop(columns=['email']) #Removes the email column


# 7.3 Sort the data by a meaningful attribute
# REQUIRED: Sort 'df_final'
df_final = df_final.sort_values(by='TotalSpent', ascending=False) #Sorts and puts the top customer first


# TODO 8: Generate Insights from Cleaned Data
# 8.1 Calculate average spent by loyalty_status
# REQUIRED: Store result
avg_spent_by_loyalty = df_final.groupby('loyalty_status')['TotalSpent'].mean() #compares customers by loyaty status and money spent


# 8.2 Find top preferred categories by total_spent
# REQUIRED: Store result
category_revenue = df_final.groupby('preferred_category')['TotalSpent'].sum().sort_values(ascending=False)


# 8.3 Calculate correlation
# REQUIRED: Store correlation value
satisfaction_spend_corr = df_final['satisfaction_rating'].corr(df_final['TotalSpent']) #checks to see if the satisfaction leads to more spending


# TODO 9: Generate Final Report
print("\n" + "=" * 60)
print("URBANSTYLE CUSTOMER DATA CLEANING REPORT")
print("=" * 60)
#displays the final report

# 9.1 Report on data quality issues
total_missing = initial_missing_counts.sum()

print("\nData Quality Issues:")
print("- Missing Values:", total_missing)
print("- Duplicates:", initial_duplicate_count)
print("- Data Type Issues: dates, money format, and phone formats were inconsistent")


# 9.2 Describe changes
print("\nStandardization Changes:")
print("- Names: Converted to proper case")
print("- Categories: Fixed capitalization")
print("- Phone Numbers:", phone_format)


# 9.3 Business insights
print("\nKey Business Insights:")
print("- Customer Base:", df_final.shape[0])
print("- Revenue by Loyalty:")
print(avg_spent_by_loyalty)

top_cat = category_revenue.idxmax()
top_val = category_revenue.max()

print("- Top Category:", top_cat, "with $", round(top_val, 2))


# 9.4 Display final dataset
print("\nCleaned Dataset Preview:")
print(df_final.head())