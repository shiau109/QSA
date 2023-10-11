
import numpy as np
import matplotlib.pyplot as plt

def get_sim_data( center:np.array, ratio:list, sigma, total_points:int ):
    """
    Get simulated data in IQ plain
    """

    point = []

    for r in ratio:
        point.append( int(r*total_points) )

    dim = center.shape[-1]
    center_num = center.shape[0]
    sim_data = np.empty( (dim, total_points) )

    print( sim_data.shape )
    # Different dimension
    for di in range(dim):
        
        buffer = np.array([])
        # Merge Different center & ratio
        for p_idx, p in enumerate(point):
            mu = center[p_idx][di]
            buffer = np.append(buffer,np.random.normal(mu, sigma, p))
        sim_data[di] = buffer
    # for i in range(dim):
    #     # sim_data[i] = cluster_data[di].flatten()
    #     print(cluster_data[di].flatten().shape)                        
    return sim_data

if __name__ == '__main__':
    pos = np.array([[0,0], [0,1], [0,2]])
    ratio = [0.2,0.7,0.1]
    noise = 0.02
    total_points = 1000
    sim_data = get_sim_data( pos, ratio, noise, total_points )    

    plt.plot(sim_data[0], sim_data[1],"o")
    plt.show()