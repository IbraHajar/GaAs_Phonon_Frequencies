import random
import os
import shutil

CWD = os.getcwd()
CONF_FILES_DIR = os.path.join(CWD, 'conf_files')
POSCAR = os.path.join(CWD, 'required_files/POSCAR')
FORCE_SETS = os.path.join(CWD, 'required_files/FORCE_SETS')

NUM_CONF_FILES = 10

NUMBER_OF_ATOMS = 512

gallium1 = 68.9255736
gallium2 = 70.9247013
arsenic = 74.921595

ratio = 0.39892

for file_num in range(NUM_CONF_FILES):
    gallium_list = []

    for count in range(int(NUMBER_OF_ATOMS/2)):
        r = random.random()
        if r <= ratio:
            gallium_list.append(gallium2)
        else:
            gallium_list.append(gallium1)
    print(file_num)

    dir_name = f'{file_num:05}'
    file_name = 'mesh.conf'

    path_to_dir = os.path.join(CWD, CONF_FILES_DIR, dir_name)
    os.mkdir(path_to_dir)

    path_to_file = os.path.join(CWD, CONF_FILES_DIR, dir_name, file_name)
    with open(path_to_file, 'w') as f:
        f.write('ATOM_NAME = Ga As\n')
        f.write('DIM = 4 4 4\n')
        f.write('MP = 1 1 1\n')
        f.write('EIGENVECTORS = .TRUE.\n')
        f.write('PRIMITIVE_AXES = 4 0 0  0 4 0  0 0 4\n')
        f.write('MASS = ')
        for element in gallium_list:
            f.write(f'{element} ')
        for _ in range(int(NUMBER_OF_ATOMS/2)):
            f.write(f'{arsenic} ')
    shutil.copy(POSCAR, path_to_dir)
    shutil.copy(FORCE_SETS, path_to_dir)
