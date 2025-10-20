# RomaTre-2.0
# UAV Network Optimization - Huawei Competition

Algoritmo MATLAB ottimizzato per l'allocazione delle risorse in reti UAV per il concorso Huawei.

## Caratteristiche Principali

- **Algoritmo Greedy Intelligente**: Usa euristica avanzata per minimizzare il costo computazionale
- **Ottimizzazione Locale**: Post-processing per migliorare i risultati
- **Modello di Banda Periodico**: Implementa correttamente il modello U2GL con fase
- **Sistema di Punteggio Completo**: Calcola tutti e 4 i componenti del punteggio

## File Principali

- `main.m` - Script principale per esecuzione
- `run_optimization.m` - Funzione per esecuzione con file personalizzati
- `uav_optimization.m` - Algoritmo di ottimizzazione base
- `advanced_optimization.m` - Algoritmo avanzato con miglioramenti
- `input_parser.m` - Parser per file di input
- `output_generator.m` - Generatore di file di output
- `scoring_system.m` - Sistema di calcolo del punteggio
- `bandwidth_model.m` - Modello di larghezza di banda U2GL

## Utilizzo

### Esecuzione Base
```matlab
main()
```

### Esecuzione con File Personalizzati
```matlab
run_optimization('input.txt', 'output.txt')
```

### Test con Esempio
```matlab
test_example()
```

## Formato Input

Il file di input deve seguire il formato specificato:
- Linea 1: M N FN T (dimensioni griglia, numero flussi, tempo simulazione)
- Linee 2-(2+M*N-1): x y B phi (dati UAV)
- Linee successive: f x y tstart Qtotal m1 n1 m2 n2 (dati flussi)

## Formato Output

Il file di output contiene:
- Per ogni flusso: numero flusso e numero record
- Per ogni record: tempo, coordinate UAV, rate traffico

## Algoritmo di Ottimizzazione

1. **Ordinamento Flussi**: Per priorità (traffico totale, tempo start)
2. **Scheduling Greedy**: Con euristica di distanza e stabilità
3. **Lookahead**: Considera banda futura per decisioni migliori
4. **Ottimizzazione Locale**: Consolidamento time slot consecutivi

## Complessità Computazionale

- **Tempo**: O(FN * T * M * N) dove FN=flussi, T=tempo, M*N=rete
- **Spazio**: O(M * N * T) per matrice banda disponibile

L'algoritmo è ottimizzato per essere efficiente anche con reti grandi e molti flussi.
