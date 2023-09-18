# Formi Clean Customer Data API
The repository contains the source code of an API that accepts the unorganized data of users of Formi's clients in the 
form of an Excel file and cleans it in a way that it can be mapped to Formi's backend in an automated fashion. 

The resulting CSV file get stored in Formi's backend bucket in S3.

## Technologies Used:  
Python3, pandas, openpyxl

## AWS Services Used: 
API Gateway, Lambda, S3, CloudWatch  

## API Endpoints:

**PUT**   _https://jvt1ypuao4.execute-api.ap-south-1.amazonaws.com/dev/<bucket_name>/<excel_file_name>_ 

You need to attach the concerned Excel File in binary format in the Body of the PUT request

<bucket_name> needs to be replaced by the bucket where you have setup a trigger to run the Lambda function to run the 
backend code to clean the data and save it in another secure S3 bucket.

<excel_file_name> needs to be replaced by the name with which you want to save your file in <bucket_name>