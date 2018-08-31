import pandas as pd
import fire
from reaflow.utils.tools import is_valid_file


def expression_filter(all_tpm, exp_cutoff, exp_tpm=None, filter_method='max'):
    exp_cutoff = float(exp_cutoff)
    exp_df = pd.read_table(all_tpm, index_col=0)
    if filter_method == 'max':
        exp_df = exp_df[exp_df.max(1) > exp_cutoff]
    if exp_tpm is None:
        return exp_df
    else:
        exp_df.to_csv(exp_tpm, sep='\t',
                      float_format='%.5f')


if __name__ == '__main__':
    fire.Fire()
