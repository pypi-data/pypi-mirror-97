# Vyúčtování Vodafone - Praha 3

Projekt pro zpracování fakturace od Vodafone proti interní evidenci zaměstanců, tarifů a limitů.
Načte soubor se zaměstnanci a jejich telefonními čísly, projede fakturu a vyhodnotí, co kdo má zaplatit.
Vyjede sjetinu se srážkami pro personální a vyúčtování pro jednotlivé zaměstnance, které jim pošle na email.

## Vstupní soubory

- Seznam zaměstnanců (např. "seznam-lidi.xlsx")
- Vodafone vyúčtování (např. "report_xls_12345_123456789_202011.xlsx")

Příklady souborů jsou ve složce **example_data**

- seznam lidí může obsahovat jak zaměstnance tak telefonní čísla, která jsou například v technickém vybavení (EZS, parkovací automat, atp.)
- vyúčtování v repozitáři, neobsahuje všechny listy, ale jen pro ukázku, co tato aplikace očekává, samotný report z Vodafone nemusíte před použitím nijak upravovat

## Výstupní soubory

- "srazky_{rok}_mesic.xls" - seznam zaměstnanců, jejich osobních čísel a výše srážky za daný měsíc
- "{os. číslo zaměstnance}_vyuctovani_{mesic}_{rok}.pdf" - rozúčtování srážek, vč. seznamu jednotlivých služeb

Výstup se tvoří v rámci vybraného adresáře pro výstupy, PDF vyúčtování se tvoří v pod-složce "{mesic}_{rok}", soubor srážek pak přímo v adresáři pro výstupy

## Diagnostická data

- SQLite Databáze, která obsahuje jednotlivé položky, vč. originální výše účtovaného nákladu od Vodafone a příp. rozdílné výše srážky z platu
- Pokud aplikaci spouštíte v terminálu, diagnostické logy, např. časování jednotlivých metod nebo zajímavé detaily z jednotlivých funkcí

Výchozí pracovní adresář je v aplikačních datech uživatelského profilu (Linux: `~/.config/P3Vodafone`, Windows: `AppData/Local/P3Vodafone`), zde se také udržuje soubor s nastavením `p3vodafone.ini` a databáze `telefonie.sqlite`,
pokud uživatel chce, může zde vyúžívat i před-vytvořené adresáře pro vstupní soubory a složku pro výstupy, tj. `outputs`

## Instalace

### Produkční instalace

Pokud chcete provozovat na Windows, nainstalujte si poslední Python 3.x vydání z [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
```
# instalace
pip install p3vodafone
# spuštění
vyuctovani-vodafone
```

### Testování / Vývoj

```
git clone https://gitlab.com/otevrenamesta/praha3/vyuctovani-vodafone.git
cd vyuctovani-vodafone
python3 -m p3vodafone.user_interface
```
