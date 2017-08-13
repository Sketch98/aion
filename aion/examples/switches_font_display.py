import os

from myhdl import always_comb, block, Signal, intbv

from simple_components import counter, clk_div
from utils import VgaPorts, RamPort, ucf_gen
from vga import font_controller


@block
def switches_font_display(clk, vga_ports, resolution, frequency, font_size):
    """A myhdl top for testing font_controller on nexys2_1200. Reads 7
    switches and writes their value to the ram at ~1800hz. The
    font_controller handles everything else. """
    screen_width, screen_height = resolution
    font_width, font_height = font_size

    ram_depth = screen_width // font_width * screen_height // font_height
    
    ram_write_port = RamPort(ram_depth, 7)
    font_ctrl = font_controller(clk, vga_ports, ram_write_port, resolution,
                                frequency, font_size, 128)
    
    write_clk = Signal(bool(0))
    div = clk_div(5e3, clk, write_clk)
    screen_crawler = counter(write_clk, ram_write_port.addr)

    @always_comb
    def write_switches():
        ram_write_port.en.next = True
        ram_write_port.data.next = ram_write_port.addr[7:]

    return font_ctrl, div, screen_crawler, write_switches


if __name__ == '__main__':
    clk = Signal(bool(0))
    vga_ports = VgaPorts(3, 3, 2)
    top = switches_font_display(clk, vga_ports, (800, 600), 72, (7, 12))
    top.convert(hdl='VHDL')
    this_dir = os.path.dirname(__file__)
    vhd_file = '/'.join([this_dir, 'switches_font_display.vhd'])
    ucf_gen(vhd_file, 'nexys2_1200.ucf')
