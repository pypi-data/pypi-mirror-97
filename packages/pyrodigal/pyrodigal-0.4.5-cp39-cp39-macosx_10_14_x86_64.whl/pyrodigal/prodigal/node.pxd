from pyrodigal.prodigal.bitmap cimport bitmap_t
from pyrodigal.prodigal.sequence cimport _mask
from pyrodigal.prodigal.training cimport _training


cdef extern from "node.h" nogil:

    const size_t STT_NOD = 100000
    const size_t MIN_GENE = 90
    const size_t MIN_EDGE_GENE = 60
    const size_t MAX_SAM_OVLP = 60
    const size_t ST_WINDOW = 60
    const size_t OPER_DIST = 60
    const double EDGE_BONUS = 0.74
    const double EDGE_UPS = -1.0
    const double META_PEN = 7.5

    struct _motif:
        int ndx
        int len
        int spacer
        int spacendx
        double score

    struct _node:
        int type
        int edge
        int ndx
        int strand
        int stop_val
        int star_ptr[3]
        int gc_bias
        double gc_score
        double cscore
        double gc_cont
        int rbs[2]
        _motif mot
        double uscore
        double tscore
        double rscore
        int traceb
        int tracef
        int ov_mark
        double score
        int elim

    int add_nodes(bitmap_t seq, bitmap_t rseq, int slen, _node* nodes, bint closed, _mask* mlist, int nm, _training* tinf)
    void reset_node_scores(_node*, int)
    int compare_nodes(const void*, const void*)
    int stopcmp_nodes(const void*, const void*)

    void record_overlapping_starts(_node*, int, _training*, int)
    void record_gc_bias(int*, _node*, int, _training*)

    void calc_dicodon_gene(_training*, unsigned char*, unsigned char*, int, _node*, int)
    void calc_amino_bg(_training*, unsigned char*, unsigned char*, int, _node*, int)

    void score_nodes(unsigned char*, unsigned char*, int, _node*, int, _training*, int, int)
    void rbs_score(unsigned char*, unsigned char*, int, _node *, int, _training *);

    void raw_coding_score(bitmap_t seq, bitmap_t rseq, int slen, _node *nod, int nn, _training *tinf)

    void determine_sd_usage(_training *tinf)

    void train_starts_sd(bitmap_t seq, bitmap_t rseq, int slen, _node *nodes, int nn, _training *tinf)
    void train_starts_nonsd(bitmap_t seq, bitmap_t rseq, int slen, _node *nodes, int nn, _training *tinf)

    int cross_mask(int, int, _mask*, int)
