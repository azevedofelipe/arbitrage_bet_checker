import CTkSpinbox.ctkspinbox
import customtkinter as ctk
from tkinter import ttk
from match_odds import MatchOdds
import webbrowser
import pandas as pd
from CTkSpinbox import CTkSpinbox
from settings import Settings, REGIONS
from arb_calculator import calculate


class FilterTab(ctk.CTkFrame):
    def __init__(self, settings, master, **kwargs):
        super().__init__(master, **kwargs)
        self.settings = settings.load()


        self.label_days = ctk.CTkLabel(self, text="Days:")
        self.label_days.grid(row=0, column=0,padx=10, sticky='w')
        self.days_var = ctk.IntVar()
        self.days_filter = CTkSpinbox(self,start_value=self.settings.days_scan,min_value=1,max_value=30,scroll_value=1,variable=self.days_var,height=30,width=70,font=('Arial',11))
        self.days_filter.grid(row=0,column=1,pady=10,padx=10,sticky='e')

        self.label_profit = ctk.CTkLabel(self, text="Profit %:")
        self.label_profit.grid(row=1, column=0,pady=10,padx=10,sticky='w')
        self.profit_var = ctk.IntVar()
        self.profit_filter = CTkSpinbox(self,start_value=self.settings.floor_profit,min_value=0,max_value=100,scroll_value=1,variable=self.profit_var,height=30,width=70,font=('Arial',11))
        self.profit_filter.grid(row=1,column=1,pady=10,padx=10,sticky='e')

        self.label_refresh = ctk.CTkLabel(self, text="Refresh Rate:")
        self.label_refresh.grid(row=2, column=0,pady=10,padx=10, sticky='w')
        self.combo_refresh = ctk.CTkComboBox(self,values=['30','60','120','300','600','1800'],width=70)
        self.combo_refresh.grid(row=2, column=1,pady=10,padx=10,sticky='e')
        self.combo_refresh.set(self.settings.refresh_time)

        self.label_region = ctk.CTkLabel(self, text="Region:")
        self.label_region.grid(row=3, column=0,pady=10,padx=10, sticky='w')
        self.combo_region = ctk.CTkComboBox(self,values=list(REGIONS.keys()),width=70)
        self.combo_region.set(self.settings.region[0])
        self.combo_region.grid(row=3, column=1,pady=10,padx=10,sticky='e')

        self.button_apply = ctk.CTkButton(self, text="Apply", command=self.apply_filters,width=80)
        self.button_apply.grid(row=4, column=0, pady=10,columnspan=2)

    def apply_filters(self):
        self.settings.days_scan = self.days_var.get()
        self.settings.floor_profit = self.profit_var.get()
        self.settings.region = (self.combo_region.get(), REGIONS[self.combo_region.get()])
        self.settings.save()


class CalculatorTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.label_odd = ctk.CTkLabel(self, text="Total Bet:",width=90)
        self.label_odd.grid(row=0, column=0,columnspan=2)
        self.bet_amount = ctk.CTkEntry(self,width=90)
        self.bet_amount.configure(justify='center')
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

        self.button_new = ctk.CTkButton(self, text="Calculate", command=self.calculate,width=90)
        self.button_new.grid(row=7, column=0, padx=10, pady=10,columnspan=2)

    def create_entry_fields(self):
        # Create two new entry fields
        row = len(self.entry_fields) + 3  # Calculate the next row based on the current number of entry fields
        entry_odd = ctk.CTkEntry(self,width=90)
        entry_amount = ctk.CTkLabel(self,width=90,text='')

        entry_odd.configure(justify='center')
        entry_amount.configure(justify='center')

        entry_odd.grid(row=row, column=0,sticky='n',padx=10,pady=4)
        entry_amount.grid(row=row, column=1,sticky='n',padx=10,pady=4)

        # Store the entry fields in the list
        self.entry_fields.append((entry_odd, entry_amount))


    def calculate(self):
        odds = [float(field[0].get()) for field in self.entry_fields if field[0].get() != '']
        bet_amount = float(self.bet_amount.get())
        returns = calculate(odds,bet_amount)

        if self.entry_fields[0][0].get() == '':
            self.label_profit.configure(text='')
            self.entry_fields[0][1].configure(text='')
            return

        for field in self.entry_fields:

            if field[0].get() == '':
                field[1].configure(text='')
                continue

            field[1].configure(text=returns[float(field[0].get())][0])
            profit = returns[float(field[0].get())][1]
            
            if profit > 0:
                color = 'green'
            else:
                color = 'red'

            self.label_profit.configure(text=f'Profit: $ {profit}', text_color = color)



class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Filters")
        self.add("Calculator")

        for tab_name in ["Filters", "Calculator"]:
            self.tab(tab_name).grid_columnconfigure(0, weight=1)
            self.tab(tab_name).grid_rowconfigure(0, weight=1)

        self.calculator_tab = CalculatorTab(master=self.tab("Calculator"),width=70)
        self.calculator_tab.grid(row=0, column=0, pady=20)

        self.filter_tab = FilterTab(Settings,master=self.tab("Filters"),width=70)
        self.filter_tab.grid(row=0,column=0,pady=20)


class TreeViewFrame(ctk.CTkFrame):
    def __init__(self, master, df, generate_and_load_data_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.df = df

        
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
        
        self.match_count = ctk.CTkLabel(self, text = '')
        self.match_count.grid(row=0,column=0,padx=20,pady=10,sticky='w')

        self.tree = ttk.Treeview(self, columns=("bookies", "profit", "url"), show='headings')
        self.tree.heading("bookies", text="Bookmakers")
        self.tree.heading("profit", text="Profit %")
        self.tree.heading("url", text="Link")

        
        self.tree.column("profit", width=80,anchor='center')  
        self.tree.column("bookies", anchor='center')  
        self.tree.column("url", width=100,anchor='center')  

        self.tree.grid(row=1,column=0,padx=20, pady=10, sticky='nsew')

        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)
        self.tree.bind("<Motion>", self.on_mouse_move)

        self.button_find = ctk.CTkButton(self, text="Find Sure Bets", command=generate_and_load_data_callback, width=100, height=30)
        self.button_find.grid(row=2,column=0, pady=10)

    def load_data(self, df):
        self.df = df

        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, row in self.df.iterrows():
            self.tree.insert("", "end",iid=idx,values=(f"{', '.join(row['bookies'])}", f"{row['profit']}%", "Link"))

        self.match_count.configure(text=f'Matches Found: {len(self.df)}')

    def on_tree_click(self, event):
        if self.tree.identify_column(event.x) == "#3":
            item_id = int(self.tree.selection()[0])
            url = self.df.loc[item_id,'url']
            webbrowser.open(url)

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
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.df = None

        self.tab_view_frame = TabView(master=self,width=70)
        self.tab_view_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        self.tree_view_frame = TreeViewFrame(master=self, df=pd.DataFrame(columns=["time", "home", "away", "profit", "url"]),generate_and_load_data_callback=self.generate_and_load_data)
        self.tree_view_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        # Load data onstart, disabled for now
        # self.after(600, self.generate_and_load_data)

    def generate_and_load_data(self):
        self.tree_view_frame.option_clear()
        self.settings = Settings.load()
        self.odds = MatchOdds(self.settings)
        self.df = self.odds.df
        self.tree_view_frame.load_data(self.df)



if __name__ == "__main__":
    app = App()
    app.mainloop()
