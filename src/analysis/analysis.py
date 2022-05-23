import pandas as pd
import re
import numpy as np

def set_up(df):
    list_prix = []
    for i in range(len(df)):
        x = df.iloc[i]
        if x['prix'] == '€':
            list_prix.append(1)
        elif x['prix'] == '€€':
            list_prix.append(2)
        elif x['prix'] == '€€€':
            list_prix.append(3)
        else:
            list_prix.append('None')
    df.assign(PRIX_VALEUR = list_prix)
            
    df.drop(df.loc[df['note']=='None'].index, inplace=True)
    df.drop(df.loc[df['nbr_avis']=='None'].index, inplace=True)
    
    changement_note = []
    for i in range(len(df)):
        x = df.iloc[i]
        note_valeur = re.compile(r'[0-9]').findall(x['note'])
        if len(note_valeur) == 3:
            test = (note_valeur[0]+'.'+note_valeur[1])
            changement_note.append(float(test))
        else:
            test = note_valeur[0]
            changement_note.append(float(test))
    df = df.assign(NOTE_VALEUR = changement_note)

    changement_avis = []
    for i in range(len(df)):
        x = df.iloc[i]
        avis_valeur = re.compile(r'[0-9]').findall(x['nbr_avis'])
        test = (avis_valeur[0])
        changement_avis.append(float(test))
    df = df.assign(AVIS_VALEUR = changement_avis)
    
    df["quartier"]= df.quartier.str.replace("75116","75016", regex=True)
    
    return(df)

    
def analysis_quartier(df):
    a = []
    b = []
    for i in range(len(df['quartier'].value_counts())-1):
        a.append(df['quartier'].value_counts()[i])
        b.append(df['quartier'].value_counts().index[i])
    df_quartier = pd.DataFrame({"Quartier" : b, 
                                "Valeur_Quartier": a})
    return(df_quartier)


def analysis_type(df):
    a = []
    b = []
    for i in range(len(df['type'].value_counts())-1):
        a.append(df['type'].value_counts()[i])
        b.append(df['type'].value_counts().index[i])
    df_type = pd.DataFrame({"Type" : b, 
                                "Valeur_Type": a})
    return(df_type)


def analysis_prix(df):
    a = []
    b = []
    for i in range(len(df['prix'].value_counts())-1):
        a.append(df['prix'].value_counts()[i])
        b.append(df['prix'].value_counts().index[i])
    df_prix = pd.DataFrame({"Prix" : b, 
                                "Valeur_Prix": a})
    return(df_prix)


def avis_quartier(df):
    x_quartier = df['quartier'].unique()
    note_quartier = sorted((df['NOTE_VALEUR'])
                        .unique())
    df_quartier = pd.DataFrame(index = note_quartier, columns = x_quartier).fillna(0)
    for x in df_quartier:
        for i in range(len(df[df['quartier'] == x])):
            y = (df[df['quartier'] == x]).iloc[i]
            for i in range(len(note_quartier)):
        
                if y['NOTE_VALEUR'] == note_quartier[i]:
                    df_quartier[x][note_quartier[i]] +=1  
    temp = []
    compte=0
    moyenne_quartier2 = []
    for yx in df_quartier.columns: 
        
        for i in range(len(df_quartier[yx])):
            x = df_quartier[yx].iloc[i]
            result = x * df_quartier[yx].index[i]
            temp.append(result)
            compte += df_quartier[yx].iloc[i]
        
        total = 0 
        for i2 in range(len(temp)):
            total+=temp[i2]
        moyenne_quartier2.append(total/compte)
    moyenne_quartier = []
    for i in range(len(moyenne_quartier2)):
        if df_quartier.columns[i] != 'None':
            moyenne_quartier.append([df_quartier.columns[i], moyenne_quartier2[i]])
    moyenne_quartier = pd.DataFrame(moyenne_quartier)
    return (moyenne_quartier)


def avis_type(df):
    x_type = df['type'].unique()
    note_type = sorted((df['NOTE_VALEUR'])
                        .unique())
    df_type = pd.DataFrame(index = note_type, columns = x_type).fillna(0)

    for x in df_type:
        for i in range(len(df[df['type'] == x])):
            y = (df[df['type'] == x]).iloc[i]
            for i in range(len(note_type)):
        
                if y['NOTE_VALEUR'] == note_type[i]:
                    df_type[x][note_type[i]] +=1
    delete = []
    for i in df_type.columns:
        if df_type[i].sum() <= 5:
            delete.append(i)
    df_type = df_type.drop(delete, axis =1)
    temp = []
    compte=0
    moyenne_type2 = []
    for yx in df_type.columns: 
        for i in range(len(df_type[yx])):
            x = df_type[yx].iloc[i]
            result = x * df_type[yx].index[i]
            temp.append(result)
            compte += df_type[yx].iloc[i]
        total = 0 
        for i2 in range(len(temp)):
            total+=temp[i2]
        moyenne_type2.append(total/compte)
    moyenne_type = []
    for i in range(len(moyenne_type2)):
        if df_type.columns[i] != 'Parcs d’attractions':
            moyenne_type.append([df_type.columns[i], moyenne_type2[i]])
    moyenne_type = pd.DataFrame(moyenne_type)
    return(moyenne_type)


def avis_prix(df):
    x_prix = df['prix'].unique()
    note_prix = sorted((df['NOTE_VALEUR']).unique())
    df_prix = pd.DataFrame(index = note_prix, columns = x_prix).fillna(0)

    for x in df_prix:
        for i in range(len(df[df['prix'] == x])):
            y = (df[df['prix'] == x]).iloc[i]
            for i in range(len(note_prix)):
                if y['NOTE_VALEUR'] == note_prix[i]:
                    df_prix[x][note_prix[i]] +=1 
                    
    temp = []
    compte=0
    moyenne_prix2 = []
    for yx in df_prix.columns: 
        
        for i in range(len(df_prix[yx])):
            x = df_prix[yx].iloc[i]
            result = x * df_prix[yx].index[i]
            temp.append(result)
            compte += df_prix[yx].iloc[i]
        
        total = 0 
        for i2 in range(len(temp)):
            total+=temp[i2]
        moyenne_prix2.append(total/compte)
    moyenne_prix = []
    for i in range(len(moyenne_prix2)):
        if df_prix.columns[i] != 'None':
            moyenne_prix.append([df_prix.columns[i], moyenne_prix2[i]])
    moyenne_prix = pd.DataFrame(moyenne_prix)  
    return(moyenne_prix)
    
    
if __name__ == "__main__":
    df = pd.read_csv('./src/analysis/LePetitFute.csv')
    df1 = set_up(df)
    analysis_quartier(df1)