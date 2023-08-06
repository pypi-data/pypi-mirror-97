#!/usr/bin/env python
"""Module for reading data fro property integral file AOPROPER"""
import pathlib
import sys
import math
import numpy as np
from util import full
from fortran_binary import FortranBinary
from . import one, sirifc, dens, rspvec


def read(*args, **kwargs):
    """Read property integral"""
    propfile = kwargs.get("filename")
    if not propfile:
        tmpdir = pathlib.Path(kwargs.get("tmpdir", "/tmp"))
        propfile = tmpdir/"AOPROPER"

    unpack = kwargs.get("unpack", True)
    AOPROPER = FortranBinary(propfile)
    mat = {}
    for rec in AOPROPER:
        buf = rec.read(32, "c")
        # stars, data, symtype, label = (
        #      buf[:8], buf[8:16], buf[16:24], buf[24:32]
        #      )
        b"".join(buf[:8])
        symtype = b"".join(buf[16:24])
        blabel = b"".join(buf[24:32]).strip()

        bargs = (s.encode() for s in args)
        if blabel.strip() in bargs:
            label = blabel.decode()
            rec = next(AOPROPER)
            buffer_ = rec.read(len(rec) // 8, "d")
            if symtype == b"SQUARE  ":
                n = int(round(math.sqrt(len(buffer_))))
                mat[label] = full.init(buffer_).reshape((n, n))
            else:
                mat[label] = np.array(buffer_).view(full.triangular)
                mat[label].anti = symtype == b"ANTISYMM"
    if unpack:
        return tuple([mat[lab].unpack() for lab in args])
    else:
        return tuple([mat[lab] for lab in args])


def grad(*args, **kwargs):
    tmpdir = pathlib.Path(kwargs.get("tmpdir", "/tmp"))

    propmat = read(*args, **kwargs)

    AOONEINT = tmpdir/"AOONEINT"
    S = one.read(label="OVERLAP", filename=AOONEINT).unpack().unblock()

    SIRIFC = tmpdir/"SIRIFC"
    ifc = sirifc.sirifc(SIRIFC)
    Da, Db = dens.Dab(ifc_=ifc)
    cmo = ifc.cmo.unblock()

    G = (
        rspvec.tovec(
            cmo.T @ (S @ Da @ P.T - P.T @ Da @ S) @ cmo
            + cmo.T @ (S @ Db @ P.T - P.T @ Db @ S) @ cmo,
            ifc,
        )
        for P in propmat
    )

    return tuple(G)


def main():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("label", help="Property label")
    parser.add_argument("-t", "--tmpdir", help="Work directory")
    parser.add_argument("--packed", action="store_true", help="Work directory")
    parser.add_argument("-o", "--savetxt", dest="savetxt")
    args = parser.parse_args()

    kwargs = {"tmpdir": args.tmpdir, "unpack": not args.packed}
    prop, = read(args.label, **kwargs)
    print(str(prop))
    if args.savetxt:
        np.savetxt(args.savetxt, prop)


if __name__ == "__main__":  # pragma no cover
    sys.exit(main())
