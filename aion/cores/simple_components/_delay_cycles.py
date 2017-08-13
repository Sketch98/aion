from myhdl import block, Signal, always_comb, always


@block
def delay_cycles(clk, din, dout, delay_by=1):
    """Delays din by delay_by clk cycles."""
    delay_sigs = [Signal(din.val) for _ in range(delay_by)]

    @always_comb
    def input_rename():
        delay_sigs[0].next = din

    @always(clk.posedge)
    def name_me():
        for i in range(1, len(delay_sigs)):
            delay_sigs[i].next = delay_sigs[i-1]
        dout.next = delay_sigs[delay_by - 1]

    return input_rename, name_me

