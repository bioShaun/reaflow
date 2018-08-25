import pandas as pd
from pandas import DataFrame
import fire
from pathlib import Path
import numpy as np


def exp_summary_group_num(exp_table, group_inf, exp_cutoff,
                          out_dir, prefix):
    exp_df = pd.read_table(exp_table)
    m_exp_df = exp_df.melt(id_vars='Gene_id',
                           value_name='circ_count',
                           var_name='sample_id')
    m_exp_df = m_exp_df[m_exp_df.circ_count > exp_cutoff]
    group_df = pd.read_table(group_inf,
                             header=None,
                             names=['group_id', 'sample_id'])
    m_exp_df = m_exp_df.merge(group_df)
    g_exp_df = m_exp_df.loc[:, ['Gene_id', 'group_id']].drop_duplicates()
    gene_summary1 = g_exp_df.Gene_id.value_counts()
    tmp_gene_summary2 = g_exp_df.groupby(['Gene_id'])['group_id'].unique()
    gene_summary2 = tmp_gene_summary2.map(','.join)
    gene_summary1.name = 'group_count'
    gene_summary2.name = 'group_name'
    gene_summary = pd.concat([gene_summary1, gene_summary2],
                             axis=1, sort=True)
    group_summary1 = g_exp_df.group_id.value_counts()
    solo_exp_genes = gene_summary1[gene_summary1 == 1].index
    solo_exp_df = m_exp_df[m_exp_df.Gene_id.isin(solo_exp_genes)]
    group_summary2 = solo_exp_df.group_id.value_counts()
    group_summary1.name = 'exp'
    group_summary2.name = 'exclusive_exp'
    group_summary = pd.concat([group_summary1, group_summary2],
                              axis=1, sort=True)
    group_summary.loc[:, 'exp_portion'] = group_summary.exp / \
        len(gene_summary)
    group_summary.loc[
        :, 'exclusive_exp_portion'] = group_summary.exclusive_exp / \
        len(gene_summary)
    out_dir = Path(out_dir)
    if not out_dir.exists():
        out_dir.mkdir()
    gene_summary_file = out_dir / f'{prefix}.gene.exp.summary.txt'
    gene_summary.index.name = 'gene_id'
    gene_summary.to_csv(gene_summary_file, sep='\t')
    group_summary_file = out_dir / f'{prefix}.group.exp.summary.txt'
    group_summary.index.name = 'group_id'
    group_summary.loc['Total'] = [len(gene_summary),
                                  group_summary.exclusive_exp.sum(),
                                  1,
                                  group_summary.exclusive_exp_portion.sum()]
    group_summary.to_csv(group_summary_file, sep='\t',
                         na_rep=0)
    group_num = len(group_df.group_id.unique())
    gene_num_p = gene_summary1 / group_num
    gene_num_dis = pd.cut(
        gene_num_p,
        np.arange(0, 1.2, 0.2),
        labels=np.arange(
            0, 1, 0.2)).value_counts().sort_index()
    gene_num_dis = DataFrame(gene_num_dis)
    gene_num_dis.index.name = 'group_portion'
    gene_num_dis.columns = ['gene_number']
    gene_num_dis = gene_num_dis.reset_index()
    gene_num_dis.loc[:, 'group_portion'] = gene_num_dis.group_portion.round(1)
    gene_num_dis.loc[:, 'gene_portion'] = gene_num_dis.gene_number / \
        gene_num_dis.gene_number.sum()
    gene_num_dis_file = out_dir / f'{prefix}.gene_number.distribution.txt'
    gene_num_dis.to_csv(gene_num_dis_file, sep='\t',
                        index=False)


def top_gene_classify(top_gene, gene_ts_type, gene_biotype, outfile):
    top_gene_df = pd.read_table(top_gene)
    gene_type_df = pd.read_table(gene_biotype)
    gene_ts_df = pd.read_table(gene_ts_type,
                               header=None,
                               names=['Gene_id', 'ts_type'])
    top_gene_df = top_gene_df.merge(gene_ts_df)
    top_gene_df = top_gene_df.merge(gene_type_df,
                                    left_on='Gene_id',
                                    right_on='gene_id')
    top_gene_type_df = top_gene_df.groupby(
        ['Group', 'gene_biotype', 'ts_type']).size().unstack(fill_value=0)
    top_gene_count_df = top_gene_df.groupby(['Group', 'gene_biotype']).size()
    top_gene_type_port_df = top_gene_type_df.div(top_gene_count_df, axis=0)
    top_gene_type_port_df.columns = [f'{each}_portion' for each in
                                     top_gene_type_port_df.columns]
    top_gene_type_port_df = pd.concat([top_gene_type_df,
                                       top_gene_type_port_df],
                                      axis=1)
    top_gene_type_port_df.to_csv(outfile, sep='\t', float_format='%.3f')


if __name__ == '__main__':
    fire.Fire()
