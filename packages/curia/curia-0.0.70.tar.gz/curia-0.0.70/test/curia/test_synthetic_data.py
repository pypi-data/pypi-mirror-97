from curia.synthetic_data import generate_data
import numpy as np
import pandas as pd
import random


def test_generate_data_defaults():
    (X_train, X_test, t_train, t_test, y_train, y_test, true_ite_train, true_ite_test,
     true_treatment_propensity_train,
     true_treatment_propensity_test) = generate_data()

    assert X_train.shape == (1000, 14)
    assert X_test.shape == (100, 14)
    assert y_train.shape == (1000,)
    assert y_test.shape == (100,)
    assert t_train.shape == (1000,)
    assert t_test.shape == (100,)
    assert true_ite_train.shape == (1000,)
    assert true_ite_test.shape == (100,)
    assert true_treatment_propensity_train.shape == (1000,)
    assert true_treatment_propensity_test.shape == (100,)

    assert np.round(y_train.mean(), 2) == 0.44
    assert np.round(y_test.mean(), 2) == 0.44

    assert np.round(t_train.mean(), 2) == 0.05
    assert np.round(t_test.mean(), 2) == 0.02

    assert np.round(true_ite_train.mean(), 2) == 0.01
    assert np.round(true_ite_test.mean(), 2) == -0.0

    assert np.round(true_treatment_propensity_train.mean(), 2) == 0.05
    assert np.round(true_treatment_propensity_test.mean(), 2) == 0.05


def test_generate_data_seed_consistency():
    """
    Ensures that the seed works properly in that two different runs with the same seed
    and same parameters will produce the same outputs and that two different runs with different
    seeds and the same parameters will produce different outputs
    """
    tuple_a = generate_data(seed=971109)
    tuple_b = generate_data(seed=971109)
    for element_a, element_b in zip(tuple_a, tuple_b):
        assert isinstance(element_a, type(element_b)), \
            f"Inconsistent data returned from generate_data with same seed: " \
            f"{type(element_a)} (type(element_a)) != {type(element_b)} (type(element_b))"
        if isinstance(element_a, (pd.DataFrame, pd.Series)):
            assert element_a.equals(element_b), \
                f"Inconsistent data returned from generate_data with same seed: " \
                f"{element_a} (element_a) != {element_b} (element_b)"
        else:
            assert element_a == element_b, \
                f"Inconsistent data returned from generate_data with same seed: " \
                f"{element_a} (element_a) != {element_b} (element_b)"
    tuple_c = generate_data(seed=190427)
    all_matching = True
    for element_a, element_b in zip(tuple_a, tuple_c):
        assert isinstance(element_a, type(element_b)), \
            f"Types of returned elements must match, even with different seeds: {type(element_a)} != {type(element_b)}"
        if isinstance(element_a, (pd.DataFrame, pd.Series)):
            if not element_a.equals(element_b):
                all_matching = False
        else:
            if not element_a == element_b:
                all_matching = False
    assert not all_matching, "Two runs with different seeds produced identical data!"


def test_columns_number_modifications():
    """
    Tests to make sure that the correct number of columns are returned in X_train and X_test depending on variations
    of num_uniform, num_binary, and num_normal
    """
    num_uniform = random.randint(2, 20)
    num_binary = random.randint(2, 20)
    num_normal = random.randint(2, 20)
    (X_train, X_test, _, _, _, _, _, _, _, _) = generate_data(uniform_dim=num_uniform,
                                                              binary_dim=num_binary,
                                                              normal_dim=num_normal,
                                                              missing_data_scaler=0,
                                                              n_confounders=0)
    x_train_cols = set(X_train.columns)
    x_test_cols = set(X_test.columns)
    required_cols = {"age"} | \
                    {f"sdoh_{i}" for i in range(num_uniform)} | \
                    {f"binary_flag_{i}" for i in range(num_binary)} | \
                    {f"vector_{i}" for i in range(num_normal)}
    assert x_train_cols == x_test_cols, "Train and test cols must match!\n" \
                                        f"In x_train_cols but not in x_test_cols: {x_train_cols - x_test_cols} \n" \
                                        f"In x_test_cols but not in x_train_cols: {x_test_cols - x_train_cols} \n"
    assert required_cols == x_train_cols, "Required and train cols must match!\n" \
                                          f"In x_train_cols but not in required_cols: {x_train_cols - required_cols} \n" \
                                          f"In required_cols but not in x_train_cols: {required_cols - x_train_cols} \n"


def test_binary_outcome():
    (_, _, _, _, y_train, y_test, _, _, _, _) = generate_data(binary_outcome=True)
    assert ((y_train == 1) | (y_train == 0)).all(), "If binary_outcome=True, then all of y_train must be 1 or 0"
    assert ((y_test == 1) | (y_test == 0)).all(), "If binary_outcome=True, then all of y_test must be 1 or 0"
    (_, _, _, _, y_train, y_test, _, _, _, _) = generate_data(binary_outcome=False)
    assert not ((y_train == 1) | (y_train == 0)).all(), \
        "If binary_outcome=False, then not all of y_train should be 1 or 0"
    assert not ((y_test == 1) | (y_test == 0)).all(), \
        "If binary_outcome=False, then not all of y_test should be 1 or 0"
