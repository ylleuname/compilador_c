
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
    print("entrei em factor")
    if ts.peek() in p.predict(91):
        ts.match('INUM')
    elif ts.peek() in p.predict(92):
        ts.match('FNUM')
    elif ts.peek() in p.predict(93):
        ts.match('PARENTESES_ESQUERDO')
    elif ts.peek() in p.predict(94):
        ts.match('PARENTESES_DIREITO')
    else:
        return


def multiplicative_operator(ts: token_sequence, p: predict_algorithm):
    print("entrei em multiplicative_operator -->", ts.peek())
    if ts.peek() in p.predict(89):
        ts.match('MULTIPLICACAO')
    elif ts.peek() in p.predict(90):
        ts.match('DIVISAO')
    else:
        return


def term(ts: token_sequence, p: predict_algorithm):
    print("estive aqui --> ", ts.peek(), p.predict(87))
    if ts.peek() in p.predict(88):
        print("entrei em term")
        factor(ts, p)
        multiplicative_operator(ts, p)
        print("passei")
        term(ts, p)
    elif ts.peek() in p.predict(88):
        print("sai do term")
        return


def simple_expression_linha(ts: token_sequence, p: predict_algorithm):
    print("Entrei em simple_expression_linha -->",ts.peek(), p.predict(85))
    if ts.peek() in p.predict(85):
        print("entrei em simple_expression_linha SOMA")
        ts.match('SOMA')
    elif ts.peek() in p.predict(86):
        print("entrei em simple_expression_linha SUB")
        ts.match('SUBTRACAO')
    elif ts.peek() in p.predict(87):
        return


def simple_expression(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(84):
        print("entrei em simple_expression")
        term(ts, p)
        simple_expression_linha(ts, p)
    elif ts.peek() in p.predict(84):
        return


def logical_operator(ts: token_sequence, p: predict_algorithm):
    print("entrei em logical_operator -->", ts.peek())
    if ts.peek() in p.predict(76):
        ts.match('SINAL_E')
    elif ts.peek() in p.predict(77):
        ts.match('SINAL_OU')
    elif ts.peek() in p.predict(78):
        ts.match('IGUAL')
    elif ts.peek() in p.predict(79):
        ts.match('DIFERENTE')
    elif ts.peek() in p.predict(80):
        ts.match('MENOR')
    elif ts.peek() in p.predict(81):
        ts.match('MAIOR')
    elif ts.peek() in p.predict(82):
        ts.match('MENOR_IGUAL')
    elif ts.peek() in p.predict(83):
        ts.match('MAIOR_IGUAL')
    elif ts.peek() in p.predict(76) or ts.peek() in p.predict(77) or ts.peek() in p.predict(78) or ts.peek() in p.predict(79) or ts.peek() in p.predict(80) or ts.peek() in p.predict(81) or ts.peek() in p.predict(82) or ts.peek() in p.predict(83):
        return


def logical_expression_linha(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(74):
        print("entrei em logical_expression_linha -->", ts.peek())
        logical_operator(ts, p)
        simple_expression(ts, p)
    elif ts.peek() in p.predict(75):
        return


def logical_expression(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(73):
        print("entrei em logical_expression")
        simple_expression(ts, p)
        logical_expression_linha(ts, p)
    elif ts.peek() in p.predict(73):
        return


def statements_finais(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(64):
        print("entrei em fim")
        ts.match('FIM')
    elif ts.peek() in p.predict(65):
        print("entrei em chaves_direita")
        ts.match('CHAVES_DIREITA')
    elif ts.peek() in p.predict(66):
        print("entrei em endif")
        ts.match('ENDIF')
    elif ts.peek() in p.predict(64) or ts.peek() in p.predict(65) or ts.peek() in p.predict(66):
        return


def expression(ts: token_sequence, p: predict_algorithm):
    print("entrei em expression-->", ts.peek(), p.predict(72))
    if ts.peek() in p.predict(72):
        print("entrei em expression")
        logical_expression(ts, p)
        assignment(ts, p)
    elif ts.peek() in p.predict(72):
        return


def assignment(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(67):
        print("entrei em assignment")
        ts.match('IDENTIFICADOR')
        ts.match('ATRIBUICAO')
        expression(ts, p)
        statements_finais(ts, p)
    elif ts.peek() in p.predict(67):
        return


def while_statement(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(71):
        print("entrei em while")
        ts.match('WHILE')
        ts.match('PARENTESES_ESQUERDO')
        expression(ts, p)
        #ts.match('PARENTESES_DIREITO')
        ts.match('CHAVES_ESQUERDA')
        lista_statement(ts, p)
        statements_finais(ts, p)
    elif ts.peek() in p.predict(71):
        return


def else_statement(ts: token_sequence, p: predict_algorithm):
    print("chamei else -->", ts.peek(), p.predict(69))
    if ts.peek() in p.predict(69):
        print("entrei em else")
        ts.match('ELSE')
        ts.match('CHAVES_ESQUERDA')
        lista_statement(ts, p)
        statements_finais(ts, p)
    elif ts.peek() in p.predict(70):
        return


def if_statement(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(68):
        ts.match('IF')
        ts.match('PARENTESES_ESQUERDO')
        expression(ts, p)
        #print("sai do expression")
        #ts.match('PARENTESES_DIREITO')
        #print("sai do PARENTESES_DIREITO")
        ts.match('CHAVES_ESQUERDA')
        lista_statement(ts, p)
        statements_finais(ts, p)
        else_statement(ts, p)
        statements_finais(ts, p)
    elif ts.peek() in p.predict(68):
        return


def statement(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(60):
        print("entrei em if statement - statement")
        if_statement(ts, p)
    elif ts.peek() in p.predict(61):
        print("entrei em while - statement")
        while_statement(ts, p)
    elif ts.peek() in p.predict(62):
        print("entrei em assignment -statement")
        assignment(ts, p)
    elif ts.peek() in p.predict(63):
        print("entrei em expression -statement")
        expression(ts, p)
    elif ts.peek() in p.predict(60) or ts.peek() in p.predict(61) or ts.peek() in p.predict(62) or ts.peek() in p.predict(63):
        return


def lista_statement(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(58):
        print("entrei em lista statement")
        statement(ts, p)
        lista_statement(ts, p)
    elif ts.peek() in p.predict(59):
        return


def declaration_int(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(56):
        print("entrei em declarações int")
        ts.match('INT')
        ts.match('IDENTIFICADOR')
        statements_finais(ts, p)
    elif ts.peek() in p.predict(56):
        return


def declaration_float(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(57):
        print("entrei no float")
        ts.match('FLOAT')
        ts.match('IDENTIFICADOR')
        statements_finais(ts, p)
    elif ts.peek() in p.predict(57):
        return

def declarations(ts:token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(54):
        print("entrei em declaration declaration_int")
        declaration_int(ts, p)
    elif ts.peek() in p.predict(55):
        print("entrei em declaration declaration_float")
        declaration_float(ts, p)
    elif ts.peek() in p.predict(50):
        return


def lista_declaration(ts: token_sequence, p: predict_algorithm):
    if ts.peek() in p.predict(52):
        print("entrei em lista_declaration")
        declarations(ts, p)
        lista_declaration(ts, p)
    elif ts.peek() in p.predict(53):
        return


def program(ts: token_sequence, p: predict_algorithm):
    print(ts)
    if ts.peek() in p.predict(51):
        print("iniciei o programa de verdade")
        lista_declaration(ts, p)
        lista_statement(ts, p)
        ts.match('$')
    elif ts.peek() in p.predict(51):
        return

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

    def print_production_ids(self):
        """Imprime o ID de cada produção."""
        for production_id, production_data in self.__productions.items():
            print(f"ID da produção: {production_id}")
            print(f"  lhs: {production_data['lhs']}")
            print(f"  rhs: {production_data['rhs']}")


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
  grammar.add_terminal('$')

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
  grammar.add_nonterminal('declarations')


  # Início do compilador: Program chama program e a lista de declarações
  grammar.add_production('program', ['lista_declaration', 'lista_statement', '$'])  # 50
  grammar.add_production('lista_declaration', ['declarations', 'lista_declaration'])  # 51
  grammar.add_production('lista_declaration', [])
  grammar.add_production('declarations', ['declaration_int'])
  grammar.add_production('declarations', ['declaration_float'])
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
  grammar.add_production('else_statement', ['ELSE', 'CHAVES_ESQUERDA', 'lista_statement', 'statements_finais'])  # 65
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
  grammar.add_production('simple_expression_linha', ['SOMA'])  # 81
  grammar.add_production('simple_expression_linha', ['SUBTRACAO'])  # 81
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

#retorna uma lista de strings
def lexical_analyser(filepath) -> list:
    with open(filepath,'r') as f:
        token_sequence = []
        identificadores_declarados = set()
        declarando = False
        for i, line in enumerate(f, start=1):
            tokens = line.split()
            for t in tokens:
                found = False
                for regex, category in regex_table.items():
                    if re.match(regex, t):
                        #print(regex, category, t)
                        if category == tipo_token.IDENTIFICADOR.name:
                            
                            if declarando:
                                if t in identificadores_declarados:
                                    print(f"Erro: Identificador '{t}' já declarado. Linha: {i}")
                                    exit(0)
                                else:
                                    identificadores_declarados.add(t)
                        token_sequence.append(category)
                        found = True
                        if category in [tipo_token.INT.name, tipo_token.FLOAT.name]:
                            declarando = True
                        elif category == tipo_token.FIM.name:  # Reinicia após ';'
                            declarando = False
                        break
                if not found:
                    print(f"Erro Léxico: '{t}'. Linha: {i}")
                    exit(0)
    token_sequence.append('$')
    return token_sequence


def main():
    filepath = 'programa.ac'
    tokens = lexical_analyser(filepath)
    print(type(tokens))
    ts = token_sequence(tokens)
    g = build_grammar()
    g.print_production_ids()

    #parser = guided_ll1_parser(g)
    #parser.parse(ts)

    predict_alg = predict_algorithm(g)
    print("é LL1: ", ll1_check.is_ll1(g, predict_alg))
    program(ts, predict_alg)


if __name__ == "__main__":
    main()
