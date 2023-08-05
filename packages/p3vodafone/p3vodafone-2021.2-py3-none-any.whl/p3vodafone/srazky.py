#!/usr/bin/env python3

import datetime
import math
import os
import sqlite3
import tkinter
import traceback
from functools import wraps
from sqlite3.dbapi2 import Connection
from time import time
from tkinter import messagebox, filedialog
from typing import Optional, Union, Dict, Set, List, Iterable, Tuple

import pandas as pd
import pkg_resources
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from p3vodafone.sendmail import mail_statement

SQL_PEOPLE_INSERT = "INSERT INTO people (personal_nr, name, email, organization) VALUES (?, ?, ?, ?)"
SQL_PEOPLE_UPDATE = "UPDATE people SET name = ?, email = ?, organization = ? WHERE personal_nr = ?"
SQL_PEOPLE_DELETE = "DELETE FROM people WHERE personal_nr = ?"

SQL_PHONES_INSERT = "INSERT INTO phone_numbers (phone, datapack, people_id) VALUES (?, ?, ?)"
SQL_PHONES_UPDATE = "UPDATE phone_numbers SET datapack = ?, people_id = ? WHERE phone = ?"
SQL_PHONES_DELETE = "DELETE FROM phone_numbers WHERE phone = ?"

SQL_SELECT_TOTAL = "SELECT people.personal_nr, people.name, people.email, people.organization, totals.total_base, " \
                   "totals.total_vat FROM people LEFT JOIN totals ON people.personal_nr = totals.people_id WHERE " \
                   "totals.invoice_number_id = ? AND totals.people_id = ? "

SQL_SELECT_DEDUCTION_ITEMS = 'SELECT phone_numbers.phone, deductions.recipient, ' \
                             'deductions.item_description, deductions.product_description, deductions.price_base, deductions.price_vat FROM people LEFT JOIN ' \
                             'phone_numbers ON people.personal_nr = phone_numbers.people_id LEFT JOIN deductions ON ' \
                             'phone_numbers.phone = deductions.phone_id WHERE deductions.invoice_number = ? AND ' \
                             'people.personal_nr = ? AND deductions.price_deduction > 0'


class DeductionItem:
    def __init__(
            self,
            bill_phone_id: int,
            action_timestamp: str,
            invoice_id: int,
            other_party_phone: Optional[str],
            original_price: float,
            original_price_with_vat: float,
            deduction_price: float,
            product_description: str,
            item_description: str,
    ):
        self.phone_id: int = bill_phone_id
        self.action_timestamp: str = action_timestamp
        self.other_party_phone: Optional[str] = other_party_phone
        self.original_price: float = original_price
        self.original_price_with_vat: float = original_price_with_vat
        self.deduction_price: float = deduction_price
        self.invoice_id: int = invoice_id
        self.product_description: str = product_description
        self.item_description: str = item_description

    def as_list(self):
        return (
            self.phone_id,
            self.product_description,
            self.item_description,
            self.action_timestamp,
            self.other_party_phone,
            round(self.original_price, 2),
            round(self.original_price_with_vat, 2),
            round(self.deduction_price, 2),
            self.invoice_id,
        )

    def set_deducted_price(self, new_deducted_price_with_vat: float):
        self.deduction_price = new_deducted_price_with_vat
        if new_deducted_price_with_vat > 0:
            self.original_price = round(new_deducted_price_with_vat * 0.827, 2)
            self.original_price_with_vat = new_deducted_price_with_vat


def timeit(func):
    """
    :param func: Decorated function
    :return: Execution time for the decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f'{func.__name__} executed in {end - start:.4f} seconds')
        return result

    return wrapper


@timeit
def init_database(
        connection: Connection
) -> None:
    with connection:
        cursor = connection.cursor()
        cursor.executescript('''CREATE TABLE IF NOT EXISTS people (
                    personal_nr INTEGER NOT NULL PRIMARY KEY UNIQUE,
                    name VARCHAR,
                    email VARCHAR,
                    organization VARCHAR);
                    
                    CREATE TABLE IF NOT EXISTS phone_numbers (
                    phone INTEGER NOT NULL PRIMARY KEY UNIQUE,
                    datapack NUMERIC,
                    people_id INTEGER);
                    
                    CREATE TABLE IF NOT EXISTS deductions (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    phone_id INTEGER,
                    item_description TEXT,
                    product_description TEXT,
                    event_date TEXT,
                    recipient INTEGER,
                    price_base INTEGER,
                    price_vat INTEGER,
                    price_deduction INTEGER,
                    invoice_number INTEGER);
                    
                    CREATE TABLE IF NOT EXISTS totals (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    people_id INTEGER,
                    invoice_number_id INTEGER,
                    total_base INTEGER,
                    total_vat INTEGER);
                    
                    CREATE TABLE IF NOT EXISTS history (
                    invoice_number INTEGER NOT NULL PRIMARY KEY UNIQUE,
                    from_date INTEGER,
                    to_date INTEGER,
                    timesgenerated INTEGER DEFAULT 0);
                    
                    CREATE TABLE IF NOT EXISTS item (
                    item INTEGER NOT NULL PRIMARY KEY UNIQUE,
                    item_descr TEXT)''')


@timeit
def set_pdf_font(font_name: str = "Timess", font_file: str = "TIMESS__.ttf") -> bool:
    """

    :param font_name:
    :param font_file:
    :return: zda se povedlo font registrovat, chyba je v konzoli
    """
    font_path: Optional[str] = None
    # Attempt 1
    try:
        if not font_path:
            font_path = pkg_resources.resource_filename(
                pkg_resources.Requirement.parse('p3vodafone'),
                os.path.join("p3vodafone", font_file)
            )
    except:
        traceback.print_exc()
    # Attempt 2
    try:
        if not font_path:
            font_path = pkg_resources.resource_filename(
                "p3vodafone",
                font_file
            )
    except:
        traceback.print_exc()
    # Attempt 3
    try:
        if not font_path:
            font_path = os.path.join(os.getcwd(), "fonts", font_file)
    except:
        traceback.print_exc()

    # load font into pdfmetrics
    try:
        print(f"Font {font_name} from path {font_file}")
        if font_path:
            pdfmetrics.registerFont(
                TTFont(
                    name=font_name,
                    filename=font_path
                )
            )
            return True
    except ValueError:
        traceback.print_exc()
        pass
    return False


@timeit
def ask_user_yesno(title: str, text: str, respond_immediately: Optional[bool] = None) -> bool:
    if respond_immediately is not None:
        return bool(respond_immediately)
    # hide the extra window shown with dialog
    tkinter.Tk().withdraw()
    return messagebox.askyesno(title=title, message=text)


@timeit
def show_notice(text: str, title: str) -> None:
    messagebox.showinfo(
        title=title,
        message=text
    )


@timeit
def ask_user_filepath(text: str, default: str = None, allow_excel: bool = False, allow_xml: bool = False) -> str:
    file_filter = []
    if allow_excel:
        file_filter.append(('Excel', '*.xlsx'))
    if allow_xml:
        file_filter.append(('Soubory XML', '*.xml'))
    if not os.path.exists(default):
        print(f"ask_user_filepath default={default} neexistuje")
        default = None
    # hide the extra window shown with dialog
    tkinter.Tk().withdraw()
    return filedialog.askopenfilename(
        title=text,
        filetypes=file_filter,
        initialdir=os.path.dirname(default) if default else os.getcwd(),
        initialfile=os.path.basename(default) if default else None
    )


def get_row_by_id(rows: List[sqlite3.Row], index, index_column: int = 0) -> Optional[sqlite3.Row]:
    for row in rows:
        if row[index_column] == index:
            return row
    return None


def normalize_phone_number(original: Union[int, str], expected_prefix: str = "420") -> int:
    original = str(original)
    if not original[0:len(expected_prefix)] == expected_prefix:
        return int(f"{expected_prefix}{original}")
    return int(original)


@timeit
def get_indexed_rows_dict(rows: List[sqlite3.Row], index_column: int = 0) -> Dict[int, sqlite3.Row]:
    rtn = {}
    for row in rows:
        rtn[row[index_column]] = row
    return rtn


@timeit
def update_zamestnanci(connection: Connection, xls_zamestnanci: str = None) -> Tuple[Dict[int, str], Dict[int, int]]:
    """

    :type connection: Connection
    :type xls_zamestnanci: str
    :param xls_zamestnanci:
    :param connection:
    :return: (phone -> datapack a phone -> email dicts)
    """
    # klíč(telefonní číslo) => hodnota(název povoleného datového balíčku)
    datapack: Dict[int, str] = {}
    # klíč(telefonní číslo ve formátu 420123456789) => hodnota(people.personal_nr)
    phone_to_people: Dict[int, int] = {}
    with connection:
        cur = connection.cursor()
        cur.row_factory = sqlite3.Row
        cur.execute('SELECT * FROM people')
        # klíč(personální číslo) => hodnota(celý řádek z tabulky people)
        known_people: Dict[int, sqlite3.Row] = get_indexed_rows_dict(cur.fetchall())

        cur.execute('SELECT * FROM phone_numbers')
        # klíč(telefonní číslo ve formátu 420123456789) => hodnota(celý řádek z tabulky phone_numbers)
        known_phones: Dict[int, sqlite3.Row] = get_indexed_rows_dict(cur.fetchall())

        # Pokud jsou v databázi telefonní čísla bez nastaveného povoleného datapack
        has_missing_datapacks: bool = False

        # create datapack and phone_to_email from db
        # must run before next user prompt
        for phone_number in known_phones:
            phone_row = known_phones[phone_number]
            for personal_nr in known_people:
                if personal_nr == phone_row['people_id']:
                    people_row = known_people[personal_nr]
                    datapack[phone_number] = phone_row['datapack']
                    phone_to_people[phone_number] = int(people_row['personal_nr'])
                    has_missing_datapacks = has_missing_datapacks or not phone_row['datapack']

        if known_people or has_missing_datapacks:
            question = "Chcete aktualizovat databázi zaměstnanců?"
            if not ask_user_yesno(title=question, text=question, respond_immediately=None):
                return datapack, phone_to_people

        xls_people: str = xls_zamestnanci if os.path.isfile(xls_zamestnanci) else ask_user_filepath(
            text="Vyberte prosím soubor se seznamem zaměstnanců",
            default=xls_zamestnanci,
            allow_xml=False,
            allow_excel=True,
        )

        if not xls_people or not os.path.exists(xls_people):
            print("Soubor se seznamem zaměstnanců nebyl vybrán, pokračuji bez aktualizace")
            return datapack, phone_to_people

        current_employee_ids = list()
        current_phone_numbers = list()

        employeelist = pd.read_excel(io=xls_people)
        for row in employeelist.itertuples():
            # (
            #   excel_row_id,
            #   0:employee_nr, 1:employee name, 2:email, 3:phone_number, 4:organization,
            #   5:allowed data pack, 6:flat_or_fallback, 7:price
            # )
            row = list(row)
            # delete excel row number
            del row[0]
            # skip rows without valid employee nr
            if math.isnan(row[0]) or row[0] < 1:
                continue
            # get current row
            _id = int(row[0])
            _name = row[1]
            _mail = row[2]
            _phone_number = normalize_phone_number(row[3])
            _org = row[4]
            _datapack = row[5]

            matching_row = known_people.get(_id, None)
            matching_phone = known_phones.get(_phone_number, None)

            current_employee_ids.append(_id)
            current_phone_numbers.append(_phone_number)

            datapack[_phone_number] = row[5]
            phone_to_people[_phone_number] = _id

            # CREATE employee
            if not matching_row:
                sql_values = (
                    _id, _name, _mail, _phone_number,
                )
                print(f"Employee does not exist, INSERT: {sql_values}")
                cur.execute(SQL_PEOPLE_INSERT, sql_values)
                matching_row = sqlite3.Row(cur, sql_values)
                known_people[_id] = matching_row

            # UPDATE employee
            if (
                    _name != matching_row[1] or
                    _mail != matching_row[2] or
                    _org != matching_row[3]
            ):
                sql_values = (
                    _name, _mail, _org, _id
                )
                print(f"Employee not up-to-date, UPDATE: {sql_values} over {list(matching_row)}")
                cur.execute(SQL_PEOPLE_UPDATE, sql_values)

            # CREATE phone number
            if not matching_phone:
                sql_values = (
                    _phone_number, _datapack, _id
                )
                print(f"Phone does not exist, INSERT: {sql_values}")
                cur.execute(SQL_PHONES_INSERT, sql_values)
                matching_phone = sqlite3.Row(cur, sql_values)
                known_phones[_phone_number] = matching_phone

            # UPDATE phone number if phone to employee nr is not valid or if datapack is not up-to-date
            if (
                    matching_phone[2] != _id or
                    matching_phone[1] != _datapack
            ):
                sql_values = (
                    _datapack, _id, _phone_number
                )
                print(f"Phone not up-to-date, UPDATE {sql_values} over {list(matching_phone)}")
                cur.execute(SQL_PHONES_UPDATE, sql_values)

        employees_to_remove: Set[int] = known_people.keys() - current_employee_ids
        if employees_to_remove:
            print(f"Will delete employees with these IDS: {employees_to_remove}")
            cur.execute("DELETE FROM people WHERE personal_nr IN (%s)" % ",".join(map(str, employees_to_remove)))

        phone_numbers_to_remove: Set[int] = known_phones.keys() - current_phone_numbers
        if phone_numbers_to_remove:
            print(f"Will delete these phone numbers: {phone_numbers_to_remove}")
            cur.execute("DELETE FROM phone_numbers WHERE phone IN (%s)" % ",".join(map(str, phone_numbers_to_remove)))

        return datapack, phone_to_people


def create_vyuctovani_pdf(connection: Connection, output_filepath: str, thismonth: str, thisyear: str,
                          invoice_number: int, statement_total: list, font: str = "Timess"):
    with connection:
        cur = connection.cursor()

        cislo_vyuctovani = f"{thismonth}-{thisyear}-{str(statement_total[0])}"
        canvas = Canvas(output_filepath)
        # hlavicka vyuctovani
        canvas.setFont(font, 10)
        canvas.drawString(420, 620, "Základ daně Kč")
        canvas.drawString(520, 620, "Celkem Kč")
        canvas.drawString(440, 650, "Vystaveno:")
        # udaje o vyuctovani
        canvas.setFont(font, 9)
        canvas.drawString(25, 605, "Přeúčtování mobilních služeb")
        canvas.drawString(25, 590, f"{thismonth}-{thisyear}".encode())
        canvas.drawString(420, 605, str(statement_total[4]).encode())  # bez DPH
        canvas.drawString(520, 605, str(statement_total[5]).encode())  # s DPH
        dnes = datetime.date.today()
        canvas.drawString(520, 650, str(dnes))
        canvas.line(25, 615, 575, 615)
        canvas.line(25, 585, 575, 585)
        #    canvas.line(25,415,575,415)
        canvas.drawString(25, 535,
                          "Za data platíte podle vnitřní směrnice. Za vyšší datový balíček, než na jaký máte nárok, "
                          "platíte část, o níž nárok převyšuje.")
        canvas.setLineWidth(3)
        # hlavicka faktury
        canvas.line(25, 810, 575, 810)
        canvas.rect(300, 680, 270, 100, stroke=1, fill=0)
        canvas.setFont(font, 14)
        canvas.drawString(25, 815, "Individuální vyúčtování")
        canvas.drawString(475, 815, cislo_vyuctovani.encode())  # cislo vyuctovani
        canvas.drawString(35, 740, str(statement_total[3]).encode())  # organization
        canvas.drawString(355, 740, str(statement_total[1]).encode())  # name
        # rozpis polozek
        canvas.drawString(25, 550, "Rozpis položek")
        cur.execute(SQL_SELECT_DEDUCTION_ITEMS, (invoice_number, statement_total[0]))
        individual_items = cur.fetchall()  # list of tuples
        xcoord = 25
        ycoord = 500
        canvas.setFont(font, 9)
        canvas.drawString(xcoord, ycoord, "Telefonní číslo")
        canvas.drawString(xcoord + 60, ycoord, "Příjemce hovoru")  # prijemce
        canvas.drawString(xcoord + 160, ycoord, "Produkt")  # produkt
        canvas.drawString(xcoord + 250, ycoord, "Položka produktu")  # polozka produktu
        canvas.drawString(xcoord + 430, ycoord, "Cena bez DPH")  # bez DPH
        canvas.drawString(xcoord + 500, ycoord, "Cena vč. DPH")  # s DPH
        canvas.setFont(font, 8)
        for record in individual_items:
            canvas.drawString(xcoord, ycoord - 15, str(record[0]).encode())  # telefonni cislo
            canvas.drawString(xcoord + 60, ycoord - 15, str(record[1]).encode())  # prijemce
            canvas.drawString(xcoord + 160, ycoord - 15, str(record[2]).encode())  # produkt
            canvas.drawString(xcoord + 250, ycoord - 15, str(record[3]).encode())  # polozka produktu
            canvas.drawString(xcoord + 430, ycoord - 15, str(record[4]).encode())  # bez DPH
            canvas.drawString(xcoord + 500, ycoord - 15, str(record[5]).encode())  # s DPH
            ycoord = ycoord - 20
        canvas.setFont(font, 14)
        canvas.drawString(320, 20, "Celkem srážka ze mzdy:")
        canvas.drawString(520, 20, f"{str(statement_total[5])} Kč".encode())  # s DPH
        canvas.save()


@timeit
def create_excel_report(connection: Connection, target_directory: str, invoice_number: int, month_number: int):
    with connection:
        cur = connection.cursor()

        cur.execute('SELECT from_date FROM history WHERE invoice_number = ?', (invoice_number,))
        current_from = cur.fetchone()[0]
        current_year = current_from[0:4]
        current_month = current_from[5:7]

        filename: str = f"srážky_{current_month}_{current_year}.xlsx"

        export_select = 'SELECT people.personal_nr, people.name, totals.total_vat FROM people LEFT JOIN totals ON ' \
                        'people.personal_nr = totals.people_id WHERE totals.invoice_number_id = ? ORDER BY people.name '
        cur.execute(export_select, (invoice_number,))
        export = cur.fetchall()
        df = pd.DataFrame(export, columns=['os. číslo', 'jméno', 'srážka (Kč)'])
        df.to_excel(os.path.join(target_directory, filename), index=False)
        print(f"Soubor {filename} byl vytvořen")


@timeit
def generate_invoices_and_send_emails(connection: Connection, invoice_number: int,
                                      pdf_output_directory: str = None, really_send: bool = True):
    with connection:
        cur = connection.cursor()
        cur.execute('UPDATE history SET timesgenerated = timesgenerated + 1 WHERE invoice_number = ?',
                    (invoice_number,))

        cur.execute('SELECT from_date FROM history WHERE invoice_number = ?', (invoice_number,))
        current_from = cur.fetchone()[0]
        current_year = current_from[0:4]
        current_month = current_from[5:7]

        # pre-create output directory
        os.makedirs(os.path.join(pdf_output_directory, f"{current_month}_{current_year}"), exist_ok=True)

        cur.execute('SELECT personal_nr FROM people')
        everyone = cur.fetchall()
        for each in everyone:
            cur.execute(SQL_SELECT_TOTAL, (invoice_number, each[0]))
            statement_total = cur.fetchone()
            if not statement_total:
                continue
            statement_total = list(statement_total)
            attach_file_name = f"{statement_total[0]}_vyuctovani_{current_month}_{current_year}.pdf"
            attach_file_name = os.path.join(pdf_output_directory, f"{current_month}_{current_year}", attach_file_name)
            to_address = statement_total[2]

            create_vyuctovani_pdf(
                output_filepath=attach_file_name,
                connection=connection,
                thismonth=current_month,
                thisyear=current_year,
                invoice_number=invoice_number,
                statement_total=statement_total,
            )

            if not really_send:
                continue

            mail_statement(
                target_email=to_address,
                source_email="vyuctovani-vodafone@praha3.cz",
                mail_server_host="mailp3c.praha3.cz",
                mail_server_port=25,
                email_text="Nejaky\nDlouhy\nText\nna\nvice\nřádkách",
                email_subject="Vyúčtování telefonu [Praha 3 - Vodafone]",
                attach_file_name_absolute_path=attach_file_name
            )


def get_datapack_amount_from_string(
        datapack_description: str
) -> float:
    try:
        return float(''.join(x for x in datapack_description if x.isdigit() or x in [',', '.']).replace(',', '.'))
    except ValueError:
        return 0


def get_valid_float(
        unknown_data: any
) -> float:
    return float(str(unknown_data).replace(',', '.'))


@timeit
def get_deduction_items_for_insert(
        original: Dict[int, List[DeductionItem]]
) -> Iterable:
    values = []
    for phone_number in original:
        for deduction_item in original[phone_number]:
            values.append(deduction_item.as_list())
    return values


def parse_timestamp(_item_timestamp: Optional[str]) -> float:
    try:
        return datetime.datetime.strptime(_item_timestamp, "%d.%m.%Y %H:%M:%S").timestamp()
    except ValueError:
        return 0


def get_deduction_totals(
        deductions: Dict[int, List[DeductionItem]],
        filter_zero: bool,
        invoice_number: int,
        phone_to_employee_id: Dict[int, int]
) -> Iterable:
    values = []
    for phone_number in deductions:
        if not phone_to_employee_id.get(phone_number, None):
            continue
        total = 0
        total_vat = 0
        for deduction_item in deductions[phone_number]:
            if deduction_item.deduction_price > 0:
                total = total + deduction_item.original_price
                total_vat = total_vat + deduction_item.original_price_with_vat
        if filter_zero and total_vat <= 0:
            # skip zero items if set
            continue
        values.append((phone_to_employee_id.get(phone_number), invoice_number, round(total, 0), round(total_vat, 0)))
    return values


@timeit
def parse_xls_faktura(
        connection: Connection,
        xls_faktura: str,
        allowed_datapacks: Dict[int, str],
        phone_to_employee_id: Dict[int, int],
        max_tarif_price_per_employee: int,
        sheet_name: str = 'Rozpis používání služeb',
) -> Tuple[Optional[int], Optional[str]]:
    if not xls_faktura or not os.path.isfile(xls_faktura):
        xls_faktura = ask_user_filepath(
            allow_xml=False,
            allow_excel=True,
            default=xls_faktura,
            text="Vyberte prosím soubor s vyúčtováním Vodafone (Excel)"
        )
    if not xls_faktura:
        return None, None

    invoice_number: int = 0
    invoice_from_datetime: float = time()
    invoice_to_datetime: float = 0

    # klíč(phone id) => hodnota(DeductionItem struct)
    deductions: Dict[int, List[DeductionItem]] = {}
    # klíč(phone number) => hodnota(zda už byla položka hrazená zaměstnavatelem zpracována)
    used_allowed_datapack: Dict[int, bool] = {}

    excel_data = pd.read_excel(io=xls_faktura, sheet_name=sheet_name)
    for excel_row in excel_data.itertuples():
        invoice_number = excel_row[1]

        if not invoice_number:
            invoice_number = excel_row[1]
        elif invoice_number != excel_row[1]:
            show_notice(
                title="Chyba zpracování",
                text="Vyúčtování obsahuje řádky pro více než jednu fakturaci"
            )
            break

        _billed_phone = excel_row[2]
        _item_product = excel_row[5]
        _item_description = excel_row[7]
        _item_timestamp = excel_row[8]
        # phone number, "data" or empty
        _other_party_phone = excel_row[9]
        _item_price_without_vat = get_valid_float(excel_row[16])
        _item_price_with_vat = get_valid_float(excel_row[17])

        if _item_price_with_vat <= 0 or _item_price_without_vat <= 0:
            # skip items that did not get billed
            continue

        _allowed_datapack = allowed_datapacks.get(_billed_phone, None)
        _deduction_item = DeductionItem(
            bill_phone_id=_billed_phone,
            other_party_phone=_other_party_phone,
            invoice_id=invoice_number,
            action_timestamp=_item_timestamp,
            original_price=_item_price_without_vat,
            original_price_with_vat=_item_price_with_vat,
            deduction_price=_item_price_with_vat,
            product_description=_item_product,
            item_description=_item_description
        )

        if _other_party_phone == 'data' and not used_allowed_datapack.get(_billed_phone, False):
            _allowed_datapack_size = get_datapack_amount_from_string(_allowed_datapack) if _allowed_datapack else 0
            _this_datapack_size = get_datapack_amount_from_string(_item_description)
            if (
                    _item_price_with_vat <= get_valid_float(max_tarif_price_per_employee) or
                    (
                            math.isclose(_allowed_datapack_size, _this_datapack_size, rel_tol=1e-3) and
                            _allowed_datapack_size > 0 and
                            _this_datapack_size > 0
                    )
            ):
                used_allowed_datapack[_billed_phone] = True
                if math.isclose(_allowed_datapack_size, _this_datapack_size, rel_tol=1e-3):
                    _deduction_item.set_deducted_price(0)
                else:
                    calc_deduction = _item_price_with_vat - get_valid_float(max_tarif_price_per_employee)
                    if calc_deduction > 0:
                        print(
                            f"A calc deduction:: {_deduction_item.__dict__} allowed {_allowed_datapack_size} this {_this_datapack_size}")
                    _deduction_item.set_deducted_price(calc_deduction if calc_deduction > 0 else 0)
                    print(
                        f"A {_billed_phone} {_allowed_datapack_size} is-NOT-close {_this_datapack_size} with {calc_deduction}")
            else:
                # odečíst od výše nákladu max. cenu za data, kterou zaměstnavatel platí
                calc_deduction = _item_price_with_vat - get_valid_float(max_tarif_price_per_employee)
                if calc_deduction > 0:
                    print(
                        f"B calc deduction:: {_deduction_item.__dict__} allowed {_allowed_datapack_size} this {_this_datapack_size}")
                _deduction_item.set_deducted_price(calc_deduction if calc_deduction > 0 else 0)
                print(
                    f"B {_billed_phone} {_allowed_datapack_size} is-NOT-close {_this_datapack_size} with {calc_deduction}")

                # update in-memory
        _tmp_deductions = deductions.get(_billed_phone, list())
        _tmp_deductions.append(_deduction_item)
        deductions[_billed_phone] = _tmp_deductions

        # update invoice from/to
        _item_timestamp_datetime = parse_timestamp(_item_timestamp)
        if _item_timestamp_datetime:
            if _item_timestamp_datetime > invoice_to_datetime:
                invoice_to_datetime = _item_timestamp_datetime
            elif _item_timestamp_datetime < invoice_from_datetime:
                invoice_from_datetime = _item_timestamp_datetime

    with connection:
        cur = connection.cursor()
        # insert all deduction items
        cur.execute("DELETE FROM deductions WHERE invoice_number = ?", (invoice_number,))
        cur.executemany(
            "INSERT INTO deductions (phone_id, item_description, product_description, event_date, recipient, price_base, "
            "price_vat, price_deduction, invoice_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            get_deduction_items_for_insert(deductions)
        )
        # insert all total deductions
        cur.execute("DELETE FROM totals WHERE invoice_number_id = ?", (invoice_number,))
        cur.executemany(
            "INSERT INTO totals (people_id, invoice_number_id, total_base, total_vat)"
            "VALUES (?, ?, ?, ?)",
            get_deduction_totals(
                deductions=deductions,
                filter_zero=True,
                invoice_number=invoice_number,
                phone_to_employee_id=phone_to_employee_id
            )
        )
        cur.execute("SELECT * FROM history WHERE invoice_number = ?", (invoice_number,))
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO history (invoice_number, from_date, to_date, timesgenerated) VALUES (?, ?, ?, 0)",
                (
                    invoice_number,
                    str(datetime.datetime.fromtimestamp(invoice_from_datetime)),
                    str(datetime.datetime.fromtimestamp(invoice_to_datetime))
                )
            )

    return invoice_number, str(datetime.datetime.fromtimestamp(invoice_from_datetime))[5:7]


@timeit
def srazky(sqlite_path: str,
           xls_zamestnanci: str,
           xls_faktura: str,
           output_directory: str,
           max_data_price_per_employee: int
           ) -> None:
    set_pdf_font()

    with sqlite3.connect(sqlite_path) as db_conn:
        cur = db_conn.cursor()
        init_database(connection=db_conn)

        datapack_dict, phone_to_people_nr = update_zamestnanci(
            connection=db_conn,
            xls_zamestnanci=xls_zamestnanci
        )

        invoice_number, invoice_month = parse_xls_faktura(
            connection=db_conn,
            xls_faktura=xls_faktura,
            allowed_datapacks=datapack_dict,
            max_tarif_price_per_employee=max_data_price_per_employee,
            phone_to_employee_id=phone_to_people_nr
        )

        if not invoice_number:
            show_notice(
                title="Načtení vyúčtování Vodafone se nezdařilo",
                text="Vybraný Excel neobsahuje očekávaná data nebo list Rozpis používání služeb"
            )
            return

        create_excel_report(
            connection=db_conn,
            invoice_number=invoice_number,
            target_directory=output_directory,
            month_number=int(invoice_month)
        )

        # update history table timesgenerated - first check if we have generated anything at all
        cur.execute('SELECT timesgenerated FROM history WHERE invoice_number = ?', (invoice_number,))
        timesgenerated = cur.fetchone()

        if not ask_user_yesno(title='Data se úspěšně nahrála',
                              text='Chcete vytvořit vyúčtování za poslední měsíc a rozeslat je všem zaměstnancům?',
                              respond_immediately=None):
            return

        if (timesgenerated and timesgenerated[0] > 0) or ask_user_yesno(
                title='Opravdu znovu rozeslat vyúčtování zaměstnancům?',
                text='Vyuctovani za tuto fakturu uz se v minulosti generovala a rozesilala zamestnancum. Skutecne '
                     'si prejete je vygenerovat a rozeslat znovu?',
                respond_immediately=None
        ):
            really_send: bool = False
            ask_user_yesno(
                title="Chcete odesílat e-maily?",
                text="Vyberte NE pokud chcete jen vygenerovat faktury\nVyberte ANO pokud chcete faktury i odeslat "
                     "příslušným zaměstnancům ",
                respond_immediately=None
            )
            generate_invoices_and_send_emails(
                pdf_output_directory=output_directory,
                invoice_number=invoice_number,
                connection=db_conn,
                really_send=really_send
            )
