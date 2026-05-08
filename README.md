# AI Hotkeys

Este projeto permite configurar teclas de atalho globais que "recortam" o texto selecionado, enviam para uma IA compatível com a API da OpenAI com um prefixo configurável, e colam a resposta da IA de volta no local original.

## Requisitos
Você precisará do Python 3.8+ instalado no seu computador.
O programa requer permissões do sistema operativo para intercetar as teclas de atalho (no Windows ele já consegue fazer isso, no macOS/Linux pode precisar rodar com permissões de root/administrador dependendo de suas configurações de segurança e da biblioteca `keyboard`).

## Instalação

```bash
pip install -r requirements.txt
```

## Como usar

Execute o script principal:
```bash
python run.py
```

O programa iniciará um servidor em segundo plano.
Abra seu navegador no endereço: `http://localhost:8000`

Na interface de configuração:
1. **Adicione Modelos:** Cadastre os modelos que deseja usar (ex: OpenAI GPT-4, Llama 3 local via LMStudio/Ollama, etc). Chaves de API serão salvas de forma segura no cofre do seu SO utilizando a biblioteca `keyring`.
2. **Adicione Atalhos:** Configure os atalhos. Ao invés de digitar `ctrl+c`, basta clicar no campo de atalho e apertar as teclas. Defina o Prefixo (ex: "Traduza o texto abaixo para Português:") e vincule a um modelo cadastrado.

**Uso Prático:** Selecione qualquer texto em qualquer janela, e aperte a tecla de atalho. O texto será recortado, o aviso "Processando..." aparecerá, e, assim que a IA responder, o "Processando..." será substituído pela resposta gerada!
