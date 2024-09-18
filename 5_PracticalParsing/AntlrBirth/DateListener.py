import sys
from datetime import date, datetime
from antlr4 import *
from DateParserLexer import DateParserLexer
from DateParserParser import DateParserParser
from antlr4.error.Errors import ParseCancellationException

class DateListener(ParseTreeListener):
    def __init__(self):
        self.name = None
        self.year = None
        self.month = None
        self.day = None

    def exitPerson_name(self, ctx: DateParserParser.Person_nameContext):
        # Combine all parts of the name into a single string
        self.name = ' '.join(ctx.getText().split())

    def exitDate(self, ctx: DateParserParser.DateContext):
        # Extract year, month, day from the context and store them
        self.year = int(ctx.year().getText())
        self.month = int(ctx.month().getText())
        self.day = int(ctx.day().getText())

def main():
    today = datetime.today().date()

    try:
        for line in sys.stdin:
            # Create a new input stream and lexer/parser
            input_stream = InputStream(line.strip())
            lexer = DateParserLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = DateParserParser(stream)

            # Add an error listener to handle parse errors
            parser.removeErrorListeners()
            parser.addErrorListener(DiagnosticErrorListener())

            # Parse the input and walk the parse tree
            tree = parser.entry()
            listener = DateListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)

            # Calculate days from birthdate
            birthdate = date(listener.year, listener.month, listener.day)
            delta = today - birthdate
            print(f"{listener.name} lived {delta.days} days.")
    
    except ParseCancellationException as e:
        print(f"Error parsing input: {e}")

if __name__ == '__main__':
    main()

