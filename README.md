<h1 align="center">Piqueteiro Bot para Telegram<img src="./image/telegram-3d-icon-free-png.webp" alt="telegram" width="40px" height="40px" /> </h1>

Piqueteiro Bot é um bot `Telegram` feito para enviar notificações sempre que o site da `VFS Global` estiver aberto para fazer agendamento para `Portugal`.

<img src="./image/piqueteiro.png" alt="telegram" width="450px" height="450px" />

<br />
Highlights:

- 🔔 Notificações em tempo real sempre que o site da VFS estiver aberto
- ⚡ Tecnologia usada: Python 🐍

---
<br />

### Instalação do Bot
###### ⚠️ OBS: Tens que ter o `Python` instalado em sua máquina para o Bot funcionar.

#### Baixando o Bot Telegram <img src="./image/telegram-3d-icon-free-png.webp" alt="telegram" width="25px" height="25px" />

Abra o `Terminal` ou `CMD` e digite:
```bash
git clone https://github.com/MauricioMbala02/piqueteiro-vfs-global.git
cd piqueteiro-vfs-global/
```

#### Instalando as dependências Python <img src="./image/3d-python-programming-language-logo-free-png.webp" alt="telegram" width="25px" height="25px" />

Instale todas as dependências em `requirements.txt`
Abra o `Terminal` ou `CMD` e digite:
```bash
pip install -r requirements.txt
```

#### Adicionando ao Telegram <img src="./image/telegram-3d-icon-free-png.webp" alt="telegram" width="25px" height="25px" />

Substitua o `telegram_token` pelo o seu token do Telegram e faça o mesmo com o `chat_id` do arquivo `config.json`

###### config.json
```json
{
    "telegram_token": "xxxxxxxxxxxxxxxxxxxxxxxxxx",
    "chat_id": xxxxxxxxxxxxx  // Número inteiro, sem aspas!
}
```

#### Iniciando o Bot <img src="./image/telegram-3d-icon-free-png.webp" alt="telegram" width="25px" height="25px" /><img src="./image/3d-python-programming-language-logo-free-png.webp" alt="telegram" width="25px" height="25px" />

Abra o `Terminal` ou `CMD` e digite:
```bash
python main.py
```
ou
```bash
python3 main.py
```