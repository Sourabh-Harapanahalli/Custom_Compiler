import sys
from sly import Lexer, Parser

class SymbolTable:

    def __init__(self):
        self.table = []

    def add_name(self, name):
        '''Insert a new identifier to the symbol table'''
        new_entry = {'name': name}
        self.table.append(new_entry)

    def add_type(self, name, typee):
        '''Insert type of an identifier to the symbol table'''
        for entry in self.table:
            if entry['name'] == name:
                entry['type'] = typee

    def add_formals(self, name, formalVar):
        '''Insert formals (parameters) of a function to the symbol table'''
        for entry in self.table:
            if entry['name'] == name:
              if 'formals' in entry:
                entry['formals'].append(formalVar)
              else:
                entry['formals'] = [formalVar]

    def get_formals(self, symbol):
        '''Get formals of a function symbol'''
        for entry in self.table:
            if entry['name'] == symbol:
                return entry.get('formals', [])
        return []  # symbol not found or formals not found

    def insert_value(self, name, value):
        '''Insert a value of symbol to the symbol table'''
        for entry in self.table:
            if entry['name'] == name:
                entry['value'] = value

    def lookup_name(self, name):
        '''Check whether an identifier name exists in symbol table'''
        for entry in self.table:
            if entry['name'] == name:
                return True
        return False

    def get_type(self, symbol):
        '''Get the type of a symbol'''
        for entry in self.table:
            if entry['name'] == symbol:
                return entry.get('type', 0)
        return 0  # symbol not found

    def get_value(self, symbol, typee):
        '''Get the value of a symbol'''
        for entry in self.table:
            if entry['name'] == symbol and entry['type'] == typee:
                return entry['value']
        return 0  # symbol not found

    def find_tuples_with_keyword(self, tree, keyword):
        tuples_with_keyword = []

        # If the current node is a tuple
        if isinstance(tree, tuple):
            # Check if the first element of the tuple matches the keyword
            if tree[0] == keyword:
                tuples_with_keyword.append(tree)

            # Recursively traverse through the elements of the tuple
            for element in tree[1:]:
                tuples_with_keyword.extend(self.find_tuples_with_keyword(element, keyword))

        return tuples_with_keyword


# Global object that instantiates symbol table: use this to insert, get, lookup, ...
tab = SymbolTable()

class DLangLexer(Lexer):

    tokens = {LE, GE, EQ, NE, AND, OR, INT, DOUBLE, STRING, IDENTIFIER, NOTHING, INTK, DOUBLEK, BOOL, BOOLK, STRINGK, NULL, FOR, WHILE, IF, ELSE, RETURN, BREAK, OUTPUT, INPUTINT, INPUTLINE}
    literals = {'+', '-', '*', '/', '%', '<', '>', '=', '!', ';', ',', '.', '[', ']', '(', ')', '{', '}'}
    ignore = ' \t\r'
    ignore_comment1 = r'\/\*[^"]*\*\/'
    ignore_comment = r'\/\/.*'
    ignore_newline = r'\n+'

    STRING = r'\"(.)*\"'
    DOUBLE = r'[0-9]+\.[0-9]*([E][+-]?\d+)?'
    INT = r'[0-9]+'
    EQ = r'=='
    NE = r'!='
    LE = r'<='
    GE = r'>='
    AND = r'&&'
    OR =  r'\|\|'
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]{0,39}'
    IDENTIFIER['nothing'] = NOTHING
    IDENTIFIER['int'] = INTK
    IDENTIFIER['double'] = DOUBLEK
    IDENTIFIER['string'] = STRINGK
    IDENTIFIER['bool'] = BOOLK
    IDENTIFIER['True'] = BOOL
    IDENTIFIER['False'] = BOOL
    IDENTIFIER['null'] = NULL
    IDENTIFIER['for'] = FOR
    IDENTIFIER['while'] = WHILE
    IDENTIFIER['if'] = IF
    IDENTIFIER['else'] = ELSE
    IDENTIFIER['return'] = RETURN
    IDENTIFIER['break'] = BREAK
    IDENTIFIER['Output'] = OUTPUT
    IDENTIFIER['InputInt'] = INPUTINT
    IDENTIFIER['InputLine'] = INPUTLINE

    def error(self, t):
        print("Invalid character '%s'" % t.value[0])
        self.index += 1


class DLangParser(Parser):

    debugfile = 'dlang-parser.log'
    tokens = DLangLexer.tokens
    precedence = (
        ('nonassoc', EQ, NE, LE, GE, AND, OR, '<', '>'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('nonassoc', '=')
    )

    def __init__(self):
        self.IDENTIFIERs = {}

    def semantic_error(self, msg, lineno):
        print('\nSemantic Error : ', msg)

    @_('Decl DeclRest', 'Epsilon')
    def Program(self, p):
        print('\nParsing completed Successfully!\n')
        return p

    @_('Decl DeclRest', 'Epsilon')
    def DeclRest(self, p):
        return p

    @_('VariableDecl')
    def Decl(self, p):
        return p

    @_('Stmt')
    def Decl(self, p):
        return p

    @_('FunctionDecl')
    def Decl(self, p):
        return p

    @_('Variable ";"')
    def VariableDecl(self, p):
        return p

    @_('Type IDENTIFIER')
    def Variable(self, p):
        tab.add_name(p.IDENTIFIER)
        tab.add_type(p.IDENTIFIER, p.Type)
        return p

    @_('INTK', 'DOUBLEK', 'BOOLK', 'STRINGK')
    def Type(self, p):
        return p

    @_('Variable "(" Formals ")" StmtBlock')
    def FunctionDecl(self, p):
      # ToDo: here check if returned value matches the return type
      left=[]
      right=[]
      tab.add_formals(p.Variable[-1],p.Formals)
      left=tab.find_tuples_with_keyword(p.Variable,'Type')[0][-1]
      x=tab.find_tuples_with_keyword(p.StmtBlock,'ReturnStmt')
      if len(x)>0:
        for c in tab.find_tuples_with_keyword(x[0],'Expr'):
          try:
            right.append(tab.get_type(c[-1])[-1])
          except:
            continue
      if len(list(set(right)))>0:
        if list(set(right))[0]!=left:
          self.semantic_error(f"Return type '{p.Variable}' does not match declared return type '{list(set(right))[0]}' for function '{left}'", p.lineno)
      return p

    @_('NOTHING IDENTIFIER "(" Formals ")" StmtBlock')
    def FunctionDecl(self, p):
        return p

    @_('Variable VariableRest', 'Epsilon')
    def Formals(self, p):
        return p

    @_('"," Variable VariableRest', 'Epsilon')
    def VariableRest(self, p):
        return p

    @_('"{" "}"', ' "{" VariableDecl "}" ', ' "{" VariableDecl VariableDeclRest "}" ', ' "{" Stmt "}" ', ' "{" Stmt StmtRest "}" ', ' "{" VariableDecl VariableDeclRest Stmt StmtRest  "}" ' )
    def StmtBlock(self, p):
        return p

    @_('VariableDecl VariableDeclRest', 'Epsilon')
    def VariableDeclRest(self, p):
        return p

    @_('Stmt StmtRest', 'Epsilon')
    def StmtRest(self, p):
        return p

    @_('Expr ";" ', ' ";" ', 'IfStmt', 'WhileStmt', 'ForStmt', 'BreakStmt', 'ReturnStmt', 'OutputStmt', 'StmtBlock')
    def Stmt(self, p):
        return p

    @_('IF "(" Expr ")" Stmt IfRest')
    def IfStmt(self, p):
        return p

    @_('ELSE Stmt', 'Epsilon')
    def IfRest(self, p):
        return p

    @_('WHILE "(" Expr ")" Stmt')
    def WhileStmt(self, p):
        return p

    @_('FOR "(" Expr ";" Expr ";" Expr ")" Stmt')
    def ForStmt(self, p):
        return p

    @_('RETURN Expr ";" ', 'RETURN ";"')
    def ReturnStmt(self, p):
        return p

    @_('BREAK ";" ')
    def BreakStmt(self, p):
        return p

    @_('OUTPUT "(" Expr ExprRest ")" ";" ')
    def OutputStmt(self, p):
        return p

    @_('"," Expr ExprRest', 'Epsilon')
    def ExprRest(self, p):
        return p

    @_('"!" Expr', 'IDENTIFIER', 'Constant', 'Call', '"(" Expr ")" ', '"-" Expr', 'INPUTINT "(" ")"', 'INPUTLINE "(" ")"')
    def Expr(self, p):
        return p

    @_('Expr "+" Expr', 'Expr "-" Expr', 'Expr "*" Expr', 'Expr "/" Expr', 'Expr "%" Expr', 'Expr "<" Expr', 'Expr LE Expr', 'Expr ">" Expr', 'Expr GE Expr', 'Expr EQ Expr', 'Expr NE Expr', 'Expr AND Expr', 'Expr OR Expr')
    def Expr(self, p):
        # ToDo: here check if types of operands are compatible
        if 'Expr' not in p.Expr0[-1]:
          s2_type = tab.get_type(p.Expr0[-1])
          left_expr=s2_type[-1]
        elif 'Expr' in p.Expr0[-1]:
          s2_type = tab.get_type(p.Expr0[-1][-1])
          left_expr=s2_type[-1]

        if 'Expr' not in p.Expr1[-1]:
          s3_type = tab.get_type(p.Expr1[-1])
          right_expr=s3_type[-1]
        elif 'Expr' in p.Expr1[-1]:
          s3_type = tab.get_type(p.Expr1[-1][-1])
          right_expr=s3_type[-1]

        # if isinstance(left_expr, tuple) or isinstance(right_expr, tuple):
        #     # One or both expressions are still tuples, indicating an error in parsing
        #     self.semantic_error("Error in parsing expression", p.lineno)
        #     return

        if left_expr != right_expr:
            self.semantic_error(f"operand type mismatch in expression: '{p.Expr0} {p.Expr1} in' '{p.Expr0[-1]} - {left_expr}' and '{p.Expr1} - {right_expr}'", p.lineno)

        # Create a new expression object with the type of the operands
        return p

    @_('IDENTIFIER "=" Expr')
    def Expr(self, p):
        # ToDo: here check if the identifier has been declared before
        for entry in tab.table:
          if entry.get('name') == p[0]:
              if 'type' not in entry:
                  self.semantic_error(f"'{p.IDENTIFIER}'is used before it is declared", p.lineno)
        return p

    @_('IDENTIFIER "(" Actuals ")" ')
    def Call(self, p):
      # ToDo: here check all things related to mismatches in number and types of parameters
      expected_formals = tab.get_formals(p.IDENTIFIER)
      left=tab.find_tuples_with_keyword(expected_formals[0],'Variable')
      right=tab.find_tuples_with_keyword(p.Actuals,'Expr')
      if len(left) != len(right):
        if len(left)> len(right):
          self.semantic_error(f"Too few arguments in function call '{right}'", p.lineno)
        else:
          self.semantic_error(f"Too many arguments in function call '{right}'", p.lineno)

      else:
          for actual, expected in zip(right, left):
            e=tab.find_tuples_with_keyword(expected,'Type')[0][1]
            a=tab.find_tuples_with_keyword(actual,'Constant')[0][1]
            if e=='int':
              try:
                int_value = int(a)
              except ValueError:
                self.semantic_error(f"Type mismatch between actual and formal parameters in function call '{a}'", p.lineno)

            elif e=='double':
              try:
                int_value = float(a)
              except ValueError:
                self.semantic_error(f"Type mismatch between actual and formal parameters in function call '{a}'", p.lineno)

            elif e=='string':
              try:
                int_value = str(a)
              except ValueError:
                self.semantic_error(f"Type mismatch between actual and formal parameters in function call '{a}'", p.lineno)

      return p


    @_('Expr ExprRest1', 'Epsilon')
    def Actuals(self, p):
        return p

    @_('"," Expr ExprRest1', 'Epsilon')
    def ExprRest1(self, p):
        return p

    @_('INT', 'DOUBLE', 'BOOL', 'STRING', 'NULL')
    def Constant(self, p):
        return p

    @_('')
    def Epsilon(self, p):
        pass

    @_('IDENTIFIER')
    def Decl(self, p):
        try:
            return self.IDENTIFIERs[p.IDENTIFIER]
        except LookupError:
            print("Undefined IDENT '%s'" % p.IDENTIFIER)
            return 0

    def error(self, p):
        print("Syntax error near '%s' at line" % p.value[0], p.lineno)


if __name__ == '__main__':

    # Read DLang source from file
    print(sys.argv)
    if len(sys.argv) == 3:
        lexer = DLangLexer()
        parser = DLangParser()
        with open(r'c:/Users/soura/Desktop/UM Dearborn CIS/Compiler Design/Mini Project 3/test-hw3.dlang') as source:
            dlang_code = source.read()
            try:
                tokens = lexer.tokenize(dlang_code)
                for tok in tokens:
                    # Add identifier tokens to the symbol table
                    if tok.type == 'IDENTIFIER':
                        if tab.lookup_name(tok.value) == 0:
                            tab.add_name(tok.value)
                parser.parse(lexer.tokenize(dlang_code))
                print('Symbol Table Content')
                print(tab.table)
            except EOFError: exit(1)
    else:
        print("[DLang]: Source file missing")

