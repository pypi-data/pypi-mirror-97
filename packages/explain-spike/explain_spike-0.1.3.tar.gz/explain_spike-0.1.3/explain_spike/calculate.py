## Imports para las librerias

from pandas.core import frame
import shap
import dalex as dx
import numpy as np
import pandas as pd
    
def init_explainer(model, data_x: frame, exp_type: str = 'shap', log_loss: bool = False, verbose: bool = False):

    """ Construye los objetos de explainer para las librerias de SHAP o DALEX, 
        estos se ocupan más adelante tanto para realizar calculos como crear graficos
    Arg: 
        model: Modelo del tipo Tree
        data_x: Datos que se ajusten a la entrada del modelo
        exp_type: Tipo de explainer a contruir, {'shap', 'dalex'}
        log_loss: Para decidir si calcular los SHAP values de la contribucion a la salida del modelo (False) o al error de clasificacion (True)
    Returns:
        Objeto explainer del tipo especificado
    """

    if exp_type=='shap':
        if log_loss:
            return  shap.TreeExplainer(model, data_x, model_output='log_loss')
        else:
            return shap.TreeExplainer(model, data_x)
    elif exp_type=='dalex':
        return dx.Explainer(model, data_x, model.predict(data_x), verbose=verbose)
    else:
        raise ValueError('exp_type="shap" or exp_type="dalex"')

def get_shap_values(model, data_x: frame, data_y = None, log_loss: bool = False,
                    check_additivity: bool = False):

    """ Para obtener los valores SHAP de los datos entregados en los argumentos segun el modelo del explainer
    Arg: 
        model: Modelo del tipo Tree
        data_x: Datos sobre los cuales calcular los SHAP values
        data_y: Datos de la salida esperada para data_x, necesario si el explainer es para la contribucion al log_loss
        check_additivity: Si correr o no un chequeo de si la suma de los SHAP values es igual a la salida del modelo
    Returns:
        Objeto explainer de los shap values
    """
    explainer = init_explainer(model, data_x, exp_type='shap', log_loss=log_loss)

    if type(data_y)!=type(None) and log_loss:
        return explainer(data_x, data_y, check_additivity=check_additivity)
    else:
        return explainer(data_x, check_additivity=check_additivity)

#### Explicacion Global

def shap_importance(features: list, shap_values, n: int = 10):

    """ Se obtienen los n features más importantes del modelo segun los SHAP values junto a sus valores (mean(|shap_value|))
    Arg: 
        features: lista con las variables de los datos del modelo (con el mismo orden con los que se calculo los SHAP values) 
        shap_values: Objeto explainer de los shap values
        n: Top n caracteristicas más importantes
    Returns:
        Tupla de una lista con las n variables más importantes y sus valores
    """
    if n>len(features): n=len(features)
    features = pd.Index(features)
    if len(np.array(shap_values.values).shape) == 2: #cuando el problema es de regresion
        abs_sum_shap = np.mean(np.abs(shap_values.values), axis=0)
    else:
        abs_sum_shap = np.mean(np.sum(np.abs(np.array(shap_values.values)),axis=0), axis=0) #cuando es clasificacion y hay shap values por clase
    top_features = list(features[abs_sum_shap.argsort()[-n:][::-1]].values)
    top_shap_values =  abs_sum_shap[abs_sum_shap.argsort()[-n:][::-1]]
    return top_features, top_shap_values

def permutation_importance(model, data_x: frame, n: int = 10, B: int = 15):
    
    """ Se obtienen los n features más importantes del modelo segun el Permutation Variable Importance
    Arg:
        model: Modelo del tipo Tree
        data_x: Datos sobre los cuales calcular los SHAP values
        n: Top n caracteristicas más importantes que se quieren
        B: Numero de rondas por las que se calcula el permutation importance
    Returns:
        Tupla de una lista con las n variables más importantes y sus valores
    """
    dalex_exp = init_explainer(model, data_x, exp_type='dalex', verbose=False)
    vi = dalex_exp.model_parts(B=B, random_state=0)
    results_vi = vi.result
    results_vi.sort_values(by=[results_vi.columns[1]], ascending=False, inplace=True)
    if n>len(data_x.columns): n=len(data_x.columns)
    top_features = list(results_vi.iloc[1:-1,0].values)[:n]
    top_values = list(results_vi.iloc[1:-1,1].values)[:n]
    return top_features, top_values

def percentiles(data: frame, y: str):

    """ Se calculan las instancias de los percentiles del frame segun la variable y (percentiles 0 y 99 junto con los deciles 10-90)
    Arg:
        data: Datos sobre los cuales calcular los percentiles
        y: Nombre de la variable sobre la cual obtener los percentiles
    Returns:
        Diccionario con los percentiles en las llaves y en sus valores las instancias representantes a su respectivo percentil
    """
    data_pred = data.copy()
    data_pred.sort_values(y, inplace=True)
    data_pred.reset_index(inplace=True)
    percentiles_dict = {}
    percentiles_dict[0] = data_pred.loc[0, 'index']
    inc = data_pred.shape[0]//10
    for i in range(1, 10):
        percentiles_dict[i * 10] = data_pred.loc[i * inc,  'index']
    percentiles_dict[99] = data_pred.loc[data_pred.shape[0]-1, 'index']
    return percentiles_dict

def partial_dependence(feature: str, frame: frame, model, resolution: int = 20, bins = None , missing: bool = True, round_=True):

    """ Calcula los partial dependence para la variable especificada en feature
    Arg:
        feature: variable del frame sobre el cual realizar los calculos
        frame: data de entrada del modelo
        model: modelo entrenado con el cual calcular el partial dependence
        resolution: numero de puntos en los que calcular el partial dependence (si bins=None)
        bins: valores en los que calcular el partial dependence
        missing: si incluir un valor faltante (Nan) en los bins
    Returns:
        Un frame con los valores de partial dependence calculados sobre la variable en features
    """
    
    pd.options.mode.chained_assignment = None
    col_cache = frame.loc[:, feature].copy(deep=True)
    if type(bins) == type(None):
        (min_, max_) = (frame[feature].min(), frame[feature].max())
        by = (max_ - min_)/resolution
        bins = np.arange(min_, (max_ + by), (by + np.round((1. / resolution) * by, 3)))
        if round_:
            n=0
            for valor in frame[feature].astype('float').values:
                _, decimals = str(valor).split('.')
                if len(decimals)>n: n=len(decimals)
            bins = np.round(bins,n)
        if missing:
            bins = np.insert(bins, 0, np.nan)
    return_frame = pd.DataFrame(columns=[feature, 'partial_dependence'])
    for j in bins:
        frame.loc[:, feature] = j
        par_dep_i = pd.DataFrame(model.predict(frame))
        par_dep_j = par_dep_i.mean().values[0]
        return_frame = return_frame.append({feature:j,
                                            'partial_dependence': par_dep_j}, 
                                            ignore_index=True)
    # return input frame to original cached state    
    frame.loc[:, feature] = col_cache
    return return_frame

def partial_residual(feature: str, frame: frame, model, y: str, resolution: int = 20, model_type: str = 'regression', bins = None, abs_: bool = False, class_: str = 'both', round_: bool = True):

    """ Calcula los residuos en el partial dependece para la variable especificada en feature
    Arg:
        feature: variable del frame sobre el cual realizar los calculos
        frame: data de entrada del modelo
        model: modelo entrenado con el cual calcular el partial dependence
        y: salida del modelo
        resolution: numero de puntos en los que calcular el partial dependence (si bins=None)
        model_type: tipo de modelo {'regression', 'classification'}
        bins: valores en los que calcular el partial dependence
        abs_: si entregar los valores absolutos o no
        class: en caso de ser un problema de clasificacion, si calcular los residuos para ambas clases o no
    Returns:
        Un frame con los valores de residuos calculados sobre la variable en features
    """

    if model_type=='classification' and class_ == 'both':
        resid_0 = partial_residual(feature, frame.loc[frame[y]==0], model, y, resolution, model_type, bins, abs_=False, class_='0')
        resid_1 = partial_residual(feature, frame.loc[frame[y]==1], model, y, resolution, model_type, bins, abs_=False, class_='1')['residual']
        return_frame =  resid_0.copy().rename(columns={'residual': 'resid_0'})
        return_frame['resid_1'] = resid_1
    else:
        #turn off pesky Pandas copy warning
        pd.options.mode.chained_assignment = None
        # initialize empty Pandas DataFrame with correct column names
        return_frame = pd.DataFrame(columns=[feature,'residual'])
        # cache original column values 
        col_cache = frame.loc[:, feature].copy(deep=True)
        # determine values at which to calculate partial dependence
        if type(bins) == type(None):
            (min_, max_) = (frame[feature].min(), frame[feature].max())
            by = (max_ - min_)/resolution
            bins = np.arange(min_, (max_ + by), (by + np.round((1. / resolution) * by, 3)))
            if round_:
                n=0
                for valor in frame[feature].astype('float').values:
                    _, decimals = str(valor).split('.')
                    if len(decimals)>n: n=len(decimals)
                bins = np.round(bins,n)
            # residuals of partial dependence
        for j in bins:
            # frame to cache intermediate results
            rframe_ = pd.DataFrame(columns=['actual', 'pred',  'res'])
            frame.loc[:, feature] = j
            dframe = frame.drop(y, axis=1)
            # reset index for expected merge behavior
            rframe_['actual'] = frame[y].reset_index(drop=True)
            rframe_['pred'] = pd.DataFrame(model.predict(dframe))
            # logloss residual
            if model_type=='regression':
                rframe_['res'] = rframe_['actual'] - rframe_['pred']
            elif model_type=='classification':
                rframe_['res'] = -rframe_['actual'] * np.log(rframe_['pred']) - (1 - rframe_['actual'])*np.log(1 - rframe_['pred'])
            else:
                raise ValueError('model_type="regression" or model_type="classification"')
            if abs_:
                # optionally return absolute value
                resid_j = np.abs(rframe_['res']).mean() 
            else:
                resid_j = rframe_['res'].mean()    
            del rframe_            
            return_frame = return_frame.append({feature:j,
                                        'residual': resid_j}, 
                                        ignore_index=True)
        # return input frame to original cached state    
        frame.loc[:, feature] = col_cache
    return return_frame

def ice(feature: str, frame: frame, model, index_: list = None, perc_data = None, labels = None, resolution: int = 20, bins = None, missing: bool = True, round_: bool = True):

    """ Calcula el partial dependence para la variable especificada en feature en las instancias de los indices entregados
    Arg:
        feature: variable del frame sobre el cual realizar los calculos
        frame: data de entrada del modelo
        model: modelo entrenado con el cual calcular el partial dependence
        index_: indices de instancias sobre las cuales obtener el calculo de partial dependence
        labels: nombres de las instancias en index_
        resolution: numero de puntos en los que calcular el partial dependence (si bins=None)
        bins: valores en los que calcular el partial dependence
        missing: si incluir un valor faltante (Nan) en los bins
    Returns:
        Un frame con los valores de partial dependence calculados sobre la variable en features en las instancias en index_
    """

    # turn off pesky Pandas copy warning
    pd.options.mode.chained_assignment = None
    # initialize empty Pandas DataFrame with correct column names
    if type(bins) == type(None):
        (min_, max_) = (frame[feature].min(), frame[feature].max())
        by = (max_ - min_)/resolution
        bins = np.arange(min_, (max_ + by), (by + np.round((1. / resolution) * by, 3)))
        if round_:
            n=0
            for valor in frame[feature].astype('float').values:
                _, decimals = str(valor).split('.')
                if len(decimals)>n: n=len(decimals)
            bins = np.round(bins,n)
        if missing:
            bins = np.insert(bins, 0, np.nan)
    return_frame = pd.DataFrame(bins, columns=[feature])

    if type(index_)==type(None):
        if type(perc_data)!=type(None):
            percentil_dict = percentiles(pd.DataFrame(perc_data), perc_data.name)
            index_= list(percentil_dict.values())
            labels = ['percentil_{}'.format(i) for i in percentil_dict.keys()]
        else:
            raise ValueError('Expected data to get percentil')
    if type(labels) == type(None):
        labels = ['index_' + str(i) for i in index_]
    for i, ind in enumerate(index_):
        return_frame[labels[i]] = partial_dependence(feature, frame.loc[[ind],:], model, bins=bins)['partial_dependence']
    return return_frame

from alibi.explainers import ALE

def ale(model, frame: frame):
    
    """ Calcula los valores de Accumulated Local Effect (ALE) del modelo para los datos en frame
    Arg:
        model: modelo entrenado con el cual calcular el partial dependence
        frame: data de entrada del modelo
    Returns:
        Entrega un diccionario con los nombres de las variables como sus llaves y los valores una tupla de los valores que estas toman
        y su valor ALE calculado
    """    
    exp_results = ALE(model.predict, feature_names=frame.columns).explain(frame.values)
    ale_results = {}
    for i in range(len(exp_results['feature_names'])):
        ale_results[exp_results['feature_names'][i]]=(exp_results['feature_values'][i],exp_results['ale_values'][i].reshape((exp_results['feature_values'][i].shape)))
    return ale_results


import string                             # for operations on character strings

def find_adversaries(xs: list, frame: frame, model, row_id: int, y: str, yhat: str, resid: str, oor_proportion: float = 0.1, 
                     resolution: int = 10, model_type: str = 'regression', verbose: bool = False):

    """ Funcion que encuentra instancias adversarias a partir de la entregada en row_id. Funciona generando loops anidados con valores
    perturbados en los valores de las variables en xs.
    Arg:
        xs: lista de los features por las cuales crear lasinstancias adversarias
        frame: frame con los datos con los cuales trabajar, debe contener los datos de entrada del modelo, la salida esperada (y),
               la prediccion del modelo (yhat) y los residuos (resid).
        model: modelo entrenado
        row_id: id de la fila desde la cual se crean los adversarios
        y: nombre de la salida del modelo en el frame
        yhat: nombre de la prediccion del modelo en el frame
        resid: nombre de los residuos de las predicciones en el frame
        oor_proportion: la proporcion por la cual la busqueda puede exceder el minimo y el maximo de los valores en el frame
        resolution: numero de puntos a traves de xs en los que buscar adversarios
        model_type: tipo de modelo (para calcular los residuos) {'regression', 'classification'}
        verbose: si mostrar o no la declaracion del codigo
    Returns:
        Entrega un frame con todos los adversarios encontrados junto con sus predicciones asociadas y sus residuos.
    """    

    # init dicts to hold bin values
    bins_dict = {}
    # find boundaries, bins and record 
    for j in xs:
        min_ = frame[j].min()
        max_ = frame[j].max()
        min_ = min_ - np.abs(oor_proportion*min_)
        max_ = max_ + np.abs(oor_proportion*max_)
        by = (max_ - min_)/resolution
        bins_dict[j] = np.arange(min_, (max_ + by), (by + np.round((1. / resolution) * by, 3)))
        bins_dict[j] = np.round_(bins_dict[j], 6)  # reasonable precision
    # initialize prototype row
    row = frame.loc[[row_id],:].copy(deep=True)
    #Variables ocupadas en los loops
    model=model
    y=y
    yhat=yhat
    resid=resid
    # generate nested loops dynamically to search all vals in all search cols
    # init true tab
    # define code variable and init returned Pandas DataFrame, adversary_frame
    tab = '    '
    code = 'global adversary_frame\n'
    code += 'adversary_frame = pd.DataFrame(columns=xs + [yhat, resid])\n'
    # generate for loop statements for search
    for i, j in enumerate(xs):
        code += i*tab + 'for ' + string.ascii_lowercase[i] + ' in ' +\
            str(list(bins_dict[j])) + ':\n'
    # generate value assignment statements to perturb search vars
    for k, j in enumerate(xs):
        code += (i + 1)*tab + 'row["' + j + '"] = ' + string.ascii_lowercase[k] +\
            '\n'
    # generate progress reporting statements  
    # generate statements for appending test values, preds, and resids to adversary_frame
    # uses only absolute residuals to avoid averaging problems between 0/1 target classes
    code += (i + 1)*tab + 'if (adversary_frame.shape[0] + 1) % 1000 == 0:\n'
    code += (i + 2)*tab +\
        'print("Built %i/%i rows ..." % (adversary_frame.shape[0] + 1, (resolution)**(i+1)))\n'
    code += (i + 1)*tab +\
        'adversary_frame = adversary_frame.append(row, ignore_index=True, sort=False)\n' 
    code += 'print("Scoring ...")\n'
    code += 'adversary_frame[yhat] = model.predict(adversary_frame[model.feature_name()])\n'
    if model_type=='regression':
        code += 'adversary_frame[resid] = np.abs(adversary_frame[y] - adversary_frame[yhat])\n'
    else:
        code += 'adversary_frame[resid] = np.abs(adversary_frame[y]*np.log(adversary_frame[yhat]) - (1 - adversary_frame[y])*np.log(1 - adversary_frame[yhat]))\n'
    code += 'print("Done.")'
    if verbose:
        print('Executing:')
        print(code)
        print('--------------------------------------------------------------------------------')
    # execute generated code
    exec(code)
    return adversary_frame

def random_attack(X, frame, model, oor_proportion=0.33, N=10000, 
                  inject_missing=True, missing_proportion=0.15, seed=12345):

    """ Genera un frame de instancias creadas aleatoriamente y calcula sus predicciones con el modelo
    Args:
        X: Variables del frame que son entradas del modelo.
        frame: frame sobre el cual calcular los datos aletatorios.
        model: modelo entrenado con el cuaL obtener las predicciones
        oor_proportion: la proporcion por la cual la busqueda puede exceder el minimo y el maximo de los valores en el frame
        N: numero de sampleos a generar.
        inject_missing: Si inyectar valores faltantes aleatoriamente o no en el frame generado
        missing_proportion: La proporcion de datos faltantes inyectados
        seed: semilla con la cual reproducir los calculos
    Returns:
        Entrega un frame con datos generados aleatoriamente
    """

    # init random frame
    random_frame = pd.DataFrame(columns=X, index=np.arange(N))
    # find bounds for each j and generate random data
    for j in X:
        min_ = frame[j].min()
        max_ = frame[j].max()
        np.random.seed(seed) # ensure column bounds are set similary 
        random_frame[j] =\
            np.random.uniform(low=(min_ - np.abs(oor_proportion*min_)),
                              high=(max_ + np.abs(oor_proportion*max_)),
                              size=(N,)) 
        # ensure treatment as numeric
        random_frame[j] = pd.to_numeric(random_frame[j])
    if inject_missing:
        np.random.seed(seed) # ensure nan is injected similarly       
        random_frame =\
            random_frame.mask(np.random.random(random_frame.shape) < missing_proportion)    
    # score
    random_frame['prediction'] = model.predict(random_frame)
    return random_frame

def get_prauc(frame, y, yhat, pos=1, neg=0, res=0.01):

    """ Calcula la precision, recall y el f1 para el frame entregado que contiene la salida esperada y obtenida de un modelo
    Args:
        frame: datos sobre los cuales calcular las metricas
        y: nombre de la columna con la salida esperada
        yhat: nombre de la columna con la salida obtenida
        pos: Valor del objetivo positivo
        neg: Valor del objetivo negativo
        res: Resolucion por la cual probar valores de cutoff.
    Returns:
        Un frame con los valores de precision, recall, y f1 para distintos valores de cutoff.
    """

    frame_ = frame.copy(deep=True) # don't destroy original data
    dname = 'd_' + str(y)          # column for predicted decisions
    eps = 1e-20                    # for safe numerical operations
    # init p-r roc frame
    prroc_frame = pd.DataFrame(columns=['cutoff', 'recall', 'precision', 'f1'])
    # loop through cutoffs to create p-r roc frame
    for cutoff in np.arange(0, 1 + res, res):
        # binarize decision to create confusion matrix values
        frame_[dname] = np.where(frame_[yhat] > cutoff , 1, 0)
        # calculate confusion matrix values
        tp = frame_[(frame_[dname] == pos) & (frame_[y] == pos)].shape[0]
        fp = frame_[(frame_[dname] == pos) & (frame_[y] == neg)].shape[0]
        tn = frame_[(frame_[dname] == neg) & (frame_[y] == neg)].shape[0]
        fn = frame_[(frame_[dname] == neg) & (frame_[y] == pos)].shape[0]
        # calculate precision, recall, and f1
        recall = (tp + eps)/((tp + fn) + eps)
        precision = (tp + eps)/((tp + fp) + eps)
        f1 = 2/((1/(recall + eps)) + (1/(precision + eps)))
        # add new values to frame
        prroc_frame = prroc_frame.append({'cutoff': cutoff,
                                          'recall': recall,
                                          'precision': precision,
                                          'f1': f1}, 
                                          ignore_index=True)
    del frame_
    return prroc_frame

def get_confusion_matrix(frame, y, yhat, by=None, level=None, cutoff=0.5):

    """ Calcula la matriz de confucion
    Args:
        frame: frame con la salida esperada (y) y la predecida (yhat).
        y: nombre de la columna con la salida esperada
        yhat: nombre de la columna con la salida obtenida
        by: variable sobre cual dividir el frame y crear la matriz de confucion
        level: valor de la variable con la cual se dividio el frame
        cutoff: valor umbral de cutoff sobre la cual realizar las decisiones de clasificacion
    Returns:
        Matriz de confucion como un DataFrame de pandas
    """
    # determine levels of target (y) variable
    # sort for consistency
    level_list = list(frame[y].unique())
    level_list.sort(reverse=True)
    # init confusion matrix
    cm_frame = pd.DataFrame(columns=['actual: ' +  str(i) for i in level_list], 
                            index=['predicted: ' + str(i) for i in level_list])
    # don't destroy original data
    frame_ = frame.copy(deep=True)
    # convert numeric predictions to binary decisions using cutoff
    dname = 'd_' + str(y)
    frame_[dname] = np.where(frame_[yhat] > cutoff , 1, 0)
    # slice frame
    if (by is not None) & (level is not None):
        frame_ = frame_[frame[by] == level]
    # calculate size of each confusion matrix value
    for i, lev_i in enumerate(level_list):
        for j, lev_j in enumerate(level_list):
            cm_frame.iat[j, i] = frame_[(frame_[y] == lev_i) & 
                                        (frame_[dname] == lev_j)].shape[0]
            # i,j vs. j,i - nasty little bug updated 8/30/19
    return cm_frame

def cm_exp_parser(expression, cm_dict):
    
    """ Traduce expresiones aberviadas de metricas provenientes de metric_dict a declaraciones ejecutables de python    
    Arg: 
        expression: Expresion de metrica de error de metric_dict.
    Returns:
        Python statements based on predefined metrics in metric_dict.
    """
    cm_dict = cm_dict
    # tp | fp       cm_dict[level].iat[0, 0] | cm_dict[level].iat[0, 1]
    # -------  ==>  --------------------------------------------
    # fn | tn       cm_dict[level].iat[1, 0] | cm_dict[level].iat[1, 1]

    expression = expression.replace('tp', '(cm_dict[level].iat[0, 0] + eps)')\
                           .replace('fp', '(cm_dict[level].iat[0, 1] + eps)')\
                           .replace('fn', '(cm_dict[level].iat[1, 0] + eps)')\
                           .replace('tn', '(cm_dict[level].iat[1, 1] + eps)')

    return expression


def get_cm_dict(name, cutoff, frame, y, yhat):

    """ Loops through levels of named variable and calculates confusion 
        matrices per level; uses dynamically generated entities to reduce 
        code duplication. 
    
    Args:
        name: Name of variable for which to calculate confusion matrices.
        cutoff: Cutoff threshold for confusion matrices. 
    
    Returns:
        Dictionary of confusion matrices. 
    
    """
    frame = frame
    y = y
    yhat = yhat
    levels = sorted(list(frame[name].unique())) # get levels
    cm_dict = {} # init dict to store confusion matrices per level
    for level in levels: 
    
        # dynamically name confusion matrices by level
        # coerce to proper python names
        cm_name = '_' + str(level).replace('-', 'm') + '_cm' 
    
        # dynamically calculate confusion matrices by level
        code = cm_name + ''' = get_confusion_matrix(frame,                              
                          y, 
                          yhat, 
                          by=name, 
                          level=level, 
                          cutoff=cutoff)'''
        exec(code)
        exec('cm_dict[level] = ' + cm_name) # store in dict
        
    return cm_dict

import seaborn as sns


def get_metrics_frame(name, frame, cutoff, y, yhat): 

    """ Loops through levels of named variable and metrics to calculate each 
        error metric per each level of the variable; uses dynamically generated 
        entities to reduce code duplication.
    
    Arg:
        name: Name of variable for which to calculate error metrics.
    
    Return:
        Pandas DataFrame of error metrics.
        
    """
    metric_dict = {
        'Prevalence': '(tp + fn) / (tp + tn +fp + fn)',
        'Accuracy':       '(tp + tn) / (tp + tn + fp + fn)',
        'Adverse Impact': '(tp + fp) / (tp + tn + fp + fn)',
        'True Positive Rate': 'tp / (tp + fn)',
        'Precision':          'tp / (tp + fp)', 
        'True Negative Rate': 'tn / (tn + fp)', 
        'Negative Predicted Value': 'tn / (tn + fn)',
        'False Positive Rate':  'fp / (tn + fp)', 
        'False Discovery Rate': 'fp / (tp + fp)',
        'False Negative Rate': 'fn / (tp + fn)',
        'False Omissions Rate':'fn / (tn + fn)'
                    }

    levels = sorted(list(frame[name].unique())) # get levels
    metrics_frame = pd.DataFrame(index=levels) # init Pandas frame for metrics
    eps = 1e-20 # for safe numerical operations

    cm_dict = get_cm_dict(name, cutoff, frame, y, yhat)

    # nested loop through:
    # - levels
    # - metrics 
    for level in levels:
        for metric in metric_dict.keys():
              
            # parse metric expressions into executable pandas statements
            expression = cm_exp_parser(metric_dict[metric], cm_dict)
        
            # dynamically evaluate metrics to avoid code duplication
            metrics_frame.loc[level, metric] = eval(expression)  

    # display results

    metrics_frame.index.name = name
    metrics_frame = metrics_frame.round(3).style.set_caption('Error Metrics for ' + name).background_gradient(cmap=sns.diverging_palette(-20, 260, n=7, as_cmap=True), axis=1)
    return metrics_frame