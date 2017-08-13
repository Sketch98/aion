import os
import re
import logging


class EntityDeclarationError(Exception):
    """The entity declaration in a .vhd file is incorrect"""
    pass


class PortDeclarationError(Exception):
    """The port declaration in .vhd file is incorrect"""
    pass

# regular expressions for finding a NET's port name, if a NET is std_logic,
# and a port's width
port_name = re.compile('^[ \t]*(\w+):')
std_logic = re.compile('std_logic')
port_width = re.compile('\(([0-9]+) downto ([0-9]+)\)')


def _add_vhd_port(ports_dict, line):
    """Pulls the port name from line. Adds (port name: port width) to
    ports_dict as a (key: value) pair. Port width is None if the port is
    std_logic and a list of ints otherwise. """
    # Grab the port from the port declaration line
    port_name_match = port_name.match(line)
    if port_name_match is not None:
        port = port_name_match.group(1)
        std_logic_match = std_logic.search(line)
        if std_logic_match is not None:
            ports_dict[port] = None
            return
        port_width_match = port_width.search(line)
        if port_width_match is not None:
            ports_dict[port] =\
                [i for i in range(int(port_width_match.group(2)),
                                  int(port_width_match.group(1))+1)]
            return
    raise PortDeclarationError('Port declaration incorrect\n{}'.format(line))


def _add_ucf_port(port, port_num, ports_dict, std_logic_found):
    v = ports_dict[port]
    if v is None:
        if port_num is None:
            del ports_dict[port]
            std_logic_found.append(port)
            logging.info('Ucf port {} added'.format(port))
            logging.info('Ucf port removed {}'.format(port))
            return
    else:
        port_num = int(port_num)
        if port_num in v:
            v.remove(port_num)
            logging.info('Ucf port {} num {} added'.format(port, port_num))
            if len(v) == 0:
                del ports_dict[port]
                logging.info('Ucf port removed {}'.format(port))
            return
    logging.warning('Vhd port num and ucf port num dont match.\nPort: {}, '
                    'vhd port num: {}, ucf port nums: {} '
                    .format(port, port_num, v))


net = re.compile('^NET[ \t]+"([a-zA-Z]\w*)(<([0-9]+)>)?"')
timespec = re.compile(
    '^TIMESPEC[ \t]+"[a-zA-Z]\w*"[ \t]+=[ \t]+PERIOD[ \t]+"([a-zA-Z]\w*)"')


def _check_ucf_port(ports_dict, std_logic_found, line, new_ucf):
    """Checks if line is a NET that matches with the ports in ports_dict. If
    line is a TIMESPEC it checks std_logic_found to see if there is a
    std_logic port with the same port name. """
    net_match = net.match(line)
    if net_match is not None:
        port = net_match.group(1)
        port_num = net_match.group(3)
        if port in ports_dict:
            _add_ucf_port(port, port_num, ports_dict, std_logic_found)
            new_ucf.write(line)
        else:
            # myhdl mangles vhd port names when they're part of interfaces
            # mangled ports will have the true port name at the end
            for key in ports_dict:
                if key.endswith(port):
                    logging.info('Ucf port {} matched with vhd port {}'
                                 .format(port, key))
                    _add_ucf_port(key, port_num, ports_dict, std_logic_found)
                    new_ucf.write(line.replace(port, key))
                    break

    timespec_match = timespec.match(line)
    if timespec_match is not None:
        port = timespec_match.group(1)
        if port in std_logic_found:
            new_ucf.write(line)


def _get_vhd_ports(vhd_file):
    # Grab ports from vhd_file header.
    ports_dict = {}
    with open(vhd_file, 'r') as vhd:
        found_port_flag = False
        for line in vhd:
            line = line.strip()
            # The 'port' keyword signifies the beginning of the entity
            # declaration where all of the ports are listed
            if line == "port (" or line == "port(":
                found_port_flag = True
                continue
            if found_port_flag:
                # ');' signifies the end of the entity declaration
                if line == ");":
                    print(ports_dict)
                    break
                
                _add_vhd_port(ports_dict, line)
        else:
            raise EntityDeclarationError("Entity declaration in {} is"
                                         " incorrect.".format(vhd_file))
    return ports_dict


def _combine_file_names(*args):
    def grab_name(file):
        start = file.rfind('/')
        end = file.find('.')
        return file[start+1:end]
    pass
    
    new_file_name = '_'.join(list(map(grab_name, args)))
    new_file_name += args[-1][args[-1].find('.'):]
    return new_file_name


def ucf_gen(vhd_file, master_ucf_file, destination_dir=None):
    """Reads the vhd file's entity declaration and builds a new ucf file by
    pulling lines from the master ucf file. """
    if destination_dir is None:
        destination_dir = '/'.join([os.path.dirname(__file__), 'master_ucfs'])
    master_ucf_file = '/'.join([destination_dir, master_ucf_file])

    # all std_logic ports found could be clocks with associated timespecs
    std_logic_found = []
    ports_dict = _get_vhd_ports(vhd_file)
    new_ucf_file = _combine_file_names(vhd_file, master_ucf_file)
    
    # Iterate through ucf file to find items in port list.
    # Lines with ports in the port list get added to the new ucf file.
    with open(new_ucf_file, 'w') as new_ucf:
        with open(master_ucf_file, 'r') as master_ucf:
            for line in master_ucf:
                _check_ucf_port(ports_dict, std_logic_found, line, new_ucf)

    if len(ports_dict) > 0:
        logging.warning('ports not found in ucf file\n{}'.format(ports_dict))
