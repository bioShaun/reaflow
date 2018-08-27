import fire
import pandas as pd
from pandas import DataFrame


CUTOFF = 0.05


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


def cal_circ_host_portion(circ_exp_matrix, group_inf, circ_host,
                          gene_type, gene_group_exp,
                          outfile):
    circ_df = pd.read_table(circ_exp_matrix)
    m_circ_df = circ_df.melt(id_vars='Gene_id', value_name='circ_count',
                             var_name='sample_id')
    m_circ_df = m_circ_df[m_circ_df.circ_count > CUTOFF]
    group_df = pd.read_table(group_inf, header=None,
                             names=['group_id', 'sample_id'])
    m_circ_df = m_circ_df.merge(group_df)
    mg_circ_df = m_circ_df.groupby(['Gene_id', 'group_id']).size()
    mg_circ_df.name = 'circ_number'
    mg_circ_df = mg_circ_df.reset_index()
    host_gene_df = pd.read_table(circ_host)
    host_gene_df.columns = ['circ_host', 'Gene_id']
    mg_circ_df = mg_circ_df.merge(host_gene_df)
    mg_host_df = mg_circ_df.loc[
        :, ['group_id', 'circ_host']].drop_duplicates()
    gene_type_df = pd.read_table(gene_type)
    mg_host_df = mg_host_df.merge(gene_type_df,
                                  left_on=['circ_host'],
                                  right_on=['gene_id'])
    mg_host_count = mg_host_df.groupby(
        ['group_id', 'gene_biotype']).size()
    mg_host_count.name = 'host_number'
    mg_host_count = mg_host_count.reset_index()
    linear_exp_genes = pd.read_table(gene_group_exp)
    mg_host_count = mg_host_count.merge(linear_exp_genes,
                                        left_on=['group_id', 'gene_biotype'],
                                        right_on=['tissue', 'gene_biotype'])
    mg_host_count.loc[:, 'host_portion'] = mg_host_count.host_number / \
        mg_host_count.detected_number
    mg_host_count.to_csv(outfile, sep='\t', index=False)


if __name__ == '__main__':
    fire.Fire()
