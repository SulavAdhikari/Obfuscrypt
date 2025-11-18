lexer grammar PythonLexer;

options {
    superClass = PythonLexerBase;
}

// Keywords
tokens {
    INDENT,
    DEDENT
}

// All your existing token definitions from the parser file should be moved here
DEF      : 'def';
RETURN   : 'return';
RAISE    : 'raise';
FROM     : 'from';
IMPORT   : 'import';
NONLOCAL : 'nonlocal';
AS       : 'as';
GLOBAL   : 'global';
ASSERT   : 'assert';
IF       : 'if';
ELIF     : 'elif';
ELSE     : 'else';
WHILE    : 'while';
FOR      : 'for';
IN       : 'in';
TRY      : 'try';
NONE     : 'None';
FINALLY  : 'finally';
WITH     : 'with';
EXCEPT   : 'except';
LAMBDA   : 'lambda';
OR       : 'or';
AND      : 'and';
NOT      : 'not';
IS       : 'is';
CLASS    : 'class';
YIELD    : 'yield';
DEL      : 'del';
PASS     : 'pass';
CONTINUE : 'continue';
BREAK    : 'break';
ASYNC    : 'async';
AWAIT    : 'await';
PRINT    : 'print';
EXEC     : 'exec';
TRUE     : 'True';
FALSE    : 'False';

// Operators
DOT                : '.';
ELLIPSIS           : '...';
REVERSE_QUOTE      : '`';
STAR               : '*';
COMMA              : ',';
COLON              : ':';
SEMI_COLON         : ';';
POWER              : '**';
ASSIGN             : '=';
OR_OP              : '|';
XOR                : '^';
AND_OP             : '&';
LEFT_SHIFT         : '<<';
RIGHT_SHIFT        : '>>';
ADD                : '+';
MINUS              : '-';
DIV                : '/';
MOD                : '%';
IDIV               : '//';
NOT_OP             : '~';
LESS_THAN          : '<';
GREATER_THAN       : '>';
EQUALS             : '==';
GT_EQ              : '>=';
LT_EQ              : '<=';
NOT_EQ_1           : '<>';
NOT_EQ_2           : '!=';
AT                 : '@';
ARROW              : '->';
ADD_ASSIGN         : '+=';
SUB_ASSIGN         : '-=';
MULT_ASSIGN        : '*=';
AT_ASSIGN          : '@=';
DIV_ASSIGN         : '/=';
MOD_ASSIGN         : '%=';
AND_ASSIGN         : '&=';
OR_ASSIGN          : '|=';
XOR_ASSIGN         : '^=';
LEFT_SHIFT_ASSIGN  : '<<=';
RIGHT_SHIFT_ASSIGN : '>>=';
POWER_ASSIGN       : '**=';
IDIV_ASSIGN        : '//=';

// Delimiters
OPEN_PAREN    : '(' {self.IncIndentLevel()};
CLOSE_PAREN   : ')' {self.DecIndentLevel()};
OPEN_BRACE    : '{' {self.IncIndentLevel()};
CLOSE_BRACE   : '}' {self.DecIndentLevel()};
OPEN_BRACKET  : '[' {self.IncIndentLevel()};
CLOSE_BRACKET : ']' {self.DecIndentLevel()};

// Basic tokens
NAME: ID_START ID_CONTINUE*;

STRING: STRING_PREFIX? (SHORT_STRING | LONG_STRING);

// NUMBER
//     : INTEGER
//     | FLOAT_NUMBER
//     | IMAG_NUMBER
//     ;

// INTEGER
//     : DECIMAL_INTEGER
//     | OCT_INTEGER
//     | HEX_INTEGER
//     | BIN_INTEGER
//     ;

DECIMAL_INTEGER : NON_ZERO_DIGIT DIGIT* | '0'+;
OCT_INTEGER     : '0' [oO] [0-7]+;
HEX_INTEGER     : '0' [xX] [0-9a-fA-F]+;
BIN_INTEGER     : '0' [bB] [01]+;

FLOAT_NUMBER    : POINT_FLOAT | EXPONENT_FLOAT;
IMAG_NUMBER     : (FLOAT_NUMBER | INT_PART) [jJ];

LINE_BREAK : ('\r'? '\n' | '\r' | '\f') ;
NEWLINE: ( {self.atStartOfInput()}? SPACES | ( '\r'? '\n' | '\r' | '\f' ) SPACES?) {self.onNewLine();};



// Fragments
fragment NON_ZERO_DIGIT : [1-9];
fragment DIGIT          : [0-9];
fragment SPACES         : [ \t]+;
fragment COMMENT        : '#' ~[\r\n\f]*;
fragment LINE_JOINING   : '\\' SPACES? ( '\r'? '\n' | '\r' | '\f' );

fragment INT_PART: DIGIT+;
fragment POINT_FLOAT: INT_PART? FRACTION | INT_PART '.';
fragment EXPONENT_FLOAT: (INT_PART | POINT_FLOAT) EXPONENT;
fragment FRACTION: '.' DIGIT+;
fragment EXPONENT: [eE] [+-]? DIGIT+;

fragment STRING_PREFIX: [rRuUfF] | 'fr' | 'Fr' | 'fR' | 'FR' | 'rf' | 'rF' | 'Rf' | 'RF';
fragment SHORT_STRING: '\'' (~[\\\r\n\f'] | ESCAPE_SEQ)* '\'' | '"' (~[\\\r\n\f"] | ESCAPE_SEQ)* '"';
fragment LONG_STRING: '\'\'\'' LONG_STRING_ITEM*? '\'\'\'' | '"""' LONG_STRING_ITEM*? '"""';
fragment LONG_STRING_ITEM: ~'\\' | ESCAPE_SEQ;
fragment ESCAPE_SEQ: '\\' .;

fragment ID_START: '_' | [A-Z] | [a-z];
fragment ID_CONTINUE: ID_START | [0-9];


SKIP_
    : ( SPACES | COMMENT | LINE_JOINING ) -> skip
    ;