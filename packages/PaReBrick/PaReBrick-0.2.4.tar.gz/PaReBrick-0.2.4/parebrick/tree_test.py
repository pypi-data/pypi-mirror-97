import sys
from ete3 import Tree, SeqMotifFace, TreeStyle, add_face_to_node

seq = ("-----------------------------------------------AQAK---IKGSKKAIKVFSSA---"
       "APERLQEYGSIFTDA---GLQRRPRHRIQSK-------ALQEKLKDFPVCVSTKPEPEDDAEEGLGGLPSN"
       "ISSVSSLLLFNTTENLYKKYVFLDPLAG----THVMLGAETEEKLFDAPLSISKREQLEQQVPENYFYVPD"
       "LGQVPEIDVPSYLPDLPGIANDLMYIADLGPGIAPSAPGTIPELPTFHTEVAEPLKVGELGSGMGAGPGTP"
       "AHTPSSLDTPHFVFQTYKMGAPPLPPSTAAPVGQGARQDDSSSSASPSVQGAPREVVDPSGGWATLLESIR"
       "QAGGIGKAKLRSMKERKLEKQQQKEQEQVRATSQGGHL--MSDLFNKLVMRRKGISGKGPGAGDGPGGAFA"
       "RVSDSIPPLPPPQQPQAEDED----")

mixed_motifs = [
    # seq.start, seq.end, shape, width, height, fgcolor, bgcolor
    [10, 100, "[]", None, 10, "black", "rgradient:blue", "arial|8|white|long text clipped long text clipped"],
    [101, 150, "o", None, 10, "blue", "pink", None],
    [155, 180, "()", None, 10, "blue", "rgradient:purple", None],
    [160, 190, "^", None, 14, "black", "yellow", None],
    [191, 200, "<>", None, 12, "black", "rgradient:orange", None],
    [201, 250, "o", None, 12, "black", "brown", None],
    [351, 370, "v", None, 15, "black", "rgradient:gold", None],
    [370, 420, "compactseq", 2, 10, None, None, None],
]

simple_motifs1 = [
    # seq.start, seq.end, shape, width, height, fgcolor, bgcolor
    [0, 30,   "[]", None, 10, 'blue', "blue", "arial|2|white|+1024"],
    [30, 40,   ">", None, 10, "blue", "blue", None],

    [50, 80, "[]", None, 10, 'grey', "grey", "arial|2|white|+n"],
    [80, 90, ">", None, 10, "grey", "grey", None],

    [100, 110, "<", None, 10, "red", "red", None],
    [110, 140, "[]", None, 10, 'red', "red", "arial|2|white|-1025"]
]

simple_motifs2 = [
    # seq.start, seq.end, shape, width, height, fgcolor, bgcolor
    [0, 30,   "[]", None, 10, 'blue', "blue", "arial|2|white|+1024"],
    [30, 40,  ">", None, 10, "blue", "blue", None],

    [50, 80,  "[]", None, 10, 'grey', "grey", "arial|2|white|+n"],
    [80, 90,  ">", None, 10, "grey", "grey", None],

    [100, 110, "<", None, 10, "red", "red", None],
    [110, 140, "[]", None, 10, 'red', "red", "arial|2|white|-1025"],
]

simple_motifs3 = [
    # seq.start, seq.end, shape, width, height, fgcolor, bgcolor
    [0, 30,   "[]", None, 10, 'blue', "blue", "arial|2|white|+1024"],
    [30, 40,  ">", None, 10, "blue", "blue", None],

    [50, 80,  "[]", None, 10, 'grey', "grey", "arial|2|white|+n"],
    [80, 90,  ">", None, 10, "grey", "grey", None],

    [100, 110, "<", None, 10, "red", "red", None],
    [110, 140, "[]", None, 10, 'red', "red", "arial|2|white|-1025"],

    [140, 200, "blank", None, 10, None, None, None],

    [200, 230, "[]", None, 10, 'green', "green", "arial|2|white|+1026"],
    [230, 240, ">", None, 10, "green", "green", None],

    [250, 280, "[]", None, 10, 'grey', "grey", "arial|2|white|+n"],
    [280, 290, ">", None, 10, "grey", "grey", None],

    [300, 310, "<", None, 10, "purple", "purple", None],
    [310, 340, "[]", None, 10, 'purple', "purple", "arial|2|white|-1023"],
]

simple_motifs4 = [
    # seq.start, seq.end, shape, width, height, fgcolor, bgcolor
    [0, 30,   "[]", None, 10, 'blue', "blue", "arial|2|white|+1024"],
    [30, 40,  ">", None, 10, "blue", "blue", None],

    [50, 80,  "[]", None, 10, 'grey', "grey", "arial|2|white|+n"],
    [80, 90,  ">", None, 10, "grey", "grey", None],

    [100, 110, "<", None, 10, "green", "green", None],
    [110, 140, "[]", None, 10, 'green', "green", "arial|2|white|-1026"],

    [140, 200, "blank", None, 10, None, None, None],

    [200, 230, "[]", None, 10, 'red', "red", "arial|2|white|+1025"],
    [230, 240, ">", None, 10, "red", "red", None],

    [250, 280, "[]", None, 10, 'grey', "grey", "arial|2|white|+n"],
    [280, 290, ">", None, 10, "grey", "grey", None],

    [300, 310, "<", None, 10, "purple", "purple", None],
    [310, 340, "[]", None, 10, 'purple', "purple", "arial|2|white|-1023"],
]

box_motifs = [
    # seq.start, seq.end, shape, width, height, fgcolor, bgcolor
    [0, 5, "[]", None, 10, "black", "rgradient:blue", "arial|8|white|10"],
    [10, 25, "[]", None, 10, "black", "rgradient:ref", "arial|8|white|10"],
    [30, 45, "[]", None, 10, "black", "rgradient:orange", "arial|8|white|20"],
    [50, 65, "[]", None, 10, "black", "rgradient:pink", "arial|8|white|20"],
    [70, 85, "[]", None, 10, "black", "rgradient:green", "arial|8|white|20"],
    [90, 105, "[]", None, 10, "black", "rgradient:brown", "arial|8|white|20"],
    [110, 125, "[]", None, 10, "black", "rgradient:yellow", "arial|8|white|20"],
]


def get_example_tree():
    # Create a random tree and add to each leaf a random set of motifs
    # from the original set

    t = Tree("( (A, B, C, D, E, F, G), H, I);")

    seqFace = SeqMotifFace('', motifs=simple_motifs1)
    (t & "A").add_face(seqFace, 0, "aligned")

    seqFace = SeqMotifFace('', motifs=simple_motifs2)
    (t & "B").add_face(seqFace, 0, "aligned")

    seqFace = SeqMotifFace('', motifs=simple_motifs3)
    (t & "C").add_face(seqFace, 0, "aligned")
    (t & "C").img_style['bgcolor'] = 'Gainsboro'

    seqFace = SeqMotifFace('', motifs=simple_motifs4)
    (t & "D").add_face(seqFace, 0, "aligned")
    (t & "D").img_style['bgcolor'] = 'Gainsboro'

    seqFace = SeqMotifFace('', motifs=simple_motifs4)
    (t & "E").add_face(seqFace, 0, "aligned")
    (t & "E").img_style['bgcolor'] = 'Gainsboro'

    seqFace = SeqMotifFace('', motifs=simple_motifs3)
    (t & "F").add_face(seqFace, 0, "aligned")
    (t & "F").img_style['bgcolor'] = 'Gainsboro'

    seqFace = SeqMotifFace('', motifs=simple_motifs3)
    (t & "H").add_face(seqFace, 0, "aligned")
    (t & "H").img_style['bgcolor'] = 'Gainsboro'

    (t & "G").img_style['bgcolor'] = 'LightGreen'
    (t & "I").img_style['bgcolor'] = 'LightGreen'

    return t


if __name__ == '__main__':
    mode = 'r'
    t = get_example_tree()
    ts = TreeStyle()
    ts.mode = mode
    ts.scale = None
    # t.show(tree_style=ts)
    t.render(f"seq_motif_faces_{mode}.pdf", tree_style=ts)