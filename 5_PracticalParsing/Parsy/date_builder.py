import sys
from datetime import date
from parsy import regex, seq, string, ParseError

def build_parser():
    year = regex("[0-9]{4}").map(int).desc("4 digit year")
    # Allow one or two digits for month and day
    month = regex("[0-9]{1,2}").map(int).desc("1 or 2 digit month")
    day = regex("[0-9]{1,2}").map(int).desc("1 or 2 digit day")
    dash = string("-")

    fulldate = seq(
        year=year << dash,
        month=month << dash,
        day=day,
    ).combine_dict(date)

    return fulldate

def parse_dates():
    fulldate = build_parser()
    try:
        for line in sys.stdin:
            parsed_date = fulldate.parse(line.strip())
            today = date.today()
            delta = today - parsed_date
            print(f"Parsed Date: {parsed_date}, Days until today: {delta.days}")
    except ParseError as e:
        print(f"Parse error: {e}")

parse_dates()
