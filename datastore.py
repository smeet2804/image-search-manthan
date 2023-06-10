import numpy as np
import json
import faiss

# GPU = faiss.StandardGPUResources()
class Datastore:

    def __init__(self, vectors=None, identifiers=None, dimensions=128, gpu=False, inbuilt_index=False):
        self.__dimensions = dimensions
        self.__vectors = None
        self.__identifiers = None

        self.representations = dict()
        self.__mappings = dict()
        # self.index = faiss.read_index("vecdata/vector.index")
        self.index = faiss.IndexFlatIP(self.__dimensions) #bruteforce search index


    def add(self,vector, identifier, name):
        """
            Adds a vector, identifier and name to the index,

            NOTE: make this method better, its very hacky
        """


        self.representations[str(identifier)] = vector
        self.__mappings[str(identifier)] = name

        to_add = []
        to_add.append(vector)
        to_add = np.array(to_add)
        to_add = to_add.reshape(1, self.__dimensions)

        faiss.normalize_L2(to_add)
        self.index.add(to_add)
        
        
    
    def search(self, emb):
        D, I = self.index.search(emb, 10)
        return D,I

    

        
