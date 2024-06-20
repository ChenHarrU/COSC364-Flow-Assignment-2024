# COSC364 Flow Assignment

## Overview

This repository is aimed at solving a network flow optimization problem from the COSC364 course. The scripts automate the generation of LP (Linear Programming) files and utilize IBM CPLEX for optimization of network configurations.

## Key Features
- **LP File Generation**: Automatically generates LP files based on user-defined parameters for source nodes, transit nodes, and destination nodes.
  
- **IBM CPLEX Integration**: Utilizes IBM CPLEX via subprocess for reading and optimizing LP files.

- **Results Analysis**: Parses and analyzes optimization results.

- **Command-Line Interface**: Supports flexible execution via command-line arguments.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/cosc364-flow-assignment.git
   cd cosc364-flow-assignment
