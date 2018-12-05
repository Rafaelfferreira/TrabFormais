Os algoritmos respons�veis por pegar e separar as informa��es do aut�mato disponibilizadas no
txt, bem como os de reconhecimento e determiniza��o de aut�matos n�o-determin�sticos, podem
ser encontrados no arquivo TrabFormais2.py, assim como a explica��o destes algoritmos atrav�s
de coment�rios.

------------------------------------------------------------------------------------------------

Algumas considera��es sobre as fun��es:

A fun��o recursao() vai ser chamada pela fun��o converte() e iniciar� com uma lista de estados 
visitados vazia, al�m de iniciar a recurs�o pelo estado inicial.

- Estado Q tratado como uma lista de estados q que converte() posteriormente juntar� em uma 
string �nica
- Checa se o estado Q j� foi visitado (retornado a recurs�o em caso afirmativo), se n�o, 
adiciona na lista de visitados
- Itera sobre todos os s�mbolos para cada estado q daquela lista checando quais os estados 
ating�veis pelos q de Q
- Se nenhum estado for ating�vel, pula para o pr�ximo s�mbolo
- Caso contr�rio, ordena a lista para que um Q [q1,q0] seja tratado da mesma forma que um 
Q [q0,q1], p. ex. e chama a recurs�o para aquele novo estado

Obs: nessas itere��es, considerar que um novo automato (a vers�o determin�stica) est� sendo 
constru�do e portanto devemos acrescentar os s�mbolos e devidas transi��es a ele.


A fun��o converte vai simplesmente pegar o resultado da fun��o recursao (o aut�mato 
determin�stico) e transformar os estados Q, representados por um lista, em uma �nica string, 
concatenando todos estes estados. 
Al�m disso, ir� instanciar cada novo estado final verificando para quais estados do aut�mato 
determin�stico, os estados finais do aut�mato n�o-determin�stico aparecem como substring

------------------------------------------------------------------------------------------------

GUIA DE USO:

Para utilizar o programa na vers�o console, basta abrir o execut�vel TrabFormais2.exe e inserir 
o nome do arquivo no qual o automato est� contido COM A EXTENS�O (.txt)
O Automato que criamos na primeira parte do trabalho est� salvo dentro do arquivo automatop.txt


Para utilizar o programa na vers�o com interface gr�fica, basta carregar o txt definindo o 
aut�mato que se deseja "determinizar" e adicionar (utilizando o bot�o de Adicionar) palavra
por palavra, separando seus s�mbolos por v�rgula. Ap�s adicionar todas as palavras que se 
deseja verificar aceita��o/rejei��o, basta clickar no bot�o Reconhecer para obter os resultados.
Caso se deseja outro aut�mato, basta carreg�-lo, novamente, utilizando
o menu > File > Inserir Aut�mato.


------------------------------------------------------------------------------------------------

O trabalho foi feito por Rafael Ferreira, Felipe Colombelli e Daives K. Chu