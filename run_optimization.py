#!/usr/bin/env python3
"""
Funzione per eseguire ottimizzazione con file personalizzati
"""

import time
from input_parser import input_parser
from uav_optimization import uav_optimization
from output_generator import output_generator
from visualization import visualization
from validation import validation

def run_optimization(input_file='input.txt', output_file='output.txt'):
    """
    Funzione per eseguire ottimizzazione con file personalizzati
    """
    try:
        # Leggi input
        print(f'Leggendo file di input: {input_file}')
        M, N, FN, T, uav_data, flows = input_parser(input_file)
        
        print(f'Parametri rete: {M}x{N}, {FN} flussi, {T} secondi')
        
        # Esegui ottimizzazione
        print('Eseguendo ottimizzazione...')
        start_time = time.time()
        schedule, total_score = uav_optimization(M, N, FN, T, uav_data, flows)
        elapsed_time = time.time() - start_time
        
        print(f'Ottimizzazione completata in {elapsed_time:.3f} secondi')
        print(f'Punteggio totale: {total_score:.3f}')
        
        # Genera output
        print(f'Generando file di output: {output_file}')
        output_generator(schedule, flows, output_file)
        
        # Visualizzazione
        print('Generando visualizzazione...')
        visualization(schedule, flows, total_score)
        
        # Validazione estesa
        validation(schedule, flows, uav_data, M, N, T)
        
        print('Processo completato con successo!')
        
    except Exception as e:
        print(f'Errore durante l\'esecuzione: {str(e)}')
        raise

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        run_optimization(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        run_optimization(sys.argv[1])
    else:
        run_optimization()
