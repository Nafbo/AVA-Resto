import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

def get_html_from_link(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    return(soup)


def get_database(soup):
    all_temp_avis = []
    all_temp_prix = []
    all_temp_type = []
    all_temp_name = []
    all_temp_adresse = []
    all_temp_note = []
    
    x_name = 0
    x_avis = 0
    x_type = 0 
    x_prix = 0
    x_adresse = 0
    
    all_infos = soup.find_all("div" ,attrs={"class" : "etab-infos"})
    for infos in all_infos:       
        name = infos.find("div" ,attrs={"class" : "etab-title"})
        if name is None:
            all_temp_name.append("None")
        else:
            name = name.find('h3')
            all_temp_name.append(name.text.strip())
        x_name+=1  
        type = infos.find("span" ,attrs={"class" : "ss-cat"})
        if type is None:
            all_temp_type.append("None")
        else:
            all_temp_type.append(type.text.strip())
        x_type+=1        
        avis = infos.find("div" ,attrs={"class" : "note"})
        if avis is None:
            all_temp_avis.append("None")
            all_temp_note.append('None')
        else:
            avis_valeur = avis.text.strip()
            avis_valeur = re.compile(r'\d+').findall(avis_valeur)
            all_temp_avis.append(avis_valeur[-1])
            if len(avis_valeur) == 3:
                note = (avis_valeur[0]+"/"+avis_valeur[1])
                all_temp_note.append(note)
            else:
                note = note = (avis_valeur[0]+","+avis_valeur[1]+"/"+avis_valeur[2])
                all_temp_note.append(note)
        x_avis+=1
        adresse = infos.find("div" ,attrs={"class" : "etab-aside"})
        adresse = adresse.find("div" ,attrs={"class" : "adresse-etab"})
        if adresse is None:
            all_temp_adresse.append("None")
        else:
            adresse_valeur = adresse.text.strip()
            adresse_valeur = re.compile(r'[0-9]{5}?').findall(adresse_valeur)
            if adresse_valeur == [] :
                all_temp_adresse.append("None")
            else:
                all_temp_adresse.append(adresse_valeur[0])
        x_adresse+=1
        prix = infos.find("div" ,attrs={"class" : "adresse-etab"})
        if prix is None:
            all_temp_prix.append("None")
        else:
            prix_valeur = prix.text.strip()
            prix_valeur = re.compile(r'€').findall(prix_valeur)
            if prix_valeur == [] :
                all_temp_prix.append("None")
            else:
                all_temp_prix.append(prix_valeur[0]*len(prix_valeur))
        x_prix+=1
              
    all_name = pd.DataFrame({"id" :range(x_name),
                                "name" : all_temp_name})
    all_avis = pd.DataFrame({"id" :range(x_avis),
                                "nbr_avis" : all_temp_avis}) 
    all_type = pd.DataFrame({"id" :range(x_type), 
                             "type" : all_temp_type})
    all_prix = pd.DataFrame({"id" :range(x_prix), 
                             "prix" : all_temp_prix})
    all_adresse = pd.DataFrame({"id" :range(x_adresse), 
                             "quartier" : all_temp_adresse})
    all_note = pd.DataFrame({"id" :range(x_avis), 
                             "note" : all_temp_note})
    
    all = all_name.merge(all_note, on = "id", how ='outer')
    all = all.merge(all_avis, on = "id" ,how ='outer')
    all = all.merge(all_type, on = "id" ,how ='outer')
    all = all.merge(all_adresse, on = "id" ,how ='outer')
    all = all.merge(all_prix, on = "id" ,how ='outer')
    
    return(all)

if __name__ == "__main__":
    url = "https://www.petitfute.com/d3-paris/c1165-restaurants/"
    html = get_html_from_link(url)
    resto_avis = get_database(html)
    resto = pd.DataFrame(resto_avis)
        
    for i in range(2,124+1):
        url = f"https://www.petitfute.com/d3-paris/c1165-restaurants/?page={i}"
        html = get_html_from_link(url)
        resto_avis = get_database(html)
        resto = pd.concat([resto, resto_avis], axis = 0, ignore_index=True)
    resto.to_csv('LePetitFute.csv', index=False)
        