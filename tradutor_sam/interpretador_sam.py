import re
from typing import Counter

#função de adicionar elemento no topo da stack -- PUSHIMM X
def pushimm(argumento, stack):
  argumento = int(argumento)
  stack.append(argumento)
  print(f"Estado atual da pilha: {stack}")


#função de multiplicação -- TIMES
def times_sam(stack):
	aux1 = stack.pop()
	aux2 = stack.pop()
	stack.append(aux1 * aux2)
	print(f"Estado atual da pilha: {stack}")

#função de adição -- ADD
def add(stack):
	aux1 = stack.pop()
	aux2 = stack.pop()
	stack.append(aux1 + aux2)
	print(f"Estado atual da pilha: {stack}")

#função de subtração -- SUB
def sub(stack):
	aux1 = stack.pop()
	aux2 = stack.pop()
	stack.append(aux1 - aux2)
	print(f"Estado atual da pilha: {stack}")

#função de adicionar espaços em branco na pilha -- ADDSP X
def addsp(argumento, stack):
	argumento = int(argumento)
	#quando o argumento de addsp for negativo ocorre uma remoção dos x elementos do topo da pilha
	#fazemos a verificação do tamanho da pilha para não dar pop na lista vazia.
	if argumento < 0 and len(stack) >= (argumento*-1):
		for i in range(argumento*(-1)):
			stack.pop()
	else:
		counter = 0
		while counter < argumento:
			stack.append(0)
			counter = counter + 1
	print(f"Estado atual da pilha: {stack}")

#função de armazenar um valor do topo da pilha em uma posição determinada da pilha -- STOREABS X
def storeabs(argumento, stack):
	argumento = int(argumento)
	aux = stack.pop()
	stack.insert(argumento, aux)
	if len(stack) > 0:
		stack.pop()
	print(f"Estado atual da pilha: {stack}")

#função que pega o elemento da posição x da pilha e insere no topo da pilha -- PUSHABS X
def pushabs(argumento, stack):
	argumento = int(argumento)
	aux = stack[argumento]
	stack.append(aux)
	print(f"Estado atual da pilha: {stack}")

#função que retorna 0 se o primeiro valor for maior que o segundo -- GREATER

def greater(stack):
	aux1 = stack.pop()
	aux2 = stack.pop()
	if aux2 < aux1:
		stack.append(0)
	else:
		stack.append(1)
	print(f"Estado atual da pilha: {stack}")

#função que verifica se o valor é igual a 0, se for aloca 1 na pilha -- ISNIL
def isnil(stack):
  aux1 = stack.pop()
  if aux1 == 0:
    stack.append(1)
  else:
    stack.append(0)
  print(f"Estado atual da pilha: {stack}")

def mudar_fluxo_codigo(numero_linha):
	return numero_linha+1

def jumpc(argumento, stack, codigo_completo):
	print(f"Estado atual da pilha: {stack}")
	label = re.compile(r"^\s*([a-zA-Z]+:)$")
	for numero_linha, linha in codigo_completo:
		match = re.match(label, linha)
		if match: 
			return numero_linha + 1
	
			
#função que verifica qual é a instrução SAM
def verificar_instrucao(instrucao, argumento, stack, codigo_completo):
	if (instrucao == "pushimm"):
		pushimm(argumento, stack)
		return 0
	elif (instrucao == "times"):
		times_sam(stack)
		return 0
	elif (instrucao == "add"):
		add(stack)
		return 0
	elif (instrucao == "stop"):
		return 0
	elif (instrucao == "sub"):
		sub(stack)
		return 0
	elif (instrucao == "addsp"):
		addsp(argumento, stack)
		return 0
	elif (instrucao == "storeabs"):
		storeabs(argumento, stack)
		return 0
	elif(instrucao == "pushabs"):
		pushabs(argumento, stack)
		return 0
	elif(instrucao == "greater"):
		greater(stack)
		return 0
	elif(instrucao == "isnil"):
		isnil(stack)
	elif(instrucao == "jumpc"):
		numero_linha_novo = jumpc(argumento, stack, codigo_completo)
		return numero_linha_novo
		

# tem algum problema com a iteração for, por ela iterar tanto em numero_linha quanto linha.
def main():

	stack = []
	identificador_regex = re.compile(r"^\s*([a-zA-Z]+)\s+(.*)")
  
	#abertura do arquivo, leitura completa e enumeração de cada linha
	with open("sam4_5.sam", "r") as arquivo:
		codigo_completo = list(enumerate(arquivo, start=1))
		numero_linha = 1
		while numero_linha <= len(codigo_completo):
			linha = codigo_completo[numero_linha - 1]
			match = re.match(identificador_regex, linha)
			if match:
				#aqui temos o comando SAM
				instrucao: str = match.group(1)
				#argumentos do comando SAM
				argumento = match.group(2)
				if not argumento:
					argumento = "0"

				print(numero_linha, linha, instrucao)
				#verifica qual instrucao foi inserida 
				altera_fluxo = verificar_instrucao(instrucao.lower(), argumento, stack, codigo_completo)
				#verificacao da necessidade de alterar o fluxo do codigo
				if instrucao == "JUMPC":
					numero_linha = altera_fluxo
					print(f"jump para a linha ", numero_linha)
		numero_linha +=1
  
if __name__ == "__main__":
	main()
