import subprocess

# List of files to run
files = [
    "process_ocurrences.py",
    "make_reservations_dataset.py",
    "add_vernacular_names.py",
    "get_images.py",
    "get_wikipedia_links.py",
    "make_species_dataset.py",
    "../observations_map.py",
]

# Run each file in order
for file in files:
    subprocess.run(["python", file], shell=True)