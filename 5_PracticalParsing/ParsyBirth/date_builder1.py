import sys
from datetime import date, datetime
from parsy import regex, seq, string, ParseError

def build_parser():
    # A name can contain letters and spaces
    name = regex("[A-Za-z ]+").desc("person's name")
    year = regex("[0-9]{4}").map(int).desc("4 digit year")
    month = regex("[0-9]{1,2}").map(int).desc("1 or 2 digit month")
    day = regex("[0-9]{1,2}").map(int).desc("1 or 2 digit day")
    dash = string("-")
    colon_space = string(": ").desc("colon and space after name")
    whitespace = regex(r"\s*")  # Optional whitespace

    # Full date parsing remains the same
    fulldate = seq(
        year=year << dash,
        month=month << dash,
        day=day,
    ).combine_dict(date)

    # Combine name and date, allow optional whitespace
    fullparser = seq(
        name=name << colon_space,
        birthdate=fulldate
    )

    return fullparser

def parse_dates():
    fullparser = build_parser()
    today = datetime.today().date()
    
    try:
        for line in sys.stdin:
            parsed_data = fullparser.parse(line.strip())
            person_name = parsed_data['name']
            birthdate = parsed_data['birthdate']
            delta = today - birthdate
            print(f"{person_name} lived {delta.days} days.")
    except ParseError as e:
        print(f"Error parsing input: {e}")

parse_dates()
