#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2016-2018 Martin Olejar
# Copyright 2019-2021 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Status and error codes used by the MBoot protocol."""

from spsdk.utils.easy_enum import Enum


########################################################################################################################
# McuBoot Status Codes (Errors)
########################################################################################################################

class StatusCode(Enum):
    """McuBoot status codes."""

    SUCCESS = (0, 'Success', 'Success')
    FAIL = (1, 'Fail', 'Fail')
    READ_ONLY = (2, 'ReadOnly', 'Read Only Error')
    OUT_OF_RANGE = (3, 'OutOfRange', 'Out Of Range Error')
    INVALID_ARGUMENT = (4, 'InvalidArgument', 'Invalid Argument Error')
    TIMEOUT = (5, 'TimeoutError', 'Timeout Error')
    NO_TRANSFER_IN_PROGRESS = (6, 'NoTransferInProgress', 'No Transfer In Progress Error')

    # Flash driver errors.
    FLASH_SIZE_ERROR = (100, 'FlashSizeError', 'FLASH Driver: Size Error')
    FLASH_ALIGNMENT_ERROR = (101, 'FlashAlignmentError', 'FLASH Driver: Alignment Error')
    FLASH_ADDRESS_ERROR = (102, 'FlashAddressError', 'FLASH Driver: Address Error')
    FLASH_ACCESS_ERROR = (103, 'FlashAccessError', 'FLASH Driver: Access Error')
    FLASH_PROTECTION_VIOLATION = (104, 'FlashProtectionViolation', 'FLASH Driver: Protection Violation')
    FLASH_COMMAND_FAILURE = (105, 'FlashCommandFailure', 'FLASH Driver: Command Failure')
    FLASH_UNKNOWN_PROPERTY = (106, 'FlashUnknownProperty', 'FLASH Driver: Unknown Property')
    FLASH_REGION_EXECUTE_ONLY = (108, 'FlashRegionExecuteOnly', 'FLASH Driver: Region Execute Only')
    FLASH_EXEC_IN_RAM_NOT_READY = (
        109, 'FlashExecuteInRamFunctionNotReady', 'FLASH Driver: Execute In RAM Function Not Ready')
    FLASH_COMMAND_NOT_SUPPORTED = (111, 'FlashCommandNotSupported', 'FLASH Driver: Command Not Supported')
    FLASH_OUT_OF_DATE_CFPA_PAGE = (132, 'FlashOutOfDateCfpaPage', 'FLASH Driver: Out Of Date CFPA Page')
    FLASH_BLANK_IFR_PAGE_DATA = (133, 'FlashBlankIfrPageData', 'FLASH Driver: Blank IFR Page Data')
    FLASH_ENCRYPTED_REGIONS_ERASE_NOT_DONE_AT_ONCE = (
        134, 'FlashEncryptedRegionsEraseNotDoneAtOnce', 'FLASH Driver: Encrypted Regions Erase Not Done At Once')
    FLASH_PROGRAM_VERIFICATION_NOT_ALLOWED = (
        135, 'FlashProgramVerificationNotAllowed', 'FLASH Driver: Program Verification Not Allowed')
    FLASH_HASH_CHECK_ERROR = (136, 'FlashHashCheckError', 'FLASH Driver: Hash Check Error')
    FLASH_SEALED_FFR_REGION = (137, 'FlashSealedFfrRegion', 'FLASH Driver: Sealed FFR Region')
    FLASH_FFR_REGION_WRITE_BROKEN = (138, 'FlashFfrRegionWriteBroken', 'FLASH Driver: FFR Region Write Broken')
    FLASH_NMPA_UPDATE_NOT_ALLOWED = (139, 'FlashNmpaUpdateNotAllowed', 'FLASH Driver: NMPA Update Not Allowed')
    FLASH_CMPA_CFG_DIRECT_ERASE_NOT_ALLOWED = (
        140, 'FlashCmpaCfgDirectEraseNotAllowed', 'FLASH Driver: CMPA Cfg Direct Erase Not Allowed')
    FLASH_FFR_BANK_IS_LOCKED = (141, 'FlashFfrBankIsLocked', 'FLASH Driver: FFR Bank Is Locked')
    # I2C driver errors.
    I2C_SLAVE_TX_UNDERRUN = (200, 'I2cSlaveTxUnderrun', 'I2C Driver: Slave Tx Underrun')
    I2C_SLAVE_RX_OVERRUN = (201, 'I2cSlaveRxOverrun', 'I2C Driver: Slave Rx Overrun')
    I2C_ARBITRATION_LOST = (202, 'I2cArbitrationLost', 'I2C Driver: Arbitration Lost')

    # SPI driver errors.
    SPI_SLAVE_TX_UNDERRUN = (300, 'SpiSlaveTxUnderrun', 'SPI Driver: Slave Tx Underrun')
    SPI_SLAVE_RX_OVERRUN = (301, 'SpiSlaveRxOverrun', 'SPI Driver: Slave Rx Overrun')

    # QuadSPI driver errors.
    QSPI_FLASH_SIZE_ERROR = (400, 'QspiFlashSizeError', 'QSPI Driver: Flash Size Error')
    QSPI_FLASH_ALIGNMENT_ERROR = (401, 'QspiFlashAlignmentError', 'QSPI Driver: Flash Alignment Error')
    QSPI_FLASH_ADDRESS_ERROR = (402, 'QspiFlashAddressError', 'QSPI Driver: Flash Address Error')
    QSPI_FLASH_COMMAND_FAILURE = (403, 'QspiFlashCommandFailure', 'QSPI Driver: Flash Command Failure')
    QSPI_FLASH_UNKNOWN_PROPERTY = (404, 'QspiFlashUnknownProperty', 'QSPI Driver: Flash Unknown Property')
    QSPI_NOT_CONFIGURED = (405, 'QspiNotConfigured', 'QSPI Driver: Not Configured')
    QSPI_COMMAND_NOT_SUPPORTED = (406, 'QspiCommandNotSupported', 'QSPI Driver: Command Not Supported')
    QSPI_COMMAND_TIMEOUT = (407, 'QspiCommandTimeout', 'QSPI Driver: Command Timeout')
    QSPI_WRITE_FAILURE = (408, 'QspiWriteFailure', 'QSPI Driver: Write Failure')

    # OTFAD driver errors.
    OTFAD_SECURITY_VIOLATION = (500, 'OtfadSecurityViolation', 'OTFAD Driver: Security Violation')
    OTFAD_LOGICALLY_DISABLED = (501, 'OtfadLogicallyDisabled', 'OTFAD Driver: Logically Disabled')
    OTFAD_INVALID_KEY = (502, 'OtfadInvalidKey', 'OTFAD Driver: Invalid Key')
    OTFAD_INVALID_KEY_BLOB = (503, 'OtfadInvalidKeyBlob', 'OTFAD Driver: Invalid Key Blob')

    # SDMMC driver errors.

    # Bootloader errors.
    UNKNOWN_COMMAND = (10000, 'UnknownCommand', 'Unknown Command')
    SECURITY_VIOLATION = (10001, 'SecurityViolation', 'Security Violation')
    ABORT_DATA_PHASE = (10002, 'AbortDataPhase', 'Abort Data Phase')
    PING_ERROR = (10003, 'PingError', 'Ping Error')
    NO_RESPONSE = (10004, 'NoResponse', 'No Response')
    NO_RESPONSE_EXPECTED = (10005, 'NoResponseExpected', 'No Response Expected')
    UNSUPPORTED_COMMAND = (10006, 'UnsupportedCommand', 'Unsupported Command')

    # SB loader errors.
    ROMLDR_SECTION_OVERRUN = (10100, 'RomLdrSectionOverrun', 'ROM Loader: Section Overrun')
    ROMLDR_SIGNATURE = (10101, 'RomLdrSignature', 'ROM Loader: Signature Error')
    ROMLDR_SECTION_LENGTH = (10102, 'RomLdrSectionLength', 'ROM Loader: Section Length Error')
    ROMLDR_UNENCRYPTED_ONLY = (10103, 'RomLdrUnencryptedOnly', 'ROM Loader: Unencrypted Only')
    ROMLDR_EOF_REACHED = (10104, 'RomLdrEOFReached', 'ROM Loader: EOF Reached')
    ROMLDR_CHECKSUM = (10105, 'RomLdrChecksum', 'ROM Loader: Checksum Error')
    ROMLDR_CRC32_ERROR = (10106, 'RomLdrCrc32Error', 'ROM Loader: CRC32 Error')
    ROMLDR_UNKNOWN_COMMAND = (10107, 'RomLdrUnknownCommand', 'ROM Loader: Unknown Command')
    ROMLDR_ID_NOT_FOUND = (10108, 'RomLdrIdNotFound', 'ROM Loader: ID Not Found')
    ROMLDR_DATA_UNDERRUN = (10109, 'RomLdrDataUnderrun', 'ROM Loader: Data Underrun')
    ROMLDR_JUMP_RETURNED = (10110, 'RomLdrJumpReturned', 'ROM Loader: Jump Returned')
    ROMLDR_CALL_FAILED = (10111, 'RomLdrCallFailed', 'ROM Loader: Call Failed')
    ROMLDR_KEY_NOT_FOUND = (10112, 'RomLdrKeyNotFound', 'ROM Loader: Key Not Found')
    ROMLDR_SECURE_ONLY = (10113, 'RomLdrSecureOnly', 'ROM Loader: Secure Only')
    ROMLDR_RESET_RETURNED = (10114, 'RomLdrResetReturned', 'ROM Loader: Reset Returned')
    ROMLDR_ROLLBACK_BLOCKED = (10115, 'RomLdrRollbackBlocked', 'ROM Loader: Rollback Blocked')
    ROMLDR_INVALID_SECTION_MAC_COUNT = (10116, 'RomLdrInvalidSectionMacCount', 'ROM Loader: Invalid Section Mac Count')
    ROMLDR_UNEXPECTED_COMMAND = (10117, 'RomLdrUnexpectedCommand', 'ROM Loader: Unexpected Command')

    # Memory interface errors.
    MEMORY_RANGE_INVALID = (10200, 'MemoryRangeInvalid', 'Memory Range Invalid')
    MEMORY_READ_FAILED = (10201, 'MemoryReadFailed', 'Memory Read Failed')
    MEMORY_WRITE_FAILED = (10202, 'MemoryWriteFailed', 'Memory Write Failed')
    MEMORY_CUMULATIVE_WRITE = (10203, 'MemoryCumulativeWrite', 'Memory Cumulative Write')
    MEMORY_NOT_CONFIGURED = (10205, 'MemoryNotConfigured', 'Memory Not Configured')
    MEMORY_APP_OVERLAP_WITH_EXECUTE_ONLY_REGION = (
        10204, 'MemoryAppOverlapWithExecuteOnlyRegion', 'Memory App Overlap with exec region')
    MEMORY_NOT_CONFIGURED = (10205, 'MemoryNotConfigured', 'Memory Not Configured')
    MEMORY_ALIGNMENT_ERROR = (10206, 'MemoryAlignmentError', 'Memory Alignment Error')
    MEMORY_VERIFY_FAILED = (10207, 'MemoryVerifyFailed', 'Memory Verify Failed')
    MEMORY_WRITE_PROTECTED = (10208, 'MemoryWriteProtected', 'Memory Write Protected')
    MEMORY_ADDRESS_ERROR = (10209, 'MemoryAddressError', 'Memory Address Error')
    MEMORY_BLANK_CHECK_FAILED = (10210, 'MemoryBlankCheckFailed', 'Memory Black Check Failed')
    MEMORY_BLANK_PAGE_READ_DISALLOWED = (
        10211, 'MemoryBlankPageReadDisallowed', 'Memory Blank Page Read Disallowed')
    MEMORY_PROTECTED_PAGE_READ_DISALLOWED = (
        10212, 'MemoryProtectedPageReadDisallowed', 'Memory Protected Page Read Disallowed')
    MEMORY_FFR_SPEC_REGION_WRITE_BROKEN = (
        10213, 'MemoryFfrSpecRegionWriteBroken', 'Memory FFR Spec Region Write Broken')
    MEMORY_UNSUPPORTED_COMMAND = (10214, 'MemoryUnsupportedCommand', 'Memory Unsupported Command')

    # Property store errors.
    UNKNOWN_PROPERTY = (10300, 'UnknownProperty', 'Unknown Property')
    READ_ONLY_PROPERTY = (10301, 'ReadOnlyProperty', 'Read Only Property')
    INVALID_PROPERTY_VALUE = (10302, 'InvalidPropertyValue', 'Invalid Property Value')

    # Property store errors.
    APP_CRC_CHECK_PASSED = (10400, 'AppCrcCheckPassed', 'Application CRC Check: Passed')
    APP_CRC_CHECK_FAILED = (10401, 'AppCrcCheckFailed', 'Application: CRC Check: Failed')
    APP_CRC_CHECK_INACTIVE = (10402, 'AppCrcCheckInactive', 'Application CRC Check: Inactive')
    APP_CRC_CHECK_INVALID = (10403, 'AppCrcCheckInvalid', 'Application CRC Check: Invalid')
    APP_CRC_CHECK_OUT_OF_RANGE = (10404, 'AppCrcCheckOutOfRange', 'Application CRC Check: Out Of Range')

    # Packetizer errors.
    PACKETIZER_NO_PING_RESPONSE = (10500, 'NoPingResponse', 'Packetizer Error: No Ping Response')
    PACKETIZER_INVALID_PACKET_TYPE = (10501, 'InvalidPacketType', 'Packetizer Error: No response received for ping '
                                                                  'command')
    PACKETIZER_INVALID_CRC = (10502, 'InvalidCRC', 'Packetizer Error: Invalid packet type')
    PACKETIZER_NO_COMMAND_RESPONSE = (10503, 'NoCommandResponse', 'Packetizer Error: No response received for command')

    # Reliable Update statuses.
    RELIABLE_UPDATE_SUCCESS = (10600, 'ReliableUpdateSuccess', 'Reliable Update: Success')
    RELIABLE_UPDATE_FAIL = (10601, 'ReliableUpdateFail', 'Reliable Update: Fail')
    RELIABLE_UPDATE_INACIVE = (10602, 'ReliableUpdateInacive', 'Reliable Update: Inacive')
    RELIABLE_UPDATE_BACKUPAPPLICATIONINVALID = (
        10603, 'ReliableUpdateBackupApplicationInvalid', 'Reliable Update: Backup Application Invalid')
    RELIABLE_UPDATE_STILLINMAINAPPLICATION = (
        10604, 'ReliableUpdateStillInMainApplication', 'Reliable Update: Still In Main Application')
    RELIABLE_UPDATE_SWAPSYSTEMNOTREADY = (
        10605, 'ReliableUpdateSwapSystemNotReady', 'Reliable Update: Swap System Not Ready')
    RELIABLE_UPDATE_BACKUPBOOTLOADERNOTREADY = (
        10606, 'ReliableUpdateBackupBootloaderNotReady', 'Reliable Update: Backup Bootloader Not Ready')
    RELIABLE_UPDATE_SWAPINDICATORADDRESSINVALID = (
        10607, 'ReliableUpdateSwapIndicatorAddressInvalid', 'Reliable Update: Swap Indicator Address Invalid')
    RELIABLE_UPDATE_SWAPSYSTEMNOTAVAILABLE = (
        10608, 'ReliableUpdateSwapSystemNotAvailable', 'Reliable Update: Swap System Not Available')
    RELIABLE_UPDATE_SWAPTEST = (10609, 'ReliableUpdateSwapTest', 'Reliable Update: Swap Test')

    # Serial NOR/EEPROM statuses.
    SERIAL_NOR_EEPROM_ADDRESS_INVALID = (10700, 'SerialNorEepromAddressInvalid', 'SerialNorEeprom: Address Invalid')
    SERIAL_NOR_EEPROM_TRANSFER_ERROR = (10701, 'SerialNorEepromTransferError', 'SerialNorEeprom: Transfer Error')
    SERIAL_NOR_EEPROM_TYPE_INVALID = (10702, 'SerialNorEepromTypeInvalid', 'SerialNorEeprom: Type Invalid')
    SERIAL_NOR_EEPROM_SIZE_INVALID = (10703, 'SerialNorEepromSizeInvalid', 'SerialNorEeprom: Size Invalid')
    SERIAL_NOR_EEPROM_COMMAND_INVALID = (10704, 'SerialNorEepromCommandInvalid', 'SerialNorEeprom: Command Invalid')

    # FlexSPI NAND statuses.
    FLEXSPINAND_READ_PAGE_FAIL = (20000, 'FlexSPINANDReadPageFail', 'FlexSPINAND: Read Page Fail')
    FLEXSPINAND_READ_CACHE_FAIL = (20001, 'FlexSPINANDReadCacheFail', 'FlexSPINAND: Read Cache Fail')
    FLEXSPINAND_ECC_CHECK_FAIL = (20002, 'FlexSPINANDEccCheckFail', 'FlexSPINAND: Ecc Check Fail')
    FLEXSPINAND_PAGE_LOAD_FAIL = (20003, 'FlexSPINANDPageLoadFail', 'FlexSPINAND: Page Load Fail')
    FLEXSPINAND_PAGE_EXECUTE_FAIL = (20004, 'FlexSPINANDPageExecuteFail', 'FlexSPINAND: Page Execute Fail')
    FLEXSPINAND_ERASE_BLOCK_FAIL = (20005, 'FlexSPINANDEraseBlockFail', 'FlexSPINAND: Erase Block Fail')
    FLEXSPINAND_WAIT_TIMEOUT = (20006, 'FlexSPINANDWaitTimeout', 'FlexSPINAND: Wait Timeout')
    FlexSPINAND_NOT_SUPPORTED = (
        20007, 'SPINANDPageSizeOverTheMaxSupportedSize', 'SPI NAND: PageSize over the max supported size')
    FlexSPINAND_FCB_UPDATE_FAIL = (
        20008, 'FailedToUpdateFlashConfigBlockToSPINAND', 'SPI NAND: Failed to update Flash config block to SPI NAND')
    FlexSPINAND_DBBT_UPDATE_FAIL = (
        20009, 'Failed to update discovered bad block table to SPI NAND',
        'SPI NAND: Failed to update discovered bad block table to SPI NAND')
    FLEXSPINAND_WRITEALIGNMENTERROR = (20010, 'FlexSPINANDWriteAlignmentError', 'FlexSPINAND: Write Alignment Error')
    FLEXSPINAND_NOT_FOUND = (20011, 'FlexSPINANDNotFound', 'FlexSPINAND: Not Found')

    # FlexSPI NOR statuses.
    FLEXSPINOR_PROGRAM_FAIL = (20100, 'FLEXSPINORProgramFail', 'FLEXSPINOR: Program Fail')
    FLEXSPINOR_ERASE_SECTOR_FAIL = (20101, 'FLEXSPINOREraseSectorFail', 'FLEXSPINOR: Erase Sector Fail')
    FLEXSPINOR_ERASE_ALL_FAIL = (20102, 'FLEXSPINOREraseAllFail', 'FLEXSPINOR: Erase All Fail')
    FLEXSPINOR_WAIT_TIMEOUT = (20103, 'FLEXSPINORWaitTimeout', 'FLEXSPINOR:Wait Timeout')
    FLEXSPINOR_NOT_SUPPORTED = (20104, 'FLEXSPINORPageSizeOverTheMaxSupportedSize', 'FlexSPINOR: PageSize over the '
                                                                                    'max supported size')
    FLEXSPINOR_WRITE_ALIGNMENT_ERROR = (20105, 'FlexSPINORWriteAlignmentError', 'FlexSPINOR:Write Alignment Error')
    FLEXSPINOR_COMMANDFAILURE = (20106, 'FlexSPINORCommandFailure', 'FlexSPINOR: Command Failure')
    FLEXSPINOR_SFDP_NOTFOUND = (20107, 'FlexSPINORSFDPNotFound', 'FlexSPINOR: SFDP Not Found')
    FLEXSPINOR_UNSUPPORTED_SFDP_VERSION = (
        20108, 'FLEXSPINORUnsupportedSFDPVersion', 'FLEXSPINOR: Unsupported SFDP Version')
    FLEXSPINOR_FLASH_NOTFOUND = (20109, 'FLEXSPINORFlashNotFound', 'FLEXSPINOR Flash Not Found')
    FLEXSPINOR_DTR_READ_DUMMYPROBEFAILED = (
        20110, 'FLEXSPINORDTRReadDummyProbeFailed', 'FLEXSPINOR: DTR Read Dummy Probe Failed')

    OCOTP_READ_FAILURE = (20200, 'OCOTPReadFailure', 'OCOTP: Read Failure')
    OCOTP_PROGRAM_FAILURE = (20201, 'OCOTPProgramFailure', 'OCOTP: Program Failure')
    OCOTP_RELOAD_FAILURE = (20202, 'OCOTPReloadFailure', 'OCOTP: Reload Failure')
    OCOTP_WAIT_TIMEOUT = (20203, 'OCOTPWaitTimeout', 'OCOTP: Wait Timeout')

    # SEMC NOR statuses.
    SEMCNOR_DEVICE_TIMEOUT = (21100, 'SemcNOR_DeviceTimeout', 'SemcNOR: Device Timeout')
    SEMCNOR_INVALID_MEMORY_ADDRESS = (21101, 'SemcNOR_InvalidMemoryAddress', 'SemcNOR: Invalid Memory Address')
    SEMCNOR_UNMATCHED_COMMAND_SET = (21102, 'SemcNOR_unmatchedCommandSet', 'SemcNOR: unmatched Command Set')
    SEMCNOR_ADDRESS_ALIGNMENT_ERROR = (21103, 'SemcNOR_AddressAlignmentError', 'SemcNOR: Address Alignment Error')
    SEMCNOR_INVALID_CFI_SIGNATURE = (21104, 'SemcNOR_InvalidCfiSignature', 'SemcNOR: Invalid Cfi Signature')
    SEMCNOR_COMMAND_ERROR_NO_OP_TO_SUSPEND = (
        21105, 'SemcNOR_CommandErrorNoOpToSuspend', 'SemcNOR: Command Error No Op To Suspend')
    SEMCNOR_COMMAND_ERROR_NO_INFO_AVAILABLE = (
        21106, 'SemcNOR_CommandErrorNoInfoAvailable', 'SemcNOR: Command Error No Info Available')
    SEMCNOR_BLOCK_ERASE_COMMAND_FAILURE = (
        21107, 'SemcNOR_BlockEraseCommandFailure', 'SemcNOR: Block Erase Command Failure')
    SEMCNOR_BUFFER_PROGRAM_COMMAND_FAILURE = (
        21108, 'SemcNOR_BufferProgramCommandFailure', 'SemcNOR: Buffer Program Command Failure')
    SEMCNOR_PROGRAM_VERIFY_FAILURE = (21109, 'SemcNOR_ProgramVerifyFailure', 'SemcNOR: Program Verify Failure')
    SEMCNOR_ERASE_VERIFY_FAILURE = (21110, 'SemcNOR_EraseVerifyFailure', 'SemcNOR: Erase Verify Failure')
    SEMCNOR_INVALID_CFG_TAG = (21116, 'SemcNOR_InvalidCfgTag', 'SemcNOR: Invalid Cfg Tag')

    # SEMC NAND statuses.
    SEMCNAND_DEVICE_TIMEOUT = (21200, 'SemcNAND_DeviceTimeout', 'SemcNAND: Device Timeout')
    SEMCNAND_INVALID_MEMORY_ADDRESS = (21201, 'SemcNAND_InvalidMemoryAddress', 'SemcNAND: Invalid Memory Address')
    SEMCNAND_NOT_EQUAL_TO_ONE_PAGE_SIZE = (
        21202, 'SemcNAND_NotEqualToOnePageSize', 'SemcNAND: Not Equal To One Page Size')
    SEMCNAND_MORE_THAN_ONE_PAGE_SIZE = (21203, 'SemcNAND_MoreThanOnePageSize', 'SemcNAND: More Than One Page Size')
    SEMCNAND_ECC_CHECK_FAIL = (21204, 'SemcNAND_EccCheckFail', 'SemcNAND: Ecc Check Fail')
    SEMCNAND_INVALID_ONFI_PARAMETER = (21205, 'SemcNAND_InvalidOnfiParameter', 'SemcNAND: Invalid Onfi Parameter')
    SEMCNAND_CANNOT_ENABLE_DEVICE_ECC = (21206, 'SemcNAND_CannotEnableDeviceEcc', 'SemcNAND: Cannot Enable Device Ecc')
    SEMCNAND_SWITCH_TIMING_MODE_FAILURE = (
        21207, 'SemcNAND_SwitchTimingModeFailure', 'SemcNAND: Switch Timing Mode Failure')
    SEMCNAND_PROGRAM_VERIFY_FAILURE = (21208, 'SemcNAND_ProgramVerifyFailure', 'SemcNAND: Program Verify Failure')
    SEMCNAND_ERASE_VERIFY_FAILURE = (21209, 'SemcNAND_EraseVerifyFailure', 'SemcNAND: Erase Verify Failure')
    SEMCNAND_INVALID_READBACK_BUFFER = (21210, 'SemcNAND_InvalidReadbackBuffer', 'SemcNAND: Invalid Readback Buffer')
    SEMCNAND_INVALID_CFG_TAG = (21216, 'SemcNAND_InvalidCfgTag', 'SemcNAND: Invalid Cfg Tag')
    SEMCNAND_FAIL_TO_UPDATE_FCB = (21217, 'SemcNAND_FailToUpdateFcb', 'SemcNAND: Fail To Update Fcb')
    SEMCNAND_FAIL_TO_UPDATE_DBBT = (21218, 'SemcNAND_FailToUpdateDbbt', 'SemcNAND: Fail To Update Dbbt')
    SEMCNAND_DISALLOW_OVERWRITE_BCB = (21219, 'SemcNAND_DisallowOverwriteBcb', 'SemcNAND: Disallow Overwrite Bcb')
    SEMCNAND_ONLY_SUPPORT_ONFI_DEVICE = (21220, 'SemcNAND_OnlySupportOnfiDevice', 'SemcNAND: Only Support Onfi Device')
    SEMCNAND_MORE_THAN_MAX_IMAGE_COPY = (21221, 'SemcNAND_MoreThanMaxImageCopy', 'SemcNAND: More Than Max Image Copy')
    SEMCNAND_DISORDERED_IMAGE_COPIES = (21222, 'SemcNAND_DisorderedImageCopies', 'SemcNAND: Disordered Image Copies')

    # SPIFI NOR statuses.
    SPIFINOR_PROGRAM_FAIL = (22000, 'SPIFINOR_ProgramFail', 'SPIFINOR: Program Fail')
    SPIFINOR_ERASE_SECTORFAIL = (22001, 'SPIFINOR_EraseSectorFail', 'SPIFINOR: Erase Sector Fail')
    SPIFINOR_ERASE_ALL_FAIL = (22002, 'SPIFINOR_EraseAllFail', 'SPIFINOR: Erase All Fail')
    SPIFINOR_WAIT_TIMEOUT = (22003, 'SPIFINOR_WaitTimeout', 'SPIFINOR: Wait Timeout')
    SPIFINOR_NOT_SUPPORTED = (22004, 'SPIFINOR_NotSupported', 'SPIFINOR: Not Supported')
    SPIFINOR_WRITE_ALIGNMENTERROR = (22005, 'SPIFINOR_WriteAlignmentError', 'SPIFINOR: Write Alignment Error')
    SPIFINOR_COMMAND_FAILURE = (22006, 'SPIFINOR_CommandFailure', 'SPIFINOR: Command Failure')
    SPIFINOR_SFDP_NOT_FOUND = (22007, 'SPIFINOR_SFDP_NotFound', 'SPIFINOR: SFDP Not Found')

    # OTP statuses.
    OTP_INVALID_ADDRESS = (52801, 'OTP_InvalidAddress', 'OTD: Invalid OTP address')
    OTP_PROGRAM_FAIL = (52802, 'OTP_ProgrammingFail', 'OTD: Programming failed')
    OTP_CRC_FAIL = (52803, 'OTP_CRCFail', 'OTP: CRC check failed')
    OTP_ERROR = (52804, 'OTP_Error', 'OTP: Error happened during OTP operation')
    OTP_ECC_CRC_FAIL = (52805, 'OTP_EccCheckFail', 'OTP: ECC check failed during OTP operation')
    OTP_LOCKED = (52806, 'OTP_FieldLocked', 'OTP: Field is locked when programming')
    OTP_TIMEOUT = (52807, 'OTP_Timeout', 'OTP: Operation timed out')
    OTP_CRC_CHECK_PASS = (52808, 'OTP_CRCCheckPass', 'OTP: CRC check passed')

    # FlexSPI statuses.
    FLEXSPI_SEQUENCE_EXECUTION_TIMEOUT = (
        70000, 'FLEXSPI_SequenceExecutionTimeout', 'FLEXSPI: Sequence Execution Timeout')
    FLEXSPI_INVALID_SEQUENCE = (70001, 'FLEXSPI_InvalidSequence', 'FLEXSPI: Invalid Sequence')
    FLEXSPI_DEVICE_TIMEOUT = (70002, 'FLEXSPI_DeviceTimeout', 'FLEXSPI: Device Timeout')
