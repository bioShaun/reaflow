import fire
import pandas as pd
from pandas import DataFrame


def cal_circ_reads_portion(circ_matrix, mapping_table,
                           outfile, group_inf=None):
    circ_df = pd.read_table(circ_matrix, index_col=0)
    mapping_df = pd.read_table(mapping_table)
    sample_circ_reads_df = DataFrame(circ_df.sum()).reset_index()
    sample_circ_reads_df.columns = ['Sample', 'circ_reads']
    sample_circ_reads_df = mapping_df.merge(sample_circ_reads_df)
    if group_inf is None:
        sample_circ_reads_df.loc[
            :, 'circ_reads_portion'] = sample_circ_reads_df.circ_reads / \
            sample_circ_reads_df.total
        sample_circ_reads_df.to_csv(outfile, sep='\t', index=False)
    else:
        group_df = pd.read_table(group_inf, header=None,
                                 names=['group_id', 'Sample'])
        sample_circ_reads_df = sample_circ_reads_df.merge(group_df)
        group_circ_reads_df = sample_circ_reads_df.groupby(['group_id']).agg(
            {'circ_reads': 'sum', 'total': 'sum'}
        )
        group_circ_reads_df.loc[
            :, 'circ_reads_portion'] = group_circ_reads_df.circ_reads / \
            group_circ_reads_df.total
        group_circ_reads_df.to_csv(outfile, sep='\t')


if __name__ == '__main__':
    fire.Fire()
