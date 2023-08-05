#------------------------------------------------------------------------------
# Description    : Pulsar QRM QCoDeS interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


#-- include -------------------------------------------------------------------

from ieee488_2.transport       import ip_transport, pulsar_dummy_transport
from pulsar_qrm.pulsar_qrm_ifc import pulsar_qrm_ifc
from qcodes                    import validators as vals
from qcodes                    import Instrument
from jsonschema                import validate
import json

#-- class ---------------------------------------------------------------------

class pulsar_qrm_qcodes(pulsar_qrm_ifc, Instrument):
    """
    This class connects `QCoDeS <https://qcodes.github.io/Qcodes/>`_ to the Pulsar QRM native interface. Do not directly instantiate this class, but instead instantiate either the
    :class:`~.pulsar_qrm` or :class:`~.pulsar_qrm_dummy`.
    """

    #--------------------------------------------------------------------------
    def __init__(self, name, transport_inst, debug=0):
        """
        Creates Pulsar QRM QCoDeS class and adds all relevant instrument parameters. These instrument parameters call the associated methods provided by the native interface.

        Parameters
        ----------
        name : str
            Instrument name.
        transport_inst : :class:`~ieee488_2.transport`
            Transport class responsible for the lowest level of communication (e.g. ethernet).
        debug : int
            Debug level (0 = normal, 1 = no version check, >1 = no version or error checking).

        Returns
        ----------

        Raises
        ----------
        Exception
            Debug level is 0 and there is a version mismatch.


        .. Note::

            To get a complete of list of the QCoDeS parameters, run the following code.

        .. code-block:: Python

            from pulsar_qrm.pulsar_qrm import pulsar_qrm_dummy

            qrm = pulsar_qrm_dummy("qrm")
            for call in qrm.snapshot()['parameters']:
                print(getattr(qrm, call).__doc__)
        """

        #Initialize parent classes.
        super(pulsar_qrm_qcodes, self).__init__(transport_inst, debug)
        Instrument.__init__(self, name)

        #Set instrument parameters
        self._num_sequencers = 1

        #Set JSON schema to validate JSON file with
        self._wave_and_prog_json_schema = {"title":       "Sequencer waveforms and program container",
                                           "description": "Contains both all waveforms and program required for a sequence.",
                                           "type":        "object",
                                           "required":    ["program", "waveforms"],
                                           "properties": {
                                               "program": {
                                                   "description": "Sequencer assembly program in string format.",
                                                   "type":        "string"
                                               },
                                               "waveforms": {
                                                   "description": "Waveform dictionary containing one or multiple AWG and/or acquisition waveform(s).",
                                                   "type":        "object",
                                                   "properties": {
                                                       "awg": {
                                                            "description": "Waveform dictionary containing one or multiple AWG waveform(s).",
                                                            "type":        "object"
                                                       },
                                                       "acq": {
                                                            "description": "Waveform dictionary containing one or multiple acquisition waveform(s).",
                                                            "type":        "object"
                                                       }
                                                   }
                                               }
                                           }}
        self._wave_json_schema = {"title":       "Waveform container",
                                  "description": "Waveform dictionary a single waveform.",
                                  "type":        "object",
                                  "required":    ["data"],
                                  "properties": {
                                      "data":  {
                                          "description": "List of waveform samples.",
                                          "type":        "array"
                                      },
                                      "index": {
                                          "description": "Optional waveform index number.",
                                          "type":        "number"
                                      }
                                  }}

        #Add QCoDeS parameters
        self.add_parameter(
            "reference_source",
            label       = "Reference source.",
            docstring   = "Sets/gets reference source ('internal' = internal 10 MHz, 'external' = external 10 MHz).",
            unit        = '',
            vals        = vals.Bool(),
            val_mapping = {"internal": True, "external": False},
            set_parser  = bool,
            get_parser  = bool,
            set_cmd     = self._set_reference_source,
            get_cmd     = self._get_reference_source
        )

        self.add_parameter(
            "in0_amp_gain",
            label      = "Input 0 amplifier gain.",
            docstring  = "Sets/gets input 0 amplifier gain in a range of -6dB to 26dB with a resolution of 1dB per step.",
            unit       = 'dB',
            vals       = vals.Numbers(-6, 26),
            set_parser = int,
            get_parser = int,
            set_cmd    = self._set_in_amp_gain_0,
            get_cmd    = self._get_in_amp_gain_0
        )

        self.add_parameter(
            "in1_amp_gain",
            label      = "Input 1 amplifier gain.",
            docstring  = "Sets/gets input 1 amplifier gain in a range of -6dB to 26dB with a resolution of 1dB per step.",
            unit       = 'dB',
            vals       = vals.Numbers(-6, 26),
            set_parser = int,
            get_parser = int,
            set_cmd    = self._set_in_amp_gain_1,
            get_cmd    = self._get_in_amp_gain_1
        )

        for seq_idx in range(0, self._num_sequencers):
            #--Sequencer settings----------------------------------------------
            self.add_parameter(
                "sequencer{}_sync_en".format(seq_idx),
                label      = "Sequencer {} synchronization enable which enables party-line synchronization.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} synchronization enable which enables party-line synchronization.".format(seq_idx),
                unit       = '',
                vals       = vals.Bool(),
                set_parser = bool,
                get_parser = bool,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "sync_en"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "sync_en")
            )

            self.add_parameter(
                "sequencer{}_nco_freq".format(seq_idx),
                label      = "Sequencer {} NCO frequency.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} NCO frequency in Hz with a resolution of 0.25 Hz.".format(seq_idx),
                unit       = 'Hz',
                vals       = vals.Numbers(-300e6, 300e6),
                set_parser = float,
                get_parser = float,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "freq_hz"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "freq_hz")
            )

            self.add_parameter(
                "sequencer{}_nco_phase_offs".format(seq_idx),
                label      = "Sequencer {} NCO phase offset.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} NCO phase offset in degrees with a resolution of 3.6e-7 degrees.".format(seq_idx),
                unit       = 'Degrees',
                vals       = vals.Numbers(0, 360),
                set_parser = float,
                get_parser = float,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "phase_offs_degree"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "phase_offs_degree")
            )

            self.add_parameter(
                "sequencer{}_marker_ovr_en".format(seq_idx),
                label      = "Sequencer {} marker override enable.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} marker override enable.".format(seq_idx),
                unit       = '',
                vals       = vals.Bool(),
                set_parser = bool,
                get_parser = bool,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "mrk_ovr_en"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "mrk_ovr_en")
            )

            self.add_parameter(
                "sequencer{}_marker_ovr_value".format(seq_idx),
                label      = "Sequencer {} marker override value.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} marker override value. Bit index corresponds to marker channel index.".format(seq_idx),
                unit       = '',
                vals       = vals.Numbers(0, 15),
                set_parser = int,
                get_parser = int,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "mrk_ovr_val"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "mrk_ovr_val")
            )

            self.add_parameter(
                "sequencer{}_waveforms_and_program".format(seq_idx),
                label      = "Sequencer {} AWG and acquistion waveforms and ASM program.".format(seq_idx),
                docstring  = "Sets sequencer {} AWG and acquistion waveforms and ASM program. Valid input is a string representing the JSON filename.".format(seq_idx),
                vals       = vals.Strings(),
                set_parser = str,
                get_parser = str,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_waveforms_and_program, seq_idx),
            )



            #--AWG settings----------------------------------------------------
            self.add_parameter(
                "sequencer{}_cont_mode_en_awg_path0".format(seq_idx),
                label      = "Sequencer {} continous waveform mode enable for AWG path 0.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} continous waveform mode enable for AWG path 0.".format(seq_idx),
                unit       = '',
                vals       = vals.Bool(),
                set_parser = bool,
                get_parser = bool,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "cont_mode_en_awg_path_0"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "cont_mode_en_awg_path_0")
            )

            self.add_parameter(
                "sequencer{}_cont_mode_en_awg_path1".format(seq_idx),
                label      = "Sequencer {} continous waveform mode enable for AWG path 1.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} continous waveform mode enable for AWG path 1.".format(seq_idx),
                unit       = '',
                vals       = vals.Bool(),
                set_parser = bool,
                get_parser = bool,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "cont_mode_en_awg_path_1"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "cont_mode_en_awg_path_1")
            )

            self.add_parameter(
                "sequencer{}_cont_mode_waveform_idx_awg_path0".format(seq_idx),
                label      = "Sequencer {} continous waveform mode waveform index for AWG path 0.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} continous waveform mode waveform index or AWG path 0.".format(seq_idx),
                unit       = '',
                vals       = vals.Numbers(0, 2**10-1),
                set_parser = int,
                get_parser = int,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "cont_mode_waveform_idx_awg_path_0"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "cont_mode_waveform_idx_awg_path_0")
            )

            self.add_parameter(
                "sequencer{}_cont_mode_waveform_idx_awg_path1".format(seq_idx),
                label      = "Sequencer {} continous waveform mode waveform index for AWG path 1.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} continous waveform mode waveform index or AWG path 1.".format(seq_idx),
                unit       = '',
                vals       = vals.Numbers(0, 2**10-1),
                set_parser = int,
                get_parser = int,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "cont_mode_waveform_idx_awg_path_1"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "cont_mode_waveform_idx_awg_path_1")
            )

            self.add_parameter(
                "sequencer{}_upsample_rate_awg_path0".format(seq_idx),
                label      = "Sequencer {} upsample rate for AWG path 0.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} upsample rate for AWG path 0.".format(seq_idx),
                unit       = '',
                vals       = vals.Numbers(0, 2**16-1),
                set_parser = int,
                get_parser = int,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "upsample_rate_awg_path_0"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "upsample_rate_awg_path_0")
            )

            self.add_parameter(
                "sequencer{}_upsample_rate_awg_path1".format(seq_idx),
                label      = "Sequencer {} upsample rate for AWG path 1.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} upsample rate for AWG path 1.".format(seq_idx),
                unit       = '',
                vals       = vals.Numbers(0, 2**16-1),
                set_parser = int,
                get_parser = int,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "upsample_rate_awg_path_1"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "upsample_rate_awg_path_1")
            )

            self.add_parameter(
                "sequencer{}_gain_awg_path0".format(seq_idx),
                label      = "Sequencer {} gain for AWG path 0.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} gain for AWG path 0.".format(seq_idx),
                unit       = '',
                vals       = vals.Numbers(-1.0, 1.0),
                set_parser = float,
                get_parser = float,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "gain_awg_path_0_float"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "gain_awg_path_0_float")
            )

            self.add_parameter(
                "sequencer{}_gain_awg_path1".format(seq_idx),
                label      = "Sequencer {} gain for AWG path 1.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} gain for AWG path 1.".format(seq_idx),
                unit       = '',
                vals       = vals.Numbers(-1.0, 1.0),
                set_parser = float,
                get_parser = float,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "gain_awg_path_1_float"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "gain_awg_path_1_float")
            )

            self.add_parameter(
                "sequencer{}_offset_awg_path0".format(seq_idx),
                label      = "Sequencer {} offset for AWG path 0.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} offset for AWG path 0.".format(seq_idx),
                unit       = '',
                vals       = vals.Numbers(-1.0, 1.0),
                set_parser = float,
                get_parser = float,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "offset_awg_path_0_float"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "offset_awg_path_0_float")
            )

            self.add_parameter(
                "sequencer{}_offset_awg_path1".format(seq_idx),
                label      = "Sequencer {} offset for AWG path 1.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} offset for AWG path 1.".format(seq_idx),
                unit       = '',
                vals       = vals.Numbers(-1.0, 1.0),
                set_parser = float,
                get_parser = float,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "offset_awg_path_1_float"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "offset_awg_path_1_float")
            )

            self.add_parameter(
                "sequencer{}_mod_en_awg".format(seq_idx),
                label      = "Sequencer {} modulation enable for AWG.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} modulation enable for AWG.".format(seq_idx),
                unit       = '',
                vals       = vals.Bool(),
                set_parser = bool,
                get_parser = bool,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "mod_en_awg"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "mod_en_awg")
            )



            #--Acquisition settings--------------------------------------------
            self.add_parameter(
                "sequencer{}_trigger_mode_acq_path0".format(seq_idx),
                label       = "Sequencer {} trigger mode for acquisition path 0.".format(seq_idx),
                docstring   = "Sets/gets sequencer {} trigger mode for acquisition path 0 ('sequencer' = triggered by sequencer, 'level' = triggered by input level).".format(seq_idx),
                unit        = '',
                vals        = vals.Bool(),
                val_mapping = {"level": True, "sequencer": False},
                set_parser  = bool,
                get_parser  = bool,
                set_cmd     = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "trig_mode_acq_path_0"),
                get_cmd     = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "trig_mode_acq_path_0")
            )

            self.add_parameter(
                "sequencer{}_trigger_mode_acq_path1".format(seq_idx),
                label       = "Sequencer {} trigger mode for acquisition path 1.".format(seq_idx),
                docstring   = "Sets/gets sequencer {} trigger mode for acquisition path 1 ('sequencer' = triggered by sequencer, 'level' = triggered by input level).".format(seq_idx),
                unit        = '',
                vals        = vals.Bool(),
                val_mapping = {"level": True, "sequencer": False},
                set_parser  = bool,
                get_parser  = bool,
                set_cmd     = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "trig_mode_acq_path_1"),
                get_cmd     = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "trig_mode_acq_path_1")
            )

            self.add_parameter(
                "sequencer{}_trigger_level_acq_path0".format(seq_idx),
                label      = "Sequencer {} trigger level when using input level trigger mode for acquisition path 0.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} trigger level when using input level trigger mode for acquisition path 0.".format(seq_idx),
                unit       = '',
                vals       = vals.Numbers(-1.0, 1.0),
                set_parser = float,
                get_parser = float,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "trig_lvl_acq_path_0_float"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "trig_lvl_acq_path_0_float")
            )

            self.add_parameter(
                "sequencer{}_trigger_level_acq_path1".format(seq_idx),
                label      = "Sequencer {} trigger level when using input level trigger mode for acquisition path 1.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} trigger level when using input level trigger mode for acquisition path 1.".format(seq_idx),
                unit       = '',
                vals       = vals.Numbers(-1.0, 1.0),
                set_parser = float,
                get_parser = float,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "trig_lvl_acq_path_1_float"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "trig_lvl_acq_path_1_float")
            )

            self.add_parameter(
                "sequencer{}_avg_mode_en_acq_path0".format(seq_idx),
                label      = "Sequencer {} averaging mode enable for acquisition path 0.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} averaging mode enable for acquisition path 0.".format(seq_idx),
                unit       = '',
                vals       = vals.Bool(),
                set_parser = bool,
                get_parser = bool,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "avg_en_acq_path_0"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "avg_en_acq_path_0")
            )

            self.add_parameter(
                "sequencer{}_avg_mode_en_acq_path1".format(seq_idx),
                label      = "Sequencer {} averaging mode enable for acquisition path 1.".format(seq_idx),
                docstring  = "Sets/gets sequencer {} averaging mode enable for acquisition path 1.".format(seq_idx),
                unit       = '',
                vals       = vals.Bool(),
                set_parser = bool,
                get_parser = bool,
                set_cmd    = pulsar_qrm._gen_set_func_par(self._set_sequencer_config_val, seq_idx, "avg_en_acq_path_1"),
                get_cmd    = pulsar_qrm._gen_get_func_par(self._get_sequencer_config_val, seq_idx, "avg_en_acq_path_1")
            )

    #--------------------------------------------------------------------------
    def _set_sequencer_config_val(self, sequencer, param, val):
        """
        Set value of specific sequencer parameter.

        Parameters
        ----------
        sequencer : int
            Sequencer index.
        param : str
            Parameter name.
        val
            Value to set parameter to.

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
            self._set_sequencer_config(sequencer, {param: val})
        except:
            raise

    #--------------------------------------------------------------------------
    def _get_sequencer_config_val(self, sequencer, param):
        """
        Get value of specific sequencer parameter.

        Parameters
        ----------
        sequencer : int
            Sequencer index.
        param : str
            Parameter name.

        Returns
        ----------
        val
            Parameter value.

        Raises
        ----------
        Exception
            Invalid input parameter type.
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            return self._get_sequencer_config(sequencer)[param]
        except:
            raise

    #--------------------------------------------------------------------------
    def _set_sequencer_waveforms_and_program(self, sequencer, file_name):
        """
        Set sequencer waveforms and program from JSON file. The JSON file needs to apply the schema specified by :member:`pulsar_qrm.pulsar_qrm_qcodes._wave_and_prog_json_schema`
        and :member:`pulsar_qrm.pulsar_qrm_qcodes._wave_json_schema`.

        Parameters
        ----------
        sequencer : int
            Sequencer index.
        file_name : str
            Sequencer waveforms and program file.

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
            Assembly failed.
        SchemaError
            Invalid JSON file.
        """

        try:
            with open(file_name, 'r') as file:
                wave_and_prog_dict = json.load(file)
                validate(wave_and_prog_dict, self._wave_and_prog_json_schema)
                target_list = ["awg", "acq"]
                for target in target_list:
                    if "target" in wave_and_prog_dict["waveforms"]:
                        for name in wave_and_prog_dict["waveforms"][target]:
                            validate(wave_and_prog_dict["waveforms"][target][name], self._wave_json_schema)
                self._delete_waveforms(sequencer)
                self._add_waveforms(sequencer, wave_and_prog_dict["waveforms"])
                self._set_sequencer_program(sequencer, wave_and_prog_dict["program"])
        except:
            raise

    #--------------------------------------------------------------------------
    @staticmethod
    def _gen_set_func_par(func, *args):
        """
        Generate set function with fixed parameters.

        Parameters
        ----------
        func : callable
            Function to generate set function for.
        args
            Function arguments.

        Returns
        ----------

        Raises
        ----------
        """

        def set_func(val):
            return func(*args, val)
        return set_func

    #--------------------------------------------------------------------------
    @staticmethod
    def _gen_get_func_par(func, *args):
        """
        Generate get function with fixed parameters.

        Parameters
        ----------
        func : callable
            Function to generate set function for.
        args
            Function arguments.

        Returns
        ----------
        val
            Function return value.

        Raises
        ----------
        """

        def get_func():
            return func(*args)
        return get_func

#-- class ---------------------------------------------------------------------

class pulsar_qrm(pulsar_qrm_qcodes):
    """
    Pulsar QRM driver class based on `QCoDeS <https://qcodes.github.io/Qcodes/>`_ that uses an IP socket to communicate
    with the instrument.
    """

    #--------------------------------------------------------------------------
    def __init__(self, name, host, port=5025, debug=0):
        """
        Creates Pulsar QRM driver object.

        Parameters
        ----------
        name : str
            Instrument name.
        host : str
            Instrument IP address.
        port : int
            Instrument port.
        debug : int
            Debug level (0 = normal, 1 = no version check, >1 = no version or error checking).

        Returns
        ----------

        Raises
        ----------
        Exception
            Debug level is 0 and there is a version mismatch.
        """

        #Create transport layer (socket interface)
        transport_inst = ip_transport(host=host, port=port)

        #Initialize parent classes.
        super(pulsar_qrm, self).__init__(name, transport_inst, debug)

#-- class ---------------------------------------------------------------------

class pulsar_qrm_dummy(pulsar_qrm_qcodes):
    """
    Pulsar QRM driver class based on `QCoDeS <https://qcodes.github.io/Qcodes/>`_ that uses the :class:`~ieee488_2.transport.pulsar_dummy_transport` layer
    to substitute an actual Pulsar QRM to allow software stack development without hardware.
    """

    #--------------------------------------------------------------------------
    def __init__(self, name, debug=1):
        """
        Creates Pulsar QRM driver object. The debug level must be set to >= 1.

        Parameters
        ----------
        name : str
            Instrument name.
        debug : int
            Debug level (0 = normal, 1 = no version check, >1 = no version or error checking).

        Returns
        ----------

        Raises
        ----------
        """

        #Create transport layer (socket interface)
        transport_inst = pulsar_dummy_transport(pulsar_qrm_ifc._get_sequencer_cfg_format())

        #Initialize parent classes.
        super(pulsar_qrm_dummy, self).__init__(name, transport_inst, debug)
