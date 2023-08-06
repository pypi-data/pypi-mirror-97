# Copyright 2010-2013, 2015-2017, 2019-2020 Richard Dymond (rjdymond@gmail.com)
#
# This file is part of SkoolKit.
#
# SkoolKit is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# SkoolKit is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# SkoolKit. If not, see <http://www.gnu.org/licenses/>.

import os.path
import argparse

from skoolkit import SkoolKitError, integer, read_bin_file, VERSION
from skoolkit.components import get_snapshot_reader

def _get_str(chars):
    return [ord(c) for c in chars]

def _get_word(word):
    return (word % 256, word // 256)

def _make_tap_block(data, header=False):
    if header:
        flag = 0
    else:
        flag = 255
    block = [0, 0, flag]
    block.extend(data)
    parity = 0
    for b in block:
        parity ^= b
    block.append(parity)
    block[:2] = _get_word(len(block) - 2)
    return block

def _get_header(title, length, start=None, line=None):
    data = _get_str(title[:10].ljust(10))   # Title padded with spaces
    data.extend(_get_word(length))          # Length of data block
    if line is None:
        data.insert(0, 3)                   # CODE block follows
        data.extend(_get_word(start))       # Start address
        data.extend((0, 0))                 # Unused
    else:
        data.insert(0, 0)                   # BASIC program follows
        data.extend(_get_word(line))        # RUN this line after LOADing
        data.extend(_get_word(length))      # Length of BASIC program only
    return _make_tap_block(data, True)

def _get_basic_loader(title, clear, start, scr):
    data = [0, 10]                          # Line 10
    if clear is None:
        start_addr = '"23296"'
        data.extend((16, 0))                # Length of line 10
    else:
        clear_addr = '"{}"'.format(clear)
        start_addr = '"{}"'.format(start)
        line_length = 12 + len(clear_addr) + len(start_addr)
        if scr:
            line_length += 20
        data.extend(_get_word(line_length)) # Length of line 10
        data.extend((253, 176))             # CLEAR VAL
        data.extend(_get_str(clear_addr))   # "address"
        data.append(58)                     # :
        if scr:
            poke_addr = _get_str('"23739"')
            data.extend((239, 34, 34, 170)) # LOAD ""SCREEN$
            data.append(58)                 # :
            data.extend((244, 176))         # POKE VAL
            data.extend(poke_addr)          # "23739"
            data.append(44)                 # ,
            data.extend((175, 34, 111, 34)) # CODE "o"
            data.append(58)                 # :
    data.extend((239, 34, 34, 175))         # LOAD ""CODE
    data.append(58)                         # :
    data.extend((249, 192, 176))            # RANDOMIZE USR VAL
    data.extend(_get_str(start_addr))       # "address"
    data.append(13)                         # ENTER

    return _get_header(title, len(data), line=10) + _make_tap_block(data)

def _get_data_loader(title, org, length, start, stack, scr):
    if scr:
        data = list(scr)
        data.extend((0,) * (6912 - len(data)))
    else:
        data = []
    address = 23296 - len(data)
    data.extend((221, 33))                  # LD IX,ORG
    data.extend(_get_word(org))
    data.append(17)                         # LD DE,LENGTH
    data.extend(_get_word(length))
    data.append(55)                         # SCF
    data.append(159)                        # SBC A,A
    data.append(49)                         # LD SP,STACK
    data.extend(_get_word(stack))
    data.append(1)                          # LD BC,START
    data.extend(_get_word(start))
    data.append(197)                        # PUSH BC
    data.extend((195, 86, 5))               # JP 1366

    return _get_header(title, len(data), address) + _make_tap_block(data)

def run(ram, clear, org, start, stack, tapfile, scr):
    title = os.path.basename(tapfile)
    if title.lower().endswith('.tap'):
        title = title[:-4]
    tap_data = _get_basic_loader(title, clear, start, scr)

    length = len(ram)
    if clear is None:
        stack_contents = _get_word(1343) + _get_word(start)
        stack_size = len(stack_contents)
        index = stack - org - stack_size
        if -stack_size < index < length:
            # If the main data block overwrites the stack, make sure that
            # SA/LD-RET (1343) and the start address are ready to be popped off
            # the stack when loading has finished
            ram = list(ram)
            for byte in stack_contents:
                if 0 <= index < length:
                    ram[index] = byte
                    index += 1
        tap_data.extend(_get_data_loader(title, org, length, start, stack, scr))
    else:
        if scr:
            tap_data.extend(_get_header(title, 6912, 16384))
            tap_data.extend(_make_tap_block(scr))
        tap_data.extend(_get_header(title, length, org))
    tap_data.extend(_make_tap_block(ram))

    with open(tapfile, 'wb') as f:
        f.write(bytearray(tap_data))

def main(args):
    parser = argparse.ArgumentParser(
        usage='bin2tap.py [options] FILE [file.tap]',
        description="Convert a binary (raw memory) file or a SNA, SZX or Z80 snapshot into a TAP file. "
                    "FILE may be a regular file, or '-' to read a binary file from standard input.",
        add_help=False
    )
    parser.add_argument('infile', help=argparse.SUPPRESS, nargs='?')
    parser.add_argument('outfile', help=argparse.SUPPRESS, nargs='?')
    group = parser.add_argument_group('Options')
    group.add_argument('-b', '--begin', dest='begin', metavar='BEGIN', type=integer,
                       help="Begin conversion at this address (default: ORG for a binary file, 16384 for a snapshot).")
    group.add_argument('-c', '--clear', dest='clear', metavar='N', type=integer,
                       help="Use a 'CLEAR N' command in the BASIC loader and leave the stack pointer alone.")
    group.add_argument('-e', '--end', dest='end', metavar='END', type=integer,
                       help="End conversion at this address.")
    group.add_argument('-o', '--org', dest='org', metavar='ORG', type=integer,
                       help="Set the origin address for a binary file (default: 65536 minus the length of FILE).")
    group.add_argument('-p', '--stack', dest='stack', metavar='STACK', type=integer,
                       help="Set the stack pointer (default: BEGIN).")
    group.add_argument('-s', '--start', dest='start', metavar='START', type=integer,
                       help="Set the start address to JP to (default: BEGIN).")
    group.add_argument('-S', '--screen', dest='screen', metavar='FILE',
                       help="Add a loading screen to the TAP file. FILE may be a snapshot or a 6912-byte SCR file.")
    group.add_argument('-V', '--version', action='version', version='SkoolKit {}'.format(VERSION),
                       help='Show SkoolKit version number and exit.')

    namespace, unknown_args = parser.parse_known_args(args)
    infile = namespace.infile
    if unknown_args or infile is None:
        parser.exit(2, parser.format_help())
    snapshot_reader = get_snapshot_reader()
    if snapshot_reader.can_read(infile):
        org = 0
        begin = namespace.begin or 16384
        end = namespace.end or 65536
        ram = snapshot_reader.get_snapshot(infile)[begin:end]
    else:
        ram = read_bin_file(infile, 49152)
        if not ram:
            raise SkoolKitError('{} is empty'.format(infile))
        org = namespace.org or 65536 - len(ram)
        begin = namespace.begin or org
        end = namespace.end or org + len(ram)
        ram = ram[begin - org:end - org]
    if not ram:
        raise SkoolKitError('Input is empty (ORG={}, BEGIN={}, END={})'.format(org, begin, end))
    clear = namespace.clear
    start = namespace.start or begin
    stack = namespace.stack or begin
    tapfile = namespace.outfile
    if tapfile is None:
        if infile.lower().endswith(('.bin', '.sna', '.szx', '.z80')):
            prefix = os.path.basename(infile)[:-4]
        elif infile == '-':
            prefix = 'program'
        else:
            prefix = os.path.basename(infile)
        tapfile = prefix + ".tap"
    scr = namespace.screen
    if scr is not None:
        if snapshot_reader.can_read(scr):
            scr = snapshot_reader.get_snapshot(scr)[16384:23296]
        else:
            scr = read_bin_file(scr, 6912)
    run(ram, clear, begin, start, stack, tapfile, scr)
