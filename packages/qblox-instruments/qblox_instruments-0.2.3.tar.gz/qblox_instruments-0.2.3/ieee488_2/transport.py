#------------------------------------------------------------------------------
# Description    : Transport layer (abstract, IP, file, pulsar_dummy)
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


#-- include -------------------------------------------------------------------

import socket
import re
import os
import sys
import struct
import subprocess

#-- class ----------------------------------------------------------------------

class transport:
    """
    Abstract base class for data transport to instruments.
    """

    #--------------------------------------------------------------------------
    def close(self) -> None:
        """
        Abstract method to close instrument.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        pass

    #--------------------------------------------------------------------------
    def write(self, cmd_str: str) -> None:
        """
        Abstract method to write command to instrument.

        Parameters
        ----------
        cmd_str : str
            Command

        Returns
        ----------

        Raises
        ----------
        """

        pass

    #--------------------------------------------------------------------------
    def write_binary(self, data: bytes) -> None:
        """
        Abstract method to write binary data to instrument.

        Parameters
        ----------
        data : bytes
            Binary data

        Returns
        ----------

        Raises
        ----------
        """

        pass

    #--------------------------------------------------------------------------
    def read_binary(self, size: int) -> bytes:
        """
        Abstract method to read binary data from instrument.

        Parameters
        ----------
        size : int
            Number of bytes

        Returns
        ----------
        bytes
            Binary data array of length "size".

        Raises
        ----------
        """

        pass

    #--------------------------------------------------------------------------
    def readline(self) -> str:
        """
        Abstract method to read data from instrument.

        Parameters
        ----------

        Returns
        ----------
        str
            String with data.

        Raises
        ----------
        """

        pass

#-- class ---------------------------------------------------------------------

class ip_transport(transport):
    """
    Class for data transport of IP socket.
    """

    #--------------------------------------------------------------------------
    def __init__(self, host: str, port: int = 5025, timeout : float = 60.0, snd_buf_size: int = 512 * 1024) -> None:
        """
        Create IP socket transport class.

        Parameters
        ----------
        host : str
            Instrument IP address.
        port : int
            Instrument port.
        timeout : float
            Instrument call timeout in seconds.
        snd_buf_size : int
            Instrument buffer size for transmissions to instrument.

        Returns
        ----------

        Raises
        ----------
        """

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(timeout)                                           #Setup timeout (before connect)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, snd_buf_size) #Enlarge buffer
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)         #Send immediately
        self._socket.connect((host, port))

    #--------------------------------------------------------------------------
    def __del__(self) -> None:
        """
        Delete IP socket transport class.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        self.close()

    #--------------------------------------------------------------------------
    def close(self) -> None:
        """
        Close IP socket.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        self._socket.close()

    #--------------------------------------------------------------------------
    def write(self, cmd_str: str) -> None:
        """
        Write command to instrument over IP socket.

        Parameters
        ----------
        cmd_str : str
            Command

        Returns
        ----------

        Raises
        ----------
        """

        out_str = cmd_str + '\n'
        self.write_binary(out_str.encode('ascii'))

    #--------------------------------------------------------------------------
    def write_binary(self, data: bytes) -> None:
        """
        Write binary data to instrument over IP socket.

        Parameters
        ----------
        data : bytes
            Binary data

        Returns
        ----------

        Raises
        ----------
        """

        exp_len = len(data)
        act_len = 0
        while True:
            act_len += self._socket.send(data[act_len:exp_len])
            if act_len == exp_len:
                break

    #--------------------------------------------------------------------------
    def read_binary(self, size: int) -> bytes:
        """
        Read binary data from instrument over IP socket.

        Parameters
        ----------
        size : int
            Number of bytes

        Returns
        ----------
        bytes
            Binary data array of length "size".

        Raises
        ----------
        """

        data = self._socket.recv(size)
        act_len = len(data)
        exp_len = size
        while act_len != exp_len:
            data += self._socket.recv(exp_len - act_len)
            act_len = len(data)
        return data

    #--------------------------------------------------------------------------
    def readline(self) -> str:
        """
        Read data from instrument over IP socket.

        Parameters
        ----------

        Returns
        ----------
        str
            String with data.

        Raises
        ----------
        """

        return self._socket.makefile().readline()

#-- class ---------------------------------------------------------------------

class file_transport(transport):
    """
    Class implementing file I/O to support driver testing.
    """

    #--------------------------------------------------------------------------
    def __init__(self, out_file_name: str, in_file_name: str = '') -> None:
        """
        Create file transport class.

        Parameters
        ----------
        out_file_name : str
            Output file name/path to write all commands to.
        in_file_name : str
            Input file name/path to read all command responses from.

        Returns
        ----------

        Raises
        ----------
        """

        self._out_file = open(out_file_name, 'wb+')
        self._in_file  = open(in_file_name, 'r')

    #--------------------------------------------------------------------------
    def __del__(self) -> None:
        """
        Delete file transport class.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        self.close()

    #--------------------------------------------------------------------------
    def close(self) -> None:
        """
        Close file descriptors.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        self._out_file.close()
        self._in_file.close()

    #--------------------------------------------------------------------------
    def write(self, cmd_str: str) -> None:
        """
        Write command to file.

        Parameters
        ----------
        cmd_str : str
            Command

        Returns
        ----------

        Raises
        ----------
        """

        out_str = cmd_str + '\n'
        self.write_binary(out_str.encode('ascii'))

    #--------------------------------------------------------------------------
    def write_binary(self, data: bytes) -> None:
        """
        Write binary data to file.

        Parameters
        ----------
        data : bytes
            Binary data

        Returns
        ----------

        Raises
        ----------
        """

        self._out_file.write(data)

    #--------------------------------------------------------------------------
    def read_binary(self, size: int) -> bytes:
        """
        Read binary data from file.

        Parameters
        ----------
        size : int
            Number of bytes

        Returns
        ----------
        bytes
            Binary data array of length "size".

        Raises
        ----------
        """

        return self._in_file.read(size)

    #--------------------------------------------------------------------------
    def readline(self) -> str:
        """
        Read data from file.

        Parameters
        ----------

        Returns
        ----------
        str
            String with data.

        Raises
        ----------
        """

        return self._in_file.readline()

#-- class ---------------------------------------------------------------------

class pulsar_dummy_transport(transport):
    """
    Class to replace Pulsar device with dummy device to support software stack testing without hardware.
    The class implements all mandatory, required and Pulsar specific SCPI calls. Call reponses are
    largely artifically constructed to be inline with the call's functionality (e.g. `*IDN?` returns valid,
    but artificial IDN data.) To assist development, the Q1ASM assembler has been completely implemented.
    Please have a look at the call's implentation to know what to expect from its response.
    """

    #--------------------------------------------------------------------------
    def __init__(self, cfg_format: str) -> None:
        """
        Create Pulsar dummy transport class.

        Parameters
        ----------
        cfg_format : str
            Configuration format based on `struct.pack <https://docs.python.org/3/library/struct.html>`_ format
            used to calculate configration transaction size.

        Returns
        ----------

        Raises
        ----------
        """

        self._cmd_hist         = []
        self._data_out         = 0
        self._bin_out          = None
        self._system_error     = []
        self._asm_status       = False
        self._asm_log          = ''
        self._cfg              = {}
        self._cfg_bin_size     = struct.calcsize(cfg_format)
        self._awg_waveforms    = {}
        self._acq_waveforms    = {}
        self._acq_acquisitions = {}
        self._cmds             = {"*CMDS?":                                         self._get_cmds,
                                  "*IDN?":                                          self._get_idn,
                                  "*RST":                                           self._reset,
                                  "SYSTem:ERRor:NEXT?":                             self._get_system_error,
                                  "SYSTem:ERRor:COUNt?":                            self._get_system_error_cnt,
                                  "STATus:ASSEMbler:SUCCess?":                      self._get_assembler_status,
                                  "STATus:ASSEMbler:LOG?":                          self._get_assembler_log,
                                  "SEQuencer#:PROGram":                             self._set_sequencer_program,
                                  "SEQuencer#:CONFiguration":                       self._set_sequencer_config,
                                  "SEQuencer#:CONFiguration?":                      self._get_sequencer_config,
                                  "SEQuencer#:AWG:WLISt:WAVeform:NEW":              self._add_awg_waveform,
                                  "SEQuencer#:AWG:WLISt:WAVeform:DELete":           self._del_awg_waveform,
                                  "SEQuencer#:AWG:WLISt:WAVeform:DATA":             self._set_awg_waveform_data,
                                  "SEQuencer#:AWG:WLISt:WAVeform:DATA?":            self._get_awg_waveform_data,
                                  "SEQuencer#:AWG:WLISt:WAVeform:INDex":            self._set_awg_waveform_index,
                                  "SEQuencer#:AWG:WLISt:WAVeform:INDex?":           self._get_awg_waveform_index,
                                  "SEQuencer#:AWG:WLISt:WAVeform:LENGth?":          self._get_awg_waveform_length,
                                  "SEQuencer#:AWG:WLISt:WAVeform:NAME?":            self._get_awg_waveform_name,
                                  "SEQuencer#:AWG:WLISt:SIZE?":                     self._get_num_awg_waveforms,
                                  "SEQuencer#:AWG:WLISt?":                          self._get_awg_waveform_names,
                                  "SEQuencer#:ACQ:WLISt:WAVeform:NEW":              self._add_acq_waveform,
                                  "SEQuencer#:ACQ:WLISt:WAVeform:DELete":           self._del_acq_waveform,
                                  "SEQuencer#:ACQ:WLISt:WAVeform:DATA":             self._set_acq_waveform_data,
                                  "SEQuencer#:ACQ:WLISt:WAVeform:DATA?":            self._get_acq_waveform_data,
                                  "SEQuencer#:ACQ:WLISt:WAVeform:INDex":            self._set_acq_waveform_index,
                                  "SEQuencer#:ACQ:WLISt:WAVeform:INDex?":           self._get_acq_waveform_index,
                                  "SEQuencer#:ACQ:WLISt:WAVeform:LENGth?":          self._get_acq_waveform_length,
                                  "SEQuencer#:ACQ:WLISt:WAVeform:NAME?":            self._get_acq_waveform_name,
                                  "SEQuencer#:ACQ:WLISt:SIZE?":                     self._get_num_acq_waveforms,
                                  "SEQuencer#:ACQ:WLISt?":                          self._get_acq_waveform_names,
                                  "SEQuencer#:ACQ:PATH#:ALISt:ACQuisition:NEW":     self._add_acq_acquisition,
                                  "SEQuencer#:ACQ:PATH#:ALISt:ACQuisition:DELete":  self._del_acq_acquisition,
                                  "SEQuencer#:ACQ:PATH#:ALISt:ACQuisition:DATA":    self._set_acq_acquisition_data,
                                  "SEQuencer#:ACQ:PATH#:ALISt:ACQuisition:DATA?":   self._get_acq_acquisition_data,
                                  "SEQuencer#:ACQ:PATH#:ALISt:ACQuisition:LENGth?": self._get_acq_acquisition_length,
                                  "SEQuencer#:ACQ:PATH#:ALISt:SIZE?":               self._get_num_acq_acquisitions,
                                  "SEQuencer#:ACQ:PATH#:ALISt?":                    self._get_acq_acquisition_names}

    #--------------------------------------------------------------------------
    def close(self) -> None:
        """
        Close and resets Pulsar dummy transport class.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        self.__init__('')

    #--------------------------------------------------------------------------
    def write(self, cmd_str: str) -> None:
        """
        Write command to Pulsar dummy. Stores command in command history (see :func:`ieee488_2.transport.pulsar_dummy_transport.get_cmd_hist`).

        Parameters
        ----------
        cmd_str : str
            Command

        Returns
        ----------

        Raises
        ----------
        """

        self._handle_cmd(cmd_str)

    #--------------------------------------------------------------------------
    def write_binary(self, data: bytes) -> None:
        """
        Write binary data to Pulsar dummy. Stores command in command history (see :func:`ieee488_2.transport.pulsar_dummy_transport.get_cmd_hist`).

        Parameters
        ----------
        data : bytes
            Binary data

        Returns
        ----------

        Raises
        ----------
        """

        cmd_parts = data.split('#'.encode())
        cmd_str   = cmd_parts[0].decode()
        bin_in    = '#'.encode() + '#'.encode().join(cmd_parts[1:])
        self._handle_cmd(cmd_str, bin_in)

    #--------------------------------------------------------------------------
    def read_binary(self, size: int) -> bytes:
        """
        Read binary data from Pulsar dummy.

        Parameters
        ----------
        size : int
            Number of bytes

        Returns
        ----------
        bytes
            Binary data array of length "size".

        Raises
        ----------
        """

        bin_var = self._bin_out[:size]
        self._bin_out = self._bin_out[size:]
        return bin_var

    #--------------------------------------------------------------------------
    def readline(self) -> str:
        """
        Read data from Pulsar dummy.

        Parameters
        ----------

        Returns
        ----------
        str
            String with data.

        Raises
        ----------
        """

        return self._data_out if isinstance(self._data_out, str) else str(self._data_out)

    #--------------------------------------------------------------------------
    def _handle_cmd(self, cmd_str: str, bin_in: bytes = 0) -> None:
        """
        Parse command and split it into command, parameters and arguments. Then execute associated command method found in command dictionary.
        If the command is not in the command dictionary, respond with the default response ('0'). The command is stored in the command history
        (see :func:`ieee488_2.transport.pulsar_dummy_transport.get_cmd_hist`).

        Parameters
        ----------
        cmd_str : str
            Command
        bin_in : bytes
            Binary data that needs to be send by the command.

        Returns
        ----------

        Raises
        ----------
        """

        cmd_parts  = cmd_str.split(' ')
        cmd_params = re.findall("[0-9]+", cmd_parts[0])
        cmd_args   = cmd_parts[1].split(',') if len(cmd_parts) > 1 else []
        cmd_args   = [arg.strip('"') for arg in cmd_args]
        cmd_str    = re.sub("[0-9]+", '#', cmd_parts[0])
        self._cmd_hist.append(cmd_str)

        if cmd_str in self._cmds:
            self._cmds[cmd_str](cmd_params, cmd_args, bin_in)
        else:
            self._data_out = 0
            self._bin_out  = self._encode_bin('0'.encode())

    #--------------------------------------------------------------------------
    @staticmethod
    def _encode_bin(data: bytes) -> None:
        """
        Encode binary data to be compatible with IEEE488.2.

        Parameters
        ----------
        data : bytes
            Binary data.

        Returns
        ----------

        Raises
        ----------
        """

        header_b = str(len(data)).encode()
        header_a = ('#' + str(len(header_b))).encode()
        end      = '\r\n'.encode()
        return header_a + header_b + data + end

    #--------------------------------------------------------------------------
    @staticmethod
    def _decode_bin(data: bytes) -> bytes:
        """
        Decode IEEE488.2 binary data.

        Parameters
        ----------
        data : bytes
            Binary data.

        Returns
        ----------

        Raises
        ----------
        RunTimeError
            Header error.
        """

        header_a = data[:2].decode() #Read '#N'
        data = data[2:]

        if header_a[0] != '#':
            raise RuntimeError('Header error: received {}'.format(header_a))
        header_b = data[:int(header_a[1])].decode()
        data = data[int(header_a[1]):]

        return data[:int(header_b)]

    #--------------------------------------------------------------------------
    def get_cmd_hist(self) -> list:
        """
        Get list of every executed command since the initialization or reset of the class.

        Parameters
        ----------

        Returns
        ----------
        list
            List of executed command strings including arguments (does not include binary data argument).

        Raises
        ----------
        """

        return self._cmd_hist

    #--------------------------------------------------------------------------
    def _get_cmds(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get SCPI commands.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = "THe:CAke:Is:A:LIe;cake;str;get_cake;lie;cake;str;0;Your trusty AI companion promised you a cake.;"

    #--------------------------------------------------------------------------
    def _get_idn(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get device identity and build information.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = "Qblox," + \
                         "Pulsar Dummy," + \
                         "whatever," + \
                         "fwVersion=0.0.0 fwBuild=28/11/1967-00:00:00 fwHash=0xDEADBEAF fwDirty=0 " + \
                         "kmodVersion=0.0.0 kmodBuild=15/07/1943-00:00:00 kmodHash=0x0D15EA5E kmodDirty=0 " + \
                         "swVersion=0.0.0 swBuild=11/05/1924-00:00:00 swHash=0xBEEFBABE swDirty=0"

    #--------------------------------------------------------------------------
    def _reset(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Reset Pulsar dummy.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self.close()

    #--------------------------------------------------------------------------
    def _get_system_error(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get system error from queue (see `SCPI <https://www.ivifoundation.org/docs/scpi-99.pdf>`_).

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if len(self._system_error) > 0:
            self._data_out = '0,' + self._system_error[0]
            self._system_error = self._system_error[1:]
        else:
            self._data_out = "No error"

    #--------------------------------------------------------------------------
    def _get_system_error_cnt(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get number of system errors (see `SCPI <https://www.ivifoundation.org/docs/scpi-99.pdf>`_).

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = str(len(self._system_error))

    #--------------------------------------------------------------------------
    def _get_assembler_status(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get assembler status. Refer to the assembler log to get more information regarding the assembler result.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = str(int(self._asm_status))

    #--------------------------------------------------------------------------
    def _get_assembler_log(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get assembler log.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._bin_out = self._encode_bin(self._asm_log.encode())



    #--------------------------------------------------------------------------
    def _set_sequencer_program(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Runs provided sequencer Q1ASM program through assembler. The assembler is a pre-compiled application, which is selected based on the platform this method
        is called on. The assembler status and log are stored and can be retrieved using corresponding methods. On a failure to assemble an error is set in
        system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        q1asm_str = self._decode_bin(bin_in).decode()
        fid = open("./tmp.q1asm", 'w')
        fid.write(q1asm_str)
        fid.close()

        if os.name == 'nt':
            assembler_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/assembler/q1asm_windows.exe")
            proc = subprocess.Popen([assembler_path, "-o", "tmp", "tmp.q1asm"], shell=True, text=True, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        elif sys.platform == 'darwin':
            assembler_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/assembler/q1asm_macos")
            proc = subprocess.Popen([assembler_path + " -o tmp tmp.q1asm"], shell=True, text=True, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            assembler_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/assembler/q1asm_linux")
            proc = subprocess.Popen([assembler_path + " -o tmp tmp.q1asm"], shell=True, text=True, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self._asm_log    = proc.communicate()[0]
        self._asm_status = not proc.returncode

        if not self._asm_status:
            self._system_error.append("Assembly failed.")

    #--------------------------------------------------------------------------
    def _set_sequencer_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Stores configuration of indexed sequencer; untouched and in binary format.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._cfg[cmd_params[0]] = self._decode_bin(bin_in)

    #--------------------------------------------------------------------------
    def _get_sequencer_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Retrieves previously stored configuration of the indexed sequencer. If no configuration was previously stored an array of
        zero bytes is returned. The length of the returned array is calculated based on the configuration format set during initialization
        of the class.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._cfg:
            self._bin_out = self._encode_bin(self._cfg[cmd_params[0]])
        else:
            self._bin_out = self._encode_bin(self._cfg_bin_size*b'\x00')



    #--------------------------------------------------------------------------
    def _add_awg_waveform(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Adds waveform to the waveform list of the indexed sequencer's AWG path. If the waveform name is already in use, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._system_error.append("Waveform {} already in waveform list.".format(cmd_args[0]))
                return

            for index in range(0, len(self._awg_waveforms[cmd_params[0]]) + 1):
                idx_unused = True
                for name in self._awg_waveforms[cmd_params[0]]:
                    if self._awg_waveforms[cmd_params[0]][name]["index"] == index:
                        idx_unused = False
                        break
                if idx_unused == True:
                    break
        else:
            self._awg_waveforms[cmd_params[0]] = {}
            index = 0
        self._awg_waveforms[cmd_params[0]][cmd_args[0]] = {"wave": [], "index": index}

    #--------------------------------------------------------------------------
    def _del_awg_waveform(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Deletes waveform from the waveform list of the indexed sequencer's AWG path. If the wavefrom name does not exist, an error is set in system error.
        The names "all" and "ALL" are reserved and those are deleted all waveforms in the waveform list of the indexed sequencer's AWG path are deleted.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_args[0].lower() == 'all':
            self._awg_waveforms[cmd_params[0]] = {}
        else:
            if cmd_params[0] in self._awg_waveforms:
                if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                    del self._awg_waveforms[cmd_params[0]][cmd_args[0]]
                    return
            self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _set_awg_waveform_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets waveform data for the waveform in the waveform list of the indexed sequencer's AWG path.
        If the wavefrom name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._awg_waveforms[cmd_params[0]][cmd_args[0]]["wave"] = self._decode_bin(bin_in)
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_awg_waveform_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform data of the waveform in the waveform list of the indexed sequencer's AWG path.
        If the wavefrom name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._bin_out = self._encode_bin(self._awg_waveforms[cmd_params[0]][cmd_args[0]]["wave"])
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _set_awg_waveform_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets waveform index of the waveform in the waveform list of the indexed sequencer's AWG path.
        If the wavefrom name does not exist or the index is already in use, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                for name in self._awg_waveforms[cmd_params[0]]:
                    if self._awg_waveforms[cmd_params[0]][name]["index"] == cmd_args[1] and name != cmd_args[0]:
                        self._system_error.append("Waveform index {} already in use by {}.".format(cmd_args[0], name))
                        return
                self._awg_waveforms[cmd_params[0]][cmd_args[0]]["index"] = cmd_args[1]
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_awg_waveform_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform index of the waveform in the waveform list of the indexed sequencer's AWG path.
        If the wavefrom name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._data_out = self._awg_waveforms[cmd_params[0]][cmd_args[0]]["index"]
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_awg_waveform_length(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform length of the waveform in the waveform list of the indexed sequencer's AWG path. The waveform lenght is returned as the number of samples.
        If the wavefrom name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._data_out = int(len(self._awg_waveforms[cmd_params[0]][cmd_args[0]]["wave"])/4)
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_awg_waveform_name(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform name of the waveform in the waveform list of the indexed sequencer's AWG path.
        If the wavefrom name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            for name in self._awg_waveforms[cmd_params[0]]:
                if self._awg_waveforms[cmd_params[0]][name]["index"] == cmd_args[0]:
                    self._data_out = name[1:-1]
                    return
        self._system_error.append("Waveform index {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_num_awg_waveforms(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Number of waveforms in the waveform list of the indexed sequencer's AWG path.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            self._data_out = len(self._awg_waveforms[cmd_params[0]])
        else:
            self._data_out = 0

    #--------------------------------------------------------------------------
    def _get_awg_waveform_names(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get the names of every waveform in the waveform list of the indexed sequencer's AWG path.
        The waveform names are returned in a ';'-separated string.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = ""
        if cmd_params[0] in self._awg_waveforms:
            names = ''
            for name in self._awg_waveforms[cmd_params[0]]:
                names += name + ';'
            self._data_out = names
            return



    #--------------------------------------------------------------------------
    def _add_acq_waveform(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Adds waveform to the waveform list of the indexed sequencer's acquisition path. If the waveform name is already in use, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_waveforms:
            if cmd_args[0] in self._acq_waveforms[cmd_params[0]]:
                self._system_error.append("Waveform {} already in waveform list.".format(cmd_args[0]))
                return

            for index in range(0, len(self._acq_waveforms[cmd_params[0]]) + 1):
                idx_unused = True
                for name in self._acq_waveforms[cmd_params[0]]:
                    if self._acq_waveforms[cmd_params[0]][name]["index"] == index:
                        idx_unused = False
                        break
                if idx_unused == True:
                    break
        else:
            self._acq_waveforms[cmd_params[0]] = {}
            index = 0
        self._acq_waveforms[cmd_params[0]][cmd_args[0]] = {"wave": [], "index": index}

    #--------------------------------------------------------------------------
    def _del_acq_waveform(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Deletes waveform from the waveform list of the indexed sequencer's acquisition path. If the wavefrom name does not exist, an error is set in system error.
        The names "all" and "ALL" are reserved and those are deleted all waveforms in the waveform list of the indexed sequencer's acquisition path are deleted.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_args[0].lower() == 'all':
            self._acq_waveforms[cmd_params[0]] = {}
        else:
            if cmd_params[0] in self._acq_waveforms:
                if cmd_args[0] in self._acq_waveforms[cmd_params[0]]:
                    del self._acq_waveforms[cmd_params[0]][cmd_args[0]]
                    return
            self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _set_acq_waveform_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets waveform data for the waveform in the waveform list of the indexed sequencer's acquisition path.
        If the wavefrom name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_waveforms:
            if cmd_args[0] in self._acq_waveforms[cmd_params[0]]:
                self._acq_waveforms[cmd_params[0]][cmd_args[0]]["wave"] = self._decode_bin(bin_in)
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_acq_waveform_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform data of the waveform in the waveform list of the indexed sequencer's acquisition path.
        If the wavefrom name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_waveforms:
            if cmd_args[0] in self._acq_waveforms[cmd_params[0]]:
                self._bin_out = self._encode_bin(self._acq_waveforms[cmd_params[0]][cmd_args[0]]["wave"])
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _set_acq_waveform_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets waveform index of the waveform in the waveform list of the indexed sequencer's acquisition path.
        If the wavefrom name does not exist or the index is already in use, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_waveforms:
            if cmd_args[0] in self._acq_waveforms[cmd_params[0]]:
                for name in self._acq_waveforms[cmd_params[0]]:
                    if self._acq_waveforms[cmd_params[0]][name]["index"] == cmd_args[1] and name != cmd_args[0]:
                        self._system_error.append("Waveform index {} already in use by {}.".format(cmd_args[0], name))
                        return
                self._acq_waveforms[cmd_params[0]][cmd_args[0]]["index"] = cmd_args[1]
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_acq_waveform_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform index of the waveform in the waveform list of the indexed sequencer's acquisition path.
        If the wavefrom name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_waveforms:
            if cmd_args[0] in self._acq_waveforms[cmd_params[0]]:
                self._data_out = self._acq_waveforms[cmd_params[0]][cmd_args[0]]["index"]
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_acq_waveform_length(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform length of the waveform in the waveform list of the indexed sequencer's acquisition path. The waveform lenght is returned as the number of samples.
        If the wavefrom name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_waveforms:
            if cmd_args[0] in self._acq_waveforms[cmd_params[0]]:
                self._data_out = int(len(self._acq_waveforms[cmd_params[0]][cmd_args[0]]["wave"])/4)
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_acq_waveform_name(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform name of the waveform in the waveform list of the indexed sequencer's acquisition path.
        If the wavefrom name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_waveforms:
            for name in self._acq_waveforms[cmd_params[0]]:
                if self._acq_waveforms[cmd_params[0]][name]["index"] == cmd_args[0]:
                    self._data_out = name[1:-1]
                    return
        self._system_error.append("Waveform index {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_num_acq_waveforms(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform name of the waveform in the waveform list of the indexed sequencer's acquistion path.
        If the wavefrom name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_waveforms:
            self._data_out = len(self._acq_waveforms[cmd_params[0]])
        else:
            self._data_out = 0

    #--------------------------------------------------------------------------
    def _get_acq_waveform_names(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get the names of every waveform in the waveform list of the indexed sequencer's acquistition path.
        The waveform names are returned in a ';'-separated string.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = ""
        if cmd_params[0] in self._acq_waveforms:
            names = ''
            for name in self._acq_waveforms[cmd_params[0]]:
                names += name + ';'
            self._data_out = names
            return



    #--------------------------------------------------------------------------
    def _add_acq_acquisition(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        if cmd_params[0] in self._acq_acquisitions:
            if cmd_params[1] in self._acq_acquisitions[cmd_params[0]]:
                if cmd_args[0] in self._acq_acquisitions[cmd_params[0]][cmd_params[1]]:
                    self._system_error.append("Acquisition {} already in acquisition list.".format(cmd_args[0]))
                else:
                    self._acq_acquisitions[cmd_params[0]][cmd_params[1]][cmd_args[0]] = {"size": cmd_args[1], "data": []}
            else:
                self._acq_acquisitions[cmd_params[0]][cmd_params[1]] = {cmd_args[0]: {"size": cmd_args[1], "data": []}}
        else:
            self._acq_acquisitions[cmd_params[0]] = {cmd_params[1]: {cmd_args[0]: {"size": cmd_args[1], "data": []}}}

    #--------------------------------------------------------------------------
    def _del_acq_acquisition(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        if cmd_params[0] in self._acq_acquisitions:
            if cmd_params[1] in self._acq_acquisitions[cmd_params[0]]:
                if cmd_args[0].lower() == 'all':
                    self._acq_acquisitions[cmd_params[0]][cmd_params[1]] = {}
                else:
                    if cmd_args[0] in self._acq_acquisitions[cmd_params[0]][cmd_params[1]]:
                        del self._acq_acquisitions[cmd_params[0]][cmd_params[1]][cmd_args[0]]
                        return
                    self._system_error.append("Acquisition {} does not exist in acquisition list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _set_acq_acquisition_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        if cmd_params[0] in self._acq_acquisitions:
            if cmd_params[1] in self._acq_acquisitions[cmd_params[0]]:
                if cmd_args[0] in self._acq_acquisitions[cmd_params[0]][cmd_params[1]]:
                    size = int(self._acq_acquisitions[cmd_params[0]][cmd_params[1]][cmd_args[0]]["size"])
                    if size > 2**14-1:
                        size = 2**14-1
                    self._acq_acquisitions[cmd_params[0]][cmd_params[1]][cmd_args[0]]["data"] = struct.pack('f'*size, *[(1.0/size)*i for i in range(0, size)])
                    return
        self._system_error.append("Acquisition {} does not exist in acquisition list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_acq_acquisition_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        if cmd_params[0] in self._acq_acquisitions:
            if cmd_params[1] in self._acq_acquisitions[cmd_params[0]]:
                if cmd_args[0] in self._acq_acquisitions[cmd_params[0]][cmd_params[1]]:
                    self._bin_out = self._encode_bin(self._acq_acquisitions[cmd_params[0]][cmd_params[1]][cmd_args[0]]["data"])
                    return
        self._system_error.append("Acquisition {} does not exist in acquisition list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_acq_acquisition_length(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        if cmd_params[0] in self._acq_acquisitions:
            if cmd_params[1] in self._acq_acquisitions[cmd_params[0]]:
                if cmd_args[0] in self._acq_acquisitions[cmd_params[0]][cmd_params[1]]:
                    self._data_out = int(len(self._acq_acquisitions[cmd_params[0]][cmd_params[1]][cmd_args[0]]["data"])/4)
                    return
        self._system_error.append("Acquisition {} does not exist in acquisition list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_num_acq_acquisitions(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        self._data_out = 0
        if cmd_params[0] in self._acq_acquisitions:
            if cmd_params[1] in self._acq_acquisitions[cmd_params[0]]:
                self._data_out = len(self._acq_acquisitions[cmd_params[0]][cmd_params[1]])
                return

    #--------------------------------------------------------------------------
    def _get_acq_acquisition_names(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        self._data_out = ""
        if cmd_params[0] in self._acq_acquisitions:
            if cmd_params[1] in self._acq_acquisitions[cmd_params[0]]:
                names = ''
                for name in self._acq_acquisitions[cmd_params[0]][cmd_params[1]]:
                    names += name + ';'
                self._data_out = names
                return
