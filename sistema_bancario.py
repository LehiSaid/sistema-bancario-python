import textwrap

def menu():
    return input(textwrap.dedent("""
    ================ MENU ================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo usuário
    [nc] Nova conta
    [lc] Listar contas
    [q] Sair
    => """))

def depositar(saldo, extrato, valor, /):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print("Depósito realizado com sucesso.")
    else:
        print("Valor inválido para depósito.")
    return saldo, extrato

def sacar(*, saldo, extrato, valor, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("Valor inválido para saque.")
    elif valor > saldo:
        print("Saldo insuficiente.")
    elif valor > limite:
        print("Valor excede o limite por saque.")
    elif numero_saques >= limite_saques:
        print("Número máximo de saques atingido.")
    else:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
        print("Saque realizado com sucesso.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n============== EXTRATO ==============")
    if not extrato:
        print("Nenhuma movimentação registrada.")
    else:
        for linha in extrato:
            print(linha)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("=====================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    if filtro_usuario(cpf, usuarios):
        print("Já existe um usuário com esse CPF.")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (rua, número - bairro - cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("Usuário criado com sucesso.")

def filtro_usuario(cpf, usuarios):
    return next((u for u in usuarios if u["cpf"] == cpf), None)

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtro_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso.")
        return {
            "agencia": agencia,
            "numero": numero_conta,
            "usuario": usuario
        }
    else:
        print("Usuário não encontrado. Crie um usuário primeiro.")

def listar_contas(contas):
    print("\n=========== CONTAS ===========")
    for conta in contas:
        print(f"Agência: {conta['agencia']}")
        print(f"Conta: {conta['numero']}")
        print(f"Titular: {conta['usuario']['nome']}")
        print("=" * 30)

def main():
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Valor do depósito: "))
            saldo, extrato = depositar(saldo, extrato, valor)

        elif opcao == "s":
            valor = float(input("Valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                extrato=extrato,
                valor=valor,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero = len(contas) + 1
            conta = criar_conta(AGENCIA, numero, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Saindo do sistema. Até logo!")
            break

        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()

