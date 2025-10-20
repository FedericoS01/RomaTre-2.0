import numpy as np

def bandwidth_model(x, y, t, uav_data, M, N):
    """
    Calcola larghezza di banda U2GL per UAV (x,y) al tempo t
    Implementa il modello periodico con fase phi
    """
    # Trova indice UAV nella griglia
    uav_indices = np.where((uav_data[:, 0] == x) & (uav_data[:, 1] == y))[0]
    if len(uav_indices) == 0:
        return 0.0
    
    uav_idx = uav_indices[0]
    B = uav_data[uav_idx, 2]  # Peak bandwidth
    phi = int(uav_data[uav_idx, 3])  # Phase
    
    # Calcola tempo relativo con fase
    t_rel = (phi + t) % 10
    
    # Applica modello periodico
    if t_rel in [0, 1, 8, 9]:
        return 0.0
    elif t_rel in [2, 7]:
        return B / 2.0
    else:  # t_rel da 3 a 6
        return B
