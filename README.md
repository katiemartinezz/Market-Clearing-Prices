# Market Strategy

This Python script simulates a market with buyers and sellers using a bipartite graph. The goal is to model the process of price adjustments based on buyer and seller interactions, using an iterative approach.

## Requirements
- Python 3.x
- NetworkX
- Matplotlib

## Usage
To run the simulation, use the following command in your terminal:
``` python market_strategy.py <input_file.gml> [--plot] [--interactive] ```
- <input_file.gml>: A GML file representing the market graph (buyers, sellers, and edges with valuations).
- --plot: Visualize the initial bipartite graph.
- --interactive: Show the graph after each round of price adjustments (useful for seeing how prices evolve).

### Example:
``` python market_strategy.py market.gml --plot --interactive ```

## How it Works
- The market simulation starts with initial prices for the sellers.
- In each round:
    - Payoffs are calculated for each buyer based on their current sellers' prices.
    - Buyers select their best seller (one with the highest payoff).
    - If a seller is matched to multiple buyers (constrained), their price is adjusted.
    - The process continues until no more price adjustments are needed.

## Output
- The final best matchings (buyer -> seller) with the highest payoff.
- Visualization of the bipartite graph, with red edges indicating the best matches.
