import random
from aigyminsper.search.graph import State
from aigyminsper.search.search_algorithms import BuscaCustoUniforme


class AgentSpecification(State):
    def __init__(self, op, pos_agente, pos_obstaculos, pos_pacote,
                 pegou_pacote, pos_pedagio, destino, dimensao, custo_acao=0):
        super().__init__(op)
        self.pos_agente = tuple(pos_agente)
        self.pos_obstaculos = frozenset(pos_obstaculos)
        self.pos_pacote = tuple(pos_pacote)
        self.pegou_pacote = pegou_pacote
        self.pos_pedagio = frozenset(pos_pedagio)
        self.destino = tuple(destino)
        self.dimensao = dimensao
        self.custo_acao = custo_acao

    def successors(self):
        sucessores = []
        if self.is_goal():
            return sucessores
        linha, coluna = self.pos_agente

        custo = 3 if self.pos_agente in self.pos_pedagio else 1

        def novo_estado(acao, agente, pacote, pegou):
            return AgentSpecification(
                acao, agente, self.pos_obstaculos, pacote, pegou,
                self.pos_pedagio, self.destino, self.dimensao, custo)

        movimentos = [('ir para cima', (linha - 1, coluna)),
                      ('ir para baixo', (linha + 1, coluna)),
                      ('ir para esquerda', (linha, coluna - 1)),
                      ('ir para direita', (linha, coluna + 1))]
        for acao, nova_pos in movimentos:
            l, c = nova_pos
            if (0 <= l < self.dimensao and 0 <= c < self.dimensao
                    and nova_pos not in self.pos_obstaculos):
                pacote = nova_pos if self.pegou_pacote else self.pos_pacote
                sucessores.append(novo_estado(
                    acao, nova_pos, pacote, self.pegou_pacote))

        if not self.pegou_pacote and self.pos_agente == self.pos_pacote:
            sucessores.append(novo_estado(
                'pegar pacote', self.pos_agente, self.pos_pacote, True))
        if self.pegou_pacote:
            sucessores.append(novo_estado(
                'entregar pacote', self.pos_agente, self.pos_agente, False))

        return sucessores

    def is_goal(self):
        return not self.pegou_pacote and self.pos_pacote == self.destino

    def cost(self):
        return self.custo_acao

    def env(self):
        return str((self.pos_agente, self.pos_pacote,
                    self.pegou_pacote, self.custo_acao))

    def description(self):
        return 'Entregador em grid com obstáculos e pedágios'


def gerar_mundo(dimensao, semente=None):
    if type(dimensao) is not int or dimensao < 1:
        raise ValueError('A dimensão deve ser um inteiro positivo.')
    rng = random.Random(semente)
    celulas = [(l, c) for l in range(dimensao) for c in range(dimensao)]
    if dimensao == 1:
        agente = pacote = destino = (0, 0)
    else:
        agente, pacote, destino = rng.sample(celulas, 3)
    candidatas = [p for p in celulas if p not in {agente, pacote, destino}]
    obstaculos = frozenset(rng.sample(
        candidatas, rng.randint(0, len(candidatas))))
    livres = [p for p in celulas if p not in obstaculos]
    pedagios = frozenset(rng.sample(livres, rng.randint(0, len(livres))))
    return AgentSpecification('', agente, obstaculos, pacote, False,
                              pedagios, destino, dimensao)


def escolher_dimensao():
    while True:
        try:
            dimensao = int(input('Digite a dimensão do grid (ex.: 5 para 5 x 5): '))
            if dimensao > 0:
                return dimensao
            print('A dimensão deve ser maior que zero.')
        except ValueError:
            print('Digite um número inteiro positivo.')
        except (EOFError, KeyboardInterrupt):
            print('\nExecução cancelada.')
            return None


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Entregador com AI Gym Insper')
    parser.add_argument('--dimensao', type=int,
                        help='Dimensão do mundo; sem este argumento, pergunta no terminal.')
    parser.add_argument('--semente', type=int, default=None,
                        help='Semente opcional para reproduzir o sorteio.')
    args = parser.parse_args()

    dimensao = args.dimensao
    if dimensao is None:
        dimensao = escolher_dimensao()
        if dimensao is None: 
            return
    try:
        estado = gerar_mundo(dimensao, args.semente)
    except ValueError as erro:
        parser.error(str(erro))

    print(f'Grid: {estado.dimensao} x {estado.dimensao}')
    print(f'Agente: {estado.pos_agente}')
    print(f'Pacote: {estado.pos_pacote}')
    print(f'Destino: {estado.destino}')
    print(f'Obstáculos: {sorted(estado.pos_obstaculos)}')
    print(f'Pedágios: {sorted(estado.pos_pedagio)}')
    print('\nBusca de custo uniforme')
    state = estado
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state, pruning="general", trace=False)
    if result is not None:
        print('Achou!')
        print(result.show_path())
        print(f'Custo da solução: {result.g}')
    else:
        print('Não achou solução')


if __name__ == '__main__':
    main()
