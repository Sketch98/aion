from myhdl import block, Signal, always_comb


def chain(chain_in, chain_out, chain_type=False):
    def chain_decorator(func):
        @block
        def chain_wrapper(*args, num_chains=1, **kwargs):
            assert num_chains > 0
            if num_chains == 1:
                return func(*args, **kwargs)
            
            lone_input = True
            lone_output = True
            c_in = kwargs.get(chain_in)
            c_out = kwargs.get(chain_out)
            
            # chain_in_sigs and chain_out_sigs can be input as either 1
            # signal, the input of output of the entire system, or as a list
            # of signals. any missing or None signals are added
            chain_in_sigs = []
            if isinstance(c_in, list):
                lone_input = False
                chain_in_sigs = kwargs.pop(chain_in)
                assert len(chain_in_sigs) == num_chains, \
                    'list arguments must match the chain length'
                for i in range(num_chains):
                    if chain_in_sigs[i] is None:
                        chain_in_sigs[i] = Signal(chain_type)
            else:
                if c_in is None:
                    lone_input = False
                chain_in_sigs = [Signal(chain_type) for _ in range(num_chains)]
            
            chain_out_sigs = []
            if isinstance(c_out, list):
                lone_output = False
                chain_out_sigs = kwargs.pop(chain_out)
                assert len(chain_out_sigs) == num_chains, \
                    'list arguments must match the chain length'
                for i in range(num_chains):
                    if chain_out_sigs[i] is None:
                        chain_out_sigs[i] = Signal(chain_type)
            else:
                if c_out is None:
                    lone_output = False
                chain_out_sigs = [Signal(chain_type) for _ in range(num_chains)]
            
            funcs = []
            for i in range(num_chains):
                arg_sigs = []
                for arg in args:
                    if isinstance(arg, list):
                        assert len(arg) == num_chains, \
                            'list arguments must match the chain length'
                        arg_sigs.append(arg[i])
                    else:
                        arg_sigs.append(arg)
                kwarg_sigs = {}
                for key, arg in kwargs.items():
                    if isinstance(arg, list):
                        assert len(arg) == num_chains, \
                            'list arguments must match the chain length'
                        if arg[i] is not None:
                            kwarg_sigs[key] = arg[i]
                    else:
                        kwarg_sigs[key] = arg
                if chain_in_sigs[i] is not None:
                    kwarg_sigs[chain_in] = chain_in_sigs[i]
                if chain_out_sigs[i] is not None:
                    kwarg_sigs[chain_out] = chain_out_sigs[i]
                funcs.append(func(*tuple(arg_sigs), **kwarg_sigs))
            
            @always_comb
            def connect():
                for j in range(1, num_chains):
                    chain_in_sigs[j].next = chain_out_sigs[j - 1]
            
            # myhdl can't detect when a signal is renamed by being added to a
            # list of signals so this compensates
            if lone_input:
                if lone_output:
                    @always_comb
                    def foo():
                        chain_in_sigs[0].next = c_in
                        c_out.next = chain_out_sigs[num_chains - 1]
                    
                    return funcs, connect, foo
                
                @always_comb
                def foo():
                    chain_in_sigs[0].next = c_in
                
                return funcs, connect, foo
            elif lone_output:
                @always_comb
                def foo():
                    c_out.next = chain_out_sigs[num_chains - 1]
                
                return funcs, connect, foo
            return funcs, connect
        
        return chain_wrapper
    
    return chain_decorator
