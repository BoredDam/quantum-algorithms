# L'algoritmo di Shor

Rappresenta una delle applicazioni pratiche più importanti del quantum computing. Dimostra la superiorità quantistica in determinati task computazionali. Permette di fattorizzare numeri in fattori primi, in tempo esponenzialmente più veloce del miglior algoritmo classico. La crittografia RSA è basata proprio sul prodotto tra numeri primi di grande dimensione.

L'algoritmo di Shor può essere generalizzato per il problema del logaritmo discreto e il problema della ricerca del periodo.

## Crittografia

La crittografia RSA si basa sulla difficoltà di trovare i due numeri primi $p$ e $q$ che danno come prodotto il numero $n$: è molto semplice da verificare, in quanto $p \times q$ è un'operazione banale da effettuare, ma il contrario no!

Le chiavi più comuni hanno 2048 bit. 

## Sui numeri primi

Teorema fondamentale dell'aritmetica: ogni numero o è primo, o è il prodotto di due o più numeri primi.

Prodotti di due numeri primi molto grandi sono molto difficili da risolvere. 
```
        1163347
       /       \
     911       1277
```

## La fattorizzazione
Fattorizzare un numero $N$ coincide con la scelta di un numero intermo $m$ che è coprimo con $N$, e trovare lordine moltiplicativo di ordine $P$

$$
m^P \equiv 1 \mod N
$$


## Algoritmo di Shor

1. Trasformare il problema di fattorizzazione in un problema di ricerca del periodo
2. Usa la QFT per trovare il periodo
3. Utilizza il periodo scoperto per computare il fattore del numero originale.

Essendo ancora nell'era dei qubit ancora soggetti a decoerenza ed errori, l'algoritmo è difficile da usare sull'hardware attuale.

## Quantum Fourier Transform

È l'equivalente quantistico della trasformata di Fourier Discreta.

### DFT

Invece di esprimere il segnale come una funzione nel tempo, è una sommatoria di sinusoidi complesse. Ha complessità $O(n^4)$

### QFT

Ha una complesistà di $O(\log^4n)$, sfrutta la sovrapposizione quantistica per parallelizzare la trasformata.

## Quantum Phase Estimation

Rappresenta una classe di problemi più vasta nel mondo del quantum computing

## Esempio

N = 15
b = 2

La sequenza $2^x \mod 15$ produce 2,4,8,1,2,4,8,1... una funzione con periodo $r=4$.

$$
2^{\frac{4}{2}} - 1 = 3
\\

2^{\frac{4}{2}} - 1 = 3
$$