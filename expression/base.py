import pandas as pd


def expression_filter(exp_table, cutoff, outfile=None, method='max'):
    exp_df = pd.read_table(exp_table, index_col=0)
    if method == 'max':
        exp_df = exp_df[exp_df.max(1) > cutoff]
    if outfile is None:
        return exp_df
    else:
        exp_df.to_csv(outfile, sep='\t',
                      float_format='%.5f')
