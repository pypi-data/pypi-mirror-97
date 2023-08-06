#!/usr/bin/env python3
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
#
# Copyright (c) 2020 Authors and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the GNU Public Licence, v2 or any higher version
# SPDX-License-Identifier: GPL-2.0-or-later

import os
import subprocess
import tempfile

import numpy as np
import MDAnalysis as mda

from .base import SingleGroupAnalysisBase
from .. import tables
from ..lib import sfactor
from ..utils import check_compound, savetxt


def compute_form_factor(q, atom_type):
    """Calculates the form factor for the given element for given q (1/nm).
       Handles united atom types like CH4 etc ..."""
    element = tables.atomtypes[atom_type]

    if element == "CH1":
        form_factor = compute_form_factor(q, "C") + compute_form_factor(q, "H")
    elif element == "CH2":
        form_factor = compute_form_factor(
            q, "C") + 2 * compute_form_factor(q, "H")
    elif element == "CH3":
        form_factor = compute_form_factor(
            q, "C") + 3 * compute_form_factor(q, "H")
    elif element == "CH4":
        form_factor = compute_form_factor(
            q, "C") + 4 * compute_form_factor(q, "H")
    elif element == "NH1":
        form_factor = compute_form_factor(q, "N") + compute_form_factor(q, "H")
    elif element == "NH2":
        form_factor = compute_form_factor(
            q, "N") + 2 * compute_form_factor(q, "H")
    elif element == "NH3":
        form_factor = compute_form_factor(
            q, "N") + 3 * compute_form_factor(q, "H")
    else:
        form_factor = tables.CM_parameters[element].c
        # factor of 10 to convert from 1/nm to 1/Angstroms
        q2 = (q / (4 * np.pi * 10))**2
        for i in range(4):
            form_factor += tables.CM_parameters[element].a[i] * \
                np.exp(-tables.CM_parameters[element].b[i] * q2)

    return form_factor


class saxs(SingleGroupAnalysisBase):
    """Computes SAXS scattering intensities S(q) for all atom types from the given trajectory.

    The q vectors are binned
    by their length using a binwidth given by -dq. Using the -nobin option
    the raw intensity for each q_{i,j,k} vector
    is saved using. Note that this only works reliable using constant box vectors!
    The possible scattering vectors q can be restricted by a miminal and maximal angle with the z-axis.
    For 0 and 180 all possible vectors are taken into account.
    For the scattering factor the structure fator is multiplied by a atom type specific form factor
    based on Cromer-Mann parameters. By using the -sel option atoms can be selected for which the
    profile is calculated. The selection uses the MDAnalysis selection commands.

    :param outfreq (float): Number of frames after which the output is updated.
    :param output (str): Output filename
    :param noboindata (bool): Do not bin the data. Only works reliable for NVT!
    :param startq (float): Starting q (1/nm)
    :param endq (float): Ending q (1/nm)
    :param dq (float): binwidth (1/nm)
    :param mintheta (float): Minimal angle (°) between the q vectors and the z-axis.
    :param maxtheta (float): Maximal angle (°) between the q vectors and the z-axis.

    :returns (dict): * q: length of binned q-vectors
                     * q_indices: Miller indices of q-vector (only if noboindata==True)
                     * scat_factor: Scattering intensities
    """

    def __init__(self,
                 atomgroup,
                 outfreq=100,
                 output="sq.dat",
                 nobin=False,
                 startq=0,
                 endq=60,
                 dq=0.05,
                 mintheta=0,
                 maxtheta=180,
                 **kwargs):
        super().__init__(atomgroup, **kwargs)
        self.outfreq = outfreq
        self.output = output
        self.nobindata = nobin
        self.startq = startq
        self.endq = endq
        self.dq = dq
        self.mintheta = mintheta
        self.maxtheta = maxtheta

    def _configure_parser(self, parser):
        parser.add_argument('-dout', dest='outfreq')
        parser.add_argument('-sq', dest='output')
        parser.add_argument('-startq', dest='startq')
        parser.add_argument('-endq', dest='endq')
        parser.add_argument('-nobin', dest='nobindata')
        parser.add_argument('-dq', dest='dq', type=float, default=0.05, help='')
        parser.add_argument('-mintheta', dest='mintheta')
        parser.add_argument('-maxtheta', dest='maxtheta')

    def _prepare(self):

        self.mintheta = min(self.mintheta, self.maxtheta)
        self.maxtheta = max(self.mintheta, self.maxtheta)

        if self.mintheta < 0 and self._verbose:
            print("mintheta = {}° < 0°: Set mininmal angle to 0°.".format(
                self.mintheta))
            self.mintheta = 0
        if self.maxtheta > 180 and self._verbose:
            print("maxtheta = {}° > 180°: Set maximal angle to 180°.".format(
                self.maxtheta))
            self.maxtheta = np.pi

        self.mintheta *= np.pi / 180
        self.maxtheta *= np.pi / 180

        self.groups = []
        self.atom_types = []
        if self._verbose:
            print("\nMap the following atomtypes:")
        for atom_type in np.unique(self.atomgroup.types).astype(str):
            try:
                element = tables.atomtypes[atom_type]
            except KeyError:
                raise RuntimeError(
                    "No suitable element for '{0}' found. You can add '{0}' together with a suitable element to 'share/atomtypes.dat'."
                    .format(atom_type))
            if element == "DUM":
                continue
            self.groups.append(
                self.atomgroup.select_atoms("type {}*".format(atom_type)))
            self.atom_types.append(atom_type)

            if self._verbose:
                print("{:>14} --> {:>5}".format(atom_type, element))

        if self._verbose:
            print("")

        if self.nobindata:
            self.box = np.diag(
                mda.lib.mdamath.triclinic_vectors(
                    self._universe.dimensions)) / 10
            self.q_factor = 2 * np.pi / self.box
            self.maxn = np.ceil(self.endq / self.q_factor).astype(int)
            self.S_array = np.zeros(list(self.maxn) + [len(self.groups)])
        else:
            self.nbins = int(np.ceil((self.endq - self.startq) / self.dq))
            self.struct_factor = np.zeros([self.nbins, len(self.groups)])

    def _single_frame(self):
        # convert everything to cartesian coordinates
        box = np.diag(mda.lib.mdamath.triclinic_vectors(self._ts.dimensions))
        for i, t in enumerate(self.groups):
            positions = t.atoms.positions - box * \
                np.round(t.atoms.positions / box)  # minimum image

            q_ts, S_ts = sfactor.compute_structure_factor(
                np.double(positions / 10), np.double(box / 10), self.startq,
                self.endq, self.mintheta, self.maxtheta)

            S_ts *= compute_form_factor(q_ts, self.atom_types[i])**2

            if self.nobindata:
                self.S_array[:, :, :, i] += S_ts
            else:
                q_ts = q_ts.flatten()
                S_ts = S_ts.flatten()
                nonzeros = np.where(S_ts != 0)[0]

                q_ts = q_ts[nonzeros]
                S_ts = S_ts[nonzeros]

                bins = ((q_ts - self.startq) /
                        ((self.endq - self.startq) / self.nbins)).astype(int)
                struct_ts = np.histogram(bins,
                                         bins=np.arange(self.nbins + 1),
                                         weights=S_ts)[0]
                with np.errstate(divide='ignore', invalid='ignore'):
                    struct_ts /= np.histogram(bins,
                                              bins=np.arange(self.nbins + 1))[0]
                self.struct_factor[:, i] += np.nan_to_num(struct_ts)

        if self._save and self._frame_index % self.outfreq == 0 and self._frame_index > 0:
            self._calculate_results()
            self._save_results()

    def _calculate_results(self):
        self._index = self._frame_index + 1
        if self.nobindata:
            self.results["scat_factor"] = self.S_array.sum(axis=3)
            self.results["q_indices"] = np.array(
                list(np.ndindex(tuple(self.maxn))))
            self.results["q"] = np.linalg.norm(self.results["q_indices"] *
                                               self.q_factor[np.newaxis, :],
                                               axis=1)
        else:
            q = np.arange(self.startq, self.endq, self.dq) + 0.5 * self.dq
            nonzeros = np.where(self.struct_factor[:, 0] != 0)[0]
            scat_factor = self.struct_factor[nonzeros]

            self.results["q"] = q[nonzeros]
            self.results["scat_factor"] = scat_factor.sum(axis=1)

        self.results["scat_factor"] /= (self._index * self.atomgroup.n_atoms)

    def _save_results(self):
        """Saves the current profiles to a file."""

        if self.nobindata:
            out = np.hstack([
                self.results["q"][:, np.newaxis], self.results["q_indices"],
                self.results["scat_factor"].flatten()[:, np.newaxis]
            ])
            nonzeros = np.where(out[:, 4] != 0)[0]
            out = out[nonzeros]
            selfort = np.selfort(out[:, 0])
            out = out[selfort]

            boxinfo = "box_x = {0:.3f} nm, box_y = {1:.3f} nm, box_z = {2:.3f} nm\n".format(
                *self.box)
            savetxt(self.output,
                    out,
                    header=boxinfo +
                    "q (1/nm)\tq_i\t q_j \t q_k \tS(q) (arb. units)",
                    fmt='%.4e')
        else:
            savetxt(self.output,
                    np.vstack([self.results["q"],
                               self.results["scat_factor"]]).T,
                    header="q (1/nm)\tS(q) (arb. units)",
                    fmt='%.4e')


class debye(SingleGroupAnalysisBase):
    """Calculates scattering intensities using the debye equation.

       :param outfreq (float): Number of frames after which the output is updated.
       :param output (str): Output filename
       :param startq (float): Starting q (1/nm)
       :param endq (float): Ending q (1/nm)
       :param dq (float): binwidth (1/nm)
       :param sinc (bool): Apply sinc damping
       :param debyer (str): Path to the debyer executable

       :returns (dict): * q: length of binned q-vectors
                        * scat_factor: Scattering intensities
    """

    def __init__(self,
                 atomgroup,
                 sel="all",
                 outfreq=100,
                 output="sq.dat",
                 startq=0,
                 endq=60,
                 dq=0.05,
                 sinc=False,
                 debyer="debyer",
                 **kwargs):
        super().__init__(atomgroup, **kwargs)
        self.outfreq = outfreq
        self.output = output
        self.startq = startq
        self.endq = endq
        self.dq = dq
        self.sinc = sinc
        self.debyer = debyer

    def _configure_parser(self, parser):
        parser.add_argument('-dout', dest='outfreq')
        parser.add_argument('-sq', dest='output')
        parser.add_argument('-startq', dest='startq')
        parser.add_argument('-endq', dest='endq')
        parser.add_argument(
            '-dq',
            dest='dq',
        )
        parser.add_argument('-sinc', dest='sinc')
        parser.add_argument('-d', dest='debyer')

    def _prepare(self):

        # Convert 1/nm to 1/Å
        self.startq /= 10
        self.endq /= 10
        self.dq /= 10

        self.atomgroup = self.atomgroup.select_atoms(
            "not name DUM and not name MW")

        # Create an extra list for the atom names.
        # This is necessary since it is not possible to efficently add axtra atoms to
        # a MDAnalysis universe, necessary for the hydrogens in united atom forcefields.

        self.atom_names = self.atomgroup.n_atoms * ['']

        for i, atom_type in enumerate(self.atomgroup.types.astype(str)):
            element = tables.atomtypes[atom_type]

            # add hydrogens in the case of united atom forcefields
            if element in ["CH1", "CH2", "CH3", "CH4", "NH", "NH2", "NH3"]:
                self.atom_names[i] = element[0]
                for h in range(int(element[-1])):
                    self.atom_names.append("H")
                    # add a extra atom to universe. It got the wrong type but we only
                    # need the position, since we maintain our own atom type list.
                    self.atomgroup += self.atomgroup.atoms[i]
            else:
                self.atom_names[i] = element

        # create tmp directory for saving datafiles
        self._tmp = tempfile.mkdtemp()

        self._OUT = open(os.devnull, 'w')

        try:
            subprocess.call(self.debyer, stdout=self._OUT, stderr=self._OUT)
        except FileNotFoundError:
            raise RuntimeError("{}: command not found".format(self.debyer))

        if self._verbose:
            print("{} is the tempory directory for all files.\n".format(
                self._tmp))

    def _writeXYZ(self, filename):
        """Writes the positions of the current frame to the given xyz file"""
        write = mda.coordinates.XYZ.XYZWriter(filename,
                                              n_atoms=len(self.atom_names),
                                              atoms=self.atom_names)

        ts = self._trajectory.ts.copy_slice(self.atomgroup.indices)
        write.write_next_timestep(ts)
        write.close()

    def _single_frame(self):

        # convert coordinates in a rectengular box
        box = np.diag(mda.lib.mdamath.triclinic_vectors(self._ts.dimensions))
        self.atomgroup.positions = self.atomgroup.positions \
            - box * np.round(self.atomgroup.positions /
                             box)  # minimum image

        self._writeXYZ("{}/{}.xyz".format(self._tmp, self._frame_index))

        ref_q = 4 * np.pi / np.min(box)
        if ref_q > self.startq:
            self.startq = ref_q

        command = "-x -f {0} -t {1} -s {2} -o {3}/{4}.dat -a {5} -b {6} -c {7} -r {8} {3}/{4}.xyz".format(
            round(self.startq, 3), self.endq, self.dq, self._tmp,
            self._frame_index, box[0], box[1], box[2],
            np.min(box) / 2.001)

        command += self.sinc * " --sinc"

        subprocess.call("{} {}".format(self.debyer, command),
                        stdout=self._OUT,
                        stderr=self._OUT,
                        shell=True)

        if self._save and self._frame_index % self.outfreq == 0 and self._frame_index > 0:
            self._calculate_results()
            self._save_results()

    def _calculate_results(self):
        datfiles = [f for f in os.listdir(self._tmp) if f.endswith(".dat")]

        s_tmp = np.loadtxt("{}/{}".format(self._tmp, datfiles[0]))
        for f in datfiles[1:]:
            s_tmp = np.vstack([s_tmp, np.loadtxt("{}/{}".format(self._tmp, f))])

        nbins = int(np.ceil((self.endq - self.startq) / self.dq))
        q = np.arange(self.startq, self.endq, self.dq) + 0.5 * self.dq

        bins = ((s_tmp[:, 0] - self.startq) /
                ((self.endq - self.startq) / nbins)).astype(int)
        s_out = np.histogram(bins,
                             bins=np.arange(nbins + 1),
                             weights=s_tmp[:, 1])[0]

        nonzeros = np.where(s_out != 0)[0]

        self.results["q"] = 10 * q[nonzeros]
        self.results["scat_factor"] = s_out[nonzeros] / len(datfiles)

    def _conclude(self):
        for f in os.listdir(self._tmp):
            os.remove("{}/{}".format(self._tmp, f))

        os.rmdir(self._tmp)

    def _save_results(self):
        savetxt(self.output,
                np.vstack([self.results["q"], self.results["scat_factor"]]).T,
                header="q (1/A)\tS(q)_tot (arb. units)",
                fmt='%.8e')


class diporder(SingleGroupAnalysisBase):
    """Calculates dipolar order parameters including
    the projected polarization density P_0⋅ρ(z)⋅cos(θ[z]),
    the dipole orientation cos(θ[z]),
    the squared dipole orientation cos²(Θ[z]) and
    the number density ρ(z)

    :param binwidth (float): specify the binwidth [nm]
    :param dim (int): direction normal to the surface (x,y,z=0,1,2)
    :param output (str): Output filename
    :param outfreq (int): Default number of frames after which output files are
                         refreshed
    :param bsym (bool): symmetrize the profiles
    :param center (bool): Shift system by half a box length (useful for
                          membrane simulations
    :param com (bool): shift system such that the water COM is centered
    :param binmethod (str): binning method: center of Mass (COM), center of charge (COC)
                            or oxygen position (OXY).
                            Note: `OXY` only works for water oxygens with name `OW*`
    :param bpbc (bool): do not make broken molecules whole again
                       (only works if molecule is smaller than shortest box vector


   :returns (dict): * z: bins [nm]
                    * P0: P_0⋅cos(θ[z]) [e/nm²]
                    * cos_theta: cos(θ[z])
                    * cos_2_theta: cos²(Θ[z])
                    * rho: ρ(z) [1/nm³]
    """

    def __init__(self,
                 atomgroup,
                 binwidth=0.01,
                 dim=2,
                 output="diporder.dat",
                 outfreq=10000,
                 bsym=False,
                 center=False,
                 com=False,
                 binmethod='COM',
                 bpbc=True,
                 **kwargs):
        super().__init__(atomgroup, **kwargs)

        self.binwidth = binwidth
        self.dim = dim
        self.output = output
        self.outfreq = outfreq
        self.bsym = bsym
        self.center = center
        self.com = com
        self.binmethod = binmethod
        self.bpbc = bpbc

    def _configure_parser(self, parser):
        parser.add_argument('-dz', dest='binwidth')
        parser.add_argument('-d', dest='dim')
        parser.add_argument('-o', dest='output')
        parser.add_argument('-dout', dest="outfreq")
        parser.add_argument('-sym', dest='bsym')
        parser.add_argument('-shift', dest='center')
        parser.add_argument('-com', dest='com')
        parser.add_argument('-bin', dest='binmethod')
        parser.add_argument('-nopbcrepair', dest='bpbc')

    def _prepare(self):
        """Set things up before the analysis loop begins"""

        self.binmethod = self.binmethod.upper()
        if self.binmethod not in ["COM", "COC", "OXY"]:
            raise ValueError('Unknown binning method: {}'.format(
                self.binmethod))

        if self.binmethod == "OXY":
            self.oxy = self.atomgroup.select_atoms("name OW*")

        # Check if all residues are identical. Choose first residue as reference.
        residue_names = [ag.names for ag in self.atomgroup.split("residue")]
        for names in residue_names[1:]:
            if len(residue_names[0]) != len(names) and np.all(
                    residue_names[0] != names):
                raise ValueError("Not all residues are identical. Please adjust"
                                 "selection.")

        # Assume a threedimensional universe...
        self.xydims = np.roll(np.arange(3), -self.dim)[1:]
        self.nbins = int(
            np.ceil(self._universe.dimensions[self.dim] / 10 / self.binwidth))
        self.P0 = np.zeros(self.nbins)
        self.cos_theta = np.zeros(self.nbins)
        self.cos_2_theta = np.zeros(self.nbins)
        self.rho = np.zeros(self.nbins)
        self.av_box_length = 0

        # unit normal vector
        self.unit = np.zeros(3)
        self.unit[self.dim] += 1

    def _single_frame(self):

        if self.center:
            # shift membrane
            self._ts.positions[:, self.dim] += self._ts.dimensions[self.dim] / 2
            self._ts.positions[:, self.dim] %= self._ts.dimensions[self.dim]
        if self.com:
            # put water COM into center
            waterCOM = np.sum(self.atomgroup.atoms.positions[:, 2] *
                              self.atomgroup.atoms.masses
                             ) / self.atomgroup.atoms.masses.sum()
            self._ts.positions[:, self.dim] += self._ts.dimensions[
                self.dim] / 2 - waterCOM
            self._ts.positions[:, self.dim] %= self._ts.dimensions[self.dim]

        # Make molecules whole
        if self.bpbc:
            self.atomgroup.unwrap(compound=check_compound(self.atomgroup))

        dz_frame = self._ts.dimensions[self.dim] / self.nbins

        chargepos = self.atomgroup.positions * self.atomgroup.charges[:, np.
                                                                      newaxis]
        dipoles = self.atomgroup.accumulate(chargepos, 
                                            compound=check_compound(self.atomgroup))
        dipoles /= 10  # convert to e nm

        if self.binmethod == 'COM':
            # Calculate the centers of the objects ( i.e. Molecules )
            coms = self.atomgroup.center_of_mass(compound=check_compound(self.atomgroup))
            bins = ((coms[:, self.dim] % self._ts.dimensions[self.dim]) /
                    dz_frame).astype(int)
        elif self.binmethod == 'COC':
            cocs = self.atomgroup.center(weights=np.abs(self.atomgroup.charges),
                                         compound=check_compound(self.atomgroup))
            bins = ((cocs[:, self.dim] % self._ts.dimensions[self.dim]) /
                    dz_frame).astype(int)
        elif self.binmethod == 'OXY':
            bins = ((self.oxy.positions[:, self.dim] %
                     self._ts.dimensions[self.dim]) / dz_frame).astype(int)

        bincount = np.bincount(bins, minlength=self.nbins)
        A = np.prod(self._ts.dimensions[self.xydims])

        self.P0 += np.histogram(
            bins,
            bins=np.arange(self.nbins + 1),
            weights=np.dot(dipoles, self.unit))[0] / (A * dz_frame / 1e3)
        cos_theta = np.histogram(
            bins,
            bins=np.arange(self.nbins + 1),
            weights=np.dot(
                dipoles / np.linalg.norm(dipoles, axis=1)[:, np.newaxis],
                self.unit))[0]
        with np.errstate(divide='ignore', invalid='ignore'):
            self.cos_theta += np.nan_to_num(cos_theta / bincount)
            self.cos_2_theta += np.nan_to_num(cos_theta**2 / bincount)
        self.rho += bincount / (A * dz_frame / 1e3)  # convert to 1/nm^3

        self.av_box_length += self._ts.dimensions[self.dim] / 10

        if self._save and self._frame_index % self.outfreq == 0 and self._frame_index > 0:
            self._calculate_results()
            self._save_results()

    def _calculate_results(self):
        """Calculate the results.

        Called at the end of the run() method to before the _conclude function.
        Can also called during a run to update the results during processing."""
        self._index = self._frame_index + 1

        dz = self.av_box_length / (self._index * self.nbins)
        if self.center:
            self.results["z"] = np.linspace(
                -self.av_box_length / self._index / 2,
                self.av_box_length / self._index / 2,
                self.nbins,
                endpoint=False) + dz / 2
        else:
            self.results["z"] = np.linspace(
                0, self.av_box_length / self._index, self.nbins,
                endpoint=False) + dz / 2

        self.results["P0"] = self.P0 / self._frame_index
        self.results["cos_theta"] = self.cos_theta / self._frame_index
        self.results["cos_2_theta"] = self.cos_2_theta / self._frame_index
        self.results["rho"] = self.rho / self._frame_index

        if self.bsym:
            for i in range(len(self.results["z"]) - 1):
                self.results["z"][i +
                                  1] = .5 * (self.results["z"][i + 1] +
                                             self.results["z"][i + 1][-1::-1])
                self.results["diporder"][
                    i + 1] = .5 * (self.results["diporder"][i + 1] +
                                   self.results["diporder"][i + 1][-1::-1])

    def _save_results(self):
        """Saves results to a file.

        Called at the end of the run() method after _calculate_results and
        _conclude"""

        header = "z [nm]\t"
        header += "P_0*cos(Theta[z]) [e/nm^2]\t"
        header += "cos(theta(z))\t"
        header += "cos^2(theta(z))\t"
        header += "rho(z) [1/nm^3]"

        savetxt(self.output,
                np.vstack([
                    self.results["z"], self.results["P0"],
                    self.results["cos_theta"], self.results["cos_2_theta"],
                    self.results["rho"]
                ]).T,
                header=header)
