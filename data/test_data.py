import data
import pandas as pd

#data.create_dataframe('catherine.calizzano@laposte.net', 'Cath0411?', 'imap.laposte.net', '/content/drive/My Drive/GreenMail/Clustering/Data', 'catherine')

dm = data.DataMail(['catherine'], '/content/drive/My Drive/GreenMail/Clustering/Data')

print(dm.get_text().head())

print(dm.get_translate().head())

print(dm.text)
print(dm.translate)
