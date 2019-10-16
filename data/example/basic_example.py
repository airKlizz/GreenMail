import data
import pandas

addr = ''
mdp = ''
#data.create_csv_mail("./mails.csv", addr, mdp) # Create mail database in a csv file of all the mailbox
data.create_csv_mail("./mails_test.csv", addr, mdp, mails_to_copy=10) # Create mail database in a csv file of 10 mails in the mailbox

list_csv = ["./mails_test.csv", "./mails_test.csv"] # Example of a list of csv file
df = data.get_pandas_from_list_csv(list_csv) 
print(df['0'][10]) # Print sending email address (['0']) of the 10th mail
print(df['1'][10]) # Print sending name (['1']) of the 10th mail
print(df['2'][10]) # Print subject (['2']) of the 10th mail
print(df['3'][10]) # Print date (['3']) of the 10th mail
print(df['4'][10]) # Print text (['4']) of the 10th mail

df = data.get_txt_from_pandas(df)
df = data.get_translated_from_pandas(df)
df = data.get_keywords_from_pandas(df, 2, 10) # Get 2 keywords from the subject and 10 keywords from the text

print(df['2'][10]) # Print subject (['2']) of the 10th mail
print(df['4'][10]) # Print text (['4']) of the 10th mail
