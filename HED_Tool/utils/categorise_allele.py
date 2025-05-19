"""Script to categorise the HLA alleles"""

HLA_CLASS_I = ['A', 'B', 'C', 'E', 'F', 'G']
HLA_CLASS_I_PSEUDO = ['H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'Y']
HLA_CLASS_II = ['DRA', 'DRB1', 'DRB2', 'DRB3', 'DRB4', 'DRB5',
                'DRB6', 'DRB7', 'DRB8', 'DRB9', 'DQA1', 'DQA2',
                'DQB1', 'DQB2', 'DPA1', 'DPA2', 'DPB1', 'DPB2',
                'DMA', 'DMB', 'DOA', 'DOB']
OTHER_NON_HLA = ['HFE', 'MICA', 'MICB', 'TAP1', 'TAP2']

def categorise_allele(allele_name: str) -> str:
    """Categorise an allele based on its name."""

    # Remove prefix if present (e.g., HLA-A*01:01 -> A)
    if allele_name.startswith("HLA-"):
        gene = allele_name[4:].split('*')[0]
    else:
        gene = allele_name.split('*')[0]

    # Determine category
    if gene in HLA_CLASS_I:
        return "class_i"
    if gene in HLA_CLASS_I_PSEUDO:
        return "class_i_pseudo"
    if gene in HLA_CLASS_II:
        return "class_ii"
    if gene in OTHER_NON_HLA:
        return "Other Non-HLA"

    return "Unknown"
