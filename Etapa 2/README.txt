Os algoritmos responsáveis por pegar e separar as informações do autômato disponibilizadas no
txt, bem como os de reconhecimento e determinização de autômatos não-determinísticos, podem
ser encontrados no arquivo TrabFormais2.py, assim como a explicação destes algoritmos através
de comentários.

------------------------------------------------------------------------------------------------

Algumas considerações sobre as funções:

A função recursao() vai ser chamada pela função converte() e iniciará com uma lista de estados 
visitados vazia, além de iniciar a recursão pelo estado inicial.

- Estado Q tratado como uma lista de estados q que converte() posteriormente juntará em uma 
string única
- Checa se o estado Q já foi visitado (retornado a recursão em caso afirmativo), se não, 
adiciona na lista de visitados
- Itera sobre todos os símbolos para cada estado q daquela lista checando quais os estados 
atingíveis pelos q de Q
- Se nenhum estado for atingível, pula para o próximo símbolo
- Caso contrário, ordena a lista para que um Q [q1,q0] seja tratado da mesma forma que um 
Q [q0,q1], p. ex. e chama a recursão para aquele novo estado

Obs: nessas itereções, considerar que um novo automato (a versão determinística) está sendo 
construído e portanto devemos acrescentar os símbolos e devidas transições a ele.


A função converte vai simplesmente pegar o resultado da função recursao (o autômato 
determinístico) e transformar os estados Q, representados por um lista, em uma única string, 
concatenando todos estes estados. 
Além disso, irá instanciar cada novo estado final verificando para quais estados do autômato 
determinístico, os estados finais do autômato não-determinístico aparecem como substring

------------------------------------------------------------------------------------------------

GUIA DE USO:

Para utilizar o programa na versão console, basta abrir o executável TrabFormais2.exe e inserir 
o nome do arquivo no qual o automato está contido COM A EXTENSÃO (.txt)
O Automato que criamos na primeira parte do trabalho está salvo dentro do arquivo automatop.txt


Para utilizar o programa na versão com interface gráfica, basta carregar o txt definindo o 
autômato que se deseja "determinizar" e adicionar (utilizando o botão de Adicionar) palavra
por palavra, separando seus símbolos por vírgula. Após adicionar todas as palavras que se 
deseja verificar aceitação/rejeição, basta clickar no botão Reconhecer para obter os resultados.
Caso se deseja outro autômato, basta carregá-lo, novamente, utilizando
o menu > File > Inserir Autômato.


------------------------------------------------------------------------------------------------

O trabalho foi feito por Rafael Ferreira, Felipe Colombelli e Daives K. Chu