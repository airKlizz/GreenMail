import data
import pandas

addr = ''
mdp = ''
data.create_csv_gmail(addr,mdp)
l = ['mails_alex.csv', 'mails_alex.csv']
df = data.get_pandas_from_list_csv(l)
print(df['4'][55])

df = data.get_txt_from_pandas(df)
df = data.get_translated_from_pandas(df)
df = data.get_keywords_from_pandas(df, 2, 10)
print(df['2'][55])
print(df['4'][55])
