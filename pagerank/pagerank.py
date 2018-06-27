import pandas as pd
import numpy as np

dataset_path = "data/soc-sign-bitcoinotc.csv"

def initialize_data_set():
    '''
        This method will read and filter dataset and return a tuple of lists

        Returns:
            Tuple(data_src,data_target,nodes): Tuple of lists
                data_src[List] : list of transactions source points
                data_target[List] : list of transactions destination points
                nodes[List]: list of union between data_src and data_target transactions
    '''
    data = pd.read_csv(dataset_path).query('Evaluation >= 8')
    data_src = list(data.Source)
    data_target = list(data.Target)
    nodes = list(set(data_src).union(set(data_target)))
    return (data_src,data_target,nodes,data)


def build_adj_matrix(data_src,data_target):
    '''
        This method will build an abstraction of graph structure that represents the relationship
        between transactions.

        Args:
            data_src[List]: List of Source columns
            data_target[List]: List of target columns
        Returns:
            adj_dict{ Source : [List of targets] } : dictionary with source and destination transactions
    '''
    adj_dict = {no:[] for no in nodes}
    for i in range(len(data_src)):
        adj_dict[data_src[i]].append(data_target[i])
    return adj_dict


def pagerank(model,treshold,vector,count):
    '''
        PageRank algorithm

        Args:
            Model: Used to determine the behavior of algorithm
            treshold: Used to determine when pagerank algorithm will converge
            vector: Used to compute pagerank algorithm
            count: count how many iterations we need to converge
        Return:
            Tuple([Results of weights], count_of_iterations)
    '''
    if sum(abs(model*vector-vector)) > treshold:
        return pagerank(model,treshold, model*vector, count + 1)
    return ( model*vector, count )


def converge_pagerank_algorithm(adj_dict,nodes,w_v):
    '''
        Used to set up and initialize some parameters used in pagerank algorithm and run it
    '''

    # Initialize weight matrix with zeros
    weight_matrix = [ [0] * len(nodes) for j in range(len(nodes)) ]
    
    #Fill weight matrix
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            out_degree = len(adj_dict[nodes[i]])
            weight_matrix[j][i] = 1/out_degree if nodes[j] in adj_dict[nodes[i]] else 0
    weight_matrix = np.matrix(weight_matrix)

    #Define parameters to init pagerank algorithm
    b = (1/len(nodes)) * np.matrix([[1 for i in range(len(nodes))] for j in range(len(nodes))])
    model = w_v * weight_matrix + (1 - w_v) * b
    vector = (1/len(nodes)) * np.matrix([[1] for i in range(len(nodes))])
    return pagerank(model,0.001,vector,0)

if __name__ == "__main__":
    data_src,data_target,nodes,data = initialize_data_set()
    adj_dict = build_adj_matrix(data_src,data_target)
    result = converge_pagerank_algorithm(adj_dict,nodes,0.85)
    result = [cell.item(0,0) for cell in result[0]]
    result_data = pd.DataFrame({'id': nodes, 'PageRank': result})
    result_data.to_csv(path_or_buf='result.csv', index=False)
    data.to_csv(path_or_buf='filtered-sign-bitcoinotc.csv', columns=['Source', 'Target'], index=False)
    
