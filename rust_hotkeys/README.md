# Rust Hotkeys

Este projeto é uma versão em Rust de um script Python que escuta atalhos de teclado globais.

Ele utiliza a biblioteca `rdev` para capturar os eventos do teclado.

## Requisitos

- Rust instalado. Se você não o possui, pode instalá-lo através do [rustup](https://rustup.rs/):
  ```bash
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  ```

No Linux, a biblioteca `rdev` necessita das bibliotecas de desenvolvimento do X11 (se você usar X11). Em sistemas baseados em Debian/Ubuntu, você pode instalá-las com:
```bash
sudo apt-get update
sudo apt-get install -y libx11-dev libxtst-dev
```

## Configuração e Execução

1. Clone ou baixe o código fonte deste projeto.
2. Navegue até a pasta `rust_hotkeys` pelo terminal:
   ```bash
   cd rust_hotkeys
   ```
3. Compile e execute o projeto usando o `cargo`:
   ```bash
   cargo run
   ```

Quando executado, o programa mostrará a seguinte mensagem no console:
`Listener ativo. Pressione F2 (melhore) ou F8 (general) ou F9 (python) ou F10(html) para enviar consulta o Gemini.`

Pressionar as teclas F2, F8, F9 e F10 invocará a respectiva ação (imprimindo no console). Para interromper a execução, pressione `Ctrl+C` no terminal.
