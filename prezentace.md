## Úvod

#### Představení projektu
- webová aplikace pro přehled pořádanýh sportovních (běžeckých) akcí
- Cílem má být přehledný kalendář akci s možností registrace a filtrování událostí
- Inspirací pro náš projekt je web ceskybeh.cz, z kterého čerpáme i skutečné pořádané akce závodů.
	Na rozdíl od zmíňovaných webových stránek jsme přidali i některá vylepšení, budeme podrobněji popisovat níže.


#### Funkcionality projektu
	👁️ Zobrazení:

		✅Zobrazení budoucích událostí (termínovka)

		🔍 Filtrování událostí podle: Kraje, Názvu závodu, datumu kdy se závod koná

		➕ Detailní zobrazení jedné události ve struktuře : název,datum,start,startovné, popis události

	👤 Uživatelský účet:
		Obecně: Registrace, přihlášení, odhlášení , změna hesla
		Přehledy: 
			přihlášených závodů, nejlepší výkony (5,10,1/2 maraton, maraton) přihlášeného běžce
	🧑‍💼 Organizátor:
		Obecně: Registrace, přihlášení, odhlášení, změna hesla
		Přehledy:
			vyhledávání svých pořadaných akcí (kraj,název závodu, datum)
			✏️ Editovat událost
			🗑️ Smazat událost
			📝 Prezenční listina (generování šablony pro výsledkovou a startovní listinu)
			📥 Možnost nahrání výsledků (MS Excel)

### Technologie projektu

	Backend:	Django (Python)
				Django admin,
				vlastní model User (umožní přihlašování pomocí emailu,přidání rolí)

	Frontend:	HTML + CSS + Javascript pro vytvoření submenu


	Databáze: 	SQLite 

	Tools:		pandas pro import výsledků

### Datový model
	User:		tvorba vlastního modelu (přihlašování pomocí emailu, uživ.role) 
			Tento model dědí z AbstractBaseUser obsahuje vlastní pole  a je 
			spravován přes vlastní UserManager (create superuser).“

	Event:		reprezentuje jednotlivé závody v termínovce.Každý závod má své základní údaje
			(datum,čas,vzdálenost,typ a místo konání). Je navázán na organizátora 
			pomocí ForeignKey, který zajišťuje, že závod můž vložit jen uživatel s rolí organizátora.

	Result:		uchovává výsledky běžců v jednotlivých závodech.Každý záznam propojuje jednoho
			uživatele s jedním závodem a ukládá dosažený čas a ročník kdy závod běžel.
			Díky unique_together s rokem je umožněna víceletá účast ve stejném závodě,
			aniž by docházelo k duplicitám.

	Registration:	eviduje registrace uživatelů na jednotlivé závody. Každá registrace obsahuje odkaz
			na uživatele,událost, datum registrace, a zvolenou kategorii. Vlastnost modelu 
			unique_together = ('id_user', 'id_event'), zajišťuje, že se uživatel nemůže registrovat
			na stejný závod dvakrát.


### Ukázka aplikace
	Hlavní stránka s kalendářem
	Detail akce
	Přihlášení uživatele
	Přidávání závodu (organizátor)
	Výsledková listina