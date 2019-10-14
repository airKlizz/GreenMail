import data.data as data
import function
import pandas

addr = input("email address : ")
mdp = input("password : ")

data.create_csv_gmail("./data/mails_method_3_1.csv", addr, mdp, mails_to_copy=100) # Create mail database in a csv file of 10 mails in the mailbox

df = data.get_pandas_from_csv("./data/mails_method_3_1.csv") 
df = data.get_txt_from_pandas(df)

df = data.get_translated_from_pandas_and_create_csv(df, "./data/mails_method_3_1_translated.csv")
