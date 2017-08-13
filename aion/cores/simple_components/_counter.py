from myhdl import Signal, intbv, block, always_comb, always_seq

from structural_decorators import chain


@chain('en', 'pulse_out')
@block
def counter(clk, count=None, max_value=0, rst=None, inc=1, min_value=0,
            pulse_out=None, en=None):
    """ A simple counter that counts from min_value to max_value by inc
    increments. Outputs a pulse when counter rolls over. """
    
    if en is None:
        en = True
    
    if max_value == 0:
        max_value = count.max
    if count is None:
        count = Signal(intbv(0, min=min_value, max=max_value))
    
    @always_seq(clk.posedge, reset=rst)
    def update_count():
        if en:
            if count == max_value - inc:
                count.next = min_value
            else:
                count.next = count + inc
    
    if pulse_out is None:
        return update_count
    
    @always_comb
    def output_pulse():
        pulse_out.next = 0
        if en and count == max_value - inc:
            pulse_out.next = 1
    
    return update_count, output_pulse