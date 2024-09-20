class token_sequence:
    def __init__(self,ts:list) -> None:
        self.__ts = ts
        self.__idx = 0

    def peek(self)->str:
        print("Posição atual no token_sequence:", self.__idx)  # Nova linha
        print("Token atual:", self.__ts[self.__idx])  # Nova linha
        return self.__ts[self.__idx]
    
    def advance(self)->None:
        self.__idx =  self.__idx + 1

    def match(self,token:str)-> None:
        print(self.peek())
        if self.peek() == token:
            self.advance()
        else:
            print('Erro sintático, era esperado o token : ',token)
            exit(0)