#!/usr/bin/env python

from .comms import printer
from .parsers import VaspOutcar
from .parsers import AbinitOutput
from .parsers import QE_ElaStic_Parser
from .parsers import QE_thermo_pw_Parser
from .core import ElasticProperties
from .core import ElasticProperties2D


def calculate_elastic(
    infile="OUTCAR",
    dim="3D",
    crystal=None,
    lattice_type = None,
    code="vasp",
    anaddbfile=None,
    outfile=None,
    adjust_pressure=True,
):

    """
    This method calculates the elastic properties
    of a material from a DFT calculation.
    """

    # welcome message
    printer.print_mechelastic()

    elastic_tensor = None
    structure = None
    lattice_constant = None
    crystal_type = crystal

    # calling parser
    if code == "vasp":
        output = VaspOutcar(infile=infile, adjust_pressure=adjust_pressure)
        elastic_tensor = output.elastic_tensor
        structure = output.structure
        lattice_constant = output.lattice_constant

    elif code == "abinit":
        output = AbinitOutput(infile=infile, anaddbfile=anaddbfile)
        elastic_tensor = output.elastic_tensor
        structure = output.structure
        lattice_constant = output.lattice_constant

    elif code == "qe_ElaStic":
        output = QE_ElaStic_Parser(outfile=outfile, infile=infile)
        elastic_tensor = output.elastic_tensor
        structure = output.structure
        lattice_constant = output.lattice_constant

    elif code == "qe_thermo_pw":
        output = QE_thermo_pw_Parser(outfile=outfile, infile=infile)
        elastic_tensor = output.elastic_tensor
        structure = output.structure
        lattice_constant = output.lattice_constant

    # elastic constants calculation for 3D materials
    if dim == "3D":
        elastic_properties = ElasticProperties(elastic_tensor, structure, crystal_type, code = code)
        elastic_properties.print_properties()

    # elastic constants calculation for 2D materials
    elif dim == "2D":
        elastic_properties = ElasticProperties2D(elastic_tensor, lattice_constant, lattice_type = lattice_type)
        elastic_properties.print_properties()

    # other
    # else: We don't need this
    #     elastic_bulk.elastic_const_bulk(
    #         cnew, snew, crystal, cell, density, natoms, totalmass
    #     )

    print("\nThanks! See you later. ")
    return output
