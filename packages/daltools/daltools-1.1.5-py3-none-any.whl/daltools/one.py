#!/usr/bin/env python
"""
Module for reading data from Dalton one-electron integral file AOONEINT
"""
import struct
import numpy as np
from util import full, blocked
from fortran_binary import FortranBinary


def readhead(filename="AOONEINT"):
    """Read data in header of AOONEINT"""
    aooneint = FortranBinary(filename)
    rec = next(aooneint)
    if len(aooneint.data) == 144:
        #
        # Newer versions: title in own record
        #
        title = aooneint.data.decode()
        #
        # Next record contains MAXREP...
        #
        rec = next(aooneint)
    else:
        #
        # Older versions: not supported
        #
        raise RuntimeError
    #
    # Buffer should now contains MAXREP data
    #

    FLOAT = "d"
    INT = _get_integer_format(rec)

    nsym = rec.read(1, INT)[0]
    naos = rec.read(nsym, INT)
    potnuc = rec.read(1, FLOAT)[0]
    import collections

    unlabeled = collections.OrderedDict(
        [
            ("ttitle", title),
            ("nsym", nsym),
            ("naos", naos),
            ("potnuc", potnuc),
            ("int_fmt", INT),
            ("float_fmt", FLOAT),
        ]
    )
    aooneint.close()
    return unlabeled


def _get_integer_format(header_record):
    """Determine integer format from first record of AOONEINT"""
    # from herrdn.F:
    #  WRITE (LUONEL) MAXREP+1,(NAOS(I),I=1,MAXREP+1), POTNUC,
    # &              (0.D0,I=1,2) ! so record is minimum 32 bytes
    floatsize = 8
    dimensions = np.array(
        [
            [intsize * (nsym + 1) + 3 * floatsize for intsize in [4, 8]]
            for nsym in [1, 2, 4, 8]
        ]
    )
    if len(header_record) in dimensions[:, 0]:
        integer_format = "i"
    elif len(header_record) in dimensions[:, 1]:
        integer_format = "q"
    else:
        raise RuntimeError("Unknown binary format in AOONEINT")

    return integer_format


def readisordk(filename="AOONEINT"):
    """Read data under label ISORDK in AOONEINT"""

    header = readhead(filename)
    INT = header["int_fmt"]
    FLOAT = header["float_fmt"]

    aooneint = FortranBinary(filename)
    aooneint.find("ISORDK")
    next(aooneint)
    next(aooneint)
    sizeofi = struct.calcsize(INT)
    sizeofd = struct.calcsize(FLOAT)
    mxcent_ = (len(aooneint.data) - sizeofi) // (4 * sizeofd)
    chrn_ = aooneint.readbuf(mxcent_, FLOAT)
    nucdep = aooneint.readbuf(1, INT)[0]
    cooo_ = aooneint.readbuf(3 * mxcent_, FLOAT)
    isordk_ = {
        # "table":table1,
        "chrn": chrn_,
        "nucdep": nucdep,
        "cooo": cooo_,
    }
    aooneint.close()
    return isordk_


def readscfinp(filename="AOONEINT"):
    """Read data under labl SCFINP in AOONEINT"""

    header = readhead(filename)
    INT = header["int_fmt"]
    FLOAT = header["float_fmt"]

    aooneint = FortranBinary(filename)
    aooneint.find("SCFINP")
    import collections

    scfinp_ = collections.OrderedDict()
    next(aooneint)
    title = aooneint.data.decode()
    next(aooneint)
    scfinp_["ttitle"] = title
    nsym = aooneint.readbuf(1, INT)[0]
    scfinp_["nsym"] = nsym
    scfinp_["naos"] = aooneint.readbuf(nsym, INT)
    scfinp_["potnuc"] = aooneint.readbuf(1, FLOAT)[0]
    kmax = aooneint.readbuf(1, INT)[0]
    scfinp_["kmax"] = kmax
    scfinp_["ncent"] = aooneint.readbuf(kmax, INT)
    nbasis = aooneint.readbuf(1, INT)[0]
    scfinp_["nbasis"] = nbasis
    scfinp_["jtran"] = aooneint.readbuf(nbasis, INT)
    scfinp_["itran"] = aooneint.readbuf(8 * nbasis, INT)
    scfinp_["ctran"] = aooneint.readbuf(8 * nbasis, FLOAT)
    scfinp_["nbasis"] = aooneint.readbuf(1, INT)[0]
    scfinp_["inamn"] = aooneint.readbuf(nbasis, INT)
    scfinp_["iptyp"] = aooneint.readbuf(nbasis, INT)
    scfinp_["dpnuc"] = aooneint.readbuf(3, FLOAT)
    nucdep = aooneint.readbuf(1, INT)[0]
    scfinp_["nucdep"] = nucdep
    scfinp_["cooo"] = aooneint.readbuf(3 * nucdep, FLOAT)
    scfinp_["ifxyz"] = aooneint.readbuf(3, INT)
    scfinp_["dummy"] = aooneint.readbuf(1, FLOAT)[0]
    scfinp_["qpol"] = aooneint.readbuf(6, FLOAT)
    scfinp_["qq"] = aooneint.readbuf(3, FLOAT)
    scfinp_["jfxyz"] = aooneint.readbuf(3, INT)
    aooneint.close()
    return scfinp_


def read(label="OVERLAP", filename="AOONEINT"):
    """Read integral for label"""
    lbuf = 600
    #
    # Initialize
    #
    unlabeled = readhead(filename)
    nsym = unlabeled["nsym"]
    nbas = unlabeled["naos"]
    INT = unlabeled["int_fmt"]
    FLOAT = unlabeled["float_fmt"]
    nnbast = 0
    for nbasi in nbas:
        nnbast += nbasi * (nbasi + 1) // 2
    s = full.matrix((nnbast,))
    #
    # Open file, locate label
    #
    aooneint = FortranBinary(filename)
    aooneint.find(label)
    #
    # Loop over records
    #

    for rec in aooneint:
        buf = rec.read(lbuf, FLOAT)
        ibuf = rec.read(lbuf, INT)
        length, = rec.read(1, INT)
        if length < 0:
            break
        for i, b in zip(ibuf[:length], buf[:length]):
            s[i - 1] = b

    _S = blocked.triangular(nbas)
    off = 0
    for isym in range(nsym):
        nbasi = nbas[isym] * (nbas[isym] + 1) // 2
        _S.subblock[isym] = np.array(s[off: off + nbasi]).view(full.triangular)
        off += nbasi
    # aooneint.close()
    return _S


def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-H", "--head", dest="head", action="store_true")
    parser.add_argument("-i", "--isordk", dest="isordk", action="store_true")
    parser.add_argument("-s", "--scfinp", dest="scfinp", action="store_true")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true")
    parser.add_argument("-u", "--unpack", dest="unpack", action="store_true")
    parser.add_argument("-o", "--savetxt", dest="savetxt")
    parser.add_argument("-l", "--label")
    # breakpoint()
    parser.add_argument("aooneint")

    args = parser.parse_args()

    if args.head:
        head = readhead(args.aooneint)
        print("Header on AOONEINT")
        for k in head:
            if type(head[k]) is float:
                print("%s %10.5f" % (k, head[k]))
            else:
                print("%s %s" % (k, head[k]))

    if args.isordk:
        isordk = readisordk(args.aooneint)
        n = isordk["nucdep"]
        chrn = isordk["chrn"]
        cooo = isordk["cooo"]
        mxcent = len(chrn)
        print("nucdep=%i" % n + " mxcent=%i" % mxcent)
        print(full.init(chrn)[:n])
        print(full.init(cooo).reshape((3, mxcent))[:, :n])

    if args.scfinp:
        scfinp = readscfinp(args.aooneint)
        for k in scfinp:
            if type(scfinp[k]) is float and k != "dummy":
                print("%s%10.6f" % (k, scfinp[k]))
            else:
                print(k + " " + str(scfinp[k]))

    if args.label is not None:
        s1 = read(label=args.label, filename=args.aooneint)
        if args.unpack:
            s2 = s1.unpack()
            S = s2.unblock()
        else:
            S = s1
        if args.verbose:
            print("%s %s" % (args.label, str(S)))
        if args.savetxt:
            np.savetxt(args.savetxt, S)


if __name__ == "__main__":
    main()
