import yaml
import numpy as np
import time
import multiprocessing
import os


def get_data(path):
    with open(path, 'r') as stream:
        data = yaml.load(stream, Loader=yaml.CLoader)
    return data


def get_all_data(paths):
    with multiprocessing.Pool() as pool:
        y = pool.map(get_data, paths)
    return y


def frequency(data):
    phonon = data['phonon']
    band = phonon[0]['band']
    return np.array([row['frequency'] for row in band])


def get_all_frequencies(all_data):
    with multiprocessing.Pool() as pool:
        y = pool.map(frequency, all_data)
    return y


def eigenvector(data):
    n_modes = 1536
    phonon = data['phonon']
    band = phonon[0]['band']
    eigenvectors = np.array([band[b]['eigenvector'] for b in range(n_modes)])
    eigenvectors = eigenvectors[:, :, :, 0]
    eigenvectors = eigenvectors.reshape(n_modes, n_modes)
    return eigenvectors


def get_all_eigenvectors(all_data):
    with multiprocessing.Pool() as pool:
        y = pool.map(eigenvector, all_data)
    return y


def normalize_eigenvector(v):
    if v.all() == 0:
        return v
    rows = v.shape[0]
    norm_v = np.linalg.norm(v, axis=1)
    return v / norm_v.reshape(rows, 1)


def normalize_base(b):
    if b.all() == 0:
        return b
    return b / np.linalg.norm(b)


def normalize_all(vectors):
    with multiprocessing.Pool() as pool:
        y = pool.map(normalize_eigenvector, vectors)
    return y


def normalize_all_bases(bases):
    with multiprocessing.Pool() as pool:
        y = pool.map(normalize_base, bases)
    return y


def dot_product(t):
    return np.dot(t[0], t[1])


def dot_products(ts):
    with multiprocessing.Pool() as pool:
        y = pool.map(dot_product, ts)
    return y


def get_argmax(v):
    return np.argmax(v)


def get_all_argmaxs(vectors):
    with multiprocessing.Pool() as pool:
        y = pool.map(get_argmax, vectors)
    return y


def max_frequency(t):
    return t[0][t[1]]


def get_all_max_frequencies(ts):
    with multiprocessing.Pool() as pool:
        y = pool.map(max_frequency, ts)
    return y


def get_bases(path):
    data = get_data(path)

    phonon = data['phonon']
    band = phonon['band']

    gallium = [band[3]['eigenvector'][0][i][0] for i in range(3)]
    arsenic = [band[3]['eigenvector'][1][i][0] for i in range(3)]
    base1 = np.array(gallium * 256 + arsenic * 256)

    gallium = [band[4]['eigenvector'][0][i][0] for i in range(3)]
    arsenic = [band[4]['eigenvector'][1][i][0] for i in range(3)]
    base2 = np.array(gallium * 256 + arsenic * 256)

    gallium = [band[5]['eigenvector'][0][i][0] for i in range(3)]
    arsenic = [band[5]['eigenvector'][1][i][0] for i in range(3)]
    base3 = np.array(gallium * 256 + arsenic * 256)

    return base1, base2, base3


if __name__ == '__main__':
    # ##################################################################################################################
    NUM_CONF_FILES = 10
    CPU = 5
    # ########################################################
    CWD = os.getcwd()
    BASE_MESH = os.path.join(CWD, 'yaml/base_mesh.yaml')
    OUTPUT = os.path.join(CWD, 'output')
    CONF_FILES = os.path.join(CWD, 'conf_files')
    # #########################################################
    print('bases')
    t0 = time.time()
    b1, b2, b3 = get_bases(BASE_MESH)
    print(f'b1, b2, b3 obtained in {time.time() - t0} seconds')

    # load mesh.yaml files
    all_paths = [f'{CONF_FILES}/{i:05}/mesh.yaml' for i in range(NUM_CONF_FILES)]

    for group in range(0, NUM_CONF_FILES, CPU):
        t0 = time.time()
        print(f'working on paths {group:05}-{group + CPU-1:05}', end='|')
        paths = all_paths[group: group + CPU]

        data = get_all_data(paths)
        frequencies = get_all_frequencies(data)
        eigenvectors = get_all_eigenvectors(data)
        normal_eigenvectors = normalize_all(eigenvectors)
        # ##############################################################################################################
        b1_list = [b1] * len(normal_eigenvectors)
        normal_b1 = normalize_all_bases(b1_list)

        zipped = zip(normal_eigenvectors, normal_b1)
        dot1 = dot_products(zipped)

        argmaxs1 = get_all_argmaxs(dot1)

        zipped = zip(frequencies, argmaxs1)
        max_frequencies = get_all_max_frequencies(zipped)

        base_file = os.path.join(OUTPUT, 'base_1.txt')
        with open(base_file, 'a') as f:
            for freq in max_frequencies:
                f.write(f'{freq}\n')
        # ##############################################################################################################
        b2_list = [b2] * len(normal_eigenvectors)
        normal_b2 = normalize_all_bases(b2_list)
        zipped = zip(normal_eigenvectors, normal_b2)
        dot2 = dot_products(zipped)
        argmaxs2 = get_all_argmaxs(dot2)
        zipped = zip(frequencies, argmaxs2)
        max_frequencies = get_all_max_frequencies(zipped)
        base_file = os.path.join(OUTPUT, 'base_2.txt')
        with open(base_file, 'a') as f:
            for freq in max_frequencies:
                f.write(f'{freq}\n')
        # ##############################################################################################################
        b3_list = [b3] * len(normal_eigenvectors)
        normal_b3 = normalize_all_bases(b3_list)
        zipped = zip(normal_eigenvectors, normal_b3)
        dot3 = dot_products(zipped)
        argmaxs3 = get_all_argmaxs(dot3)
        zipped = zip(frequencies, argmaxs3)
        max_frequencies = get_all_max_frequencies(zipped)
        base_file = os.path.join(OUTPUT, 'base_3.txt')
        with open(base_file, 'a') as f:
            for freq in max_frequencies:
                f.write(f'{freq}\n')
        # ##############################################################################################################
        print(f'done in {time.time() - t0:.0f} seconds')
