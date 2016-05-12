=======================
Semplice esempio di GUI
=======================

:Author: Luca Manini
:Date:   dicembre 2005

Introduzione
============

Questa directory contiene un semplice esempio di programma Python con
interfaccia a linea di comando (cli) e grafica (gui, in gtk).  Il
programma dovrebbe essere una implementazione del gioco "five in a
row" (chiamato "lines" nel package Debian gnome-games).

Il fatto di essere un gioco dovrebbe rendere più interessante il
lavoraccio di scrivere la gui.

La gui viene generata tutta da codice, sia perché si spera sia
sufficientemente semplice da rendere la cosa fattibile, sia perché
l'interfaccia assolutamente logorroica di (py)gtk è un ottimo problema
per illustrare la comodità di Python nel "wrappare" delle API che non
ci piacciono in qualcosa di più programmer-friendly.

Struttura
=========

Comandi: i due programmi eseguibili sono cli-gui.py e gui-gui.py.  Il
nome con il segno meno è una mia convenzione, che evita anche la
possibilità di importare il file come modulo (spero non sia un
problema per altri strumenti). Entrambi non fanno altro che creare una
istanza di Boss e una della gui chiamando la funzione get_gui_for_boss
dei moduli opportuni (cli.py e gui.py).

Boss: una classe che fornisce una interfaccia uniforme per le GUI, in
pratica wrappa Game e Board.

Game: sa "come si gioca".

Board: mantiene i dati della scacchiera.

Grouper: sa trovare i "gruppi" (da eliminare).

Walker: sa trovare i percorsi liberi.

Protocollo testuale
===================

Un protocollo solo testo (come HTTP, SMTP e simili) per l'interfaccia
di Boss.  Il protocollo è client-pushed (à la HTTP), il client manda
dei comandi o delle query e legge delle risposte, che si sono sempre e
posso contenere una semplice conferma, altri dati o un errore.  

I messagggi sono "per riga", ogni riga inizia con una stringa che
identifica il comando/risposta.  La lunghezza (in token) dei messaggi
è sempre nota in quanto o è fissa o è esplicitata in un parametro
della risposta.  L'idea è che i messaggi devono essere facilmente
leggibili anche dagli umani.

Nota: almeno in questa implementazione iniziale non vengono usati
codici numerici (escluso il caso degli errori) e i messaggi non
contengono un "sequence number" (come invece fa IMAP).

Nota: non ho ancora deciso se usare dei prefissi (es: < e >) per
distinguere client e server; la distinzione è ovviamente inutile per
il protocollo, ma utile per gli umani.  In ogni caso il parsing verrà
fatto con reg-exp che potrebbero saltare tutta la parte iniziale non
[A-Z].

Protocollo
----------

Di seguito descrivo tutti i messaggi, mostrando il messaggio mandato
dal client e le possibili risposte del server.  I messaggi si possono
dividere prima di tutto in comandi e query e poi in indispensabili e
"di comodo" (principalmente query di info).  Nota: è possibile giocare
utilizzando solo i comandi indispensabili.

Nel seguito, indicherò con RC una coppia di interi che individua una
riga e una colonna (es: 3 7), con RCV al tripla che include anche un
valore (colore) della cella (es: 3 7 4), con N l'intero che indica
quanti "elementi" seguono e con RC(N) oppure RCV(N) gli elementi
stessi.  

I messaggi di errore sono tutti della forma::

  ERROR CODE DESCRIPTION

quindi non vengono esplicitati qui ma elencati alla fine.

I messaggi **indispensabili** sono quindi:

1) Nuova partita

  Il client manda un messaggio che include le dimensioni richieste per
  la scacchiera, o 0 0 per indicare "usa il default"::

    NEW RC(1)

  Se tutto va bene, il server risponde con due righe::

    NEW   RC(1)
    ADDED N RCV(N)
    NEXT  N V(N)

  che indicano le dimensioni attuali del gioco, le pedine inserite
  (posizione e valore) e i valori delle prossime.

2) mossa del client::

     MOVE RC(2)

   se la mossa **del client completa** dei gruppi, il server le
   posizioni delle pedine rimosse (non credo che il valore interessi),
   il punteggio realizzato (P) e quello totale (T), notare che le
   "prossime" sono quelle di prima quindi non serve includerle nella
   risposta::

     REMOVED N RC(N)
     SCORE   P T

   se la mossa **del client NON completa** dei gruppi, allora il
   server aggiunge delle pedine, la cui lista viene restituita::

     ADDED N RCV(N)

   se poi **questa aggiunta completa** dei gruppi, ciò viene
   segnalato::

     REMOVED N RC(N)
     SCORE   P T

   In ogni caso, il tutto finisce con la lista delle "prossime"::

     NEXT  N V(N)

3) il gioco finisce normalmente quando una mossa del server riempie la
   scacchiera (il client non aggiunge mai nulla) ed è indicata dal
   fatto che non ci sono "prossime" pedine (notare che con le
   "costanti" solite, il gioco non finisce mai "subito dopo" una
   remove, perché questa tolgie sempre almeno cinque pedine e la add
   ne agguinge tre, il protocollo potrebbe però prevedre tutti i
   casi)::

     ADDED N RCV(N)
     NEXT  0

   oppure il client può arrendersi::

     QUIT

I messaggi **opzionali** sono comprendono le richieste della
dimensione della scacchiera, delle posizioni e valori delle pedine
sulla scacchiera, sui valori delle prossime pedine, sul punteggio,
sulla possibilità di fare un dato spostamento e sul percorso tra due
celle (per eventuali "animazioni" dello spostamento)::

   SIZE  -> SIZE  RC(1)
   BOARD -> BOARD N RCV(N)
   NEXT  -> NEXT  N V(N)
   SCORE -> SCORE 0 T  o forse SCORE L T
   CANMOVE RC(2) -> CANMOVE YES/NO
   PATH RC(2) -> PATH N RC(N)

Nota: sul formato di SCORE ho dei dubbi, lo vorrei simile a quello
standard", ma il contesto è diverso e mancano i punti appena fatti...

I messaggi opzionali permettono al client di non mantenere nessuno
"stato", e di richiedere tutto ogni volta.

La lista degli errori può essere abbastanza libera in quanto il
"significato" è noto al client dal contesto, e comunque c'è la
descrizione (e il codice per eventuale traduzione), una lista
possibile::

  NO GAME	(non è stato cominciato nessun gioco)
  GAME OVER	(partita finita)
  NOPATH	(da MOVE: nessun path possibile, ossai CANMOVE NO)
  BADMOVE	(da MOVE: from è vuota e/o to è piena)