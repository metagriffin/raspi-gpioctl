# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.github@metagriffin.net>
# date: 2014/09/24
# copy: (C) Copyright 2014-EOT metagriffin -- see LICENSE.txt
#------------------------------------------------------------------------------
# This software is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#------------------------------------------------------------------------------

import RPi.GPIO as GPIO
import sys
import time
import argparse

truthy = frozenset(('1', 'on', 'true', 't', 'yes'))
falsy  = frozenset(('0', 'off', 'false', 'f', 'no'))

#------------------------------------------------------------------------------
def boolstr(s):
  v = s.lower()
  if v in truthy:
    return True
  if v in falsy:
    return False
  raise argparse.ArgumentTypeError('invalid boolean value: "{}"'.format(s))

function_map = {
  GPIO.IN         : 'input',
  GPIO.OUT        : 'output',
  GPIO.SPI        : 'SPI',
  GPIO.I2C        : 'I2C',
  GPIO.HARD_PWM   : 'PWM',
  GPIO.SERIAL     : 'serial',
  GPIO.UNKNOWN   : 'unknown',
}

#------------------------------------------------------------------------------
def main(args=None):
  cli = argparse.ArgumentParser()
  cli.add_argument(
    '-s', '--status',
    dest='exitcode', default=False, action='store_true',
    help='use the exit status to indicate pin state (with no output)')
  cli.add_argument(
    metavar='PIN',
    dest='pin', type=int,
    help='the GPIO pin number to read from or write to')
  cli.add_argument(
    metavar='STATE', nargs='?',
    dest='state', default=None, type=boolstr,
    help='if specified, the boolean state to write to PIN')
  options = cli.parse_args(args)

  # todo: figure out how to leave the state of a pin permanent...
  # (then i can re-enable the ".cleanup")
  GPIO.setwarnings(False)

  GPIO.setmode(GPIO.BCM)
  curfunc = GPIO.gpio_function(options.pin)

  try:

    if options.state is None:
      GPIO.setup(options.pin, curfunc)
      if options.exitcode:
        return GPIO.input(options.pin)
      print 'function:',function_map.get(curfunc, '[invalid]')
      print 'state:',GPIO.input(options.pin)
      return 0

    GPIO.setup(options.pin, GPIO.OUT)
    GPIO.output(options.pin, options.state)
    return 0

  finally:
    pass
    # todo: re-enable this when pin state is permanent...
    # GPIO.cleanup()

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
