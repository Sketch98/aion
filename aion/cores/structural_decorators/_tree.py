from myhdl import block, Signal, intbv


# def bloopadoop(terms):
#     cur_sum = 0
#     for term in terms:
#         cur_sum += term.val.max
#     return cur_len.bit_length()


# def schmeckle(terms):
#     cur_product = 1
#     for term in terms:
#         cur_product *= term.val.max
#     return cur_product.bit_length()


def tree(num_branches, get_result_width):
    """Decorates a hardware block that takes a list of signal inputs, terms,
    and a signal result. This decorator uses a tree structure with
    num_branches branches. get_result_width is a function that is called with
    terms to compute the length of the result that func will give if given
    those terms. Any additional args or kwargs will be passed to every
    hardware block instance. """
    
    def tree_decorator(func):
        @block
        def wrapper(terms, root_result, *args, **kwargs):
            assert len(terms) > 0
            if len(terms) <= num_branches:
                return func(terms, root_result, *args, **kwargs)
            
            branch_indices = _balanced_tree_indexer(len(terms), num_branches)
            branches = []
            branch_results = []
            for i in range(num_branches):
                branch_terms = terms[branch_indices[i][0]:branch_indices[i][1]]
                result_width = get_result_width(branch_terms)
                branch_result = Signal(intbv(0)[result_width:])
                branches.append(
                    wrapper(branch_terms, branch_result, *args, **kwargs))
                branch_results.append(branch_result)
            
            root = wrapper(branch_results, root_result, *args, **kwargs)
            return root, branches
        
        return wrapper
    
    return tree_decorator


def _balanced_tree_indexer(num_leaves, num_branches):
    """Makes num_branches buckets and fills the buckets as evenly as possible
    with num_leaves
    leaves then returns a set of start and end indices for slicing the list
    of leaves. """
    floor = num_leaves // num_branches
    widths = [floor] * num_branches
    for i in range(num_leaves % num_branches):
        widths[i] += 1
    branch_indices = []
    cur_index = 0
    for i in range(num_branches):
        branch_indices.append((cur_index, cur_index + widths[i]))
        cur_index += widths[i]
    return branch_indices
