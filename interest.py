import argparse
import operator
"""
    Arguments:
        - Start balance
        - End balance (e.g: 0 or x amount)
        - Change (Putting in x every week/month/year)
        - Change Amount (amount putting in at regular interval)
        - Interest rate (2 = 2%, 4.21 = 4.21%, etc)
        - Interest calculated (e.g: daily, weekly, monthly, etc)
        - 
"""

def __main__():
    args = parse_arguments()
    print(args)

    calculate(args)

def calculate(args):
    current = args.start
    operator = get_operator(args)
    interest_amount = get_interest_amount(args.interest_amount, args.interest_frequency)
    
    counter = 0
    total_interest = 0
    total_change = 0
    while operator(current, args.end):
        # calculate change/deposit/withdrawal
        if (counter % args.change_frequency == 0):
            s_current = current
            current += args.change_amount
            total_change += current - s_current
        
        if (counter % args.interest_frequency == 0):
            s_current = current
            current *= interest_amount
            total_interest += current - s_current
            print(current - s_current)
        
        print(f'{current} | {counter=}')
        counter += 1
    print(total_change)
    print(total_interest)


""" ***** ARGUMENTS ***** """
# Parsing args
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', '-s', type=int, required=True, help='Start Balance')
    parser.add_argument('--end', '-e', type=int, required=True, help='End balance')
    parser.add_argument('--change-amount', '-ca', type=int, required=True, help='How much money is put in')
    parser.add_argument('--change-frequency', '-cf', type=int, required=True, help='How often money is put in')
    
    parser.add_argument('--interest-frequency', '-if', type=int, required=True, help='How often interest is calculated')
    parser.add_argument('--interest-amount', '-ia', type=float, required=True, help='How much interest is calculated')
    
    return parser.parse_args()

def get_interest_amount(ia, interest_frequency):
    return 1 + (ia / 100 / 365 * interest_frequency)

def get_operator(args):
    if args.start < args.end:
        return operator.le
    else:
        return operator.ge

if __name__ == __main__():
    main()