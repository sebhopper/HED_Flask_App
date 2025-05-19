"""Build the required alignments"""
import pathlib
from pathlib import Path
from HED_Flask_App.HED_Tool.utils.alignment_parsing import HEDAlignment
from HED_Flask_App.HED_Tool.utils.translate import translate_nt_to_prot
from HED_Flask_App.HED_Tool.utils.process_indels import process_indels

def build_alignments(patient_data:dict, alignments_directory:pathlib.Path, ARD:bool):
    """Function to build the required alignments"""
        #Ensure alignments_directory is a Path object
    if isinstance(alignments_directory, str):
        alignments_directory = Path(alignments_directory)

    grouped_allele_seqs = {}  # {gene_prefix: {allele: protein_sequence}}

    for classification, genes in patient_data['typing'].items():
        for gene, typings in genes.items():

            if any('N' in item for item in typings):
                continue
            # Load the alignment file for the current gene
            alignment_file = alignments_directory / f"{gene}_nuc.txt"
            preprocessed_alignment = HEDAlignment(alignment_file, required_typings=typings)

            #If ARD is True, extract the ARD region
            if ARD:
                preprocessed_alignment = preprocessed_alignment.extract_ard()

            # Process the alignment
            processed_alignment = process_indels(preprocessed_alignment)
            processed_alignment = processed_alignment.remove_pipes(processed_alignment)

            # Translate nucleotide sequences to protein sequences
            for allele in typings:
                if allele in processed_alignment:
                    protein_seq = translate_nt_to_prot(processed_alignment[allele]).rstrip('*')

                    # Organize by classification and gene
                    if classification not in grouped_allele_seqs:
                        grouped_allele_seqs[classification] = {}
                    if gene not in grouped_allele_seqs[classification]:
                        grouped_allele_seqs[classification][gene] = {}
                    grouped_allele_seqs[classification][gene][allele] = protein_seq

    # Convert to a list of grouped dictionaries (if needed)
    allele_seq_list = [
        {classification: genes}
        for classification, genes in grouped_allele_seqs.items()
    ]


    return allele_seq_list
