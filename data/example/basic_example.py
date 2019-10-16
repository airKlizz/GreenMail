import sys
sys.path.append("../")
import data
import pandas

addr = ''
mdp = ''
#data.create_csv_mail("./mails.csv", addr, mdp) # Create mail database in a csv file of all the mailbox
data.create_csv_mail("./mails_test.csv", addr, mdp, mails_to_copy=10) # Create mail database in a csv file of 10 first mails in the mailbox

list_csv = ["./mails_test.csv", "./mails_test.csv"] # Example of a list of csv file
df = data.get_pandas_from_list_csv(list_csv) 
print(df['from address'][10]) # Print sending email address of the 10th mail
print(df['from name'][10]) # Print sending name of the 10th mail
print(df['subject'][10]) # Print subject of the 10th mail
print(df['date'][10]) # Print date of the 10th mail
print(df['text'][10]) # Print text of the 10th mail

df = data.get_txt_from_pandas(df)
df = data.get_translated_from_pandas(df)
df = data.get_keywords_from_pandas(df, 2, 10) # Get 2 keywords from the subject and 10 keywords from the text

print(df['subject'][10]) # Print subject of the 10th mail
print(df['text'][10]) # Print text of the 10th mail