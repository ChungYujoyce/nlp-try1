from typing import List
from vectors import vector

class Word:
    # A single word (one line of the input file)

    def __init__(self, text, vector, frequency):
        self.text = text
        self.vector = vector
        self.frequency = frequency
    
    def __repr(slef):
        vector_preview = ', '.join(map(str, self.vector[:2]))
        return f"{self.text} [{vector_preview}...]"

