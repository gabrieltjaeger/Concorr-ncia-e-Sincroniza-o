import threading


class ContaCorrente:
    contas = 1

    def __init__(self, saldo = 0):
        self.numero_da_conta = ContaCorrente.contas
        ContaCorrente.contas += 1
        self.__saldo = saldo
        self.lock = threading.Lock()
        self.lock_operacoes = threading.Lock()
        self.numero_de_semaforos = 5
        self.semaforo = threading.Semaphore(5)
        self.lendo = 0
        self.escrevendo = False

    def __repr__(self):
        return f"Conta {self.numero_da_conta} com saldo {self.saldo}"

    @property
    def saldo(self):
        return self.__saldo

    def consultar(self):
        while True:
            self.lock_operacoes.acquire()
            if self.escrevendo and self.lendo >= self.numero_de_semaforos:
                self.lock_operacoes.release()
                continue
            break
        self.lendo += 1
        self.lock_operacoes.release()
        self.semaforo.acquire()
        print(
            f"{threading.current_thread().name} está consultando conta {self.numero_da_conta} com saldo {self.saldo}\n"
        )
        saldo = self.saldo
        self.semaforo.release()
        self.lock_operacoes.acquire()
        self.lendo -= 1
        self.lock_operacoes.release()
        return saldo

    def depositar(self, valor):
        while True:
            self.lock_operacoes.acquire()
            if self.escrevendo and self.lendo >= self.numero_de_semaforos:
                self.lock_operacoes.release()
                continue
            break
        self.escrevendo = True
        self.lock_operacoes.release()
        self.lock.acquire()
        print(
            f"{threading.current_thread().name} está depositando {valor} na conta {self.numero_da_conta}"
        )
        self.__saldo += valor
        self.lock.release()
        print(
            f"{threading.current_thread().name} terminou de depositar na conta {self.numero_da_conta}\n"
        )
        self.lock_operacoes.acquire()
        self.escrevendo = False
        self.lock_operacoes.release()

    def possui_saldo(self, valor):
        return self.consultar() >= valor

    def sacar(self, valor):
        while True:
            self.lock_operacoes.acquire()
            if self.escrevendo and self.lendo >= self.numero_de_semaforos:
                self.lock_operacoes.release()
                continue
            break
        self.escrevendo = True
        self.lock_operacoes.release()
        self.lock.acquire()
        print(
            f"{threading.current_thread().name} está sacando {valor} da conta {self.numero_da_conta}"
        )
        if self.possui_saldo(valor):
            self.__saldo -= valor
            self.lock.release()
            print(
                f"{threading.current_thread().name} terminou de sacar na conta {self.numero_da_conta}\n"
            )
            self.lock_operacoes.acquire()
            self.escrevendo = False
            self.lock_operacoes.release()
            return True
        else:
            self.lock.release()
            print(
                f"{threading.current_thread().name} não tem saldo suficiente na conta {self.numero_da_conta}\n"
            )
            self.lock_operacoes.acquire()
            self.escrevendo = False
            self.lock_operacoes.release()
            return False
        
    def transferir(self, valor, conta):
        if self.sacar(valor):
            conta.depositar(valor)
            return True
        return False
