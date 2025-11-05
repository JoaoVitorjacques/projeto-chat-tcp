# Documento do Protocolo - Mini-Chat TCP

Este documento define os comandos e respostas do sistema de chat.
Toda comunicação usa UTF-8.

---

## 1. Comunicação Cliente -> Servidor (Comandos)

O cliente envia dados brutos ao servidor. O servidor interpreta baseado no contexto.

### 1.1. Registro de Apelido
* **Descrição:** A *primeira* mensagem que o cliente envia após a conexão.
* **Formato:** `<apelido_desejado>`
* **Exemplo:** `ana`

### 1.2. Mensagem Broadcast
* **Descrição:** Mensagem padrão, enviada para todos.
* **Formato:** `<texto_da_mensagem>` (que não comece com `@` e não seja `WHO` ou `QUIT`).
* **Exemplo:** `Olá a todos!`

### 1.3. Mensagem Direta (DM)
* **Descrição:** Mensagem enviada a um usuário específico.
* **Formato:** `@<apelido_destino> <texto_da_mensagem>`
* **Exemplo:** `@joao você pode me ajudar?`

### 1.4. Comando `WHO`
* **Descrição:** Solicita a lista de usuários conectados.
* **Formato:** `WHO` (ou `who`)

### 1.5. Comando `QUIT`
* **Descrição:** Encerra a conexão de forma limpa.
* **Formato:** `QUIT` (ou `quit`)

---

## 2. Comunicação Servidor -> Cliente (Respostas)

O servidor envia mensagens formatadas para o cliente.

### 2.1. Confirmações de Sistema
* `New User. Você está conectado!` (Enviado ao cliente ao conectar).
* `SYSTEM: {nickname} entrou no chat.` (Broadcast quando alguém entra).
* `SYSTEM: {nickname} saiu do chat.` (Broadcast quando alguém sai).
* `SYSTEM: Usuários conectados: ana, bruno` (Resposta ao `WHO`).
* `SYSTEM: DM para {nickname} enviada.` (Confirmação de DM para o remetente).

### 2.2. Mensagens de Chat Recebidas
* **Broadcast:** `FROM {remetente} [all]: {mensagem}`
* **DM:** `FROM {remetente} [dm]: {mensagem}`

### 2.3. Erros
* `ERR apelido_em_uso` (Enviado se o apelido escolhido já existe).
* `ERR user_not_found` (Enviado ao tentar mandar DM para um usuário offline/inexistente).