#------------------------------------------------------------------------------
# Description    : Pulsar QCM native interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


#-- include -------------------------------------------------------------------

import numpy
import struct
import time

#Add SCPI support
from pulsar_qcm.pulsar_qcm_scpi_ifc import pulsar_qcm_scpi_ifc

#-- class ---------------------------------------------------------------------

class pulsar_qcm_ifc(pulsar_qcm_scpi_ifc):
    """
    Class that provides the native API for the Pulsar QCM. It provides methods to control all
    functions and features provided by the Pulsar QCM, like sequencer and waveform handling.
    """

    #--------------------------------------------------------------------------
    def __init__(self, transport_inst, debug = 0):
        """
        Creates Pulsar QCM native interface object.

        Parameters
        ----------
        transport_inst : :class:`~ieee488_2.transport`
            Transport class responsible for the lowest level of communication (e.g. ethernet).
        debug : int
            Debug level (0 = normal, 1 = no version check, >1 = no version or error checking).

        Returns
        ----------
        :class:`~pulsar_qcm.pulsar_qcm_ifc`
            Pulsar QCM native interface object.

        Raises
        ----------
        Exception
            Debug level is 0 and there is a version mismatch.
        """

        #Build information
        self._build = {"version": "0.2.3",
                       "date":    "03/03/2021-14:15:57",
                       "hash":    "0xE82D5dEE",
                       "dirty":   False}

        #Initialize parent class.
        super(pulsar_qcm_ifc, self).__init__(transport_inst, debug)

    #--------------------------------------------------------------------------
    def _get_scpi_commands(self):
        """
        Get SCPI commands.

        Parameters
        ----------

        Returns
        ----------
        dict
            Dictionary containing all available SCPI commands, corresponding parameters, arguments and Python methods and finally a descriptive comment.

        Raises
        ----------
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            #Format command string
            cmds          = super()._get_scpi_commands()
            cmd_elem_list = cmds.split(';')[:-1]
            cmd_list      = numpy.reshape(cmd_elem_list, (int(len(cmd_elem_list) / 9), 9))
            cmd_dict      = {cmd[0]: {"scpi_in_type":    cmd[1].split(',') if cmd[1] != "None" and cmd[1] != "" else [],
                                      "scpi_out_type":   cmd[2].split(',') if cmd[2] != "None" and cmd[2] != "" else [],
                                      "python_func":     cmd[3],
                                      "python_in_type":  cmd[4].split(',') if cmd[4] != "None" and cmd[4] != "" else [],
                                      "python_in_var":   cmd[5].split(',') if cmd[5] != "None" and cmd[5] != "" else [],
                                      "python_out_type": cmd[6].split(',') if cmd[6] != "None" and cmd[6] != "" else [],
                                      "comment":         cmd[8]} for cmd in cmd_list}

            return cmd_dict
        except:
            raise

    #--------------------------------------------------------------------------
    def get_idn(self):
        """
        Get device identity and build information.

        Parameters
        ----------

        Returns
        ----------
        dict
            Dictionary containing manufacturer, model, serial number and build information. The build information is subdivided into FPGA firmware,
            kernel module software, application software and driver software build information. Each of those consist of the version, build date,
            build Git hash and Git build dirty indication.

        Raises
        ----------
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            #Format IDN string
            idn            = self._get_idn()
            idn_elem_list  = idn.split(',')
            idn_build_list = idn_elem_list[-1].split(' ')
            idn_dict       = {"manufacturer":  idn_elem_list[0],
                              "device":        idn_elem_list[1],
                              "serial_number": idn_elem_list[2],
                              "build":         {"firmware":    {"version": idn_build_list[0].split("=")[-1],
                                                                "date":    idn_build_list[1].split("=")[-1],
                                                                "hash":    idn_build_list[2].split("=")[-1],
                                                                "dirty":   int(idn_build_list[3].split("=")[-1]) > 0},
                                                "kernel_mod":  {"version": idn_build_list[4].split("=")[-1],
                                                                "date":    idn_build_list[5].split("=")[-1],
                                                                "hash":    idn_build_list[6].split("=")[-1],
                                                                "dirty":   int(idn_build_list[7].split("=")[-1]) > 0},
                                                "application": {"version": idn_build_list[8].split("=")[-1],
                                                                "date":    idn_build_list[9].split("=")[-1],
                                                                "hash":    idn_build_list[10].split("=")[-1],
                                                                "dirty":   int(idn_build_list[11].split("=")[-1]) > 0},
                                                "driver":      self._build}}

            return idn_dict
        except:
            raise



    #--------------------------------------------------------------------------
    def get_system_status(self):
        """
        Get general system state.

        Parameters
        ----------

        Returns
        ----------
        str
            Dictionary containing general status and corresponding flags:

            :Status:
                - OKAY: System is okay.
                - CRITICAL: An error indicated by the flags occured, but has been resolved.
                - ERROR: An error indicated by the flags is occuring.

            :Flags:
                - CARRIER_PLL_UNLOCK: Carrier board PLL is unlocked.
                - FPGA_PLL_UNLOCK: FPGA PLL is unlocked.
                - FPGA_TEMP_OR: FPGA temperature is out-of-range.
                - CARRIER_TEMP_OR: Carrier board temperature is out-of-range.
                - AFE_TEMP_OR: Analog frontend board temperature is out-of-range.

        Raises
        ----------
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            #Format status string
            status           = self._get_system_status()
            status_elem_list = status.split(';')
            status_flag_list = status_elem_list[-1].split(',')[:-1] if status_elem_list[-1] != '' else []
            status_dict      = {"status": status_elem_list[0],
                                "flags":  status_flag_list}
            return status_dict
        except:
            raise

    #--------------------------------------------------------------------------
    def _set_sequencer_program(self, sequencer, program):
        """
        Assemble and set Q1ASM program for the indexed sequencer. If assembling failes, an exception is thrown with the
        assembler log.

        Parameters
        ----------
        sequencer : int
            Sequencer index.
        program : str
            Q1ASM program.

        Returns
        ----------

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            Assembly failed.
        """

        try:
            super()._set_sequencer_program(sequencer, program)
        except:
            print(self.get_assembler_log())
            raise

    @staticmethod
    #--------------------------------------------------------------------------
    def _get_sequencer_cfg_format():
        """
        Get format for converting the configuration dictionary to a C struct.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        seq_proc_cfg_format  = '?I'
        awg_cfg_format       = '??IIIIIIIIIII?III??I'
        awg_float_cfg_format = 'ffffff'

        return seq_proc_cfg_format + awg_cfg_format + awg_float_cfg_format

    #--------------------------------------------------------------------------
    def _set_sequencer_config(self, sequencer, cfg_dict):
        """
        Set configuration of the indexed sequencer. The configuration consists dictionary containing multiple parameters
        that will be converted into a C struct supported by the Pulsar QCM.

        Parameters
        ----------
        sequencer : int
            Sequencer index.
        config : dict
            Configuration dictionary.

        Returns
        ----------

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            #Get current configuration and merge dictionaries
            cfg_dict = {**self._get_sequencer_config(sequencer), **cfg_dict}

            #Set new configuration
            cfg = [#Sequence processor
                   cfg_dict["sync_en"],                           #Sequence processor synchronization enable
                   0,                                             #Sequence processor program counter start (unused)

                   #AWG
                   cfg_dict["cont_mode_en_awg_path_0"],           #Continuous mode enable for AWG path 0
                   cfg_dict["cont_mode_en_awg_path_1"],           #Continuous mode enable for AWG path 1
                   cfg_dict["cont_mode_waveform_idx_awg_path_0"], #continuous mode waveform index for AWG path 0
                   cfg_dict["cont_mode_waveform_idx_awg_path_1"], #Continuous mode waveform index for AWG path 1
                   cfg_dict["upsample_rate_awg_path_0"],          #Upsample rate for AWG path 0
                   cfg_dict["upsample_rate_awg_path_1"],          #Upsample rate for AWG path 1
                   0,                                             #Gain for AWG path 0         (unused)
                   0,                                             #Gain for AWG path 1         (unused)
                   0,                                             #Offset for AWG path 0       (unused)
                   0,                                             #Offset for AWG path 1       (unused)
                   0,                                             #Phase increment; ultra-fine (unused)
                   0,                                             #Phase increment; fine       (unused)
                   0,                                             #Phase increment; coarse     (unused)
                   0,                                             #Phase increment; sign       (unused)
                   0,                                             #Phase; ultra-fine           (unused)
                   0,                                             #Phase; fine                 (unused)
                   0,                                             #Phase; coarse               (unused)
                   cfg_dict["mod_en_awg"],                        #Modulation enable for AWG paths 0 and 1
                   cfg_dict["mrk_ovr_en"],                        #Marker override enable
                   cfg_dict["mrk_ovr_val"],                       #Marker override value

                   #AWG floating point values to be converted
                   cfg_dict["freq_hz"],                           #Frequency in Hz
                   cfg_dict["phase_offs_degree"],                 #Phase offset in degrees
                   cfg_dict["gain_awg_path_0_float"],             #Gain for AWG path 0 as float
                   cfg_dict["gain_awg_path_1_float"],             #Gain for AWG path 1 as float
                   cfg_dict["offset_awg_path_0_float"],           #Offset for AWG path 0 as float
                   cfg_dict["offset_awg_path_1_float"]]           #Offset for AWG path 1 as float

            super()._set_sequencer_config(sequencer, struct.pack(pulsar_qcm_ifc._get_sequencer_cfg_format(), *cfg))
        except:
            raise

    #--------------------------------------------------------------------------
    def _get_sequencer_config(self, sequencer):
        """
        Get configuration of the indexed sequencer. The configuration consists dictionary containing multiple parameters
        that will be converted from a C struct provided by the Pulsar QCM.

        Parameters
        ----------
        sequencer : int
            Sequencer index.

        Returns
        ----------
        dict
            Configuration dictionary.

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            cfg      = struct.unpack(pulsar_qcm_ifc._get_sequencer_cfg_format(), super()._get_sequencer_config(sequencer))
            cfg_dict = {#Sequence processor
                        "sync_en":                           cfg[0],

                        #AWG
                        "cont_mode_en_awg_path_0":           cfg[2],
                        "cont_mode_en_awg_path_1":           cfg[3],
                        "cont_mode_waveform_idx_awg_path_0": cfg[4],
                        "cont_mode_waveform_idx_awg_path_1": cfg[5],
                        "upsample_rate_awg_path_0":          cfg[6],
                        "upsample_rate_awg_path_1":          cfg[7],
                        "mod_en_awg":                        cfg[19],
                        "mrk_ovr_en":                        cfg[20],
                        "mrk_ovr_val":                       cfg[21],

                        #AWG floating point values
                        "freq_hz":                           cfg[22],
                        "phase_offs_degree":                 cfg[23],
                        "gain_awg_path_0_float":             cfg[24],
                        "gain_awg_path_1_float":             cfg[25],
                        "offset_awg_path_0_float":           cfg[26],
                        "offset_awg_path_1_float":           cfg[27]}
            return cfg_dict
        except:
            raise



    #--------------------------------------------------------------------------
    def arm_sequencer(self, sequencer=None):
        """
        Prepare the indexed sequencer to start by putting it in the armed state. If no sequencer index is given, all sequencers are armed.
        Any sequencer that was already running is stopped and rearmed. If an invalid sequencer index is given, an error is set in system error.

        Parameters
        ----------
        sequencer : int
            Sequencer index.

        Returns
        ----------

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            if sequencer is not None:
                self._arm_sequencer(sequencer)
            else:
                try:
                    #Arm all sequencers (SCPI call)
                    self._write('SEQuencer:ARM')
                except Exception as err:
                    self._check_error_queue(err)
                finally:
                    self._check_error_queue()
        except:
            raise

    #--------------------------------------------------------------------------
    def start_sequencer(self, sequencer=None):
        """
        Start the indexed sequencer, thereby putting it in the running state. If an invalid sequencer index is given or the indexed sequencer was
        not yet armed, an error is set in system error. If no sequencer index is given, all armed sequencers are started and any sequencer not in
        the armed state is ignored. However, if no sequencer index is given and no sequencers are armed, and error is set in system error.

        Parameters
        ----------
        sequencer : int
            Sequencer index.

        Returns
        ----------

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            if sequencer is not None:
                self._start_sequencer(sequencer)
            else:
                try:
                    #Start all sequencers (SCPI call)
                    self._write('SEQuencer:START')
                except Exception as err:
                    self._check_error_queue(err)
                finally:
                    self._check_error_queue()
        except:
            raise

    #--------------------------------------------------------------------------
    def stop_sequencer(self, sequencer=None):
        """
        Stop the indexed sequencer, thereby putting it in the stopped state. If an invalid sequencer index is given, an error is set in system error.
        If no sequencer index is given, all sequencers are stopped.

        Parameters
        ----------
        sequencer : int
            Sequencer index.

        Returns
        ----------

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            if sequencer is not None:
                self._stop_sequencer(sequencer)
            else:
                try:
                    #Stop all sequencers (SCPI call)
                    self._write('SEQuencer:STOP')
                except Exception as err:
                    self._check_error_queue(err)
                finally:
                    self._check_error_queue()
        except:
            raise

    #--------------------------------------------------------------------------
    def get_sequencer_state(self, sequencer, timeout=0, timeout_poll_res=0.1):
        """
        Get the sequencer state. If an invalid sequencer index is given, an error is set in system error. If the timeout is set to zero, the function returns the state immediately.
        If a positive non-zero timeout is set, the function blocks until the sequencer completes. If the sequencer hasn't stopped before the timeout expires, a timeout exception
        is thrown.

        Parameters
        ----------
        sequencer : int
            Sequencer index.
        timeout : int
            Timeout in minutes.
        timeout_poll_res : float
            Timeout polling resolution in seconds.

        Returns
        ----------
        str
            Concatinated list of strings separated by the semicolon character. Status is indicated by one status string and an optional number of flags respectively ordered as:

            :Status:
                - IDLE: Sequencer waiting to be armed and started.
                - ARMED: Sequencer is armed and ready to start.
                - RUNNING: Sequencer is running.
                - Q1 STOPPED: Classical part of the sequencer has stopped; waiting for real-time part to stop.
                - STOPPED: Sequencer has completely stopped.

            :Flags:
                - DISARMED: Sequencer was disarmed.
                - FORCED STOP: Sequencer was stopped while still running.
                - SEQUENCE PROCESSOR Q1 ILLEGAL INSTRUCTION: Classical sequencer part executed an unknown instruction.
                - SEQUENCE PROCESSOR RT EXEC ILLEGAL INSTRUCTION: Real-time sequencer part executed an unknown instruction.
                - AWG WAVE PLAYBACK INVALID PATH 0: AWG path 0 tried to play an unknown waveform.
                - AWG WAVE PLAYBACK INVALID PATH 1: AWG path 1 tried to play an unknown waveform.
                - CLOCK INSTABILITY: Clock source instability occurred.

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        TypeError
            Timeout is not an integer.
        TimeoutError
            Timeout
        """

        try:
            #Check timeout value
            if not isinstance(timeout, int):
                raise TypeError("Timeout is not an integer.")

            #Format status string
            status           = self._get_sequencer_state(sequencer)
            status_elem_list = status.split(';')
            status_flag_list = status_elem_list[-1].split(',')[:-1] if status_elem_list[-1] != '' else []
            status_dict      = {"status": status_elem_list[0],
                                "flags":  status_flag_list}
            elapsed_time = 0.0
            timeout      = timeout * 60.0
            while (status_dict["status"] == "RUNNING" or status_dict["status"] == "Q1 STOPPED") and elapsed_time < timeout:
                time.sleep(timeout_poll_res)

                status_dict   = self.get_sequencer_state(sequencer)
                elapsed_time += timeout_poll_res

                if elapsed_time >= timeout:
                    raise TimeoutError("Sequencer {} did not stop in timeout period of {} minutes.".format(sequencer, int(timeout / 60)))

            return status_dict
        except:
            raise



    #--------------------------------------------------------------------------
    def _add_awg_waveform(self, sequencer, name, waveform, index=None):
        """
        Add new waveform to AWG waveform list of indexed sequencer's AWG path. If an invalid sequencer index is given or if the waveform causes the waveform memory limit to be exceeded or
        if the waveform samples are out-of-range, an error is set in the system error. The waveform names 'all' and 'ALL' are reserved and adding waveforms with those names will also result
        in an error being set in system error. The optional index argument is used to specify an index for the waveform in the waveform list which is used by the sequencer Q1ASM program to
        refer to the waveform. If no index is given, the next available waveform index is selected (starting from 0). If an invalid waveform index is given, an error is set in system error.

        Parameters
        ----------
        sequencer : int
            Sequencer index.
        name : str
            Waveform name.
        waveform : list
            List of floats in the range of 1.0 to -1.0 representing the waveform.
        index : int
            Waveform index of the waveform in the waveform list.

        Returns
        ----------

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            super()._add_awg_waveform(sequencer, name, len(waveform), False)
            self._set_awg_waveform_data(sequencer, name, waveform)
            if index is not None:
                self._set_awg_waveform_index(sequencer, name, index)
        except:
            raise

    #--------------------------------------------------------------------------
    def _get_awg_waveform_data(self, sequencer, name, start=0, size=2**31):
        """
        Get waveform data of waveform in AWG waveform list of indexed sequencer. If an invalid sequencer index is given or if a non-existing waveform
        name is given, an error is set in system error. The start and size arguments can be used to return a section of the waveform. If the start argument
        is not given, zero is used as the default start sample. If the size argument is not given, all samples starting from the start sample are returned.

        Parameters
        ----------
        sequencer : int
            Sequencer index.
        name : str
            Waveform name.
        start : int
            First sample within the waveform to be returned.
        size : int
            Number of samples starting from the start sample to be returned.

        Returns
        ----------
        list
            List of floats in the range of 1.0 to -1.0 representing the waveform.

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            return super()._get_awg_waveform_data(sequencer, name, start, size)
        except:
            raise

    #--------------------------------------------------------------------------
    def _get_awg_waveform_names(self, sequencer):
        """
        Get all waveform names in AWG waveform list of indexed sequencer's AWG path. If an invalid sequencer index is given, an error is set in system error.

        Parameters
        ----------
        sequencer : int
            Sequencer index.

        Returns
        ----------
        int
            Number of waveforms.

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            names     = super()._get_awg_waveform_names(sequencer)
            name_list = names.split(';')[:-1] if names != '' else []
            return name_list
        except:
            raise



    #--------------------------------------------------------------------------
    def _add_waveforms(self, sequencer, waveform_dict):
        """
        Add all waveforms in JSON compatible dictionary to AWG waveform list of indexed sequencer.
        The dictionary must be structured as follows:

        - awg

            - name: waveform name.

                - data: waveform samples in a range of 1.0 to -1.0.
                - index: optional waveform index used by the sequencer Q1ASM program to refer to the waveform.

        Parameters
        ----------
        sequencer : int
            Sequencer index.
        waveform_dict : dict
            JSON compatible dictionary with one or more waveforms.

        Returns
        ----------

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        Exception
            Missing waveform data of waveform in dictionary.
        """

        try:
            if "awg" in waveform_dict:
                for name in waveform_dict["awg"]:
                    if "data" in waveform_dict["awg"][name]:
                        if "index" in waveform_dict["awg"][name]:
                            self._add_awg_waveform(sequencer, name, waveform_dict["awg"][name]["data"], waveform_dict["awg"][name]["index"])
                        else:
                            self._add_awg_waveform(sequencer, name, waveform_dict["awg"][name]["data"])
                    else:
                        raise Exception("Missing data key for {} in AWG waveform dictionary".format(name))
        except:
            raise

    #--------------------------------------------------------------------------
    def _delete_waveforms(self, sequencer):
        """
        Delete all waveforms in AWG waveform list of indexed sequencer.

        Parameters
        ----------
        sequencer : int
            Sequencer index.

        Returns
        ----------

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            self._delete_awg_waveform(sequencer, "all")
        except:
            raise

    #--------------------------------------------------------------------------
    def get_waveforms(self, sequencer):
        """
        Get all waveforms in AWG waveform list of indexed sequencer.
        The returned dictionary is structured as follows:

        - awg

            - name: waveform name.

                - data: waveform samples in a range of 1.0 to -1.0.
                - index: optional waveform index used by the sequencer Q1ASM program to refer to the waveform.

        Parameters
        ----------
        sequencer : int
            Sequencer index.

        Returns
        ----------
        dict
            Dictionary with waveforms.

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            waveform_dict = {"awg": {}}

            name_list = self._get_awg_waveform_names(sequencer)
            for name in name_list:
                waveform_dict["awg"][name] = {}
                waveform_dict["awg"][name]["data"]  = self._get_awg_waveform_data(sequencer, name, 0, 2**31-1)
                waveform_dict["awg"][name]["index"] = self._get_awg_waveform_index(sequencer, name)

            return waveform_dict
        except:
            raise
