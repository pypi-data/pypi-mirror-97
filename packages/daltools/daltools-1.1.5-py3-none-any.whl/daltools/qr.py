#!/usr/bin/env python
"""Quadratic response module"""

from pathlib import Path
import sys
from .sirifc import sirifc
from .dens import ifc as dens_ifc
from .prop import read as prop_read
from .rspvec import read as rspvec_read
from .rspvec import tomat as rspvec_tomat
from .one import read as one_read


def QR(A, B, C, wb=0.0, wc=0.0, tmpdir="/tmp", **kwargs):
    """Calculate the linear response function <<A;B>> from response vector
    on RSPVEC for B, as <[kB,A]>"""
    propfile = Path(tmpdir)/"AOPROPER"
    a, = prop_read(A, filename=propfile, unpack=True)
    BC = B.ljust(8) + C.ljust(8)
    dBC = D2k(BC, bcfreqs=((wb, wc),), tmpdir=tmpdir, **kwargs)
    return a & dBC[BC, wb, wc]


def D2k(*args, **kwargs):
    """Calculated second-order density matrix for quadratic response"""

    bclabs = args

    bcfreqs = kwargs.get("bcfreqs", ((0.0, 0.0),))
    tmpdir = Path(kwargs.get("tmpdir", "/tmp"))
    ifc = kwargs.get("ifc", None)

    SIRIFC = tmpdir/"SIRIFC"
    RSPVEC = tmpdir/"RSPVEC"
    AOONEINT = tmpdir/"AOONEINT"
    #
    # Read interface data from SIRIFC if not provided
    #
    if ifc is None:
        ifc = sirifc(name=SIRIFC)
    #
    # Get densities in AO basis
    #
    dc, do = dens_ifc(SIRIFC, ifc)
    d = dc + do
    #
    # Get linear response vector (no symmetry)
    #
    # kzywop = 2 * ifc.nwopt

    bfreqs = {wbc[0] for wbc in bcfreqs}
    cfreqs = {wbc[1] for wbc in bcfreqs}
    blabs = {bclab[:8] for bclab in bclabs}
    clabs = {bclab[8:] for bclab in bclabs}
    bkeys = [(_l, w) for _l in blabs for w in bfreqs]
    ckeys = [(_l, w) for _l in clabs for w in cfreqs]
    bckeys = [(_l, wb, wc) for _l in bclabs for wb in bfreqs for wc in cfreqs]

    NB = rspvec_read(*blabs, freqs=bfreqs, propfile=RSPVEC)
    NC = rspvec_read(*clabs, freqs=cfreqs, propfile=RSPVEC)
    NBC = rspvec_read(*bclabs, bfreqs=bfreqs, cfreqs=cfreqs, propfile=RSPVEC)
    # transform density over unique pairs
    cmo = ifc.cmo.unblock()
    kb = {
        lw: cmo @ rspvec_tomat(NB[lw], ifc, tmpdir=tmpdir).T @ cmo.T
        for lw in bkeys
    }
    kc = {
        lw: cmo @ rspvec_tomat(NC[lw], ifc, tmpdir=tmpdir).T @ cmo.T
        for lw in ckeys
    }

    kbc = {
        lw: cmo @ rspvec_tomat(NBC[lw], ifc, tmpdir=tmpdir).T @ cmo.T
        for lw in bckeys
    }

    S = one_read(filename=AOONEINT).unpack().unblock()
    Sd = S @ d
    dkb = {lw: kb[lw] @ Sd - Sd.T @ kb[lw] for lw in bkeys}
    dkc = {lw: kc[lw] @ Sd - Sd.T @ kc[lw] for lw in ckeys}
    dkbc = {lw: kbc[lw] @ Sd - Sd.T @ kbc[lw] for lw in bckeys}

    for lbc, wb, wc in bckeys:
        lb, lc = lbc[:8], lbc[8:]
        _dkbc = dkbc[(lbc, wb, wc)]
        _dkb = dkb[(lb, wb)]
        _dkc = dkc[(lc, wc)]
        _kb = kb[(lb, wb)]
        _kc = kc[(lc, wc)]

        _da2bc = 0.5 * (
            _kc @ S @ _dkb - _dkb @ S @ _kc + _kb @ S @ _dkc - _dkc @ S @ _kb
        )

        if "a2test" in kwargs:
            _dkbc.clear()
        _dkbc += _da2bc

        # Symmetrize keys
        dkbc.update({(lbc[8:] + lbc[:8], wc, wb): _dkbc})

    return dkbc


def main():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("A")
    parser.add_argument("B")
    parser.add_argument("C")
    parser.add_argument(
        "-t", "--tmpdir", dest="tmpdir", default="/tmp",
        help="scratch directory [/tmp]"
    )
    args = parser.parse_args()

    print("%12.5g" % QR(args.A, args.B, args.C, tmpdir=args.tmpdir))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
