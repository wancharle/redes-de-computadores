Redes-de-computadores
=====================

Material da disciplina de redes de computadores


## Trabalho 1

Este trabalho foi feito utilizando a linguagem python. A aplicação do trabalho se chama p2p.py. Para executá-la basta acessar algum terminal/console e digitar o seguinte comando:

```bash
python p2p.py
```

### Dependências

A aplicação deste trabalho é multiplataforma e roda tanto em linux, Windows e Mac OS X. Porém. possui dependência da biblioteca netifaces do python.  Para instalá-la basta executar o seguinte comando no Ubuntu Linux:

```bash
sudo  apt-get install python-netifaces
```

Para instalar no Windows basta executar o instalador que se encontra na pasta libs externas.

### Manual de Utilização

Ao executar a aplicação, ela irá detectar as interfaces disponíveis  no host e, caso exista mais de uma,  perguntará qual se deseja utilizar. Devido algumas dúvidas sobre como implementar determinadas partes do protocolo a aplicação implementa, nesses casos, as duas opções. Dessa forma, para definir quais opções desejamos utilizar a aplicação realizaa mais duas outras perguntas. Após receber as repostas a aplicação apresenta um prompt de comando onde se pode digitar os seguintes comandos: info, start, lookup, leave,  netinfo e quit.

#### info

Este comando informa a situação do nó que pertencente a aplicação. Basicamente imprime o ID e o IP do no da aplicação. Mas quando o nó esta conectado a um rede as informações do antecessor e do sucessor também são exibidas. Para executar este comando basta digitar "info" no prompt de comando.


#### start

Ao iniciar a aplicação o nó não pertence ainda à uma rede p2p. Dessa forma, a aplicação tem duas opções: criar uma rede própria ou se juntar a uma rede existente. O comando start cria uma rede própria onde o sucessor e o antecessor é o nó da aplicação. Para executar este comando basta digitar "start" no prompt de comando.

#### lookup

O comando lookup serve tanto para buscar informações de um nó da rede quanto para adicionar um nó na rede. Quando o nó não esta na rede ele deve realizar um lookup perguntando pelo seu id para algum nó da rede. Ao receber a resposta ele envia uma mensagem de join para se juntar a rede. Caso já esteja na rede a aplicação apenas exibe a resposta do lookup. Para executar esse comando basta digitar "lookup" no prompt de comando e informar os dados requisitados.

#### leave
O comando leave retira o nó da rede. Quando o nó sai duas mensagens de leave são enviadas: uma para seu antecessor e outra para o seu sucessor.  Para executar este comando basta digitar "leave" no promt de comando.

#### netinfo
O comando netinfo faz uma serie de requisições lookups para os membros da rede com o intuito de descobrir a estrura formada pela rede. Ao terminar de realizar os lookups ele imprime a estrutura da rede comecando pelo primeiro nó da rede.

#### quit
Ao digitar este comando no prompt de comando a aplicação é encerrada.

### Testes

Os testes realizados podem ser vistos nos videos abaixo:
<video src="http://www.screenr.com/embed/1ZAN"></video>
