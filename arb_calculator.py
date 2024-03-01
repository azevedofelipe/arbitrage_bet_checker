
def main():
    pass

if __name__ == '__main__':
    main()
else:
    def calculator(odds):
        unbiased_bet = {}   #Stores the amount to bet for each outcome for even profit
        
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
    
    def print_calc_results(unbiased_bet):
        keys = list(unbiased_bet.keys())
        print("\nPlace following amount on respective odds:")
        print(f"{'Odd':<10}{'Initial Bet':<15}{'Profit':<15}")
        print('-'*50)

        for key in keys:
            print(f"{key:<10}{unbiased_bet[key][0]:<15}{unbiased_bet[key][1]:<15}")


        