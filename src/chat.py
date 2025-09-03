from search import search_prompt

def main():

    pergunta = input("Pergunta: ")
    print("Processando sua pergunta...")
    chain = search_prompt(pergunta)

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    print(chain.content)
    
    print("Execução finalizada.")
    

if __name__ == "__main__":
    main()