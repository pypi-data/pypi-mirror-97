#!/usr/bin/env python
"""
Linear response module
"""

import sys
import pathlib

from . import prop, sirifc, dens, rspvec, one


class LinearResponseReader:
    def __init__(self, A, B, w=0, tmpdir='/tmp'):
        self.A = A
        self.B = B
        self.w = w
        self.tmpdir = pathlib.Path(tmpdir)
        self.sirifc = sirifc.SirIfc(self.tmpdir/"SIRIFC")
        self.propfile = self.tmpdir/"AOPROPER"
        self.absorption = False

    def get_property(self):
        self.a, = prop.read(self.A, filename=self.propfile, unpack=True)

    def get_density(self):
        self.dkb = Dk(
            self.B, freqs=(self.w,), ifc=self.sirifc, tmpdir=self.tmpdir,
            absorption=self.absorption
        )

    def evaluate(self):
        return self.a & self.dkb[(self.B, self.w)]


class CLinearResponseReader(LinearResponseReader):

    def __init__(self, A, B, w=0, tmpdir='/tmp'):
        super().__init__(A, B, w, tmpdir)
        self.absorption = True

    def evaluate(self):
        return (
            self.a & self.dkb[0][(self.B, self.w)],
            self.a & self.dkb[1][(self.B, self.w)]
        )


def LR(A, B, w=0.0, tmpdir="/tmp", absorption=False):
    """
    Calculate the linear response function <<A;B>> from response vector
    on RSPVEC for B, as <[kB,A]>
    """
    if absorption:
        reader = CLinearResponseReader(A, B, w, tmpdir)
    else:
        reader = LinearResponseReader(A, B, w, tmpdir)

    reader.get_property()
    reader.get_density()

    return reader.evaluate()


def Dk(*args, **kwargs):
    """Calculate the density transformed with response vector kb
    on RSPVEC for B, as d S kb - kb S d"""
    freqs = kwargs.get("freqs", (0.0,))
    ifc = kwargs.get("ifc", None)
    tmpdir = pathlib.Path(kwargs.get("tmpdir", "/tmp"))
    absorption = kwargs.get("absorption", False)
    #
    # Read interface data from SIRIFC if not provided
    #
    if ifc is None:
        ifc = sirifc.sirifc(name=tmpdir/"SIRIFC")
    cmo = ifc.cmo
    #
    # Get densities in AO basis
    #
    dc, do = dens.ifc(tmpdir/"SIRIFC", ifc)
    d = dc + do
    #
    # Get response vector (no symmetry)
    #

    if absorption:
        vecfile = tmpdir/"ABSVECS"
    else:
        vecfile = tmpdir/"RSPVEC"

    NB = rspvec.read(*args, freqs=freqs, propfile=vecfile)

    #
    # Vector to matrix
    #
    cmo = ifc.cmo.unblock()
    S = one.read(filename=tmpdir/"AOONEINT").unpack().unblock()
    # (D S kb - kb S D)
    dS = d @ S

    if absorption:
        ReNB = {lw: NB[lw][: len(NB[lw]) // 2] for lw in NB}
        Rekb = {
            lw: cmo @ rspvec.tomat(ReNB[lw], ifc, tmpdir=tmpdir).T @ cmo.T
            for lw in NB
        }

        ImNB = {lw: NB[lw][len(NB[lw]) // 2:] for lw in NB}
        Imkb = {
            lw: cmo @ rspvec.tomat(ImNB[lw], ifc, tmpdir=tmpdir).T @ cmo.T
            for lw in NB
        }
        dkb = (
            {lw: dS @ Rekb[lw] - Rekb[lw] @ dS.T for lw in Rekb},
            {lw: dS @ Imkb[lw] - Imkb[lw] @ dS.T for lw in Imkb},
        )
    else:
        kb = {
            lw: cmo @ rspvec.tomat(NB[lw], ifc, tmpdir=tmpdir).T @ cmo.T
            for lw in NB
        }
        dkb = {lw: dS @ kb[lw] - kb[lw] @ dS.T for lw in kb}
    return dkb


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("A")
    parser.add_argument("B")
    parser.add_argument(
        "-t", "--tmpdir", dest="tmpdir", default="/tmp",
        help="scratch directory [/tmp]"
    )
    args = parser.parse_args()

    print("{:.6f}".format(LR(args.A, args.B, tmpdir=args.tmpdir)))


if __name__ == "__main__":  # pragma no cover
    sys.exit(main())
