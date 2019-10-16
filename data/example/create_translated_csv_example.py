import sys
sys.path.append("../")
import data
import pandas

addr = ''
mdp = ''
#data.create_csv_mail("./mails.csv", addr, mdp) # Create mail database in a csv file of all the mailbox
data.create_csv_mail("./mails_test.csv", addr, mdp, mails_to_copy=50) # Create mail database in a csv file of 50 mails in the mailbox

df = data.get_pandas_from_csv("./mails_test.csv") 
df = data.get_txt_from_pandas(df)

df = data.get_translated_from_pandas_and_create_csv(df, "./mails_test_translated.csv")

df_2 = data.get_pandas_from_csv("./mails_test_translated.csv")
df_2 = data.get_keywords_from_pandas(df_2, 1, 8) # Get 1 keyword from the subject and 8 keywords from the text

print(df_2['2'][10]) # Print subject (['2']) of the 10th mail
print(df_2['4'][10]) # Print text (['4']) of the 10th mail
