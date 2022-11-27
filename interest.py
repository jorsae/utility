import sys
import re
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
        
# TODO:
    Currently does not support ia, to 0%
    Clean up output. Have args for how output should be formatted.
    args -o for outputfile?
"""
def __main__():
    args = parse_arguments()
    print(args)

    calculate(args)

def calculate(args):
    current = args.start
    args.end, end_days = get_end(args.end)
    print(f'{args.end=} {end_days=}')
    
    operator = get_operator(args)
    print(f'{operator=}')
    
    interest_amount = get_interest_amount(args.interest_amount, args.interest_frequency)
    
    counter = 0
    total_interest = 0
    total_change = 0

    input('enter to start')
    while True:
        # calculate change/deposit/withdrawal
        if (counter % args.change_frequency == 0):
            s_current = current
            current += args.change_amount
            total_change += current - s_current
        
        # Calculate interest
        if (counter % args.interest_frequency == 0):
            s_current = current
            current *= interest_amount
            total_interest += current - s_current
        
        # Check if end is reached
        if end_days:
            if counter > args.end:
                break
        else:
            if operator(args.end, current):
                break
        print(f'{current=} | {counter=}')
        counter += 1
    print(f'{total_change=}')
    print(f'{total_interest=}')


""" ***** ARGUMENTS ***** """
# Parsing args
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', '-s', type=int, required=True, help='Start Balance')
    parser.add_argument('--end', '-e', type=str, required=True, help='End balance/days')
    parser.add_argument('--change-amount', '-ca', type=int, required=True, help='How much money is put in')
    parser.add_argument('--change-frequency', '-cf', type=int, required=True, help='How often money is put in')
    
    parser.add_argument('--interest-frequency', '-if', type=int, required=True, help='How often interest is calculated')
    parser.add_argument('--interest-amount', '-ia', type=float, required=True, help='How much interest is calculated')
    return parser.parse_args()

def get_end(end):
    end_days = True if end.endswith('d') else False
    try:
        end = re.search('\d+', end).group()
        return int(end), end_days
    except Exception as e:
        print(f'args.end error: {e}')
        sys.exit()
    print('args.end weird error.')
    sys.exit()

def end_type_is_valid(end_type):
    if end_type == 'bal' or end_type == 'days':
        return True
    return False

def get_interest_amount(ia, interest_frequency):
    return 1 + (ia / 100 / 365 * interest_frequency)

def get_operator(args):
    if args.start < args.end:
        return operator.le
    else:
        return operator.ge

if __name__ == __main__():
    main()