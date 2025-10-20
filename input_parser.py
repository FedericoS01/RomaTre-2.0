import numpy as np

def input_parser(filename):
    """
    Parser per input del concorso Huawei UAV optimization
    Legge file di input e restituisce dati strutturati
    """
    try:
        with open(filename, 'r') as fid:
            # Leggi prima riga: M, N, FN, T
            line1 = fid.readline().strip()
            data = [int(x) for x in line1.split()]
            M, N, FN, T = data[0], data[1], data[2], data[3]
            
            print(f'Debug parser: M={M}, N={N}, FN={FN}, T={T}')
            
            # Leggi dati UAV: x, y, B, phi
            uav_data = np.zeros((M*N, 4))
            for i in range(M*N):
                line = fid.readline().strip()
                data = line.split()
                x, y = int(data[0]), int(data[1])
                B, phi = float(data[2]), int(data[3])
                uav_data[i, :] = [x, y, B, phi]
            
            # Leggi dati flussi: f, x, y, tstart, Qtotal, m1, n1, m2, n2
            flows = np.zeros((FN, 9), dtype=int)
            for i in range(FN):
                line = fid.readline().strip()
                data = [int(x) for x in line.split()]
                flows[i, :] = data
            
            return M, N, FN, T, uav_data, flows
            
    except FileNotFoundError:
        raise FileNotFoundError('Impossibile aprire il file di input')
    except Exception as e:
        raise Exception(f'Errore nel parsing: {str(e)}')
