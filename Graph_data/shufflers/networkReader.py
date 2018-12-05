from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

#input_file_address = "../network data/giant/"
input_file_address = "../network data/clean/"
#input_file_name = "clean sociopattern_conference_contact.txt"
input_file_name = "clean sociopattern_hospital.txt"

#input_file_name = "giant clean brazil.txt"
#input_file_name = "giant clean email.txt"
#input_file_name = "giant clean brazil.txt"
#input_file_name = "giant clean FilmMessages.txt"
#input_file_name = "giant clean FilmForum.txt"
input_file =  input_file_address + input_file_name 

pandas_data = pd.read_csv( input_file , sep ='\t', header = None)

raw_data = np.array( pandas_data[[0,1,2]] ) #for the case in which we have 2 extra columns of data.
data = raw_data.copy()
vertices_num = np.max( data[:, 1:] ) + 1

print(input_file_name)
#print("hi")