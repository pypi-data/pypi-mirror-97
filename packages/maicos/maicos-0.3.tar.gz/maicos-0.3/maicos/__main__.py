#!/usr/bin/env python3
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
#
# Copyright (c) 2019 Authors and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the GNU Public Licence, v2 or any higher version
# SPDX-License-Identifier: GPL-2.0-or-later

import argparse
import os
import sys
import traceback
import warnings

from threadpoolctl import threadpool_limits
import MDAnalysis as mda
import maicos

from . import __version__
from . import __all__ as available_modules
from .utils import get_cli_input
from .arg_completion import complete_parser

# Try to use IPython shell for debug
try:
    import IPython
    use_IPython = True
except ImportError:
    import code
    use_IPython = False


class bcolors:
    warning = '\033[93m'
    fail = '\033[91m'
    endc = '\033[0m'


def _warning(message,
             category=UserWarning,
             filename='',
             lineno=-1,
             file=None,
             line=None):
    print("{}Warning: {}{}".format(bcolors.warning, message, bcolors.endc))


warnings.showwarning = _warning


def parse_args():
    """Parse the command line arguments."""

    if '--bash_completion' in sys.argv:
        print(
            os.path.join(os.path.dirname(__file__),
                         "share/maicos-completion.bash"))
        sys.exit(0)

    parser = argparse.ArgumentParser(
        description="Analyse molecular dynamics simulations of "
        "interfacial and confined systems.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("program",
                        type=str,
                        help="Program to start",
                        choices=available_modules)
    parser.add_argument('--debug',
                        action='store_true',
                        help="Run with debug options. Will start an "
                        "interactive Python interpreter at the end of "
                        "the program.")
    parser.add_argument('--version',
                        action='version',
                        version="maicos {}".format(__version__))

    try:
        sys.argv.remove("--debug")
        debug = True
    except ValueError:
        debug = False
        warnings.filterwarnings("ignore")

    try:
        if sys.argv[1] in available_modules:
            selected_module = getattr(maicos, sys.argv[1])
        else:
            parser.parse_args()
    except IndexError:
        parser.parse_args()

    print('\n{}\n'.format(get_cli_input()))
    parser = argparse.ArgumentParser(
        prog="maicos " + sys.argv[1],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-s",
                        dest="topology",
                        type=str,
                        default="topol.tpr",
                        help="The topolgy file. "
                        "The FORMATs {} are implemented in MDAnalysis."
                        "".format(", ".join(mda._PARSERS.keys())))
    parser.add_argument("-top",
                        dest="topology_format",
                        type=str,
                        default=None,
                        help="Override automatic topology type detection. "
                        "See topology for implemented formats")
    parser.add_argument("-f",
                        dest="trajectory",
                        type=str,
                        default=None,
                        nargs="+",
                        help="A single or multiple trajectory files. "
                        "The FORMATs {} are implemented in MDAnalysis."
                        "".format(", ".join(mda._READERS.keys())))
    parser.add_argument("-traj",
                        dest="trajectory_format",
                        type=str,
                        default=None,
                        help="Override automatic trajectory type detection. "
                        "See trajectory for implemented formats")
    parser.add_argument("-atom_style",
                        dest="atom_style",
                        type=str,
                        default=None,
                        help="Manually set the atom_style information"
                        "(currently only LAMMPS parser)."
                        "E.g. atom_style='id type x y z'.")
    parser.add_argument("-b",
                        dest="begin",
                        type=float,
                        default=0,
                        help="start time (ps) for evaluation.")
    parser.add_argument("-e",
                        dest="end",
                        type=float,
                        default=None,
                        help="end time (ps) for evaluation.")
    parser.add_argument("-dt",
                        dest="dt",
                        type=float,
                        default=0,
                        help="time step (ps) to read analysis frame. "
                        "If `0` take all frames")
    parser.add_argument("-box",
                        dest="box",
                        type=float,
                        default=None,
                        nargs="+",
                        help="Sets the box dimensions x y z [alpha beta gamma]"
                        "(Å). If 'None' dimensions from the trajectory "
                        "will be used.")
    parser.add_argument("-nt",
                        dest="num_threads",
                        type=int,
                        default=0,
                        help="Total number of threads to start (0 is guess)")

    try:
        _configure_parser = getattr(selected_module, "_configure_parser")
        _allow_multiple_atomgroups = getattr(selected_module,
                                             "_allow_multiple_atomgroups")

        if _allow_multiple_atomgroups:
            parser.add_argument(
                '-sel',
                dest='selection',
                type=str,
                default=['all'],
                nargs='+',
                help='Atomgroup(s) for which to perform the analysis.',
            )
        else:
            parser.add_argument(
                '-sel',
                dest='selection',
                type=str,
                default='all',
                help='Atomgroup for which to perform the analysis.',
            )

        _configure_parser(selected_module, parser)
        complete_parser(parser, selected_module)
        args = parser.parse_args(sys.argv[2:])
        args.debug = debug
        args._allow_multiple_atomgroups = _allow_multiple_atomgroups
        args.selected_module = selected_module
    except Exception as e:
        if debug:
            traceback.print_exc()
        else:
            print("{}Error: {}{}".format(bcolors.fail, e, bcolors.endc))

    return args


def main(args, verbose=True):
    """The maicos main function including universe initialization and module running."""

    try:
        with threadpool_limits(limits=args.num_threads):
            if verbose:
                print("Loading trajectory... ", end="")
                sys.stdout.flush()

            # prepare kwargs dictionary for other optional arguments
            ukwargs = {}
            if args.atom_style is not None:
                ukwargs['atom_style'] = args.atom_style

            u = mda.Universe(args.topology,
                             topology_format=args.topology_format,
                             **ukwargs)
            if args.trajectory is not None:
                u.load_new(args.trajectory, format=args.trajectory_format)
            if verbose:
                print("Done!\n")

            if args.box is not None:
                if len(args.box) == 6:
                    u.dimensions = args.box
                if len(args.box) == 3:
                    u.dimensions[:3] = args.box
                    u.dimensions[3:] = [90, 90, 90]
                else:
                    raise IndexError(
                        "The boxdimensions must contain 3 entries for "
                        "the box length and possibly 3 more for the angles.")
            if verbose:
                print("Performing analysis for the following group(s):")

            if type(args.selection) is str:
                args.selection = [args.selection]

            atomgroups = []
            for i, gr in enumerate(args.selection):
                sel = u.select_atoms(gr)
                if verbose:
                    print("{:>15}: {:>10} atoms".format(gr, sel.n_atoms))
                if sel.n_atoms > 0:
                    atomgroups.append(sel)
                else:
                    with warnings.catch_warnings():
                        warnings.simplefilter('always')
                        warnings.warn(
                            "Selection '{}' not taken for profile, "
                            "since it does not contain any atoms.".format(gr))

            if len(atomgroups) == 0:
                raise ValueError("No atoms found in selection."
                                 "Please adjust group selection.")

            if not args._allow_multiple_atomgroups:
                atomgroups = atomgroups[0]

            ana_obj = args.selected_module(atomgroups, verbose=True, save=True)
            # Insert parser arguments into ana_obj
            for var in vars(args):
                if var not in [
                        "topology", "topology_format", "trajectory",
                        "trajectory_format", "atom_style", "begin", "end", "dt",
                        "box", "selection"
                ]:
                    vars(ana_obj)[var] = vars(args)[var]

            ana_obj.run(begin=args.begin, end=args.end, dt=args.dt)

    except Exception as e:
        if args.debug:
            traceback.print_exc()
        else:
            sys.exit("{}Error: {}{}".format(bcolors.fail, e, bcolors.endc))

    if args.debug:
        # Inject local variables into global namespace for debugging.
        for key, value in locals().items():
            globals()[key] = value

        banner = "\nStarting interactive Python interpreter for debug.⁠"
        banner += "\nYou can access all your analysis class atrributes via"
        banner += " ana_obj.<attributes>."
        if use_IPython:
            IPython.embed(banner1=banner)
        else:
            code.interact(banner=banner, local=dict(globals(), **locals()))

    # Only return if ana_obj exists
    if "ana_obj" in locals():
        return ana_obj


def entry_point():
    args = parse_args()
    main(args)


if __name__ == "__main__":
    entry_point()
