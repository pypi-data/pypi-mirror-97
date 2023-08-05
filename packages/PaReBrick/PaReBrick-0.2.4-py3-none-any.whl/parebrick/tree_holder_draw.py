from parebrick.tree.tree_holder import TreeHolder

import logging
from collections import defaultdict
from ete3 import Tree


BALANCED_COLORS = ['White', 'LightBlue', 'LightGreen', 'LightPink', 'LightGreen', 'Peru', 'NavajoWhite', 'LightPink',
                   'LightCoral', 'Purple', 'Navy', 'Olive', 'Teal', 'SaddleBrown', 'SeaGreen', 'DarkCyan',
                   'DarkOliveGreen', 'DarkSeaGreen']

if __name__ == '__main__':
    # th = TreeHolder('((Strain 1:1,Strain 2:1):2,((Strain 3:1,Strain 4:1),Strain 5:2):1);', logging.getLogger(), scale=100)
    # th = TreeHolder('(((((Strain 1,Strain 2),Strain 3:2), (Strain 4:2,Strain 5:2)), (Strain 6,Strain 7):3), ((Strain 8:1,Strain 9:1),Strain 10:2):3);', logging.getLogger(), scale=42)
    th = TreeHolder('(((((Strain 1:0.15,Strain 2:0.1):0.15,Strain 3:0.22):0.1, (Strain 4:0.2,Strain 5:0.25):0.1):0.15, (Strain 6:0.1,Strain 7:0.15):0.15):0.15, ((Strain 8:0.1,Strain 9:0.15):0.1,Strain 10:0.35):0.1);', logging.getLogger(), scale=500)

    th.count_innovations_fitch({
        'Strain 1': 2,
        'Strain 2': 0,
        'Strain 3': 1,
        'Strain 4': 0,
        'Strain 5': 2,
        'Strain 6': 0,
        'Strain 7': 2,
        'Strain 8': 1,
        'Strain 9': 1,
        'Strain 10': 0,
    })

    # th.count_innovations_fitch({
    #     'Strain 1': 2,
    #     'Strain 2': 2,
    #     'Strain 3': 2,
    #     'Strain 4': 0,
    #     'Strain 5': 0,
    #     'Strain 6': 0,
    #     'Strain 7': 0,
    #     'Strain 8': 0,
    #     'Strain 9': 0,
    #     'Strain 10': 0,
    # })

    # th.count_innovations_fitch(defaultdict(lambda: 1))
    th.draw('pic6.pdf', BALANCED_COLORS, show_branch_support=False, show_scale=True, color_internal_nodes=True, mode='r')
    # th.draw('pic-pres2.svg', BALANCED_COLORS, show_branch_support=False, show_scale=False, color_internal_nodes=True, mode='c')
    # th.draw('pic4.pdf', BALANCED_COLORS, show_branch_support=False, show_scale=False, color_internal_nodes=True, mode='c')
