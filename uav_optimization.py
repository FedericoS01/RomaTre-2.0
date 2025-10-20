import numpy as np
from bandwidth_model import bandwidth_model

def uav_optimization(M, N, FN, T, uav_data, flows):
    """
    Algoritmo di ottimizzazione principale per scheduling traffico UAV
    Usa approccio greedy con euristica per efficienza computazionale
    """
    # Usa numero reale di flussi
    actual_FN = flows.shape[0]
    schedule = [[] for _ in range(actual_FN)]
    
    # Ordina flussi per priorità (traffico totale decrescente, tempo start crescente)
    sort_indices = np.lexsort((flows[:, 3], -flows[:, 4]))  # tstart crescente, Qtotal decrescente
    flow_order = flows[sort_indices, 0] - 1  # Converti a 0-based
    
    # Debug: verifica che flow_order sia valido
    if np.max(flow_order) >= actual_FN or np.min(flow_order) < 0:
        raise ValueError('Indici di ordinamento flussi non validi')
    
    # Inizializza matrice di larghezza di banda disponibile
    bandwidth_available = np.zeros((M, N, T))
    for t in range(T):
        for x in range(M):
            for y in range(N):
                bandwidth_available[x, y, t] = bandwidth_model(x, y, t, uav_data, M, N)
    
    # Processa ogni flusso nell'ordine di priorità
    for f_idx in range(actual_FN):
        f = flow_order[f_idx]
        
        # Verifica che l'indice sia valido
        if f < 0 or f >= actual_FN:
            continue
        
        # Estrai parametri flusso
        access_x = flows[f, 1] + 1  # Converti a 1-based indexing
        access_y = flows[f, 2] + 1
        tstart = flows[f, 3] + 1
        Qtotal = flows[f, 4]
        m1 = flows[f, 5] + 1
        n1 = flows[f, 6] + 1
        m2 = flows[f, 7] + 1
        n2 = flows[f, 8] + 1
        
        # Trova destinazioni valide
        valid_destinations = []
        for x in range(m1, m2 + 1):
            for y in range(n1, n2 + 1):
                if x <= M and y <= N:
                    valid_destinations.append([x, y])
        
        if len(valid_destinations) == 0:
            schedule[f] = []
            continue
        
        valid_destinations = np.array(valid_destinations)
        
        # Algoritmo greedy migliorato per scheduling
        remaining_traffic = Qtotal
        current_schedule = []
        current_time = tstart
        last_dest = None  # Traccia ultima destinazione per penalizzare cambi
        
        while remaining_traffic > 0 and current_time <= T:
            # Trova migliore destinazione per questo time slot
            best_dest = None
            best_score = -np.inf
            
            for dest_idx in range(len(valid_destinations)):
                dest_x = valid_destinations[dest_idx, 0]
                dest_y = valid_destinations[dest_idx, 1]
                
                # Calcola rate massimo possibile
                available_bw = bandwidth_available[dest_x-1, dest_y-1, current_time-1]
                max_rate = min(remaining_traffic, available_bw)
                
                if max_rate <= 0:
                    continue
                
                # Calcola score euristico migliorato
                distance = abs(dest_x - access_x) + abs(dest_y - access_y)
                
                # Bonus per stabilità (stessa destinazione del time slot precedente)
                stability_bonus = 1.0
                if last_dest is not None and dest_x == last_dest[0] and dest_y == last_dest[1]:
                    stability_bonus = 1.2  # 20% bonus per stabilità
                
                # Bonus per destinazioni centrali nella regione
                region_center_x = (m1 + m2) / 2
                region_center_y = (n1 + n2) / 2
                center_distance = abs(dest_x - region_center_x) + abs(dest_y - region_center_y)
                center_bonus = 1.0 / (1 + 0.05 * center_distance)
                
                # Score combinato
                heuristic_score = max_rate * stability_bonus * center_bonus / (1 + 0.1 * distance)
                
                if heuristic_score > best_score:
                    best_score = heuristic_score
                    best_dest = [dest_x, dest_y]
            
            if best_dest is not None and best_score > -np.inf:
                dest_x = best_dest[0]
                dest_y = best_dest[1]
                available_bw = bandwidth_available[dest_x-1, dest_y-1, current_time-1]
                allocated_rate = min(remaining_traffic, available_bw)
                
                if allocated_rate > 0:
                    current_schedule.append([current_time-1, dest_x-1, dest_y-1, allocated_rate])
                    
                    # Aggiorna traffico rimanente e larghezza di banda
                    remaining_traffic -= allocated_rate
                    bandwidth_available[dest_x-1, dest_y-1, current_time-1] -= allocated_rate
                    
                    # Aggiorna ultima destinazione
                    last_dest = [dest_x, dest_y]
            
            current_time += 1
        
        schedule[f] = np.array(current_schedule) if current_schedule else np.array([]).reshape(0, 4)
    
    # Calcola punteggio totale
    from scoring_system import scoring_system
    total_score, _ = scoring_system(schedule, flows, M, N, T)
    
    return schedule, total_score
