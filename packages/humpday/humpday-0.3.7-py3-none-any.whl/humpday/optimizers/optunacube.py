import optuna
from optuna.logging import CRITICAL
from humpday.objectives.classic import CLASSIC_OBJECTIVES
import logging
from humpday.transforms.zcurves import curl_factory

logging.getLogger('optuna').setLevel(logging.ERROR)


def optuna_cube_factory(objective, n_trials, n_dim, with_count=False, method=None):

    if method.lower()=='random':
        sampler = optuna.samplers.RandomSampler()
    elif method.lower()=='cmaes':
        sampler = optuna.samplers.CmaEsSampler()
    elif method.lower()=='tpe':
        sampler = optuna.samplers.TPESampler()
    else:
        raise ValueError('random, cmaes, tpe or grid please')

    global feval_count
    feval_count = 0

    def cube_objective(trial):
        global feval_count
        us = [ trial.suggest_float('u'+str(i),0,1) for i in range(n_dim)]
        feval_count += 1
        return objective(us)

    optuna.logging.set_verbosity(CRITICAL)
    study = optuna.create_study(sampler=sampler)
    study.optimize(cube_objective,n_trials=n_trials)

    best_x = [ study.best_params['u'+str(i)] for i in range(n_dim) ]

    if with_count:
        return study.best_value, best_x, feval_count
    else:
        return study.best_value, best_x


def optuna_random_cube(objective, n_trials,n_dim, with_count=False):
    return optuna_cube_factory(objective=objective, n_trials=n_trials, n_dim=n_dim, with_count=with_count, method='random')


def optuna_random_cube_clone(objective, n_trials,n_dim, with_count=False): # duplicate
    return optuna_cube_factory(objective=objective, n_trials=n_trials, n_dim=n_dim, with_count=with_count, method='random')


def optuna_random_cube_clone_1(objective, n_trials,n_dim, with_count=False): # duplicate
    return optuna_cube_factory(objective=objective, n_trials=n_trials, n_dim=n_dim, with_count=with_count, method='random')


def optuna_random_cube_clone_2(objective, n_trials,n_dim, with_count=False): # duplicate
    return optuna_cube_factory(objective=objective, n_trials=n_trials, n_dim=n_dim, with_count=with_count, method='random')


def optuna_cmaes_cube(objective, n_trials, n_dim, with_count=False):
    return optuna_cube_factory(objective=objective, n_trials=n_trials, n_dim=n_dim, with_count=with_count, method='cmaes')


def optuna_tpe_cube(objective, n_trials, n_dim, with_count=False):
    return optuna_cube_factory(objective=objective, n_trials=n_trials, n_dim=n_dim, with_count=with_count, method='tpe')


def optuna_cmaes_curl2_cube(objective, n_trials, n_dim, with_count=False):
    # Highly experimental
    return curl_factory(optimizer=optuna_cmaes_cube, objective=objective, n_trials=n_trials, n_dim=n_dim, with_count=with_count,d=2)


def optuna_cmaes_curl3_cube(objective, n_trials, n_dim, with_count=False):
    # Highly experimental
    return curl_factory(optimizer=optuna_cmaes_cube, objective=objective, n_trials=n_trials, n_dim=n_dim, with_count=with_count,d=3)


OPTUNA_OPTIMIZERS = [optuna_cmaes_cube,
                     optuna_tpe_cube, optuna_random_cube, optuna_random_cube_clone, optuna_random_cube_clone_1,
                     optuna_random_cube_clone_2]


if __name__=='__main__':
    for objective in CLASSIC_OBJECTIVES:
        print(' ')
        print(objective.__name__)
        for optimizer in OPTUNA_OPTIMIZERS:
            print((optimizer(objective, n_trials=250, n_dim=16, with_count=True)))
