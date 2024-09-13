
from enum import Enum
from typing import Iterable, Dict, List, Tuple
import ll1_check
import grammar
from predict import predict_algorithm
from token_sequence import token_sequence
from guided_ll1 import guided_ll1_parser
import re


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
#começar: tabelas de signos q vai ter o nome de cada variavel com um endereço único
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



# Funções do Parser
def factor(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(86):
        ts.match('INUM')
    elif ts.peek() in p.predict(87):
        ts.match('FNUM')
    elif ts.peek() in p.predict(88):
        ts.match('PARENTESES_ESQUERDO')
    elif ts.peek() in p.predict(89):
        ts.match('PARENTESES_DIREITO')
    else:
        return


def multiplicative_operator(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(84):
        ts.match('MULTIPLICACAO')
    elif ts.peek() in p.predict(85):
        ts.match('DIVISAO')
    else:
        return


def term(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(83):
        factor(ts, p)
        multiplicative_operator(ts, p)
        term(ts, p)
    elif ts.peek() in p.predict(83):
        return


def simple_expression_linha(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(81):
        ts.match('SOMA')
        ts.match('SUBTRACAO')
    elif ts.peek() in p.predict(82):
        return


def simple_expression(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(80):
        term(ts, p)
        simple_expression_linha(ts, p)
    elif ts.peek() in p.predict(80):
        return


def logical_operator(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(72):
        ts.match('SINAL_E')
    elif ts.peek() in p.predict(73):
        ts.match('SINAL_OU')
    elif ts.peek() in p.predict(74):
        ts.match('IGUAL')
    elif ts.peek() in p.predict(75):
        ts.match('DIFERENTE')
    elif ts.peek() in p.predict(76):
        ts.match('MENOR')
    elif ts.peek() in p.predict(77):
        ts.match('MAIOR')
    elif ts.peek() in p.predict(78):
        ts.match('MENOR_IGUAL')
    elif ts.peek() in p.predict(79):
        ts.match('MAIOR_IGUAL')
    elif ts.peek() in p.predict(72) or ts.peek() in p.predict(73) or ts.peek() in p.predict(74) or ts.peek() in p.predict(75) or ts.peek() in p.predict(76) or ts.peek() in p.predict(77) or ts.peek() in p.predict(78) or ts.peek() in p.predict(79):
        return


def logical_expression_linha(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(70):
        logical_operator(ts, p)
        simple_expression(ts, p)
    elif ts.peek() in p.predict(71):
        return


def logical_expression(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(69):
        simple_expression(ts, p)
        logical_expression_linha(ts, p)
    elif ts.peek() in p.predict(69):
        return


def statements_finais(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(60):
        ts.match('FIM')
    elif ts.peek() in p.predict(61):
        ts.match('CHAVES_DIREITA')
    elif ts.peek() in p.predict(62):
        ts.match('ENDIF')
    elif ts.peek() in p.predict(60) or ts.peek() in p.predict(61) or ts.peek() in p.predict(62):
        return


def expression(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(68):
        logical_expression(ts, p)
        assignment(ts, p)
    elif ts.peek() in p.predict(68):
        return


def assignment(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(63):
        ts.match('IDENTIFICADOR')
        ts.match('ATRIBUICAO')
        expression(ts, p)
        statements_finais(ts, p)
    elif ts.peek() in p.predict(63):
        return


def while_statement(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(67):
        ts.match('WHILE')
        ts.match('PARENTESES_ESQUERDO')
        expression(ts, p)
        ts.match('PARENTESES_DIREITO')
        ts.match('CHAVES_ESQUERDA')
        lista_statement(ts, p)
        statements_finais(ts, p)
    elif ts.peek() in p.predict(67):
        return


def else_statement(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(65):
        ts.match('CHAVES_ESQUERDA')
        lista_statement(ts, p)
        statements_finais(ts, p)
    elif ts.peek() in p.predict(66):
        return


def if_statement(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(64):
        ts.match('IF')
        ts.match('PARENTESES_ESQUERDO')
        expression(ts, p)
        ts.match('PARENTESES_DIREITO')
        ts.match('CHAVES_ESQUERDA')
        lista_statement(ts, p)
        else_statement(ts, p)
        statements_finais(ts, p)
    elif ts.peek() in p.predict(64):
        return


def statement(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(56):
        if_statement(ts, p)
    elif ts.peek() in p.predict(57):
        while_statement(ts, p)
    elif ts.peek() in p.predict(58):
        assignment(ts, p)
    elif ts.peek() in p.predict(59):
        expression(ts, p)
    elif ts.peek() in p.predict(56) or ts.peek() in p.predict(57) or ts.peek() in p.predict(58) or ts.peek() in p.predict(59):
        return


def lista_statement(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(54):
        statement(ts, p)
        lista_statement(ts, p)
    elif ts.peek() in p.predict(55):
        return


def declaration_int(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(52):
        ts.match('INT')
        ts.match('IDENTIFICADOR')
        statements_finais(ts, p)
    elif ts.peek() in p.predict(52):
        return


def declaration_float(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(53):
        ts.match('FLOAT')
        ts.match('IDENTIFICADOR')
        statements_finais(ts, p)
    elif ts.peek() in p.predict(53):
        return


def lista_declaration(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(51):
        declaration_int(ts, p)
        declaration_float(ts, p)
    elif ts.peek() in p.predict(51):
        return


def program(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(50):
        lista_declaration(ts, p)
        lista_statement(ts, p)
        ts.match('$')
    elif ts.peek() in p.predict(50):
        return


"""class Parser(Token):
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
        return criarToken(tipo_token.VAZIO, ""), entrada[1:]"""


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
  grammar.add_nonterminal('lista_declaration')
  grammar.add_nonterminal('declaration_int')
  grammar.add_nonterminal('declaration_float')
  grammar.add_nonterminal('assignment')
  grammar.add_nonterminal('if_statement')
  grammar.add_nonterminal('else_statement')
  grammar.add_nonterminal('while_statement')
  grammar.add_nonterminal('expression')
  grammar.add_nonterminal('logical_expression')
  grammar.add_nonterminal('logical_expression_linha')
  grammar.add_nonterminal('logical_operator')
  grammar.add_nonterminal('simple_expression')
  grammar.add_nonterminal('term')
  grammar.add_nonterminal('term_linha')
  grammar.add_nonterminal('multiplicativeOperator')
  grammar.add_nonterminal('factor')
  grammar.add_nonterminal('simple_expression_linha')
  grammar.add_nonterminal('statements_finais')
  #grammar.add_nonterminal('atribuicao_ou_expressao')

  # Início do compilador: Program chama program e a lista de declarações
  grammar.add_production('program', ['lista_declaration', 'lista_statement', '$'])  # 50
  grammar.add_production('lista_declaration', ['declaration_int', 'declaration_float'])  # 51
  grammar.add_production('declaration_int', ['INT', 'IDENTIFICADOR', 'statements_finais'])  # 52
  grammar.add_production('declaration_float', ['FLOAT', 'IDENTIFICADOR', 'statements_finais'])  # 53


  # Lista de statements e Statements
  grammar.add_production('lista_statement', ['statement', 'lista_statement'])  # 54
  grammar.add_production('lista_statement', [])  # 55
  grammar.add_production('statement', ['if_statement'])  # 56
  grammar.add_production('statement', ['while_statement'])  # 57
  grammar.add_production('statement', ['assignment'])  # 58
  grammar.add_production('statement', ['expression'])  # 59

  # Símbolos finais / statements_finais
  grammar.add_production('statements_finais', ['FIM'])  # 60
  grammar.add_production('statements_finais', ['CHAVES_DIREITA'])  # 61
  grammar.add_production('statements_finais', ['ENDIF'])  # 62

  # Assignment
  grammar.add_production('assignment', ['IDENTIFICADOR', 'ATRIBUICAO', 'expression', 'statements_finais'])  # 63

  # Condicional If
  grammar.add_production('if_statement', ['IF', 'PARENTESES_ESQUERDO', 'expression', 'PARENTESES_DIREITO',
                                          'CHAVES_ESQUERDA', 'lista_statement', 'else_statement',
                                          'statements_finais'])  # 64

  # Else
  grammar.add_production('else_statement', ['CHAVES_ESQUERDA', 'lista_statement', 'statements_finais'])  # 65
  grammar.add_production('else_statement', [])  # 66

  # Loop While
  grammar.add_production('while_statement', ['WHILE', 'PARENTESES_ESQUERDO', 'expression', 'PARENTESES_DIREITO',
                                             'CHAVES_ESQUERDA', 'lista_statement', 'statements_finais'])  # 67

  # Expression
  grammar.add_production('expression', ['logical_expression', 'assignment'])  # 68

  # Expressões lógicas e relacionais juntas
  grammar.add_production('logical_expression', ['simple_expression', 'logical_expression_linha'])  # 69
  grammar.add_production('logical_expression_linha', ['logical_operator', 'simple_expression'])  # 70
  grammar.add_production('logical_expression_linha', [])  # 71
  grammar.add_production('logical_operator', ['SINAL_E'])  # 72
  grammar.add_production('logical_operator', ['SINAL_OU'])  # 73
  grammar.add_production('logical_operator', ['IGUAL'])  # 74
  grammar.add_production('logical_operator', ['DIFERENTE'])  # 75
  grammar.add_production('logical_operator', ['MENOR'])  # 76
  grammar.add_production('logical_operator', ['MAIOR'])  # 77
  grammar.add_production('logical_operator', ['MENOR_IGUAL'])  # 78
  grammar.add_production('logical_operator', ['MAIOR_IGUAL'])  # 79

  # Expressões aritméticas (SOMA E SUBTRAÇÃO)
  grammar.add_production('simple_expression', ['term', 'simple_expression_linha'])  # 80
  grammar.add_production('simple_expression_linha', ['SOMA', 'SUBTRACAO'])  # 81
  grammar.add_production('simple_expression_linha', [])  # 82

  # Expressões aritmética (MULTIPLICAÇÃO E DIVISÃO)
  grammar.add_production('term', ['factor', 'multiplicative_operator', 'term'])  # 83
  grammar.add_production('multiplicative_operator', ['MULTIPLICACAO'])  # 84
  grammar.add_production('multiplicative_operator', ['DIVISAO'])  # 85

  # Termos de uma expressão (números e parênteses)
  grammar.add_production('factor', ['INUM'])  # 86
  grammar.add_production('factor', ['FNUM'])  # 87
  grammar.add_production('factor', ['PARENTESES_ESQUERDO'])  # 88
  grammar.add_production('factor', ['PARENTESES_DIREITO'])  # 89

  grammar.add_terminal('$') #90
  grammar.add_production('lista_declaration', []) #91


  #a linguagem não vai sustentar expressões lógicas com outra expressão lógica entre parênteses
  return grammar



regex_table = {
    r'^int$': tipo_token.INT.name,
    r'^float$': tipo_token.FLOAT.name,
    r'^printf$': tipo_token.PRINTF.name,
    r'^if$': tipo_token.IF.name,
    r'^else$': tipo_token.ELSE.name,
    r'^endif$': tipo_token.ENDIF.name,
    r'^while$': tipo_token.WHILE.name,
    r'^==$': tipo_token.IGUAL.name,
    r'^=$': tipo_token.ATRIBUICAO.name,
    r'^\+$': tipo_token.SOMA.name,
    r'^\-$': tipo_token.SUBTRACAO.name,
    r'^\/$': tipo_token.DIVISAO.name,
    r'^\*$': tipo_token.MULTIPLICACAO.name,
    r'^\($': tipo_token.PARENTESES_ESQUERDO.name,
    r'^\)$': tipo_token.PARENTESES_DIREITO.name,
    r'^\{$': tipo_token.CHAVES_ESQUERDA.name,
    r'^\}$': tipo_token.CHAVES_DIREITA.name,
    r'^<$': tipo_token.MENOR.name,
    r'^>$': tipo_token.MAIOR.name,
    r'^&&$': tipo_token.SINAL_E.name,
    r'^\|\|$': tipo_token.SINAL_OU.name,
    r'^!=$$': tipo_token.DIFERENTE.name,
    r'^<=$$': tipo_token.MENOR_IGUAL.name,
    r'^>=$$': tipo_token.MAIOR_IGUAL.name,
    r'^;$': tipo_token.FIM.name,
    r'^[a-zA-Z_][a-zA-Z_]*$': tipo_token.IDENTIFICADOR.name,
    r'^[0-9]+$': tipo_token.INUM.name,
    r'^[0-9]+\.[0-9]+$': tipo_token.FNUM.name,
}


def lexical_analyser(filepath) -> str:
    with open(filepath,'r') as f:
        token_sequence = []
        tokens = []
        for line in f:
            tokens = tokens + line.split(' ')
        for t in tokens:
            found = False
            for regex,category in regex_table.items():
                if re.match(regex,t):
                    token_sequence.append(category)
                    found=True
                    break
            if not found:
                print('Lexical error: ',t)
                exit(0)
    token_sequence.append('$')
    return token_sequence


def main():
    filepath = 'teste.ac'
    tokens = lexical_analyser(filepath)
    print(tokens)
    ts = token_sequence(tokens)
    g = build_grammar()

    parser = guided_ll1_parser(g)
    parser.parse(ts)

    """pred_alg = predict_algorithm(g)
    #print(ll1_check.is_ll1(g, pred_alg))
    parser = Parser(entrada)
    try:
        program(parser, pred_alg)
        if parser.token_atual.tipo == tipo_token.FIM:
            print("Análise sintática concluída com sucesso!")
        else:
            print("Erro na análise sintática")
    except SyntaxError as e:
        print(e)
    """

#teste github desktop
if __name__ == "__main__":
    main()