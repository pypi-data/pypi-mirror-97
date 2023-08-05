#!/usr/bin/env python3
import os
from tkinter import Tk, Frame, RAISED, BOTH, X, Label, Button, Entry, LEFT, StringVar, filedialog, RIGHT
from typing import Optional

import profig
from appdirs import user_config_dir

from p3vodafone.srazky import srazky, ask_user_filepath, show_notice


class MainWindow(Frame):
    KEY_XLS_LIDI: str = "lidi.xls"
    KEY_XLS_FAKTURA: str = "faktura.xls"
    KEY_XML_FAKTURA: str = "faktura.xml"
    KEY_XLS_SRAZKY: str = "srazky.xls"
    KEY_DB_PATH: str = "db.path"
    KEY_OUT_PATH: str = "output.path"
    KEY_MAX_EMPLOYEE_PRICE: str = "lidi.max_employee_price"

    def __init__(self, master=None):
        super().__init__(master)

        self.config_filename: str = "p3vodafone.ini"
        self.config_location: str = user_config_dir(appname="P3Vodafone", appauthor="OtevrenaMesta")
        self.config: profig.Config = profig.Config(os.path.join(self.config_location, self.config_filename))

        self.load_settings()

        self.xls_lidi_entry: Optional[StringVar] = StringVar(value=self.config[self.KEY_XLS_LIDI])
        self.xml_faktura_entry: Optional[StringVar] = StringVar(value=self.config[self.KEY_XML_FAKTURA])
        self.xls_faktura_entry: Optional[StringVar] = StringVar(value=self.config[self.KEY_XLS_FAKTURA])
        self.output_dir_entry: Optional[StringVar] = StringVar(value=self.config[self.KEY_OUT_PATH])
        self.db_path_entry: Optional[StringVar] = StringVar(value=self.config[self.KEY_DB_PATH])
        self.max_employee_price: Optional[StringVar] = StringVar(value=self.config[self.KEY_MAX_EMPLOYEE_PRICE])

        os.makedirs(self.output_dir_entry.get(), exist_ok=True)
        os.makedirs(os.path.join(self.config_location, "data"), exist_ok=True)

        self.show_ui()

    def load_settings(self):
        self.config.init(self.KEY_XLS_LIDI, os.path.join(self.config_location, "data", "lidi.xlsx"))
        self.config.init(self.KEY_XLS_FAKTURA, os.path.join(self.config_location, "data", "faktura.xlsx"))
        self.config.init(self.KEY_XML_FAKTURA, os.path.join(self.config_location, "data", "faktura.xml"))
        self.config.init(self.KEY_OUT_PATH, os.path.join(self.config_location, "output"))
        self.config.init(self.KEY_DB_PATH, os.path.join(self.config_location, "telefonie.sqlite"))
        self.config.init(self.KEY_XLS_SRAZKY, os.path.join(self.config_location, "data", "srazky.xlsx"))
        self.config.init(self.KEY_MAX_EMPLOYEE_PRICE, 220)
        self.config.sync()

    @staticmethod
    def add_input_pane(
            label: str,
            callback: Optional[callable],
            button_label: Optional[str],
            parent: Frame,
            input_content: StringVar
    ) -> Entry:
        frame_pane: Frame = Frame(parent)
        frame_pane.pack(fill=X)
        label_xml: Label = Label(frame_pane, text=label)
        label_xml.pack(side=LEFT, padx=5, pady=5)

        frame_input_button: Frame = Frame(parent)
        frame_input_button.pack(fill=X)
        entry_xml: Entry = Entry(frame_input_button, textvariable=input_content)
        entry_xml.pack(fill=X, padx=5, pady=5)
        if button_label and callback:
            choose_xml: Button = Button(frame_input_button, text=button_label, command=callback)
            choose_xml.pack(side=RIGHT, padx=5, pady=5)
        return entry_xml

    def select_faktura_xml(self):
        path: str = ask_user_filepath(
            text="Vyberte XML soubor Faktury",
            allow_xml=True,
            allow_excel=False,
            default=self.xml_faktura_entry.get()
        )
        if path:
            self.xml_faktura_entry.set(path)
            self.config[self.KEY_XML_FAKTURA] = path
            self.config.sync()

    def select_faktura_xls(self):
        path: str = ask_user_filepath(
            text="Vyberte soubor Faktury (Excel)",
            allow_xml=False,
            allow_excel=True,
            default=self.xls_faktura_entry.get()
        )
        if path:
            self.xls_faktura_entry.set(path)
            self.config[self.KEY_XLS_FAKTURA] = path
            self.config.sync()

    def select_lidi_xls(self):
        path: str = ask_user_filepath(
            text="Vyberte soubor Zaměstnanci (Excel)",
            allow_xml=False,
            allow_excel=True,
            default=self.xls_lidi_entry.get()
        )
        if path:
            self.xls_lidi_entry.set(path)
            self.config[self.KEY_XLS_LIDI] = path
            self.config.sync()

    def select_output_dir(self):
        path: str = filedialog.askdirectory(
            title="Vyberte adresář",
            initialdir=self.output_dir_entry.get(),
        )
        if path:
            self.output_dir_entry.set(path)
            self.config[self.KEY_OUT_PATH] = path
            self.config.sync()

    def select_db_file(self):
        path: str = filedialog.askopenfilename(
            text="Vyberte soubor databáze",
            filetypes=[("SQLite databáze", "*.sqlite")],
            initialdir=self.output_dir_entry.get(),
            initialfile=self.db_path_entry.get(),
        )
        if path:
            self.output_dir_entry.set(path)
            self.config[self.KEY_DB_PATH] = path
            self.config.sync()

    def check_run_conditions(self) -> bool:
        if not self.output_dir_entry.get():
            print("Chybí adresář pro PDF soubory")
            return False
        if not self.db_path_entry.get():
            print("Chybí cesta k databázi")
            return False

        return True

    def run(self):
        if self.check_run_conditions():
            srazky(
                xls_faktura=self.xls_faktura_entry.get(),
                xls_zamestnanci=self.xls_lidi_entry.get(),
                output_directory=self.output_dir_entry.get(),
                sqlite_path=self.db_path_entry.get(),
                max_data_price_per_employee=self.max_employee_price.get()
            )
            show_notice(
                title="Hotovo !",
                text="Hotovo !"
            )
        else:
            show_notice(
                title="Nejsou vyplněny všechny požadované položky",
                text="Vyberte příslušné soubory a znovu použijte tlačítko 'Spustit'"
            )

    def show_ui(self):
        self.pack(fill=BOTH, expand=True)

        frame: Frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        self.add_input_pane(callback=self.select_faktura_xls,
                            label="Vodafone Faktura (Excel)",
                            button_label="Vybrat soubor",
                            parent=frame,
                            input_content=self.xls_faktura_entry)

        self.add_input_pane(callback=self.select_lidi_xls,
                            label="Seznam zaměstnanců (Excel)",
                            button_label="Vybrat soubor",
                            parent=frame,
                            input_content=self.xls_lidi_entry)

        self.add_input_pane(callback=self.select_output_dir,
                            label="Adresář pro vygenerované faktury a přehled srážek",
                            button_label="Vybrat adresář",
                            parent=frame,
                            input_content=self.output_dir_entry)

        self.add_input_pane(callback=None,
                            label="Aktuální cena nejvyššího datového balíčku (10 GB)",
                            button_label=None,
                            parent=frame,
                            input_content=self.max_employee_price)

        button = Button(self, text="Spustit", command=self.run)
        button.pack(fill=BOTH)


def gui():
    window: Tk = Tk()
    window.title("Vyúčtování Vodafone")
    window.minsize(width=800, height=400)
    window.wm_protocol(name="WM_DELETE_WINDOW", func=window.quit)
    MainWindow(window)
    window.mainloop()


if __name__ == "__main__":
    gui()
