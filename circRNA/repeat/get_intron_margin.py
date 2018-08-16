import fire
import pandas as pd


VAL_MAP = {
    '+': 1,
    '-': -1,
    'up': 1,
    'down': -1
}


def intron_margin(intron_bed, outfile, margin_dis=500):
    intron_df = pd.read_table(intron_bed, header=None,
                              names=['chrom', 'start', 'end',
                                     'circ_id', 'score', 'strand',
                                     'direction'])

    def ext_margin_flag(strand, direction):
        return VAL_MAP[strand] * VAL_MAP[direction]

    intron_df.loc[:, 'margin_flag'] = list(map(ext_margin_flag,
                                               intron_df.strand,
                                               intron_df.direction))

    def to_margin(start, end, margin_flag,
                  is_start=True, margin_dis=margin_dis):
        if is_start:
            if margin_flag == -1:
                return start
            else:
                return max(end - margin_dis, start)
        else:
            if margin_flag == -1:
                return min(start + margin_dis, end)
            else:
                return end

    intron_df.loc[:, 'new_start'] = list(map(to_margin,
                                             intron_df.start,
                                             intron_df.end,
                                             intron_df.margin_flag,
                                             [True] * len(intron_df)))
    intron_df.loc[:, 'new_end'] = list(map(to_margin,
                                           intron_df.start,
                                           intron_df.end,
                                           intron_df.margin_flag,
                                           [False] * len(intron_df)))

    intron_df.to_csv(outfile, sep='\t', index=False, header=False,
                     columns=['chrom', 'new_start', 'new_end',
                              'circ_id', 'score', 'strand',
                              'direction'])


if __name__ == '__main__':
    fire.Fire(intron_margin)
