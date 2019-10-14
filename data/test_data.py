import data
import pandas

addr = ''
mdp = ''
#data.create_csv_gmail("./mails.csv", addr, mdp) # Create mail database in a csv file of all the mailbox
data.create_csv_gmail("./mails2.csv", addr, mdp, mails_to_copy=10) # Create mail database in a csv file of 10 mails in the mailbox

l = ["./mails2.csv", "./mails2.csv"] # Example of a list of csv file
df = data.get_pandas_from_list_csv(l) 
print(df['2'][10]) # Print subject (['2']) of 55th mail
print(df['4'][10]) # Print text (['4']) of 55th mail

df = data.get_txt_from_pandas(df)
df = data.get_translated_from_pandas(df)
df = data.get_keywords_from_pandas(df, 2, 10) # Get 2 keywords for the subject and 10 keywords for the text

print(df['2'][10]) # Print subject (['2']) of 55th mail
print(df['4'][10]) # Print text (['4']) of 55th mail
