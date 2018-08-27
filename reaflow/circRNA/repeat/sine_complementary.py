import fire
import pandas as pd
from pandas import DataFrame
from pathlib import Path


REPEAT_OVERLAP_HEADER = [
    'chrom1',
    'start1',
    'end1',
    'circ_id',
    'score1',
    'strand1',
    'direction',
    'chrom2',
    'start2',
    'end2',
    'repeat_name',
    'score2',
    'strand2',
    'repeat_class',
    'repeat_type',
    'overlap_len'
]


TARGET_REPEAT = 'Type I Transposons/SINE'


def sine_comp_analysis(intron_margin_repeat,
                       intron_reverse_repeat,
                       circ_catogery, out_dir):
    intron_margin_df = pd.read_table(intron_margin_repeat,
                                     header=None, names=REPEAT_OVERLAP_HEADER)
    sine_intron_margin_df = intron_margin_df[
        intron_margin_df.repeat_type == TARGET_REPEAT]
    intron_reverse_df = pd.read_table(intron_reverse_repeat,
                                      header=None, names=REPEAT_OVERLAP_HEADER)
    IR_df = sine_intron_margin_df.merge(intron_reverse_df,
                                        left_on=['circ_id', 'repeat_type'],
                                        right_on=['circ_id', 'repeat_type'],
                                        how='left')
    within_IR_mask = IR_df.direction_x == IR_df.direction_y
    within_IR_df = IR_df.loc[within_IR_mask]
    sine_circs = sine_intron_margin_df.circ_id.unique()
    sine_circ_df = DataFrame(index=sine_circs)
    sine_circ_df.loc[:, 'comp'] = 'non-complementary'
    within_IR_circs = within_IR_df.circ_id.unique()
    sine_circ_df.loc[within_IR_circs, 'comp'] = 'complementary'
    circ_catogery_df = pd.read_table(circ_catogery, index_col=0)
    sine_circ_df = sine_circ_df.merge(circ_catogery_df,
                                      left_index=True,
                                      right_index=True)
    sine_circ_count_df = sine_circ_df.groupby(['comp', 'cat']).size()
    sine_circ_count_df = (sine_circ_count_df.unstack(1) /
                          circ_catogery_df.cat.value_counts()).stack()
    sine_circ_count_df = DataFrame(sine_circ_count_df).reset_index()
    sine_circ_count_df.columns = ['comp', 'cat', 'portion']
    out_dir = Path(out_dir)
    if not out_dir.exists():
        out_dir.mkdir()
    sine_circ_count_file = out_dir / 'intron.complementary.sine.txt'
    sine_circ_count_df.to_csv(sine_circ_count_file, sep='\t', index=False)

    def repeat_dis(start1, end1, start2, end2):
        return max(start1 - end2, start2 - end1, 0)

    within_IR_df.loc[:, 'sine_distance'] = list(map(within_IR_df.start2_x,
                                                    within_IR_df.end2_x,
                                                    within_IR_df.start2_y,
                                                    within_IR_df.end2_y))


if __name__ == '__main__':
    fire.Fire()
