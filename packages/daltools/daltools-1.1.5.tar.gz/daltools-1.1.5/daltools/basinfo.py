#!/usr/bin/env python
"""
        Extract info from DALTON/SIRIUS restart file stored under label BASINFO
        """

import sys
import numpy
from fortran_binary import FortranBinary


class BasInfo:
    """
    Simple class for BASINFO data
    """

    label = "BASINFO"

    def __init__(self, name="SIRIUS.RST"):
        self.name = name
        with FortranBinary(name) as sirrst:
            sirrst.find(BasInfo.label)
            next(sirrst)
            self.nsym, = sirrst.readbuf(1, "i")
            self.nbas = numpy.array(sirrst.readbuf(8, "i"))[: self.nsym]
            self.norb = numpy.array(sirrst.readbuf(8, "i"))[: self.nsym]
            self.nrhf = numpy.array(sirrst.readbuf(8, "i"))[: self.nsym]
            self.ioprhf, = sirrst.readbuf(1, "i")

    def __repr__(self):
        """
        Print method for BasInfo objects
        """
        retstr = f"""\
NSYM   : {self.nsym:3d}
NBAS   : {printv(self.nbas)}
NORB   : {printv(self.norb)}
NRHF   : {printv(self.nrhf)}
IOPRHF : {self.ioprhf:3d}
"""
        return retstr

    @property
    def nbast(self):
        """
        Return total number of AO:s
        """
        return self.nbas[: self.nsym].sum()

    @property
    def norbt(self):
        """
        Return total number of MO
        """
        return self.norb[: self.nsym].sum()

    @property
    def ncmot(self):
        """
        Return number of MO coefficients
        """
        return sum(i*j for i, j in zip(self.nbas, self.norb))


def printv(v):
    return ('{:3d}'*len(v)).format(*v)


def main():
    """
        main routine
        """
    try:
        print(BasInfo(sys.argv[1]))
    except IndexError:
        print(f"Usage: {sys.argv[0]} [path]/SIRIUS.RST")
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
