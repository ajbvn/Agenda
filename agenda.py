import sys
from string import ascii_uppercase

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

def dataFormatada(data):
    return (data[0:2]+"/"+data[2:4]+"/"+data[4:8])

def horaFormatada(hora):
    return (hora[0:2]+":"+hora[2:4])

def inteiroDataHora(data, hora):
    dia = data[0:2]
    mes = data[2:4]
    ano = data[4:8]
    return (int(ano+mes+dia+hora))

def comparaDatas(data1, hora1, data2, hora2):
    d1 = inteiroDataHora(data1, hora1)
    d2 = inteiroDataHora(data2, hora2)
    return (d1 > d2)

def printCores(texto, cor):
    print(cor + texto + RESET)

def adicionar(descricao, extras):
    if descricao == '':
        return(False)
    data, hora, pri, ctx, proj = extras

    novaAtividade = descricao
    if pri:
        novaAtividade = pri + " " + novaAtividade
    if hora:
        novaAtividade = hora + " " + novaAtividade
    if data:
        novaAtividade = data + " " + novaAtividade
    if ctx:
        novaAtividade = novaAtividade + " " + ctx
    if proj:
        novaAtividade = novaAtividade + " " + proj

    try:
        f = open(TODO_FILE, 'a')
        f.write(novaAtividade + "\n")
        f.close()
    except IOError as err:
        print("Não foi possível escrever para o arquivo " + TODO_FILE)
        print(err)
        return(False)
    return(True)

def prioridadeValida(pri):
    if len(pri) != 3:
        return(False)
    if pri[0] != '(' or pri[2] != ')':
        return(False)
    if not pri[1].isalpha():
        return(False)
    return(True)

def horaValida(horaMin):
    if len(horaMin) != 4 or not soDigitos(horaMin):
        return(False)
    else:
        horaMin = int(horaMin)
        horas = horaMin // 100
        minutos = horaMin % 100
        if horas > 23 or minutos > 59:
            return(False)
    return(True)

def dataValida(data):
    if len(data) != 8 or not soDigitos(data):
        return(False)
    else:
        data = int(data)
        dia = data // 1000000
        mes = (data // 10000) % 100
        if dia < 1 or dia > 31 or mes < 1 or mes > 12:
            return(False)
        if mes in [4, 6, 9, 11]:
            if dia > 30:
                return(False)
        if mes == 2:
            if dia > 29:
                return(False)
    return(True)

def projetoValido(proj):
    if len(proj) < 2:
        return(False)
    if proj[0] != '+':
        return(False)
    return(True)

def contextoValido(cont):
    if len(cont) < 2:
        return(False)
    if cont[0] != '@':
        return(False)
    return(True)

def soDigitos(numero):
    if type(numero) != str:
        return(False)
    for x in numero:
        if x < '0' or x > '9':
            return(False)
    return(True)

def organizar(linhas):
    itens = []

    for l in linhas:
        data = ''
        hora = ''
        pri = ''
        desc = ''
        contexto = ''
        projeto = ''

        tokens = l.strip().split()

        if dataValida(tokens[0]):
            data = tokens.pop(0)
        if horaValida(tokens[0]):
            hora = tokens.pop(0)
        if prioridadeValida(tokens[0]):
            pri = tokens.pop(0)
        if projetoValido(tokens[-1]):
            projeto = tokens.pop(-1)
        if contextoValido(tokens[-1]):
            contexto = tokens.pop(-1)
        desc = " ".join(tokens)

        itens.append((desc, (data, hora, pri, contexto, projeto)))

    return(itens)

def listar():
    f = open(TODO_FILE, "r")
    itens = organizar(f.readlines())
    f.close()
    itens = ordenarPorDataHora(itens)
    itens = ordenarPorPrioridade(itens)

    for i in range(len(itens)):
        descricao, extras = itens[i]
        data, hora, pri, ctx, proj = extras

        atividade = f"{i+1}"
        if data:
            atividade += " " + dataFormatada(data)
        if hora:
            atividade += " " + horaFormatada(hora)
        if pri:
            atividade += " " + pri
        atividade += " " + descricao
        if ctx:
            atividade += " " + ctx
        if proj:
            atividade += " " + proj

        if pri in ["(A)", "(B)", "(C)", "(D)"]:
            if pri == "(A)":
                printCores(atividade, RED)
            if pri == "(B)":
                printCores(atividade, YELLOW)
            if pri == "(C)":
                printCores(atividade, BLUE)
            if pri == "(D)":
                printCores(atividade, GREEN)
        else:
            print(atividade)

def ordenarPorDataHora(itens):
    for i in range(len(itens)-1):
        for j in range(i, len(itens)):
            datai = itens[i][1][0]
            if not datai:
                datai = "99999999"
            horai = itens[i][1][1]
            if not horai:
                horai = "9999"
            dataj = itens[j][1][0]
            if not dataj:
                dataj = "99999999"
            horaj = itens[j][1][1]
            if not horaj:
                horaj = "9999"
            if comparaDatas(datai, horai, dataj, horaj):
                itens[i], itens[j] = itens[j], itens[i]
    return(itens)

def ordenarPorPrioridade(itens):
    pos = 0
    for c in ascii_uppercase:
        for i in range(pos, len(itens)):
            pri = itens[i][1][2]
            if pri:
                if pri[1].upper() == c:
                    item = itens.pop(i)
                    itens.insert(pos, item)
                    pos += 1
    return(itens)

def fazer(num):
    item = remover(num)

    descricao, extras = item
    data, hora, pri, ctx, proj = extras

    atividade = descricao
    if pri:
        atividade = pri + " " + atividade
    if hora:
        atividade = hora + " " + atividade
    if data:
        atividade = data + " " + atividade
    if ctx:
        atividade = atividade + " " + ctx
    if proj:
        atividade = atividade + " " + proj

    f = open(ARCHIVE_FILE, 'a')
    f.write(atividade + "\n")
    f.close()


def remover(num):
    f = open(TODO_FILE, "r")
    itens = organizar(f.readlines())
    f.close()
    itens = ordenarPorDataHora(itens)
    itens = ordenarPorPrioridade(itens)

    if num < 1 or num > len(itens):
        print("Essa atividade não existe.")
    else:
        removido = itens.pop(num-1)
        f = open(TODO_FILE, "w")
        f.close()
        for item in itens:
            adicionar(item[0], item[1])
        return(removido)

def priorizar(num, prioridade):
    f = open(TODO_FILE, "r")
    itens = organizar(f.readlines())
    f.close()
    itens = ordenarPorDataHora(itens)
    itens = ordenarPorPrioridade(itens)

    if num < 1 or num > len(itens):
        print("Essa atividade não existe.")
    else:
        descricao, extras = itens[num-1]
        data, hora, pri, ctx, proj = extras
        pri = "(" + prioridade + ")"
        remover(num)
        adicionar(descricao, (data, hora, pri, ctx, proj))
    return()

def processarComandos(comandos):
    if comandos[1] == ADICIONAR:
        comandos.pop(0)
        comandos.pop(0)
        itemParaAdicionar = organizar([' '.join(comandos)])[0]
        adicionar(itemParaAdicionar[0], itemParaAdicionar[1])
    elif comandos[1] == LISTAR:
        listar()
    elif comandos[1] == REMOVER:
        remover(int(comandos[2]))
    elif comandos[1] == FAZER:
        fazer(int(comandos[2]))
    elif comandos[1] == PRIORIZAR:
        priorizar(int(comandos[2]), comandos[3])
    else:
        print("Comando inválido.")

f = open(TODO_FILE, 'a')
f.close()
f = open(ARCHIVE_FILE, 'a')
f.close()

processarComandos(sys.argv)
