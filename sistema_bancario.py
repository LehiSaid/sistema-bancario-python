
import textwrap

def menu():
    menu_text = """\n
    ================ MENU ================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q] Sair
    => """
    return input(textwrap.dedent(menu_text))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Valor inválido!")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("Saldo insuficiente!")
    elif valor > limite:
        print("Excede o limite por saque!")
    elif numero_saques >= limite_saques:
        print("Número máximo de saques atingido!")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Valor inválido!")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n============== EXTRATO ==============")
    print(extrato if extrato else "Sem movimentações.")
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=====================================")

def criar_usuario(usuarios):
    cpf = input("CPF (somente números): ")
    if any(u["cpf"] == cpf for u in usuarios):
        print("Usuário já cadastrado.")
        return
    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (rua, nº - bairro - cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("Usuário criado com sucesso!")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("CPF do usuário: ")
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero": numero_conta, "usuario": usuario}
    print("Usuário não encontrado.")

def listar_contas(contas):
    for conta in contas:
        print("=" * 30)
        print(f"Agência: {conta['agencia']}")
        print(f"Número da Conta: {conta['numero']}")
        print(f"Titular: {conta['usuario']['nome']}")

def main():
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo, valor=valor, extrato=extrato,
                limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES
            )
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == "nu":
            criar_usuario(usuarios)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
