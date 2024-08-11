import CTkSpinbox.ctkspinbox
import customtkinter as ctk
from tkinter import ttk
from match_odds import MatchOdds
from datetime import date, timedelta
import webbrowser
import pandas as pd
from CTkSpinbox import CTkSpinbox

START = date.today()
END = date.today() + timedelta(days=1)


class FilterTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        custom_font = ctk.CTkFont(size=11)  # Change 12 to your desired font size


        self.label_odd = ctk.CTkLabel(self, text="Days:")
        self.label_odd.grid(row=0, column=0,sticky='n',padx=20)

        spin_var = ctk.IntVar()
        self.days_filter = CTkSpinbox(self,start_value=1,min_value=0,max_value=10,scroll_value=1,variable=spin_var,height=30,width=70,font=custom_font)
        self.days_filter.grid(row=0,column=1)


class CalculatorTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        

        self.label_odd = ctk.CTkLabel(self, text="Odd")
        self.label_odd.grid(row=0, column=0,sticky='n')

        self.label_amount = ctk.CTkLabel(self, text="Amount")
        self.label_amount.grid(row=0, column=1,sticky='n')


        self.entry_fields = []


        for _ in range(3):
            self.create_entry_fields() 

        self.button_subtract = ctk.CTkButton(self, text="New Odd", command=self.create_entry_fields)
        self.button_subtract.grid(row=8, column=0, padx=10, pady=10)

    def create_entry_fields(self):
        # Create two new entry fields
        row = len(self.entry_fields) + 1  # Calculate the next row based on the current number of entry fields
        entry_odd = ctk.CTkEntry(self)
        entry_amount = ctk.CTkEntry(self)

        entry_odd.grid(row=row, column=0,pady=10)
        entry_amount.grid(row=row, column=1,pady=10)

        # Store the entry fields in the list
        self.entry_fields.append((entry_odd, entry_amount))


class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Filters")
        self.add("Calculator")

        for tab_name in ["Filters", "Calculator"]:
            self.tab(tab_name).grid_columnconfigure(0, weight=2)
            self.tab(tab_name).grid_rowconfigure(0, weight=2)

        self.calculator_tab = CalculatorTab(master=self.tab("Calculator"))
        self.calculator_tab.grid(row=0, column=0, padx=20, pady=20)

        self.filter_tab = FilterTab(master=self.tab("Filters"))
        self.filter_tab.grid(row=0,column=0,padx=20,pady=20)


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

        self.tree = ttk.Treeview(self, columns=("time", "match", "profit", "url"), show='headings')
        self.tree.heading("time", text="Time")
        self.tree.heading("match", text="Matchup")
        self.tree.heading("profit", text="Profit %")
        self.tree.heading("url", text="Link")

        
        self.tree.column("time", width=100,anchor='center')  
        self.tree.column("profit", width=80,anchor='center')  
        self.tree.column("match", anchor='center')  
        self.tree.column("url", width=100,anchor='center')  

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)
        self.tree.bind("<Motion>", self.on_mouse_move)

        self.button_find = ctk.CTkButton(self, text="Find Sure Bets", command=generate_and_load_data_callback, width=100, height=30)
        self.button_find.pack(pady=10)

    def load_data(self, df):
        self.df = df

        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, row in self.df.iterrows():
            self.tree.insert("", "end",iid=idx,values=(row['time'], f"{row['home']} vs {row['away']}", f"{row['profit']}%", "Link"))

    def on_tree_click(self, event):
        if self.tree.identify_column(event.x) == "#4":
            item_id = int(self.tree.selection()[0])
            url = self.df.loc[item_id,'url']
            webbrowser.open(url)

    def on_mouse_move(self, event):
        region = self.tree.identify_region(event.x, event.y)
        item = self.tree.identify_row(event.y)
        if region == "cell" and item:
            column = self.tree.identify_column(event.x)
            if column == "#4":
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

        self.tab_view_frame = TabView(master=self)
        self.tab_view_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.tree_view_frame = TreeViewFrame(master=self, df=pd.DataFrame(columns=["time", "home", "away", "profit", "url"]),generate_and_load_data_callback=self.generate_and_load_data)
        self.tree_view_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        # Load data onstart, disabled for now
        # self.after(100, self.generate_and_load_data)

    def generate_and_load_data(self):
        self.tree_view_frame.option_clear()
        self.df = MatchOdds('football', START, START, 1, 'prematch').df
        self.tree_view_frame.load_data(self.df)



if __name__ == "__main__":
    app = App()
    app.mainloop()
