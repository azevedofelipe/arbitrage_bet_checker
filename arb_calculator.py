import os

def main():
    pass

if __name__ == '__main__':
    main()
else:
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')


    def calculator(odds,bet_amount):
        unbiased_bet = {}   #Stores the amount to bet for each outcome for even profit
        
        if not bet_amount:
            bet_amount = int(input("\nEnter the amount you wish to bet on this match: "))
        print(odds)
        for odd in odds:
            bet_outputs = []
            odd_cumulative = 0
            
            # Calculates the number to divide bet_amount by
            for odd2 in odds:
                odd_cumulative += odd / odd2
            initial_bet = bet_amount/odd_cumulative
            
            bet_outputs.append(round(initial_bet,2))

            bet_outputs.append(round((initial_bet * odd) - bet_amount,2))
            unbiased_bet[odd] = bet_outputs

        return(unbiased_bet)
    
    def calculate_remaining_bets(odds):
        for x,odd in enumerate(odds,1):
            print(f"[{x}] - {odd:.2f}")
            
        odd_selected = int(input("Which odd are you betting on: "))
        odd_selected = odds[odd_selected-1]
        amount_bet = float(input(f"How much are you betting on {odd_selected}: "))

        value_multiplier = 0

        for odd1 in odds:
            value_multiplier += odd_selected / odd1
        total_bet = value_multiplier * amount_bet

        clear_terminal()
        print(f"You need to bet ${total_bet:.2f} in order to bet ${amount_bet} on {odd_selected}")
        print_calc_results(calculator(odds=odds,bet_amount=total_bet))
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
        
    def input_odds():
        odd_count = 1
        odd_input -1
        odds = []

        clear_terminal()
        print("[C] - Exit")

        while(odd_input != "C"):
            odd_input = input(f"Enter odd #{odd_count}: ").upper()
            if is_float(odd_input):
                odds.append(float(odd_input))
                rolling_count += (1/float(odd_input))
                odd_count += 1
            else:
                if odd_input != "C":
                    print("\nEnter a valid input\n")

        return odds
    
    def calculate_user_odds():
        rolling_count = 0
        odds = input_odds()

        for odd in odds:
            rolling_count += (1/float(odd))

        rolling_count = round(((1/rolling_count)-1) * 100,2)
        if(rolling_count > 0.0):
            clear_terminal()
            print(f"Odds: {*odds,}, To Profit {rolling_count}%")
            if(input("[C] - Calculate bet amount\n[R] - Return\n").upper() == "C"):
                print_calc_results(calculator(odds=odds,bet_amount=None))
        else:
            clear_terminal()
            print(f"Not a profitable bet ({rolling_count}%)")



    def print_calc_results(unbiased_bet):
        keys = list(unbiased_bet.keys())
        print("\nPlace following amount on respective odds:")
        print(f"{'Odd':<10}{'Initial Bet':<15} {'Profit':<15}")
        print('-'*50)

        for key in keys:
            print(f"{key:<10}${unbiased_bet[key][0]:<15}${unbiased_bet[key][1]:<15}")


        