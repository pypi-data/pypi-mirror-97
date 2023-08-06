# Techfin Golden Records Parser Pipeline
# Introduction 
This project is dedicated to TOTVS developers that works with Anticipation or Financial Cockpit projects.  
With this package you will be able to:
- Download the data from Carol platform
- Merge the data
- Clean the unneeded informations
- Get the last status from each installment considering all the history of payments events
- Parsing the NFe XML

# Getting Started
As first step you need to configure a .env file with Carol's authentication information.  
After this you can simply call: default_techfin_data_parser(connector_name) this function will return two pandas dataframes with receivables and payments already treated.