import os

from myhdl import Signal, block, intbv

from vga import vga_timer, n_bit_color
from utils import VgaSignals, VgaPorts, ucf_gen


@block
def vga_top(clk, vga_ports, resolution, frequency):
    """A myhdl top for testing vga_timer on nexys2_1200. Outputs a constant
    image on a monitor at 800x600 pixels at 72fps. """
    width, height = resolution
    vga_signals = VgaSignals(width, height)
    timer = vga_timer(clk, vga_signals, resolution, 72)
    color = n_bit_color(clk, vga_signals.x[8:], vga_signals, vga_ports)
    return timer, color


if __name__ == "__main__":
    clk = Signal(bool(0))
    vga_ports = VgaPorts(3, 3, 2)
    vga_top_inst = vga_top(clk, vga_ports, (800, 600), 72)
    vga_top_inst.convert(hdl='VHDL')
    this_dir = os.path.dirname(__file__)
    vhd_file = '/'.join([this_dir, 'vga_top.vhd'])
    ucf_gen(vhd_file, 'nexys2_1200.ucf')
if __name__ == '__main__':
    clk = Signal(bool(0))
    vga_ports = VgaPorts(3, 3, 2)
    top = switches_font_display(clk, vga_ports, (800, 600), 72, (7, 12))
    top.convert(hdl='VHDL')
    this_dir = os.path.dirname(__file__)
    vhd_file = '/'.join([this_dir, 'switches_font_display.vhd'])
    ucf_gen(vhd_file, 'nexys2_1200.ucf')