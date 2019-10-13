import data
import pandas as pd

#data.create_dataframe('catherine.calizzano@laposte.net', 'Cath0411?', 'imap.laposte.net', 'catherine')

dm = data.DataMail(['catherine'])

print(dm.get_text().head())

print(dm.get_translate().head())

print(dm.text)
print(dm.translate)
