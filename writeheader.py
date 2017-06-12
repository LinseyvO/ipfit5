from pandas import read_csv
x = read_csv('clean_mail.csv')
x.columns = ['col1', 'col2', 'col3', 'col4', 'col5']
x.to_csv('cleaned_mail.csv', index=False)