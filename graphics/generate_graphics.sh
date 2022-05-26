echo "Generating tori for morse chapter"
mkdir morse
python3 morse_torus.py --path_to_output morse/

mkdir rips
python3 rips_circle.py --path_to_output rips --delta 0.3
python3 rips_circle.py --path_to_output rips --delta 0.5
