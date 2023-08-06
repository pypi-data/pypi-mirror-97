from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.MMCIFParser import MMCIFParser, FastMMCIFParser
from Bio.PDB.StructureBuilder import StructureBuilder
from Bio.PDB.PDBIO import PDBIO
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from Bio.PDB.mmcifio import MMCIFIO
from Bio.PDB.StructureBuilder import StructureBuilder
from Bio.PDB.Polypeptide import PPBuilder
import sys
import string
import json
import copy
import os
import argparse
import subprocess
import numpy as np

AA_3LET_TO_1LET = {'ALA': 'A',
                   'ARG': 'R',
                   'ASN': 'N',
                   'ASP': 'D',
                   'CYS': 'C',
                   'GLU': 'E',
                   'GLN': 'Q',
                   'GLY': 'G',
                   'HIS': 'H',
                   'ILE': 'I',
                   'LEU': 'L',
                   'LYS': 'K',
                   'MET': 'M',
                   'PHE': 'F',
                   'PRO': 'P',
                   'SER': 'S',
                   'THR': 'T',
                   'TRP': 'W',
                   'TYR': 'Y',
                   'VAL': 'V',
                   'HIC': 'H'}


def load_structure(model_path):
    """
    Creates Biopython structure object from file
    :param model_path: pdb, cif file in_dir
    :return: Biopython structure object
    """
    def copy_label_seq_id(in_path):
        parser = MMCIFParser(QUIET=True)
        parser._mmcif_dict = MMCIF2Dict(in_path)
        if "_atom_site.auth_seq_id" in parser._mmcif_dict:
            for i in parser._mmcif_dict["_atom_site.auth_seq_id"]:
                try:
                    int(i)
                except ValueError:
                    parser._mmcif_dict["_atom_site.auth_seq_id"] = parser._mmcif_dict["_atom_site.label_seq_id"]
        parser._build_structure(in_path.split('/')[-1].split('.')[0])
        return parser._structure_builder.get_structure()

    if model_path.split('.')[-1] == 'pdb' or model_path.split('.')[-1] == 'ent':
        parser = PDBParser(PERMISSIVE=1, QUIET=True)
        structure = parser.get_structure(model_path.split('/')[-1].split('.')[0], model_path)
    elif model_path.split('.')[-1] == 'cif':
        try:
            parser = MMCIFParser(QUIET=True)
            structure = parser.get_structure(model_path.split('/')[-1].split('.')[0], model_path)
        except ValueError:
            structure = copy_label_seq_id(model_path)
    else:
        raise Exception('Please provide the input residue in pdb or cif format')

    return structure

def save_model(model, out_path, preserve_atom_numbering=False):
    """
    Save residue to file
    :param model: structure object
    :param out_path: output file in_dir
    """
    ext = out_path.split('.')[-1]
    if ext == 'pdb' or ext == 'ent':
        io = PDBIO()
    else:
        io = MMCIFIO()
    io.set_structure(model)
    io.save(out_path, preserve_atom_numbering=preserve_atom_numbering)

def calc_residue_static_pairwise_rmsd(model1, model2):
    """
    Calculate pairwise RMSD for residue structure objects without superimposing
    Takes into account residues symmetry
    :param model1: structure object
    :param model2: structure object
    :return: RMSD value
    """
    atoms1 = [atom for atom in model1.get_atoms() if atom.get_name().upper() in ['C', 'CA', 'N', 'O']]
    atoms2 = [atom for atom in model2.get_atoms() if atom.get_name().upper() in ['C', 'CA', 'N', 'O']]
    # print(atoms1)
    # print(atoms2)
    if len(atoms2) != len(atoms1):
        return 100
    atoms1.sort(key=lambda x: x.get_name())
    atoms2.sort(key=lambda x: x.get_name())

    array1, array2 = np.array([atoms1[0].get_coord()]), np.array([atoms2[0].get_coord()])
    for i in range(1, len(atoms1)):
        array1 = np.concatenate((array1, np.array([atoms1[i].get_coord()])), axis=0)
        array2 = np.concatenate((array2, np.array([atoms2[i].get_coord()])), axis=0)

    return rmsd(array1, array2)

def rmsd(array1, array2):
    """
    Calculates RMSD between two sets of coordinates without alignment
    :param array1: numpy 2d array
    :param array2: numpy 2d array
    :return: rmsd
    """
    if np.shape(array1) != np.shape(array1):
        raise Exception('The coordinate arrays must have the same dimensions')
    dif = array1 - array2
    return np.sqrt(np.mean(np.sum(dif * dif, axis=1)))


def filter_far_residues(target, reference, max_rms):
    del_r = []
    for t_res in target.get_residues():
        tmp = []
        r_tmp = []
        for r_res in reference.get_residues():
            # print(t_res, r_res)
            tmp.append(calc_residue_static_pairwise_rmsd(t_res, r_res))
            r_tmp.append(r_res)
        min_r = min(tmp)
        index = tmp.index(min(tmp))
        r = r_tmp[index]
        print(t_res.resname, t_res.parent.id, t_res.id,'--', r.resname, r.parent.id, r.id, min(tmp))
        if min_r > max_rms:
            del_r.append(t_res)
        else:
            t_res.resname = r.resname

    out = copy.deepcopy(target)[0]
    for r in del_r:
        ch = r.get_parent().get_id()
        del out[ch][r.get_id()]
    return out

def del_sidechain(model):
    del_atoms = []
    bb = ['CA', 'C', 'N', 'O', 'CB']
    for chain in model:
        for residue in chain:
            for atom in residue:
                if atom.get_name().upper() not in bb:
                    del_atoms.append((chain.get_id(), residue.get_id(), atom.get_id()))
    for chain, resi, atom in del_atoms:
        del model[chain][resi][atom]
    return model


def match_backbones(target_mod, ref_mod, max_rms):
    target = load_structure(target_mod)
    reference = load_structure(ref_mod)

    out = filter_far_residues(target, reference, max_rms)
    return out
from itertools import permutations
def filter_chains(model, min_len, max_bond):

    # for res in model.get_residues():
    #     res.parent.id = '99'

    ids = string.ascii_uppercase + string.ascii_lowercase
    # ids = ids[::-1]
    short_ids = []

    sb = StructureBuilder()
    sb.init_structure('structure')
    sb.init_seg(' ')
    # res_model_id = {0}


    ch_id = 0
    residues = [r for r in model.get_residues()]
    sb.init_model(0)
    sb.init_chain(ids[0])
    sb.structure[0][ids[0]].add(residues[0].copy())

    for i, res in enumerate(residues[:-1]):
        # a = [c.id for c in model.get_chains()]
        # print(a)
        n = 0
        c = 0
        next_r = residues[i+1]
        for atom in res:
            if atom.get_name() == 'C':
                c = atom
        for atom in next_r:
            if atom.get_name() == 'N':
                n = atom
        d = n - c
        if d > max_bond:
            print(ids[ch_id])
            print(d)
            ch_id += 1
            if ch_id > len(ids)-1:
                ids = [''.join(i) for i in permutations(ids, 2)]
                print(ids)
            sb.init_chain(ids[ch_id])
        sb.structure[0][ids[ch_id]].add(next_r.copy())
    short = [c.id for c in sb.structure.get_chains() if len(c) < min_len]
    for c in short:
        del sb.structure[0][c]

    # for i, c in enumerate(model.get_chains()):
    #     c.id = ids[i]
    return sb.structure


# t = '/Volumes/data/filter/build1.pdb'
# r = '/Volumes/data/filter/6272_shifted.pdb'
# o = '/Volumes/data/filter/build1_filt15_ala_rename.pdb'
# t = '/Users/andrei/filter_build/20584/build1.pdb'
# r = '/Users/andrei/filter_build/20584/6tys.pdb'
# o = '/Users/andrei/filter_build/20584/built_filt.pdb'

t = '/Volumes/data/filter/0703/build1.pdb'
r = '/Volumes/data/filter/0703/6kku.cif'
o = '/Volumes/data/filter/0703/0703_built_filt1.cif'
o_tmp = '/Volumes/data/filter/0703/tmp_0703_built_filt.cif'
o_pdb = '/Volumes/data/filter/0703/tmp_0703_built_filt.pdb'
out = match_backbones(t, r, 1.5)
out = del_sidechain(out)
save_model(out, o_tmp)
out = load_structure(o_tmp)[0]
out = filter_chains(out, 10, 1.5)
save_model(out, o)
save_model(out, o_pdb)