#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 16:00:49 2018

@author: sebastianw
"""

import argparse
from argparse import ArgumentParser

APPNAME = "intelmqctl"
VERSION = '1.1.0a1'
DESCRIPTION = """
description: intelmqctl is the tool to control intelmq system.

Outputs are logged to /opt/intelmq/var/log/intelmqctl"""
EPILOG = '''
intelmqctl [start|stop|restart|status|reload] bot-id
intelmqctl [start|stop|restart|status|reload]
intelmqctl list [bots|queues]
intelmqctl log bot-id [number-of-lines [log-level]]
intelmqctl run bot-id message [get|pop|send]
intelmqctl run bot-id process [--msg|--dryrun]
intelmqctl run bot-id console
intelmqctl clear queue-id
intelmqctl check

Starting a bot:
intelmqctl start bot-id
Stopping a bot:
intelmqctl stop bot-id
Restarting a bot:
intelmqctl restart bot-id
Get status of a bot:
intelmqctl status bot-id

Run a bot directly for debugging purpose and temporarily leverage the logging level to DEBUG:
intelmqctl run bot-id
Get a pdb (or ipdb if installed) live console.
intelmqctl run bot-id console
See the message that waits in the input queue.
intelmqctl run bot-id message get
See additional help for further explanation.
intelmqctl run bot-id --help

Starting the botnet (all bots):
intelmqctl start
etc.

Get a list of all configured bots:
intelmqctl list bots
If -q is given, only the IDs of enabled bots are listed line by line.

Get a list of all queues:
intelmqctl list queues
If -q is given, only queues with more than one item are listed.

Clear a queue:
intelmqctl clear queue-id

Get logs of a bot:
intelmqctl log bot-id number-of-lines log-level
Reads the last lines from bot log.
Log level should be one of DEBUG, INFO, ERROR or CRITICAL.
Default is INFO. Number of lines defaults to 10, -1 gives all. Result
can be longer due to our logging format!

Outputs are additionally logged to /opt/intelmq/var/log/intelmqctl'''
RETURN_TYPES = ['text', 'json']
LOG_LEVEL = {
    'DEBUG': 0,
    'INFO': 1,
    'WARNING': 2,
    'ERROR': 3,
    'CRITICAL': 4,
}


parser = argparse.ArgumentParser(
    prog=APPNAME,
    description=DESCRIPTION,
    epilog=EPILOG,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

parser.add_argument('-v', '--version',
                    action='version', version=VERSION)
parser.add_argument('--type', '-t', choices=RETURN_TYPES,
                    default=RETURN_TYPES[0],
                    help='choose if it should return regular text '
                         'or other machine-readable')

parser.add_argument('--quiet', '-q', action='store_const',
                    help='Quiet mode, useful for reloads initiated '
                         'scripts like logrotate',
                    const=True)

subparsers = parser.add_subparsers(title='subcommands')

parser_list = subparsers.add_parser('list', help='Listing bots or queues')
parser_list.add_argument('kind', choices=['bots', 'queues'])
parser_list.add_argument('--quiet', '-q', action='store_const',
                         help='Only list non-empty queues '
                              'or the IDs of enabled bots.',
                         const=True)

parser_clear = subparsers.add_parser('clear', help='Clear a queue')
parser_clear.add_argument('queue', help='queue name')

parser_log = subparsers.add_parser('log', help='Get last log lines of a bot')
parser_log.add_argument('bot_id', help='bot id')
parser_log.add_argument('number_of_lines', help='number of lines',
                        default=10, type=int, nargs='?')
parser_log.add_argument('log_level', help='logging level',
                        choices=LOG_LEVEL.keys(), default='INFO', nargs='?')

parser_run = subparsers.add_parser('run', help='Run a bot interactively')
parser_run.add_argument('bot_id')
parser_run_subparsers = parser_run.add_subparsers(title='run-subcommands')

parser_run_console = parser_run_subparsers.add_parser('console', help='Get a ipdb live console.')
parser_run_console.add_argument('console_type', nargs='?',
                                help='You may specify which console should be run. Default is ipdb (if installed)'
                                ' or pudb (if installed) or pdb but you may want to use another one.')
parser_run_console.set_defaults(run_subcommand="console")

parser_run_message = parser_run_subparsers.add_parser('message',
                                                      help='Debug bot\'s pipelines. Get the message in the'
                                                      ' input pipeline, pop it (cut it) and display it, or'
                                                      ' send the message directly to bot\'s output pipeline.')
parser_run_message.add_argument('message_action_kind', choices=["get", "pop", "send"])
parser_run_message.add_argument('msg', nargs='?', help='If send was chosen, put here the message in JSON.')
parser_run_message.set_defaults(run_subcommand="message")

parser_run_process = parser_run_subparsers.add_parser('process', help='Single run of bot\'s process() method.')
parser_run_process.add_argument('--dryrun', '-d', action='store_true',
                                help='Never really pop the message from the input pipeline '
                                     'nor send to output pipeline.')
parser_run_process.add_argument('--msg', '-m',
                                help='Trick the bot to process this JSON '
                                     'instead of the Message in its pipeline.')
parser_run_process.set_defaults(run_subcommand="process")

parser_check = subparsers.add_parser('check',
                                     help='Check installation and configuration')
parser_check.add_argument('--quiet', '-q', action='store_const',
                          help='Only print warnings and errors.',
                          const=True)

parser_help = subparsers.add_parser('help',
                                    help='Show the help')
parser_help.set_defaults(func=parser.print_help)

parser_start = subparsers.add_parser('start', help='Start a bot or botnet')
parser_start.add_argument('bot_id', nargs='?')

parser_stop = subparsers.add_parser('stop', help='Stop a bot or botnet')
parser_stop.add_argument('bot_id', nargs='?')

parser_restart = subparsers.add_parser('restart', help='Restart a bot or botnet')
parser_restart.add_argument('bot_id', nargs='?')

parser_reload = subparsers.add_parser('reload', help='Reload a bot or botnet')
parser_reload.add_argument('bot_id', nargs='?')

parser_status = subparsers.add_parser('status', help='Status of a bot or botnet')
parser_status.add_argument('bot_id', nargs='?')

parser_status = subparsers.add_parser('enable', help='Enable a bot')
parser_status.add_argument('bot_id')

parser_status = subparsers.add_parser('disable', help='Disable a bot')
parser_status.add_argument('bot_id')
