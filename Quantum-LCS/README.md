# **Progetto di Quantum Computer Programming - Quantum Longest Common Substring**


Con il seguente elaborato, si affronta una soluzione ibrida classico-quantistica per la risoluzione del problema **Longest Common Substring**.

> Cantone, Domenico & Faro, Simone & Pavone, Arianna & Viola, Caterina. (2023). Longest Common Substring and Longest Palindromic Substring in $\tilde{\mathcal{O}}(\sqrt{n})$ Time. 10.48550/arXiv.2309.01250. 

## **Problema Longest Common Substring**

Il problema Longest Common Substring è un **problema di ottimizzazione** definito nel seguente modo:

> Date due stringhe $X = \{x_1, x_2, \dots, x_n\}$ e $Y = \{y_1, y_2, \dots, y_m\}$, trovare $S = \{s_1, s_2, \dots, s_k\}$ tale che $S$ sia sottostringa sia di $X$ che di $Y$, e massimizzando la lunghezza $k$. 

È un problema tipico del text processing, cui soluzioni trovano applicazioni nell'ambito della deduplicazione dei dati, negli algoritmi anti-plagio e nella bioinformatica (assieme al Longest Common Subsequence).

## **Quantum-LCS Algorithm**

L'algoritmo che si propone, è una soluzione ibrida classico-quantistica, che si compone di un algoritmo iterativo classico, e uno step di verifica quantistico.

```
QUANTUM-LCS(x,y,n):                    
    l = 0;                             
    r = n;                             
    while l < r do                     
        d = floor((l+r)/2)             
        if QUANTUM-TEST(x, y, d) then  
            l = d                      
        else                           
            r = d - 1                  
                                       
    return l                           
```

## **Algoritmo classico**

Tratteremo temporaneamente $\text{QUANTUM-TEST}(X, Y, d)$ come una black-box, ignorandone il funzionamento, ma solo il comportamento. Questa funzione ritorna `True` se e solo se 
$$\exists S \text{ sottostringa di } X \text{ e } Y \text{ di dimensione } d$$


Noto questo, l'algoritmo $\text{QUANTUM-LCS}(X,Y,n)$ si basa su una ricerca binaria del valore di $k$, verificando ad ogni step usando $\text{QUANTUM-TEST}(X,Y,d)$ come verifica. In altre parole:


> 1. Pongo $l = 0$ ed $r = n$. Questi coincidono col più ampio range di valori che la dimensione della LCS può assumere, ossia $0 \leq |S| \leq n$.
> 2. Stimo che la LCS tra $X$ e $Y$ sia di dimensione $d = \lfloor (l + r)/2\rfloor$.
> 3. Se esiste una sottostringa comune a $X$ e a $Y$ di dimensione $d$, pongo $l = d$, altrimenti pongo $r = d - 1$.
> 4. Se $l = r$, $l$ è la lunghezza della LCS ad $X$ e $Y$, altrimenti torno allo step $2$. 

Noto questo, è banale dire che la complessità della funzione, sarà:

$$
\mathcal{O}(\log n) \cdot (\text{Complessità di QUANTUM-TEST})
$$
## **Test quantistico**

Affrontiamo adesso l'analisi della componente quantistica dell'algoritmo. Abbiamo già detto che vogliamo che $\text{QUANTUM-TEST}(X,Y,d)$ torni `True` se e solo se esiste una sottostringa di dimensione $d$ condivisa tra $X$ e $Y$.

### **Prerequisiti di computazione quantistica**

Riassumiamo i prerequisiti di computazione quantistica (non triviali) richiesti per la comprensione della funzione $\text{QUANTUM-TEST}(X,Y,d)$.

- [Oracoli booleani](../q-miscellaneous/q-oracles/boolean-oracles.ipynb) - gate che implementano funzioni del tipo $f: \{0,1\}^n \to \{0,1\}$;
- [Phase kickback](../q-miscellaneous/q-oracles/phase-kickback.ipynb) - conseguenza dell'applicazione di operazioni controllate su qubit in sovrapposizione;
- [Oracoli di fase](../q-miscellaneous/q-oracles/phase-oracles.ipynb) - i quali uniscono le intuizioni degli oracoli booleani col phase kickback;
- Operatore di rotazione arbitraria;
- [Algoritmo di Grover](../Grover-algorithm/grover.ipynb) - per amplificare la probabilità di ottenere stati che soddisfano le condizioni di un oracolo di fase.

### **Idea dietro il test quantistico**

Come tutti i problemi risolti tramite l'algoritmo di Grover, vogliamo costruire degli oracoli di fase $P_f$ per invertire la fase delle soluzioni che cerchiamo. Lo step di diffusione, farà invece da ponte tra la verifica di una soluzione e la sua costruzione effettiva.

Ricordiamo che col nostro $\text{QUANTUM-TEST}$ vogliamo porre la seguente domanda:

$$
\text{Esiste una sottostringa di dimensione $d$ comune a $X$ e $Y$?}
$$

Introduciamo quindi gli oracoli necessari per il test.

- $\text{SFC}$: Shared Fix Substring Check
- $\text{FPM}$: Fixed Prefix Matching

costruiti entrambi come variazioni dell'operatore $\text{Fixed Substring Matching}$, o $\text{FSM}$, nel quale è possibile specificare la posizione di partenza della sottostringa (tramite $|D[-1]\rangle$), e la sua dimensione (tramite $|d\rangle$).

## **Operatore FSM**

L'operatore Fixed Substring Matching implementa la seguente $f$:

$$
\begin{array}{l}
\text{FSM}(d, x, y, D^{-1}): \\
1.\quad \lambda^{0} \leftarrow M(x,y) \\
2.\quad \text{if } \bar{d}[0] = 1 \text{ then } D^{0} \leftarrow (D^{-1} \land \lambda^{0}) \gg 2^{0} \\
3.\quad \text{for } i \leftarrow 1 \text{ to } \log(d) \text{ do} \\
4.\qquad \lambda^{i} \leftarrow \mathrm{EXT}_{i}(\lambda^{i-1}) \\
5.\qquad\quad \text{if } \bar{d}[i] = 1 \text{ then } D^{i} \leftarrow (D^{i-1} \land \lambda^{i}) \gg 2^{i} \\
6.\qquad\quad \text{else } D^{i} \leftarrow (D^{i-1} \land \lambda^{i}) \\
7.\quad r \leftarrow \displaystyle \bigvee_{j=d}^{n+d} D^{\log(d)}[j] \\
8.\quad \text{return } r
\end{array}
$$


In cui 
- Ogni vettore $\lambda$ è detto di *matching substring*, ed è definito ricorsivamente come

$$
\lambda^{i}[j] = \lambda^{i-1}[j] \land \lambda^{i-1}[j + 2^{i-1}] \qquad 
\lambda^{0}[j] = (x_j \land y_j) \lor (\neg x_j \land \neg y_j)
$$

- Ogni vettore $D$ è definito ricorsivamente (a meno di $D^{-1}$, stabilito in funzione del problema di string matching) come

$$
D^i = (D^{i-1} \land \lambda^{i-1}) >> 2^i \text{ se } \overline{d}[i]=1 \qquad \text{altrimenti} \quad D^i = D^{i-1}
$$


1. Costruisco il vettore di *matching substring* $\lambda^0$ contenendo le posizioni in cui i caratteri di $X,Y$ coincidono.
2. Costruisco il vettore $D^0$. In generale, se $D^i[j+\overline{d}[0:i]] = 1$, sappiamo che in quella posizione c'è una sottostringa di lunghezza $d$ comune a $X$ e $Y$.
3. Costruisco, per $i = 0, 1, \dots, \log n$ i vari vettori $\lambda^i$ e $D^i$.
4. Ritorno l' $\text{OR}$ logico tra tutte le linee di $D^{\log(d)}$ (l'ultimo vettore).

In particolare, l'inizializzazione di $D^{-1}$ dipende esclusivamente dal tipo di problema che si sta affrontando ($\text{SFC},\text{FPM}$).
