
from enum import Enum
from typing import Iterable, Dict, List, Tuple
import ll1_check
import predict
import grammar
#criar endif para o fim do IF
#
class tipo_token(Enum):
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

nomes_token = [
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
        self.token_atual = Token(tipo_token.VAZIO, "")
        self.avancar()

    def avancar(self):
        self.token_atual, self.entrada = self.proximo_token(self.entrada)

    def consumir(self, tipo_esperado):
        if self.token_atual.tipo == tipo_esperado:
            self.avancar()
        else:
            raise SyntaxError(
                f"Erro de sintaxe: token inesperado. "
                f"Esperado: {nomes_token[tipo_esperado.value - 1]}, "
                f"Encontrado: {nomes_token[self.token_atual.tipo.value - 1]}"
            )

    def match(self, tipo_esperado):
        if self.token_atual.tipo == tipo_esperado:
            self.consumir(tipo_esperado)
        else:
            raise SyntaxError(
                f"Erro de sintaxe: token esperado não encontrado. "
                f"Esperado: {nomes_token[tipo_esperado.value - 1]}, "
                f"Encontrado: {nomes_token[self.token_atual.tipo.value - 1]}"
            )

    def program(self):
        self.lista_statement()

    def lista_statement(self):
        while (self.token_atual.tipo != tipo_token.FIM):
            self.statement()
            if self.token_atual.tipo == tipo_token.FIM:
                break

    def while_statement(self):
        self.match(tipo_token.WHILE)
        self.match(tipo_token.PARENTESES_ESQUERDO)
        while (self.token_atual.tipo != tipo_token.PARENTESES_DIREITO):
            self.expression()
        self.match(tipo_token.PARENTESES_DIREITO)
        self.match(tipo_token.CHAVES_ESQUERDA)
        self.statement()
        self.statements_finais()

    def if_statement(self):
        self.match(tipo_token.IF)
        self.match(tipo_token.PARENTESES_ESQUERDO)
        #para consumir toda a expressão que estiver entre parenteses
        while(self.token_atual.tipo != tipo_token.PARENTESES_DIREITO):
            self.expression()
        self.match(tipo_token.PARENTESES_DIREITO)
        self.match(tipo_token.CHAVES_ESQUERDA)
        self.lista_statement()  # Permite múltiplos statements dentro do 'if'
        self.statements_finais()
        if self.token_atual.tipo == tipo_token.ELSE:
            self.consumir(tipo_token.ELSE)
            self.match(tipo_token.CHAVES_ESQUERDA)
            self.lista_statement()  # Permite múltiplos statements dentro do 'else'
            self.statements_finais()
        self.statements_finais()  # Adicionado 'endif'


    def statement(self):
        #int x 
        if self.token_atual.tipo == tipo_token.INT:
            self.declaration_int()
            print("declaracao int")
        elif self.token_atual.tipo == tipo_token.FLOAT:
            self.declaration_float()
            print("declaracao float")
        elif self.token_atual.tipo == tipo_token.IF:
            self.if_statement()
            print("if statement")
        elif self.token_atual.tipo == tipo_token.IDENTIFICADOR:
            if self.proximo_token(self.entrada)[0].tipo == tipo_token.ATRIBUICAO:
                self.assignment()
                print("declaracao assignment")
            else:
                self.expression()
                self.match(tipo_token.FIM)
        elif self.token_atual.tipo == tipo_token.WHILE:
            self.while_statement()
        else:
            self.expression()
            self.statements_finais()

    #um statement pode finalizar com $ (FIM), } (chaves direta) ou endif (endif para statements IF)
    def statements_finais(self):
        if self.token_atual.tipo == tipo_token.FIM:
            self.match(tipo_token.FIM)
        elif self.token_atual.tipo == tipo_token.CHAVES_DIREITA:
            self.match(tipo_token.CHAVES_DIREITA)
        elif self.token_atual.tipo == tipo_token.ENDIF:  # 'endif' adicionado
            self.match(tipo_token.ENDIF)
        else:
            raise SyntaxError(
                "Erro de sintaxe: Esperado FIM, CHAVES_DIREITA ou ENDIF, "
                f"Encontrado: {nomes_token[self.token_atual.tipo.value - 1]}"
            )

    # regra para aceitar declarações simples do tipo "int nome_variavel"
    def declaration_int(self):

        self.match(tipo_token.INT)
        self.match(tipo_token.IDENTIFICADOR)
        self.statements_finais()

    def declaration_float(self):
        self.match(tipo_token.FLOAT)
        self.match(tipo_token.IDENTIFICADOR)
        if self.token_atual.tipo == tipo_token.FIM:
            self.match(tipo_token.FIM)
        elif self.token_atual.tipo == tipo_token.CHAVES_DIREITA:
            self.match(tipo_token.CHAVES_DIREITA)

    #x = 1
    def assignment(self):
        self.match(tipo_token.IDENTIFICADOR)
        self.match(tipo_token.ATRIBUICAO)
        self.expression()
        if self.token_atual.tipo == tipo_token.FIM:
            self.match(tipo_token.FIM)
        elif self.token_atual.tipo == tipo_token.CHAVES_DIREITA:
            self.match(tipo_token.CHAVES_DIREITA)

    # expressões lógicas agora têm prioridade menor que aritméticas
    def expression(self):
        self.simple_expression()
        self.expression_linha()

    def expression_linha(self):
        if self.token_atual.tipo in (tipo_token.IGUAL, tipo_token.DIFERENTE,
                                    tipo_token.MENOR, tipo_token.MAIOR,
                                    tipo_token.MENOR_IGUAL, tipo_token.MAIOR_IGUAL, tipo_token.ATRIBUICAO):
            self.consumir(self.token_atual.tipo)
            self.simple_expression()
            self.expression_linha()
        else:
            #verifica se a expressão se trata de uma expressão lógica
            self.logical_expression_linha()

    def logical_expression(self):
        self.logical_expression_linha()

    def logical_expression_linha(self):
        if self.token_atual.tipo in (tipo_token.SINAL_E, tipo_token.SINAL_OU):
            self.consumir(self.token_atual.tipo)
            self.logical_expression_linha()

    def simple_expression(self):
        self.term()
        self.simple_expression_linha()

    def simple_expression_linha(self):
        if self.token_atual.tipo in (tipo_token.SOMA, tipo_token.SUBTRACAO):
            self.consumir(self.token_atual.tipo)
            self.term()
            self.simple_expression_linha()
        else:
            return

    def term(self):
        self.factor()
        self.term_linha()

    def term_linha(self):
        if self.token_atual.tipo in (tipo_token.MULTIPLICACAO, tipo_token.DIVISAO):
            self.consumir(self.token_atual.tipo)
            self.factor()
            self.term_linha()  # Recursão à direita
        else:
            return

    def factor(self):
        if self.token_atual.tipo in (
                tipo_token.IDENTIFICADOR,
                tipo_token.INUM,
                tipo_token.FNUM,
                tipo_token.IF
        ):
            self.consumir(self.token_atual.tipo)
        elif self.token_atual.tipo == tipo_token.PARENTESES_ESQUERDO:
            self.consumir(tipo_token.PARENTESES_ESQUERDO)
            self.expression()
            self.consumir(tipo_token.PARENTESES_DIREITO)
        else:
            raise SyntaxError(
                "Erro de sintaxe: fator inválido. "
                f"Encontrado: {nomes_token[self.token_atual.tipo.value - 1]}"
            )

    #vai "pulando" os espaços em branco para poder ir para o próximo token
    def proximo_token(self, entrada):
      while entrada:
        if entrada[0].isspace():
            entrada = entrada[1:]
            continue
        else:
            break
      if not entrada:
        return criarToken(tipo_token.FIM, ""), ""

      # Verifica cada tipo de token
      if entrada.startswith("int"):
        return criarToken(tipo_token.INT, 'int'), entrada[3:]
      if entrada.startswith("float"):
        return criarToken(tipo_token.FLOAT, 'float'), entrada[5:]
      elif entrada.startswith("printf"):
        return criarToken(tipo_token.PRINTF, 'printf'), entrada[6:]
      elif entrada.startswith("=="):
        return criarToken(tipo_token.IGUAL, '=='), entrada[2:]
      elif entrada[0] == '=':
        return criarToken(tipo_token.ATRIBUICAO, '='), entrada[1:]
      elif entrada[0] == '+':
        return criarToken(tipo_token.SOMA, '+'), entrada[1:]
      elif entrada[0] == '-':
        return criarToken(tipo_token.SUBTRACAO, '-'), entrada[1:]
      elif entrada[0] == '/':
        return criarToken(tipo_token.DIVISAO, '/'), entrada[1:]
      elif entrada[0] == '*':
        return criarToken(tipo_token.MULTIPLICACAO, '*'), entrada[1:]
      elif entrada[0] == '(':
        return criarToken(tipo_token.PARENTESES_ESQUERDO, '('), entrada[1:]
      elif entrada[0] == ')':
        return criarToken(tipo_token.PARENTESES_DIREITO, ')'), entrada[1:]
      elif entrada[0] == '{':
        return criarToken(tipo_token.CHAVES_ESQUERDA, '{'), entrada[1:]
      elif entrada[0] == '}':
        return criarToken(tipo_token.CHAVES_DIREITA, '}'), entrada[1:]
      elif entrada[0] == '<':
        return criarToken(tipo_token.MENOR, '<'), entrada[1:]
      elif entrada[0] == '>':
        return criarToken(tipo_token.MAIOR, '>'), entrada[1:]
      elif entrada[0] == 'endif':
        return criarToken(tipo_token.ENDIF, 'endif'), entrada[5:]
      elif entrada[0] == '$':
        return criarToken(tipo_token.FIM, '$'), entrada[1:]
      elif entrada.startswith("if"):
        return criarToken(tipo_token.IF, "if"), entrada[2:]
      elif entrada.startswith("else"):
        return criarToken(tipo_token.ELSE, "else"), entrada[4:]
      elif entrada.startswith("while"):
        return criarToken(tipo_token.WHILE, "while"), entrada[5:]
      if entrada.startswith("&&"):
        return criarToken(tipo_token.SINAL_E, '&&'), entrada[2:]
      if entrada.startswith("||"):
        return criarToken(tipo_token.SINAL_OU, '||'), entrada[2:]
      if entrada.startswith("!="):
        return criarToken(tipo_token.DIFERENTE, '!='), entrada[2:]
      if entrada.startswith("<="):
        return criarToken(tipo_token.MENOR_IGUAL, '<='), entrada[2:]
      if entrada.startswith(">="):
        return criarToken(tipo_token.MAIOR_IGUAL, '>='), entrada[2:]
      #Caso onde a entrada é um dígito
      elif entrada[0].isdigit():
        inicio = 0
        while inicio < len(entrada) and entrada[inicio].isdigit():
          inicio += 1
        if inicio < len(entrada) and entrada[inicio] == '.':
          inicio += 1
          while inicio < len(entrada) and entrada[inicio].isdigit():
            inicio += 1
          return criarToken(tipo_token.FNUM, entrada[:inicio]), entrada[inicio:]
        return criarToken(tipo_token.INUM, entrada[:inicio]), entrada[inicio:]
      #Caso onde a entrada é uma palavra (Identificador)
      elif entrada[0].isalpha():
        inicio = 0
        while inicio < len(entrada) and entrada[inicio].isalpha():
          inicio += 1
        return criarToken(tipo_token.IDENTIFICADOR, entrada[:inicio]), entrada[inicio:]
      else:
        return criarToken(tipo_token.VAZIO, ""), entrada[1:]

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


def build_grammar():
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
  grammar.add_nonterminal('lista_statement')
  grammar.add_nonterminal('statement')
  grammar.add_nonterminal('declaration')
  grammar.add_nonterminal('declarationList')
  grammar.add_nonterminal('declaration_int')
  grammar.add_nonterminal('declaration_float')
  grammar.add_nonterminal('assignment')
  grammar.add_nonterminal('if_statement')
  grammar.add_nonterminal('elseStatement')
  grammar.add_nonterminal('while_statement')
  grammar.add_nonterminal('expression')
  #grammar.add_nonterminal('relationalExpression')
  #grammar.add_nonterminal('relationalOperator')
  grammar.add_nonterminal('logical_expression')
  grammar.add_nonterminal('logical_expression_linha')
  grammar.add_nonterminal('logicalOperator')
  grammar.add_nonterminal('simple_expression')
  #grammar.add_nonterminal('additiveOperator')
  grammar.add_nonterminal('term')
  grammar.add_nonterminal('term_linha')
  grammar.add_nonterminal('multiplicativeOperator')
  grammar.add_nonterminal('factor')
  grammar.add_nonterminal('simple_expression_linha')
  grammar.add_nonterminal('statements_finais')


  grammar.add_production('program', ['declarationList','lista_statement'])

# Declarações
  #grammar.add_production('declarationList', ['declaration', 'declarationList'])
  #grammar.add_production('declarationList', [])
  grammar.add_production('declaration', ['declaration_int'])
  grammar.add_production('declaration', ['declaration_float'])
  grammar.add_production('declaration_int', ['INT', 'IDENTIFICADOR'])
  grammar.add_production('declaration_float', ['FLOAT', 'IDENTIFICADOR'])

# Statements
  grammar.add_production('lista_statement', ['statement', 'lista_statement'])
  grammar.add_production('lista_statement', [])

  grammar.add_production('statement', ['if_statement'])
  grammar.add_production('statement', ['while_statement'])
  grammar.add_production('statement', ['assignment'])
  grammar.add_production('statement', ['declaration_int'])
  grammar.add_production('statement', ['declaration_float'])
  #Algum problema aqui que faz a regra não ser LL1
  #grammar.add_production('statement', ['expression'])

  grammar.add_production('statements_finais', ['FIM'])
  grammar.add_production('statements_finais', ['CHAVES_DIREITA'])
  grammar.add_production('statements_finais', ['ENDIF']) 

# Assignment
  grammar.add_production('assignment', ['IDENTIFICADOR', 'ATRIBUICAO', 'expression'])
# IF
  grammar.add_production('if_statement', ['IF', 'PARENTESES_ESQUERDO', 'expression', 'PARENTESES_DIREITO',
                                         'CHAVES_ESQUERDA', 'lista_statement', 'CHAVES_DIREITA', 'elseStatement','ENDIF'])
# Else
  grammar.add_production('elseStatement', ['CHAVES_ESQUERDA', 'lista_statement', 'CHAVES_DIREITA'])
  grammar.add_production('elseStatement', [])

  grammar.add_production('while_statement', ['WHILE', 'PARENTESES_ESQUERDO', 'expression', 'PARENTESES_DIREITO', 'CHAVES_ESQUERDA', 'lista_statement', 'CHAVES_DIREITA'])

  grammar.add_production('expression', ['logical_expression'])

  """grammar.add_production('relationalExpression', ['simple_expression', 'relationalOperator', 'simple_expression'])
  grammar.add_production('relationalOperator', ['IGUAL'])
  grammar.add_production('relationalOperator', ['DIFERENTE'])
  grammar.add_production('relationalOperator', ['MENOR'])
  grammar.add_production('relationalOperator', ['MAIOR'])
  grammar.add_production('relationalOperator', ['MENOR_IGUAL'])
  grammar.add_production('relationalOperator', ['MAIOR_IGUAL'])"""

  grammar.add_production('logical_expression', ['simple_expression', 'logical_expression_linha'])
  grammar.add_production('logical_expression_linha', ['logicalOperator', 'simple_expression'])
  grammar.add_production('logical_expression_linha', [])
  grammar.add_production('logicalOperator', ['SINAL_E'])
  grammar.add_production('logicalOperator', ['SINAL_OU'])

  #Expressão aritmética
  grammar.add_production('simple_expression', ['term', 'simple_expression_linha'])
  grammar.add_production('simple_expression_linha', ['SOMA', 'SUBTRACAO'])
  grammar.add_production('simple_expression_linha', [])

  #Term
  grammar.add_production('term', ['factor', 'multiplicativeOperator', 'term'])
  grammar.add_production('term_linha', ['multiplicativeOperator', 'term'])
  grammar.add_production('term_linha', [])

  grammar.add_production('multiplicativeOperator', ['MULTIPLICACAO'])
  grammar.add_production('multiplicativeOperator', ['DIVISAO'])

  grammar.add_production('factor', ['IDENTIFICADOR'])
  grammar.add_production('factor', ['INUM'])
  grammar.add_production('factor', ['FNUM'])
  grammar.add_production('factor', ['PARENTESES_ESQUERDO'])
  grammar.add_production('factor', ['PARENTESES_DIREITO'])
  #a linguagem não vai sustentar expressões lógicas com outra expressão lógica entre parênteses
  return grammar

def main():
    g = build_grammar()
    pred_alg = predict.predict_algorithm(g)
    #print(ll1_check.is_ll1(g,pred_alg))
    entrada = "while(x||x){x=x+1}"
    #entrada = 'a = 1'
    parser = Parser(entrada)
    try:
        parser.program()
        if parser.token_atual.tipo == tipo_token.FIM:
            print("Análise sintática concluída com sucesso!")
        else:
            print("Erro na análise sintática")
    except SyntaxError as e:
        print(e)

#teste github desktop
if __name__ == "__main__":
    main()