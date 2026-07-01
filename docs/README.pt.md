# KindleBoard - Self-hosted Kindle and E-ink Dashboard

**Versão atual:** `V1.1`

KindleBoard é um painel auto-hospedado para Kindle e telas e-ink, feito para Docker. Ele transforma um Kindle Paperwhite antigo em um quadro sempre visível para escala semanal, notas e lista de tarefas.

Ele é útil para quem procura Kindle Paperwhite dashboard, e-ink dashboard, self-hosted dashboard, Docker Kindle dashboard, Kindle todo list, Kindle memo board ou weekly schedule display no próprio servidor.

![Prévia do KindleBoard como painel auto-hospedado para Kindle e e-ink com escala semanal](preview.png)

KindleBoard foi pensado para redes privadas confiáveis. Se você expuser o serviço à internet, use VPN, autenticação em proxy reverso ou outra camada de controle de acesso.

## Casos de uso

- Transformar um Kindle Paperwhite antigo em um painel e-ink sempre visível.
- Mostrar uma escala semanal pessoal com total automático de horas.
- Exibir notas, mensagens ou lembretes grandes e legíveis.
- Usar o Kindle como lista de tarefas com toque para concluir.
- Executar em casa, em um host Docker ou em um ambiente homelab.

## Palavras-chave de busca

Kindle dashboard, Kindle Paperwhite dashboard, e-ink dashboard, e-paper dashboard, self-hosted dashboard, Docker Kindle dashboard, Kindle todo list, Kindle memo board, Kindle schedule display, home dashboard, homelab dashboard, SQLite dashboard.
## Recursos

- Escala semanal pessoal com turnos, dias de descanso, notas e total automático de horas.
- Suporte a turnos que passam da meia-noite, como `22:00` a `06:00`.
- Modo de notas com texto grande.
- Lista de tarefas com conclusão diretamente no Kindle.
- Painel administrativo para editar conteúdo, trocar modo e escolher idioma.
- Download de backup do banco de dados e restauração a partir de um arquivo local.
- Página otimizada para Kindle, com alto contraste e botão grande de atualizar.
- Um único banco SQLite para escala, notas, tarefas, modo de exibição e idioma.
- Interface multilíngue.
- Porta padrão: `10000`.

## Modos de exibição

- **Schedule**: escala semanal e total de horas.
- **Memo**: uma nota grande.
- **To-do**: lista de tarefas clicável.

A página do Kindle mostra apenas o modo selecionado.

## Instalação com Docker

Imagem recomendada:

```text
neil2046/kindleboard:latest
```

Imagem espelho:

```text
ghcr.io/neil2046/kindleboard:latest
```

```bash
mkdir kindleboard
cd kindleboard
```

Crie `docker-compose.yml`:

```yaml
services:
  kindleboard:
    image: neil2046/kindleboard:latest
    container_name: kindleboard
    ports:
      - "10000:10000"
    volumes:
      - ./data:/data
    restart: unless-stopped
```

Inicie:

```bash
docker compose up -d
```

Acesse:

```text
Admin:  http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

## Persistência de dados

Os dados ficam em `./data/schedule.db`. Escala, notas, tarefas, modo de exibição e idioma ficam nesse único banco SQLite.

O painel administrativo inclui ferramentas para baixar um backup SQLite e restaurar dados a partir de um arquivo local de backup do KindleBoard.

Na primeira inicialização, se `/data/schedule.db` não existir, o KindleBoard copia um banco de demonstração em inglês. Dados existentes nunca são sobrescritos.

## Atualização

```bash
docker compose pull
docker compose up -d
```

## Notas para Kindle

- Abra `http://SERVER-IP:10000/kindle` no navegador do Kindle.
- Ative o modo sempre ligado, sem suspensão ou kiosk se o seu Kindle ou firmware oferecer suporte.
- O Kindle precisa acessar o host Docker.
- A página inclui um botão grande de atualização.
- Barra do navegador e proteção de tela são controladas pelo Kindle OS.

## Segurança

KindleBoard não inclui contas ou login. Use em ambientes confiáveis. Para acesso externo, use VPN ou proxy reverso com autenticação.

