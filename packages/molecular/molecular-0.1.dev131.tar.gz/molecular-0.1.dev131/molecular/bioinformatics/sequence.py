"""
sequence.py

>>> abeta = Protein('YEVHHQKLVFFAEDVGSNKGAIIGLMVGGVV')
"""

from typelike import ArrayLike


class Sequence:
    def __init__(self):
        pass


class Protein(Sequence):
    """
    Construct for dealing with protein sequence.

    """

    def __init__(self, sequence, ):
        """


        Parameters
        ----------
        sequence : np.ndarray
            List of residues.
        """

        # Convert to list if not already list
        super().__init__()
        if not isinstance(sequence, ArrayLike):
            residues = list(sequence)

        # Which format are these residues in?
        len_sequence = len(sequence[0])
        if len_sequence == 1:
            residues = _letter_to_code(sequence)
        elif len_sequence != 3:
            raise AttributeError('must supply residue triplets')

        # Save
        self.sequence = sequence

    def to_letters(self, join=False):
        code_to_letter = {
            'ALA': 'A',
            'ARG': 'R',
            'ASN': 'N',
            'ASP': 'D',
            'CYS': 'C',
            'GLN': 'Q',
            'GLU': 'E',
            'GLY': 'G',
            'HIS': 'H',
            'HSD': 'H',
            'ILE': 'I',
            'LEU': 'L',
            'LYS': 'K',
            'MET': 'M',
            'PHE': 'F',
            'PRO': 'P',
            'SER': 'S',
            'THR': 'T',
            'TRP': 'W',
            'TYR': 'Y',
            'VAL': 'V',
        }

        sequence = [code_to_letter[code] for code in self.sequence]

        if join:
            sequence = ''.join(sequence)

        return sequence


    def to_str(self):
        pass


def _letter_to_code(residues):
    # Make sure we're in the right format
    # noinspection DuplicatedCode
    letter_to_code = {
        'A': 'ALA',
        'R': 'ARG',
        'N': 'ASN',
        'D': 'ASP',
        'C': 'CYS',
        'Q': 'GLN',
        'E': 'GLU',
        'G': 'GLY',
        'H': 'HIS',
        'I': 'ILE',
        'L': 'LEU',
        'K': 'LYS',
        'M': 'MET',
        'F': 'PHE',
        'P': 'PRO',
        'S': 'SER',
        'T': 'THR',
        'W': 'TRP',
        'Y': 'TYR',
        'V': 'VAL'
    }
    return [letter_to_code.get(residue, residue) for residue in residues]