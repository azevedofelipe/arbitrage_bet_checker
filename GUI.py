import customtkinter as ctk
from CTkTable import CTkTable
from match_odds import MatchOdds
from datetime import date,timedelta


START = date.today()
END = date.today() + timedelta(days=1)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Arbitrage Bet Finder")
        self.geometry("700x300")

        self.button = ctk.CTkButton(self, text="Find Sure Bets", command=self.generate_and_load_data)
        self.button.pack(pady=10)

        self.value = []

        # Create a CTkTable widget
        self.table = CTkTable(master=self,row=0, column=4,values=self.value)
        self.table.pack(pady=10)


    def generate_and_load_data(self):
        # Generate the DataFrame and then load it into the table
        df = MatchOdds('football',START,END,1,'prematch').df
        self.load_data(df)

    def load_data(self, df):

        # Insert new data into the table
        self.value = [[row['time'], f"{row['home']} vs {row['away']}", f"{row['profit']}%", row['url']] for _, row in df.iterrows()]
        self.table.update_values(self.value)


#TODO Make a quit button
#TODO Make settings screen
#TODO Make filter sidescreen, choose sports and date range
#TODO Hyperlink the url and format the table better
#TODO Calculator screen
#TODO Select start and end dates before pressing button

if __name__ == "__main__":
    app = App()
    app.mainloop()
