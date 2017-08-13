from __future__ import absolute_import

from myhdl import Signal, intbv, always_comb, block, instances, always

from ._vga_constants import supported_resolutions, screen_constants
from simple_components import counter


@block
def vga_timer(
        # ports and interfaces
        clk,
        vga_signals,
        
        # parameters
        resolution=(800, 600),
        frequency=72,
        edge_buffers=(0, 0, 0, 0)
        ):
    """
    A generic vga timer module.
    
    Although it is generic, it does NOT support arbitrary screen resolutions
    and frame rates. Only resolutions and frame rates supported by most VGA
    monitors can be used with this module. Not all resolutions will work
    with all monitors. For instance, my monitor didn't vga 1024x768 @ 43 fps
    
    The four buffers (left, right, top, and bottom) are the number of pixels
    on that side of the monitor that should be left black (video_on=0)

    VGA parameters are shamelessly stolen from eewiki:
    https://www.eewiki.net/pages/viewpage.action?pageId=15925278

    720p and 1080p parameters stolen from hamsterworks:
    http://hamsterworks.co.nz/mediawiki/index.php/VGA_timings
    """
    
    assert (*resolution, frequency) in supported_resolutions, \
        '{}x{} @ {}fps not a supported resolution'.format(*resolution,
                                                          frequency)
    
    # h and v for horizontal and vertical constants and signals
    h_front_porch, h_sync_width, h_back_porch, h_polarity, \
        v_front_porch, v_sync_width, v_back_porch, \
        v_polarity = screen_constants.get((*resolution, frequency))
    
    width, height = resolution
    h_total = width + h_front_porch + h_sync_width + h_back_porch
    v_total = height + v_front_porch + v_sync_width + v_back_porch
    
    h = Signal(intbv(0, 0, h_total))
    v = Signal(intbv(0, 0, v_total))
    counters = counter(clk, [h, v], [h_total, v_total], en=Signal(True),
                       pulse_out=[vga_signals.h_refresh, vga_signals.v_refresh],
                       num_chains=2)
    
    left_buffer, right_buffer, top_buffer, bottom_buffer = edge_buffers
    
    @always_comb
    def sync_pulses():
        # determines h_sync and v_sync
        # h_polarity and v_polarity are the polarities during the sync pulse
        h_sync_left = width + h_front_porch - left_buffer
        h_sync_right = h_sync_left + h_sync_width
        vga_signals.h_sync.next = not h_polarity
        if h_sync_left <= h:
            if h < h_sync_right:
                vga_signals.h_sync.next = h_polarity
        
        v_sync_left = height + v_front_porch - top_buffer
        v_sync_right = v_sync_left + v_sync_width
        vga_signals.v_sync.next = not v_polarity
        if v_sync_left <= v:
            if v < v_sync_right:
                vga_signals.v_sync.next = v_polarity
    
    @always_comb
    def blanking():
        vga_signals.video_on.next = 0
        blanking_h = width - left_buffer - right_buffer
        blanking_v = height - top_buffer - bottom_buffer
        if h < blanking_h and v < blanking_v:
            vga_signals.video_on.next = 1
    
    @always_comb
    def xy_out():
        vga_signals.x.next = h[len(vga_signals.x):]
        vga_signals.y.next = v[len(vga_signals.y):]
    
    return instances()
