import sys
import re
import argparse
import operator
"""
    Arguments:
        - Start balance
        - End balance (e.g: 0 or x amount)
        - Contribution (Putting in x every week/month/year)
        - Contribution Amount (amount putting in at regular interval)
        - Interest rate (2 = 2%, 4.21 = 4.21%, etc)
        - Interest calculated (e.g: daily, weekly, monthly, etc)
        - Output string
        - Output frequency (how often to print output string)

         Calculate time

            A = Accrued amount (principal + interest)
            P = Principal amount
            r = Annual nominal interest rate as a decimal
            R = Annual nominal interest rate as a percent
            r = R/100
            n = number of compounding periods per unit of time
            t = time in decimal years; e.g., 6 months is calculated as 0.5 years. Divide your partial year number of months by 12 to get the decimal years.
            I = Interest amount
            ln = natural logarithm, used in formulas below


            Solve for t
            ln is the natural logarithm
            t = ln(A/P) / n(ln(1 + r/n)), then also
            t = (ln(A) - ln(P)) / n(ln(1 + r/n))
"""

def __main__():
    args = parse_arguments()
    print_arguments(args)

    calculate(args)

def calculate(args):
    total = args.start
    args.end, end_days = get_end(args.end)
    operator = get_operator(args)
    
    interest_amount = get_interest_amount(args.interest_amount, args.interest_frequency)
    
    day = 0
    total_interest = 0
    total_contributions = 0

    while True:
        # calculate change/deposit/withdrawal
        if (day % args.contribution_frequency == 0) and day != 0:
            s_current = total
            total += args.contribution_amount
            total_contributions += total - s_current
        
        # Calculate interest
        if (day % args.interest_frequency == 0) and day != 0:
            s_current = total
            total *= interest_amount
            total_interest += total - s_current
        
        # Check if end is reached
        if end_days:
            if day > args.end:
                break
        else:
            if operator(args.end, total):
                break
        
        # Check if need to print output
        if (day % args.output_frequency == 0) and day != 0:
            print(get_output(args.output, total, total_contributions, total_interest, day))
        day += 1
    
    o = get_output(args.output, total, total_contributions, total_interest, day)
    print(o)
    print('-'*30)
    print('Finished Results:')
    print_recap(args, day, total, total_interest, total_contributions)


""" ***** ARGUMENTS ***** """
# Parsing args
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', '-s', type=int, required=True, help='Start Balance')
    parser.add_argument('--end', '-e', type=str, required=True, help='End balance/days')
    parser.add_argument('--contribution-amount', '-ca', type=int, required=True, help='How much money is put in')
    parser.add_argument('--contribution-frequency', '-cf', type=int, required=True, help='How often money is put in')
    
    parser.add_argument('--interest-amount', '-ia', type=float, required=True, help='How much interest is calculated')
    parser.add_argument('--interest-frequency', '-if', type=int, required=True, help='How often interest is calculated')

    parser.add_argument('--output', '-o', type=str, default='[%d] Total: %t\tContributions: %c\tInterest: %i\t', help='Output format string')
    parser.add_argument('--output-frequency', '-of', type=int, default=1, help='How often to print output')
    return parser.parse_args()

def print_recap(args, day, total, total_interest, total_contributions):
    if args.start > total:
        total_interest_percent = abs(total_interest / args.start * 100)
    else:
        total_interest_percent = abs(total_interest / total * 100)
    contribution_interest = abs(total_interest / total_contributions * 100)
    
    print(get_time_passed(day))
    print(f'Interest of total: {round(total_interest_percent, 2)}%')
    print(f'Interest of contributions: {round(contribution_interest, 2)}%')

def get_time_passed(day):
    years = day // 365
    months = (day - (years * 365)) // 30
    days = (day - (years * 365) - (months * 30))
    output = ''

    if years:
        output += f'{years} years, '
    if months:
        output += f'{months} months, '
    if days:
        output += f'{days} days'
    return output

def print_arguments(args):
    end, end_days = get_end(args.end)
    if end_days:
        print(f'Starting with ${args.start:,} for {end:,} days')
    else:
        print(f'Starting with ${args.start:,} till reaching ${end:,}')
    print(f'Contributing ${args.contribution_amount:,}, every {args.contribution_frequency} days')
    print(f'Interest: {args.interest_amount}%, calculated every {args.interest_frequency} days at {get_interest_amount(args.interest_amount, args.interest_frequency)}x')
    print('-'*30)

def get_output(output, total, contributions, interest, day):
    out = output
    out = out.replace('%d', str(day))
    
    total = f'${round(total, 2):,}'
    out = out.replace('%t', total)
    
    contributions = f'${round(contributions, 2):,}'
    out = out.replace('%c', contributions)
    
    interest = f'${round(interest, 2):,}'
    out = out.replace('%i', interest)
    return out

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