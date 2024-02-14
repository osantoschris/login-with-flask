# Login with Flask (a python app)
Este é o ínicio de uma jornada de criação de aplicações web utilizando python. Neste caso, Flask. 

## Login
A primeira etapa da aplicação consiste em um sistema de login buscando o usuário em um banco de dados SQLite3. É possível realizar o cadastro do usuário através do link fornecido pela aplicação. 
<br>
No momento do registro do usuário, será solicitado os seguintes campos:
 - Nome
 - Sobrenome
 - Email
 - Nome de usuário
 - Senha
<br>
A senha do usuário será criptografada utilizando o método 'pbkdf2:sha256'.

## Cadastro de clientes
A segunda etapa da aplicação é responsável pelo cadastro de clientes, onde são solicitados os seguintes campos;
 - Nome do cliente
 - Empresa do cliente
 - Email do cliente

# Anotações do desenvolvedor
Este é um projeto que está em execução para fins de portifólio. Serão aplicadas melhorias no decorrer do desenvolvimento. Abaixo estão as etapas de desenvolvimento até o momento. Cada nova modificação será atualizada no arquivo de README. 

# Etapas de execução
**25/01/2024**
Este é o ínicio de um projeto Front-End onde será criado um sistema de cadastro de usuários com a utilização do banco de dados SQLite3.
A aplicação está sendo desenvolvida com as seguintes linguagens:
1. Python
    * Utilização da biblioteca Flask
2. HTML
3. CSS

Esta documentação está em processo de criação juntamente com a aplicação. Em breve serão publicadas as etapas do processo de criação e as primeiras tasks realizadas.

**29/01/2024**
 - Página de registro atualizada para incluir novos campos para os usuários.
 - Criado nova tabela para cadastro de clientes. Deve ser feita a normalização para verificar se está de acordo com as regras de negócio.
 - Ajustar botão de sair da pagina de dashboard, ainda está com o layout default. Combinar com o gradiente do fundo.
 - Trocar fonte da tela de dashboard

**30/01/2024**
 - Tentativa 1 de fazer deploy
 - Botão de sair ajustado
 - Fonte da tela de dashboard ajustada

**09/02/2024**
Após alguns dias de viagem, retomei as programações da aplicação. 
 - Botões de telas de cadastro e consulta de clientes.

**14/02/2024**
Implementações:
 - Pesquisas no banco de dados para preenchimento de combobox
 - Criação da view dentro do banco de dados
Próximos passos:
 - Criar o formulário de cadastro com um botão de cadastrar e voltar (duas ações no mesmo formulário)
 - Ver rotas dentro da aplicação, não está conseguindo redirecionar para a função correta quando clica em voltar. 