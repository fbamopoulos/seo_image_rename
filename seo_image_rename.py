from os import walk, path
from pathlib import Path
from shutil import copyfile

PINNED_KEYWORDS = ['ibiza', 'spanien', 'balearen']
NOT_PINNED_KEYWORDS = ['pool', 'meeresblick', 'luxusurlaub', 'privat', 'luxusvilla', 'aktivurlaub']

INPUT_DIR = '.'
OUTPUT_DIR = path.join(INPUT_DIR, 'renamed_images')
SUPPORTED_EXTENSIONS = ['jpg', 'jpeg', 'png']


def assemble_filename(pinned_index, not_pinned_index):
    filename = f'{PINNED_KEYWORDS[pinned_index]} {NOT_PINNED_KEYWORDS[not_pinned_index]}'
    return filename


def rename_images(input_directory, output_directory):
    _, _, filenames = next(walk(input_directory))
    pinned_index = 0
    not_pinned_index = 0
    suffix = ''
    overflow_counter = 0
    for filename in filenames:
        filename_no_extension, file_extension = filename.rsplit('.', maxsplit=1)
        if file_extension.lower() not in SUPPORTED_EXTENSIONS:
            continue
        file_path = path.join(input_directory, filename)
        file_path_new = path.join(output_directory,
                                  assemble_filename(pinned_index, not_pinned_index) + suffix + f'.{file_extension}')
        copyfile(file_path, file_path_new)
        not_pinned_index += 1
        if not_pinned_index == len(NOT_PINNED_KEYWORDS):
            not_pinned_index = 0
            pinned_index += 1
            if pinned_index == len(PINNED_KEYWORDS):
                pinned_index = 0
                overflow_counter += 1
                suffix = f'_{overflow_counter}'
    return


if __name__ == '__main__':
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    rename_images(INPUT_DIR, OUTPUT_DIR)
    print('Done')
