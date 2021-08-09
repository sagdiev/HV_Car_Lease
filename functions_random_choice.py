import random
from constants import *
from constants_columns import *

def random_choice_seed_list (len_list, seed):
    random.seed(seed)
    print(len_list)
    seed_list = random.sample(range(100000), len_list)
    print(seed_list)
    return seed_list

def random_choice_by_weight_single (options, weights, seed):
    """Генерирование случайного выбора по заданому вектору с весами (веса в сумме не обязаны быть 100 - любая сумма)"""
    weighted_options = [[opt] * wgt for opt, wgt in zip(options, weights)]
    weighted_options = [opt for sublist in weighted_options for opt in sublist]
    random.seed(seed)
    random_choice_result_sigle = random.choice(weighted_options)

    return random_choice_result_sigle


def random_choice_by_option_matrix (options_input, case_input, options_matrix, weights_for_row, seed):
    """Генерирование случайного выбора по заданой матрице с весами (веса в сумме не обязаны быть 100 - любая сумма)"""
    number_of_row = options_input.index(case_input)
    options_row = options_matrix[number_of_row]
    # random.seed(seed)
    random_choice_result_matrix = random_choice_by_weight_single(options_row, weights_for_row, seed)

    return random_choice_result_matrix


def random_choice_by_weight_matrix (options_input, case_input, options_for_row, weights_matrix, seed):
    """Генерирование случайного выбора по заданой матрице с весами (веса в сумме не обязаны быть 100 - любая сумма)"""
    number_of_row = options_input.index(case_input)
    weights_row = weights_matrix[number_of_row]
    # random.seed(seed)
    random_choice_result_matrix = random_choice_by_weight_single(options_for_row, weights_row, seed)

    return random_choice_result_matrix


def random_choice_client_type_pairs(seed):
    return random_choice_by_weight_single(CLIENT_TYPE_BY_SAVING_PAIR, EXPERT_CLIENT_TYPE_BY_SAVING_PAIR_DISTR, seed)

def random_choice_client_type_sign(seed):
    return 'Toyota RAV'

def random_choice_auto_type_sign(seed):
    return random_choice_by_weight_single(CLIENT_TYPE_BY_SAVING_SIGN, EXPERT_CLIENT_TYPE_BY_SAVING_PAIR_DISTR, seed)

def random_choice_period_saving(client_type, seed):
    return random_choice_by_option_matrix(
        CLIENT_TYPE_BY_SAVING_PAIR,
        client_type,
        EXPERT_PERIOD_SAVING_OPTIONS_BY_CLIENT_TYPE,
        EXPERT_PERIOD_SAVING_WEIGHTS,
        seed)


def random_choice_cost_flat(client_type, seed):
    return random_choice_by_weight_matrix(
        CLIENT_TYPE_BY_SAVING_PAIR, client_type,
        EXPERT_FLAT_COST_OPTIONS, EXPERT_FLAT_COST_WEIGHTS_BY_CLIENT_TYPE, seed)


def random_choice_period_postpayments(client_type, seed):
    return random_choice_by_option_matrix(
        CLIENT_TYPE_BY_SAVING_PAIR, client_type,
        EXPERT_PERIOD_POSTPAYMENT_OPTIONS_BY_CLIENT_TYPE, EXPERT_PERIOD_POSTPAYMENT_WEIGHTS, seed)



# x = random_choice_by_option_matrix (
#     CLIENT_TYPE_BY_SAVING_PAIR, [50, 0], EXPERT_PERIOD_SAVING_DISTR_BY_CLIENT_TYPE, EXPERT_PERIOD_SAVING_DISTR)
# print(x)
#
# x = random_choice_by_weight_matrix (
#     CLIENT_TYPE_BY_SAVING_PAIR, [30, 20], EXPERT_FLAT_COST_OPTIONS, EXPERT_FLAT_COST_WEIGHTS_BY_CLIENT_TYPE)
# print(x)

# print(random_choice_seed_list (1062, 1))
