"""Script involving functions to process a single patient's alleles and compute HED"""
#Standard imports
import statistics as stats

#Project imports
from HED_Flask_App.HED_Tool.utils.build_alignments import build_alignments
from HED_Flask_App.HED_Tool.core.hed_calculate import calculate
from HED_Flask_App.HED_Tool.utils.categorise_allele import HLA_CLASS_I, HLA_CLASS_I_PSEUDO, \
                                             HLA_CLASS_II, OTHER_NON_HLA

def process_patient(patient, alignment_dir, ard_status):
    """Function to build alignments of sequences for a patient from their typings and produce HED results"""
    results = []
    allele_sequences = build_alignments(patient, alignment_dir, ard_status)
    for classification in allele_sequences:
        results.extend(process_sequences(classification))

    results = produce_results(patient.get('patient_id'), results)

    return results

def process_sequences(classification):
    """Extract genes and alleles from classifications and compute HED"""
    results = []
    for sequences_dict in classification.values():
        for gene, alleles in sequences_dict.items():
            hed = calculate(alleles)
            results.append({'gene': gene,
                            'HED': hed})

    return results

def produce_results(patient, results):
    """Function to produce the final results dict"""
    hla_categories = {'class_i': HLA_CLASS_I,
                         'class_i_pseudo': HLA_CLASS_I_PSEUDO,
                         'class_ii': HLA_CLASS_II,
                         'other_non_hla': OTHER_NON_HLA}

    hla_class_hed_results = {key: [] for key in hla_categories}

    for locus in results:
        gene = locus['gene']
        hed = locus['HED']

        for hla_class, genes in hla_categories.items():
            if gene in genes:
                hla_class_hed_results[hla_class].append(hed)
                break

    hla_class_averages = {hla_class: stats.mean(hed_values)
                          for hla_class, hed_values in hla_class_hed_results.items()
                          if hed_values
                         }


    return {'patient_id': patient,
            'batch_results': hla_class_averages,
            'individual_results': results}
