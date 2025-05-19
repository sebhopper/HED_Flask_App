"""Script to calculate the HED value for a given typing dictionary"""

#Standard imports
from itertools import zip_longest

#Project imports
from HED_Flask_App.HED_Tool.resources.aa_matrices import grantham_distance

def calculate(typing:dict):
    """Function to perform the HED calculation utilising the Grantham Distance"""

    #If the typing values is only one this indicates that the patient is homozygous at this allele and therefore HED will be 0 #pylint: disable=line-too-long
    if len(typing.values()) == 1:
        return 0

    #Load the Grantham Distance matrix from the resources
    grantham = grantham_distance()

    #Sort the sequences by length and make sure the longest length is stored as seq1 for normalisation
    seq1, seq2 = sorted(typing.values(), key=len, reverse=True)[:2]

    #Complete the HED calculation using the Grantham distance matrix
    hed = sum(grantham[xx] for xx in zip_longest(seq1,seq2))/len(seq1)

    return hed
