from tkinter import *
from tkinter import ttk   # para a combobox
from tkinter import filedialog # para procurar arquivo
from TrabFormais2 import *




def limpaOutputbox():   #simplesmente limpa a outputbox

    output.config(state=NORMAL)   # habilita edição da text box
    output.delete(0.0, END)
    return



# função responsável pela navegação no explorer para achar o txt e carregar o autômato
def carregarAutomato():

    # define-se que vai alterar as variáveis globais abaixo
    global listaDePalavras
    global listaSimbConcatenados
    global automato

    try:   # tenta carregar, ler e converter o autômato
        window.fileName = filedialog.askopenfilename(title="select file", filetypes=(("text files", "*.txt"), ("all files", "*.*")))   # pega nome do arquivo
        automato = converte(window.fileName)
        limpaOutputbox()
        output.config(state=DISABLED) # desabilita edição da text box novamente


    except ValueError:   # caso dê algum problema, avisa na outputbox
        limpaOutputbox()
        output.insert(END, "Erro ao converter o autômato! Certifique-se de adicionar um arquivo válido.\n\n")   # insere resultado
        output.config(state=DISABLED) # desabilita edição da text box novamente


    listaDePalavras.clear()
    listaSimbConcatenados.clear()

    return



# função que checa se o automato aceita ou rejeita a palavra passada para o automato definido globalmente
def reconhecerPalavras():

    # define-se que vai alterar as variáveis globais abaixo
    global listaDePalavras
    global listaSimbConcatenados

    limpaOutputbox()

    # se lista vazia retorna avisando que deve-se inserir palavras
    if not listaDePalavras:

        output.insert(END, "Erro! Você deve inserir palavras a serem reconhecidas pelo autômato.\n\n")   # insere resultado
        output.config(state=DISABLED) # desabilita edição da text box novamente

        listaDePalavras.clear()
        listaSimbConcatenados.clear()

        return



    if not automato:   # caso um automato não tenha  sido carregado e convertido devidamente, avisa na outputbox e retorna

            limpaOutputbox()
            output.insert(END, "Erro! Certifique-se de adicionar um arquivo válido para seu autômato.\n\n")   # insere resultado
            output.config(state=DISABLED) # desabilita edição da text box novamente

            listaDePalavras.clear()
            listaSimbConcatenados.clear()

            return


    counter = 0   # utilizado apenas para indicar na string de saída qual palavra foi/não foi reconhecida (pegando da lista das concatenadas)
    # feitas as validações, checa aceitação do autômato para as palavras inseridas
    for palavra in listaDePalavras:
        palavra = palavra.split(",") # salva em palavra uma lista com cada simbolo da palavra de entrada
        resultado = checaSeAceita(automato, palavra)

        output.config(state=NORMAL)   # habilita edição da text box
        # a string abaixo será num formato:
        # 1. aabba   ACEITA
        output.insert(END, " " + str(counter+1) + ". " + listaSimbConcatenados[counter] + "   " + resultado + "\n\n")   # insere resultado
        output.config(state=DISABLED) # desabilita edição da text box novamente

        counter += 1


    listaDePalavras.clear()
    listaSimbConcatenados.clear()

    return



# função que adiciona mais palavras a serem reconhecidas na lista de palavras
def adicionarPalavra():

    # define-se que vai alterar as variáveis globais abaixo
    global listaDePalavras
    global listaSimbConcatenados

    palavra = input.get()   # pega o input da entrybox
    input.delete(0, 'end')   # deleta o que foi escrito na entrybox


    if palavra == "":   # se o usuário não digitar nada, retorna avisando na box de output

        output.config(state=NORMAL)   # habilita edição da text box
        output.insert(END, "Entrada inválida! Digite a palavra separando os símbolos por vírgulas.\n\n")   # insere resultado
        output.config(state=DISABLED) # desabilita edição da text box novamente

        return

    # caso seja uma entrada válida, junta na lista de palavras a serem reconhecidas
    listaDePalavras.append(palavra)

    # e concatena a string juntando também na lista de palavras com símbolos concatenados
    palavra = palavra.replace(',', '')
    listaSimbConcatenados.append(palavra)

    # avisa na box que a palavra foi adicionada
    output.config(state=NORMAL)   # habilita edição da text box
    output.insert(END, "Palavra adicionada: " + palavra + "\n\n")   # insere texto
    output.config(state=DISABLED) # desabilita edição da text box novamente

    return



# função que apaga a outputbox e mostra os créditos
def showCredits():

    limpaOutputbox()
    output.insert(END, "By\n\nFelipe Colombelli: github.com/colombelli/\nRafael Ferreira: github.com/Rafaelfferreira/\nDaives Kawon Chu: github.com/daivesk/\n\nProjeto: https://github.com/Rafaelfferreira/TrabFormais")
    output.config(state=DISABLED) # desabilita edição da text box novamente


    return






# variável utilizada para carregar o automato e convertê-lo, começa por padrão com o autômato definido como cenário
automato = converte("automatop.txt")

listaDePalavras = []   # cada item é uma palavra onde as strings estão separadas por vírgula
listaSimbConcatenados = []   # cada item é uma palavra (sem as vírgulas), i.e, com símbolos concatenados






'''

    DEFINIÇÕES DA GUI

'''




# main
window = Tk()

# definição do tamanho da janela
width_window = 403
height_window = 425

# pega tamanho da tela do usuário
screenW = window.winfo_screenwidth()
screenH = window.winfo_screenheight()

# coordenadas para centralizar janela
xpos = (screenW/2) - (width_window/2)
ypos = (screenH/2) - (height_window/2)

# seta um título na janela
window.title("Automatop")
# seta tamanho da janela e posição na tela
window.geometry("%dx%d+%d+%d" % (width_window, height_window, xpos, ypos))
# seta cor de fundo da janela
window.configure(background="white")
# bloqueia redimensionamento da janela
window.resizable(width=False, height=False)
# define icone da janela
window.iconbitmap('images/inf_logo.ico')



# Menu para adicionar autômato ou fechar programa
menu = Menu(window) # menu topo da janela
window.config(menu=menu)

subMenu = Menu(menu, tearoff=0) # submenu dropdown
menu.add_cascade(label="File", menu=subMenu)
menu.add_command(label="Credits", command=showCredits)
menu.add_command(label="Exit", command=window.destroy)
subMenu.add_command(label="Carregar Autômato", command=carregarAutomato)





# logo automatop
logo = PhotoImage(file="images/automatop_400.gif")
# o columnspan do grid define que a imagem vai ocupar duas colunas
Label (window, image=logo, bg="white") .grid(row=0, column=0, sticky=EW)
# o columnspan do grid define que a imagem vai ocupar duas colunas
Label (window, text="Digite a palavra separando os símbolos por vírgula:", bg="white", fg="black", font="Arial 10") .grid(row=1, column=0, pady=(10,0), sticky=EW)

# caixa de input
input = Entry(window, font="none 11", bg="white")
input.grid(row=2, column=0, padx=10, sticky=EW)

# botão de adicionar mais palavras
Button(window, text="Adicionar", command=adicionarPalavra) .grid(row=3, column=0, padx=(130,0), pady=10, sticky=W)

# botão de reconhecer palavras
Button(window, text="Reconhecer", command=reconhecerPalavras) .grid(row=3, column=0, padx=(200,0), pady=10, sticky=W)

# cria textbox de output (onde os resultados vão ser printados)
output = Text (window, width=45, height=12, wrap=WORD)
output.grid(row=4, column=0, padx=6, pady=15, sticky=W)
output.insert(END, "")
output.config(state=DISABLED)   # não permite mexer na text box (tem que habilitar para inserir texto mesmo com .insert())
# scrollbar  para textbox:
scrollb = Scrollbar(window, command=output.yview)
scrollb.grid(row=4, column=0, padx=(370,0), pady=15, ipady=72)   # sendo ipady o tamanho da scrollbar
output['yscrollcommand'] = scrollb.set


window.mainloop()
