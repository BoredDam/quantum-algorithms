# **Progetto di Quantum Computer Programming - Quantum Longest Common Substring**


Con il seguente progetto, si affronta una soluzione ibrida classico-quantistica per la risoluzione del problema **Longest Common Substring**.

Basato sull'articolo:
> Cantone, Domenico & Faro, Simone & Pavone, Arianna & Viola, Caterina. (2023). Longest Common Substring and Longest Palindromic Substring in $\tilde{\mathcal{O}}(\sqrt{n})$ Time. 10.48550/arXiv.2309.01250.

## **In breve**

Utilizzare l'algoritmo di Grover per verificare la presenza di LCS tra due stringhe $X$ e $Y$ in tempo $\mathcal{O}(\sqrt{N})$. 
In particolar modo, verificare la presenza di una LCS di lunghezza $d$ a ogni passaggio, e usare un approccio di ricerca binaria per minimizzare i test da effettuare, ottenendo così una complessità $\tilde{\mathcal{O}}(\sqrt{n})$.