#!/usr/bin/env python     
# -*- coding: utf-8 -*-     
# Copyright (C)   2021 Sudarshan Ghonge <sudarshan.ghonge>
#     
# This program is free software; you can redistribute it and/or modify     
# it under the terms of the GNU General Public License as published by     
# the Free Software Foundation; either version 2 of the License, or     
# (at your option) any later version.     
# This program is distributed in the hope that it will be useful,     
# but WITHOUT ANY WARRANTY; without even the implied warranty of     
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the     
# GNU General Public License for more details.     
#     
# You should have received a copy of the GNU General Public License along     
# with this program; if not, write to the Free Software Foundation, Inc.,     
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.    

# DAG Class definitions for bayeswave

from __future__ import print_function

import ast
import os
import sys

import numpy as np
import pandas as pd
from glue import pipeline
from glue.ligolw import ilwd
from glue.ligolw import ligolw
from glue.ligolw import lsctables

try:
    import configparser
except ImportError:  # python < 3
    import ConfigParser as configparser
else:  # other python3 compatibility stuff
    xrange = range
# XXX Hardcoded cvmfs frame root
CVMFS_FRAMES = "/cvmfs/oasis.opensciencegrid.org/ligo/frames/"


# define a content handler
class LIGOLWContentHandler(ligolw.LIGOLWContentHandler):
    pass


lsctables.use_in(LIGOLWContentHandler)


def write_res_post_cmd(res_workdir, ifos):
    """ Sets up the cache files for the residual frames to be used in 
        the bayeswave residual runs using `lalapps_path2cache` command
    """

    script = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Sudarshan Ghonge <sudarshan.ghonge@ligo.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
\"\"\"Setup the cache files for residual frame files
 needed by residual BW run.

\"\"\"

import os
for ifo in %s:
    a = os.popen('ls residual_frame/*%%s*.gwf | lalapps_path2cache'%%ifo).read().strip("\\n").split(' ')
    a[4] = os.path.basename(a[4].split('localhost')[-1])
    a[4] = os.path.join('residual_frame', a[4])
    with open(os.path.join('datafind', '%%s_res.cache'%%ifo), 'w') as res_cache_file:
        res_cache_file.write(' '.join(a) + '\\n')
        res_cache_file.close()
    
""" % str(ifos)

    with open(os.path.join(res_workdir, "make_res_cache.py"), 'w') as postfile:
        postfile.writelines(script)
        postfile.close()
    os.chmod(os.path.join(res_workdir, "make_res_cache.py"), 0o755)


def condor_job_config(job_type, condor_job, config_parser):
    """
    Configure the condor job executable and environment for one of:
     * job_type='gwcomp_reclal'
     * job_type='gwcomp_bw_li_inj'
     * job_type='gwcomp_residuals'
     * job_type='gwcomp_testgr'

    This identifies the site (OSG vs LDG) and set properties of the condor job
    (file transfers, executable location etc) accordingly

    """
    valid_job_types = ['gwcomp_reclal', 'gwcomp_bw_li_inj', 'gwcomp_residuals', 'gwcomp_testgr']
    try:
        job_index = valid_job_types.index(job_type)
    except ValueError:
        print("unrecognized job type", file=sys.stderr)

    executable = config_parser.get('engine', job_type)
    universe = config_parser.get('condor', 'universe')
    pipeline.CondorDAGJob.__init__(condor_job, universe, executable)
    pipeline.AnalysisJob.__init__(condor_job, config_parser, dax=False)

    requires = []

    #
    # Singularity configuration
    #
    if config_parser.getboolean('engine', 'use-singularity'):

        print("Running with singularity(image={})".format(
            config_parser.get('engine', 'singularity')))

        # Force quotes if absent
        singularityImage = config_parser.get('engine', 'singularity')
        if singularityImage[0] != '"':  singularityImage = '"' + singularityImage
        if singularityImage[-1] != '"':  singularityImage += '"'
        condor_job.add_condor_cmd('+SingularityImage', singularityImage)

        requires.append("(HAS_SINGULARITY=?=TRUE)")

        singularityImage = config_parser.get('engine', 'singularity')
        # Force quotes if absent
        if singularityImage[0] != '"':  singularityImage = '"' + singularityImage
        if singularityImage[-1] != '"':  singularityImage += '"'
        condor_job.add_condor_cmd('+SingularityImage', singularityImage)

    else:
        condor_job.add_condor_cmd('getenv', True)

    if config_parser.getboolean('condor', 'transfer-files'):
        print("Configuring file transfers for {}".format(job_type), file=sys.stdout)
        condor_job.add_condor_cmd('should_transfer_files', 'YES')
        condor_job.add_condor_cmd("transfer_executable", False)

    #
    # OSG specific configuration
    #
    if config_parser.getboolean('condor', 'osg-deploy'):
        # --- Force jobs to run locally
        requires.append("(GLIDEIN_SITE=?=undefined)")
        if not job_type == 'gwcomp_residuals':
            requires.append("(HAS_LIGO_FRAMES=?=TRUE)")

    try:
        condor_job.add_condor_cmd('accounting_group',
                                  config_parser.get('condor', 'accounting-group'))
    except configparser.NoOptionError:
        print("Error: no accounting-group supplied in [condor]")
        sys.exit(1)

    try:
        condor_job.add_condor_cmd('accounting_group_user',
                                  config_parser.get('condor', 'accounting-group-user'))
    except configparser.NoOptionError:
        print("Warning: no accounting-group-user supplied in [condor]")

    # Condor notifications
    if config_parser.has_option('condor', 'notify-user'):
        condor_job.add_condor_cmd('notify_user',
                                  config_parser.get('condor', 'notify-user'))

    try:
        condor_job.add_condor_cmd('notify_user',
                                  config_parser.get('condor', 'notify-user'))
    except configparser.NoOptionError:
        pass

    try:
        condor_job.set_notification(config_parser.get('condor',
                                                      'notification'))
    except:
        condor_job.set_notification('Error')

    # Finally tie requirements together into a condor-friendly string
    if len(requires) > 0:
        condor_job.add_condor_cmd("requirements", " && ".join(requires))

    return


def bayeswaveConfigTemplate():
    # A bayeswave config file template.
    config_bw = configparser.ConfigParser()
    config_bw.optionxform = str
    config_bw.add_section("input")
    config_bw.set("input", "dataseed", "1234")
    config_bw.set("input", "seglen", "")
    config_bw.set("input", "window", "1.0")
    config_bw.set("input", "flow", "20")
    config_bw.set("input", "srate", "")
    config_bw.set("input", "PSDlength", "")
    config_bw.set("input", "padding", "0.0")
    config_bw.set("input", "keep-frac", "1.0")
    config_bw.set("input", "rho-threshold", "7.0")
    config_bw.set("input", "ifo-list", "")
    config_bw.add_section("engine")
    config_bw.set("engine", "install_path", "")
    config_bw.set("engine", "bayeswave", "")
    config_bw.set("engine", "bayeswave_post", "")
    config_bw.set("engine", "megaplot", "")
    config_bw.set("engine", "megasky", "")
    config_bw.add_section("datafind")
    config_bw.set("datafind", "frtype-list", "")
    config_bw.set("datafind", "channel-list", "")
    config_bw.set("datafind", "url-type", "file")
    config_bw.set("datafind", "veto-categories", "[1]")
    config_bw.add_section("bayeswave_options")
    config_bw.set("bayeswave_options", "updateGeocenterPSD", "")
    config_bw.set("bayeswave_options", "waveletPrior", "")
    config_bw.set("bayeswave_options", "Dmax", "100")
    config_bw.set("bayeswave_options", "signalOnly", "")
    config_bw.add_section("bayeswave_post_options")
    config_bw.set("bayeswave_post_options", "0noise", "")
    # config_bw.set("bayeswave_post_options","lite","")
    # config_bw.add_section("injections")
    # config_bw.set("injections","events","all")
    config_bw.add_section("condor")
    config_bw.set("condor", "checkpoint", "")
    config_bw.set("condor", "bayeswave-request-memory", "")  # config["bayeswave"]["request-memory"])
    config_bw.set("condor", "bayeswave_post-request-memory", "")  # config["bayeswave"]["post-request-memory"])
    config_bw.set("condor", "datafind", "/usr/bin/gw_data_find")
    config_bw.set("condor", "ligolw_print", "/usr/bin/ligolw_print")
    config_bw.set("condor", "segfind", "/usr/bin/ligolw_segment_query_dqsegdb")
    config_bw.set("condor", "accounting-group", "")  # config["bayeswave"]["accounting-group"])
    config_bw.set("condor", "accounting-group-user", os.popen("whoami").read().strip())
    config_bw.add_section("segfind")
    config_bw.set("segfind", "segment-url", "https://segments.ligo.org")
    config_bw.add_section("segments")
    config_bw.set("segments", "h1-analyze", "H1:DMT-ANALYSIS_READY:1")
    config_bw.set("segments", "l1-analyze", "L1:DMT-ANALYSIS_READY:1")
    config_bw.set("segments", "v1-analyze", "V1:ITF_SCIENCEMODE")

    return config_bw


def create_xml_table(pe_file, pe_config, trigtimes, injfile_name):
    sim_inspiral_dt = [
        ('waveform', '|S64'),
        ('taper', '|S64'),
        ('f_lower', 'f8'),
        ('mchirp', 'f8'),
        ('eta', 'f8'),
        ('mass1', 'f8'),
        ('mass2', 'f8'),
        ('geocent_end_time', 'f8'),
        ('geocent_end_time_ns', 'f8'),
        ('distance', 'f8'),
        ('longitude', 'f8'),
        ('latitude', 'f8'),
        ('inclination', 'f8'),
        ('coa_phase', 'f8'),
        ('polarization', 'f8'),
        ('spin1x', 'f8'),
        ('spin1y', 'f8'),
        ('spin1z', 'f8'),
        ('spin2x', 'f8'),
        ('spin2y', 'f8'),
        ('spin2z', 'f8'),
        ('amp_order', 'i4'),
        ('numrel_data', '|S64')
    ]
    ninj = trigtimes.shape[0]
    injections = np.zeros((ninj), dtype=sim_inspiral_dt)
    pe_structured_array = np.genfromtxt(pe_file, names=True)
    params = pe_structured_array.dtype.names
    post_samples = pd.DataFrame(pe_structured_array)
    post_samples = post_samples.sample(ninj)
    # Get approximant.
    approx = pe_config["engine"]["approx"]
    amp_order = int(pe_config["engine"]["amporder"])

    pe_ifos = ast.literal_eval(pe_config["analysis"]["ifos"])
    pe_flows = ast.literal_eval(pe_config["lalinference"]["flow"])
    pe_flows = [float(pe_flows[ifo]) for ifo in pe_ifos]
    pe_flow = np.max(pe_flows)

    trigtimes_ns, trigtimes_s = np.modf(trigtimes)
    trigtimes_ns *= 10 ** 9
    injections["waveform"] = [approx for i in range(ninj)]
    injections["taper"] = ["TAPER_NONE" for i in range(ninj)]
    injections["f_lower"] = [pe_flow for i in range(ninj)]
    try:
        injections["mchirp"] = np.array(post_samples["chirp_mass"])
    except:
        injections["mchirp"] = np.array(post_samples["mc"])
    try:
        injections["eta"] = np.array(post_samples["symmetric_mass_ratio"])
    except:
        injections["eta"] = np.array(post_samples["eta"])
    try:
        injections["mass1"] = np.array(post_samples["mass_1"])
    except:
        injections["mass1"] = np.array(post_samples["m1"])
    try:
        injections["mass2"] = np.array(post_samples["mass_2"])
    except:
        injections["mass2"] = np.array(post_samples["m2"])
    injections["geocent_end_time"] = trigtimes_s
    injections["geocent_end_time_ns"] = trigtimes_ns
    try:
        injections["distance"] = np.array(post_samples["luminosity_distance"])
    except:
        injections["distance"] = np.array(post_samples["dist"])
    injections["longitude"] = np.array(post_samples["ra"])
    injections["latitude"] = np.array(post_samples["dec"])
    injections["inclination"] = np.array(post_samples["iota"])
    injections["coa_phase"] = np.array(post_samples["phase"])
    injections["polarization"] = np.array(post_samples["psi"])
    try:
        injections["spin1x"] = np.array(post_samples["spin_1x"])
    except:
        injections["spin1x"] = np.array(post_samples["a1"]) * np.sin(np.array(post_samples["theta1"])) * np.cos(
            np.array(post_samples["phi1"]))
    try:
        injections["spin1y"] = np.array(post_samples["spin_1y"])
    except:
        injections["spin1y"] = np.array(post_samples["a1"]) * np.sin(np.array(post_samples["theta1"])) * np.sin(
            np.array(post_samples["phi1"]))
    try:
        injections["spin1z"] = np.array(post_samples["spin_1z"])
    except:
        injections["spin1z"] = np.array(post_samples["a1"]) * np.cos(np.array(post_samples["theta1"]))
    try:
        injections["spin2x"] = np.array(post_samples["spin_2x"])
    except:
        injections["spin2x"] = np.array(post_samples["a2"]) * np.sin(np.array(post_samples["theta2"])) * np.cos(
            np.array(post_samples["phi2"]))
    try:
        injections["spin2y"] = np.array(post_samples["spin_2y"])
    except:
        injections["spin2y"] = np.array(post_samples["a2"]) * np.sin(np.array(post_samples["theta2"])) * np.sin(
            np.array(post_samples["phi2"]))
    try:
        injections["spin2z"] = np.array(post_samples["spin_2z"])
    except:
        injections["spin2z"] = np.array(post_samples["a2"]) * np.cos(np.array(post_samples["theta2"]))
    injections["amp_order"] = [amp_order for i in range(ninj)]
    injections["numrel_data"] = ["" for i in range(ninj)]
    # Create a new XML document
    xmldoc = ligolw.Document()
    xmldoc.appendChild(ligolw.LIGO_LW())
    sim_table = lsctables.New(lsctables.SimInspiralTable)
    xmldoc.childNodes[0].appendChild(sim_table)

    # Add empty rows to the sim_inspiral table
    for inj in range(ninj):
        row = sim_table.RowType()
        for slot in row.__slots__:
            setattr(row, slot, 0)
        sim_table.append(row)

    # Fill in IDs
    for i, row in enumerate(sim_table):
        row.process_id = ilwd.ilwdchar("process:process_id:{0:d}".format(i))
        row.simulation_id = ilwd.ilwdchar("sim_inspiral:simulation_id:{0:d}".format(i))

    # Fill rows
    for field in injections.dtype.names:
        vals = injections[field]
        for row, val in zip(sim_table, vals):
            setattr(row, field, val)
    with open(injfile_name, "w") as f:
        print("Saving file...")
        xmldoc.write(f)


class gwcomp_reclalJob(pipeline.CondorDAGJob, pipeline.AnalysisJob):
    def __init__(self, gwcomp_config, cacheFiles, psdFiles, peFile,
                 dax=False):

        condor_job_config('gwcomp_reclal', self, gwcomp_config)
        onsource_workdir = os.getcwd()
        self.add_condor_cmd('initialdir', onsource_workdir)
        self.set_sub_file(os.path.join(onsource_workdir, 'gwcomp_reclal.sub'))

        self.set_stdout_file(os.path.join(onsource_workdir, 'logs',
                                          'gwcomp_reclal_$(cluster)-$(process).out'))
        self.set_stderr_file(os.path.join(onsource_workdir, 'logs',
                                          'gwcomp_reclal_$(cluster)-$(process).err'))
        self.set_log_file(os.path.join(onsource_workdir, 'logs',
                                       'gwcomp_reclal_$(cluster)-$(process).log'))

        if gwcomp_config.has_option('condor', 'arch'):
            self.add_condor_cmd('+arch', gwcomp_config.get('condor', 'arch'))

        if gwcomp_config.has_option('condor', 'gwcomp_reclal-request-memory'):
            self.add_condor_cmd('request_memory',
                                gwcomp_config.get('condor', 'gwcomp_reclal-request-memory'))

        if gwcomp_config.has_option('condor', 'gwcomp_reclal-request-disk'):
            self.add_condor_cmd('request_disk',
                                gwcomp_config.get('condor', 'gwcomp_reclal-request-disk'))

        if gwcomp_config.has_option('condor', 'bayeswave-cit-nodes'):
            self.add_condor_cmd('+BayesWaveCgroup', 'True')
            self.add_condor_cmd('Rank', '(TARGET.BayesWaveCgroup =?= True)')

        if gwcomp_config.has_option('condor', 'environment'):
            self.add_condor_cmd('environment', gwcomp_config.get('condor', 'environment'))

        transfer_string = '$(macrooutputdir), %s' % peFile
        for psdf in list(psdFiles.values()):
            transfer_string = transfer_string + "," + psdf

        self.add_condor_cmd('transfer_input_files', transfer_string)
        self.add_condor_cmd('transfer_output_files', '$(macrooutputdir)')


class gwcomp_reclalNode(pipeline.CondorDAGNode, pipeline.AnalysisNode):
    def __init__(self, gwcomp_reclal_job):
        pipeline.CondorDAGNode.__init__(self, gwcomp_reclal_job)
        pipeline.AnalysisNode.__init__(self)

    def set_li_samples_file(self, li_samples_file):
        self.add_var_opt('li-samples-file', li_samples_file)
        self.li_samples_file = li_samples_file

    def set_psd_files(self, psd_files):
        self.add_var_opt('psd', ' '.join(psd_files))
        self.psd_files = psd_files

    def set_asd_file_flag(self):
        self.add_var_opt('is-asd-file', '')

    def set_srate(self, srate):
        self.add_var_opt('srate', srate)

    def set_li_epoch(self, li_epoch):
        self.add_var_opt('li-epoch', li_epoch)

    def set_trigtime(self, trigtime):
        self.add_var_opt('trigtime', trigtime)

    def set_nwaves(self, nwaves):
        self.add_var_opt('nwaves', nwaves)

    def set_approx(self, approx):
        self.add_var_opt('approx', approx)

    def set_duration(self, duration):
        self.add_var_opt('duration', duration)

    def set_output_dir(self, output_dir):
        self.add_var_opt('output-dir', output_dir)

    def set_make_plots_flag(self):
        self.add_var_opt('make-plots', '')

    def set_flow(self, flow):
        self.add_var_opt('flow', flow)

    def set_ifos(self, ifos):
        self.add_var_opt('ifos', ' '.join(ifos))

    def set_choose_fd_flag(self):
        self.add_var_opt('choose-fd', '')

    def set_fref(self, fref):
        self.add_var_opt('fref', fref)

    def set_amp_order(self, amp_order):
        self.add_var_opt('amp-order', amp_order)

    def set_phase_order(self, phase_order):
        self.add_var_opt('phase-order', phase_order)


class gwcomp_bw_li_injJob(pipeline.CondorDAGJob, pipeline.AnalysisJob):
    def __init__(self, gwcomp_config, dax=False):

        condor_job_config('gwcomp_bw_li_inj', self, gwcomp_config)
        workdir = os.getcwd()
        self.add_condor_cmd('initialdir', workdir)
        self.set_sub_file(os.path.join(workdir, 'gwcomp_bw_li_inj.sub'))

        self.set_stdout_file(os.path.join(workdir, 'logs',
                                          'gwcomp_bw_li_inj_$(cluster)-$(process).out'))
        self.set_stderr_file(os.path.join(workdir, 'logs',
                                          'gwcomp_bw_li_inj_$(cluster)-$(process).err'))
        self.set_log_file(os.path.join(workdir, 'logs',
                                       'gwcomp_bw_li_inj_$(cluster)-$(process).log'))

        if gwcomp_config.has_option('condor', 'arch'):
            self.add_condor_cmd('+arch', gwcomp_config.get('condor', 'arch'))

        if gwcomp_config.has_option('condor', 'gwcomp_bw_li_inj-request-memory'):
            self.add_condor_cmd('request_memory',
                                gwcomp_config.get('condor', 'gwcomp_bw_li_inj-request-memory'))

        if gwcomp_config.has_option('condor', 'gwcomp_bw_li_inj-request-disk'):
            self.add_condor_cmd('request_disk',
                                gwcomp_config.get('condor', 'gwcomp_bw_li_inj-request-disk'))

        if gwcomp_config.has_option('condor', 'bayeswave-cit-nodes'):
            self.add_condor_cmd('+BayesWaveCgroup', 'True')
            self.add_condor_cmd('Rank', '(TARGET.BayesWaveCgroup =?= True)')

        if gwcomp_config.has_option('condor', 'environment'):
            self.add_condor_cmd('environment', gwcomp_config.get('condor', 'environment'))

        transfer_string = '$(macrooutputdir)'

        self.add_condor_cmd('transfer_input_files', transfer_string)
        self.add_condor_cmd('transfer_output_files', '$(macrooutputdir)')


class gwcomp_bw_li_injNode(pipeline.CondorDAGNode, pipeline.AnalysisNode):
    def __init__(self, gwcomp_bw_li_inj_job):
        pipeline.CondorDAGNode.__init__(self, gwcomp_bw_li_inj_job)
        pipeline.AnalysisNode.__init__(self)

    def set_bw_dir(self, bw_dir):
        self.add_var_opt('bw-dir', bw_dir)

    def set_li_dir(self, li_dir):
        self.add_var_opt('li-dir', li_dir)

    def set_flow(self, flow):
        self.add_var_opt('flow', flow)

    def set_srate(self, srate):
        self.add_var_opt('srate', srate)

    def set_ifos(self, ifos):
        self.add_var_opt('ifos', ' '.join(ifos))

    def set_trigtime(self, trigtime):
        self.add_var_opt('trigtime', trigtime)

    def set_epoch(self, epoch):
        self.add_var_opt('epoch', epoch)

    def set_duration(self, duration):
        self.add_var_opt('duration', duration)

    def set_output_dir(self, output_dir):
        self.add_var_opt('output-dir', output_dir)

    def set_injection_flag(self):
        self.add_var_opt('injection', '')

    def set_plot_flag(self):
        self.add_var_opt('make-plots', '')

    def set_whitened_data_flag(self):
        self.add_var_opt('whitened-data', '')

    def set_matched_filter_snr_flag(self):
        self.add_var_opt('matched-filter-snr', '')

    def set_matches_flag(self):
        self.add_var_opt('compute-matches', '')


class gwcomp_residualsJob(pipeline.CondorDAGJob, pipeline.AnalysisJob):
    def __init__(self, gwcomp_config, cacheFiles, psdFiles, peFile,
                 dax=False):

        condor_job_config('gwcomp_residuals', self, gwcomp_config)
        res_workdir = os.getcwd()
        self.add_condor_cmd('initialdir', res_workdir)
        self.set_sub_file(os.path.join(res_workdir, 'gwcomp_residuals.sub'))

        self.set_stdout_file(os.path.join(res_workdir, 'logs',
                                          'gwcomp_residuals_$(cluster)-$(process).out'))
        self.set_stderr_file(os.path.join(res_workdir, 'logs',
                                          'gwcomp_residuals_$(cluster)-$(process).err'))
        self.set_log_file(os.path.join(res_workdir, 'logs',
                                       'gwcomp_residuals_$(cluster)-$(process).log'))

        if gwcomp_config.has_option('condor', 'arch'):
            self.add_condor_cmd('+arch', gwcomp_config.get('condor', 'arch'))

        if gwcomp_config.has_option('condor', 'gwcomp_residuals-request-memory'):
            self.add_condor_cmd('request_memory',
                                gwcomp_config.get('condor', 'gwcomp_residuals-request-memory'))

        if gwcomp_config.has_option('condor', 'gwcomp_residuals-request-disk'):
            self.add_condor_cmd('request_disk',
                                gwcomp_config.get('condor', 'gwcomp_residuals-request-disk'))

        if gwcomp_config.has_option('condor', 'bayeswave-cit-nodes'):
            self.add_condor_cmd('+BayesWaveCgroup', 'True')
            self.add_condor_cmd('Rank', '(TARGET.BayesWaveCgroup =?= True)')

        if gwcomp_config.has_option('condor', 'environment'):
            self.add_condor_cmd('environment', gwcomp_config.get('condor', 'environment'))

        transfer_string = 'datafind,make_res_cache.py,%s,residual_frame' % peFile
        for psdf in list(psdFiles.values()):
            transfer_string = transfer_string + "," + psdf

        self.add_condor_cmd('transfer_input_files', transfer_string)
        self.add_condor_cmd('transfer_output_files', 'residual_frame,datafind')

        write_res_post_cmd(res_workdir, list(psdFiles.keys()))
        self.add_condor_cmd("+PostCmd", '"make_res_cache.py"')

        self.add_opt('frame-cache', ' '.join(list(cacheFiles.values())))


class gwcomp_residualsNode(pipeline.CondorDAGNode, pipeline.AnalysisNode):
    def __init__(self, gwcomp_residuals_job):
        pipeline.CondorDAGNode.__init__(self, gwcomp_residuals_job)
        pipeline.AnalysisNode.__init__(self)

    def set_li_samples_file(self, li_samples_file):
        self.add_var_opt('li-samples', li_samples_file)
        self.li_samples_file = li_samples_file

    def set_input_channel(self, input_channel_list):
        self.add_var_opt('input-channel', ' '.join(input_channel_list))

    def set_output_channel(self, output_channel_list):
        self.add_var_opt('output-channel', ' '.join(output_channel_list))

    def set_output_frame(self, output_frame_list):
        self.add_var_opt('output-frame-type', ' '.join(output_frame_list))

    def set_psd_files(self, psd_files):
        self.add_var_opt('psd-files', ' '.join(psd_files))
        self.psd_files = psd_files

    def set_asd_file_flag(self):
        self.add_var_opt('is-asd-file', '')

    def set_srate(self, srate):
        self.add_var_opt('srate', srate)

    def set_li_epoch(self, li_epoch):
        self.add_var_opt('epoch', li_epoch)

    def set_trigtime(self, trigtime):
        self.add_var_opt('trigtime', trigtime)

    def set_approx(self, approx):
        self.add_var_opt('approx', approx)

    def set_duration(self, duration):
        self.add_var_opt('duration', duration)

    def set_output_dir(self, output_dir):
        self.add_var_opt('output-path', output_dir)

    def set_make_plots_flag(self):
        self.add_var_opt('make-plots', '')

    def set_make_omega_scans_flag(self):
        self.add_var_opt('make-omega-scans', '')

    def set_flow(self, flow):
        self.add_var_opt('flow', flow)

    def set_ifos(self, ifos):
        self.add_var_opt('ifos', ' '.join(ifos))

    def set_choose_fd_flag(self):
        self.add_var_opt('choose-fd', '')

    def set_fref(self, fref):
        self.add_var_opt('fref', fref)

    def set_amp_order(self, amp_order):
        self.add_var_opt('amp-order', amp_order)

    def set_phase_order(self, phase_order):
        self.add_var_opt('phase-order', phase_order)
