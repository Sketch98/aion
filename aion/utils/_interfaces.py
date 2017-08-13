from myhdl import Signal, intbv, TristateSignal


class RamPort(object):
    def __init__(self, ram_depth, ram_width):
        self.addr = Signal(intbv(0, 0, ram_depth))
        self.data = Signal(intbv(0)[ram_width:])
        self.en = Signal(bool(0))


class RomPort(object):
    def __init__(self, rom_depth, rom_width):
        self.clk = Signal(bool(0))
        self.addr = Signal(intbv(0, 0, rom_depth))
        self.data = Signal(intbv(0)[rom_width:])


class VgaPorts(object):
    def __init__(self, red_width, green_width, blue_width):
        self.red = Signal(intbv(0)[red_width:])
        self.grn = Signal(intbv(0)[green_width:])
        self.blu = Signal(intbv(0)[blue_width:])
        self.h_sync = Signal(bool(0))
        self.v_sync = Signal(bool(0))


class VgaSignals(object):
    def __init__(self, resolution):
        self.h_sync = Signal(bool(0))
        self.v_sync = Signal(bool(0))
        self.video_on = Signal(bool(0))
        self.h_refresh = Signal(bool(0))
        self.v_refresh = Signal(bool(0))
        self.x = Signal(intbv(0, 0, resolution[0]))
        self.y = Signal(intbv(0, 0, resolution[1]))


class SevenSegmentDisplay(object):
    def __init__(self, num_digits):
        self.segment_n = Signal(intbv(0)[7:])
        self.decimal_point_n = Signal(bool(0))
        self.digit_sel_n = Signal(intbv(0)[num_digits:])


class MicroSD(object):
    def __init__(self):
        self.sd_reset = Signal(bool(0))
        self.sd_card_detect = Signal(bool(0))
        self.sd_clk = Signal(bool(0))
        self.sd_cmd = Signal(bool(0))
        self.sd_data = Signal(intbv(0)[4:])


class PS2Ports(object):
    def __init__(self):
        self.clk_tri = TristateSignal(bool(0))
        self.data_tri = TristateSignal(bool(0))


class PS2Signals(object):
    def __init__(self):
        self.clk_rx = Signal(bool(0))
        self.clk_tx = Signal(bool(0))
        self.clk_en = Signal(bool(0))
        self.data_rx = Signal(bool(0))
        self.data_tx = Signal(bool(0))
        self.data_en = Signal(bool(0))
        

class RS232(object):
    def __init__(self):
        self.rs_rx = Signal(bool(0))
        self.rs_tx = Signal(bool(0))


class Nexys2Memory(object):
    def __init__(self):
        self.addr = Signal(intbv(0)[24:])
        self.data = Signal(intbv(0)[16:])
        self.mem_oe = Signal(bool(0))
        self.mem_wr = Signal(bool(0))


class Nexys2RAM(object):
    def __init__(self):
        self.ram_cs = Signal(bool(0))
        self.ram_clk = Signal(bool(0))
        self.ram_ctrl_reg_en = Signal(bool(0))
        self.ram_LB = Signal(bool(0))
        self.ram_UB = Signal(bool(0))
        self.ram_wait = Signal(bool(0))


class Nexys2Flash(object):
    def __init__(self):
        self.flash_reset = Signal(bool(0))
        self.flash_cs = Signal(bool(0))
        self.flash_status = Signal(bool(0))


class Nexys4RAM(object):
    def __init__(self):
        self.ram_clk = Signal(bool(0))
        self.ram_addr_valid_n = Signal(bool(0))
        self.ram_ce_n = Signal(bool(0))
        self.ram_ctrl_reg_en = Signal(bool(0))
        self.ram_oe_n = Signal(bool(0))
        self.ram_we_n = Signal(bool(0))
        self.ram_LB_n = Signal(bool(0))
        self.ram_UB_n = Signal(bool(0))
        self.ram_wait = Signal(bool(0))
        self.data = Signal(intbv(0)[16:])
        self.addr = Signal(intbv(0)[23:])


class Nexys4Flash(object):
    def __init__(self):
        self.qspi_sck = Signal(bool(0))
        self.qspis_data = Signal(intbv(0)[4:])
        self.qspics_n = Signal(bool(0))


class Nexys4Amp(object):
    def __init__(self):
        self.amp_pwm = Signal(bool(0))
        self.amp_en = Signal(bool(0))


class Nexys4Microphone(object):
    def __init__(self):
        self.mic_clk = Signal(bool(0))
        self.mic_data = Signal(bool(0))
        self.mic_lr_sel = Signal(bool(0))


class Nexys4TempSensor(object):
    def __init__(self):
        self.tmp_scl = Signal(bool(0))
        self.tmp_sda = Signal(bool(0))
        self.tmp_int = Signal(bool(0))
        self.tmp_crit_temp = Signal(bool(0))


class Nexys4Accelerometer(object):
    def __init__(self):
        self.acl_miso = Signal(bool(0))
        self.acl_mosi = Signal(bool(0))
        self.acl_sck = Signal(bool(0))
        self.acl_ss = Signal(bool(0))
        self.acl_int1 = Signal(bool(0))
        self.acl_int2 = Signal(bool(0))
