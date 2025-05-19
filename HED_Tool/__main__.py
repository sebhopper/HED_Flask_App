"""HED tool"""

#Standard Imports
import argparse
import pathlib

#Project imports
from HED_tool.utils.read import read
from HED_tool.core.process_patient_alleles import process_patient

def main():
    """Main function"""

    args = get_args()

    patient_data = read(args.input_file)

    for patient in patient_data:
        results = process_patient(patient, args.alignments, args.ard_status)
        print(results)

def get_args():
    """Create the Argument Parser"""

    #Construct the argument parser
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('input_file',
                        type=pathlib.Path,
                        help="Input file containg typings")

    parser.add_argument('ard_status',
                        type=bool,
                        default= True,
                        help="True false are you analysing the ARD or full CDS, defaults to True which is ARD only") #pylint: disable=line-too-long

    parser.add_argument('alignments',
                        type=pathlib.Path,
                        help="Directory containing all alignment files")

    return parser.parse_args()

if __name__ == '__main__':
    main()
