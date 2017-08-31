#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-

import sys
import os

from aiida.common.example_helpers import test_and_get_code
from aiida.common.exceptions import NotExistent

################################################################

ParameterData = DataFactory('parameter')

try:
    dontsend = sys.argv[1]
    if dontsend == "--dont-send":
        submit_test = True
    elif dontsend == "--send":
        submit_test = False
    else:
        raise IndexError
except IndexError:
    print >> sys.stderr, ("The first parameter can only be either "
                          "--send or --dont-send")
    sys.exit(1)

try:
    codename = sys.argv[2]
except IndexError:
    codename = 'plstm-4.0@rinaldo'

code = test_and_get_code(codename, expected_code_type='siesta.stm')
#
#  Set up calculation object first
#
calc = code.new_calc()
calc.label = "Test STM"
calc.description = "STM calculation test"

#
#----Settings first  -----------------------------
#
settings_dict={'additional_retrieve_list': []}
settings = ParameterData(dict=settings_dict)
calc.use_settings(settings)
#---------------------------------------------------

# Parameters ---------------------------------------------------
params_dict= {
    'z': 7.50     # In Angstrom
}
parameters = ParameterData(dict=params_dict)
calc.use_parameters(parameters)
#
calc.set_max_wallclock_seconds(30*60) # 30 min
calc.set_resources({"num_machines": 1, "num_mpiprocs_per_machine": 1})

from aiida.orm.data.remote import RemoteData
remotedata = load_node(3163)
calc.use_parent_folder(remotedata)

if submit_test:
    subfolder, script_filename = calc.submit_test()
    print "Test_submit for calculation (uuid='{}')".format(
        calc.uuid)
    print "Submit file in {}".format(os.path.join(
        os.path.relpath(subfolder.abspath),
        script_filename
        ))
else:
    calc.store_all()
    print "created calculation; calc=Calculation(uuid='{}') # ID={}".format(
        calc.uuid,calc.dbnode.pk)
    calc.submit()
    print "submitted calculation; calc=Calculation(uuid='{}') # ID={}".format(
        calc.uuid,calc.dbnode.pk)
