grammar DateParser;

// Root rule
entry: person_name COLON_SPACE date EOF;

// Name parsing rule: allows letters and spaces
person_name: NAME (SPACE NAME)*;

// Date parsing rule: YYYY-MM-DD
date: year DASH month DASH day;

// Tokens for year, month, day
year: DIGIT DIGIT DIGIT DIGIT;
month: DIGIT DIGIT?;
day: DIGIT DIGIT?;

// Lexer rules
NAME: [A-Za-z]+;
SPACE: ' ';
DASH: '-';
COLON_SPACE: ': ';
DIGIT: [0-9];
WS: [ \t\r\n]+ -> skip;  // Skipping whitespace
