import pathlib

import usb.core

try:
    from mp.firmware import pydfu
except ImportError:
    import pydfu

URL_README = pydfu.URL_README

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).absolute().parent

def main():
    try:
        pydfu.init()
    except usb.core.NoBackendError:
        raise SystemExit(f"ERROR: Driver not installed. Please follow 'Install USB driver for STM32 BOOTLOADER' on {URL_README}")

    list_firmwares = sorted(DIRECTORY_OF_THIS_FILE.glob('*.dfu'), reverse=True)
    print(f'Firmwares available:')
    for i, firmware in enumerate(list_firmwares):
        print(f'  [{i}] {firmware.name}')
    selected = input('Which firmware do you want to program? ')
    firmware_filename = list_firmwares[int(selected)]

    elements = pydfu.read_dfu_file(str(firmware_filename))
    if not elements:
        print('No data in dfu file')
        return
    print('Writing memory...')
    pydfu.write_elements(elements, mass_erase_used=False, progress=pydfu.cli_progress)

    print(f'Successfully wrote {firmware_filename.name}')
    pydfu.exit_dfu()


if __name__ == '__main__':
    main()
