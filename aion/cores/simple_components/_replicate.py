from myhdl import ConcatSignal


def replicate(din, num_reps, mask=None):
    """Takes a bool input din and replicates it into an intbv of length
    num_reps.

    Mask, an optional argument, is a string of 0's, 1's, and x's of length
    num_reps. Every 0 in mask causes that bit in the output to be a 0 and
    similarly for 1. An x will insert din at that bit. The defaul mask is all
    x's which replicates din num_reps times.

    Ex: mask = '1xx10x'
    output = 1 & din & din & 1 & 0 & din' """
    if mask is None:
        mask = 'x' * num_reps
    
    concat_terms = []
    if isinstance(mask, str):
        assert len(mask) == num_reps, \
            "if mask is a string, then it must be num_reps characters long.\n"\
            "num_reps = {}, mask length = {}".format(num_reps, len(mask))
        for bit in mask:
            if bit == '1':
                concat_terms.append(True)
            elif bit == '0':
                concat_terms.append(False)
            elif bit == 'x':
                concat_terms.append(din)
            else:
                raise ValueError("if mask is a string, then it must be "
                                 "composed of only 0's and 1's")
    else:
        raise ValueError("mask must be none or a list")
    return ConcatSignal(*tuple(concat_terms))
