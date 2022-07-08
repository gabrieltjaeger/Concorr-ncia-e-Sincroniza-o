class Banco:
    def __init__(self):
        self.contas = []

    def adiciona_conta(self, conta):
        self.contas.append(conta)

    def __repr__(self):
        return str(self.contas)

    def __iter__(self):
        return iter(self.contas)

    def __next__(self):
        return next(self.contas)

    def __len__(self):
        return len(self.contas)

    def __getitem__(self, index):
        return self.contas[index]
