# ReadMe

## How to Run
1. Put ***main.py***, ***DataParsing.py***, ***License.py*** and ***constants.py*** in your working directory.
2. You may alter variable *if_save* to *False* in ***constants.py*** if you do not want to save dataframes to local csv files.
3. You may also alter variable *path* in ***constants.py*** to the directory where your would like to store data sheets.
4. You may use this command to run this project and get data sheets. You can add extra stickers as arg parameters

        python main.py BIDU JD

## Files Description
### License.py
You have to add your own account information in this file.
To pass robot test on website, *headers* is set to a browser address.
And 4 different accounts are given. You may also change them to your accounts. In each request, the login account is chosen in the list of *users* randomly to avoid the case of too many requests per user per hour.

### constants.py
You may change your data directory here.
Also, if there is a robot test situation, please set *sleep_time* larger to avoid the case of too many requests per user per hour.

### DataParsing.py
This file contains all methods about crawling data and parsing text from html.
* ***get_url***: get the website address based on given sticker.
* ***get_sub_url***: get urls for 12 cosecutive quarters
* ***get_text***: parse the html file and generate dataframe.

### BIDU.csv
Sample data sheet.
