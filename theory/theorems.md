# Alcuni teoremi

## **Teorema di non clonazione**

Non esiste operatore unitario $U$ tale che

$$
U|\psi\rangle| 0\rangle = |\psi\rangle| \psi\rangle 
$$

### Dimostrazione

La dimostrazione si basa sul tentativo di clonare una combinazione lineare di stati: questo darà un esito differente da quello atteso applicando o meno la proprietà di lineareità degli operatori quantistici. Ne consegue che non è possibile creare un operatore quantistico del genere, in quanto la lineareità è condizione necessaria per ciascun operatore $U$.

## **Teorema di non cancellazione**

Non esiste operatore unitario $U$ tale che

$$
U|\psi\rangle|\psi\rangle =|\psi\rangle| 0 \rangle
$$

### Dimostrazione

La dimostrazione avviene per assurdo, osservando che il prodotto scalare deve essere preservato. Quindi

$$
\langle\phi\phi|\psi\psi\rangle = \langle\phi0|\psi0\rangle
$$

Scomponendo i prodotti scalari, concludiamo che

$$
\langle\phi|\psi\rangle = (\langle\phi|\psi\rangle)^2
$$

E ciò è un assurdo.


## **Teorema di no-hiding**

L'informazione quantistica di un sottosistema, dal quale viene eliminata questa informazione, si deve disperdere nel resto del sistema, a meno di una trasformazione unitaria.


```c
      init           ┌───┐ ░ ┌─┐
  A: ──░─────■───────┤ X ├─░─┤M├
       ░   ┌─┴─┐┌───┐└─┬─┘ ░ └╥┘
  B: ──░───┤ X ├┤ H ├──■───░──╫─
       ░   └───┘└───┘      ░  ║ 
c: 1/═════════════════════════╩═
                              0 
```

L'informazione quantistica di `A` è codificata esattamente in `B`, a meno di una trasformazione unitaria. È il principio alla base di Quantum Teleportation, Superdense Coding, e di Entanglement Swap.