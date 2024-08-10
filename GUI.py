import customtkinter as ctk
from tkinter import ttk
from match_odds import MatchOdds
from datetime import date, timedelta
import webbrowser


START = date.today()
END = date.today() + timedelta(days=1)

class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Tabs
        self.add("Filters")
        self.add("Calculator")

        for tab_name in ["Filters", "Calculator"]:
            self.tab(tab_name).grid_columnconfigure(0, weight=2)
            self.tab(tab_name).grid_rowconfigure(0, weight=2)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Arbitrage Bet Finder")
        self.geometry("1024x500")
        self.resizable(False, False)

        self.tab_view = TabView(master=self)
        self.tab_view.grid(row=0, column=5, padx=20, pady=0)

        self.button_find = ctk.CTkButton(self, text="Find Sure Bets", command=self.generate_and_load_data)
        self.button_find.grid(row=1, column=0, padx=20, pady=10)

        self.button_quit = ctk.CTkButton(self, text="Quit", command=self.quit)
        self.button_quit.grid(row=0, column=0, padx=20, pady=10)

        self.value = [["Time", "Matchup", "Profit %", "Link"]]

		# Style configuration for dark mode
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

        # Create a Treeview widget to replace CTkTable
        self.tree = ttk.Treeview(self, columns=("time", "match", "profit", "url"), show='headings')
        self.tree.heading("time", text="Time")
        self.tree.heading("match", text="Matchup")
        self.tree.heading("profit", text="Profit %")
        self.tree.heading("url", text="Link")
        self.tree.column("url", width=200)
        self.tree.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        
        # Set column widths
        self.tree.column("time", width=100,anchor='center')  
        self.tree.column("profit", width=80,anchor='center')  
        self.tree.column("match", anchor='center')  
        self.tree.column("url", width=100,anchor='center')  

        # Bind the click event to the treeview
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)
        self.tree.bind("<Motion>", self.on_mouse_move)  # Bind mouse motion event


    def generate_and_load_data(self):
        self.df = MatchOdds('football', START, START, 1, 'prematch').df
        self.load_data(self.df)
		  

    def load_data(self, df):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(row['time'], f"{row['home']} vs {row['away']}", f"{row['profit']}%", "Oddspedia Link"))


    def open_url(self, url):
        webbrowser.open(url)


    def on_tree_click(self, event):
        item = self.tree.selection()[0]  # Get selected item
        link_text = self.tree.item(item, "values")[3]  # Get the text in the link column
        if link_text == "Oddspedia Link":  # Check if the clicked link text is "Oddspedia Link"
            url = self.df.loc[self.df['home'] == self.tree.item(item, "values")[1].split(" vs ")[0], 'url'].values[0]  # Get the URL for the selected row
            webbrowser.open(url)  # Open the URL in the default web browser


    def on_mouse_move(self, event):
        """Change cursor on hover over link column."""
        region = self.tree.identify_region(event.x, event.y)
        item = self.tree.identify_row(event.y)

        if region == "cell" and item:
            column = self.tree.identify_column(event.x)
            if column == "#4":  # Check if hovering over the "Link" column
                self.tree.configure(cursor="hand2")  # Change cursor to hand
            else:
                self.tree.configure(cursor="")  # Reset cursor


    def quit(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
