import threading

class ContaCorrente:
    contas = 1

    def __init__(self):
        self.numero_da_conta = ContaCorrente.contas
        ContaCorrente.contas += 1
        self.__saldo = 0
        self.lock = threading.Lock()
        self.semaforo = threading.Semaphore(5)

    def __repr__(self):
        return f"Conta {self.numero_da_conta} com saldo {self.saldo}"

    @property
    def saldo(self):
        self.semaforo.acquire()
        print(
            f"{threading.current_thread().name} está lendo o saldo da conta {self.numero_da_conta}")
        saldo_atual = self.__saldo
        self.semaforo.release()
        print(
            f"{threading.current_thread().name} terminou de ler o saldo da conta {self.numero_da_conta}\n"
        )
        return saldo_atual

    def consultar(self):
        return self.saldo

    def depositar(self, valor):
        self.lock.acquire()
        print(
            f"{threading.current_thread().name} está depositando na conta {self.numero_da_conta}"
        )
        self.__saldo += valor
        self.lock.release()
        print(
            f"{threading.current_thread().name} terminou de depositar na conta {self.numero_da_conta}\n"
        )
        return True

    def possui_saldo(self, valor):
        return self.saldo >= valor

    def sacar(self, valor):
        if self.possui_saldo(valor):
            self.lock.acquire()
            print(
                f"{threading.current_thread().name} está sacando da conta {self.numero_da_conta}"
            )
            self.__saldo -= valor
            self.lock.release()
            print(
                f"{threading.current_thread().name} terminou de sacar da conta {self.numero_da_conta}\n"
            )
            return True
        return False

    def transferir(self, valor, conta):
        if self.sacar(valor):
            conta.depositar(valor)
            return True
        return False
