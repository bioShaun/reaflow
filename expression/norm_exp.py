import pandas as pd
import numpy as np
import fire


def norm_exp(exp_file, outfile, prop=False):
    exp_df = pd.read_table(exp_file, index_col=0)
    log_exp_df = np.log2(exp_df + 1)
    if prop:
        log_exp_df = log_exp_df / log_exp_df.max(0)
    max_exp = log_exp_df.max().max()
    print(f'Max exp value: {max_exp}')
    log_exp_df.to_csv(outfile, sep='\t',
                      float_format='%.3f')


def miRNA_tpm(exp_file, outfile):
    exp_df = pd.read_table(exp_file, index_col=0)
    norm_df = exp_df * (10 ** 6) / exp_df.sum()
    norm_df.to_csv(outfile, sep='\t',
                   float_format='%.5f')


if __name__ == '__main__':
    fire.Fire()
