#############
## Imports ##
#############

import pickle
import numpy as np
import pandas as pd
import bnlearn as bn
from test_model import test_model
import time

######################
## Boilerplate Code ##
######################

def load_data():
    """Load train and validation datasets from CSV files."""
    train_data = pd.read_csv("train_data.csv")  # Load training data
    val_data = pd.read_csv("validation_data.csv")  # Load validation data
    return train_data, val_data

def make_network(df):
    """Define and fit the initial Bayesian Network."""
    print("[+] Constructing initial Bayesian network...")
    start_time = time.time()
    
    # Use Hill Climbing for the initial structure
    DAG = bn.structure_learning.fit(df, methodtype='hc')
    model = bn.parameter_learning.fit(DAG, df)
    
    end_time = time.time()
    print(f"[+] Initial network created in {end_time - start_time:.2f} seconds.")
    return model

def some_dependency_metric(DAG, edge):
    """Calculate a metric to determine edge importance."""
    # Placeholder for an actual metric; modify as needed
    return 0.5  # Placeholder value; modify as needed

def make_pruned_network(df):
    """Define and fit a pruned Bayesian Network."""
    print("[+] Pruning Bayesian network...")
    start_time = time.time()
    
    # Learn the initial structure
    DAG = bn.structure_learning.fit(df, methodtype='hc')  # Use Hill Climbing for initial structure
    
    # Use a different pruning strategy based on a simple heuristic
    pruned_DAG = DAG.copy()
    edges_to_remove = []  # List to store edges to remove
    threshold = 0.1  # Adjusted threshold for pruning

    # Iterate through the adjacency matrix to find edges
    for (i, j), value in np.ndenumerate(DAG['adjmat']):
        if value != 0:  # Check if there is an edge
            # Placeholder for edge importance; replace with actual logic
            edge_strength = 1.0  # Replace this with your actual logic for edge strength
            if edge_strength < threshold:
                edges_to_remove.append((i, j))  # Store the indices of edges to remove
    
    for edge in edges_to_remove:
        pruned_DAG = bn.delete_edge(pruned_DAG, edge)

    # Re-learn parameters for the pruned network
    pruned_model = bn.parameter_learning.fit(pruned_DAG, df)
    end_time = time.time()
    print(f"[+] Pruned network created in {end_time - start_time:.2f} seconds.")
    return pruned_model

def make_optimized_network(df):
    """Perform structure optimization and fit the optimized Bayesian Network."""
    print("[+] Optimizing Bayesian network structure...")
    start_time = time.time()
    
    # Use Hill Climbing for optimization
    optimized_DAG = bn.structure_learning.fit(df, methodtype='hc')  # Hill Climbing
    optimized_model = bn.parameter_learning.fit(optimized_DAG, df)
    
    end_time = time.time()
    print(f"[+] Optimized network created in {end_time - start_time:.2f} seconds.")
    return optimized_model

def save_model(fname, model):
    """Save the model to a file using pickle."""
    with open(fname, 'wb') as f:
        pickle.dump(model, f)
    print(f"[+] Model saved to {fname}")

def evaluate(model_name, val_df):
    """Load and evaluate the specified model."""
    with open(f"{model_name}.pkl", 'rb') as f:
        model = pickle.load(f)
        correct_predictions, total_cases, accuracy = test_model(model, val_df)
        print(f"Total Test Cases: {total_cases}")
        print(f"Total Correct Predictions: {correct_predictions} out of {total_cases}")
        print(f"Model accuracy on filtered test cases: {accuracy:.2f}%")
        return accuracy

############
## Driver ##
############

def main():
    # Load data
    train_df, val_df = load_data()

    # Create and save base model
    base_model = make_network(train_df.copy())
    save_model("base_model.pkl", base_model)

    # Create and save pruned model
    pruned_network = make_pruned_network(train_df.copy())
    save_model("pruned_model.pkl", pruned_network)

    # Create and save optimized model
    optimized_network = make_optimized_network(train_df.copy())
    save_model("optimized_model.pkl", optimized_network)

    # Evaluate all models on the validation set
    print("\nEvaluating models on the validation set...")
    base_accuracy = evaluate("base_model", val_df)
    pruned_accuracy = evaluate("pruned_model", val_df)
    optimized_accuracy = evaluate("optimized_model", val_df)

    print("\nSummary of results:")
    print(f"Base Model Accuracy: {base_accuracy:.2f}%")
    print(f"Pruned Model Accuracy: {pruned_accuracy:.2f}%")
    print(f"Optimized Model Accuracy: {optimized_accuracy:.2f}%")

    print("\n[+] Done")

if __name__ == "__main__":
    main()