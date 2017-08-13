from myhdl import block, always_comb, TristateSignal


@block
def tristate(tri, tx, rx, en):
    """ tristate driver
    Ports:
        tri: tri-state signal
        rx: tri-state input
        tx: the signal to drive the tri-state
        en: enable the tri-state for driving
        
    taken with permission from
    https://gist.github.com/cfelton/e24ed00b78fa4331f602
    """
    assert isinstance(tri, TristateSignal)
    tri_driver = tri.driver()
    
    @always_comb
    def tri_in():
        rx.next = bool(tri)
    
    @always_comb
    def tri_out():
        if en:
            tri_driver.next = tx
        else:
            tri_driver.next = None
    
    return tri_in, tri_out
