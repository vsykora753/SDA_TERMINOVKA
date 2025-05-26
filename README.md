# SDA_TERMINOVKA

zdrojový kód pro SDA terminovku:

https://github.com/vsykora753/SDA_TERMINOVKA

## Popis projektu
Termínovka je webová aplikace, která slouží k evidenci a správě závodů v běhu. Uživatelé se mohou registrovat, přihlašovat a odhlašovat ze závodů,umožňuje vyhledávání a zobrazení detailů závodů, jako jsou datum, místo konání, typ závodu a další informace. Uživatelé mohou také sledovat své přihlášky a výsledky závodů, které absolvovali.

## Instalace
#### 1. Naklonujte repozitář:
   -   git clone https://github.com/vsykora753/SDA_TERMINOVKA.git
#### 2. Vytvořte virtuální prostředí a aktivujte ho:
   -   python -m venv venv
   -   source venv/bin/activate  # Na Windows použijte `venv\Scripts\activate`
#### 3. Nainstalujte závislosti:
   -   pip install -r requirements.txt
#### 4. Proveďte migrace databáze:
   -   python manage.py migrate
#### 5. Spusťte vývojový server:
   -   python manage.py runserver


## Funkcionality

#### 1. Hlavní stránka 
    -[] výpis seznamu událostí seřazených podle data   
    -[] navigační lišta    
    -[] vyhledávání událostí
    -[] registrace a přihlášení uživatele

#### 2. Základní funkcionality pro uživatele:
    -[] registrace uživatele
    -[] přihlášení/odhlášení uživatele
        -[] účet uživatele/profil
            -[] ověření emailu
            -[] změna hesla
            -[] přehled přihlášených závodů
            -[] přehled výsledků
            -[] registrace na závod
            -[] odhlášení ze závodů

#### 3. Základní funkcionality pro organizátory:

    -[] role organizátora (typ uživatele nebo samostatný model, skupina-) Nevím co je lepší? (zatím mám jako samostatný model)

        -[] přidání události
        -[] úprava události
        -[] smazání události
        -[] přehled přihlášených závodníků
        -[] přidání výsledků závodníků (možnost importu) excel


#### 4. Administrace:
        -[] přidání uživatele
        -[] úprava uživatele
        -[] smazání uživatele
        -[] přidání organizátora
        -[] úprava organizátora
        -[] smazání organizátora

## Databáze

#### 1. Uživatelé
    -[] fields:
    -[] id,         IntegerField,primary_key=True,auto_created=True
    -[] email,      CharField,unique=True,max_length=60,not null,blank=False
    -[] first_name, CharField,max_length=30,not null,blank=False
    -[] last_name,  CharField,max_length=30,not null,blank=False
    -[] birth_date, DateField,not null,blank=False
    -[] sex,        CharField,choices=[
                    ('M', 'Male'), ('F', 'Female')],max_length=1,not null,blank=False
    -[] password,   CharField,max_length=128,not null,blank=False
    -[] role,       CharField,choices=[
                    ('R', 'Runner'), ('O', 'Organizer'), ('A', 'Admin')],max_length=1,not null,blank=False

    
#### 2. Události   
    -[] fields:
    -[] idevent,        IntegerField,primary_key=True,auto_created=True
    -[] name_event,     CharField,max_length=30,not null,blank=False 
    -[] description,    TextField,not null,blank=False 
    -[] start_time,     DateTimeField,not null,blank=False
    -[] distance,       IntegerField,not null,blank=False
    -[] country,        CharField,max_length=50,not null,blank=False
    -[] city,           CharField,max_length=50,not null,blank=False      
    -[] region,         CharField,max_length=100,not null,blank=False
    -[] typ_race,       CharField,choices=[
                        ('Silnice', 'Silnice'), ('Trail', 'Trail'), , ('Mix', 'Smíšený')],max_length=7,not null,blank=False
    -[] propozition,    charfield, max_length=100,null,blank=False
    -[] start_fee,      IntegerField,null,blank=False
    -[] organizer,      ForeignKey,Organizer,on_delete=models.CASCADE,not null,blank=False
  


#### 3. Výsledky
    -[] id
    -[] závodník
    -[] událost
    -[] čas
    
#### 4. Organizátoři
    -[] id
    -[] jméno
    -[] příjmení
    -[] email
    -[] heslo
    -[] role (závodník, organizátor, admin);


