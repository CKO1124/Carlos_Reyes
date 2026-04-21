**SQL Server Data Cleaning & Analytics Pipeline**:

A Python-based ETL (Extract, Transform, Load) pipeline that automates the cleaning and analysis of retail transaction data stored in SQL Server.

This project connects to a local SQL Server instance to extract raw, unformatted data. Using Pandas, the script cleans inconsistencies, handles missing values, and calculates business KPIs before exporting a final dataset for reporting.


**🛠️ Key Technical Features**
- Database Connectivity: Uses pyodbc to securely fetch data from SQL Server.
- Data Cleaning: 
Standardizes inconsistent naming and category formats.
Parses complex/mixed date strings into uniform datetime objects.
Handles null values in price and quantity columns.


**Automated Analytics:**
- Calculates total sales per transaction and per customer.
- Identifies top-performing store locations and product categories.
- Generates percentage-based category distribution reports.
- Export: Saves the final cleaned data to a .csv file for use in Power BI or Excel.
