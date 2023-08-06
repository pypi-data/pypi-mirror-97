import numpy as np
import pandas as pd
from typing import Union, List, Optional, Sequence
from  sklearn.decomposition import PCA
from sklearn.utils import check_array, check_random_state
from .. import logging as logg
from .._settings import settings
from ..utils import AnyRandom
from ..types import CnvData

def shuffle_columns(X:np.ndarray):
    for i in range(X.shape[1]):
        np.random.shuffle(X[:,i])
    return X

def _pca(
    data: Union[CnvData, np.ndarray],
    n_comps: Optional[int] = None,
    jackstraw_perms: Optional[int] = None,
    svd_solver: str = 'arpack',
    random_state: AnyRandom = 0,
    use_highly_variable: Optional[bool] = False
) -> np.ndarray:
    if svd_solver in {'auto', 'randomized'}:
        logg.info(
            'Note that scikit-learn\'s randomized PCA might not be exactly '
            'reproducible across different computational platforms. For exact '
            'reproducibility, choose `svd_solver=\'arpack\'.`'
        )
    
    cnvdata = data if isinstance(data, CnvData) else CnvData(data)

    if use_highly_variable is True and 'highly_variable' not in cnvdata.feat.columns:
        raise ValueError(
            'Did not find cnv.feat[\'highly_variable\']. '
            'Either your data already only consists of highly-variable features '
            'or consider running `Sample.variable_features()` first.'
        )
    if use_highly_variable:
        logg.info('    on highly variable features')
    data_comp = (
        cnvdata[:, cnvdata.feat['highly_variable']] if use_highly_variable else cnvdata
    )

    if n_comps is None:
        min_dim = min(data_comp.n_feat, data_comp.n_obs)
        if settings.N_PCS >= min_dim:
            n_comps = min_dim - 1
        else:
            n_comps = settings.N_PCS

    logg.info(f'    with n_comps={n_comps}')

    random_state = check_random_state(random_state)

    X = data_comp.X
    pca_ = PCA(n_components=n_comps, svd_solver=svd_solver, random_state=random_state)
    X_pca = pca_.fit_transform(X)
    pca_components = pca_.components_
    pca_explained_variance_ratio = pca_.explained_variance_ratio_
    pca_explained_variance = pca_.explained_variance_

    
    #jackstraw
    expl_var_ratio_perm = pd.DataFrame()
    if jackstraw_perms is not None:
        n_perm = jackstraw_perms
    else:
        n_perm = settings.JS_PERMS
    for k in range(n_perm):
        perm = shuffle_columns(X)
        pca_perm = pca_.fit_transform(perm)
        expl_var_ratio_df = pd.DataFrame(data=pca_.explained_variance_ratio_.reshape(-1, len(pca_.explained_variance_ratio_)))
        expl_var_ratio_perm = expl_var_ratio_perm.append(expl_var_ratio_df)

    mean_expl_var_ratio_perm = expl_var_ratio_df.mean().values


    return (X_pca, pca_components, pca_explained_variance_ratio, pca_explained_variance, mean_expl_var_ratio_perm)
