
def main():
    pass

if __name__ == '__main__':
    main()
else:
    def calculator(odds,bet_amount):
        unbiased_bet = {}   #Stores the amount to bet for each outcome for even profit
        
        if not bet_amount:
            bet_amount = int(input("\nEnter the amount you wish to bet on this match: "))

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
        amount_bet = float(input("How much are you betting on {odd_selected:.2f}: "))

        for odd1 in odds:
            value_multiplier = odd_selected / odd1
        total_bet = value_multiplier * amount_bet

        print(f"You need to bet ${total_bet} in order to bet ${amount_bet} on {odd_selected}")
        print_calc_results(calculator(odds=odds,bet_amount=total_bet))
                




    def print_calc_results(unbiased_bet):
        keys = list(unbiased_bet.keys())
        print("\nPlace following amount on respective odds:")
        print(f"{'Odd':<10}{'Initial Bet':<15}{'Profit':<15}")
        print('-'*50)

        for key in keys:
            print(f"{key:<10}{unbiased_bet[key][0]:<15}{unbiased_bet[key][1]:<15}")


        