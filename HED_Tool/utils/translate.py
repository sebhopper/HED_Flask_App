import Bio
from Bio.Seq import Seq



def translate_nt_to_prot(nt_sequence: str):
    """
    This function translates nucleotide sequences to protein sequences.
    It uses the Biopython library to perform the translation.
    """
    #Create a Seq object
    seq_obj = Seq(nt_sequence)

    #Translate the nucleotide sequence to protein
    protein_sequence = seq_obj.translate()

    return str(protein_sequence)
