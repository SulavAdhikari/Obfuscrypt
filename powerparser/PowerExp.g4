// PowerExp.g4 - Real-World PowerShell Parser with Full Features

grammar PowerExp;

// ===== ENTRY =====
script: (statement SEMICOLON)* EOF;

// ===== STATEMENTS =====
statement
    : commandStatement
    | assignment
    | flowControl
    | ifStatement
    | whileStatement
    | foreachStatement
    | doWhileStatement
    | forStatement
    | tryCatchStatement
    | switchStatement
    | functionDecl
    | paramBlock
    | expression
    ;

commandStatement
    : commandName (parameterBinding | expression)*
    ;

parameterBinding
    : PARAMETER_NAME (expression)?
    ;

commandName
    : COMMAND_NAME
    | IDENTIFIER
    ;

assignment
    : VARIABLE EQUALS expression
    ;

functionDecl
    : 'function' IDENTIFIER codeBlock
    ;

paramBlock
    : 'Param' '(' param (',' param)* ')'
    ;

param
    : attribute* VARIABLE (typeCast)?
    ;

typeCast
    : '[' expression ('[' ']')? ']'
    | VARIABLE
    ;

typeCastExpression: typeCast expression;

attribute
    : '[' 'Parameter' ('(' attributeParams ')')? ']'
    ;

attributeParams
    : attributeParam (',' attributeParam)*
    ;

attributeParam
    : IDENTIFIER '=' expression
    | expression
    ;

codeBlock
    : '{'  (statement SEMICOLON? )* '}'
    ;

ifStatement
    : 'if' '(' expression ')' codeBlock ('else' codeBlock)?
    ;

whileStatement
    : 'while' '(' expression ')' codeBlock
    ;

doWhileStatement
    : 'do' codeBlock 'while' '(' expression ')'
    ;

foreachStatement
    : 'foreach' '(' VARIABLE 'in' expression ')' codeBlock
    ;

forStatement
    : 'for' '(' assignment? ';' expression? ';' assignment? ')' codeBlock
    ;

tryCatchStatement
    : 'try' codeBlock ('catch' codeBlock)? ('finally' codeBlock)?
    ;

switchStatement
    : 'switch' '(' expression ')' '{' switchClause* '}'
    ;

switchClause
    : expression codeBlock
    ;

flowControl
    : 'return' expression?
    | 'break'
    | 'continue'
    | 'throw' expression
    | 'exit' expression?
    ;

// ===== EXPRESSIONS =====
expression
    : pipelineExpression
    ;

pipelineExpression
    : logicalExpression ('|' logicalExpression)*
    ;

logicalExpression
    : bitwiseExpression ((AND | OR | XOR) bitwiseExpression)*
    ;

bitwiseExpression
    : comparisonExpression ((BAND | BOR | BXOR) comparisonExpression)*
    ;

comparisonExpression
    : additiveExpression (comparisonOperator additiveExpression)*
    ;

additiveExpression
    : multiplicativeExpression ((PLUS | MINUS) multiplicativeExpression)*
    ;

multiplicativeExpression
    : unaryExpression ((MULTIPLY | DIVIDE) unaryExpression)*
    ;

unaryExpression
    : unaryOperator? postfixExpression
    ;

postfixExpression
    : baseExpression postfixSuffix*
    ;

postfixSuffix
    : '.' expression
    | functionArguments
    | '[' expression ']'
    | STATIC_MEMBER_ACCESS_OPERATOR expression
    ;

unaryOperator
    : MINUS
    | PLUS
    | NOT
    ;

comparisonOperator
    : EQ | NE | GT | LT | GE | LE | MATCH | LIKE
    ;

type
    : IDENTIFIER ('[' ']')?
    ;

baseExpression
    : '(' expression ')'
    | '[' type ']'
    | commandInvocation
    | functionCall
    | arrayLiteral
    | hashtableLiteral
    | expressionArray
    | typeCastExpression
    | codeBlock
    | NUMBER
    | STRING
    | INTERP_STRING
    | VARIABLE
    | IDENTIFIER
    ;

commandInvocation
    : commandName (parameterBinding | baseExpression)*
    ;

functionArguments
    : '(' (expression (',' expression)*)? ')'
    ;

functionCall
    : IDENTIFIER functionArguments
    ;

arrayLiteral
    : '@(' (expression (',' expression)*)? ')'
    ;

expressionArray
    : '@(' expression (',' expression)* ')'
    ;

hashtableLiteral
    : '@{' (keyValuePair (',' keyValuePair)*)? '}'
    ;

keyValuePair
    : expression '=' expression
    ;

// ===== LEXER RULES =====
HEX_NUMBER : '0x' [0-9a-fA-F]+;
NUMBER     : ('-')?[0-9]+;
STRING     : '\'' .*? '\'' | '"' .*? '"';
INTERP_STRING : '"' (~["\\$] | '\\' . | VARIABLE)* '"';
HEREDOC    : '@"' ( ~["'] | '"' ~'@' | '\r'? '\n' )* '"@';
VARIABLE   : '$' IDENTIFIER;
IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]*;
COMMAND_NAME: [a-zA-Z_][a-zA-Z0-9_-]*;

// Comments
LINE_COMMENT  : '#' ~[\r\n]* -> skip;
BLOCK_COMMENT : '<#' .*? '#>' -> skip;

// Operators
EQUALS  : '=';
STATIC_MEMBER_ACCESS_OPERATOR: '::';
PLUS    : '+';
MINUS   : '-';
MULTIPLY: '*';
DIVIDE  : '/';
OR      : '-' [oO] [rR];
AND     : '-' [aA] [nN] [dD];
XOR     : '-' [xX] [oO] [rR];
NOT     : '-' [nN] [oO] [tT];
LE      : '-' [lL] [eE];
GE      : '-' [gG] [eE];
LT      : '-' [lL] [tT];
GT      : '-' [gG] [tT];
NE      : '-' [nN] [eE];
EQ      : '-' [eE] [qQ];
LIKE    : '-' [lL] [iI] [kK] [eE];
MATCH   : '-' [mM] [aA] [tT] [cC] [hH];
BXOR    : '-' [bB] [xX] [oO] [rR];
BOR     : '-' [bB] [oO] [rR];
BAND    : '-' [bB] [aA] [nN] [dD];

PARAMETER_NAME : '-' [a-zA-Z_][a-zA-Z0-9_]*;
SEMICOLON : ';';
WS        : [\r\n \t]+ -> skip;
