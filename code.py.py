import itertools
from queue import Queue
#fromtwodivisible
#koristi se Breadth First Search

rj={}


def UnosKorisnika():
    N=int(input("Unesi broj gradova: ")) #korisnik unosi broj gradova npr. 11
    Source=int(input("Unesi grad iz kojeg se polazi: ")) #korisnik unosi grad iz kojeg se polazi(broj, npr. 9)
    Target=int(input("Unesi grad u koji se dolazi: ")) #unosi se grad u kjoji se dolazi npr.6
    M=int(input("Unesi broj elemenata: ")) #broj elemanata u nizu s kojim se grad bit djeljiv 
    a=[] #prvi niz
    b=[] #drugi niz
    brojac=0
    while(brojac<M): #M je broj elemenata u nizu i ako imamo npr. 2 elementa u svaki niz ce se unosit 2 elementa
        element_a=int(input("Unesi element: "))
        element_b=int(input("Unesi element: "))
        a.append(element_a)
        b.append(element_b)
        brojac=brojac+1 #broji se koliko je elemenata uneseno(brojac) i ako je jednak M onda se ne unosi vise
    
    return N, Source,Target,M, a,b

def PronadiSveCeste(N, M, a, b): #prima se broj gradova, broj elemenata i dva nzia
    kombinacije_cesta1=[]
    d=len(a)
    k=list(zip(a,b)) # npr. a=[5,3], b=[10,2] -->k=[(5,10),(3,2)]
    for x in range(0,M): #od 0 do M
        for y in range(0,2): #od 0 do 2
            for z in range(1,N): #od 1 do br gradova(11)
                if(z%k[x][y]==0): #ako je z(npr. 2) , k[x][y] , x=0, y=0 -> 5 , 2%5 nije 0, ne dodaje se u niz
                    kombinacije_cesta1.append(z)
       
            kombinacije_cesta1.append("-") #crtica je dodana kad su nadeni svi brojevi s kojima je djeljiv svaki broj
 
    
    return kombinacije_cesta1 #[3, 6, 9, '-', 5, 10, '-', 10, '-', 2, 4, 6, 8, 10, '-']
    
def NapraviKombinaciju(kombinacije_cesta): #[3, 6, 9, '-', 5, 10, '-', 10, '-', 2, 4, 6, 8, 10, '-']
    #print(kombinacije_cesta)
    brojac=0
    niz1=[]
    niz2=[]
    cesta1=[]
    brojac=0
    for x in kombinacije_cesta:
        if(brojac==2): #broje se crtice, ako su dvi,  uzmi ta dva niza u kojima su brojevi i napravi njihove kombinacije
            cesta1.append(list(itertools.product(niz1,niz2))) #npr. ispisuje sve kombinacije od brojeva od ta dva niza[[(3, 5), (3, 10), (6, 5), (6, 10), (9, 5), (9, 10)]]
            niz1.clear() #isprazni niz 
            niz2.clear()
            brojac=0 #resetiraj brojac da se gleda za druge nizove
            
        if(x!='-' and brojac==0):
            niz1.append(x) #dodaj u niz1 (sve prije prve crtice) npr. 3 6 9 
        if(brojac==1 and x!='-'):
            niz2.append(x) #brojac=1, prodena je prva crtica, dodaje se u niz2 ->5 10
        elif(x=='-'):
            brojac=brojac+1
    
    cesta1.append(list(itertools.product(niz1,niz2)))
    return cesta1

def Remove(road): #[[(3, 5), (3, 10), (6, 5), (6, 10), (9, 5), (9, 10)], [(10, 2), (10, 4), (10, 6), (10, 8), (10, 10)]]
     # 2 liste u isti 
    all_roads=[]
    for y in road: #prva iteracija y=[(3, 5), (3, 10), (6, 5), (6, 10), (9, 5), (9, 10)] (prva lista u listi)
        for x in y:
            all_roads.append(x)
    
    return all_roads #[(3, 5), (3, 10), (6, 5), (6, 10), (9, 5), (9, 10), (10, 2), (10, 4), (10, 6), (10, 8), (10, 10)]

def Shortest_path(all_roads):
    #print(all_roads)
    for x in all_roads: #npr. (3,5)
        if(x[0] not in rj.keys()): #ukoliko 3 nije kljuc, dodaj ga,a ukoliko je, dodaj grad u koji 3 dolazi kao vaule
            rj[x[0]]=[]
        rj[x[0]].append(x[1])
    
    return rj #{3: [5, 10], 6: [5, 10], 9: [5, 10], 10: [2, 4, 6, 8, 10]}

def DoesExist(Target,rj):
    values=rj.values() #vrijednosti u rjecniku
    target=Target
    for v in values: #ovo sluzi za provjeru postoji li target kao value
        for x in v: #ako target ne postoji kao odredisni grad nekog polazisnog grada , onda nema ni ceste, vratit ce false
            if(target == x):
                vrijednost=True
                break
    return vrijednost
    

def FindShortestPath(Source,Target,rj):
    visited={} #koji su posjeceni
    level={} #udaljenosti
    parent={} #tko je kome prethodnik
    queue=Queue()
    for x in rj.keys(): #postavi da nitko nije posjecen, da je udaljenost -1 i da nemaju prethodnika
        visited[x]=False
        parent[x]=None
        level[x]=-1

    source=Source
    visited[source]=True #polazisni grad je posjecen -> True
    level[source]=0 #udaljenost od polazinog grada je stavljena na 0
    queue.put(source)
    while not queue.empty(): #sve dok se ne isprazni queue
        u=queue.get() #pop first element of que
        if(not rj): #ukoliko je rjecnik prazan (moze biti ako su brojevi premali ili nema nijedan djeljiv)
            break

        d1=len(rj[u]) #koliko je duga lista od odredenog keya
        brojielemente=0
        for v in rj[u]: #npr. u=9, 9:[5,10], znaci v je u prvoj iteraciji 5
            if(v in rj.keys()): #ako postoji u rjecniku kao key, onda postoji mogucnost da dode u odrediste, a ukoliko ne postoji ide se dalje kroz listu
                if not visited[v]: #ukoliko postoji kao key i nije posjecen
                    visited[v]=True #stavi da je posjecen
                    parent[v]=u #prethodnik mu je grad koji dolazi u njega (npr. 9->5, parent od 5 je 9)
                    level[v]=level[v]+1 #udaljenost
                    queue.put(v) #postavi u queue, vraca se na pocetak while i skinut ce se key koji se provjeravao

            else:
              brojielemente=brojielemente+1#ako je d1=brojielemente, proslo se kroz sve vrijednosti od keya, nijedna vrijednost nije kao key i znaci da nema puta (ukoliko vrijednost pocetnog keya vec nije target) 
              continue
   
    if(rj): #ako rjecnik postoji
        target=Target
        path=[]
        if(DoesExist(target,rj) and brojielemente!=d1): #ako su isti d1 i brojielemente znaci da se proslo kroz listu keya i nijedan od brojeva u listi ne postoji kao key i nema puta
            while (target is not None): #ako je none znaci da ga nema u rjecniku , pa nema puta
                path.append(target) #stavlja se prvo target, pa ko je isao u target,
                target=parent[target] #pa ko je isao u target, formira se put
            path.reverse() # 6 10 9 , obrnuto 9 10 6
            d=len(path) #duljina staze
            if(d !=0):
                print("Najkraci put je "+str(path)  +", a duljina je: " +str(d-1)) #d-1 ,u pathu su 3 broja, ali je duljina 2 , npr 9->10 10->6, dvi ceste
        
        
        else:
            print(-1) # =>ako ne postoji kao target
        
    else:
        print(-1) #ako je rjecnik prazan =>-1


    
N, Source, Target,M, a, b=UnosKorisnika()
kombinacije_cesta=PronadiSveCeste(N,M, a, b)
road=NapraviKombinaciju(kombinacije_cesta) #[[(3, 5), (3, 10), (6, 5), (6, 10), (9, 5), (9, 10)], [(10, 2), (10, 4), (10, 6), (10, 8), (10, 10)]]
all_roads=Remove(road)
rj=Shortest_path(all_roads) #{3: [5, 10], 6: [5, 10], 9: [5, 10], 10: [2, 4, 6, 8, 10]}
FindShortestPath(Source,Target,rj)










