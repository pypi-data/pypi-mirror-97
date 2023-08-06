""" BioSimulators-compliant command-line interface to the `BioNetGen <https://bionetgen.org/>`_ simulation program.

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2021-01-05
:Copyright: 2020-2021, Center for Reproducible Biomedical Modeling
:License: MIT
"""

from .data_model import KISAO_METHOD_ARGUMENTS_MAP
from .utils import (validate_time_course, validate_data_generator_variables, get_boolnet,
                    set_simulation_method_arg, get_variable_results)
from biosimulators_utils.combine.exec import exec_sedml_docs_in_archive
from biosimulators_utils.log.data_model import CombineArchiveLog, TaskLog  # noqa: F401
from biosimulators_utils.plot.data_model import PlotFormat  # noqa: F401
from biosimulators_utils.report.data_model import ReportFormat, VariableResults  # noqa: F401
from biosimulators_utils.sedml import validation
from biosimulators_utils.sedml.data_model import (Task, ModelLanguage, ModelAttributeChange,  # noqa: F401
                                                  UniformTimeCourseSimulation, Variable)
from biosimulators_utils.sedml.exec import exec_sed_doc
from biosimulators_utils.xml.utils import get_namespaces_for_xml_doc
from rpy2.robjects.vectors import StrVector
from lxml import etree
import functools
import numpy

__all__ = ['exec_sedml_docs_in_combine_archive', 'exec_sed_task']


def exec_sedml_docs_in_combine_archive(archive_filename, out_dir,
                                       report_formats=None, plot_formats=None,
                                       bundle_outputs=None, keep_individual_outputs=None):
    """ Execute the SED tasks defined in a COMBINE/OMEX archive and save the outputs

    Args:
        archive_filename (:obj:`str`): path to COMBINE/OMEX archive
        out_dir (:obj:`str`): path to store the outputs of the archive

            * CSV: directory in which to save outputs to files
              ``{ out_dir }/{ relative-path-to-SED-ML-file-within-archive }/{ report.id }.csv``
            * HDF5: directory in which to save a single HDF5 file (``{ out_dir }/reports.h5``),
              with reports at keys ``{ relative-path-to-SED-ML-file-within-archive }/{ report.id }`` within the HDF5 file

        report_formats (:obj:`list` of :obj:`ReportFormat`, optional): report format (e.g., csv or h5)
        plot_formats (:obj:`list` of :obj:`PlotFormat`, optional): report format (e.g., pdf)
        bundle_outputs (:obj:`bool`, optional): if :obj:`True`, bundle outputs into archives for reports and plots
        keep_individual_outputs (:obj:`bool`, optional): if :obj:`True`, keep individual output files

    Returns:
        :obj:`CombineArchiveLog`: log
    """
    sed_doc_executer = functools.partial(exec_sed_doc, exec_sed_task)
    return exec_sedml_docs_in_archive(sed_doc_executer, archive_filename, out_dir,
                                      apply_xml_model_changes=True,
                                      report_formats=report_formats,
                                      plot_formats=plot_formats,
                                      bundle_outputs=bundle_outputs,
                                      keep_individual_outputs=keep_individual_outputs)


def exec_sed_task(task, variables, log=None):
    """ Execute a task and save its results

    Args:
       task (:obj:`Task`): task
       variables (:obj:`list` of :obj:`Variable`): variables that should be recorded
       log (:obj:`TaskLog`, optional): log for the task

    Returns:
        :obj:`tuple`:

            :obj:`VariableResults`: results of variables
            :obj:`TaskLog`: log

    Raises:
        :obj:`NotImplementedError`:

          * Task requires a time course that BoolNet doesn't support
          * Task requires an algorithm that BoolNet doesn't support
    """
    log = log or TaskLog()

    # validate task
    validation.validate_task(task)
    validation.validate_model_language(task.model.language, ModelLanguage.SBML)
    validation.validate_model_change_types(task.model.changes, ())
    validation.validate_model_changes(task.model.changes)
    validation.validate_simulation_type(task.simulation, (UniformTimeCourseSimulation, ))
    validate_time_course(task.simulation)
    validation.validate_uniform_time_course_simulation(task.simulation)
    validation.validate_data_generator_variables(variables)
    namespaces = get_namespaces_for_xml_doc(etree.parse(task.model.source))
    target_x_paths_ids = validation.validate_variable_xpaths(
        variables,
        task.model.source,
        attr={
            'namespace': {
                'prefix': 'qual',
                'uri': namespaces['qual'],
            },
            'name': 'id',
        }
    )

    # get BoolNet
    boolnet = get_boolnet()

    # read model
    model = boolnet.loadSBML(StrVector([task.model.source]))

    # initialize arguments for BoolNet's time course simulation method
    sim = task.simulation
    simulation_method_args = {
        'numMeasurements': int(sim.number_of_points) + 1,
        'numSeries': 1,
        'perturbations': 0,
    }

    # Load the algorithm specified by :obj:`task.simulation.algorithm.kisao_id`
    alg_kisao_id = sim.algorithm.kisao_id
    alg = KISAO_METHOD_ARGUMENTS_MAP.get(alg_kisao_id, None)
    if alg is None:
        raise NotImplementedError("".join([
            "Algorithm with KiSAO id '{}' is not supported. ".format(alg_kisao_id),
            "Algorithm must have one of the following KiSAO ids:\n  - {}".format('\n  - '.join(
                '{}: {}'.format(kisao_id, alg['name'])
                for kisao_id, alg in KISAO_METHOD_ARGUMENTS_MAP.items())),
        ]))

    simulation_method_args['type'] = StrVector([alg['type']])

    # Apply the algorithm parameter changes specified by `simulation.algorithm.parameter_changes`
    for change in sim.algorithm.changes:
        set_simulation_method_arg(model, alg_kisao_id, change, simulation_method_args)

    # validate that BoolNet can produce the desired variables of the desired data generators
    validate_data_generator_variables(variables, alg_kisao_id)

    # execute simulation
    species_results_matrix = boolnet.generateTimeSeries(model, **simulation_method_args)[0]
    species_results_dict = {}
    for i_species, species_id in enumerate(species_results_matrix.rownames):
        species_results_dict[species_id] = numpy.array(species_results_matrix.rx(i_species + 1, True))

    # get the results in BioSimulator's format
    variable_results = get_variable_results(sim, variables, target_x_paths_ids, species_results_dict)
    for variable in variables:
        variable_results[variable.id] = variable_results[variable.id][-(int(sim.number_of_points) + 1):]

    # log action
    log.algorithm = alg_kisao_id
    log.simulator_details = {
        'method': 'BoolNet::generateTimeSeries',
        'arguments': simulation_method_args,
    }

    # return the result of each variable and log
    return variable_results, log
