from classes.banco import Banco
from classes.contaCorrente import ContaCorrente
from random import randrange
import threading

NUMERO_DE_THREADS = 40
NUMERO_DE_CONTAS = 10
VALOR_MAXIMO_PARA_TRANSACOES = 100
OPERACOES = ['sacar', 'depositar', 'consultar', 'transferir']


def main():
    banco = Banco()
    threads = []

    for _ in range(NUMERO_DE_CONTAS):
        banco.adiciona_conta(ContaCorrente(saldo = VALOR_MAXIMO_PARA_TRANSACOES))

    for _ in range(NUMERO_DE_THREADS):
        conta = banco[randrange(0, len(banco))] # seleciona uma conta aleató-
        # ria do banco.
        operacao = OPERACOES[randrange(0, len(OPERACOES))] # seleciona uma o-
        # peração aleatória.
        match operacao:
            case 'sacar':
                threads.append(
                    threading.Thread(
                        target=conta.sacar,
                        args=(randrange(0, VALOR_MAXIMO_PARA_TRANSACOES),)
                    )
                )
            case 'depositar':
                threads.append(
                    threading.Thread(
                        target=conta.depositar, args=(
                            randrange(0, VALOR_MAXIMO_PARA_TRANSACOES),)
                    )
                )
            case 'consultar':
                threads.append(
                    threading.Thread(
                        target=conta.consultar, args=()
                    )
                )
            case 'transferir':
                threads.append(
                    threading.Thread(
                        target=conta.transferir,
                        args=(
                            randrange(0, VALOR_MAXIMO_PARA_TRANSACOES),
                            banco[randrange(0, len(banco))]
                        )
                    )
                )
            case _:
                raise ValueError(f"operacao \"{operacao}\" não reconhecida.")

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for conta in banco:
        print(conta)


if __name__ == '__main__':
    main()
