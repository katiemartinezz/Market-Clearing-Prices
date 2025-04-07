import sys
import networkx as nx
from networkx.algorithms import bipartite
import os
from collections import Counter
import matplotlib.pyplot as plt

def get_payoff(g):
    #sellers = list(bipartite.sets(g)[0])
    target_payoff = {} # create a dictionary that stores target and its payoff - v : [source, payoff] payoff from corresponding source 
    for source, target, data in g.edges(data=True):  # loop through each edge (u, v) 
        payoff = data['valuation'] - g.nodes[source]['price']  # payoff = valuation of buyer - price of seller 
        if target not in target_payoff:
            target_payoff[target] = []  # initialize an empty list for each target (buyer) if not already present
        target_payoff[target].append((source, payoff))  # add seller and payoff as a tuple for each buyer (v)     
    return target_payoff

def get_best_payoffs(round):
    best = {}
    for buyer, matches in round.items():
        best_seller, max_payoff = max(matches, key=lambda x: x[1])  # select the seller with max payoff
        best[buyer] = (best_seller, max_payoff)
    return best

def find_constrained_set(best): # based on best_payoffs
    constrained_sellers = set()
    list_seller = []
    for seller, payoff in best.values():
        list_seller.append(seller)
    count = Counter(list_seller) # count seller popularity
    elements_more_than_one = {key: value for key, value in count.items() if value > 1} # get popular sellers
    for i in elements_more_than_one:
        constrained_sellers.add(i)
    return constrained_sellers

def adjust_seller_price(g, constrained_sellers): # increase the price of sellers in the constrained set
    for seller in constrained_sellers:
        g.nodes[seller]['price'] += 1
    

def plot_bipartite_graph(g, best_payoffs=None): # plots a bipartite graph with color-coded nodes for two sets: A (sellers) and B (buyers).

    # separate the nodes into two sets A and B
    A, B = bipartite.sets(g)
    
    # create a layout for bipartite graph
    pos = {}
    pos.update((node, (1, index)) for index, node in enumerate(A))  # position of A nodes
    pos.update((node, (2, index)) for index, node in enumerate(B))  # position of B nodes
    
    # draw the graph with specific node color based on sets A and B
    plt.figure(figsize=(10, 8))
    nx.draw(g, pos, with_labels=True, node_size=500, font_size=10, node_color=['skyblue' if node in A else 'lightgreen' for node in g.nodes])

    # If best_payoffs is provided, highlight the edges corresponding to the best payoffs
    if best_payoffs:
        edges_to_highlight = []
        for buyer, (seller, _) in best_payoffs.items():
            edges_to_highlight.append((seller, buyer))

        # Highlight the best match edges
        nx.draw_networkx_edges(g, pos, edgelist=edges_to_highlight, edge_color='red', width=2)

    
    # add labels for better understanding
    plt.title("Bipartite Graph Visualization")
    plt.show()



def main():
    # python ./market_strategy.py market.gml --plot --interactive
    args = sys.argv

    input_file = args[1] # market.gml
    if not os.path.exists(input_file):
        print(f"Error: {input_file} does not exist.")
        return
    
    else: # if file and in path, create graph
        try: 
            graph = nx.read_gml(input_file)
        except (nx.NetworkXError):
            print("Error: Please specify a valid input file or the file format is incorrect.")
            return
    
    if "--plot" in args:
        plot_bipartite_graph(graph)

    # start a round to find payoffs of initial prices 
    round = get_payoff(graph)

    # find out which source provides buyer with best payoff 
    best_payoffs = get_best_payoffs(round)

    # check for constrained sellers
    constrained_sellers = find_constrained_set(best_payoffs)
    
    # if there are constrained sellers, adjust their prices and continue rounds
    while constrained_sellers:
        print(f"Constrained sellers found: {constrained_sellers}. Adjusting prices...")
        
        # adjust new prices
        adjust_seller_price(graph, constrained_sellers)

        # recalculate payoffs with new prices
        round = get_payoff(graph)

        # get the best payoffs for each buyer again
        best_payoffs = get_best_payoffs(round)

        # check for constrained sellers again
        constrained_sellers = find_constrained_set(best_payoffs)

        if "--interactive" in args:
            plot_bipartite_graph(graph, best_payoffs)
        

    print("Market cleared.")
    print("Final best payoff", best_payoffs )
    for i in best_payoffs:
        print(f"Buyer {i} should buy from seller {best_payoffs[i][0]}")


if __name__ == "__main__":
    main()