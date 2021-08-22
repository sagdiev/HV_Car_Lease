import pandas as pd
import math as m
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer
import random
from statistics import mean
from constants import *
from constants_CF import *
from constants_columns import *

from functions_base import *
from functions_random_choice import *
from functions_path_file import *


# START
start = timer()
print('START\n')

# папки и файлы
path_folder = path_folder(PATH_FOLDER, GLOBAL_EXPERIMENT_NAME)
create_folder_or_check_existence(path_folder)

results_cash_flow                           = []
results_invest_port                         = []
results_invest_port_month                   = []
results_bep_month                           = []
results_months_port                         = []
results_mean_cash_flow_port                 = []
results_mean_cash_flow_port_accumulative    = []
postpayment_percent_amount_list             = []

print('Кол-во Продаж в одном эксперименте:', COUNT_SELLS)

df_experiments      = pd.DataFrame(columns=COLUMN_EXPERIMENTS_NAMES)
df_results          = pd.DataFrame(columns=COLUMN_EXPERIMENTS_RESULT_NAMES)
df_result_client    = pd.DataFrame(columns=COLUMN_RESULT_CLIENT_NAMES)

df_start_units      = pd.read_csv(PATH_FILE_UNIT_START, sep=',')
# df_csv.reset_index(drop=True, inplace=True)
print(df_start_units)
fixed_user_count    = len(df_start_units)
max_id_fixed_user   = fixed_user_count - 1
print('max_id_fixed_user', max_id_fixed_user)




# РАСЧЕТ ЭКСПЕРИМЕНТОВ по одному
for j in range(COUNT_EXPERIMENTS):
    print('\nExperiment ' , j+1, 'СТАРТ ==========================================='
                                 '=============================')  # печать времени работы алгоритма
    k                               = 0
    accum_ALL                       = 0
    funds_spent_total               = 0
    results_accum_ALL_experiment    = []
    cost_admin_t                    = 0

    profitloss_income_total_acc     = 0
    profitloss_expenses_total_acc   = 0
    profitloss_profit_net_acc       = 0

    print('COUNT_SELLS', COUNT_SELLS)
    if IS_RANDOM_CONTROLLED_BY_SEED is True:
        seed_root_experiment_j = RANDOM_SEED_START
    else:
        seed_root_experiment_j = random.randint(1,1000)
    seed_list = random_choice_seed_list(COUNT_SELLS, seed_root_experiment_j)
    print('seed_list', seed_list)

    df = pd.DataFrame(columns=COLUMN_UNIT_NAMES)

    df_summary                                      = pd.DataFrame(columns=COLUMN_UNITS_SUMMARY_NAMES)
    # df_summary.loc[0, column_accum_savings_total]   = 0
    # df_summary.loc[0, column_funds_ready_to_spend]  = 0
    # df_summary.loc[0, column_funds_spent]           = 0
    # df_summary.loc[0, column_funds_spent_total]     = 0

    df_cashflow = pd.DataFrame(columns=COLUMN_CASH_FLOW)

    ### ГЕНЕРИРОВАНИЕ ВСЕХ КЛИЕНТОВ с самого начала
    ### ===============================================
    id_user = 0

    for p in range(len(COUNT_SELLS_BY_MONTHS)):  # Перебор всех месяцев продаж

        sells_in_period = COUNT_SELLS_BY_MONTHS[p]
        # print(sells_in_period)
        # seed_i = RANDOM_SEED_START

        for i in range(sells_in_period):  # Перебор всех продаж в конкретный месяц

            # генерирование seed random (ядра случайного выбора) для каждого из типов значений, выбираемых случайно
            seed_i                      = seed_list[id_user]
            seed_i_list                 = random_choice_seed_list(3, seed_i)
            seed_auto_type              = seed_i_list[0]
            seed_if_unplaned_stop       = seed_i_list[1]
            seed_unplaned_stop_period   = seed_i_list[2]
            # seed_period_saving          = seed_i_list[2]
            # seed_period_postpayments    = seed_i_list[3]

            # генерирование вводных значений Клиента
            if id_user > max_id_fixed_user:
                auto_type               = random_choice_client_type_sign(seed_auto_type)
                # # client_type_pair     = CLIENT_TYPE_BY_SAVING_PAIR[CLIENT_TYPE_BY_SAVING_SIGN.index(client_type)]
                # cost_flat            = random_choice_cost_flat(client_type_pair, seed_cost_flat)
                # period_saving        = random_choice_period_saving(client_type_pair, seed_period_saving)
                # period_postpayments  = random_choice_period_postpayments(client_type_pair, seed_period_postpayments)
            else:
                auto_type          = df_start_units[column_auto_type][id_user]
                # client_type_pair     = CLIENT_TYPE_BY_SAVING_PAIR[CLIENT_TYPE_BY_SAVING_SIGN.index(client_type)]
                # cost_flat            = df_start_units[column_cost_vehicle][id_user]
                # period_saving        = df_start_units[column_period_saving][id_user]
                # period_postpayments  = df_start_units[column_period_postpayments][id_user]

            # client_type = random_choice_client_type_sign(seed_client_type)
            # client_type_pair = CLIENT_TYPE_BY_SAVING_PAIR[CLIENT_TYPE_BY_SAVING_SIGN.index(client_type)]  # определяем индекс клиентской пары по рандомно выбранному типу
            # cost_flat = random_choice_cost_flat(client_type_pair, seed_cost_flat)
            # period_saving = random_choice_period_saving(client_type_pair, seed_period_saving)
            # period_postpayments = random_choice_period_postpayments (client_type_pair, seed_period_postpayments)


            price_auto_client                = DICT_AUTO[auto_type]['price']
            price_auto_company               = price_auto_client * (1 - DISCOUNT_AUTO_FOR_CONPANY / 100)  # TODO лучше привязать такую скидку к марке автомобиля
            period_payments                 = PERIOD_PAYMENTS  # Общий плановый период Выплат
            period_payments_start           = p  # Номер месяца начала Выплат
            period_payments_uplaned_stop    = 'Period Payments Uplaned Stop'  # Номер месяца незапланированной остановки

            payment_monthly                 = DICT_AUTO[auto_type]['payment_monthly']  # Размер платежа в месяц
            prepayment                      = payment_monthly * COUNT_PREPAYMENTS  # Размер Залога

            client_status                   = CLIENT_STATUS_START
            rank                            = RANK_START

            cashflow_client_plan            = [prepayment] + [payment_monthly] * ( period_payments - COUNT_PREPAYMENTS )

            cost_prepayment                 = price_auto_company * 25 / 100
            cost_payment_onboard            = price_auto_company * COST_ONBOARD_PAYMENT_PERCENT / 100
            cost_payment_notary             = price_auto_company * COST_NOTARY_PERCENT / 100
            cost_payment_tax                = price_auto_company * COST_TAX_PERCENT / 100
            cost_payment_bank               = price_auto_company * COST_BANK_FEE_PERCENT / 100

            annuity_pair                    = calc_annuity_payments_company(price_auto_company,
                                                                            period_payments,
                                                                            BANK_PERCENT_MARKET)
            cost_payments_auto_company_monthly      = annuity_pair[0]
            # total_amount_postpayments       = annuity_pair[1]
            # postpayment_percent_amount_list = annuity_pair[2]
            # credit_base_cover_list          = annuity_pair[3]
            # credit_base_list                = annuity_pair[4]
            cashflow_company_annuity_plan   = [cost_payments_auto_company_monthly] * 36
            cost_payment_company_in_first_period    = cost_prepayment + cost_payment_onboard \
                                                    + cost_payment_notary + cost_payment_tax + cost_payment_bank

            cashflow_company_plan           = [cost_payment_company_in_first_period] \
                                            + [cost_payments_auto_company_monthly] * 36

            cashflow_client_fact            = []
            cashflow_company_fact           = []

            fair_value_auto_client          = price_auto_client
            fair_value_aut_company          = price_auto_company

            accum_payments_amount_client    = 0  # Накопленные платежи Клиента
            accum_payments_amount_company   = 0  # Накопленные платежи Компания


            df.loc[k, column_id_user]                           = id_user
            df.loc[k, column_auto_type]                         = auto_type
            df.loc[k, column_price_auto_client]                 = price_auto_client
            df.loc[k, column_price_auto_company]                = price_auto_company
            df.loc[k, column_period_payments]                   = period_payments
            df.loc[k, column_period_payments_start]             = period_payments_start
            df.loc[k, column_period_payments_uplaned_stop]      = period_payments_uplaned_stop
            df.loc[k, column_payment_monthly]                   = payment_monthly
            df.loc[k, column_prepayment]                        = prepayment
            df.loc[k, column_client_status]                     = client_status
            df.loc[k, column_rank]                              = rank
            df.loc[k, column_cashflow_client_plan]              = cashflow_client_plan
            df.loc[k, column_cashflow_company_plan]             = cashflow_company_plan
            df.loc[k, column_cashflow_client_fact]              = cashflow_client_fact
            df.loc[k, column_cashflow_company_fact]             = cashflow_company_fact
            df.loc[k, column_fair_value_auto_client]            = fair_value_auto_client
            df.loc[k, column_fair_value_aut_company]            = fair_value_aut_company
            df.loc[k, column_accum_payments_amount_client]      = accum_payments_amount_client
            df.loc[k, column_accum_payments_amount_company]     = accum_payments_amount_company

            id_user += 1
            k += 1
            print('exp', j+1, 'unit', k, 'param:', client_status, auto_type, price_auto_client,
                  '| period_payments', period_payments, 'start', period_payments_start, 'payment_monthly', payment_monthly)

    print(df.to_string())




    ### ПОДСЧЕТ ШАГА НА КАЖДОМ МЕСЯЦЕ
    ### ==================================================================================================================================
    cashflow_accum_t = 0

    for t in range(COUNT_MONTHS_OF_CALC):

        # todo расчитать максимальное время t!!!!

        print('               ')
        print('=========== ЭКСПЕРИМЕНТ', j, '=== Месяц', t, '=========================================================')
        # print(t)

        income_payments_t           = 0
        income_prepayment_t         = 0

        cost_payments_t             = 0
        cost_prepayment_t           = 0
        cost_payment_onboard_t      = 0
        cost_payment_notary_t       = 0
        cost_payment_tax_t          = 0
        cost_payment_bank_deal_t         = 0






        for i in range(COUNT_SELLS):
            # print('i = ', i)

            period_payments_start_i         = df[column_period_payments_start][i]

            # _i = df[column_][i]


            if period_payments_start_i == t:
                # ВЫДАЧА АВТО ==========================================================================================================================
                ### ==================================================================================================================================
                id_user_i                   = df[column_id_user][i]
                client_status_i             = df[column_client_status][i]
                price_auto_client_i         = df[column_price_auto_client][i]
                price_auto_company_i        = df[column_price_auto_company][i]
                prepayment_i                = df[column_prepayment][i]

                # print('START id_user_i = ', id_user_i)
                # print('price_auto_client_i = ', price_auto_client_i)

                # Расчет Deal income и cost - поступления и затрат при оформлении Клиенту Лизинга
                income_payments_t           += 0
                income_prepayment_t         += prepayment_i

                cost_payments_t             += 0
                cost_prepayment_t           += price_auto_company_i * 25 / 100
                cost_payment_onboard_t      += price_auto_company_i * COST_ONBOARD_PAYMENT_PERCENT / 100
                cost_payment_notary_t       += price_auto_company_i * COST_NOTARY_PERCENT / 100
                cost_payment_tax_t          += price_auto_company_i * COST_TAX_PERCENT / 100
                cost_payment_bank_deal_t         += price_auto_company_i * COST_BANK_FEE_PERCENT / 100

            elif period_payments_start_i in range (t - PERIOD_PAYMENTS, t):
                # ПОТОЧНЫЙ МЕСЯЦ КЛМЕНТА ==========================================================================================================================
                ### ==================================================================================================================================
                id_user_i                   = df[column_id_user][i]
                client_status_i             = df[column_client_status][i]
                price_auto_client_i         = df[column_price_auto_client][i]
                price_auto_company_i        = df[column_price_auto_company][i]
                payment_monthly_i           = df[column_payment_monthly][i]
                cashflow_company_plan_i     = df[column_cashflow_company_plan][i]

                # Расчет Deal income и cost - поступления и затрат при оформлении Клиенту Лизинга
                income_payments_t           += payment_monthly_i
                income_prepayment_t         += 0

                cost_payments_t             += cashflow_company_plan_i[t - period_payments_start_i]
                cost_prepayment_t           += 0
                cost_payment_onboard_t      += 0
                cost_payment_notary_t       += 0
                cost_payment_tax_t          += 0
                cost_payment_bank_deal_t         += 0

                # df_cashflow.loc[t, cf_income_payments] = round(income_payments_t, 0)
                # df_cashflow.loc[t, cf_income_prepayment] = round(income_prepayment_t, 0)


        # Подсчет ИСХОДЯЩИХ САЛЬДО по общим фондам
        ### ==================================================================================================================================
#
#         accum_amount_saving         = df[column_accum_amount_saving].sum()
#         accum_amount_postpayments   = df[column_accum_amount_postpayments].sum()
#         accum_ALL                   = accum_amount_saving + accum_amount_postpayments
#

        income_client_t                     = income_payments_t + income_prepayment_t
        income_add_t                        = 0
        income_total_t                      = income_client_t + income_add_t

        cost_buy_payment_t                  = cost_payments_t + \
                                              cost_prepayment_t + \
                                              cost_payment_onboard_t + \
                                              cost_payment_notary_t + \
                                              cost_payment_tax_t + \
                                              cost_payment_bank_deal_t

        cost_bank_percent_t                 = 0

        cost_admin_t                        = COST_ADMIN
        cost_market_t                       = COST_MARKETING_PERCENT

        cost_total_t                        = cost_buy_payment_t + \
                                              cost_bank_percent_t + \
                                              cost_admin_t + \
                                              cost_market_t


        cashflow_net_t                  = income_total_t - cost_total_t
        cashflow_accum_buttom_t         = cashflow_accum_t - cost_total_t  # дно остатков
        cashflow_accum_t               += cashflow_net_t
#
#
#         profitloss_income_total_t       = income_postpayments_percent_t + \
#                                           income_onboard_payment_t + \
#                                           income_buy_payment_t + \
#                                           income_add_percent_t + \
#                                           income_discount_t
#
#         profitloss_expenses_total_t     = cost_buy_payment_t + \
#                                           cost_bank_percent_t + \
#                                           cost_admin_t + \
#                                           cost_market_t
#
#         profitloss_profit_net_t         = profitloss_income_total_t - profitloss_expenses_total_t
#
#         profitloss_income_total_acc    += profitloss_income_total_t
#         profitloss_expenses_total_acc  += profitloss_expenses_total_t
#         profitloss_profit_net_acc      += profitloss_profit_net_t
#

        df_cashflow.loc[t, cf_period]                               = round(t, 0)

        df_cashflow.loc[t, cf_income_client]                        = round(income_client_t, 0)
        df_cashflow.loc[t, cf_income_add]                           = round(income_add_t, 0)
        df_cashflow.loc[t, cf_income_total]                         = round(income_total_t, 0)

        df_cashflow.loc[t, cf_cost_payments]                        = round(-cost_payments_t, 0)
        df_cashflow.loc[t, cf_cost_prepayment]                      = round(-cost_prepayment_t, 0)
        df_cashflow.loc[t, cf_cost_payment_onboard]                 = round(-cost_payment_onboard_t, 0)
        df_cashflow.loc[t, cf_cost_payment_notary]                  = round(-cost_payment_notary_t, 0)
        df_cashflow.loc[t, cf_cost_payment_tax]                     = round(-cost_payment_tax_t, 0)
        df_cashflow.loc[t, cf_cost_payment_bank_deal]               = round(-cost_payment_bank_deal_t, 0)
        df_cashflow.loc[t, cf_cost_admin]                           = round(-cost_admin_t, 0)
        df_cashflow.loc[t, cf_cost_market]                          = round(-cost_market_t, 0)

        df_cashflow.loc[t, cf_cost_buy_total]                       = round(-cost_buy_payment_t, 0)
        df_cashflow.loc[t, cf_cost_total]                           = round(-cost_total_t, 0)

        df_cashflow.loc[t, cf_cashflow_net]                         = round(cashflow_net_t, 0)
        df_cashflow.loc[t, cf_cashflow_accum_buttom]                = round(cashflow_accum_buttom_t, 0)
        df_cashflow.loc[t, cf_cashflow_accum]                       = round(cashflow_accum_t, 0)
#
#         df_cashflow.loc[t, pl_income_total]                         = round(profitloss_income_total_t, 0)
#         df_cashflow.loc[t, pl_expenses_total]                       = round(-profitloss_expenses_total_t, 0)
#         df_cashflow.loc[t, pl_profit_net]                           = round(profitloss_profit_net_t, 0)
#
#         df_cashflow.loc[t, pl_income_total_acc]                     = round(profitloss_income_total_acc, 0)
#         df_cashflow.loc[t, pl_expenses_total_acc]                   = round(-profitloss_expenses_total_acc, 0)
#         df_cashflow.loc[t, pl_profit_net_acc]                       = round(profitloss_profit_net_acc, 0)

        df_cashflow.loc[t, cf_income_payments]                      = round(income_payments_t, 0)
        df_cashflow.loc[t, cf_income_prepayment]                    = round(income_prepayment_t, 0)

        df_cashflow.describe()
#
#
#         df_summary.loc[t, column_accum_savings_total]               = round(accum_amount_saving, 0)  # общий фонд Накопленный за все время
#         df_summary.loc[t, column_accum_amount_postpayments_total]   = round(accum_amount_postpayments, 0)  # общий фонд Накопленный за все время
#         df_summary.loc[t, column_accum_ALL]                         = round(accum_ALL, 0)
#
#         df_summary.loc[t + 1, column_cost_next_flat]                = cost_next_flat
#         df_summary.loc[t + 1, column_id_next]                       = id_next
#         df_summary.loc[t, column_count_flat_received]               = count_flat_received
#         df_summary.loc[t + 1, column_count_waiting]                 = count_waiting
#
#         df_summary.loc[t + 1, column_funds_ready_to_spend]          = round(cashflow_accum_t, 0)  # Весь остаток Денег
#         # df_summary.loc[t + 1, column_funds_ready_to_spend] = \
#         #     df_summary[column_accum_ALL][t] - df_summary[column_funds_spent_total][t]  # разница между суммой всех накоплений и суммой всех трат на закупку квартир
#
#
#
#         # print('accum_funds_total =', df_summary[column_accum_savings_total][t])
#         # print('accum_amount_postpayments_total =', df_summary[column_accum_amount_postpayments_total][t])
#         # print('funds_ready_to_spend =', df_summary[column_funds_ready_to_spend][t])
#         # print('cost_next_flat  =', cost_next_flat)
#         # print('count_flat_received_total  =', count_flat_received)
#         # print('count_waiting  =', count_waiting)
#         # print('funds_spent_step =', df_summary[column_funds_spent][t])
#         # print('funds_spent_total =', df_summary[column_funds_spent_total][t])
#
#         # print(df.to_string())
#         # print(df_summary.to_string())

    # Подведение РЕЗУЛЬТАТОВ одного ЭКСПЕРИМЕНТА
    ### ==================================================================================================================================
    print(df.to_string())
#     print(df_summary.to_string())
    print(df_cashflow.to_string())
#     print(df_cashflow.sum())
#
#
#     df_experiments.loc[j, column_id_experiment]         = j
#     df_experiments.loc[j, column_accum_ALL]             = accum_ALL
#     df_experiments.loc[j, column_funds_spent_total]     = funds_spent_total
#
#     df_experiments.loc[j, column_max_waiting_period]    = df[column_waiting_period].max()
#     df_experiments.loc[j, column_max_waiting_count]     = df_summary[column_count_waiting].max()
#     # column_max_waiting_period = 'MAX Waiting Period'
#     # column_max_waiting_count
#
#     print(df_experiments.to_string())
#
#     # Подведение РЕЗУЛЬТАТОВ одного ЭКСПЕРИМЕНТА для ГРАФИКОВ
#     ### ==================================================================================================================================
#     results_accum_savings_total_experiment              = df_summary[column_accum_savings_total].tolist()
#     results_accum_amount_postpayments_total_experiment  = df_summary[column_accum_amount_postpayments_total].tolist()
#     results_accum_ALL_experiment                        = df_summary[column_accum_ALL].tolist()
#     results_count_waiting_experiment                    = df_summary[column_count_waiting].tolist()
#     results_funds_ready_to_spend_experiment             = df_summary[column_funds_ready_to_spend].tolist()
#     results_funds_spent_experiment                      = df_summary[column_funds_spent].tolist()
#     results_count_flat_received_experiment              = df_summary[column_count_flat_received].tolist()
#     results_waiting_period_experiment                   = df[column_waiting_period].tolist()
#     # results_column_client_type_experiment = df[column_client_type].tolist()
#
#     results_cashflow_experiment                         = df_cashflow[cf_cashflow_net].tolist()
#     results_cashflow_accum_buttom_experiment            = df_cashflow[cf_cashflow_accum_buttom].tolist()
#     results_cashflow_accum_experiment                   = df_cashflow[cf_cashflow_accum].tolist()
#
#     results_profitloss_profit_net_experiment            = df_cashflow[pl_profit_net_acc].tolist()

    # Запись в файл CF результатов эксперимента
    print('path_folder = ', path_folder)
    path_file_j = path_file(path_folder + 'units', j + 1)  # файл экспериманта j
    file_clear(path_file_j)
    df.to_csv(path_file_j, sep=',', index=False, )
    print("Файл создан: ", path_file_j)

    # path_file_j = path_file(path_folder + 'summary', j + 1)  # файл экспериманта j
    # file_clear(path_file_j)
    # df_summary.to_csv(path_file_j, sep=',', index=False, )
    # print("Файл создан: ", path_file_j)

    path_file_j = path_file(path_folder + 'cashflow', j + 1)  # файл экспериманта j
    file_clear(path_file_j)
    df_cashflow.to_csv(path_file_j, sep=',', index=False, )
    print("Файл создан: ", path_file_j)
#
#
#
# c = [mean(value_i) for value_i in zip(results_accum_savings_total_experiment,results_accum_amount_postpayments_total_experiment)]
#
#
# print('Experiment' , j+1, 'завершен. Время:', timer(), 'сек \n')  # печать времени работы алгоритма
#
#
# # ГРАФИКИ
# ### ==================================================================================================================================
#
#
# plt.figure(1, figsize=(15, 10))
#
# plt.subplot(1,1,1)
# plot_1 = pd.Series(results_funds_ready_to_spend_experiment)
# plot_2 = pd.Series(results_funds_spent_experiment)
# plot_3 = pd.Series(results_cashflow_experiment)
# plot_4 = pd.Series(results_profitloss_profit_net_experiment)
# plot_5 = pd.Series(results_cashflow_accum_buttom_experiment)
# plot_1.plot(grid=False)
# plot_2.plot.bar(grid=False)
# plot_3.plot(grid=False)
# plot_4.plot(grid=False)
# plot_5.plot(grid=False)
# plt.title('SUMMARY of Experiment')
# plt.grid(axis='y', alpha=0.75)
#
#
# plt.figure(2, figsize=(15, 10))
#
# plt.subplot(2,2,1)
# plot_1 = pd.Series(results_funds_ready_to_spend_experiment)
# plot_2 = pd.Series(results_funds_spent_experiment)
# plot_3 = pd.Series(results_cashflow_experiment)
# plot_4 = pd.Series(results_profitloss_profit_net_experiment)
# plot_1.plot(grid=True)
# plot_2.plot.bar(grid=False)
# plot_3.plot(grid=True)
# plot_4.plot(grid=True)
# plt.title('SUMMARY of Experiment')
# plt.grid(axis='y', alpha=0.75)
#
# plt.subplot(2,2,2)
# plot_1 = pd.Series(results_accum_savings_total_experiment)
# plot_2 = pd.Series(results_accum_amount_postpayments_total_experiment)
# plot_3 = pd.Series(results_accum_ALL_experiment)
# # plot_3 = pd.Series(c)
# plot_4 = pd.Series(results_funds_ready_to_spend_experiment)
# plot_5 = pd.Series(results_funds_spent_experiment)
# plot_1.plot(grid=True)
# plot_2.plot(grid=True)
# plot_3.plot(grid=True)
# plot_4.plot(grid=True)
# plot_5.plot.bar(grid=False)
# plt.title('Savings and PostPayments')
# plt.grid(axis='y', alpha=0.75)
#
# plt.subplot(2,3,4)
# plot_1 = pd.Series(results_waiting_period_experiment)
# plot_1.plot.hist(grid=True, bins=40, rwidth=0.9, color='#607c8e')
# plt.title('Hist Waiting Period')
# plt.grid(axis='y', alpha=0.75)
#
# plt.subplot(2,3,5)
# plot_1 = pd.Series(results_count_waiting_experiment)
# plot_1.plot.bar(grid=False)
# plt.title('Count Waiting')
# plt.grid(axis='y', alpha=0.75)
#
# plt.subplot(2,3,6)
# plot_1 = pd.Series(results_count_flat_received_experiment)
# # plot_1.plot.hist(grid=True, rwidth=0.9, color='#607c8e')
# plot_1.plot(grid=True)
# plt.title('Count Flat received Accum')
# plt.grid(axis='y', alpha=0.75)
#
# # plt.show()
#
# # plt.figure(3, figsize=(15, 10))
# #
# # plt.subplot(2,2,1)
# # plot_1 = pd.Series(results_cashflow_experiment)
# # plot_2 = pd.Series(results_cashflow_accum_experiment)
# # # plot_3 = pd.Series(results_accum_ALL_experiment)
# # # # plot_3 = pd.Series(c)
# # # plot_4 = pd.Series(results_funds_ready_to_spend_experiment)
# # # plot_5 = pd.Series(results_funds_spent_experiment)
# # plot_1.plot(grid=True)
# # plot_2.plot(grid=True)
# # # plot_3.plot(grid=True)
# # # plot_4.plot(grid=True)
# # # plot_5.plot.bar(grid=False)
# # plt.title('Cash Flow Accumulative')
# # plt.grid(axis='y', alpha=0.75)
# #
# # plt.subplot(2,2,2)
# # plot_1 = pd.Series(results_funds_ready_to_spend_experiment)
# # plot_2 = pd.Series(results_funds_spent_experiment)
# # plot_3 = pd.Series(results_cashflow_experiment)
# # plot_4 = pd.Series(results_cashflow_accum_experiment)
# #
# # plot_1.plot(grid=True)
# # plot_2.plot.bar(grid=False)
# # plot_3.plot(grid=True)
# # plot_4.plot(grid=True)
# # plt.title('Funds Ready to spend')
# # plt.grid(axis='y', alpha=0.75)
#
# plt.show()

print('Общее время работы алгоритма', timer(), 'сек') # печать времени работы алгоритма