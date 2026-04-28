# Pomodoro Timer

Um cronômetro Pomodoro simples e elegante para o terminal, escrito em Python utilizando a biblioteca `curses`.

## Funcionalidades
- Ciclos de trabalho e descanso (curto e longo).
- Interface visual no terminal com fonte grande.
- Notificações de desktop (via `notify-send`).
- Atalhos de teclado para pausar, resetar e sair.

## Requisitos
- Python 3
- Biblioteca `curses` (geralmente inclusa no Python no Linux)
- `libnotify` (opcional, para notificações no Linux)

## Como Baixar e Executar

### 1. Clonar o Repositório
Abra o terminal e execute:
```bash
git clone https://github.com/samucapxx/pomodoro-timer.git
cd pomodoro-timer
```

### 2. Executar o Programa
Você pode executar diretamente com:
```bash
python3 pomodoro.py
```
Ou, se preferir, dê permissão de execução:
```bash
chmod +x pomodoro.py
./pomodoro.py
```

## Atalhos de Teclado
- `Espaço`: Iniciar/Pausar
- `R`: Resetar o ciclo atual
- `Q`: Sair do programa
