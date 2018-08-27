import pandas as pd


def expression_filter(all_tpm, exp_cutoff, exp_tpm=None, method='max'):
    exp_df = pd.read_table(all_tpm, index_col=0)
    if method == 'max':
        exp_df = exp_df[exp_df.max(1) > exp_cutoff]
    if exp_tpm is None:
        return exp_df
    else:
        exp_df.to_csv(exp_tpm, sep='\t',
                      float_format='%.5f')
