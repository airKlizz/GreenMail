import data
import pandas

addr = input("email address : ")
mdp = input("password : ")
folder_path = input("folder_path (ex : database/) : ")
file_name = input("file_name (ex : my_emails) : ")

data.create_csv_mail(folder_path+file_name+"_no_translated.csv", addr, mdp) # Create mail database in a csv file of 100 mails in the mailbox

df = data.get_pandas_from_csv(folder_path+file_name+"_no_translated.csv") 
df = data.get_txt_from_pandas(df)

df = data.get_translated_from_pandas_and_create_csv(df, folder_path+file_name+"_translated.csv")
