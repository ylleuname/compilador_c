from enum import Enum
from typing import Iterable, Dict, List, Tuple

#criar endif para o fim do IF
#
class TipoToken(Enum):
  INT = 1
  PRINTF = 2
  IDENTIFICADOR = 3
  ATRIBUICAO = 4
  SOMA = 5
  SUBTRACAO = 6
  INUM = 7
  #Float Number
  FNUM = 8
  ESPACO = 9
  FIM = 10
  VAZIO = 11
  IF = 12
  ELSE = 13
  PARENTESES_ESQUERDO = 14
  PARENTESES_DIREITO = 15
  DECLARACAO_FLOAT = 16
  FLOAT = 17
  SINAL_OU = 18
  SINAL_E = 19
  DIVISAO = 20
  MULTIPLICACAO = 21
  WHILE = 22
  CHAVES_ESQUERDA = 23
  CHAVES_DIREITA = 24
  IGUAL = 25
  DIFERENTE = 26
  MENOR = 27
  MAIOR = 28
  MENOR_IGUAL = 29
  MAIOR_IGUAL = 30
  ENDIF = 31

class Token:
  def __init__(self, tipo, valor):
    self.tipo = tipo
    self.valor = valor

  def __str__(self):
    return f"Token({self.tipo}, '{self.valor}')"

nomesTokens = [
    "DECLARACAO_INT", "IMPRIMIR", "IDENTIFICADOR", "ATRIBUICAO", "SOMA",
    "SUBTRACAO", "INUM", "FNUM", "ESPACO", "FIM", "NENHUM",
    "IF", "ELSE",
    "PARENTESE_ESQ", "PARENTESE_DIR", "DECLARACAO_FLOAT", "DECLARACAO_FLOAT",
    "OU", "E",
    "DIVISAO", "MULTIPLICACAO",
    "WHILE", "CHAVES_ESQ", "CHAVES_DIR",
    "IGUAL", "DIFERENTE", "MENOR", "MAIOR", "MENOR_IGUAL", "MAIOR_IGUAL", "ENDIF"
]

def criarToken(tipo, valor):
  return Token(tipo, valor)


class Parser(Token):
    def __init__(self, entrada):
        self.entrada = entrada
        self.tokenAtual = Token(TipoToken.VAZIO, "")
        self.avancar()

    def avancar(self):
        self.tokenAtual, self.entrada = self.proximoToken(self.entrada)

    def consumir(self, tipoEsperado):
        if self.tokenAtual.tipo == tipoEsperado:
            self.avancar()
        else:
            raise SyntaxError(
                f"Erro de sintaxe: token inesperado. "
                f"Esperado: {nomesTokens[tipoEsperado.value - 1]}, "
                f"Encontrado: {nomesTokens[self.tokenAtual.tipo.value - 1]}"
            )

    def match(self, tipoEsperado):
        if self.tokenAtual.tipo == tipoEsperado:
            self.consumir(tipoEsperado)
        else:
            raise SyntaxError(
                f"Erro de sintaxe: token esperado não encontrado. "
                f"Esperado: {nomesTokens[tipoEsperado.value - 1]}, "
                f"Encontrado: {nomesTokens[self.tokenAtual.tipo.value - 1]}"
            )

    def program(self):
        self.statementList()

    def statementList(self):
        while (self.tokenAtual.tipo != TipoToken.FIM):
            self.statement()
            if self.tokenAtual.tipo == TipoToken.FIM:
                break

    def whileStatement(self):
        self.match(TipoToken.WHILE)
        self.match(TipoToken.PARENTESES_ESQUERDO)
        self.expression()
        self.match(TipoToken.PARENTESES_DIREITO)
        self.match(TipoToken.CHAVES_ESQUERDA)
        self.statement()

    def ifStatement(self):
        self.match(TipoToken.IF)
        self.match(TipoToken.PARENTESES_ESQUERDO)
        self.expression()
        self.match(TipoToken.PARENTESES_DIREITO)
        self.match(TipoToken.CHAVES_ESQUERDA)
        self.statement()
        if self.tokenAtual.tipo == TipoToken.ELSE:
            self.consumir(TipoToken.ELSE)
            self.match(TipoToken.CHAVES_ESQUERDA)
            self.statement()
        self.match(TipoToken.ENDIF)

 #x=1             x+1
    def statement(self):
        if self.tokenAtual.tipo == TipoToken.INT:
            self.declaration_int()
            print("declaracao int")
        elif self.tokenAtual.tipo == TipoToken.FLOAT:
            self.declaration_float()
            print("declaracao float")
        elif self.tokenAtual.tipo == TipoToken.IF:
            self.ifStatement()
            print("if statement")
        elif self.tokenAtual.tipo == TipoToken.IDENTIFICADOR:
            if self.proximoToken(self.entrada)[0].tipo == TipoToken.ATRIBUICAO:
                self.assignment()
                print("declaracao assignment")
            else:
                self.expression()
                self.match(TipoToken.FIM)
        elif self.tokenAtual.tipo == TipoToken.WHILE:
            self.whileStatement()
        else:
            self.expression()
            self.statementEnd()

    def statementEnd(self):
        if self.tokenAtual.tipo == TipoToken.FIM:
            self.match(TipoToken.FIM)
        elif self.tokenAtual.tipo == TipoToken.CHAVES_DIREITA:
            self.match(TipoToken.CHAVES_DIREITA)
        else:
            raise SyntaxError(
                "Erro de sintaxe: Esperado FIM ou CHAVES_DIREITA, "
                f"Encontrado: {nomesTokens[self.tokenAtual.tipo.value - 1]}"
            )

    # regra para aceitar declarações simples do tipo "int nome_variavel"
    def declaration_int(self):
        self.match(TipoToken.INT)
        self.match(TipoToken.IDENTIFICADOR)
        if self.tokenAtual.tipo == TipoToken.FIM:
            self.match(TipoToken.FIM)
        elif self.tokenAtual.tipo == TipoToken.CHAVES_DIREITA:
            self.match(TipoToken.CHAVES_DIREITA)

    def declaration_float(self):
        self.match(TipoToken.FLOAT)
        self.match(TipoToken.IDENTIFICADOR)
        if self.tokenAtual.tipo == TipoToken.FIM:
            self.match(TipoToken.FIM)
        elif self.tokenAtual.tipo == TipoToken.CHAVES_DIREITA:
            self.match(TipoToken.CHAVES_DIREITA)

    def assignment(self):
        self.match(TipoToken.IDENTIFICADOR)
        self.match(TipoToken.ATRIBUICAO)
        self.expression()
        if self.tokenAtual.tipo == TipoToken.FIM:
            self.match(TipoToken.FIM)
        elif self.tokenAtual.tipo == TipoToken.CHAVES_DIREITA:
            self.match(TipoToken.CHAVES_DIREITA)

    # expressões lógicas agora têm prioridade menor que aritméticas
    def expression(self):
        self.simpleExpression()
        self.expressionLinha()

    def expressionLinha(self):
        if self.tokenAtual.tipo in (TipoToken.IGUAL, TipoToken.DIFERENTE,
                                    TipoToken.MENOR, TipoToken.MAIOR,
                                    TipoToken.MENOR_IGUAL, TipoToken.MAIOR_IGUAL):
            self.consumir(self.tokenAtual.tipo)
            self.simpleExpression()
            self.expressionLinha()

    def logicalExpression(self):
        self.relationalExpression()
        self.logicalExpressionLinha()

    def logicalExpressionLinha(self):
        if self.tokenAtual.tipo in (TipoToken.SINAL_E, TipoToken.SINAL_OU):
            self.consumir(self.tokenAtual.tipo)
            self.relationalExpression()
            self.logicalExpressionLinha()

    def simpleExpression(self):
        self.term()
        self.simpleExpressionLinha()

    def simpleExpressionLinha(self):
        if self.tokenAtual.tipo in (TipoToken.SOMA, TipoToken.SUBTRACAO):
            self.consumir(self.tokenAtual.tipo)
            self.term()
            self.simpleExpressionLinha()
        else:
            return

    def term(self):
        self.factor()
        self.termLinha()

    def termLinha(self):
        if self.tokenAtual.tipo in (TipoToken.MULTIPLICACAO, TipoToken.DIVISAO):
            self.consumir(self.tokenAtual.tipo)
            self.factor()
            self.termLinha()  # Recursão à direita
        else:
            return

    def factor(self):
        if self.tokenAtual.tipo in (
                TipoToken.IDENTIFICADOR,
                TipoToken.INUM,
                TipoToken.FNUM,
                TipoToken.IF
        ):
            self.consumir(self.tokenAtual.tipo)
        elif self.tokenAtual.tipo == TipoToken.PARENTESES_ESQUERDO:
            self.consumir(TipoToken.PARENTESES_ESQUERDO)
            self.expression()
            self.consumir(TipoToken.PARENTESES_DIREITO)
        else:
            raise SyntaxError(
                "Erro de sintaxe: fator inválido. "
                f"Encontrado: {nomesTokens[self.tokenAtual.tipo.value - 1]}"
            )

    #vai "pulando" os espaços em branco para poder ir para o próximo token
    def proximoToken(self, entrada):
      while entrada:
        if entrada[0].isspace():
            entrada = entrada[1:]
            continue
        else:
            break
      if not entrada:
        return criarToken(TipoToken.FIM, ""), ""

      # Verifica cada tipo de token
      if entrada.startswith("int"):
        return criarToken(TipoToken.INT, 'int'), entrada[3:]
      if entrada.startswith("float"):
        return criarToken(TipoToken.FLOAT, 'float'), entrada[5:]
      elif entrada.startswith("printf"):
        return criarToken(TipoToken.PRINTF, 'printf'), entrada[6:]
      elif entrada.startswith("=="):
        return criarToken(TipoToken.IGUAL, '=='), entrada[2:]
      elif entrada[0] == '=':
        return criarToken(TipoToken.ATRIBUICAO, '='), entrada[1:]
      elif entrada[0] == '+':
        return criarToken(TipoToken.SOMA, '+'), entrada[1:]
      elif entrada[0] == '-':
        return criarToken(TipoToken.SUBTRACAO, '-'), entrada[1:]
      elif entrada[0] == '/':
        return criarToken(TipoToken.DIVISAO, '/'), entrada[1:]
      elif entrada[0] == '*':
        return criarToken(TipoToken.MULTIPLICACAO, '*'), entrada[1:]
      elif entrada[0] == '(':
        return criarToken(TipoToken.PARENTESES_ESQUERDO, '('), entrada[1:]
      elif entrada[0] == ')':
        return criarToken(TipoToken.PARENTESES_DIREITO, ')'), entrada[1:]
      elif entrada[0] == '{':
        return criarToken(TipoToken.CHAVES_ESQUERDA, '{'), entrada[1:]
      elif entrada[0] == '}':
        return criarToken(TipoToken.CHAVES_DIREITA, '}'), entrada[1:]
      elif entrada[0] == '<':
        return criarToken(TipoToken.MENOR, '<'), entrada[1:]
      elif entrada[0] == '>':
        return criarToken(TipoToken.MAIOR, '>'), entrada[1:]
      elif entrada[0] == 'endif':
        return criarToken(TipoToken.ENDIF, 'endif'), entrada[5:]
      elif entrada[0] == '$':
        return criarToken(TipoToken.FIM, '$'), entrada[1:]
      elif entrada.startswith("if"):
        return criarToken(TipoToken.IF, "if"), entrada[2:]
      elif entrada.startswith("else"):
        return criarToken(TipoToken.ELSE, "else"), entrada[4:]
      elif entrada.startswith("while"):
        return criarToken(TipoToken.WHILE, "while"), entrada[5:]
      if entrada.startswith("&&"):
        return criarToken(TipoToken.SINAL_E, '&&'), entrada[2:]
      if entrada.startswith("||"):
        return criarToken(TipoToken.SINAL_OU, '||'), entrada[2:]
      if entrada.startswith("!="):
        return criarToken(TipoToken.DIFERENTE, '!='), entrada[2:]
      if entrada.startswith("<="):
        return criarToken(TipoToken.MENOR_IGUAL, '<='), entrada[2:]
      if entrada.startswith(">="):
        return criarToken(TipoToken.MAIOR_IGUAL, '>='), entrada[2:]
      #Caso onde a entrada é um dígito
      elif entrada[0].isdigit():
        inicio = 0
        while inicio < len(entrada) and entrada[inicio].isdigit():
          inicio += 1
        if inicio < len(entrada) and entrada[inicio] == '.':
          inicio += 1
          while inicio < len(entrada) and entrada[inicio].isdigit():
            inicio += 1
          return criarToken(TipoToken.FNUM, entrada[:inicio]), entrada[inicio:]
        return criarToken(TipoToken.INUM, entrada[:inicio]), entrada[inicio:]
      #Caso onde a entrada é uma palavra (Identificador)
      elif entrada[0].isalpha():
        inicio = 0
        while inicio < len(entrada) and entrada[inicio].isalpha():
          inicio += 1
        return criarToken(TipoToken.IDENTIFICADOR, entrada[:inicio]), entrada[inicio:]
      else:
        return criarToken(TipoToken.VAZIO, ""), entrada[1:]

class Grammar:

    def __init__(self) -> None:
        self.__terminals = {}
        self.__nonterminals = {}
        self.__productions = {}
        self.__id = 0

    def add_terminal(self, x: str) -> int:
        if x in self.__nonterminals:
            raise ValueError()
        self.__terminals[x] = self.__id
        self.__id = self.__id+1
        return self.__terminals[x]

    def add_nonterminal(self, X: str):
        if X in self.__terminals:
            raise ValueError()
        self.__nonterminals[X] = self.__id
        self.__id = self.__id + 1
        return self.__nonterminals[X]

    def grammar(self, S: str) -> None:
        self.add_nonterminal(S)

    def add_production(self, A: str, rhs: list) -> int:
        self.__productions[self.__id] = {'lhs': '', 'rhs': []}
        self.__productions[self.__id]['lhs'] = A
        self.__productions[self.__id]['rhs'] = rhs
        self.__id = self.__id+1
        return self.__id - 1

    def terminals(self) -> iter:
        return iter(self.__terminals)

    def nonterminals(self) -> iter:
        return iter(self.__nonterminals)

    def productions(self) -> iter:
        return iter(self.__productions)

    def is_terminal(self, X: str) -> bool:
        return X in self.__terminals

    def rhs(self, p: int) -> list:
        return self.__productions[p]['rhs']

    def lhs(self, p: int) -> str:
        return self.__productions[p]['lhs']

    def productions_for(self, A: str) -> list:
        l = []
        for k, v in self.__productions.items():
            if v['lhs'] == A:
                l.append(k)
        return l

    def occurrences(self, X: str) -> list:
        l = []
        for k, v in self.__productions.items():
            for i, rhs in enumerate(v['rhs']):
                if (rhs == X):
                    l.append((k, i))
        return l

    def production(self, O: tuple[int, int]) -> int:
        return O[0]

    def tail(self, p: int, i:int) -> list:
        return self.__productions[p]['rhs'][i+1:]

grammar = Grammar()

# Definir os terminais
grammar.add_terminal('INT')
grammar.add_terminal('FLOAT')
grammar.add_terminal('IDENTIFICADOR')
grammar.add_terminal('ATRIBUICAO')
grammar.add_terminal('SOMA')
grammar.add_terminal('SUBTRACAO')
grammar.add_terminal('MULTIPLICACAO')
grammar.add_terminal('DIVISAO')
grammar.add_terminal('IGUAL')
grammar.add_terminal('DIFERENTE')
grammar.add_terminal('MENOR')
grammar.add_terminal('MAIOR')
grammar.add_terminal('MENOR_IGUAL')
grammar.add_terminal('MAIOR_IGUAL')
grammar.add_terminal('SINAL_E')
grammar.add_terminal('SINAL_OU')
grammar.add_terminal('PARENTESES_ESQUERDO')
grammar.add_terminal('PARENTESES_DIREITO')
grammar.add_terminal('CHAVES_ESQUERDA')
grammar.add_terminal('CHAVES_DIREITA')
grammar.add_terminal('IF')
grammar.add_terminal('ELSE')
grammar.add_terminal('ENDIF')
grammar.add_terminal('WHILE')
grammar.add_terminal('FIM')
grammar.add_terminal('INUM')
grammar.add_terminal('FNUM')

# Definir os não-terminais
grammar.grammar('program')
grammar.add_nonterminal('statementList')
grammar.add_nonterminal('statement')
grammar.add_nonterminal('declaration')
grammar.add_nonterminal('declaration_int')
grammar.add_nonterminal('declaration_float')
grammar.add_nonterminal('assignment')
grammar.add_nonterminal('ifStatement')
grammar.add_nonterminal('whileStatement')
grammar.add_nonterminal('expression')
grammar.add_nonterminal('relationalExpression')
grammar.add_nonterminal('relationalOperator')
grammar.add_nonterminal('logicalExpression')
grammar.add_nonterminal('logicalOperator')
grammar.add_nonterminal('simpleExpression')
grammar.add_nonterminal('additiveOperator')
grammar.add_nonterminal('term')
grammar.add_nonterminal('multiplicativeOperator')
grammar.add_nonterminal('factor')

grammar.add_production('program', ['statementList'])
grammar.add_production('statementList', ['statement', 'statementList'])
grammar.add_production('statementList', ['ε'])

grammar.add_production('statement', ['declaration'])
grammar.add_production('statement', ['ifStatement'])
grammar.add_production('statement', ['whileStatement'])
grammar.add_production('statement', ['assignment'])
grammar.add_production('statement', ['simpleExpression', 'statementEnd'])
grammar.add_production('statementEnd', ['FIM'])
grammar.add_production('statementEnd', ['CHAVES_DIREITA'])

grammar.add_production('declaration', ['declaration_int'])
grammar.add_production('declaration', ['declaration_float'])
grammar.add_production('declaration_int', ['INT', 'IDENTIFICADOR', 'FIM'])
grammar.add_production('declaration_int', ['INT', 'IDENTIFICADOR', 'CHAVES_DIREITA'])
grammar.add_production('declaration_float', ['FLOAT', 'IDENTIFICADOR', 'FIM'])
grammar.add_production('declaration_float', ['FLOAT', 'IDENTIFICADOR', 'CHAVES_DIREITA'])

grammar.add_production('assignment', ['IDENTIFICADOR', 'ATRIBUICAO', 'expression', 'FIM'])
grammar.add_production('assignment', ['IDENTIFICADOR', 'ATRIBUICAO', 'expression', 'CHAVES_DIREITA'])

grammar.add_production('ifStatement', ['IF', 'PARENTESES_ESQUERDO', 'relationalExpression', 'PARENTESES_DIREITO', 'CHAVES_ESQUERDA', 'statement', 'CHAVES_DIREITA'])
grammar.add_production('ifStatement', ['IF', 'PARENTESES_ESQUERDO', 'relationalExpression', 'PARENTESES_DIREITO', 'CHAVES_ESQUERDA', 'statement', 'ELSE', 'CHAVES_ESQUERDA', 'statement', 'CHAVES_DIREITA', 'ENDIF'])

grammar.add_production('whileStatement', ['WHILE', 'PARENTESES_ESQUERDO', 'relationalExpression', 'PARENTESES_DIREITO', 'CHAVES_ESQUERDA', 'statement', 'CHAVES_DIREITA'])

grammar.add_production('expression', ['logicalExpression'])

grammar.add_production('relationalExpression', ['simpleExpression', 'relationalOperator', 'simpleExpression'])
grammar.add_production('relationalOperator', ['IGUAL'])
grammar.add_production('relationalOperator', ['DIFERENTE'])
grammar.add_production('relationalOperator', ['MENOR'])
grammar.add_production('relationalOperator', ['MAIOR'])
grammar.add_production('relationalOperator', ['MENOR_IGUAL'])
grammar.add_production('relationalOperator', ['MAIOR_IGUAL'])

grammar.add_production('logicalExpression', ['simpleExpression', 'logicalOperator', 'logicalExpression'])
grammar.add_production('logicalExpression', ['simpleExpression'])
grammar.add_production('logicalOperator', ['SINAL_E'])
grammar.add_production('logicalOperator', ['SINAL_OU'])

grammar.add_production('simpleExpression', ['term', 'additiveOperator', 'simpleExpression'])
grammar.add_production('simpleExpression', ['term'])

grammar.add_production('additiveOperator', ['SOMA'])
grammar.add_production('additiveOperator', ['SUBTRACAO'])

grammar.add_production('term', ['factor', 'multiplicativeOperator', 'term'])
grammar.add_production('term', ['factor'])

grammar.add_production('multiplicativeOperator', ['MULTIPLICACAO'])
grammar.add_production('multiplicativeOperator', ['DIVISAO'])

grammar.add_production('factor', ['IDENTIFICADOR'])
grammar.add_production('factor', ['INUM'])
grammar.add_production('factor', ['FNUM'])
grammar.add_production('factor', ['PARENTESES_ESQUERDO', 'expression', 'PARENTESES_DIREITO'])

def main():
    entrada = "while(x==2){x=1}$"
    #entrada = 'a = 1'
    parser = Parser(entrada)
    try:
        parser.program()
        if parser.tokenAtual.tipo == TipoToken.FIM:
            print("Análise sintática concluída com sucesso!")
        else:
            print("Erro na análise sintática")
    except SyntaxError as e:
        print(e)

#teste github desktop
if __name__ == "__main__":
    main()