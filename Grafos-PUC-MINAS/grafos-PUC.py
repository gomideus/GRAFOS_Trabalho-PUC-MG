from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from tkinter import *
import numpy as np
import geopy.distance
import os

checkButton = 0

def isButtonOnePressed():
    global checkButton
    checkButton = 1

def isButtonTwoPressed():
    global checkButton
    checkButton = 2

def isButtonThreePressed():
    global checkButton
    checkButton = 3

def isButtonFourPressed():
    global checkButton
    checkButton = 4


def isButtonFivePressed():
    global checkButton
    checkButton = 5

root = Tk()
myButtonOne = Button(root, text="MENOR CAMINHO", command = isButtonOnePressed )
myButtonTwo = Button(root, text="MEDIR TARIFA", command = isButtonTwoPressed )
myButtonThree = Button(root, text="TARIFA - MUNDO", command = isButtonThreePressed )
myButtonFour = Button(root, text="ALTURA DE VOO", command = isButtonFourPressed )
myButtonFive = Button(root, text="FECHAR", command = isButtonFivePressed )

altura_botao = 2
largura_botao = 30

myButtonOne.config( height = altura_botao, width = largura_botao )
myButtonTwo.config( height = altura_botao, width = largura_botao )
myButtonThree.config( height = altura_botao, width = largura_botao )
myButtonFour.config( height = altura_botao, width = largura_botao )
myButtonFive.config( height = altura_botao, width = largura_botao )

root.geometry("300x250+1500+700")

inputtxt = Text(root, height = 1,width = 4, bg = "gray")
inputtxtB = Text(root, height = 1,width = 4,bg = "gray")

inputtxt.pack()
inputtxtB.pack()
myButtonOne.pack()
myButtonTwo.pack()
myButtonThree.pack()
myButtonFour.pack()
myButtonFive.pack()

while checkButton != 5: # Enquanto o botão FECHAR não for pressionado

    fig = plt.figure(figsize=(12,9))

    m = Basemap(projection='mill',
                llcrnrlat = -90,
                urcrnrlat = 90,
                llcrnrlon = -180,
                urcrnrlon = 180,
                resolution = 'c')

    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary(fill_color='lightskyblue')
    m.fillcontinents(color='white')

    sigla = [] # Vetor para guardar SIGLAS
    lat = [] # Vetor para guardar Latitudes
    longi = [] # Vetor para guardar Longitudes

    getnum = open('airports.txt')
    num_airports_str = getnum.readline()
    getnum.close

    num_airports = int(num_airports_str)

    reader = open('airports.txt') # Abrir arquivo contendo SIGLA, Latitude e Longitude dos aeroportos

    # Pegar SIGLA
    for x in reader:
        for string in reader:
            strA = ""
            j = 0
            while string[j] != ' ':
                strA = strA + string[j]
                j+=1
            sigla.append(strA)

            j+=1

            # Pegar Latitude
            strA = ""
            while string[j] != ' ':
                strA = strA + string[j]
                j+=1
            lat.append(float(strA))

            j+=1

            # Pegar Longitude
            strA = ""
            while j < len(string) and string[j] != '\n':
                strA = strA + string[j]
                j+=1
            longi.append(float(strA))

    reader.close()

    array = np.zeros((num_airports,num_airports)) # Criando matriz de adjacencia com '0' em todas posições
    arrayDistances = np.zeros((num_airports,num_airports)) # Criando matriz de distancias/tarifas com '0' em todas posições

    sAux = []
    origem = [] # Array para guardar SIGLA do aeroporto de origem
    destino = [] # Array para guardar SIGLA do aeroporto de destino
    preco = [] # Para guardar precos das rotas
    actualRespA_arr = []
    actualRespB_arr = []

    readerB = open('rotas.txt') # Abrir arquivo de rotas

    # Pegar SIGLA (origem)
    for x in readerB:
        n = int(x)
        for string in readerB:
            strA = ""
            j = 0
            while string[j] != ' ':
                strA = strA + string[j]
                j+=1
            origem.append(strA)

            j+=1

            # Pegar SIGLA (destino)
            strA = ""
            while string[j] != ' ':
                strA = strA + string[j]
                j+=1
            destino.append((strA))

            j+=1

            # Pegar preco da rota
            strA = ""
            while j < len(string) and string[j] != '\n':
                strA = strA + string[j]
                j+=1
            preco.append(int(strA))

    readerB.close()
            

    latiOrigem = [] # Para guardar latitude do vertice de origem
    longiOrigem = [] # Para guardar longitude do vertice de origem
    latiDestino = [] # Para guardar latitude do vertice de destino
    longiDestino = [] # Para guardar longitude do vertice de destino

    # Pegar latitude e longitude de origem e armazenar no array
    for x in origem :
        i = 0
        for y in sigla:
            if x == y:
                latiOrigem.append(lat[i])
                longiOrigem.append(longi[i])
                break
            i+=1
    
    # Pegar latitude e longitude de destino e armazenar no array
    for x in destino :
        i = 0
        for y in sigla:
            if x == y:
                latiDestino.append(lat[i])
                longiDestino.append(longi[i])
                break
            i+=1


    if checkButton == 1: # Se o primeiro botão for pressionado

        # Limpar terminal
        clear = lambda: os.system('cls')
        clear()

        print('\nBOTÃO 1 - MENOR CAMINHO - Pressionado\n')

        INPUT = inputtxt.get("1.0", "end-1c") # Receber SIGLA escrita no primeiro campo de texto
        INPUT_B = inputtxtB.get("1.0", "end-1c") # Receber SIGLA escrita no segundo campo de texto

        def swap(xPos): 

            tempSigla = sigla[0]
            tempLati = lat[0]
            tempLongi = longi[0]


            sigla[0] = sigla[xPos]
            lat[0] = lat[xPos]
            longi[0] = longi[xPos]


            sigla[xPos] = tempSigla
            lat[xPos] = tempLati
            longi[xPos] = tempLongi

        achou = False
        xn=0
        for value in sigla:
            if INPUT == value and achou == False:
                swap(xn)
                achou = True
                break
            xn += 1

        # Para pegar o index do destino
        numDestino = 0
        for item in sigla:
            if item == INPUT_B:
                break
            numDestino+=1
        
        w=0
        while w < n:
            sAux = origem[w]
            auxCounter = 0
            fim = False
            actualResp = -1
            for strin in sigla:
                if fim == False:
                    if strin == sAux:
                        fim = True
                        actualResp = auxCounter
                        actualRespA_arr.append(actualResp)
                    auxCounter = auxCounter + 1

            sAux = destino[w]
            auxCounter = 0
            fim = False
            actualRespB = -1
            for strinB in sigla:
                if fim == False:
                    if strinB == sAux:
                        fim = True
                        actualRespB = auxCounter
                        actualRespB_arr.append(actualRespB)
                    auxCounter = auxCounter + 1
            w+=1


            array[actualResp][actualRespB] = 1
            array[actualRespB][actualResp] = 1


        tracker = [] # Pegar rota do algoritmo Djikstra
        distanciaTotal = 0 
        destinoFinal = 0 # Armazena o index do vertice de destino

        distancias = []

        # Criando matriz de adjacencia a partir das distancias reais entre latitude/longitude dos vertices de origem/destino
        auxNumber = 0
        for aux in latiOrigem:
            coords1 = (latiOrigem[auxNumber], longiOrigem[auxNumber])
            coords2 = (latiDestino[auxNumber], longiDestino[auxNumber])
            dist =  geopy.distance.geodesic(coords1, coords2).km
            distancias.append(round(dist,2))
            arrayDistances[actualRespA_arr[auxNumber]][actualRespB_arr[auxNumber]] = round(dist,2)
            arrayDistances[actualRespB_arr[auxNumber]][actualRespA_arr[auxNumber]] = round(dist,2)
            auxNumber = auxNumber + 1

        print(arrayDistances) 

        #Class para representar o grafo
        class Grafo:
        
            def menorDist(self,dist,fila):
                valorMinimo = float(99999999999) # Setar valor minimo como maior possível
                indexMinimo = -1
                for i in range(len(dist)):
                    if dist[i] < valorMinimo and i in fila: # Se o valor atual for menor que o valor minimo
                        valorMinimo = dist[i] # Substituir valor minimo
                        indexMinimo = i # Atualizar index
                return indexMinimo # Retornar index
        

            # Este algorítimo é executado recursivamente. Ele se inicia obtendo todas as rotas que levam ao destino, e quando chega na origem entra no if, parando
            # a recursividade e printando o caminho completo desde a origem (0) até o destino (j)
            def pegarRota(self, pai, j):
                
                if pai[j] == -1 : # Se o pai do vértice for o vértice origem
                    tracker.append(j) # Dar append de 0
                    return
                self.pegarRota(pai , pai[j])
                tracker.append(j) # Dar append nos vértices do caminho

            def mostrarResultado(self, dist, pai, numDestino):
                src = 0
                for i in range(numDestino, numDestino+1): # Percorre apenas o vértice escolhido como destino
                    print("\nOrigem: %d --> Destino: %d \t Distancia Total: %d \t" % (src, i, dist[i])), # Mostra dados no terminal (origem,destino e distancia)
                    global distanciaTotal 
                    distanciaTotal = dist[i] # Armazenar distancia
                    global destinoFinal
                    destinoFinal = i # Armazenar índice do destino
                    self.pegarRota(pai,i) # Chamar função para pegar rota da origem para o destino

            def dijkstra(self, grafo, src):
        
                num_linhas = len(grafo)
                num_colunas = len(grafo[0])

                dist = [float(99999999999)] * num_linhas # Array que irá guardar menor distancia entre vértices. Inicializa armazenando maior valor (infinito) 
        
                pai = [-1] * num_linhas # Para armazenar menor caminho
        
                dist[src] = 0 # Distancia de um vértice para ele mesmo
            
                fila = [] # Adicionar todos os vértices na fila
                for i in range(num_linhas):
                    fila.append(i)
                    
                # Achar menor caminho para todos os vértices
                while fila:
        
                    k = self.menorDist(dist,fila)  # Pegar vértice de menor distancia do conjunto de vertices da fila
        
                    fila.remove(k) # Remover menor elemento

                    # Atualizar valor de distancia e index do pai dos vertices adjacentes ao vertice escolhido.
                    for i in range(num_colunas):
                        if grafo[k][i] and i in fila:
                            if dist[k] + grafo[k][i] < dist[i]:
                                dist[i] = dist[k] + grafo[k][i]
                                pai[i] = k
        
        
                self.mostrarResultado(dist,pai,numDestino)
        
        g= Grafo()
        
        grafo = arrayDistances
        
        # Printar a solução
        g.dijkstra(grafo,0)
        print(tracker)

        # Criação do mapa -> vértices e arestas vermelhos
        i=0
        while i<n:
            xs = []
            ys = []
            xpt, ypt = m(longiOrigem[i], latiOrigem[i])
            xs.append(xpt)
            ys.append(ypt)
            plt.annotate(origem[i], m(longiOrigem[i], latiOrigem[i]),fontsize = 15)
            plt.annotate(destino[i], m(longiDestino[i], latiDestino[i]),fontsize = 15)
            xpt, ypt = m(longiDestino[i], latiDestino[i])
            xs.append(xpt)
            ys.append(ypt)
            m.plot(xs, ys, 'o-', color ='r', markersize=5, linewidth=1.5)
            i+=1

        i=0
        length = len(tracker)

        # Criação da rota retornada pelo algoritmo de Djikstra (mostrando na cor VERDE)
        while i < length-1:
            i+=1
            xd = []
            yd = []
            xpt, ypt = m(longi[tracker[i-1]], lat[tracker[i-1]])
            xd.append(xpt)
            yd.append(ypt)
            xpt, ypt = m(longi[tracker[i]], lat[tracker[i]])
            xd.append(xpt)
            yd.append(ypt)
            m.plot(xd, yd, 'o-', color ='g', markersize=15, linewidth=1.5)

        
        plt.title('Mapa De Conexão de Aeroportos')
        plt.show()



    elif checkButton == 2: # Se o segundo botão for pressionado

        # Limpar terminal
        clear = lambda: os.system('cls')
        clear()

        print('\nBOTÃO 2 - Medir Tarifa - Pressionado\n')

        INPUT = inputtxt.get("1.0", "end-1c") # Receber SIGLA escrita no primeiro campo de texto
        INPUT_B = inputtxtB.get("1.0", "end-1c") # Receber SIGLA escrita no segundo campo de texto

        def swap(xPos):

            tempSigla = sigla[0]
            tempLati = lat[0]
            tempLongi = longi[0]


            sigla[0] = sigla[xPos]
            lat[0] = lat[xPos]
            longi[0] = longi[xPos]


            sigla[xPos] = tempSigla
            lat[xPos] = tempLati
            longi[xPos] = tempLongi

        achou = False
        xn=0
        for value in sigla:
            if INPUT == value and achou == False:
                swap(xn)
                achou = True
                break
            xn += 1

        # Para pegar o index do destino
        numDestino = 0
        for item in sigla:
            if item == INPUT_B:
                break
            numDestino+=1
        
        w=0
        while w < n:
            sAux = origem[w]
            auxCounter = 0
            fim = False
            actualResp = -1
            for strin in sigla:
                if fim == False:
                    if strin == sAux:
                        fim = True
                        actualResp = auxCounter
                        actualRespA_arr.append(actualResp)
                    auxCounter = auxCounter + 1

            sAux = destino[w]
            auxCounter = 0
            fim = False
            actualRespB = -1
            for strinB in sigla:
                if fim == False:
                    if strinB == sAux:
                        fim = True
                        actualRespB = auxCounter
                        actualRespB_arr.append(actualRespB)
                    auxCounter = auxCounter + 1
            w+=1


            array[actualResp][actualRespB] = 1
            array[actualRespB][actualResp] = 1

        tracker = [] # Pegar rota do algoritmo Djikstra
        distanciaTotal = 0 
        destinoFinal = 0 # Armazena o index do vertice de destino

        distancias = []

        # Criando matriz de adjacencia armazenando os preços
        auxNumber = 0
        while auxNumber < n:
            arrayDistances[actualRespA_arr[auxNumber]][actualRespB_arr[auxNumber]] = preco[auxNumber]
            arrayDistances[actualRespB_arr[auxNumber]][actualRespA_arr[auxNumber]] = preco[auxNumber]
            auxNumber = auxNumber + 1

        print(arrayDistances)

        #Class para representar o grafo
        class Grafo:
        
            def menorDist(self,dist,fila):
                valorMinimo = float(99999999999) # Setar valor minimo como maior possível
                indexMinimo = -1
                for i in range(len(dist)):
                    if dist[i] < valorMinimo and i in fila: # Se o valor atual for menor que o valor minimo
                        valorMinimo = dist[i] # Substituir valor minimo
                        indexMinimo = i # Atualizar index
                return indexMinimo # Retornar index
        

            # Este algorítimo é executado recursivamente. Ele se inicia obtendo todas as rotas que levam ao destino, e quando chega na origem entra no if, parando
            # a recursividade e printando o caminho completo desde a origem (0) até o destino (j)
            def pegarRota(self, pai, j):
                
                if pai[j] == -1 : # Se o pai do vértice for o vértice origem
                    tracker.append(j) # Dar append de 0
                    return
                self.pegarRota(pai , pai[j])
                tracker.append(j) # Dar append nos vértices do caminho

            def mostrarResultado(self, dist, pai, numDestino):
                src = 0
                for i in range(numDestino, numDestino+1): # Percorre apenas o vértice escolhido como destino
                    print("\nOrigem: %d --> Destino: %d \t Distancia Total: %d \t" % (src, i, dist[i])), # Mostra dados no terminal (origem,destino e distancia)
                    global distanciaTotal 
                    distanciaTotal = dist[i] # Armazenar distancia
                    global destinoFinal
                    destinoFinal = i # Armazenar índice do destino
                    self.pegarRota(pai,i) # Chamar função para pegar rota da origem para o destino

            def dijkstra(self, grafo, src):
        
                num_linhas = len(grafo)
                num_colunas = len(grafo[0])

                dist = [float(99999999999)] * num_linhas # Array que irá guardar menor distancia entre vértices. Inicializa armazenando maior valor (infinito) 
        
                pai = [-1] * num_linhas # Para armazenar menor caminho
        
                dist[src] = 0 # Distancia de um vértice para ele mesmo
            
                fila = [] # Adicionar todos os vértices na fila
                for i in range(num_linhas):
                    fila.append(i)
                    
                # Achar menor caminho para todos os vértices
                while fila:
        
                    k = self.menorDist(dist,fila)  # Pegar vértice de menor distancia do conjunto de vertices da fila
        
                    fila.remove(k) # Remover menor elemento

                    # Atualizar valor de distancia e index do pai dos vertices adjacentes ao vertice escolhido.
                    for i in range(num_colunas):
                        if grafo[k][i] and i in fila:
                            if dist[k] + grafo[k][i] < dist[i]:
                                dist[i] = dist[k] + grafo[k][i]
                                pai[i] = k
        
        
                self.mostrarResultado(dist,pai,numDestino)
        
        g= Grafo()
        
        grafo = arrayDistances
        
        # Printar a solução
        g.dijkstra(grafo,0)

        print(tracker)

        # Criação do mapa -> vértices e arestas vermelhos
        i=0
        while i<n:
            xs = []
            ys = []
            xpt, ypt = m(longiOrigem[i], latiOrigem[i])
            xs.append(xpt)
            ys.append(ypt)
            plt.annotate(origem[i], m(longiOrigem[i], latiOrigem[i]),fontsize = 15)
            plt.annotate(destino[i], m(longiDestino[i], latiDestino[i]),fontsize = 15)
            xpt, ypt = m(longiDestino[i], latiDestino[i])
            xs.append(xpt)
            ys.append(ypt)
            m.plot(xs, ys, 'o-', color ='r', markersize=5, linewidth=1.5)
            i+=1

        i=0
        length = len(tracker)

        # Criação da rota retornada pelo algoritmo de Djikstra (cor AZUL)
        while i < length-1:
            i+=1
            xd = []
            yd = []
            xpt, ypt = m(longi[tracker[i-1]], lat[tracker[i-1]])
            xd.append(xpt)
            yd.append(ypt)
            xpt, ypt = m(longi[tracker[i]], lat[tracker[i]])
            xd.append(xpt)
            yd.append(ypt)
            m.plot(xd, yd, 'o-', color ='b', markersize=15, linewidth=1.5)
        
        plt.title('Mapa De Conexão de Aeroportos')
        plt.show()

    elif checkButton == 3: # Quando botão 3 por pressionado

        # Limpar o terminal
        clear = lambda: os.system('cls')
        clear()

        print('BOTÃO 3 - TARIFA MUNDO - Pressionado')
        
        w=0
        while w < n:
            sAux = origem[w]
            auxCounter = 0
            fim = False
            actualResp = -1
            for strin in sigla:
                if fim == False:
                    if strin == sAux:
                        fim = True
                        actualResp = auxCounter
                        actualRespA_arr.append(actualResp)
                    auxCounter = auxCounter + 1

            sAux = destino[w]
            auxCounter = 0
            fim = False
            actualRespB = -1
            for strinB in sigla:
                if fim == False:
                    if strinB == sAux:
                        fim = True
                        actualRespB = auxCounter
                        actualRespB_arr.append(actualRespB)
                    auxCounter = auxCounter + 1
            w+=1

            array[actualResp][actualRespB] = 1
            array[actualRespB][actualResp] = 1

        circuito = []

        # Criando matriz de adjacencia armazenando os preços
        auxNumber = 0
        while auxNumber < n:
            arrayDistances[actualRespA_arr[auxNumber]][actualRespB_arr[auxNumber]] = preco[auxNumber]
            arrayDistances[actualRespB_arr[auxNumber]][actualRespA_arr[auxNumber]] = preco[auxNumber]
            auxNumber = auxNumber + 1

        print(arrayDistances)
  
        mapa = {}
        matriz = []
        nos = []

        def algoritmo():

            global matriz
            global mapa
            global nos

            matriz = arrayDistances

            caminho = [ _ for _ in range(1, num_airports)]

            valor = heuristicaMenorCaminho(0, caminho)
            caminho = rebuild_path(0, caminho)

            circuito_str = ""

            for i in caminho:
                circuito_str = circuito_str + str(i + 1) + " - "
                circuito.append((int(str(i+1))))


            print("Valor : " + str(valor))
 

        def heuristicaMenorCaminho(num_airports, caminho):

            global matriz
            global mapa
            global nos

            if len(caminho) == 0:
                return matriz[0][num_airports]

            key = str(num_airports) + "_" + "".join(map(str, caminho))

            # se valor ja estiver no mapa => utilizar
            if key in mapa:
                return mapa[key]["value"]
            else:
                #se nao => calcular recursivamente
                # guarda as chamadas para no final decidir a mais barata
                calls = []

                for i in caminho: # para cada elemento do conjunto de pontos => calcular custo

                    new_caminho = [ _ for _ in caminho if _ is not i ]
                    new_key = str(i) + "_" + "".join(map(str, new_caminho))
                    res = heuristicaMenorCaminho(i, new_caminho) + matriz[i][num_airports] # chamada recursiva
                    map_obj = { "value" : res, "from" : i }
                    calls.append(map_obj)

                minimo = min(calls, key=lambda x : x["value"])
            
                new_key = str(num_airports) + "_" + "".join(map(str, caminho))
                map_obj = { "value" : minimo['value'], "from" : minimo['from'] } # guarda custo no mapa de custos para possivel uso futuro
                mapa[new_key] = map_obj

                return minimo['value']


        # refaz o caminho e retorna os pontos onde o custo eh menor
        def rebuild_path(inicial, conj_pontos) :
        
            global mapa

            caminho = [0] # inicia com ponto zero

            pontos = conj_pontos
            chegada = inicial

            while(True):
                key = str(chegada) + "_" + "".join(map(str, pontos))
                try: # ate nao encontrar a chave no MAPA => remontar o caminho
                    atual = mapa[key] 

                    pontos = [ _ for _ in list(str(key.split("_")[1])) if _ not in [ str(atual['from']) ]]
                    chegada = atual['from']

                    caminho.append(atual['from'])
                except: # quando der error de acesso no mapa => o caminho foi encontrado
                    caminho.append(0) # adiciona ponto inicial
                    break;

            return caminho[::-1] # retorna o inverso do caminho ( do inicio ao fim )

        algoritmo()

        # Criação de mapa com vértices e arestas vermelhos 
        i=0
        while i<n:
            xs = []
            ys = []
            xpt, ypt = m(longiOrigem[i], latiOrigem[i])
            xs.append(xpt)
            ys.append(ypt)
            plt.annotate(origem[i], m(longiOrigem[i], latiOrigem[i]),fontsize = 15)
            plt.annotate(destino[i], m(longiDestino[i], latiDestino[i]),fontsize = 15)
            xpt, ypt = m(longiDestino[i], latiDestino[i])
            xs.append(xpt)
            ys.append(ypt)
            m.plot(xs, ys, 'o-', color ='r', markersize=5, linewidth=1.5)
            i+=1

        i=0
        length = len(circuito)

        print(circuito)

        while i < length:
            circuito[i] = circuito[i]-1
            i+=1

        # Criação de rota retornada pela heuristica do menor caminho (cor VIOLETA-NEGRO)
        i=0
        while i < length-1:
            i+=1
            xd = []
            yd = []
            xpt, ypt = m(longi[circuito[i-1]], lat[circuito[i-1]])
            xd.append(xpt)
            yd.append(ypt)
            xpt, ypt = m(longi[circuito[i]], lat[circuito[i]])
            xd.append(xpt)
            yd.append(ypt)
            m.plot(xd, yd, 'o-', color ='darkviolet', markersize=15, linewidth=1.5)

        
        plt.title('Mapa De Conexão de Aeroportos')
        plt.show()

    elif checkButton == 9999999: # Botão para a questão 4 ( BOTÃO NÃO UTILIZADO - VALOR INCACESSIVEL )

        clear = lambda: os.system('cls')
        clear()

        print('\nBOTÃO 4 - ALTURA DE VOO - Pressionado\n')

    else: # Para a criação do mapa PADRÃO, após a inicialização do programa.

        # Limpar o terminal
        clear = lambda: os.system('cls')
        clear()

        # Marcar vértices em vermelho no mapa
        xpt, ypt = m(longi, lat)
        m.plot(xpt, ypt, 'o', color='r', markersize=5)

        # Criação do mapa, traçando aresta entre vértices de origem/destino na cor VERMELHO
        i=0
        while i<n:
            xs = []
            ys = []
            xpt, ypt = m(longiOrigem[i], latiOrigem[i])
            xs.append(xpt)
            ys.append(ypt)
            plt.annotate(origem[i], m(longiOrigem[i], latiOrigem[i]),fontsize = 15)
            plt.annotate(destino[i], m(longiDestino[i], latiDestino[i]),fontsize = 15)
            xpt, ypt = m(longiDestino[i], latiDestino[i])
            xs.append(xpt)
            ys.append(ypt)
            m.plot(xs, ys, 'o-', color ='r', markersize=5, linewidth=1.5)
            i+=1

        plt.title('Mapa De Conexão de Aeroportos')

        plt.show()