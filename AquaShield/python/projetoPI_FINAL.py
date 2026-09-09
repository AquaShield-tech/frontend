import psutil
import time
import mysql.connector
import socket
import uuid


# Grupo 4

# Danilo 
# Alicia 
# Rodrigo 
# Melissa 
# Matheus Bernardino

banco = mysql.connector.connect(
    user='root',
    password='Empresario00700@',
    host='localhost',
    database='aquashield'
)

cursor = banco.cursor()

nomeMaquina = mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])

print(f"Endereço MAC: {mac}")


def verificarMaquina():
    comando = """
        SELECT idMaquina
        FROM maquina
        WHERE nome = %s
        LIMIT 1
    """

    cursor.execute(comando, (nomeMaquina,))
    resultado = cursor.fetchone()

    if resultado is not None:
        return resultado[0]

    comando = """
        INSERT INTO maquina
        (nome, fkEmpresa)
        VALUES (%s, %s)
    """

    cursor.execute(comando, (nomeMaquina, 1))
    banco.commit()

    return cursor.lastrowid


def BancoMemoria(memoria_usada, memoria_disponivel, idMaquina):
    comando = """
        INSERT INTO memoria
        (memoria_usada, memoria_disponivel, fkMaquina)
        VALUES (%s, %s, %s)
    """

    valores = (
        memoria_usada,
        memoria_disponivel,
        idMaquina
    )

    cursor.execute(comando, valores)


def BancoDisco(discoUso, espacoLivre, idMaquina):
    comando = """
        INSERT INTO disco
        (discoUso, `espaçoLivre`, fkMaquina)
        VALUES (%s, %s, %s)
    """

    valores = (
        discoUso,
        espacoLivre,
        idMaquina
    )

    cursor.execute(comando, valores)


def BancoCPU(temperatura, frequencia, porcentagemUso, idMaquina):
    comando = """
        INSERT INTO processador
        (temperatura, frequencia, porcentagemUso, fkMaquina)
        VALUES (%s, %s, %s, %s)
    """

    valores = (
        temperatura,
        frequencia,
        porcentagemUso,
        idMaquina
    )

    cursor.execute(comando, valores)


def classificarTemperaturaCPU(temperatura):
    if temperatura <= 70:
        return "BOM"
    elif temperatura <= 85:
        return "ATENÇÃO"
    else:
        return "CRÍTICO"


def classificarUsoCPU(porcentagemUso):
    if porcentagemUso <= 70:
        return "BOM"
    elif porcentagemUso <= 95:
        return "ATENÇÃO"
    else:
        return "CRÍTICO"


def classificarFrequenciaCPU(frequenciaMHz):

    frequenciaGHz = frequenciaMHz / 1000

    if 0.79 <= frequenciaGHz <= 1.5:
        return "CRÍTICO"
    elif 1.5 < frequenciaGHz <= 2.5:
        return "BOM"
    else:
        return "ATENÇÃO"


def classificarMemoriaUsadaPercentual(percentualUsado):
    if percentualUsado <= 75:
        return "BOM"
    elif percentualUsado <= 90:
        return "ATENÇÃO"
    else:
        return "CRÍTICO"


def classificarMemoriaDisponivelPercentual(percentualDisponivel):
    if percentualDisponivel > 25:
        return "BOM"
    elif percentualDisponivel >= 10:
        return "ATENÇÃO"
    else:
        return "CRÍTICO"


def classificarDiscoUsoPercentual(percentualUso):
    if percentualUso <= 30:
        return "BOM"
    elif percentualUso <= 90:
        return "ATENÇÃO"
    else:
        return "CRÍTICO"


def classificarDiscoLivrePercentual(percentualLivre):
    if percentualLivre > 20:
        return "BOM"
    elif percentualLivre >= 10:
        return "ATENÇÃO"
    else:
        return "CRÍTICO"


# ===========================================================================


def capturaMemoria(idMaquina):
    memoria = psutil.virtual_memory()

    memoria_usada = round(memoria.used / (1024 ** 3))
    memoria_disponivel = round(memoria.available / (1024 ** 3))

    percentualUsado = memoria.percent
    percentualDisponivel = (memoria.available / memoria.total) * 100

    statusUsada = classificarMemoriaUsadaPercentual(percentualUsado)
    statusDisponivel = classificarMemoriaDisponivelPercentual(percentualDisponivel)

    BancoMemoria(
        memoria_usada,
        memoria_disponivel,
        idMaquina
    )

    print()
    print("===== MEMÓRIA =====")
    print("Memória usada:", memoria_usada, "GB", f"({percentualUsado:.1f}%) -", statusUsada)
    print("Memória disponível:", memoria_disponivel, "GB", f"({percentualDisponivel:.1f}%) -", statusDisponivel)


def capturaDisco(idMaquina):
    disco = psutil.disk_usage('C:\\')

    discoUso = round(disco.used / (1024 ** 3))
    espacoLivre = round(disco.free / (1024 ** 3))

    percentualUso = disco.percent
    percentualLivre = (disco.free / disco.total) * 100

    statusUso = classificarDiscoUsoPercentual(percentualUso)
    statusLivre = classificarDiscoLivrePercentual(percentualLivre)

    BancoDisco(
        discoUso,
        espacoLivre,
        idMaquina
    )

    print()
    print("===== DISCO =====")
    print("Disco usado:", discoUso, "GB", f"({percentualUso:.1f}%) -", statusUso)
    print("Espaço livre:", espacoLivre, "GB", f"({percentualLivre:.1f}%) -", statusLivre)


def capturaTemperaturaCPU():

    temperatura = 0

    try:
        sensores = psutil.sensors_temperatures()
    except AttributeError:
        print("Aviso: leitura de temperatura via psutil não é suportada neste SO.")
        return temperatura

    if not sensores:
        print("Aviso: nenhum sensor de temperatura foi encontrado nesta máquina.")
        return temperatura

    nomesPrioritarios = ("coretemp", "k10temp", "cpu_thermal", "acpitz")

    for nomeSensor in nomesPrioritarios:
        if nomeSensor in sensores and len(sensores[nomeSensor]) > 0:
            temperatura = sensores[nomeSensor][0].current
            return temperatura

    chaves = list(sensores.keys())
    primeiraChave = chaves[0]

    if len(sensores[primeiraChave]) > 0:
        temperatura = sensores[primeiraChave][0].current

    return temperatura

def capturaCPU(idMaquina):
    temperatura = capturaTemperaturaCPU()

    frequencia = psutil.cpu_freq()

    if frequencia is not None:
        frequenciaAtual = frequencia.current
    else:
        frequenciaAtual = 0

    porcentagemUso = psutil.cpu_percent(
        interval=1
    )

    statusTemperatura = classificarTemperaturaCPU(temperatura)
    statusFrequencia = classificarFrequenciaCPU(frequenciaAtual)
    statusUso = classificarUsoCPU(porcentagemUso)

    BancoCPU(
        temperatura,
        frequenciaAtual,
        porcentagemUso,
        idMaquina
    )

    print()
    print("===== PROCESSADOR =====")
    print("Temperatura:", round(temperatura, 2), "°C -", statusTemperatura)
    print("Frequência:", round(frequenciaAtual, 2), "MHz -", statusFrequencia)
    print("Uso:", porcentagemUso, "% -", statusUso)


def capturarDados():
    idMaquina = verificarMaquina()

    print()
    print("================================")
    print("        DADOS DA MÁQUINA")
    print("================================")

    print("Nome da máquina:", nomeMaquina)
    print("ID da máquina:", idMaquina)

    capturaCPU(idMaquina)
    capturaMemoria(idMaquina)
    capturaDisco(idMaquina)

    banco.commit()

    print()
    print("================================")
    print("DADOS CAPTURADOS COM SUCESSO!")
    print("================================")


def atualizarDados():
    print()
    print("===== ATUALIZAR =====")

    print("1 - Memória")
    print("2 - Disco")
    print("3 - Processador")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        idRegistro = input("Digite o ID da memória: ")
        novoValor = input("Digite a nova memória usada: ")

        comando = """
            UPDATE memoria
            SET memoria_usada = %s
            WHERE idMemoria = %s
        """

        cursor.execute(
            comando,
            (novoValor, idRegistro)
        )

    elif opcao == "2":
        idRegistro = input("Digite o ID do disco: ")
        novoValor = input("Digite o novo valor de disco usado: ")

        comando = """
            UPDATE disco
            SET discoUso = %s
            WHERE idDisco = %s
        """

        cursor.execute(
            comando,
            (novoValor, idRegistro)
        )

    elif opcao == "3":
        idRegistro = input("Digite o ID do processador: ")
        novoValor = input("Digite o novo percentual de uso: ")

        comando = """
            UPDATE processador
            SET porcentagemUso = %s
            WHERE idProcessador = %s
        """

        cursor.execute(
            comando,
            (novoValor, idRegistro)
        )

    else:
        print("Opção inválida.")
        return

    banco.commit()

    print()
    print("REGISTRO ATUALIZADO COM SUCESSO!")


def deletarDados():
    print()
    print("===== DELETAR =====")

    print("1 - Memória")
    print("2 - Disco")
    print("3 - Processador")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        idRegistro = input("Digite o ID da memória: ")

        comando = """
            DELETE FROM memoria
            WHERE idMemoria = %s
        """

    elif opcao == "2":
        idRegistro = input("Digite o ID do disco: ")

        comando = """
            DELETE FROM disco
            WHERE idDisco = %s
        """

    elif opcao == "3":
        idRegistro = input("Digite o ID do processador: ")

        comando = """
            DELETE FROM processador
            WHERE idProcessador = %s
        """

    else:
        print("Opção inválida.")
        return

    cursor.execute(
        comando,
        (idRegistro,)
    )

    banco.commit()

    print()
    print("REGISTRO DELETADO COM SUCESSO!")


# ===================== VISUALIZAÇÃO =====================

def visualizarMemoria(idMaquina):
    comando = """
        SELECT idMemoria, dtHora, memoria_usada, memoria_disponivel
        FROM memoria
        WHERE fkMaquina = %s
        ORDER BY dtHora DESC
    """

    cursor.execute(comando, (idMaquina,))
    registros = cursor.fetchall()

    print()
    print("===== HISTÓRICO DE MEMÓRIA =====")
    print("(% estimado a partir dos GB salvos: usado / (usado + disponível) * 100)")

    if len(registros) == 0:
        print("Nenhum registro encontrado.")
        return

    print(f"{'ID':<5} {'Data/Hora':<20} {'Usada (GB)':<12} {'Disp. (GB)':<12} {'Status Usada':<14} {'Status Disp.':<14}")
    print("-" * 90)

    for linha in registros:
        idRegistro, dtHora, memUsada, memDisponivel = linha

        total = memUsada + memDisponivel
        if total > 0:
            percentualUsado = (memUsada / total) * 100
            percentualDisponivel = (memDisponivel / total) * 100
        else:
            percentualUsado = 0
            percentualDisponivel = 0

        statusUsada = classificarMemoriaUsadaPercentual(percentualUsado)
        statusDisponivel = classificarMemoriaDisponivelPercentual(percentualDisponivel)

        print(f"{idRegistro:<5} {str(dtHora):<20} {memUsada:<12} {memDisponivel:<12} {statusUsada:<14} {statusDisponivel:<14}")


def visualizarDisco(idMaquina):
    comando = """
        SELECT idDisco, dtHora, discoUso, `espaçoLivre`
        FROM disco
        WHERE fkMaquina = %s
        ORDER BY dtHora DESC
    """

    cursor.execute(comando, (idMaquina,))
    registros = cursor.fetchall()

    print()
    print("===== HISTÓRICO DE DISCO =====")
    print("(% estimado a partir dos GB salvos: usado / (usado + livre) * 100)")

    if len(registros) == 0:
        print("Nenhum registro encontrado.")
        return

    print(f"{'ID':<5} {'Data/Hora':<20} {'Usado (GB)':<12} {'Livre (GB)':<12} {'Status Uso':<14} {'Status Livre':<14}")
    print("-" * 90)

    for linha in registros:
        idRegistro, dtHora, discoUso, espacoLivre = linha

        total = discoUso + espacoLivre
        if total > 0:
            percentualUso = (discoUso / total) * 100
            percentualLivre = (espacoLivre / total) * 100
        else:
            percentualUso = 0
            percentualLivre = 0

        statusUso = classificarDiscoUsoPercentual(percentualUso)
        statusLivre = classificarDiscoLivrePercentual(percentualLivre)

        print(f"{idRegistro:<5} {str(dtHora):<20} {discoUso:<12} {espacoLivre:<12} {statusUso:<14} {statusLivre:<14}")


def visualizarProcessador(idMaquina):
    comando = """
        SELECT idProcessador, dtHora, temperatura, frequencia, porcentagemUso
        FROM processador
        WHERE fkMaquina = %s
        ORDER BY dtHora DESC
    """

    cursor.execute(comando, (idMaquina,))
    registros = cursor.fetchall()

    print()
    print("===== HISTÓRICO DO PROCESSADOR =====")
    print("(Se a Temp. aparecer como 0, verifique se há sensores compatíveis via psutil.sensors_temperatures() nesta máquina)")

    if len(registros) == 0:
        print("Nenhum registro encontrado.")
        return

    print(f"{'ID':<5} {'Data/Hora':<20} {'Temp(°C)':<10} {'St.Temp':<10} {'Freq(MHz)':<12} {'St.Freq':<10} {'Uso(%)':<8} {'St.Uso':<10}")
    print("-" * 100)

    for linha in registros:
        idRegistro, dtHora, temperatura, frequencia, porcentagemUso = linha

        statusTemperatura = classificarTemperaturaCPU(float(temperatura))
        statusFrequencia = classificarFrequenciaCPU(float(frequencia))
        statusUso = classificarUsoCPU(float(porcentagemUso))

        print(f"{idRegistro:<5} {str(dtHora):<20} {temperatura:<10} {statusTemperatura:<10} {frequencia:<12} {statusFrequencia:<10} {porcentagemUso:<8} {statusUso:<10}")


def visualizarDados():
    idMaquina = verificarMaquina()

    while True:
        print()
        print("===== VISUALIZAR DADOS =====")
        print("Máquina:", nomeMaquina)

        print("1 - Memória")
        print("2 - Disco")
        print("3 - Processador")
        print("4 - Voltar ao menu")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            visualizarMemoria(idMaquina)

        elif opcao == "2":
            visualizarDisco(idMaquina)

        elif opcao == "3":
            visualizarProcessador(idMaquina)

        elif opcao == "4":
            break

        else:
            print("Opção inválida.")


# ==========================================================


def capturaAutomatica():
    while True:
        print()
        print("===== CAPTURA AUTOMÁTICA =====")

        print("1 - Fazer captura")
        print("2 - Parar captura")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            capturarDados()

            print()
            print("Próxima captura em 5 segundos...")

            time.sleep(5)

        elif opcao == "2":
            print("Captura automática encerrada.")
            break

        else:
            print("Opção inválida.")


while True:
    print()
    print("==============================")
    print("         AQUASHIELD")
    print("==============================")

    print("Máquina:", nomeMaquina)

    print()
    print("1 - Capturar dados")
    print("2 - Atualizar dados")
    print("3 - Deletar dados")
    print("4 - Captura automática")
    print("5 - Visualizar dados")
    print("6 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        capturarDados()

    elif opcao == "2":
        atualizarDados()

    elif opcao == "3":
        deletarDados()

    elif opcao == "4":
        capturaAutomatica()

    elif opcao == "5":
        visualizarDados()

    elif opcao == "6":
        print("Encerrando programa...")

        cursor.close()
        banco.close()

        break

    else:
        print("Opção inválida.")