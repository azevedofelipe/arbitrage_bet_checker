
def main():
    pass

if __name__ == '__main__':
    main()
else:
    def calculator(odds):
        unbiased_bet = {}   #Stores the amount to bet for each outcome for even profit
        
        bet_amount = int(input("Enter the amount you wish to bet on this match: "))
        #bias = input()

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
        