from myhdl import ConcatSignal


def replicate(din, num_reps, mask=None, mask_to='0'):
    """Takes a bool input din and replicates it into an intbv of length
    num_reps.

    Mask, an optional argument, is a string of 0's and 1's. Every 1 in mask
    causes din to be added to the output intbv while a 0 causes that bit to
    be only 0.

    Ex: mask = '10110
    output = din & 0 & din & din & 0'

    mask_to is what is inserted when mask[i]=='0', so mask_to='1' will change
    the output of the example to: output = din & 1 & din & din & 1

    I added some extra functionality that seemed a natural extension of the
    concept, but i have no idea what the use case is. If din is an intbv then
    the components inserted by mask will be len(din) wide. This forces the
    output to be len(din)*num_reps wide. """
    if mask is None:
        mask = [True] * num_reps
    elif isinstance(mask, str):
        assert len(mask) == num_reps, \
            "if mask is a string, then it must be num_reps characters long.\n" \
            "num_reps = {}, mask length = {}".format(num_reps, len(mask))
        new_mask = []
        for bit in mask:
            if bit == '1':
                new_mask.append(True)
            elif bit == '0':
                new_mask.append(False)
            else:
                raise ValueError("if mask is a string, then it must be "
                                 "composed of only 0's and 1's")
        mask = new_mask
    
    if not isinstance(din, bool):
        mask_to = mask_to * len(din)
    
    concat_terms = []
    for i in range(num_reps):
        if mask[i]:
            concat_terms.append(din)
        else:
            concat_terms.append(mask_to)
    
    return ConcatSignal(*tuple(concat_terms))
