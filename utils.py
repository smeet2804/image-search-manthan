import json
import numpy as np
from numpy.lib.utils import source

with open("vecdata/representations_deepface_lfw.json") as outputFile:
        representaions = json.load(outputFile)
        outputFile.close()

with open("vecdata/mappings_deepface_lfw.json") as outputFile:
        mappings = json.load(outputFile)
        outputFile.close()

with open("vecdata/file_name_mappings_lfw.json") as outputFile:
        file_name_mappings = json.load(outputFile)
        outputFile.close()

# with open("vecdata/link_maps.json") as outputFile:
#         link_maps = json.load(outputFile)
#         outputFile.close()


def get_link_maps():
        return link_maps

def get_file_name_mappings():
        return file_name_mappings        

def get_representations():
        return representaions

def make_mappings():
        """
        Mappings contain maps of identifiers to names

        {
                "identifier" : "name"
        }
        """

        mappings = dict()
        for idx in representaions:
                mappings[idx] = list(representaions[idx].keys())[0]
                # print(list(representaions[idx].keys())[0])
        with open("vecdata/mappings_deepface", "w") as outputFile:
                json.dump(mappings, outputFile)
                outputFile.close()

def get_vectors():
        """
                returns all the embeddings as a list from representations
        """

        mappings = get_mappings()
        vectors = []
        names = []
        identifiers = list(mappings.keys())
        identifiers = np.array(identifiers, dtype=np.float32)

        print(identifiers) 

        for index in mappings:
                name, vector = yield_pairs(index)
                vector = np.array(vector, dtype=np.float32)
                vectors.append(vector)
                names.append(name)
        
        return names, vectors
 
def get_mappings():
        return mappings

def yield_pairs(index):
    return mappings[str(index)], representaions[str(index)][mappings[str(index)]]


    

    
