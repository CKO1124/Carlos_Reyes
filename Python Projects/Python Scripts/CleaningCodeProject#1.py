import pandas as pd
import pyodbc

#Connecting to SQL server to retrieve the dataset we'll be using
DRIVER = 'ODBC Driver 17 for SQL Server'
SERVER = r'YOUR_SERVER_NAME'
DATABASE = 'DataCleaning'
conn_str = f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"

try:
    with pyodbc.connect(conn_str) as conn: 
        query = '''SELECT * 
            FROM dbo.messy_data'''
        
        df = pd.read_sql(query, conn)
        

        #Validating that query and connection gave an actual result
        if not df.empty:
            
            #Replacing wrongly spelled values and capitalizing names and product_category column
            df['Product_Category'] = df['Product_Category'].str.strip().str.replace('elec.', 'Electronics', case=False).str.capitalize()
            df['Store_Location'] = df['Store_Location'].str.replace('ny', 'New York', case=False)
            df['Customer_Name'] = df['Customer_Name'].str.capitalize().str.title()
            df['Store_Location'] = df['Store_Location'].str.title()


            #Standarizing date format
            df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
            df['Date'] = df['Date'].dt.strftime('%m-%d-%Y')


            #Adjusting price format to float to show decimals and filling any NA value with 1 as default value
            df['Unit_Price'] = df['Unit_Price'].fillna(1).astype(float).round(2)

            #__________________________________________
            #=====Analytics and Data Manipulation======
            #------------------------------------------

            #1. Adding a column of total sells per row
            df['Total_sells'] = df['Unit_Price'] * df['Quantity']
            df = df.sort_values(by='Total_sells', ascending=False)


            #2. Amount Spent by each customer
            customer_purchase = df.groupby('Customer_Name').agg(
                amount_spent=('Total_sells', 'sum'),
                units_acquired=('Quantity','sum')
            ).reset_index().sort_values(by='amount_spent', ascending=False)


            #3. Top Sales Store location
            top_location = df.groupby('Store_Location').agg(
                location_sells=('Total_sells','sum')
            ).sort_values(by='location_sells', ascending=False).reset_index()


            #4. Top Categories and amount sold 
            top_category = df.groupby('Product_Category').agg(
                total_unit=('Quantity','sum'),
                total_sells=('Total_sells','sum')
            ).sort_values(by='total_sells', ascending=False).reset_index()

            #5. Percentage per Category in the Dataset
            cat_percentage = (df['Product_Category'].value_counts(normalize=True) * 100).map('{:.0f}%'.format)

            
            #Saving final dataset into a new file
            df.to_csv("FinalDatasetProject#1.csv")
          
        else:
            print("File is empty")

except Exception as e:
    print(f"Error occured: {e}")
    



