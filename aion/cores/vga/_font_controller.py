from __future__ import absolute_import

from myhdl import always, always_comb, block, Signal, intbv, ResetSignal

from ._vga_timer import vga_timer
from ._vga_color import one_bit_color
from hard_cores import font_rom
from simple_components import delay_cycles, counter
from utils import VgaSignals, RamPort, RomPort


@block
def font_ram(
        # ports and interfaces
        clk,
        write_port,
        read_port,
        
        # parameters
        depth,):
    """
    Infers simple dual port ram with generic depth.
    """
    assert len(write_port.data) == len(read_port.data),\
        'font ram data widths do not match\n dina width {}, doutb width {}'\
        .format(len(write_port.data), len(read_port.data))
    assert len(write_port.addr) == len(read_port.addr),\
        'font ram addresses do not match\n addra width {}, addrb width {}'\
        .format(len(write_port.addr), len(read_port.addr))
    assert 2 ** (len(write_port.addr) - 1) < depth\
        <= 2 ** (len(write_port.addr))
    width = len(write_port.data)
    
    ram = [Signal(intbv(0)[width:]) for _ in range(depth)]
    
    @always(clk.posedge)
    def read():
        read_port.data.next = ram[int(read_port.addr)]
    
    @always(clk.posedge)
    def write():
        if write_port.en:
            ram[int(write_port.addr)].next = write_port.data
    
    return read, write


@block
def font_controller(
        # ports and interfaces
        clk,
        vga_ports,
        ram_write_port,
        
        # parameters
        resolution=(800, 600),
        frequency=72,
        font_size=(12, 16),
        num_characters=128):
    """A hardware block that handles a rom, ram, and vga timer to provide a
    simple interface from a system on an fpga to a vga controlled monitor.

    The inputs write_enable, addr, and data are the write port to the ram.
    Resolution is a tuple of screen width, screen height, and screen
    frequency. Font size is a tuple of font width and font height. """
    
    # calculate constants like rom and ram depth
    screen_width, screen_height = resolution
    font_width, font_height = font_size
    chars_per_row = screen_width // font_width
    rows_per_screen = screen_height // font_height
    
    # screen buffers so partial characters are not shown
    h_buffer = screen_width % font_width
    l_buffer = h_buffer // 2
    r_buffer = h_buffer - l_buffer
    v_buffer = screen_height % font_height
    t_buffer = v_buffer // 2
    b_buffer = v_buffer - t_buffer
    edge_buffers = (l_buffer, r_buffer, t_buffer, b_buffer)
    
    vga_signals = VgaSignals(resolution)
    timer = vga_timer(clk, vga_signals, resolution, frequency, edge_buffers)
    
    rom_depth = num_characters * font_height
    rom_port = RomPort(rom_depth, font_width)
    rom = font_rom(font_size, 'font_rom', rom_port)
    
    ram_depth = chars_per_row * rows_per_screen
    ram_width = (num_characters - 1).bit_length()
    ram_read_port = RamPort(ram_depth, ram_width)
    ram = font_ram(clk, ram_write_port, ram_read_port, ram_depth)
    
    # h and v rsts that trigger when h_refresh and v_refresh from vga timer
    # are set. these reset the x and y counters
    h_rst = ResetSignal(0, 1, 'sync')
    v_rst = ResetSignal(0, 1, 'sync')
    
    # x and y counters to calculate which character is being displayed
    pixel_sel = Signal(intbv(0, 0, font_width))
    x_ram = Signal(intbv(0, 0, chars_per_row))
    x_counters = counter(clk, [pixel_sel, x_ram], [font_width, chars_per_row],
                         h_rst, en=Signal(True), num_chains=2)
    
    y_char_row = Signal(intbv(0, 0, font_height))
    y_ram = Signal(intbv(0, 0, ram_depth))
    y_counters = counter(clk, [y_char_row, y_ram], [font_height, ram_depth],
                         v_rst, [1, chars_per_row], en=vga_signals.h_refresh,
                         num_chains=2)
    
    sigs = [vga_signals.h_sync, vga_signals.v_sync, vga_signals.video_on, pixel_sel]
    delayed_vga_sigs = VgaSignals(resolution)
    delayed_pixel_sel = Signal(intbv(0, 0, font_width))
    delayed_sigs = [delayed_vga_sigs.h_sync, delayed_vga_sigs.v_sync,
                    delayed_vga_sigs.video_on, delayed_pixel_sel]
    delays = [delay_cycles(clk, sigs[i], delayed_sigs[i], 2)
              for i in range(len(sigs))]
    
    pixel = Signal(bool(0))
    color = one_bit_color(clk, pixel, delayed_vga_sigs, vga_ports)
    
    @always_comb
    def foo():
        rom_port.clk.next = clk
        ram_read_port.addr.next = x_ram + y_ram
        rom_port.addr.next = ram_read_port.data * font_height + y_char_row
        pixel.next = rom_port.data[delayed_pixel_sel]
        
        h_rst.next = vga_signals.h_refresh
        v_rst.next = vga_signals.v_refresh
    
    return rom, ram, timer, foo, delays, color, x_counters, y_counters
