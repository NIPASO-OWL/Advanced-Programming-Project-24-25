import pandas as pd
from Bio import SeqIO
from Bio import Align
from Bio.SeqUtils import gc_fraction
from Bio.SeqUtils import nt_search



def process_file(file_path):
    in_file = SeqIO.parse(file_path, "fasta")
    seq_ID = []
    seq_description = []
    sequence = []
    GC_content = []
    length = []
    #calculating GC and length
    for record in in_file:
        seq_ID.append(record.id)
        seq_description.append(record.description)
        sequence.append(str(record.seq))
        GC_content.append(gc_fraction(record.seq) * 100)
        length.append(len(record.seq))
    # creating pandas dataframe including GC and length
    df = pd.DataFrame({
        'Sequence_ID': seq_ID,
        'Sequence': sequence,
        'GC_Content': GC_content,
        'Sequence_Length': length,
        'Description': seq_description,
    })
    return df

def motif_search(motif, dat):
    occurrence = []
    search = []
    for seq in dat['Sequence']:
        result = nt_search(seq, motif)
        search.append(result)
        occurrence.append(len(result)-1)
    #creating motif data frame
    motif_frame = pd.DataFrame({
        'Seq_ID': dat['Sequence_ID'],
        'Location': search,
        'Occurrences': occurrence
    })
    return motif_frame

def align_sequences(ID1, ID2, dat):
    seq1 = dat.loc[dat['Sequence_ID'] == ID1, 'Sequence'].values[0]
    seq2 = dat.loc[dat['Sequence_ID'] == ID2, 'Sequence'].values[0]
    aligner = Align.PairwiseAligner()
    alignments = aligner.align(seq1, seq2)
    best = alignments[0]
    return best, best.score