import os
import re
import csv

class FileSearcher:
    def __init__(self, search_pattern):
        self.search_pattern = search_pattern

    def find_files(self, directory, pattern=None):
        """
        Caută fișierele din directorul specificat care se potrivesc u paternul dat.
        Dacă nu este specificat niciun patern, caută toate fișierele.
        """
        results = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if pattern and not re.match(pattern, file):
                    continue
                results.append(os.path.join(root, file))
        return results

    def save_to_csv(self, file_list, filename):
        """
        Salvează lista de fișiere într-un fișier CSV.
        """
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['File Path']) # Scriem header-ul
            for file_path in file_list:
                writer.writerow([file_path])
