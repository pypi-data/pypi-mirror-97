// concrete syntax
grammar Cal;

// non-terminals expressed as context-free grammar (BNF)
# 定义表达式
expr:
        left=expr op='?' right=expr  # ConditionExpr
	|   left=expr op='&' right=expr  # AndExpr
	|   left=expr op='#' right=expr  # DependExpr
    |   left=expr op=('>='|'<='|'>'|'<'|'='|'==') right=expr  # CheckExpr
    |	left=expr op=('*'|'/') right=expr  # OpExpr
    |	left=expr op=('+'|'-') right=expr  # OpExpr
    |	atom=WORD                    # AtomExpr
    |	'(' expr ')'                       # ParenExpr
    ;

// tokens expressed as regular expressions
WORD : DIGIT+ '.' DIGIT* EXPONET?
      | '.' DIGIT+ EXPONET?
      | DIGIT+ EXPONET?
      | [0-9A-Za-z|\-|_|'|"|:|' ']+;

fragment DIGIT : '0'..'9' ;
fragment EXPONET : ('e'|'E') ('+'|'-')? DIGIT+ ;
WS  :   [ \t]+ -> skip ;
