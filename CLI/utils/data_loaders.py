from typing import List, Union
import numpy as np
from . import aa_letters


def seq_to_one_hot(sequence: str, aa_key: dict) -> np.ndarray:
    """

    Parameters
    ----------
    sequence : str
    aa_key : Dict[str, int]

    Returns
    -------
    numpy.ndarray
    """
    arr: np.ndarray = np.zeros((len(sequence), len(aa_key)))
    j: int
    for j, c in enumerate(sequence):
        err: KeyError
        try:
            arr[j, aa_key[c]] = 1
        except KeyError as err:
            print("Invalid sequence letter")
            exit(err)
    return arr


def to_one_hot(seqlist: Union[str, List[str]], alphabet: List[str] = aa_letters) -> np.ndarray:
    """

    Parameters
    ----------
    seqlist : List[str]
    alphabet : List[str]

    Returns
    -------
    numpy.ndarray
    """
    aa_key: dict = {l: i for i, l in enumerate(alphabet)}
    if type(seqlist) == str:
        return seq_to_one_hot(seqlist, aa_key)
    else:
        encoded_seqs: List[np.ndarray] = []
        prot: str
        for prot in seqlist:
            encoded_seqs.append(seq_to_one_hot(prot, aa_key))
        return np.stack(encoded_seqs)
