# APS 4 — Exercício de Revisão da Prova

Programa em Python que usa 'BuscaCustoUniforme' para buscar e entregar um pacote em um grid com obstáculos e pedágios.

## Execução

Crie e ative um ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalação da biblioteca aigyminsper:
```bash:
python -m pip install aigyminsper==0.3.9
```

Execute o arquivo:
```bash
python aps_entregador.py
```

Digite a dimensão no terminal. O mapa é gerado aleatoriamente, e o programa mostra as ações e o custo total ou diz que não há solução.

## Exemplos de execução

| Grid | Resultado | Ações | Custo |
|---|---|---:|---:|
| 5 × 5 | Entrega concluída; todas as ações começaram em pedágios | 7 | 21 |
| 3 × 3 | Entrega concluída; apenas a primeira ação começou em pedágio | 7 | 9 |
| 7 × 7 | Pacote e destino isolados por obstáculos | — | Sem solução |
