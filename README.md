# Projeto Mini-Chat TCP com Python

Este é um projeto de um sistema de chat multiusuário cliente-servidor,
desenvolvido em Python 3.x utilizando a biblioteca padrão `socket`. O objetivo é explorar conceitos de conexão TCP e comunicação entre múltiplos clientes.

## Funcionalidades
* Servidor concorrente (usando threads) para múltiplos clientes.
* Registro de apelidos únicos (impede duplicados).
* Mensagens em **Broadcast** (para todos).
* Mensagens **Diretas (DM)** (para usuários específicos).
* Comando `WHO` para listar usuários online.
* Comando `QUIT` para sair.

---

## 🚀 Guia de Execução

Estas são as instruções para rodar o servidor e conectar dois ou mais clientes.

**1. Terminal 1: Iniciar o Servidor**
No primeiro terminal, inicie o servidor. Ele ficará escutando por conexões:
```bash
python server.py
Saída esperada: [STATUS] Servidor escutando em 127.0.0.1:50001...

2. Terminal 2: Conectar Cliente A No segundo terminal, inicie o primeiro cliente:

Bash

python client.py
O programa pedirá: Escolha seu apelido: Digite um apelido (ex: ana) e pressione Enter.

3. Terminal 3: Conectar Cliente B Repita o processo no terceiro terminal para conectar mais um cliente.

Bash

python client.py
O programa pedirá: Escolha seu apelido: Digite outro apelido (ex: bruno) e pressione Enter.

Pronto! Agora envie mensagens, DMs (@apelido) ou use os comandos.

🧪 Casos de Teste
Aqui estão os casos de teste exigidos:

Broadcast com múltiplos clientes:

Cliente ana digita: Olá

Resultado: Cliente bruno recebe: FROM ana [all]: Olá

Mensagem direta para usuário existente:

Cliente ana digita: @bruno oi

Resultado: Apenas bruno recebe: FROM ana [dm]: oi

Mensagem direta para usuário inexistente (erro):

Cliente ana digita: @carlos tudo bem?

Resultado: Apenas ana recebe: ERR user_not_found

Tentativa de apelido duplicado:

Cliente ana está conectado.

Cliente carlos tenta se conectar com o apelido ana.

Resultado: Cliente carlos recebe: ERR apelido_em_uso e é desconectado.