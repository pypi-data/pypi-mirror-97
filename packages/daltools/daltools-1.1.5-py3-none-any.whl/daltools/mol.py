"""Extract molecular info from Dalton molecule file"""
from __future__ import print_function

SPD = ('s', 'p', 'd', 'f', 'g', 'h', 'i')


def readin(inputfile):
    """Read from DALTON.BAS"""
#
# Read inputfile into list lines
#
    molinp = open(inputfile, 'r')
    lines = molinp.readlines()
#
# Check if input format is INTGRL, remove aSPD lines before that
#
    start = lines.index('INTGRL\n')
    if start > 0:
        del lines[0:start]
#
# Two comment lines
#
#   comments = lines[1:3]
#
# Symmetry info extracted form this line
#
    symline = lines[3]
    atom_types = int(symline[1:5])
#   charge = float(symline[5:8])
#
# The molecule is a list of atom types which are hashes with structure
#    atom{'charge'} charge of this atom type
#    atom{'label'}  list of atom label strings of this type
#    atom{'center'} list of atom label strings of this type
#    atom{'basis '} structure of form
#                   [angmom][block]{'prim':[], 'cont':[][]}
#
    molecule = []
    for _ in range(atom_types):
        atom = {}
        molecule.append(atom)
        atline = lines.pop(4)
        atfield = atline.split()
#
#   Information for this atom type
#
        atom['charge'] = float(atfield[0])
        unique = int(atfield[1])
        maxl = int(atfield[2])
        atom['label'] = []
        atom['center'] = []
        atom['basis'] = []
#
#   Information for aSPD atoms of this atom type
#
        for at in range(unique):
            line = lines.pop(4)
            field = line.split()
            atom['label'].append([])
            atom['label'][at] = field[0]
            atom['center'].append([])
            for i in range(1, 4):
                atom['center'][at].append(float(field[i]))
#
#   Information for the basis set of this atom type
#
        for _l in range(maxl):
            atom['basis'].append([])
            nbl = int(atfield[3+_l])
            for block in range(nbl):
                atom['basis'][_l].append([])
                atom['basis'][_l][block] = {}
                atom['basis'][_l][block]['prim'] = []
                atom['basis'][_l][block]['cont'] = []
                line = lines.pop(4)
                field = line.split()
                npr = int(field[1])
                nco = int(field[2])
                for prim in range(npr):
                    line = lines.pop(4)
                    if nco > 3:
                        line += lines.pop(4)
                    if nco > 6:
                        line += lines.pop(4)
                    field = line.split()
                    atom['basis'][_l][block]['prim'].append(float(field[0]))
                    atom['basis'][_l][block]['cont'].append([])
                    for cont in range(nco):
                        atom['basis'][_l][block]['cont'][prim].append(
                            float(field[cont+1])
                            )
    return molecule


def printbasis(molecule):
    """Print molecular info returned by function molecule"""

    retstr = ""
    for i, atom in enumerate(molecule, start=1):
        retstr += ("Atom type %d charge %f\n" % (i, atom['charge']))
        for at in range(len(atom['label'])):
            retstr += f"center {at+1} {atom['center'][at]}\n"
        for _l in range(len(atom['basis'])):
            retstr += ("%s-functions\n" % SPD[_l])
            for block in atom['basis'][_l]:
                prim = block['prim']
                prim = block['prim']
                cont = block['cont']
                for ip, p in enumerate(prim):
                    retstr += f"    {p} {cont[ip][:]}\n"

    print(retstr)


def atoms_in(molecule):
    """Whats this"""
    atomlist = []
    for atype in molecule:
        for a in atype["center"]:
            Z = atype["charge"]
            atom = {"charge": Z, "center": a, "type": atype}
            contracted = 0
            for _l, bas in enumerate(atype['basis']):
                contracted_l = 0
                for block in bas:
                    cont = block['cont']
                    contracted += len(cont[0])*(2*_l+1)
                    contracted_l += len(cont[0])*(2*_l+1)
                atom[SPD[_l]] = contracted_l
            atom["contracted"] = contracted
            atomlist.append(atom)
    return atomlist


def contracted_per_atom(molecule):
    """Return number of contracted per atom"""
    atomlist = atoms_in(molecule)
    contracted = []
    for atom in atomlist:
        contracted.append(atom["contracted"])
    return contracted


def contracted_per_atom_l(molecule):
    """Return number of contracted and angular momentum"""
    atomlist = atoms_in(molecule)
    contracted_l = []
    for i in range(len(atomlist)):
        atom = atomlist[i]
        contracted_l.append([])
        for _l in range(len(atom["type"]["basis"])):
            contracted_l[i].append(atom[SPD[_l]])
    return contracted_l


def occupied_per_atom(molecule):
    """Return number of occupied per atom (assuming ANO type basis)"""
    cpal = contracted_per_atom_l(molecule)
    atomlist = atoms_in(molecule)
    assert len(cpal) == len(atomlist)
    nocclist = []
    for a in range(len(atomlist)):
        offset = 0
        atom = atomlist[a]
        Z = int(atom["charge"]+0.5)
        nocclist.append([])
        for _l in range(len(cpal[a])):
            if Z <= 1:
                if _l == 0:
                    nocclist[a].append(offset)
            elif Z <= 2:
                if _l == 0:
                    nocclist[a].append(offset)
                    nocclist[a].append(offset+1)
            elif Z <= 8:
                if _l == 0:
                    nocclist[a].append(offset)
                    nocclist[a].append(offset+1)
                elif _l == 1:
                    nocclist[a].append(offset)
                    nocclist[a].append(offset+1)
                    nocclist[a].append(offset+2)
            elif Z <= 18:
                if _l == 0:
                    nocclist[a].append(offset)
                    nocclist[a].append(offset+1)
                    nocclist[a].append(offset+2)
                elif _l == 1:
                    nocclist[a].append(offset)
                    nocclist[a].append(offset+1)
                    nocclist[a].append(offset+2)
                    nocclist[a].append(offset+3)
                    nocclist[a].append(offset+4)
                    nocclist[a].append(offset+5)
            else:
                raise NotImplementedError
            offset += cpal[a][_l]
    return nocclist


def nuc(molecule):
    """Test nuclear repulsion energy"""
    atomlist = atoms_in(molecule)
    Z = 0.0
    for a in atomlist:
        ZA = a["charge"]
        RA = a["center"]
        ia = atomlist.index(a)
        for b in atomlist[:ia]:
            ZB = b["charge"]
            RB = b["center"]
            Z += ZA*ZB/dist(RA, RB)
    return Z


def dist(A, B):
    """distance beteen two atoms"""
    from math import sqrt
    return sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2)


if __name__ == "__main__":  # pragma: nocover
    mo = readin("tests/test_mol.d/DALTON.BAS")
    printbasis(mo)
