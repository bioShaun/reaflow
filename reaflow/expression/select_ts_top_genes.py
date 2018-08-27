import fire
import pandas as pd


def select_top(ts_bin_file, outfile):
    ts_df = pd.read_table(ts_bin_file, header=None,
                          names=['chrom', 'start',
                                 'end', 'ts', 'gene'])
    ts_df = ts_df.sort_values('ts', ascending=False)
    top_genes = ts_df.groupby(['chrom', 'start', 'end'])['gene'].head(1)
    top_gene_df = ts_df.loc[ts_df.gene.isin(top_genes)]
    top_gene_df = top_gene_df.sort_values(['chrom', 'start', 'end'])
    top_gene_df = top_gene_df[~top_gene_df.gene.duplicated()]
    top_gene_df.to_csv(outfile, header=None,
                       index=False, sep='\t',
                       columns=['chrom', 'start',
                                'end', 'gene'])


if __name__ == '__main__':
    fire.Fire(select_top)
