import matplotlib.pyplot as plt
import numpy as np

def visualization(schedule, flows, total_score):
    """
    Visualizzazione semplice e efficace per concorso
    Solo le informazioni essenziali
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Soluzione UAV - Concorso Huawei - Punteggio: {total_score:.3f}', fontsize=14)
    
    # Plot 1: Topologia semplice
    ax1.set_title('Flussi e Regioni Destinazione')
    ax1.grid(True)
    
    # Griglia UAV
    for f in range(flows.shape[0]):
        start_x = flows[f, 1]
        start_y = flows[f, 2]
        m1 = flows[f, 5]
        n1 = flows[f, 6]
        m2 = flows[f, 7]
        n2 = flows[f, 8]
        
        # Punto di partenza
        ax1.plot(start_x, start_y, 'ro', markersize=10, markerfacecolor='red')
        
        # Regione di destinazione
        from matplotlib.patches import Rectangle
        rect = Rectangle((m1, n1), m2-m1, n2-n1, linewidth=2, 
                        edgecolor='blue', facecolor='none', linestyle='--')
        ax1.add_patch(rect)
        
        # Etichetta
        ax1.text(start_x+0.1, start_y+0.1, f'F{f+1}', fontsize=12, fontweight='bold')
    
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.axis('equal')
    
    # Plot 2: Utilizzo banda nel tempo
    ax2.set_title('Utilizzo Banda nel Tempo')
    T = 10
    time_usage = np.zeros(T)
    
    for f in range(len(schedule)):
        if len(schedule[f]) > 0:
            for i in range(len(schedule[f])):
                t = int(schedule[f][i, 0]) + 1  # Converti a 1-based
                rate = schedule[f][i, 3]
                if 0 <= t < T:
                    time_usage[t] += rate
    
    ax2.bar(range(T), time_usage)
    ax2.set_xlabel('Time Slot')
    ax2.set_ylabel('Banda (Mbps)')
    ax2.grid(True)
    
    # Plot 3: Punteggi per flusso
    ax3.set_title('Punteggio per Flusso')
    flow_scores = np.zeros(flows.shape[0])
    for f in range(flows.shape[0]):
        if f < len(schedule) and len(schedule[f]) > 0:
            # Calcolo semplificato del punteggio
            total_traffic = np.sum(schedule[f][:, 3])
            flow_scores[f] = (total_traffic / flows[f, 4]) * 100
    
    ax3.bar(range(1, len(flow_scores)+1), flow_scores)
    ax3.set_xlabel('Flusso')
    ax3.set_ylabel('Punteggio')
    ax3.grid(True)
    
    # Plot 4: Statistiche riassuntive
    ax4.axis('off')
    ax4.set_title('Statistiche Riassuntive')
    
    total_flows = flows.shape[0]
    scheduled_flows = sum(1 for s in schedule if len(s) > 0)
    total_traffic = np.sum(flows[:, 4])
    scheduled_traffic = sum(np.sum(s[:, 3]) for s in schedule if len(s) > 0)
    
    efficiency = (scheduled_traffic / total_traffic) * 100 if total_traffic > 0 else 0
    
    stats_text = [
        f'Punteggio: {total_score:.3f}',
        f'Flussi: {scheduled_flows}/{total_flows}',
        f'Efficienza: {efficiency:.1f}%',
        f'Traffico: {scheduled_traffic:.1f}/{total_traffic:.1f} Mbps'
    ]
    
    for i, text in enumerate(stats_text):
        ax4.text(0.1, 0.8 - i*0.2, text, fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
