from pandas import read_csv
import os

dirt = './mail/' # dirt variabele wordt gedeclareerd
for root,dirs, filenames in os.walk(dirt): # er wordt door de opgegeven dirt variabele geitereerd
    for f in filenames: # f wordt gelijk aan de filenames in de opgegeven folder
        if f.endswith('.csv'): # als de file eindigt met de csv extensie ->
            mboxfile = f # wordt mboxfile gelijk gemaakt aan f
            print (f) # f wordt uitgeprint op de terminal

            ff = './mail/' + f # ff wordt gedeclareerd en gelijk gemaakt aan het pad + het gevonden csv bestand

            x = read_csv(ff) # het csv bestand wordt gelezen en aan x toegevoegd
            x.columns = ['col1', 'col2', 'col3', 'col4', 'col5'] # er wordt aan elke column een header title meegegeven
            x.to_csv('./mail/cleaned_mail.csv', index=False) # deze wijzigingen worden toegevoegd aan een nieuw csv bestand
