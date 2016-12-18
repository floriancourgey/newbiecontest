#! /usr/bin/env python3
# coding: utf-8

import config
import requests
import re
import time
from math import sqrt

def get(url):
    print("Appel GET "+url)
    r = requests.get(url, cookies=cookies)
    html = r.text
    print("html reçu", html)
    return html
def post(url, data):
    print("Appel POST "+url, data)
    r = requests.post(url, cookies=cookies, data=data)
    html = r.text
    print("html reçu", html)
    return html

# constantes
cookies = {config.COOKIE_KEY:config.COOKIE_VALUE}
urlBase = 'https://www.newbiecontest.org/epreuves/prog/frok-fichus_nb/'
urlProg1 = urlBase+'prog_1.php'
urlProg1Validation = urlBase+'verif_1.php'
urlProg2 = urlBase+'prog_2.php'
urlProg2Validation = urlBase+'verif_2.php'
urlProg3 = urlBase+'prog_3.php'

# html = "<strong>Bienvenue!</strong><br/><br/>Les sept anagrammes dans l'ordre sont:  0716454-4023366x8527952;6959196'1563139°3531833&8282988<br/><br/>Renvoyez les réponses en moins d'une seco"

# Programme 1
def programme1():
    # ouverture du dico et strip des lignes (car elles contiennent chacune \n)
    dico = []
    with open('anag.txt') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            dico.append(line)

    # appel à l'url
    print("====================")
    print("==== Question 1 ====")
    print("====================")
    html = get(urlProg1)
    print("====================")
    print("====================")
    print("====================")
    matches = re.search(r"sont:\s+(.+)<br/><br/>Renvoyez", html)
    mots = matches.group(1)
    mots = re.findall(r"[\d]+", mots)
    print("mots trouvés : ",mots)
    if(len(mots) != 7):
        print("Erreur, il faut 7 mots")
        exit()

    # recherche des anagrammes
    anagrammes = []
    for mot in mots:
        for anagramme in dico:
            if len(anagramme) == len(mot):
                anagramme_ok = True
                for lettre in mot:
                    if mot.count(lettre) != anagramme.count(lettre):
                        anagramme_ok = False
                        break
                if anagramme_ok:
                    anagrammes.append(anagramme)
                    break
    # envoi de la réponse
    data = {}
    for i,anagramme in enumerate(anagrammes):
        data['rep'+str(i+1)] = anagramme
    html = post(urlProg1Validation, data)
    matches = re.search(r"<br/>Le login est: (.+)\.</body>", html)
    login = matches.group(1)
    print("===================")
    print("==== Réponse 1 ====")
    print("login : "+login)
    print("===================")
    print("===================")
    print()
    return login

# Programme 2
def programme2():
    # get html
    print("====================")
    print("==== Question 2 ====")
    print("====================")
    html = get(urlProg2)
    print("====================")
    print("====================")
    print("====================")
    # matches = re.search(r"(1\).+année\?)", html)
    # questions = matches.group(1)

    # question 1.
    # tout ceci peut se pré-calculer car les données ne changent pas
    # fwords = fibword(45)
    # print("milliardième lettre "+fwords[44][1000000000-1])
    # print("10 lettres avant et 10 lettres après la milliardième : "+fwords[44][1000000000-10:1000000000+10])
    # milliard = fwords[44][0:1000000000]
    # milliard_taille = len(milliard)
    # milliard_nb_hommes = milliard.count('H')
    # milliard_nb_femmes = milliard.count('F')
    # milliard_check = milliard_nb_hommes + milliard_nb_femmes
    # print("len milliard : "+str(milliard_taille)+", nb hommes : "+str(milliard_nb_hommes)+", nb femmes : "+str(milliard_nb_femmes)+', check h+f :'+str(milliard_check))
    reponse1_sexe = 'Femme'
    reponse1_hommes = 381966011
    reponse1_femmes = 618033989

    # question 2.
    ## recherche des données :
    matches = re.search(r"extraterrestres pour enlever (\d+) habitants", html)
    nbHabitantsAEnlever = matches.group(1)
    print("nbHabitantsAEnlever : "+nbHabitantsAEnlever)
    nbHabitantsAEnlever = int(nbHabitantsAEnlever)
    ## calcul réponse :
    nbHabitantsEnleves = 0
    n = 0
    while(nbHabitantsEnleves < nbHabitantsAEnlever):
        n += 1
        nbHabitantsEnleves += fibonacci(n)
    reponse2 = n
    print("2. "+str(nbHabitantsEnleves)+" habitants enlevés sur un total de "+str(reponse2)+" années")

    # question 3.
    ## recherche des données :
    matches = re.search(r"captifs durant la (\d+)", html)
    n = matches.group(1)
    print("durant la "+n+"ème année")
    n = int(n)
    ## calcul réponse
    nbHabitantsEnleves = fibonacci(n)
    reponse3 = nbHabitantsEnleves
    print("3. "+str(reponse3)+" habitants enlevés sur l'année "+str(n))

    # validation
    data = {
        "rep1":reponse1_sexe,
        "rep2":reponse1_hommes,
        "rep3":reponse1_femmes,
        "rep4":reponse2,
        "rep5":reponse3
    }
    html = post(urlProg2Validation, data=data)
    # matches = re.search(r"<br/>Le login est: (.+)\.</body>", html)
    # login = matches.group(1)
    # print("login : "+login)
# question 1
def fibword(n=38):
    # fwords = ['1', '0']
    fwords = ['H', 'F']
    print('%-3s %13s %10s %s' % tuple('N Longueur Secondes Résultat'.split()))
    def pr(n, fwords):
        temps1 = time.time()
        while len(fwords) < n:
            fwords += [''.join(fwords[-2:][::-1])]
        v = fwords[n-1]
        temps2 = time.time()-temps1
        longueur = format(len(v), ',d')
        secondes = '{0:.2g}'.format(temps2)
        resultat = v if len(v) < 150 else '_'
        print('%3i %13s %10s %s' % (n, longueur, secondes, resultat))
    for n in range(1, n+1): pr(n, fwords)
    return fwords
# question 2 & 3
def fibonacci(n):
    return round( ((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5)) )

programme1()
programme2()



#envoi
