from os import walk, path
from pathlib import Path
from shutil import copyfile

PINNED_KEYWORDS = ['ibiza', 'spanien', 'balearen']
NOT_PINNED_KEYWORDS = ['pool', 'meeresblick', 'luxusurlaub', 'privat', 'luxusvilla', 'aktivurlaub']

INPUT_DIR = '.'
OUTPUT_DIR = path.join(INPUT_DIR, 'renamed_images')
SUPPORTED_EXTENSIONS = ['jpg', 'jpeg', 'png']


def check_overflow(index, overflow_counter, suffix):
    try:
        NOT_PINNED_KEYWORDS[index]
    except IndexError:
        index = 0
        overflow_counter += 1
        suffix = f'_{overflow_counter}'
    return index, overflow_counter, suffix


def assemble_filename(index):
    filename = f"{' '.join(PINNED_KEYWORDS)} {NOT_PINNED_KEYWORDS[index]}"
    return filename


def rename_images(input_directory, output_directory):
    _, _, filenames = next(walk(input_directory))
    index = 0
    suffix = ''
    overflow_counter = 0
    for filename in filenames:
        filename_no_extension, file_extension = filename.rsplit('.', maxsplit=1)
        if file_extension.lower() not in SUPPORTED_EXTENSIONS:
            continue
        file_path = path.join(input_directory, filename)
        index, overflow_counter, suffix = check_overflow(index, overflow_counter, suffix)
        file_path_new = path.join(output_directory, assemble_filename(index) + suffix + f'.{file_extension}')
        copyfile(file_path, file_path_new)
        index += 1
    return


if __name__ == '__main__':
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    rename_images(INPUT_DIR, OUTPUT_DIR)
