import fire
import configparser
import pandas as pd
import sys


CUTOFF = (0.1, 0.2, 0.5, 1)
TYPE = ('lncRNA', 'protein_coding', 'TUCP', 'circRNA', 'miRNA')

gene_exp = sys.argv[1]
gene_type = sys.argv[2]
tissue = sys.argv[3]
cutoff = float(sys.argv[4])
prefix = sys.argv[5]


def cal_grp_exp_gene(exp_table, gene_type, grp_inf, cutoff):
    gene_exp_df = pd.read_table(gene_exp, index_col=0)
    gene_type_df = pd.read_table(gene_type, index_col=0)
    gene_type_df = pd.DataFrame(gene_type_df.loc[:, 'gene_biotype'])
    genes_in_type = [each in TYPE for each in gene_type_df.gene_biotype]
    gene_type_df = gene_type_df[genes_in_type]
    tissue_df = pd.read_table(tissue, index_col=1, header=None)
    tissue_df.columns = ['tissue']
    overall_df = pd.DataFrame(gene_exp_df.T.max())

    def detected_genes(overall_df, gene_type_df, cutoff, tissue=None):
        overall_cut = overall_df > cutoff
        overall_cut.columns = ['detected_number']
        overall_cut_type = pd.merge(overall_cut, gene_type_df,
                                    left_index=True, right_index=True,
                                    how='right')
        overall_cut_count = pd.DataFrame(
            overall_cut_type.groupby(['gene_biotype']).sum())
        overall_cut_count.loc[:,
                              'all'] = gene_type_df.gene_biotype.value_counts()
        overall_cut_count.loc[:, 'undetected_number'] = (
            overall_cut_count.loc[:, 'all'] -
            overall_cut_count.loc[:, 'detected_number'])
        overall_cut_count.loc[:, 'detect_rate'] = (
            overall_cut_count.loc[:, 'detected_number'] /
            overall_cut_count.loc[:, 'all']
        )
        overall_cut_count.loc[:, 'cutoff'] = cutoff
        if tissue:
            overall_cut_count.loc[:, 'tissue'] = tissue
        return overall_cut_count

    detect_list = []
    detect_list.append(detected_genes(overall_df, gene_type_df, cutoff))
    merged_df = pd.concat(detect_list)
    merged_df.to_csv('{pref}.detected_genes.all_samples.txt'.format(pref=prefix),
                     sep='\t')

    tissue_gene_exp_df = pd.merge(
        gene_exp_df.T, tissue_df,
        left_index=True, right_index=True,
        how='left')
    tissue_max_df = tissue_gene_exp_df.groupby(['tissue']).max().T
    exp_tissue_df = tissue_max_df > 1
    gt_exp_tissue_df = pd.merge(exp_tissue_df, gene_type_df,
                                left_index=True, right_index=True,
                                how='left')
    sort_gt_exp_tissue_df = gt_exp_tissue_df.sort_values(by=['gene_biotype'])
    sort_gt_exp_tissue_df.index.name = 'Gene_id'
    sort_gt_exp_tissue_df.to_csv('{pref}.expressed.genes.by.tissue.txt'.format(pref=prefix),
                                 sep='\t')

    tissue_detect_list = []
    for each_t in tissue_max_df.columns:
        each_tissue_df = pd.DataFrame(tissue_max_df.loc[:, each_t])
        tissue_detect_list.append(detected_genes(
            each_tissue_df, gene_type_df, cutoff, each_t))
    tissue_merged_df = pd.concat(tissue_detect_list)
    tissue_merged_df.to_csv('{pref}.tissue.detected_genes.all_samples.txt'.format(pref=prefix),
                            sep='\t')
