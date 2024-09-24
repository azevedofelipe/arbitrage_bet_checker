import CTkSpinbox.ctkspinbox
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from match_odds import MatchOdds
import webbrowser
from CTkSpinbox import CTkSpinbox
from settings import Settings, REGIONS
from arb_calculator import calculate, get_profit, calc_total_bet_needed, calculate_profit
from utils.utils import get_region_bookmakers


class FilterTab(ctk.CTkFrame):
    def __init__(self, settings, master, **kwargs):
        super().__init__(master, **kwargs)
        self.settings = settings.load()


        self.label_days = ctk.CTkLabel(self, text="Days:")
        self.label_days.grid(row=0, column=0,padx=10, sticky='w')
        self.days_var = ctk.IntVar()
        self.days_filter = CTkSpinbox(self,start_value=self.settings.days_scan,min_value=1,max_value=30,scroll_value=1,variable=self.days_var,height=30,width=70,font=('Arial',11))
        self.days_filter.grid(row=0,column=1,pady=(0,10),padx=10,sticky='e')

        self.label_profit = ctk.CTkLabel(self, text="Min. Profit %:")
        self.label_profit.grid(row=1, column=0,pady=(0,10),padx=10,sticky='w')
        self.profit_var = ctk.IntVar()
        self.profit_filter = CTkSpinbox(self,start_value=self.settings.floor_profit,min_value=0,max_value=100,scroll_value=1,variable=self.profit_var,height=30,width=70,font=('Arial',11))
        self.profit_filter.grid(row=1,column=1,pady=(0,10),padx=10,sticky='e')

        self.label_region = ctk.CTkLabel(self, text="Region:")
        self.label_region.grid(row=3, column=0,pady=(0,10),padx=10, sticky='w')
        self.combo_region = ctk.CTkComboBox(self,values=list(REGIONS.keys()),width=90)
        self.combo_region.set(self.settings.region[0])
        self.combo_region.grid(row=3, column=1,pady=(0,10),padx=10,sticky='e')

        self.label_bookies = ctk.CTkLabel(self, text="Bookmakers:")
        self.label_bookies.grid(row=4, column=0,pady=(10,0), padx=10, sticky='w')
        self.bookies = Bookies(self,settings=self.settings,height=50)
        self.bookies._scrollbar.configure(height=100)
        self.bookies.grid(row=5,column=0,columnspan=2,padx=10,pady=(0,10))

        self.button_apply = ctk.CTkButton(self, text="Apply", command=self.apply_filters,width=80)
        self.button_apply.grid(row=6, column=0, columnspan=2)

    def apply_filters(self):
        region = self.combo_region.get()

        self.settings.days_scan = self.days_var.get()
        self.settings.floor_profit = self.profit_var.get()

        if self.settings.region[0] != region:
            self.settings.region = (region, REGIONS[region])
            self.settings.bookmakers = get_region_bookmakers(REGIONS[region])
            self.settings.save()
            self.bookies.reset_items()
        else: 
            self.settings.bookmakers = self.bookies.list_items()

        self.settings.save()


class Bookies(ctk.CTkScrollableFrame):
    def __init__(self,master, settings, **kwargs):
        super().__init__(master,**kwargs)

        self.checkbox_list = []
        self.settings = settings
        self.item_list = settings.bookmakers
        self.add_items()


    def add_items(self):
        for item, value in self.item_list.items():
            var = tk.BooleanVar(value=value)
            checkbox = ctk.CTkCheckBox(self, text=item,variable=var, checkbox_width=15, checkbox_height=15, width=150)
            checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10))
            self.checkbox_list.append(checkbox)

    def list_items(self) -> dict:
        items = {item.cget("text"): item.cget("variable").get() for item in self.checkbox_list}
        return items

    def reset_items(self):
        self.settings.load() 
        self.item_list = self.settings.bookmakers

        for item in self.checkbox_list:
            item.destroy()

        self.checkbox_list.clear()
        self.add_items() 


class CalculatorTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.settings = master.master.settings

        self.label_odd = ctk.CTkLabel(self, text="Total Bet:",width=90)
        self.label_odd.grid(row=0, column=0,columnspan=2)
        self.bet_amount = ctk.CTkEntry(self,width=90)
        self.bet_amount.configure(justify='center')
        self.bet_amount.insert(-1,self.settings.bet_amount)
        self.bet_amount.grid(row=1, column=0,pady=5,columnspan=2)

        self.label_odd = ctk.CTkLabel(self, text="Odd",width=90)
        self.label_odd.grid(row=2, column=0,sticky='s')

        self.label_amount = ctk.CTkLabel(self, text="$ Bet",width=90)
        self.label_amount.grid(row=2, column=1,sticky='s')


        self.entry_fields = []


        for _ in range(3):
            self.create_entry_fields() 

        self.label_profit = ctk.CTkLabel(self, text="", width=90)
        self.label_profit.grid(row=6, column=0,columnspan=2)

        self.button_new = ctk.CTkButton(self, text="Calculate", command=self.calculate_odds,width=90)
        self.button_new.grid(row=7, column=1, padx=10, pady=10,columnspan=1)

        self.button_clear = ctk.CTkButton(self, text="Clear", command=self.clear,width=90)
        self.button_clear.grid(row=7, column=0, padx=10, pady=10,columnspan=1)

    def create_entry_fields(self):
        # Create two new entry fields
        row = len(self.entry_fields) + 3  # Calculate the next row based on the current number of entry fields
        entry_odd = ctk.CTkEntry(self,width=90)
        entry_amount = ctk.CTkLabel(self,width=90,text='-')

        entry_odd.configure(justify='center')
        entry_amount.configure(justify='center')

        entry_odd.grid(row=row, column=0,sticky='n',padx=10,pady=4)
        entry_amount.grid(row=row, column=1,sticky='n',padx=10,pady=4)

        # Store the entry fields in the list
        self.entry_fields.append((entry_odd, entry_amount))


    def calculate_odds(self):
        odds = [float(field[0].get().replace(',','.')) for field in self.entry_fields if field[0].get() != '']
        bet_amount = float(self.bet_amount.get().replace(',','.'))
        self.settings.bet_amount = bet_amount
        self.settings.save()

        returns = calculate(odds,bet_amount)
        profit_perc = get_profit(odds)

        if self.entry_fields[0][0].get() == '':
            self.label_profit.configure(text='')
            self.entry_fields[0][1].configure(text='-')
            return

        for field in self.entry_fields:
            if field[0].get() == '':
                field[1].configure(text='-')
                continue

            odd = float(field[0].get().replace(',','.'))

            field[1].configure(text=returns[odd][0])
            profit = calculate_profit(returns[odd], odd, bet_amount)
            
            if profit > 0:
                color = 'green'
            else:
                color = 'red'

            self.label_profit.configure(text=f'Profit: $ {profit}  ( {profit_perc}% )', text_color = color)
    

    def clear(self):
        self.label_profit.configure(text='')

        for field in self.entry_fields:
            field[0].delete(0,'end')
            field[1].configure(text='-')


    def calc_match_odds(self,odds):
        self.clear()

        for odd, entry in zip(odds,self.entry_fields):
            entry[0].insert(-1,odd['value'])

        if self.bet_amount.get() != '':
            self.calculate_odds()


class TabView(ctk.CTkTabview):
    def __init__(self, master, settings, **kwargs):
        super().__init__(master, **kwargs)
        self.settings = settings

        self.add("Filters")
        self.add("Calculator")

        for tab_name in ["Filters", "Calculator"]:
            self.tab(tab_name).grid_columnconfigure(0, weight=1)
            self.tab(tab_name).grid_rowconfigure(0, weight=1)

        self.calculator_tab = CalculatorTab(master=self.tab("Calculator"), width=100,height=200)
        self.calculator_tab.grid(row=0, column=0, pady=(10,10))

        self.filter_tab = FilterTab(Settings,master=self.tab("Filters"),width=100, height=200)
        self.filter_tab.grid(row=0,column=0,pady=(10,10))


class TreeViewFrame(ctk.CTkFrame):
    def __init__(self, master, generate_and_load_data_callback, tabs, **kwargs):
        super().__init__(master, **kwargs)
        self.tabs = tabs
        self.calculator_tab = tabs.calculator_tab

        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2e2e2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#2e2e2e",
                        font=('Calibri', 10))
        style.configure("Treeview.Heading", 
                        background="#333333",
                        foreground="white",
                        font=('Calibri', 11))
        style.map('Treeview', 
                  background=[('selected', '#4a4a4a')])
        

        self.tree = ttk.Treeview(self, columns=("bookies", "profit", "url","calculate"), show='headings')
        self.tree.heading("bookies", text="Bookmakers")
        self.tree.heading("profit", text="Profit %")
        self.tree.heading("url", text="Link")
        self.tree.heading("calculate", text="Calculate")

        
        self.tree.column("bookies", width=250, anchor='center')  
        self.tree.column("profit", width=100, anchor='center')  
        self.tree.column("url", width=150,anchor='center')  
        self.tree.column("calculate", width=150,anchor='center')  

        self.tree.grid(row=0,column=0,padx=10, pady=10, sticky='nsew')

        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)
        self.tree.bind("<Motion>", self.on_mouse_move)

        self.match_count = ctk.CTkLabel(self, text = '')
        self.match_count.grid(row=1,column=0,padx=20)
        self.blacklist_count = ctk.CTkLabel(self, text = '')
        self.blacklist_count.grid(row=2,column=0,padx=20)

        self.button_find = ctk.CTkButton(self, text="Find Sure Bets", command=generate_and_load_data_callback, width=100, height=30)
        self.button_find.grid(row=3,column=0, pady=(0,10))

    def load_data(self, df, blacklisted):
        self.df = df
        self.blacklisted = blacklisted

        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, row in self.df.iterrows():
            self.tree.insert("", "end",iid=idx,values=(f"{', '.join(row['bookies'])}", f"{row['profit']}%", "Link", "Calculate"))

        self.match_count.configure(text=f'Sure Bets Found: {len(self.df)}')

        blacklist_text = ''
        if len(self.blacklisted) > 0:
            blacklist_text = f'Blacklisted Matches: {len(self.blacklisted)} '

        self.blacklist_count.configure(text=blacklist_text)

    def on_tree_click(self, event):
        if self.tree.identify_column(event.x) == "#3":
            item_id = int(self.tree.selection()[0])
            url = self.df.loc[item_id,'url']
            webbrowser.open(url)

        if self.tree.identify_column(event.x) == "#4":
            item_id = int(self.tree.selection()[0])
            odds = self.df.loc[item_id,'odds']
            self.tabs.set('Calculator')
            self.calculator_tab.calc_match_odds(odds)


    def on_mouse_move(self, event):
        region = self.tree.identify_region(event.x, event.y)
        item = self.tree.identify_row(event.y)
        if region == "cell" and item:
            column = self.tree.identify_column(event.x)
            if column == "#3":
                self.tree.configure(cursor="hand2")
            else:
                self.tree.configure(cursor="")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Arbitrage Bet Finder")
        self.geometry("1024x500")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.df = None
        self.settings = Settings.load()

        self.tab_view_frame = TabView(master=self,settings=self.settings, width=70)
        self.tab_view_frame.grid(row=0, column=1, padx=15, pady=10, sticky="nsew")

        self.tree_view_frame = TreeViewFrame(master=self, generate_and_load_data_callback=self.generate_and_load_data, tabs = self.tab_view_frame)
        self.tree_view_frame.grid(row=0, column=0, padx=0, pady=30, sticky="ns")

        # Load matches on start
        # self.after(600, self.generate_and_load_data)

    def generate_and_load_data(self):
        self.tree_view_frame.option_clear()
        self.settings = Settings.load()
        self.odds = MatchOdds(self.settings)
        self.tree_view_frame.load_data(self.odds.df, self.odds.blacklisted_df)



if __name__ == "__main__":
    app = App()
    app.mainloop()
