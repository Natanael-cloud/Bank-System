from abc import ABC, abstractmethod
from datetime import datetime

# Interface Transacao
class Transacao(ABC):
    def __init__(self):
        self.data_hora = datetime.now()  # Data e hora da transação
    
    @abstractmethod
    def registrar(self, conta):
        pass

# Classe Historico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

# Classe Conta
class Conta:
    def __init__(self, numero, agencia, cliente):
        self.numero = numero
        self.agencia = agencia
        self.saldo = 0.0
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    def nova_conta(self, cliente, numero):
        return Conta(numero, "001", cliente)

    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            return True
        else:
            print("Saldo insuficiente!")
            return False

    def depositar(self, valor):
        self.saldo += valor
        return True

# Classe Deposito
class Deposito(Transacao):
    def __init__(self, valor):
        super().__init__()
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)
        conta.historico.adicionar_transacao(self)
        print(f"Depósito de R${self.valor} realizado na conta {conta.numero}. Data: {self.data_hora}")

# Classe Saque
class Saque(Transacao):
    def __init__(self, valor):
        super().__init__()
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            print(f"Saque de R${self.valor} realizado na conta {conta.numero}. Data: {self.data_hora}")
        else:
            print(f"Saque de R${self.valor} falhou na conta {conta.numero}. Data: {self.data_hora}")

# Classe Cliente
class Cliente:
    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Classe PessoaFisica
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(nome, endereco)
        self.cpf = cpf
        self.data_nascimento = data_nascimento

# Função para interagir com o usuário via terminal
def menu():
    print("\nBem-vindo ao Sistema Bancário!")
    print("Escolha uma opção:")
    print("1. Criar Conta")
    print("2. Depositar")
    print("3. Sacar")
    print("4. Consultar Saldo")
    print("5. Sair")

def main():
    clientes = {}
    while True:
        menu()
        opcao = input("Escolha uma opção (1/2/3/4/5): ")

        if opcao == "1":
            nome = input("Nome do Cliente: ")
            endereco = input("Endereço do Cliente: ")
            cpf = input("CPF do Cliente: ")
            data_nascimento = input("Data de Nascimento do Cliente (dd/mm/aaaa): ")
            cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
            numero_conta = int(input("Número da conta: "))
            conta = Conta(numero_conta, "001", cliente)
            cliente.adicionar_conta(conta)
            clientes[cpf] = cliente
            print(f"Conta criada com sucesso para {nome}!")
        
        elif opcao == "2":
            cpf = input("Informe o CPF do cliente para depósito: ")
            if cpf in clientes:
                cliente = clientes[cpf]
                numero_conta = int(input("Informe o número da conta para depósito: "))
                conta = next((c for c in cliente.contas if c.numero == numero_conta), None)
                if conta:
                    valor = float(input("Informe o valor para depósito: "))
                    deposito = Deposito(valor)
                    cliente.realizar_transacao(conta, deposito)
                else:
                    print("Conta não encontrada!")
            else:
                print("Cliente não encontrado!")

        elif opcao == "3":
            cpf = input("Informe o CPF do cliente para saque: ")
            if cpf in clientes:
                cliente = clientes[cpf]
                numero_conta = int(input("Informe o número da conta para saque: "))
                conta = next((c for c in cliente.contas if c.numero == numero_conta), None)
                if conta:
                    valor = float(input("Informe o valor para saque: "))
                    saque = Saque(valor)
                    cliente.realizar_transacao(conta, saque)
                else:
                    print("Conta não encontrada!")
            else:
                print("Cliente não encontrado!")

        elif opcao == "4":
            cpf = input("Informe o CPF do cliente para consultar saldo: ")
            if cpf in clientes:
                cliente = clientes[cpf]
                numero_conta = int(input("Informe o número da conta para consultar saldo: "))
                conta = next((c for c in cliente.contas if c.numero == numero_conta), None)
                if conta:
                    print(f"Saldo da conta {conta.numero}: R${conta.saldo}")
                else:
                    print("Conta não encontrada!")
            else:
                print("Cliente não encontrado!")

        elif opcao == "5":
            print("Saindo... Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
