from pandas import read_csv
import os

dirt = './mail/'
for root,dirs, filenames in os.walk(dirt):
    for f in filenames:
        if f.endswith('.csv'):
            mboxfile = f
            print (f)

            ff = './mail/' + f

            x = read_csv(ff)
            x.columns = ['col1', 'col2', 'col3', 'col4', 'col5']
            x.to_csv('./mail/cleaned_mail.csv', index=False)