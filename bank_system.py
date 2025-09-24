from abc import ABC, abstractmethod
from datetime import datetime

# Interface Transacao
class Transacao(ABC):
    def __init__(self):
        self.__data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')  # Formato legível da data e hora
    
    @abstractmethod
    def registrar(self, conta):
        pass
    
    @property
    def data_hora(self):
        return self.__data_hora

# Classe Historico
class Historico:
    def __init__(self):
        self.__transacoes = []

    def adicionar_transacao(self, transacao):
        self.__transacoes.append(transacao)

    @property
    def transacoes(self):
        return self.__transacoes

# Classe Conta
class Conta:
    def __init__(self, numero, agencia, cliente):
        self.__numero = numero
        self.__agencia = agencia
        self.__saldo = 0.0
        self.__cliente = cliente
        self.__historico = Historico()

    @property
    def saldo(self):
        return self.__saldo  # Retorno do saldo 

    def nova_conta(self, cliente, numero):
        return Conta(numero, "001", cliente)

    def sacar(self, valor):
        if valor <= self.__saldo:
            self.__saldo -= valor
            return True
        else:
            print("Saldo insuficiente!")
            return False

    def depositar(self, valor):
        self.__saldo += valor
        return True

# Classe Deposito
class Deposito(Transacao):
    def __init__(self, valor):
        super().__init__()
        self.__valor = valor

    def registrar(self, conta):
        conta.depositar(self.__valor)
        conta._Conta__historico.adicionar_transacao(self)
        print(f"Depósito de R${self.__valor} realizado na conta {conta._Conta__numero}. Data: {self.data_hora}")

# Classe Saque
class Saque(Transacao):
    def __init__(self, valor):
        super().__init__()
        self.__valor = valor

    def registrar(self, conta):
        if conta.sacar(self.__valor):
            conta._Conta__historico.adicionar_transacao(self)
            print(f"Saque de R${self.__valor} realizado na conta {conta._Conta__numero}. Data: {self.data_hora}")
        else:
            print(f"Saque de R${self.__valor} falhou na conta {conta._Conta__numero}. Data: {self.data_hora}")

# Classe Cliente
class Cliente:
    def __init__(self, nome, endereco):
        self.__nome = nome
        self.__endereco = endereco
        self.__contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.__contas.append(conta)

    @property
    def nome(self):
        return self.__nome
    
    @property
    def endereco(self):
        return self.__endereco
    
    @property
    def contas(self):
        return self.__contas

# Classe PessoaFisica
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(nome, endereco)
        self.__cpf = cpf
        self.__data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self.__cpf
    
    @property
    def data_nascimento(self):
        return self.__data_nascimento

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
                conta = next((c for c in cliente.contas if c._Conta__numero == numero_conta), None)
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
                conta = next((c for c in cliente.contas if c._Conta__numero == numero_conta), None)
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
                conta = next((c for c in cliente.contas if c._Conta__numero == numero_conta), None)
                if conta:
                    print(f"Saldo da conta {conta._Conta__numero}: R${conta.saldo}")
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
