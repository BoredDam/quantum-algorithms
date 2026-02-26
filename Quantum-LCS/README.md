# **Progetto di Quantum Computer Programming - Quantum Longest Common Substring**

Con il seguente progetto, si affronta una soluzione ibrida classico-quantistica per la risoluzione del problema  [**Longest Common Substring**]((https://www.geeksforgeeks.org/dsa/longest-common-substring-dp-29/)).

Basato sul paper:
> Cantone, Domenico & Faro, Simone & Pavone, Arianna & Viola, Caterina. (2023). Longest Common Substring and Longest Palindromic Substring in $\tilde{\mathcal{O}}(\sqrt{n})$ Time. 10.48550/arXiv.2309.01250.

## **In breve**

Si effettua una ricerca binaria (classica) sul valore massimo di $d$ per cui, nelle stringhe d'input $X$ e $Y$, esiste una sottostringa comune di dimensione $d$.

La verifica della presenza della sottostringa in questione, avviene tramite l'algoritmo (quantistico) di Grover. A tal fine, vengono implementati degli opportuni oracoli per il problema. La parte quantistica dell'algoritmo è contenuta all'interno di una funzione chiamata $\text{QUANTUM-TEST}$.
