import json
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

from matplotlib.pyplot import figure, close
import numpy as np

def read_json(json_path):
    with open(json_path) as j:
        data = json.load(j)
    return data


def save_json(file_path, data):
    with open(file_path, 'w') as j:
        json.dump(data, j, indent=4)


def get_percentage(file, top_n):
    data = read_json(file)
    if len(data) == 0:
        return 0, 0
    nr_1 = 0
    nr_top = 0
    for entry in data:
        if entry['place'] == 0:
            nr_1 += 1
        if -1 < entry['place'] < top_n:
            nr_top += 1
    cor_perc = nr_1 / len(data) * 100
    top_n_perc = nr_top / len(data) * 100
    print(len(data))
    return cor_perc, top_n_perc


def single_bar(x, y, out=None):
    fig, ax = plt.subplots()
    plt.bar(x, y)
    plt.ylim(0, 100)
    plt.xticks([i for i in range(nr[0], nr[-1] + 1, 5)])
    ax.yaxis.set_minor_locator(MultipleLocator(5))
    ax.set_xlabel('Fragment length')
    ax.set_ylabel('% Correct predictions')
    if out is not None:
        fig.savefig(out)
    else:
        plt.show()

def double_bar(title, x1, x2, y1, y2, out=None):
    bar_width = 0.35
    fig, ax = plt.subplots()
    print(dir(fig))
    fig.set_size_inches(10,4)
    ax.bar(x1, y1, bar_width, color='b', label='Buccaneer')
    ax.bar(np.array(x2) + bar_width, y2, bar_width, color='g', label='Strudel')
    ax.set_xlabel('Fragment length')
    ax.set_ylabel('% Correct predictions')
    ax.yaxis.set_minor_locator(MultipleLocator(5))
    ax.legend()
    plt.title(title)
    if out is not None:
        fig.savefig(out)
    else:
        plt.show()


def get_data(path):
    top_number = 10
    files = os.listdir(path)
    j_files = [f for f in files if f.endswith('.json') and not f.startswith('.')]
    try:
        j_files.sort(key=lambda z: int(z.split('_')[0]))
    except ValueError:
        j_files.sort(key=lambda z: int(z.split('.')[0]))
    nr = []
    perc = []
    first_10_perc = []
    for f in j_files:
        try:
            n = int(f.split('_')[0])
        except ValueError:
            n = int(f.split('.')[0])
        nr.append(n)
        j_path = os.path.join(path, f)
        cor_perc, top_n = get_percentage(j_path, top_number)
        perc.append(cor_perc)
        first_10_perc.append(top_n)
    return nr, perc

# j_dir = '/Volumes/data/Work/test_segm/out_6/vs_2.5-3_formated/res_jsons_1000_60'
#j_dir = '/Volumes/data/Work/test_segm/out_6/vs_2.5-3_formated/buc_jsons'
# j_dir = '/Volumes/data/Work/test_segm/out_6/vs_2.5-3_formated/jsons_blind'
# j_dir = '/Volumes/data/bucc_find_seq/results/20584'
# j_dir = '/Volumeses/data/find_seq/0711_strudel/jsons_75_74-'
# j_dir = '/Volumes/data/find_seq/untitled_folder/20584out_sd1/jsons_75'
# top_number = 10
# files = os.listdir(j_dir)
# j_files = [f for f in files if f.endswith('.json') and not f.startswith('.')]
# j_files.sort(key=lambda z: int(z.split('_')[0]))
#
# nr = []
# perc = []
# first_10_perc = []
# for f in j_files:
#     n = int(f.split('_')[0])
#     nr.append(n)
#     j_path = os.path.join(j_dir, f)
#     cor_perc, top_n = get_percentage(j_path, top_number)
#     perc.append(cor_perc)
#     first_10_perc.append(top_n)
# #
# print(nr)
# # fig = figure(num=1, figsize=(4, 4), dpi=200, facecolor='w', edgecolor='k')
# fig, ax = plt.subplots()
# plt.bar(nr, perc)
# plt.ylim(0, 100)
# plt.xticks([i for i in range(nr[0], nr[-1] + 1, 5)])
# ax.yaxis.set_minor_locator(MultipleLocator(5))

# fig.savefig("/Volumes/data/find_seq/plots/" + '20584_strudel_sd2.png')

# strud = '/Users/andrei/sequence_data/6272_strudel/res_jsons_1000'
# buc = '/Users/andrei/sequence_data/6272_buc/jsons'
# out = '/Users/andrei/sequence_data/plots_double/6272_dep.png'
#
# strud = '/Users/andrei/sequence_data/6272_strud_built_results/sd2/jsons_75'
# buc = '/Users/andrei/sequence_data/6272_buc_bui/jsons'
# out = '/Users/andrei/sequence_data/plots_double/6272_built_sd2_75.png'

# strud = '/Users/andrei/sequence_data/6272_strud_built_results/sd1/jsons_75'
# buc = '/Users/andrei/sequence_data/6272_buc_bui/jsons'
# out = '/Users/andrei/sequence_data/plots_double/6272_built_sd1_75.png'

# strud = '/Users/andrei/sequence_data/20584_strud_bui/sd1/jsons_75'
# buc = '/Users/andrei/sequence_data/20584_buc_bui/jsons'
# out = '/Users/andrei/sequence_data/plots_double/20584_built_sd1_75.png'

# strud = '/Users/andrei/sequence_data/20584_strud_bui/sd1/jsons_60'
# buc = '/Users/andrei/sequence_data/20584_buc_bui/jsons'
# out = '/Users/andrei/sequence_data/plots_double/20584_built_sd1_60.png'

strud = '/Volumes/data/find_seq/0703/strudel/0703/jsons_75'
buc = '/Volumes/data/find_seq/0703/buc/jsons'
out = '/Users/andrei/sequence_data/plots_double/0703_dep_sd1_75.png'


# st_nr, st_perc = get_data(strud)
# buc_nr, buc_perc = get_data(buc)
# print(st_nr)
# print(buc_nr)

# double_bar(buc_nr, st_nr, buc_perc, st_perc, out)


def all_plots(in_path, out_path):
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    entries = os.listdir(in_path)
    entries = [p for p in entries if p!= 'plots']
    for entry in entries:
        code, resol = entry.split('_')
        buc_path = os.path.join(in_path, entry, 'buc/jsons')
        strud_fold = os.path.join(in_path, entry, 'strudel')
        percs = os.listdir(strud_fold)
        for fldr in percs:
            aa = r"$\mathring{A}$"
            strud_path = os.path.join(strud_fold, fldr)
            title = f'Entry: {code}, resolution: {resol} {aa}'
            print(title)
            perc = fldr.split('_')[-1]
            st_nr, st_perc = get_data(strud_path)
            buc_nr, buc_perc = get_data(buc_path)
            out = os.path.join(out_path, f'{code}_{resol}_{perc}.png')
            double_bar(title, buc_nr, st_nr, buc_perc, st_perc, out)

all_in = '/Volumes/data/find_seq/all_results'
all_out = '/Volumes/data/find_seq/all_results/plots'

all_plots(all_in, all_out)