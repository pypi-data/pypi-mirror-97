from parebrick.utils.data.parsers import parse_infercars_to_df
from parebrick.utils.data.stats import distance_between_blocks_distribution
from parebrick.utils.data.unique_gene_filters import filter_dataframe_unique

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import numpy as np
import pandas as pd

from matplotlib.colors import LogNorm
from matplotlib import rc

import argparse
import os


def blocks_length_dist(df):
    return [end_ - start_ for start_, end_ in zip(df['chr_beg'], df['chr_end'])]


def distance_between_blocks_distribution_2(df_blocks):
    ds = []

    change_name = {
        'GCA_002310595.1': '$\it{Escherichia}$ $\it{coli}$ $\it{C4}$',
        # 'GCA_002310595.1': r'\textit{}',
        # 'GCA_000012005.1': r'\textit{Shigella\ndysenteriae sd197}'
        'GCA_000012005.1': '$\it{Shigella}$\n$\it{dysenteriae}$ $\it{sd197}$'
    }

    for sp, df_sp in df_blocks.groupby('species'):
        if sp not in change_name.keys(): continue

        df_sp = df_sp.sort_values(by=['chr_beg'])

        print(len(df_sp['chr_beg']) - 1)
        for start_, end_ in zip(df_sp['chr_beg'][1:], df_sp['chr_end']):
            ds.append([change_name[sp], start_ - end_])

    return pd.DataFrame(ds, columns=['', 'Adjacency lengths, kb, log scale'])


def lengths_between(state):
    plt.figure()
    if state == 'after':
        df_filtered = filter_dataframe_unique(df)
        ds = distance_between_blocks_distribution_2(df_filtered)
    else:
        ds = distance_between_blocks_distribution_2(df)

    # sns.histplot(ds, bins=100, log_scale=(False), kde_kws={'alpha': 0.7})
    # sns.histplot(hue='', x='Adjacency lengths, kb, log scale', data=ds, log_scale=(True, False), bins=25, element="poly")
    sns.histplot(hue='', x='Adjacency lengths, kb, log scale', data=ds, log_scale=(True, False), bins=25, element="step")
    # sns.histplot(hue='genome', x='Length', data=ds, log_scale=(True, False), bins=25, multiple="dodge")

    # plt.ylabel('Length')
    # plt.xlabel('Strain')
    # plt.yscale('log')

    plt.tight_layout()

    plt.savefig(out_folder + f'd_lengths_between_log_x_1.svg')
    plt.show()


def makesweetgraph(x=None, y=None, cmap='jet', bins=120, snsbins=100):
    ax1 = sns.jointplot(x=x, y=y, marginal_kws=dict(bins=snsbins))

    ax1.fig.set_size_inches(6, 4)
    ax1.ax_joint.cla()
    ax1.set_axis_labels('Number of strains in which a block is present', 'Mean block length, kb')

    plt.sca(ax1.ax_joint)
    plt.hist2d(x, y, bins=(150, 120), norm=LogNorm(), cmap=sns.color_palette("Spectral_r", as_cmap=True))
    cbar_ax = ax1.fig.add_axes([0.82, 0.1, .03, .7])
    cb = plt.colorbar(cax=cbar_ax)
    cb.set_label(r'$\log_{10}$ density of points', fontsize=13)


def hex_len_genomes_count(log):
    plt.figure()
    xs = []
    ys = []
    for block, df_block in df.groupby('block'):
        xs.append(len(df_block.species.unique()))
        ys.append(np.mean(df_block.len) / 1000)

    if log: plt.yscale('log')
    # h = sns.jointplot(xs, ys, marker="+")
    # h = sns.jointplot(xs, ys, kind='kde')
    # h = sns.jointplot(x=xs, y=ys, kind='hex', joint_kws=dict(gridsize=40), palette='rocket_r')
    # h.set_axis_labels('Number of genomes', 'Length of blocks')

    makesweetgraph(xs, ys)

    # plt.xlim(xmin=0 - 0.02 * (max(xs)), xmax=max(xs) + 0.02 * (max(xs)))
    # if not log: plt.ylim(ymin=0)

    plt.tight_layout()
    plt.subplots_adjust(right=0.8)
    plt.savefig(out_folder + f'b_density_number_length{"_log" if log else ""}.svg')
    plt.show()

    # plt.subplots_adjust(left=0.14, right=0.99)

    # plt.show()


def main():
    global out_folder, df
    # rc('text', usetex=True)

    parser = argparse.ArgumentParser(
        description='Building charts for pan-genome analysis based on synteny blocks.')

    parser.add_argument('--infercars_file', '-f', required=True,
                        help='Path to file in infercars format, can be found in main script output')

    parser.add_argument('--output', '-o', default='parebrick_charts', help='Path to output folder.')

    args = parser.parse_args()
    d = vars(args)

    file, out_folder = d['infercars_file'], d['output']

    if out_folder[-1] != '/': out_folder += '/'
    os.makedirs(out_folder, exist_ok=True)

    df = parse_infercars_to_df(file)
    df['len'] = df['chr_end'] - df['chr_beg']
    sns.set(style="whitegrid", font="serif")
    # sns.set(style='white', font="serif")

    print('Plotting lengths between blocks')
    lengths_between('after')


    # print('Plotting scatter for occurrence of synteny blocks vs its length')
    # hex_len_genomes_count(False)


if __name__ == "__main__":
    main()
