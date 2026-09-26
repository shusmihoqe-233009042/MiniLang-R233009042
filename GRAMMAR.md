Program → StatementList

StatementList → Statement StatementList | ε

Statement →
      Declaration
    | Assignment
    | WhileStatement
    | SwitchStatement
    | Block

WhileStatement →
    WHILE LPAREN Expression RPAREN Block

SwitchStatement →
    SWITCH LPAREN Expression RPAREN
    LBRACE CaseList RBRACE

ArrayDeclaration →
    ARRAY ID LBRACKET NUMBER RBRACKET

Expression →
    ID
    | NUMBER
    | Expression PLUS Expression
    | Expression LESS Expression
