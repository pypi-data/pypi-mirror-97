'''
File: nativemethods.py
Project: pyautd3
Created Date: 30/12/2020
Author: Shun Suzuki
-----
Last Modified: 08/03/2021
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2021 Hapis Lab. All rights reserved.

'''

import os
import threading
import ctypes
from ctypes import c_void_p, c_bool, c_int, POINTER, c_float, c_char_p, c_ubyte, c_uint, c_ulong, c_ushort


class Singleton(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Nativemethods(metaclass=Singleton):
    main_dll = None
    gain_holo_dll = None
    link_soem_dll = None
    link_twincat_dll = None
    modulation_from_file_dll = None

    # SOEM link requires wpcap.dll on Windows. Therefore, it should not be loaded until it is actually need.
    def init_soem_dll(self):
        if self.link_soem_dll is not None:
            return

        self.link_soem_dll = ctypes.CDLL(os.path.join(self._bin_location, self._bin_name_base + '-link-soem' + self._bin_ext))

        self.link_soem_dll.AUTDSOEMLink.argtypes = [POINTER(c_void_p), c_char_p, c_int]
        self.link_soem_dll.AUTDSOEMLink.restypes = [None]

        self.link_soem_dll.AUTDGetAdapterPointer.argtypes = [POINTER(c_void_p)]
        self.link_soem_dll.AUTDGetAdapterPointer.restypes = [c_int]

        self.link_soem_dll.AUTDGetAdapter.argtypes = [c_void_p, c_int, c_char_p, c_char_p]
        self.link_soem_dll.AUTDGetAdapter.restypes = [None]

        self.link_soem_dll.AUTDFreeAdapterPointer.argtypes = [c_void_p]
        self.link_soem_dll.AUTDFreeAdapterPointer.restypes = [None]

    def init_dll(self, bin_location, bin_name_base, bin_ext):
        self._bin_location = bin_location
        self._bin_name_base = bin_name_base
        self._bin_ext = bin_ext

        self.main_dll = ctypes.CDLL(os.path.join(bin_location, bin_name_base + bin_ext))
        self.gain_holo_dll = ctypes.CDLL(os.path.join(bin_location, bin_name_base + '-gain-holo' + bin_ext))
        self.link_twincat_dll = ctypes.CDLL(os.path.join(bin_location, bin_name_base + '-link-twincat' + bin_ext))
        self.modulation_from_file_dll = ctypes.CDLL(os.path.join(bin_location, bin_name_base + '-modulation-from-file' + bin_ext))

        self.main_dll.AUTDCreateController.argtypes = [POINTER(c_void_p)]
        self.main_dll.AUTDCreateController.restypes = [None]

        self.main_dll.AUTDOpenControllerWith.argtypes = [c_void_p, c_void_p]
        self.main_dll.AUTDOpenControllerWith.restypes = [c_int]

        self.main_dll.AUTDAddDevice.argtypes = [c_void_p, c_float, c_float, c_float, c_float, c_float, c_float, c_int]
        self.main_dll.AUTDAddDevice.restypes = [c_int]

        self.main_dll.AUTDAddDeviceQuaternion.argtypes = [c_void_p, c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_int]
        self.main_dll.AUTDAddDeviceQuaternion.restypes = [c_int]

        self.main_dll.AUTDCalibrate.argtypes = [c_void_p, c_int, c_int]
        self.main_dll.AUTDCalibrate.restypes = [c_bool]

        self.main_dll.AUTDCloseController.argtypes = [c_void_p]
        self.main_dll.AUTDCloseController.restypes = [None]

        self.main_dll.AUTDClear.argtypes = [c_void_p]
        self.main_dll.AUTDClear.restypes = [None]

        self.main_dll.AUTDFreeController.argtypes = [c_void_p]
        self.main_dll.AUTDFreeController.restypes = [None]

        self.main_dll.AUTDSetSilentMode.argtypes = [c_void_p, c_bool]
        self.main_dll.AUTDSetSilentMode.restypes = [None]

        self.main_dll.AUTDStop.argtypes = [c_void_p]
        self.main_dll.AUTDStop.restypes = [None]

        self.main_dll.AUTDGetFirmwareInfoListPointer.argtypes = [c_void_p, POINTER(c_void_p)]
        self.main_dll.AUTDGetFirmwareInfoListPointer.restypes = [c_int]

        self.main_dll.AUTDGetFirmwareInfo.argtypes = [c_void_p, c_int, c_char_p, c_char_p]
        self.main_dll.AUTDGetFirmwareInfo.restypes = [None]

        self.main_dll.AUTDFreeFirmwareInfoListPointer.argtypes = [c_void_p]
        self.main_dll.AUTDFreeFirmwareInfoListPointer.restypes = [None]

        self.main_dll.AUTDIsOpen.argtypes = [c_void_p]
        self.main_dll.AUTDIsOpen.restypes = [c_bool]

        self.main_dll.AUTDIsSilentMode.argtypes = [c_void_p]
        self.main_dll.AUTDIsSilentMode.restypes = [c_bool]

        self.main_dll.AUTDWavelength.argtypes = [c_void_p]
        self.main_dll.AUTDWavelength.restypes = [c_float]

        self.main_dll.AUTDSetWavelength.argtypes = [c_void_p, c_float]
        self.main_dll.AUTDSetWavelength.restypes = [None]

        self.main_dll.AUTDNumDevices.argtypes = [c_void_p]
        self.main_dll.AUTDNumDevices.restypes = [c_int]

        self.main_dll.AUTDNumTransducers.argtypes = [c_void_p]
        self.main_dll.AUTDNumTransducers.restypes = [c_int]

        self.main_dll.AUTDRemainingInBuffer.argtypes = [c_void_p]
        self.main_dll.AUTDRemainingInBuffer.restypes = [c_ulong]

        self.main_dll.AUTDFocalPointGain.argtypes = [POINTER(c_void_p), c_float, c_float, c_float, c_ubyte]
        self.main_dll.AUTDFocalPointGain.restypes = [None]

        self.main_dll.AUTDGroupedGain.argtypes = [POINTER(c_void_p), POINTER(c_int), POINTER(c_void_p), c_int]
        self.main_dll.AUTDGroupedGain.restypes = [None]

        self.main_dll.AUTDBesselBeamGain.argtypes = [POINTER(c_void_p), c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_ubyte]
        self.main_dll.AUTDBesselBeamGain.restypes = [None]

        self.main_dll.AUTDPlaneWaveGain.argtypes = [POINTER(c_void_p), c_float, c_float, c_float, c_ubyte]
        self.main_dll.AUTDPlaneWaveGain.restypes = [None]

        self.main_dll.AUTDCustomGain.argtypes = [POINTER(c_void_p), POINTER(c_ushort), c_int]
        self.main_dll.AUTDCustomGain.restypes = [None]

        self.gain_holo_dll.AUTDHoloGain.argtypes = [POINTER(c_void_p), POINTER(c_float), POINTER(c_float), c_int, c_int, c_void_p]
        self.gain_holo_dll.AUTDHoloGain.restypes = [None]

        self.main_dll.AUTDTransducerTestGain.argtypes = [POINTER(c_void_p), c_int, c_ubyte, c_ubyte]
        self.main_dll.AUTDTransducerTestGain.restypes = [None]

        self.main_dll.AUTDNullGain.argtypes = [POINTER(c_void_p)]
        self.main_dll.AUTDNullGain.restypes = [None]

        self.main_dll.AUTDDeleteGain.argtypes = [c_void_p]
        self.main_dll.AUTDDeleteGain.restypes = [None]

        self.main_dll.AUTDModulation.argtypes = [POINTER(c_void_p), c_ubyte]
        self.main_dll.AUTDModulation.restypes = [None]

        self.main_dll.AUTDCustomModulation.argtypes = [POINTER(c_void_p), POINTER(c_ubyte), c_uint]
        self.main_dll.AUTDCustomModulation.restypes = [None]

        self.modulation_from_file_dll.AUTDRawPCMModulation.argtypes = [POINTER(c_void_p), c_char_p, c_float]
        self.modulation_from_file_dll.AUTDRawPCMModulation.restypes = [None]

        self.main_dll.AUTDSawModulation.argtypes = [POINTER(c_void_p), c_int]
        self.main_dll.AUTDSawModulation.restypes = [None]

        self.main_dll.AUTDSineModulation.argtypes = [POINTER(c_void_p), c_int, c_float, c_float]
        self.main_dll.AUTDSineModulation.restypes = [None]

        self.main_dll.AUTDSquareModulation.argtypes = [POINTER(c_void_p), c_int, c_ubyte, c_ubyte]
        self.main_dll.AUTDSquareModulation.restypes = [None]

        self.modulation_from_file_dll.AUTDWavModulation.argtypes = [POINTER(c_void_p), c_char_p]
        self.modulation_from_file_dll.AUTDWavModulation.restypes = [None]

        self.main_dll.AUTDDeleteModulation.argtypes = [c_void_p]
        self.main_dll.AUTDDeleteModulation.restypes = [None]

        self.main_dll.AUTDSequence.argtypes = [POINTER(c_void_p)]
        self.main_dll.AUTDSequence.restypes = [None]

        self.main_dll.AUTDSequenceAppendPoint.argtypes = [c_void_p, c_float, c_float, c_float]
        self.main_dll.AUTDSequenceAppendPoint.restypes = [None]

        self.main_dll.AUTDSequenceAppendPoints.argtypes = [c_void_p, POINTER(c_float), c_ulong]
        self.main_dll.AUTDSequenceAppendPoints.restypes = [None]

        self.main_dll.AUTDSequenceSetFreq.argtypes = [c_void_p, c_float]
        self.main_dll.AUTDSequenceSetFreq.restypes = [c_float]

        self.main_dll.AUTDSequenceFreq.argtypes = [c_void_p]
        self.main_dll.AUTDSequenceFreq.restypes = [c_float]

        self.main_dll.AUTDSequenceSamplingFreq.argtypes = [c_void_p]
        self.main_dll.AUTDSequenceSamplingFreq.restypes = [c_float]

        self.main_dll.AUTDSequenceSamplingFreqDiv.argtypes = [c_void_p]
        self.main_dll.AUTDSequenceSamplingFreqDiv.restypes = [c_ushort]

        self.main_dll.AUTDCircumSequence.argtypes = [POINTER(c_void_p), c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_ulong]
        self.main_dll.AUTDCircumSequence.restypes = [None]

        self.main_dll.AUTDDeleteSequence.argtypes = [c_void_p]
        self.main_dll.AUTDDeleteSequence.restypes = [None]

        self.link_twincat_dll.AUTDTwinCATLink.argtypes = [POINTER(c_void_p), c_char_p, c_char_p]
        self.link_twincat_dll.AUTDTwinCATLink.restypes = [None]

        self.link_twincat_dll.AUTDLocalTwinCATLink.argtypes = [POINTER(c_void_p)]
        self.link_twincat_dll.AUTDLocalTwinCATLink.restypes = [None]

        self.main_dll.AUTDAppendGain.argtypes = [c_void_p, c_void_p]
        self.main_dll.AUTDAppendGain.restypes = [None]

        self.main_dll.AUTDAppendGainSync.argtypes = [c_void_p, c_void_p, c_bool]
        self.main_dll.AUTDAppendGainSync.restypes = [None]

        self.main_dll.AUTDAppendModulation.argtypes = [c_void_p, c_void_p]
        self.main_dll.AUTDAppendModulation.restypes = [None]

        self.main_dll.AUTDAppendModulationSync.argtypes = [c_void_p, c_void_p]
        self.main_dll.AUTDAppendModulationSync.restypes = [None]

        self.main_dll.AUTDAppendSTMGain.argtypes = [c_void_p, c_void_p]
        self.main_dll.AUTDAppendSTMGain.restypes = [None]

        self.main_dll.AUTDStartSTModulation.argtypes = [c_void_p, c_float]
        self.main_dll.AUTDStartSTModulation.restypes = [None]

        self.main_dll.AUTDStopSTModulation.argtypes = [c_void_p]
        self.main_dll.AUTDStopSTModulation.restypes = [None]

        self.main_dll.AUTDFinishSTModulation.argtypes = [c_void_p]
        self.main_dll.AUTDFinishSTModulation.restypes = [None]

        self.main_dll.AUTDAppendSequence.argtypes = [c_void_p, c_void_p]
        self.main_dll.AUTDAppendSequence.restypes = [None]

        self.main_dll.AUTDFlush.argtypes = [c_void_p]
        self.main_dll.AUTDFlush.restypes = [None]

        self.main_dll.AUTDDeviceIdxForTransIdx.argtypes = [c_void_p, c_int]
        self.main_dll.AUTDDeviceIdxForTransIdx.restypes = [c_int]

        self.main_dll.AUTDTransPositionByGlobal.argtypes = [c_void_p, c_int]
        self.main_dll.AUTDTransPositionByGlobal.restypes = [POINTER(c_float)]

        self.main_dll.AUTDTransPositionByLocal.argtypes = [c_void_p, c_int, c_int]
        self.main_dll.AUTDTransPositionByLocal.restypes = [POINTER(c_float)]

        self.main_dll.AUTDDeviceDirection.argtypes = [c_void_p, c_int]
        self.main_dll.AUTDDeviceDirection.restypes = [POINTER(c_float)]
