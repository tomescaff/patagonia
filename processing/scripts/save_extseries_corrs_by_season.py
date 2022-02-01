from save_piseries_indices_corrs_by_season import *

runs = [
    ['z300-drake', 'mb', 'corr_seas_z300drake_mb'],
    ['enso-ep', 'z300-drake', 'corr_seas_ensoep_z300drake'],
    ['sst-pat', 'tas', 'corr_seas_sstpat_tas'],
    ['t850-drake', 'tas', 'corr_seas_t850drake_tas'],
    ['t850-drake', 'sst-pat', 'corr_seas_t850drake_sstpat'],
    ['enso-ep', 'sst-pat', 'corr_seas_ensoep_sstpat'],
    ['enso-ep', 'asl-mean', 'corr_seas_ensoep_aslmean'],
    ['u850-pat', 'mb', 'corr_seas_u850pat_mb'],
    ['z300-drake', 'u850-pat', 'corr_seas_z300drake_u850pat'],
    ['u850-pat', 'sst-pat', 'corr_seas_u850pat_sstpat'],
    ['sam', 'sst-pat', 'corr_seas_sam_sstpat'],
    ['asl-mean', 'mb', 'corr_seas_aslmean_mb'],
    ['sam', 'asl-mean', 'corr_seas_sam_aslmean'],
]

# get series of monthly anomalies
data = prepare_series(detrend=False)

# create and save tables
for run in runs:
    save_correlation_table(data[run[0]], data[run[1]], '../data/corr_seas/'+run[2]+'_rval.md', '../data/corr_seas/'+run[2]+'_pval.md')

name= 'corr_seas_ensoep_z300drake_aslremoved'
save_correlation_table(data['enso-ep'], data['z300-drake'], '../data/corr_seas/'+name+'_rval.md', '../data/corr_seas/'+name+'_pval.md', remove_serie=data['asl-mean'])