echo "Running Ising simulation..."
mkdir data
python3 simulate.py --path_to_output data

echo "Generating persistence diagrams in dim 0..."
mkdir diagrams_dim_0
python3 persistence_diagrams.py --path_to_folder data --path_to_output diagrams_dim_0 --dim 0

echo "Generating persistence diagrams in dim 1..."
mkdir diagrams_dim_1
python3 persistence_diagrams.py --path_to_folder data --path_to_output diagrams_dim_1 --dim 1

echo "Done!"
