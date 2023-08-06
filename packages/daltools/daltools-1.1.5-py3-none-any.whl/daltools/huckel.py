from . import dens, one, prop


def get_mo(wrkdir):
    """
    Replicates Huckel start guess in Dalton

    Input: wrkdir
    directory expected to contain integral files AOONEINT, AOPROPER

    """
    H, S = prop.read("HUCKEL", "HUCKOVLP", filename=wrkdir/'AOPROPER')
    h1 = one.read('ONEHAMIL', filename=wrkdir/'AOONEINT').unpack().unblock()

    blockdim = (len(h1), len(H) - len(h1))

    S = S.subblocked(blockdim, blockdim)
    H = H.subblocked(blockdim, blockdim)
    S_ao = S[0, 0]
    S_ao_hu = S[0, 1]
    S_hu = S[1, 1]
    H_hu = S_hu@H[1, 1]@S_hu

    C_hu = dens.cmo(H_hu, S_hu)
    C0 = S_ao.solve(S_ao_hu @ C_hu)
    C0 = C0.GS(S_ao)  # Finalize with Gram-Schmidt
    return C0
