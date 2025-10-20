def output_generator(schedule, flows, filename):
    """
    Genera file di output secondo le specifiche del concorso
    """
    try:
        with open(filename, 'w') as fid:
            FN = flows.shape[0]  # Usa numero reale di flussi
            
            for f in range(FN):
                if f >= len(schedule) or len(schedule[f]) == 0:
                    # Flusso senza scheduling
                    fid.write(f'{f+1} 0\n')
                else:
                    # Numero di record di scheduling
                    p = len(schedule[f])
                    fid.write(f'{f+1} {p}\n')
                    
                    # Record di scheduling
                    for i in range(p):
                        t = int(schedule[f][i, 0])
                        x = int(schedule[f][i, 1])
                        y = int(schedule[f][i, 2])
                        z = schedule[f][i, 3]
                        fid.write(f'{t} {x} {y} {z:.6f}\n')
                        
    except Exception as e:
        raise Exception(f'Impossibile creare il file di output: {str(e)}')
