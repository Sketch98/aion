from myhdl import block, always

from simple_components import replicate


@block
def one_bit_color(clk, din, vga_signals, vga_ports):
    """
    Maps one bit input, din, to every vga color port. This leads to black and
    white images/text
    """

    red = replicate(din, len(vga_ports.red))
    grn = replicate(din, len(vga_ports.grn))
    blu = replicate(din, len(vga_ports.blu))

    @always(clk.posedge)
    def colors():
        vga_ports.h_sync.next = vga_signals.h_sync
        vga_ports.v_sync.next = vga_signals.v_sync

        vga_ports.red.next = 0
        vga_ports.grn.next = 0
        vga_ports.blu.next = 0
        if vga_signals.video_on:
            vga_ports.red.next = red
            vga_ports.grn.next = grn
            vga_ports.blu.next = blu

    return colors


@block
def n_bit_color(clk, din, vga_signals, vga_ports):
    """
    Maps n bit input, din, to n bit vga color ports
    
    Ex: din=10010101, r=100, g=101, b=01
    """
    blu = len(vga_ports.blu)
    grn = len(vga_ports.grn) + blu
    red = len(vga_ports.red) + grn
    assert len(din) == red

    @always(clk.posedge)
    def colors():
        vga_ports.h_sync.next = vga_signals.h_sync
        vga_ports.v_sync.next = vga_signals.v_sync

        vga_ports.red.next = 0
        vga_ports.grn.next = 0
        vga_ports.blu.next = 0
        if vga_signals.video_on == 1:
            vga_ports.red.next = din[red:grn]
            vga_ports.grn.next = din[grn:blu]
            vga_ports.blu.next = din[blu:0]
    
    return colors
