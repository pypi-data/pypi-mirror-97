#!/usr/bin/env python     
# -*- coding: utf-8 -*-     
# Copyright (C) 2016-2017 James Clark <james.clark@ligo.org>     
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
import random
import shutil
import socket
import subprocess
import sys
import traceback
import numpy as np
from glue import pipeline
from glue.ligolw import ligolw
from glue.ligolw import lsctables
from glue.ligolw import utils as ligolw_utils

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


def write_pre_cmd(workdir):
    """
    Returns a string with a script for job setup and and geolocaiton which runs
    as a PreCmd.  Output is dumped to a file called <identifier>_cehostname.txt

    >>> write_pre_cmd("trigtime_123", "BayesWave")

    Creates a file: BayesWave_cehostname.txt
    """

    script = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018-2019 James Clark <james.clark@ligo.org>
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
\"\"\"Compute element hostname.

Creates the output directory for a BayesWave job and prints the name of the
GLIDEIN gatekeeper for OSG jobs.  Prints the name of the local host if not a
GLIDEIN.

The hostname identification comes from:
    https://opensciencegrid.org/user-school-2017/#materials/day2/part1-ex3-submit-osg/

Note that we could use many more env variables for similar purposes if needed.
\"\"\"

import re
import os,sys
import socket

#
# Preliminary setup
#
outputDir=sys.argv[1]
executable=sys.argv[2]
if not os.path.exists(outputDir): os.makedirs(outputDir)
geolocation=open("{0}/{1}_cehostname.txt".format(outputDir, executable), "w")

#
# Geolocation
#
machine_ad_file_name = os.getenv('_CONDOR_MACHINE_AD')
try:
    machine_ad_file = open(machine_ad_file_name, 'r')
    machine_ad = machine_ad_file.read()
    machine_ad_file.close()
except TypeError:
    host = socket.getfqdn()+"\\n"
    geolocation.writelines(host)
    geolocation.close()
    exit(0)

try:
    host = re.search(r'GLIDEIN_Gatekeeper = "(.*):\d*/jobmanager-\w*"', machine_ad, re.MULTILINE).group(1) 
except AttributeError:
    try:
        host = re.search(r'GLIDEIN_Gatekeeper = "(\S+) \S+:9619"', machine_ad, re.MULTILINE).group(1)
    except AttributeError:
        host = socket.getfqdn()
geolocation.writelines(host+"\\n")
geolocation.close()
exit(0)

"""
    with open(os.path.join(workdir, "setupdirs.py"), 'w') as prefile:
        prefile.writelines(script)
        prefile.close()
    os.chmod(os.path.join(workdir, "setupdirs.py"), 0o755)

    return


#
# Convenience Defs
#
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def hyphen_range(s):
    """
    yield each integer from a complex range string like "1-9,12, 15-20,23"

    Stolen from:
    http://code.activestate.com/recipes/577279-generate-list-of-numbers-from-hyphenated-and-comma/
    """

    for x in s.split(','):
        elem = x.split('-')
        if len(elem) == 1:  # a number
            yield int(elem[0])
        elif len(elem) == 2:  # a range inclusive
            start, end = map(int, elem)
            for i in xrange(start, end + 1):
                yield i
        else:  # more than one hyphen
            raise ValueError('format error in %s' % x)


def x509_manipulation(workdir):
    """ 
    Copy x509 proxy cert to the working directory and return its location
    """

    try:
        print("Trying to get X509 location from grid-proxy-info")
        x509 = subprocess.check_output('grid-proxy-info -path', shell=True)
    except subprocess.CalledProcessError:
        print("Trying to get X509 location from X509_USER_PROXY")
        try:
            x509 = os.environ['X509_USER_PROXY']
        except KeyError:
            traceback.print_exc(file=sys.stderr)
            print("Warning: No X509 proxy found, please run ligo-proxy-init")
    x509 = str(x509.decode("utf-8").rstrip())

    # Copy X509 to workdir and return the new path

    x509_name = os.path.basename(x509)
    x509_new = os.path.join(workdir, x509_name)

    shutil.copy(x509, x509_new)

    print("Jobs will use X509_USER_PROXY={}".format(x509_new))

    return x509_new


class eventTrigger:
    """
    Stores event characteristics and determines run configuration for this event
    """

    def __init__(self, cp, trigger_time=None, hl_time_lag=0.0, hv_time_lag=0.0, lv_time_lag=0.0,
                 trigger_frequency=None, rho=None, graceID=None, gdb_playground=False, injevent=None,
                 frequency_threshold=200., default_srate=1024., min_srate=1024.,
                 max_srate=4096., default_seglen=4., max_seglen=4., min_seglen=2.,
                 default_flow=16., max_flow=64., min_flow=16., default_window=1.0,
                 min_window=0.5, max_window=1.0, veto1=None, veto2=None,
                 BW_event=None):

        #
        # Get run configuration
        #
        try:
            self.frequency_threshold = cp.getfloat('input', 'frequency-threshold')
        except:
            self.frequency_threshold = frequency_threshold

        try:
            self.default_srate = cp.getfloat('input', 'srate')
        except:
            self.default_srate = default_srate

        try:
            self.min_srate = cp.getfloat('input', 'min-srate')
        except:
            self.min_srate = default_srate

        try:
            self.max_srate = cp.getfloat('input', 'max-srate')
        except:
            self.max_srate = default_srate

        assert self.min_srate <= self.max_srate, "ERROR: min-srate > max-srate"

        try:
            self.default_seglen = cp.getfloat('input', 'seglen')
        except:
            self.default_seglen = default_seglen

        try:
            self.max_seglen = cp.getfloat('input', 'max-seglen')
        except:
            self.max_seglen = default_seglen

        try:
            self.min_seglen = cp.getfloat('input', 'min-seglen')
        except:
            self.min_seglen = default_seglen

        assert self.min_seglen <= self.max_seglen, "ERROR: min-seglen > max-seglen"

        try:
            self.default_flow = cp.getfloat('input', 'flow')
        except:
            self.default_flow = default_flow

        try:
            self.max_flow = cp.getfloat('input', 'max-flow')
        except:
            self.max_flow = default_flow

        try:
            self.min_flow = cp.getfloat('input', 'min-flow')
        except:
            self.min_flow = default_flow

        assert self.min_flow <= self.max_flow, "ERROR: min-flow > max-flow"

        try:
            self.default_window = cp.getfloat('input', 'window')
        except:
            self.default_window = default_window

        try:
            self.max_window = cp.getfloat('input', 'max-window')
        except:
            self.max_window = default_window

        try:
            self.min_window = cp.getfloat('input', 'min-window')
        except:
            self.min_window = default_window

        assert self.min_window <= self.max_window, "ERROR: min-window > max-window"
        #
        # Add trigger properties
        #
        self.trigger_time = trigger_time
        self.hl_time_lag = hl_time_lag
        self.hv_time_lag = hv_time_lag
        self.lv_time_lag = lv_time_lag
        self.trigger_frequency = trigger_frequency

        # Variable sample rate / window length [fixed TF volume]

        if trigger_frequency is not None:
            # Adjust sample rate for this trigger
            # - min srate => max_seglen
            # - max srate => min_seglen
            if trigger_frequency < self.frequency_threshold:
                self.srate = self.min_srate
                self.seglen = self.max_seglen
                self.window = self.max_window
                self.flow = self.min_flow
            else:
                self.srate = self.max_srate
                self.seglen = self.min_seglen
                self.window = self.min_window
                self.flow = self.max_flow
        else:
            self.srate = self.default_srate
            self.seglen = self.default_seglen
            self.window = self.default_window
            self.flow = self.default_flow

        self.rho = rho
        self.injevent = injevent

        self.veto1 = veto1
        self.veto2 = veto2

        self.BW_event = BW_event

        #
        # GraceDB Support
        #

        # If graceID is given, override other trigger values
        self.graceID = graceID
        if graceID is not None:
            self.query_graceDB(graceID, gdb_playground=gdb_playground)

    #
    # Update trigger properties
    #
    def set_injevent(self, injevent):
        self.injevent = injevent

    def query_graceDB(self, graceid, gdb_playground=False):

        from ligo.gracedb.rest import GraceDb

        # Instantiate graceDB event
        if gdb_playground:
            gracedb = GraceDb("https://gracedb-playground.ligo.org/api/")
        else:
            gracedb = GraceDb()
        event = gracedb.event(graceid)
        event_info = event.json()

        # First check for olib info
        if event_info['submitter'] == 'oLIB':
            try:
                self.rho = event_info['extra_attributes']['LalInferenceBurst']['bci']
                # put bci in the place of rho for bookkeping
            except KeyError:
                print >> sys.stderr, \
                "graceDB UID %s has no MultiBurst snr attribute" % (graceid)

            # Set time
            self.trigger_time = event_info['gpstime']

            # Set frequency
            try:
                self.trigger_frequency = \
                    event_info['extra_attributes']['LalInferenceBurst']['frequency_median']

                if self.trigger_frequency < self.frequency_threshold:
                    self.srate = self.min_srate
                    self.seglen = self.max_seglen
                    self.window = self.max_window
                    self.flow = self.min_flow
                else:
                    self.srate = self.max_srate
                    self.seglen = self.min_seglen
                    self.window = self.min_window
                    self.flow = self.max_flow

            except KeyError:
                print >> sys.stderr, \
                "graceDB UID %s has no MultiBurst central_freq attribute" % (graceid)
                print >> sys.stderr, "...using default sample rate"
                self.srate = self.default_srate

        else:
            # Assume it's cwb trigger
            # Get loudness (for informational, not analysis, purposes)
            try:
                self.rho = event_info['extra_attributes']['MultiBurst']['snr']
            except KeyError:
                print >> sys.stderr, \
                "graceDB UID %s has no MultiBurst snr attribute" % (graceid)

            # Set time
            self.trigger_time = event_info['gpstime']

            # Set frequency
            try:
                self.trigger_frequency = \
                    event_info['extra_attributes']['MultiBurst']['central_freq']

                if self.trigger_frequency < self.frequency_threshold:
                    self.srate = self.min_srate
                    self.seglen = self.max_seglen
                    self.window = self.max_window
                    self.flow = self.min_flow
                else:
                    self.srate = self.max_srate
                    self.seglen = self.min_seglen
                    self.window = self.min_window
                    self.flow = self.max_flow

            except KeyError:
                print >> sys.stderr, \
                "graceDB UID %s has no MultiBurst central_freq attribute" % (graceid)
                print >> sys.stderr, "...using default sample rate"
                self.srate = self.default_srate


class triggerList:
    """
    Object to store trigger properties and associated configuration

    Allowed formats:
        trigger_gps 
        trigger_gps | hl_time_lag
        trigger_gps | hl_time_lag | trigger_frequency
        trigger_gps | hl_time_lag | trigger_frequency | rho
    """

    def __init__(self, cp, gps_times=None, trigger_file=None,
                 injection_file=None, followup_injections=None,
                 cwb_trigger_file=None, rho_threshold=-1.0,
                 internal_injections=False, graceIDs=None, gdb_playground=False):

        #
        # Assign trigger data
        #
        if gps_times is not None and not internal_injections:
            # Create trigger list from gps times
            self.triggers = list()
            for gps_time in gps_times:
                self.triggers.append(eventTrigger(cp, trigger_time=gps_time))

        elif trigger_file is not None and not internal_injections:
            # Create trigger list from ascii file
            self.triggers = self.parse_trigger_list(cp, trigger_file)

        elif injection_file is not None:
            # Create trigger list from sim* LIGOLW-XML table
            self.triggers = self.parse_injection_file(cp, injection_file,
                                                      followup_injections=followup_injections)

        elif cwb_trigger_file is not None:
            # Create trigger list from cwb triggers
            self.triggers = self.parse_cwb_trigger_list(cp, cwb_trigger_file)

        elif internal_injections:
            # Set up || runs to sample from the prior
            self.triggers = self.build_internal_injections(cp, gps_times, trigger_file)

        elif graceIDs is not None:
            # Create trigger list from graceDB queries
            self.triggers = self.parse_graceDB_triggers(cp, graceIDs, gdb_playground=gdb_playground)

        else:
            # Fail
            print("don't know what to do.", file=sys.stdout)
            sys.exit()

    def parse_graceDB_triggers(self, cp, graceIDs, gdb_playground=False):

        triggers = []
        for graceid in graceIDs:
            triggers.append(eventTrigger(cp, graceID=graceid, gdb_playground=gdb_playground))

        return triggers

    def build_internal_injections(self, cp, gps_time=None, trigger_file=None):

        # Determine chain length
        injtype = cp.get('bayeswave_options', 'BW-inject')
        try:
            injname = cp.get('bayeswave_options', 'BW-injName')
            injname += '_'
        except:
            injname = ''

        try:
            BW_chainLength = cp.getint('bayeswave_options', 'BW-chainLength')
        except configparser.NoOptionError:

            print("Reading chainlength from files in %s" % (
                cp.get('bayeswave_options', 'BW-path')), file=sys.stdout)

            # O1 names:
            if injtype == 'glitch':
                filename = injname + 'glitch_glitchchain_ifo0.dat.0'
            else:
                filename = injname + 'signal_wavechain.dat.0'
            filename = os.path.join(cp.get('bayeswave_options', 'BW-path'), filename)

            try:
                # O1 names
                o1 = os.path.exists(filename)
                if not o1:
                    raise ValueError(
                        "o1 style chain-names not found,trying o2-style")
            except:
                # O2 names:
                if injtype == 'glitch':
                    filename = injname + 'glitch_params_ifo0.dat.0'
                else:
                    filename = injname + 'signal_params.dat.0'
                filename = os.path.join(cp.get('bayeswave_options', 'BW-path'), filename)

            BW_chainLength = file_len(filename)

        # User specified injection indices
        if cp.has_option('bayeswave_options', 'BW-internal-events'):
            events = cp.get('bayeswave_options', 'BW-internal-events')

            if events != 'all':
                BW_events = list(hyphen_range(events))
            else:
                BW_events = range(0, BW_chainLength)

        else:
            try:
                BW_Nsamples = cp.getint('bayeswave_options', 'BW-Nsamples')
            except:
                print("Error: must specify either BW-Nsamples or BW-internal-events.")
                sys.exit(1)
            try:
                BW_seed = cp.getint('bayeswave_options', 'BW-seed')
            except:
                BW_seed = None

            random.seed(BW_seed)
            BW_events = random.sample(xrange(0, BW_chainLength), BW_Nsamples)

        if trigger_file is not None:  # injecting into specific GPS times from a list
            print("Injecting int gps times specified by trigger file.")
            trigger_data = np.loadtxt(trigger_file, ndmin=2)
            nrows, ncols = trigger_data.shape

            if ncols == 1:
                trig_times = []
                for i in xrange(nrows):
                    trig_times.append(trigger_data[i])
            else:
                print("Warning: GPS file has more than one column. Using first column to set GPS times.")
        elif gps_time is not None:  # Use a single GPS time for injections
            # A little bit of a hack here, but it's the most straightforward thing I could think of:
            #   For injections without a trigger list of GPS times, cope the single gps time to be used into a list.
            trig_times = [gps_time for ii in range(BW_chainLength)]
        else:
            print("Could not find GPS time for BW internal injections.")
            sys.exit(1)

        triggers = []
        for BW_event in BW_events:
            triggers.append(eventTrigger(cp, trigger_time=trig_times[BW_event],
                                         BW_event=BW_event))

        return triggers

    def parse_injection_file(self, cp, injection_file, followup_injections=None,
                             injwindow=2.0):

        xmldoc = ligolw_utils.load_filename(injection_file, contenthandler=
        LIGOLWContentHandler, verbose=True)
        sim_inspiral_table = lsctables.SimInspiralTable.get_table(xmldoc)

        geocent_end_time = \
            sim_inspiral_table.getColumnByName('geocent_end_time')
        geocent_end_time_ns = \
            sim_inspiral_table.getColumnByName('geocent_end_time_ns')

        injection_times = geocent_end_time.asarray() + \
                          1e-9 * geocent_end_time_ns.asarray()

        print("..read %d injections" % len(injection_times))

        triggers = []
        if followup_injections is None:

            print('downsampling to requested injections using events= in config')

            # reduce to specified values
            events = cp.get('injections', 'events')

            if events != 'all':
                injevents = list(hyphen_range(events))
            else:
                injevents = range(len(injection_times))

            for i in injevents:
                triggers.append(eventTrigger(cp, trigger_time=injection_times[i],
                                             injevent=i))

        else:

            # Parse the detected injections

            print("downsampling to events listed in %s" % followup_injections)
            trigger_list_from_file = triggerList(cp,
                                                 trigger_file=followup_injections)

            # Find corresponding injection events
            for trigger in trigger_list_from_file.triggers:
                injevent = np.concatenate(np.argwhere(
                    abs(trigger.trigger_time - injection_times) < injwindow))[0]

                trigger.set_injevent(injevent)

                triggers.append(trigger)

        return triggers

    def parse_cwb_trigger_list(self, cp, cwb_trigger_file, rho_threshold=-1.0,
                               keep_frac=1.0):

        # Get rho threshold
        try:
            rho_threshold = cp.getfloat('input', 'rho-threshold')
        except:
            rho_threshold = rho_threshold

        # Determine network
        ifo_list = ast.literal_eval(cp.get('input', 'ifo-list'))
        if 'H1' in ifo_list:
            network = 'H'
            if 'L1' in ifo_list:
                network += 'L'
            if 'V1' in ifo_list:
                network += 'V'
        elif 'L1' in ifo_list:
            network = 'L'
            if 'V1' in ifo_list:
                network += 'V'
        else:
            print("Error setting up timeslides from cWB trigger list. Please check IFO list.", file=sys.stderr)

        print("Network: {}".format(network), file=sys.stdout)

        print("Discarding rho<=%f" % rho_threshold, file=sys.stdout)

        if network == 'HL':

            names = ['veto1', 'veto2', 'rho', 'cc1', 'cc2', 'cc3', 'amp', 'tshift',
                     'tsupershift', 'like', 'penalty', 'disbalance', 'f',
                     'bandwidth', 'duration', 'pixels', 'resolution', 'runnumber',
                     'Lgps', 'Hgps', 'sSNRL', 'sSNRH', 'hrssL', 'hrssH', 'phi',
                     'theta', 'psi']

        elif network == 'HV':

            names = ['veto1', 'veto2', 'rho', 'cc1', 'cc2', 'cc3', 'amp', 'tshift',
                     'tsupershift', 'like', 'penalty', 'disbalance', 'f',
                     'bandwidth', 'duration', 'pixels', 'resolution', 'runnumber',
                     'Hgps', 'Vgps', 'sSNRH', 'sSNRV', 'hrssH', 'hrssV', 'phi',
                     'theta', 'psi']

        elif network == 'LV':

            names = ['veto1', 'veto2', 'rho', 'cc1', 'cc2', 'cc3', 'amp', 'tshift',
                     'tsupershift', 'like', 'penalty', 'disbalance', 'f',
                     'bandwidth', 'duration', 'pixels', 'resolution', 'runnumber',
                     'Lgps', 'Vgps', 'sSNRL', 'sSNRV', 'hrssL', 'hrssV', 'phi',
                     'theta', 'psi']

        elif network == 'HLV':

            names = ['veto1', 'veto2', 'rho', 'cc1', 'cc2', 'cc3', 'amp', 'tshift',
                     'tsupershift', 'like', 'penalty', 'disbalance', 'f',
                     'bandwidth', 'duration', 'pixels', 'resolution', 'runnumber',
                     'Lgps', 'Hgps', 'Vgps', 'sSNRL', 'sSNRH', 'sSNRV', 'hrssL',
                     'hrssH', 'hrssV', 'phi', 'theta', 'psi']

        data = np.recfromtxt(cwb_trigger_file, names=names)

        if network == 'HL':

            Hgps = data['Hgps']
            Lgps = data['Lgps']

            HLlagList = []
            for h, l in zip(Hgps, Lgps):
                HLlagList.append(round(h - l))

            # Dummy list of nan
            HVlagList = [0] * len(HLlagList)

        elif network == 'HV':

            Hgps = data['Hgps']
            Vgps = data['Vgps']

            HVlagList = []
            for h, v in zip(Hgps, Vgps):
                HVlagList.append(round(h - v))

                # Dummy list of nan
            HLlagList = [0] * len(HVlagList)

        elif network == 'LV':

            Lgps = data['Lgps']
            Vgps = data['Vgps']

            LVlagList = []
            for l, v in zip(Lgps, Vgps):
                LVlagList.append(round(l - v))

                # Dummy list of nan
            HVlagList = [0] * len(LVlagList)

        elif network == 'HLV':

            Hgps = data['Hgps']
            Lgps = data['Lgps']
            Vgps = data['Vgps']

            HLlagList = []
            for h, l in zip(Hgps, Lgps):
                HLlagList.append(round(h - l))

            HVlagList = []
            for h, v in zip(Hgps, Vgps):
                HVlagList.append(round(h - v))

        rhoList = data['rho']
        freqList = data['f']

        plusveto = data['veto1']
        minusveto = data['veto2']

        # Trigger time given by H1 time, or L1 in the case of an LV network
        try:
            gpsList = Hgps
        except:
            gpsList = Lgps

        triggers = []

        if 'H' in network:
            for gps, hl_lag, hv_lag, freq, rho, veto1, veto2 in zip(gpsList,
                                                                    HLlagList, HVlagList, freqList, rhoList, plusveto,
                                                                    minusveto):

                # Apply rho threshold
                if rho < rho_threshold: continue

                triggers.append(eventTrigger(cp,
                                             trigger_time=gps,
                                             hl_time_lag=hl_lag,
                                             hv_time_lag=hv_lag,
                                             trigger_frequency=freq,
                                             rho=rho,
                                             veto1=veto1,
                                             veto2=veto2))

        else:
            for gps, lv_lag, hv_lag, freq, rho, veto1, veto2 in zip(gpsList,
                                                                    LVlagList, HVlagList, freqList, rhoList, plusveto,
                                                                    minusveto):

                # Apply rho threshold
                if rho < rho_threshold: continue

                triggers.append(eventTrigger(cp,
                                             trigger_time=gps,
                                             lv_time_lag=lv_lag,
                                             hv_time_lag=hv_lag,
                                             trigger_frequency=freq,
                                             rho=rho,
                                             veto1=veto1,
                                             veto2=veto2))

        # Finally, downsample to a smaller fraction of triggers
        try:
            keep_frac = cp.getfloat('input', 'keep-frac')
        except:
            keep_frac = keep_frac

        nall = len(triggers)
        nkeep = int(np.ceil(keep_frac * nall))
        keepidx = random.sample(range(0, len(triggers)), nkeep)
        triggers_out = [triggers[i] for i in sorted(keepidx)]

        print("Read %d triggers, following up %d" % (
            nall, len(triggers_out)), file=sys.stdout)

        return triggers_out

    def parse_trigger_list(self, cp, trigger_file, rho_threshold=-1.0,
                           keep_frac=1.0):

        trigger_data = np.loadtxt(trigger_file, ndmin=2)
        nrows, ncols = trigger_data.shape

        triggers = list()

        if ncols == 1:
            # Just have trigger time
            for i in xrange(nrows):
                triggers.append(eventTrigger(cp,
                                             trigger_time=trigger_data[i]))

        elif ncols == 2:
            # Trigger time, hl_lag
            for i in xrange(nrows):
                triggers.append(eventTrigger(cp,
                                             trigger_time=trigger_data[i, 0],
                                             hl_time_lag=trigger_data[i, 1]))

        elif ncols == 3:
            # Trigger time, hl_lag, frequency
            for i in xrange(nrows):
                triggers.append(eventTrigger(cp,
                                             trigger_time=trigger_data[i, 0],
                                             hl_time_lag=trigger_data[i, 1],
                                             trigger_frequency=trigger_data[i, 2]))

        elif ncols == 4:
            print("""WARNING: Looks like you're using an old style cwb trigger
                    list.  Success is not guarenteed""", file=sys.stderr)
            # Trigger time, hl_lag, frequency, rho
            try:
                rho_threshold = cp.getfloat('input', 'rho-threshold')
            except:
                rho_threshold = rho_threshold

            print("Discarding rho<=%f" % rho_threshold, file=sys.stdout)

            for i in xrange(nrows):
                # Apply rho threshold
                if trigger_data[i, 3] < rho_threshold: continue
                triggers.append(eventTrigger(cp,
                                             trigger_time=trigger_data[i, 0],
                                             hl_time_lag=trigger_data[i, 1],
                                             trigger_frequency=trigger_data[i, 2],
                                             rho=trigger_data[i, 3]))

        # Finally, downsample to a smaller fraction of triggers
        try:
            keep_frac = cp.getfloat('input', 'keep-frac')
        except:
            keep_frac = keep_frac

        nkeep = int(np.ceil(keep_frac * len(triggers)))
        keepidx = random.sample(range(0, len(triggers)), nkeep)
        triggers_out = [triggers[i] for i in sorted(keepidx)]

        print("Read %d triggers, following up %d" % (
            nrows, len(triggers_out)), file=sys.stdout)

        return triggers_out

    # -- END trigger_list class


#
# Condor Definitions
#

def condor_job_config(job_type, condor_job, config_parser):
    """
    Configure the condor job executable and environment for one of:
     * job_type='bayeswave'
     * job_type='bayeswave_post'
     * job_type='bayeswave_fpeak'
     * job_type='bayeswave_clean_frame'
     * job_type='megaplot.py'
     * job_type='megasky.py'

    This identifies the site (OSG vs LDG) and set properties of the condor job
    (file transfers, executable location etc) accordingly

    """
    valid_job_types = ['bayeswave', 'bayeswave_post', 'bayeswave_fpeak', 'bayeswave_clean_frame', 'megasky', 'megaplot']
    try:
        job_index = valid_job_types.index(job_type)
    except ValueError:
        print("unrecognized job type", file=sys.stderr)

    # --- Set executable and choose singularity image
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

    #
    # File Transfer configuration
    #
    if config_parser.getboolean('condor', 'transfer-files'):
        print("Configuring file transfers for {}".format(job_type), file=sys.stdout)
        condor_job.add_condor_cmd('should_transfer_files', 'YES')
        condor_job.add_condor_cmd("transfer_executable", False)

        # Only checkpoitn bayeswave jobs
        if job_type == 'bayeswave':

            #
            # Checkpoint configuration
            #
            # See:
            # https://htcondor-wiki.cs.wisc.edu/index.cgi/wiki?p=HowToRunSelfCheckpointingJobs

            # Using +SuccessCheckpointExitCode (recommended approach)
            if job_type == 'bayeswave':
                condor_job.add_condor_cmd('+SuccessCheckpointExitCode', 77)
                condor_job.add_condor_cmd('+WantFTOnCheckpoint', True)

            # "Working Around The Assumptions"

            # 
            # condor_job.add_condor_cmd('+SuccessCheckpointExitBySignal', True) #  
            # condor_job.add_condor_cmd('+SuccessCheckpointExitSignal', '"SIGTERM"')
            # condor_job.add_condor_cmd('+CheckpointExitSignal', '"SIGTERM"')

            # "Delayed Transfers" (strongly discouraged)
            # condor_job.add_condor_cmd('+WantCheckpointSignal', True)
            # condor_job.add_condor_cmd('+CheckpointSig', '"SIGINT"')
            # condor_job.add_condor_cmd('when_to_transfer_output', 'ON_EXIT_OR_EVICT')
        else:
            condor_job.add_condor_cmd('when_to_transfer_output', 'ON_EXIT')

        # Time limit before job self-evicts to preserve checkpointing
        #       hstr = '(JobStatus == 2) && (time() - EnteredCurrentStatus > {})'.format(
        #               config_parser.get('condor', 'max-runtime'))
        #       condor_job.add_condor_cmd('periodic_hold', hstr)
        #       condor_job.add_condor_cmd('periodic_hold_subcode', '12345')
        #       rstr = '(JobStatus == 5) && (time() - EnteredCurrentStatus > {}) && (PeriodicHoldSubCode =?= 12345)'.format(
        #               config_parser.get('condor', 'resume-time'))
        #       condor_job.add_condor_cmd('periodic_release', rstr)

        # Enable stdout / stderr streaming
        condor_job.add_condor_cmd('stream_output', True)
        condor_job.add_condor_cmd('stream_error', True)

    #
    # OSG specific configuration
    #
    if config_parser.getboolean('condor', 'osg-deploy'):
        # --- Force downstream jobs to run locally
        if job_type in ['bayeswave_post', 'bayeswave_fpeak', 'bayeswave_clean_frame',
                        'megaplot.py', 'megasky.py']:
            requires.append("(GLIDEIN_SITE=?=undefined)")
        else:
            try:
                condor_job.add_condor_cmd('+DESIRED_Sites',
                                          config_parser.get('condor', 'desired-sites'))
            except configparser.NoOptionError:
                pass
            try:
                condor_job.add_condor_cmd('+UNDESIRED_Sites',
                                          config_parser.get('condor', 'undesired-sites'))
            except configparser.NoOptionError:
                pass

            # Ensure LIGO data is present 
            if not config_parser.getboolean('datafind', 'sim-data'):
                requires.append("(HAS_LIGO_FRAMES=?=TRUE)")
            #
            # Accounting configurations
            #
            workdir = os.getcwd()
            x509 = x509_manipulation(os.getcwd())
            condor_job.add_condor_cmd('x509userproxy', x509)

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


class bayeswaveJob(pipeline.CondorDAGJob, pipeline.AnalysisJob):

    def __init__(self, cp, cacheFiles, injfile=None, numrel_data=None,
                 dax=False):

        #
        # [condor]: Common workflow configuration
        #
        condor_job_config('bayeswave', self, cp)

        workdir = os.getcwd()
        self.add_condor_cmd('initialdir', workdir)
        self.set_sub_file(os.path.join(workdir, 'bayeswave.sub'))

        self.set_stdout_file(os.path.join(workdir, 'logs',
                                          'BayesWave_$(macrooutputDir)-$(cluster)-$(process).out'))
        self.set_stderr_file(os.path.join(workdir, 'logs',
                                          'BayesWave_$(macrooutputDir)-$(cluster)-$(process).err'))
        self.set_log_file(os.path.join(workdir, 'logs',
                                       'BayesWave_$(macrooutputDir)-$(cluster)-$(process).log'))

        if cp.has_option('condor', 'arch'):
            self.add_condor_cmd('+arch', cp.get('condor', 'arch'))

        # --- Additional CIT configuration:
        if cp.has_option('condor', 'bayeswave-request-memory'):
            self.add_condor_cmd('request_memory',
                                cp.get('condor', 'bayeswave-request-memory'))

        if cp.has_option('condor', 'bayeswave-request-disk'):
            self.add_condor_cmd('request_disk',
                                cp.get('condor', 'bayeswave-request-disk'))

        if cp.has_option('condor', 'bayeswave-cit-nodes'):
            self.add_condor_cmd('+BayesWaveCgroup', 'True')
            self.add_condor_cmd('Rank', '(TARGET.BayesWaveCgroup =?= True)')

        # --- Self-checkpointing
        if cp.has_option('condor', 'checkpoint'):
            self.add_opt('checkpoint', cp.get('condor', 'checkpoint'))

        # --- Environment
        if cp.has_option('condor', 'environment'):
            self.add_condor_cmd('environment', cp.get('condor', 'environment'))

        #
        # File Transfers
        #
        if cp.getboolean('condor', 'transfer-files'):

            # Generate a script for PreCmd to setup directory structure
            write_pre_cmd(workdir)
            self.add_condor_cmd("+PreCmd", '"setupdirs.py"')
            self.add_condor_cmd("+PreArgs", '"$(macrooutputDir) bayeswave"')

            # Configure file transfers
            transferstring = 'datafind,setupdirs.py'

            if cp.getboolean('condor', 'copy-frames'):
                transferstring += ',$(macroframes)'

            if injfile is not None:
                transferstring += ',' + injfile
            if numrel_data is not None:
                transferstring += ',' + numrel_data

            if cp.has_option('condor', 'extra-files'):
                # allow specification of additional files to transfer
                transferstring += ',%s' % cp.get('condor', 'extra-files')

            self.add_condor_cmd('transfer_input_files', transferstring)
            self.add_condor_cmd('transfer_output_files', '$(macrooutputDir)')

        #
        # [input], [datafind]: Data configuration
        #
        ifo_list = ast.literal_eval(cp.get('input', 'ifo-list'))
        if not cp.getboolean('datafind', 'sim-data'):
            channel_list = ast.literal_eval(cp.get('datafind', 'channel-list'))

        # Hack to repeat option for --ifo H1 --ifo L1 etc
        ifo_list_opt = ifo_list[0]
        for ifo in ifo_list[1:]: ifo_list_opt += ' --ifo {0}'.format(ifo)
        self.add_opt('ifo', ifo_list_opt)

        self.add_opt('psdlength', cp.get('input', 'PSDlength'))

        for ifo in ifo_list:
            self.add_opt('{ifo}-cache'.format(ifo=ifo), cacheFiles[ifo])

            if not cp.getboolean('datafind', 'sim-data'):
                # only specify channels for real data
                self.add_opt('{ifo}-channel'.format(ifo=ifo), channel_list[ifo])

            if cp.has_option('input', 'fhigh'):
                self.add_opt('{ifo}-fhigh'.format(ifo=ifo), cp.get('input', 'fhigh'))

        # Find PSD files for pre-computed estimates
        if cp.has_option('datafind', 'psd-files'):
            psdFiles = ast.literal_eval(cp.get('datafind', 'psd-files'))
            for ifo in ifo_list:
                self.add_opt('{ifo}-psd'.format(ifo=ifo), psdFiles[ifo])

        #
        # [bayeswave_options]: Algorithm configuration 
        #
        for item in cp.items('bayeswave_options'):
            # Add any option and value which exists
            self.add_opt(item[0], item[1])

        #
        # [injections]: injection configuration
        #

        # --- LALSimulation options
        # Injection file
        if injfile is not None:
            injfile = os.path.join('..', injfile)
            self.add_opt('inj', injfile)

        # NR file
        if numrel_data is not None:
            numrel_data = os.path.join('..', numrel_data)
            self.add_opt('inj-numreldata', numrel_data)

        # --- MDC-style injection configuration

        # mdc-cache
        if cp.has_option('injections', 'mdc-cache'):
            mdc_cache_list = str(['../datafind/MDC.cache' for ifo in
                                  ifo_list]).replace("'", '')
            mdc_cache_list = mdc_cache_list.replace(' ', '')
            self.add_opt('MDC-cache', mdc_cache_list)

        # mdc-channels
        if cp.has_option('injections', 'mdc-channels'):
            mdc_channel_list = ast.literal_eval(cp.get('injections', 'mdc-channels'))
            mdc_channel_str = str(mdc_channel_list.values()).replace("'", '')
            mdc_channel_str = mdc_channel_str.replace(' ', '')
            self.add_opt('MDC-channel', mdc_channel_str)

        # mdc-prefactor
        if cp.has_option('injections', 'mdc-prefactor'):
            self.add_opt('MDC-prefactor', cp.get('injections', 'mdc-prefactor'))


class bayeswaveNode(pipeline.CondorDAGNode, pipeline.AnalysisNode):

    def __init__(self, bayeswave_job):

        pipeline.CondorDAGNode.__init__(self, bayeswave_job)
        pipeline.AnalysisNode.__init__(self)

    def set_trigtime(self, trigtime):
        self.add_var_opt('trigtime', '%.9f' % trigtime)
        self.trigtime = trigtime

    def set_segment_start(self, segment_start):
        self.add_var_opt('segment-start', '%.9f' % segment_start)
        self.segment_start = segment_start

    def set_srate(self, srate):
        self.add_var_opt('srate', srate)
        self.srate = srate

    def set_seglen(self, seglen):
        self.add_var_opt('seglen', seglen)
        self.seglen = seglen

    def set_flow(self, ifo_list, flow):
        for i, ifo in enumerate(ifo_list):
            self.add_var_opt('{ifo}-flow'.format(ifo=ifo), flow)
        self.flow = flow

    def set_window(self, window):
        self.add_var_opt('window', window)
        self.window = window

    def set_rolloff(self, rolloff):
        self.add_var_opt('padding', rolloff)
        self.rolloff = rolloff

    def set_PSDstart(self, PSDstart):
        self.add_var_opt('psdstart', '%.9f' % PSDstart)
        self.PSDstart = PSDstart

    def set_outputDir(self, outputDir):
        self.add_var_opt('outputDir', outputDir)
        self.outputDir = outputDir

    def set_injevent(self, event):
        self.add_var_opt('event', event)
        self.event = event

    def set_dataseed(self, dataseed):
        self.add_var_opt('dataseed', dataseed)
        self.dataseed = dataseed

    def add_frame_transfer(self, framedict):
        """
        Add a list of frames to transfer
        """
        self.frames = []
        for ifo in framedict.keys():
            for frame in framedict[ifo]:
                self.frames.append(frame)
        self.frames = ",".join(self.frames)
        self.add_macro('macroframes', self.frames)

    def set_L1_timeslide(self, L1_timeslide):
        self.add_var_opt('L1-timeslide', L1_timeslide)
        self.L1_timeslide = L1_timeslide

    def set_V1_timeslide(self, V1_timeslide):
        self.add_var_opt('V1-timeslide', V1_timeslide)
        self.V1_timeslide = V1_timeslide

    def set_BW_event(self, BW_event):
        self.add_var_opt('BW-event', BW_event)
        self.BW_event = BW_event


#
# Post-processing
#


class bayeswave_postJob(pipeline.CondorDAGJob, pipeline.AnalysisJob):

    def __init__(self, cp, cacheFiles, injfile=None, numrel_data=None, dax=False):

        #
        # [condor]: Common workflow configuration
        #
        condor_job_config('bayeswave_post', self, cp)

        workdir = os.getcwd()
        self.add_condor_cmd('initialdir', workdir)
        self.set_sub_file(os.path.join(workdir, 'bayeswave_post.sub'))

        self.set_stdout_file(os.path.join(workdir, 'logs',
                                          'BayesWavePost_$(macrooutputDir)-$(cluster)-$(process).out'))
        self.set_stderr_file(os.path.join(workdir, 'logs',
                                          'BayesWavePost_$(macrooutputDir)-$(cluster)-$(process).err'))
        self.set_log_file(os.path.join(workdir, 'logs',
                                       'BayesWavePost_$(macrooutputDir)-$(cluster)-$(process).log'))

        if cp.has_option('condor', 'arch'):
            self.add_condor_cmd('+arch', cp.get('condor', 'arch'))

        if cp.has_option('condor', 'bayeswave_post-request-memory'):
            self.add_condor_cmd('request_memory',
                                cp.get('condor', 'bayeswave_post-request-memory'))

        if cp.has_option('condor', 'bayeswave_post-request-disk'):
            self.add_condor_cmd('request_disk',
                                cp.get('condor', 'bayeswave_post-request-disk'))

        if cp.has_option('condor', 'bayeswave_post-cit-nodes'):
            self.add_condor_cmd('+BayesWaveCgroup', 'True')
            self.add_condor_cmd('Rank', '(TARGET.BayesWaveCgroup =?= True)')

        #
        # File Transfers
        #
        if cp.getboolean('condor', 'transfer-files'):

            # File transfers
            transferstring = '$(macrooutputDir),datafind'

            if cp.getboolean('condor', 'copy-frames'):
                transferstring += ',$(macroframes)'

            if injfile is not None:
                transferstring += ',' + injfile
            if numrel_data is not None:
                transferstring += ',' + numrel_data

            if cp.has_option('condor', 'extra-files'):
                # allow specification of additional files to transfer
                transferstring += ',%s' % cp.get('condor', 'extra-files')

            self.add_condor_cmd('transfer_input_files', transferstring)
            self.add_condor_cmd('transfer_output_files', '$(macrooutputDir)')

        #
        # [input], [datafind]: Data configuration
        #
        ifo_list = ast.literal_eval(cp.get('input', 'ifo-list'))
        if not cp.get('datafind', 'sim-data'):
            channel_list = ast.literal_eval(cp.get('datafind', 'channel-list'))

        # XXX: hack to repeat option
        ifo_list_opt = ifo_list[0]
        for ifo in ifo_list[1:]:
            ifo_list_opt += ' --ifo {0}'.format(ifo)
        self.add_opt('ifo', ifo_list_opt)

        self.add_opt('psdlength', cp.get('input', 'PSDlength'))

        flow = ast.literal_eval(cp.get('input', 'flow'))

        #
        # [bayeswave_post_options]: Algorithm configuration 
        #
        for item in cp.items('bayeswave_post_options'):
            # Add any option and value which exists
            self.add_opt(item[0], item[1])

        #
        # [injections]: injection configuration
        #

        # --- LALSimulation options
        # Injection file
        if injfile is not None:
            # XXX: note that bayeswave works within the outputDir, so point to
            # injection
            injfile = os.path.join('..', injfile)
            self.add_opt('inj', injfile)

        if numrel_data is not None:
            numrel_data = os.path.join('..', numrel_data)
            self.add_opt('inj-numreldata', numrel_data)

        # --- MDC-style injection configuration
        if cp.has_option('injections', 'mdc-cache'):
            mdc_cache_list = str(['../datafind/MDC.cache' for ifo in
                                  ifo_list]).replace("'", '')
            mdc_cache_list = mdc_cache_list.replace(' ', '')
            self.add_opt('MDC-cache', mdc_cache_list)

        if cp.has_option('injections', 'mdc-channels'):
            mdc_channel_list = ast.literal_eval(cp.get('injections', 'mdc-channels'))
            mdc_channel_str = str(mdc_channel_list.values()).replace("'", '')
            mdc_channel_str = mdc_channel_str.replace(' ', '')
            self.add_opt('MDC-channel', mdc_channel_str)

        if cp.has_option('injections', 'mdc-prefactor'):
            self.add_opt('MDC-prefactor', cp.get('injections', 'mdc-prefactor'))


class bayeswave_postNode(pipeline.CondorDAGNode, pipeline.AnalysisNode):

    def __init__(self, bayeswave_post_job):

        pipeline.CondorDAGNode.__init__(self, bayeswave_post_job)
        pipeline.AnalysisNode.__init__(self)

    def set_trigtime(self, trigtime):
        self.add_var_opt('trigtime', '%.9f' % trigtime)
        self.trigtime = trigtime

    def set_segment_start(self, segment_start):
        self.add_var_opt('segment-start', '%.9f' % segment_start)
        self.segment_start = segment_start

    def set_window(self, window):
        self.add_var_opt('window', window)
        self.window = window

    def set_rolloff(self, rolloff):
        self.add_var_opt('padding', rolloff)
        self.rolloff = rolloff

    def set_srate(self, srate):
        self.add_var_opt('srate', srate)
        self.srate = srate

    def set_seglen(self, seglen):
        self.add_var_opt('seglen', seglen)
        self.seglen = seglen

    def set_flow(self, ifo_list, flow):
        for i, ifo in enumerate(ifo_list):
            self.add_var_opt('{ifo}-flow'.format(ifo=ifo), flow)
        self.flow = flow

    def set_PSDstart(self, PSDstart):
        self.add_var_opt('psdstart', '%.9f' % PSDstart)
        self.PSDstart = PSDstart

    def set_outputDir(self, ifo_list, outputDir):
        self.add_var_opt('outputDir', outputDir)
        self.outputDir = outputDir

        # bayeswave_post now uses PSD estimates straight from bayeswave and
        # no channel name needed.  These estimates lie in the outputDir so add
        # the variable option here
        for i, ifo in enumerate(ifo_list):
            self.add_var_opt("{ifo}-cache".format(ifo=ifo),
                             "interp:{outputDir}/{ifo}_fairdraw_asd.dat".format(
                                 outputDir=outputDir, ifo=ifo))

    def set_injevent(self, event):
        self.add_var_opt('event', event)
        self.event = event

    def set_dataseed(self, dataseed):
        self.add_var_opt('dataseed', dataseed)
        self.dataseed = dataseed

    def set_L1_timeslide(self, L1_timeslide):
        self.add_var_opt('L1-timeslide', L1_timeslide)
        self.L1_timeslide = L1_timeslide

    def set_V1_timeslide(self, V1_timeslide):
        self.add_var_opt('V1-timeslide', V1_timeslide)
        self.V1_timeslide = V1_timeslide

    def set_BW_event(self, BW_event):
        self.add_var_opt('BW-event', BW_event)
        self.BW_event = BW_event


class bayeswave_fpeakJob(bayeswave_postJob):

    def __init__(self, cp, cacheFiles, injfile=None, numrel_data=None, dax=False):
        bayeswave_postJob.__init__(self, cp, cacheFiles, injfile=injfile,
                                   numrel_data=numrel_data, dax=dax)

        print("bayeswave_fpeak is not currently supported",
              "contact james.clark@ligo.org")
        sys.exit(1)

        #
        # [condor]: Common workflow configuration
        #
        condor_job_config('bayeswave_fpeak', self, cp)

        #
        # bayeswave_post like options
        #

        # --- OSG-specifics unique to this job
        # Files to include in transfer
        if cp.getboolean('condor', 'osg-deploy'):
            transferstring = '$(macrooutputDir)'
            if injfile is not None: transferstring += ',' + injfile
            if numrel_data is not None: transferstring += ',' + numrel_data
            if cp.has_option('condor', 'transfer-files'):
                # allow specification of additional files to transfer
                transferstring += ',%s' % cp.get('condor', 'transfer-files')
            self.add_condor_cmd('transfer_input_files', transferstring)
            self.add_condor_cmd('transfer_output_files', '$(macrooutputDir)')

        self.set_stdout_file('$(macrooutputDir)/bayeswave_fpeak_$(cluster)-$(process)-$(node).out')
        self.set_stderr_file('$(macrooutputDir)/bayeswave_fpeak_$(cluster)-$(process)-$(node).err')
        self.set_log_file('$(macrooutputDir)/bayeswave_fpeak_$(cluster)-$(process)-$(node).log')

        #
        # [input], [datafind]: Data configuration
        #
        ifo_list = ast.literal_eval(cp.get('input', 'ifo-list'))
        if not cp.get('datafind', 'sim-data'):
            channel_list = ast.literal_eval(cp.get('datafind', 'channel-list'))

        # XXX: hack to repeat option
        ifo_list_opt = ifo_list[0]
        for ifo in ifo_list[1:]:
            ifo_list_opt += ' --ifo {0}'.format(ifo)
        self.add_opt('ifo', ifo_list_opt)

        self.add_opt('psdlength', cp.get('input', 'PSDlength'))

        flow = ast.literal_eval(cp.get('input', 'flow'))

        #
        # [bayeswave_post_options]: Algorithm configuration 
        #
        for item in cp.items('bayeswave_post_options'):
            # Add any option and value which exists
            self.add_opt(item[0], item[1])

        #
        # [injections]: injection configuration
        #

        # --- LALSimulation options
        # Injection file
        if injfile is not None:
            # XXX: note that bayeswave works within the outputDir, so point to
            # injection
            injfile = os.path.join('..', injfile)
            self.add_opt('inj', injfile)

        if numrel_data is not None:
            numrel_data = os.path.join('..', numrel_data)
            self.add_opt('inj-numreldata', numrel_data)

        # --- MDC-style injection configuration
        if cp.has_option('injections', 'mdc-cache'):
            mdc_cache_list = str(['../datafind/MDC.cache' for ifo in
                                  ifo_list]).replace("'", '')
            mdc_cache_list = mdc_cache_list.replace(' ', '')
            self.add_opt('MDC-cache', mdc_cache_list)

        if cp.has_option('injections', 'mdc-channels'):
            mdc_channel_list = ast.literal_eval(cp.get('injections', 'mdc-channels'))
            mdc_channel_str = str(mdc_channel_list.values()).replace("'", '')
            mdc_channel_str = mdc_channel_str.replace(' ', '')
            self.add_opt('MDC-channel', mdc_channel_str)

        if cp.has_option('injections', 'mdc-prefactor'):
            self.add_opt('MDC-prefactor', cp.get('injections', 'mdc-prefactor'))

        #
        # [bayeswave_fpeak_options]: Algorithm configuration 
        #

        # Now add the fpeak options
        # (some options should not be added this way)
        excluded = ['flow']
        for item in cp.items('bayeswave_fpeak_options'):
            # Add any option and value which exists
            if item[0] in excluded:
                continue
            else:
                self.add_opt(item[0], item[1])

        self.set_sub_file('bayeswave_fpeak.sub')


class bayeswave_fpeakNode(bayeswave_postNode):

    def __init__(self, bayeswave_post_job, bayeswave_fpeak_job):
        bayeswave_postNode.__init__(self, bayeswave_post_job)
        pipeline.CondorDAGNode.__init__(self, bayeswave_fpeak_job)
        pipeline.AnalysisNode.__init__(self)


class bayeswave_clean_frameJob(pipeline.CondorDAGJob, pipeline.AnalysisJob):

    def __init__(self, cp, cacheFiles, injfile=None, numrel_data=None, dax=False):

        condor_job_config('bayeswave_clean_frame', self, cp)

        workdir = os.getcwd()
        self.add_condor_cmd('initialdir', workdir)
        self.set_sub_file(os.path.join(workdir, 'bayeswave_clean_frame.sub'))

        self.set_stdout_file(os.path.join(workdir, 'logs',
                                          'BayesWaveCleanFrame_$(macrooutdir)-$(macroifo)-$(cluster)-$(process).out'))
        self.set_stderr_file(os.path.join(workdir, 'logs',
                                          'BayesWaveCleanFrame_$(macrooutdir)-$(macroifo)-$(cluster)-$(process).err'))
        self.set_log_file(os.path.join(workdir, 'logs',
                                       'BayesWaveCleanFrame_$(macrooutdir)-$(macroifo)-$(cluster)-$(process).log'))

        if cp.has_option('condor', 'arch'):
            self.add_condor_cmd('+arch', cp.get('condor', 'arch'))

        if cp.has_option('condor', 'bayeswave_clean_frame-request-memory'):
            self.add_condor_cmd('request_memory',
                                cp.get('condor', 'bayeswave_clean_frame-request-memory'))

        if cp.has_option('condor', 'bayeswave_clean_frame-request-disk'):
            self.add_condor_cmd('request_disk',
                                cp.get('condor', 'bayeswave_clean_frame-request-disk'))

        if cp.has_option('condor', 'bayeswave_clean_frame-cit-nodes'):
            self.add_condor_cmd('+BayesWaveCgroup', 'True')
            self.add_condor_cmd('Rank', '(TARGET.BayesWaveCgroup =?= True)')

        #
        # File Transfers
        #
        if cp.getboolean('condor', 'transfer-files'):

            # File transfers
            transferstring = '$(macrooutdir),datafind'

            if cp.getboolean('condor', 'copy-frames'):
                transferstring += ',$(macroframes)'

            self.add_condor_cmd('transfer_input_files', transferstring)
            self.add_condor_cmd('transfer_output_files', '$(macrooutdir)')

        clean_suffix = cp.get('bayeswave_clean_frame_options', 'clean-suffix')
        self.add_opt('clean-suffix', clean_suffix)


class bayeswave_clean_frameNode(pipeline.CondorDAGNode, pipeline.AnalysisNode):

    def __init__(self, bayeswave_clean_frame_job):
        pipeline.CondorDAGNode.__init__(self, bayeswave_clean_frame_job)
        pipeline.AnalysisNode.__init__(self)

    def set_trigtime(self, trigtime):
        self.add_var_opt('trigtime', '%.9f' % trigtime)
        self.trigtime = trigtime

    def set_segment_start(self, segment_start):
        self.add_var_opt('segment-start', '%.9f' % segment_start)

    def set_seglen(self, seglen):
        self.add_var_opt('seglen', seglen)
        self.seglen = seglen

    def set_frame_srate(self, frame_srate):
        self.add_var_opt('frame-srate', frame_srate)
        self.frame_srate = frame_srate

    def set_frame_start(self, frame_start):
        self.add_var_opt('frame-start', frame_start)
        self.frame_start = frame_start

    def set_frame_length(self, frame_length):
        self.add_var_opt('frame-length', frame_length)
        self.frame_length = frame_length

    def set_glitch_param_file(self, glitch_param_file):
        self.add_var_opt('glitch-model', glitch_param_file)

    def set_outdir(self, outdir):
        self.add_var_opt('outdir', outdir)

    def set_ifo(self, ifo):
        self.add_var_opt('ifo', ifo)

    def set_channel_name(self, channel):
        self.add_var_opt('channel', channel)

    def set_frame_type(self, frame_type):
        self.add_var_opt('frame-type', frame_type)

    def set_cache_file(self, cache_file):
        self.add_var_opt('cachefile', cache_file)


#
# skymap job
#

class megaskyJob(pipeline.CondorDAGJob, pipeline.AnalysisJob):

    def __init__(self, cp, inj=None, dax=False):

        # --- Common workflow configuration
        condor_job_config('megasky', self, cp)
        if inj is not None:
            self.add_opt('inj', inj)

        workdir = os.getcwd()
        self.add_condor_cmd('initialdir', workdir)
        self.set_sub_file(os.path.join(workdir, 'megasky.sub'))

        self.set_stdout_file(os.path.join(workdir, 'logs',
                                          'megasky_$(macrooutputDir)-$(cluster)-$(process).out'))
        self.set_stderr_file(os.path.join(workdir, 'logs',
                                          'megasky_$(macrooutputDir)-$(cluster)-$(process).err'))
        self.set_log_file(os.path.join(workdir, 'logs',
                                       'megasky_$(macrooutputDir)-$(cluster)-$(process).log'))

        # Mega-jobs require same disk as post jobs
        if cp.has_option('condor', 'bayeswave_post-request-disk'):
            self.add_condor_cmd('request_disk',
                                cp.get('condor', 'bayeswave_post-request-disk'))

        #
        # File transfers
        #
        if cp.getboolean('condor', 'transfer-files'):
            self.add_condor_cmd('transfer_input_files', '$(macroargument0)')
            self.add_condor_cmd('transfer_output_files', '$(macroargument0)')


class megaskyNode(pipeline.CondorDAGNode, pipeline.AnalysisNode):

    def __init__(self, megasky_job, rundir):
        pipeline.CondorDAGNode.__init__(self, megasky_job)
        pipeline.AnalysisNode.__init__(self)

    # Set eventnum if injection
    def set_injevent(self, eventnum):
        # print('eventnum:', eventnum, end='\r')
        self.add_var_opt('eventnum', eventnum)
        self.eventnum = eventnum

    # Set work dir
    def set_outputDir(self, outputDir):
        self.add_var_arg(outputDir)
        self.outputDir = outputDir


#
# megaplot job
#

class megaplotJob(pipeline.CondorDAGJob, pipeline.AnalysisJob):

    def __init__(self, cp, dax=False):

        # --- Common workflow configuration
        condor_job_config('megaplot', self, cp)

        workdir = os.getcwd()
        self.add_condor_cmd('initialdir', workdir)
        self.set_sub_file(os.path.join(workdir, 'megaplot.sub'))

        self.set_stdout_file(os.path.join(workdir, 'logs',
                                          'megaplot_$(macrooutputDir)-$(cluster)-$(process).out'))
        self.set_stderr_file(os.path.join(workdir, 'logs',
                                          'megaplot_$(macrooutputDir)-$(cluster)-$(process).err'))
        self.set_log_file(os.path.join(workdir, 'logs',
                                       'megaplot_$(macrooutputDir)-$(cluster)-$(process).log'))

        # Mega-jobs require same disk as post jobs
        if cp.has_option('condor', 'bayeswave_post-request-disk'):
            self.add_condor_cmd('request_disk',
                                cp.get('condor', 'bayeswave_post-request-disk'))

        #
        # Singularity configurations
        #
        if cp.getboolean('condor', 'transfer-files'):
            self.add_condor_cmd('transfer_input_files', '$(macroargument0)')
            self.add_condor_cmd('transfer_output_files', '$(macroargument0)')


class megaplotNode(pipeline.CondorDAGNode, pipeline.AnalysisNode):

    def __init__(self, megaplot_job, rundir):
        pipeline.CondorDAGNode.__init__(self, megaplot_job)
        pipeline.AnalysisNode.__init__(self)

    # Set work dir
    def set_outputDir(self, outputDir):
        self.add_var_arg(outputDir)
        self.outputDir = outputDir


#
# submitGraceDB
#

class submitToGraceDB(pipeline.CondorDAGJob, pipeline.AnalysisJob):

    def __init__(self, cp, dax=False):

        universe = 'vanilla'

        # Point this to the src dir
        gdb_submitter = cp.get('engine', 'gdb-submitter')
        pipeline.CondorDAGJob.__init__(self, universe, gdb_submitter)
        pipeline.AnalysisJob.__init__(self, cp, dax=dax)

        hostname = socket.gethostname()

        # --- Allow desired sites
        if cp.has_option('condor', 'desired-sites'):
            self.add_condor_cmd('+DESIRED_Sites', cp.get('condor', 'desired-sites'))
        if cp.has_option('condor', 'undesired-sites'):
            self.add_condor_cmd('+UNDESIRED_Sites', cp.get('condor', 'desired-sites'))

        if cp.has_option('condor', 'accounting-group'):
            self.add_condor_cmd('accounting_group', cp.get('condor', 'accounting-group'))

        self.add_condor_cmd('getenv', 'True')

        self.set_stdout_file('gdb_submitter_$(cluster)-$(process)-$(node).out')
        self.set_stderr_file('gdb_submitter_$(cluster)-$(process)-$(node).err')
        self.set_log_file('gdb_submitter_$(cluster)-$(process)-$(node).log')
        self.set_sub_file('gdb_submitter.sub')


class submitToGraceDBNode(pipeline.CondorDAGNode, pipeline.AnalysisNode):

    def __init__(self, gdb_submitter_job, rundir, htmlDir):
        pipeline.CondorDAGNode.__init__(self, gdb_submitter_job)
        pipeline.AnalysisNode.__init__(self)
        # Set job initialdir, so python codes know where to expect input files
        self.add_var_condor_cmd('initialdir', rundir)
        self.rundir = rundir

        # Set html directory
        self.add_var_opt('htmlDir', htmlDir)
        self.htmlDir = htmlDir
