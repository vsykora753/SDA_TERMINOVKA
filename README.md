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
    -[x] výpis seznamu událostí seřazených podle data   
    -[x] navigační lišta    
    -[x] vyhledávání událostí
    -[x] registrace a přihlášení uživatele i organizátora

#### 2. Základní funkcionality pro uživatele:
    -[x] registrace uživatele
    -[x] přihlášení/odhlášení uživatele
        -[x] účet uživatele/profil
            -[x] ověření emailu
            -[] změna hesla
            -[x] přehled přihlášených závodů
            -[] přehled výsledků
            -[x] registrace na závod
            -[x] odhlášení ze závodů

#### 3. Základní funkcionality pro organizátory:

    -[x] role organizátora 

        -[x] přidání události
        -[x] úprava události
        -[x] smazání události
        -[x] přehled přihlášených závodníků
        -[] přidání výsledků závodníků (možnost importu) excel


#### 4. Administrace:
        -[] přidání uživatele
        -[] úprava uživatele
        -[] smazání uživatele
        -[] přidání organizátora
        -[] úprava organizátora
        -[] smazání organizátora

## Databáze

#### 1. Uživatelé (users)
    -[] fields:

    -[x] id,                 IntegerField,primary_key=True,auto_created=True
    -[x] last_login          datetime
    -[x] is_superuser        bool    
    -[x] email               varchar(254)
    -[x] password            varchar(128)
    -[x] role                varchar(1)
    -[x] first_name          varchar(30)
    -[x] last_name           varchar(60)
    -[x] birth_date          date
    -[x] sex                 varchar(1)
    -[x] organization_name   varchar(100)
    -[x] website             varchar(200)
    -[x] is_active           bool
    -[x] is_staff            bool

    
#### 2. Události (events)  
    -[x] fields:
    -[x] id,             IntegerField,primary_key=True,auto_created=True
    -[x] date_event,     date
    -[x] name_event,     varchar(30) 
    -[x] description,    text not null 
    -[x] start_time,     datetime
    -[x] distance,       integer
    -[x] country,        varchar(50)
    -[x] city,           varchar(50)     
    -[x] region,         varchar(100)
    -[x] typ_race,       varchar(7)
    -[x] propozition,    varchar(100)
    -[x] start_fee,      integer
    -[x] organizer,      integer (references to user_user.id table)
  
#### 3. Registrace (registrations)
    -[x] fields:
    -[x] id,                 integer
    -[x] id_user,            integer (references to user_user.id table)
    -[x] id_event,           integer (references to events_event.id table)  
    -[x] registration_date,  datetime     
    -[x] category,           varchar(7)
    


#### 4. Výsledky (results)
    -[x] fields:
    -[x] id,            integer
    -[x] id_user,       integer (references to user_user.id table)
    -[x] id_event,      integer (references to events_event.id table)
    -[x] result_time,   time




#### 5. Platby (payments)
    -[x] fields:
    -[x] id,                 integer
    -[x] id_user,            integer (references to user_user.id table)
    -[x] id_event,           integer (references to events_event.id table)
    -[x] id_registration,    integer (references to registrations_registration.id table)   
    -[x] payment_amount,     decimal
    -[x] payment_status,     varchar(15)
    -[x] payment_date,       date
    -[x] QR_code,            varchar(255)



