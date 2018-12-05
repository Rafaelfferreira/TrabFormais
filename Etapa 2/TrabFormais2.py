import re #biblioteca para realizar buscas dentro do arquivo texto
import os
import copy

#Classe do automato de entrada (não deterministico)
class automato:
    def __init__(self, arqtxt): #recebe como parametro um arquivo texto contendo o automato

        #Retorna os simbolos do alfabeto, os estados do automato, o estado inicial e os estados finais
        quadrupla = re.search("\(.*?\)",arqtxt) #Procura a parte da string entre parenteses e a retorna (com os parenteses) dentro de um objeto match
        quadrupla = quadrupla.group(0) #Extrai a string do objeto match
        quadrupla = quadrupla[1:len(quadrupla)-1] #Retira os parenteses do começo e do final

        #filtra os estados
        simbolos = re.search("\{.*?\}", quadrupla)
        simbolos = simbolos.group(0)
        simbolos = simbolos[1:len(simbolos)-1]
        self.simbolos = simbolos.split(',')  #Salva os simbolos do objeto automato

        tripla = quadrupla[len(simbolos)+3:] #passa para a variavel tripla a variavel quadrupla menos os estados

        #filtra os simbolos
        estados = re.search("\{.*?\}", tripla)
        estados = estados.group(0)
        estados = estados[1:len(estados)-1]
        self.estados = estados.split(',') #Salva os estados do objeto automato

        dupla = tripla[len(estados)+3:] #passa para a variavel dupla a variavel tripla menos os simbolos

        #filtra o estado inicial
        restante = dupla.split(',')
        self.inicial = restante[0]
        if(len(restante) == 2):
            self.finais = restante[1]
        else:
            #filtra os estados finais
            finais = dupla[len(self.inicial)+1:]
            finais = finais[1:len(finais)-1]
            self.finais = finais.split(',')

        #Salva a tabela de transição como uma lista de listas
        #Da um slice em dados a partir do index inicial da palavra Prog + o tamanho da palavra prog + 1 (pois tem um '\n' dps de prog)
        transitiv_raw = (arqtxt[arqtxt.index('Prog') + len('Prog') + 1:])
        transitiv_raw = transitiv_raw.split('\n') #salva cada elemento em uma linha

        transitiv = [] #inicializa a lista vazia que vai armazenar a tabela de transitividade
        for x in transitiv_raw: #itera por cada elemento da tabela de transitividade
            inst = [] #inicializa a lista que vai salvar os 3 elemento de cada transição
            x = x.split('=') #divide o estado inicial + entrada do estado resultante

            atual = x[0][1:len(x[0])-1] #salva na variavel atual o estado atual + a variavel de entrada sem os parenteses
            atual = atual.split(',') #faz com que atual contenha uma lista contendo o estado atual e a variavel
            inst.append(atual[0]) #salva o estado atual
            inst.append(atual[1]) #salva a variavel da transição
            inst.append(x[1]) #salva o estado resultante no terceiro espaço da lista

            transitiv.append(inst) #salva a lista interna na lista externa
        self.transitiv = transitiv

#classe que vai conter o automato determinístico
class automatoP:
    def __init__(self,automato):
        self.estados = []
        self.simbolos = []
        self.inicial  = automato.inicial #Já é instanciado com o mesmo estado inicial do automato de entrada
        self.finais = []
        self.transitiv = []

def recursao(estado, simbolos, transicoes, visited, automatoDFA):

    # se o estado já foi checado e tratado, simplesmente retorna e continua a recursão
    if estado in visited:
        return


    # caso não, antes de tratá-lo, a primeira coisa para garantir que a recursão não entre em loop é justamente sinalizar como já visitado:
    visited.append(estado)

    for simbolo in simbolos:

        # coleta todos os estados alcançáveis por aquele determinado estado recebendo aquele determinado símbolo
        listaEstadosAlcancados = []

        # o estado sempre será tratado como uma lista de estados (que depois serão concatenados em um único):
        for e in estado:
            for t in range(len(transicoes)):
                # checa nas transições se é o estado e a transição atuais e se o resultado já não está na lista de estados alcançados
                if (e == transicoes[t][0]) and (simbolo == transicoes[t][1]) and not (transicoes[t][2] in listaEstadosAlcancados):
                    listaEstadosAlcancados.append(transicoes[t][2])


        #  checa se a lista de estados alcançados é vazia
        if not listaEstadosAlcancados:
            continue   # se for, skipa  uma iteração


        # sempre dá um sort pra garantir que não se criará um estado novo que na verdade é igual a um já existente
        listaEstadosAlcancados.sort()
        # depois dessa coleta, essa lista de estados vai virar um estado só do  automato determinístico final
        automatoDFA.transitiv.append([estado, simbolo, listaEstadosAlcancados])
        if not(simbolo in automatoDFA.simbolos):
            automatoDFA.simbolos.append(simbolo)  # adiciona o simbolo atual ao automato determinístico final
        if not(estado in automatoDFA.estados):
            automatoDFA.estados.append(estado)   # adiciona  o estado atual ao automato determinístico final

        recursao(listaEstadosAlcancados, simbolos, transicoes, visited, automatoDFA)

#função que faz a conversão do automato ND para Deterministico
def converte(arquivo):
    openfile = open(arquivo,"r", encoding="utf-8",) #Lembrar de incluir o encoding para que ele leia os acentos corretamente
    dados = openfile.read()

    automatoND = automato(dados) #le o arquivo e cria um automato nao deterministico
    automatoDFA = automatoP(automatoND) #instancia o automato deterministico

    visited = [] #estados  já visitados

    recursao([automatoDFA.inicial], automatoND.simbolos, automatoND.transitiv, visited, automatoDFA) #preenche o automato deterministico

    # agora temos que transformar as listas de estados em um estado só representado pela concatenação dos itens da lista:
    # primeiro na lista de estados:
    counter = 0
    for estado in automatoDFA.estados:
        if type(estado) == list:   # se for um estado ou mais em forma de lista, converte
            string = ""
            for q in estado:   # para cada estado dentro desse estado que deveria ser único, concatena-os
                string = string+q
            automatoDFA.estados[counter] = string
        counter +=1


    # depois fazemos o mesmo para as transições:
    counter = 0
    for trans in automatoDFA.transitiv:
        # trata estado atual da transição
        if type(trans[0]) == list:   # se for um estado ou mais em forma de lista, converte
            string = ""
            for q in trans[0]:   # para cada estado dentro desse estado que deveria ser único, concatena-os
                string = string+q
            automatoDFA.transitiv[counter][0] = string

        # trata estado final da transição
        if type(trans[2]) == list:   # se for um estado ou mais em forma de lista, converte
            string = ""
            for q in trans[2]:   # para cada estado dentro desse estado que deveria ser único, concatena-os
                string = string+q
            automatoDFA.transitiv[counter][2] = string
        counter += 1

    # os estados finais serão todos aqueles que tiverem o próprio final do NFA ou algum estados agrupado com o final:
    for estado in automatoDFA.estados:
        # aqui só faz um teste para saber se existe apenas um final, neste caso deve-se passar uma lista desse um elemento
        finais = automatoND.finais
        if type(finais) == str: #transforma em uma lista de 1 elemento se o estado final for unico
            finais = [finais]

        for efinal in finais:
            if (efinal in estado) and (not(estado in automatoDFA.finais)): #procura a substring efinal nos estado e confere se ele ja nao esta salvo com um estado final do automato deterministico
                automatoDFA.finais.append(estado)

    return automatoDFA

def checaSeAceita(automato,palavra):

    # começa no estado inicial sempre
    eAtual = automato.inicial

    # vai lendo os simbolos da palavra e tentando percorrer o autômato
    for simbolo in palavra:
        transValida = False   # se encontrar uma transição válida, muda
        # procura uma transição válida na lista de transições
        for trans in automato.transitiv:
            # se o simbolo e a palavra são uma transição válida, atualiza o estado atual e passa para o próximo símbolo
            if (eAtual == trans[0]) and (simbolo == trans[1]):
                eAtual = trans[2]
                transValida = True
                break

        if transValida:
            continue   # vai para o próximo símbolo

        # se não encontrar, retorna com "REJEITA"
        return "REJEITA"


    # se finalizou-se o loop sem retornar "REJEITA", testa se o estado atual é um estado final
    if eAtual in automato.finais:
        return "ACEITA"

    else:
        return "REJEITA"

#função a ser chamada para passar as palavras que serão testadas
def reconhecimento(automato):
    listaDePalavras = [] #lista de palavras a serem testadas

    print('------- Teste do autômato para reconhecimento ou não de palavras  -------')
    print('Digite uma palavra separando os símbolos por vírgula, sem espaço, para verificar seu reconhecimento:')
    listaDePalavras.append(input())

    while True: #permite a entrada de mais palavras
        print('Deseja fornecer mais palavras? s/n')
        select = input()

        if select == "s":
            print('Digite uma palavra separando os símbolos por vírgula, sem espaço, para verificar seu reconhecimento:')
            listaDePalavras.append(input())
        else:
            break

    print("\n")
    counter = 1
    for palavra in listaDePalavras:
        palavra = palavra.split(",") #salva em palavra uma lista com cada simbolo da palavra de entrada
        print("Palavra "+ str(counter) + ": ", checaSeAceita(automato,palavra))
        counter += 1

#funcao main do programa
def main():
	print('Digite o nome do arquivo texto a ser lido: ')
	nomeArquivo = input()
	automato = converte(nomeArquivo)
	reconhecimento(automato)
	print('\nPressione qualquer tecla para encerrar.')
	input('').split(" ")[0]


if __name__ == "__main__":
	main()



	'''
	Exemplos de palavras que sao aceitas no arquivo automatop.txt:

    Liga,Ficha Inserida,Alavanca,7,Limão,Exibe Mensagem de Derrota,Libera Inserção de Ficha,Desliga
    Liga,Ficha Inserida,Alavanca,Diamante,Diamante,Diamante,Jackpot,Retira Prêmio,Libera Inserção de Ficha,Desliga
    Liga,Ficha Inserida,Alavanca,Diamante,Diamante,7,Exibe Mensagem de Derrota,Libera Inserção de Ficha,Ficha Inserida,Alavanca,7,7,Limão,Exibe Mensagem de Derrota,Libera Inserção de Ficha,Desliga
    Liga,Ficha Inserida,Alavanca,Limão,Limão,Limão,Jackpot,Retira Prêmio,Libera Inserção de Ficha,Ficha Inserida,Alavanca,7,7,7,Jackpot,Retira Prêmio,Libera Inserção de Ficha,Desliga
    Liga,Ficha Inserida,Alavanca,7,7,Cereja,Exibe Mensagem de Derrota,Libera Inserção de Ficha,Desliga

	Exemplos de palavras que sao rejeitadas no arquivo automatop.txt:

    Liga,Retira Prêmio
    Libera Inserção De Ficha,Limão,Limão,7,7,Diamante,Alavanca
    Liga,Ficha Inserida,Retira Prêmio,Desliga
    Liga,Alavanca,Cereja,Cereja,Cereja,Jackpot,Retira Prêmio,Libera Inserção de Ficha,Desliga
    Liga,Liga
	'''
