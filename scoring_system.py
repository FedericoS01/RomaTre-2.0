import numpy as np

def scoring_system(schedule, flows, M, N, T):
    """
    Calcola punteggio totale basato su 4 componenti pesati
    schedule: lista con scheduling per ogni flusso
    """
    FN = flows.shape[0]  # Usa numero reale di flussi
    flow_scores = np.zeros(FN)
    total_traffic = np.sum(flows[:, 4])  # Qtotal per tutti i flussi
    
    print(f'Debug: FN={FN}, size(flows)={flows.shape}, size(schedule)={len(schedule)}')
    
    for f in range(FN):
        if f >= len(schedule) or len(schedule[f]) == 0:
            flow_scores[f] = 0
            continue
        
        # Estrai dati flusso
        Qtotal = flows[f, 4]
        tstart = flows[f, 3]
        access_x = flows[f, 1]
        access_y = flows[f, 2]
        
        # 1. Total U2G Traffic Score (peso 0.4)
        u2g_traffic = np.sum(schedule[f][:, 3])  # Somma traffico U2G
        u2g_score = u2g_traffic / Qtotal
        
        # 2. Traffic Delay Score (peso 0.2)
        Tmax = 10
        delay_score = 0.0
        for i in range(len(schedule[f])):
            ti = schedule[f][i, 0] - tstart
            qi = schedule[f][i, 3]
            if ti >= 0:
                delay_score += (Tmax / (ti + Tmax)) * (qi / Qtotal)
        
        # 3. Transmission Distance Score (peso 0.3)
        a = 0.1
        distance_score = 0.0
        for i in range(len(schedule[f])):
            x = schedule[f][i, 1]
            y = schedule[f][i, 2]
            qi = schedule[f][i, 3]
            
            # Calcola distanza hop (Manhattan distance)
            di = abs(x - access_x) + abs(y - access_y)
            distance_score += (2**(-a * di)) * (qi / Qtotal)
        
        # 4. Landing UAV Point Score (peso 0.1)
        landing_points = np.unique(schedule[f][:, 1:3], axis=0)
        k = len(landing_points)
        landing_score = 1.0 / k
        
        # Calcola punteggio totale del flusso
        flow_scores[f] = 100 * (0.4 * u2g_score + 0.2 * delay_score + 
                               0.3 * distance_score + 0.1 * landing_score)
    
    # Calcola punteggio totale ponderato
    total_score = 0.0
    for f in range(FN):
        if f < flows.shape[0]:
            Qtotal_f = flows[f, 4]
            total_score += (Qtotal_f / total_traffic) * flow_scores[f]
    
    return total_score, flow_scores
