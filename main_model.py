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

# # папки и файлы
# path_folder = path_folder(PATH_FOLDER, GLOBAL_EXPERIMENT_NAME)
# create_folder_or_check_existence(path_folder)

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

            payment_monthly                 = price_auto_client / (1 - GROSS_MARGIN / 100)  # Размер платежа в месяц
            prepayment                      = payment_monthly * COUNT_PREPAYMENTS  # Размер Залога

            client_status                   = CLIENT_STATUS_START
            rank                            = RANK_START

            cashflow_client_plan            = [prepayment] + [payment_monthly] * ( period_payments - COUNT_PREPAYMENTS )


            annuity_pair                    = calc_annuity_payments_company(price_auto_company,
                                                                            period_payments,
                                                                            BANK_PERCENT_MARKET)
            cost_payments_auto_company_monthly      = annuity_pair[0]
            # total_amount_postpayments       = annuity_pair[1]
            # postpayment_percent_amount_list = annuity_pair[2]
            # credit_base_cover_list          = annuity_pair[3]
            # credit_base_list                = annuity_pair[4]

            cashflow_company_annuity_plan   = [cost_payments_auto_company_monthly] * 36
            cost_prepayment                 = price_auto_company * 25 / 100
            cost_payment_onboard            = price_auto_company * COST_ONBOARD_PAYMENT_PERCENT / 100
            cost_payment_notary             = price_auto_company * COST_NOTARY_PERCENT / 100
            cost_payment_tax                = price_auto_company * COST_TAX_PERCENT / 100
            cost_payment_bank               = price_auto_company * COST_BANK_FEE_PERCENT / 100

            cost_payment_company_in_first_period    = cost_prepayment + cost_payment_onboard \
                                                    + cost_payment_notary + cost_payment_tax + cost_payment_bank

            cashflow_company_plan           = [cost_payment_company_in_first_period] \
                                            + [cost_payments_auto_company_monthly] * 36  # TODO ИСПРАВИТЬ ПЕРВЫЙ МЕСЯЦ

            cashflow_client_fact            = []
            cashflow_company_fact           = []

            fair_value_auto_client          = price_auto_client
            fair_value_aut_company          = price_auto_company

            accum_payments_amount_client    = 0  # Накопленные платежи Клиента
            accum_payments_amount_company   = 0  # Накопленные платежи Компания

            # annuity_pair                    = BankInterest(
            #     total_amount_postpayments_base, period_postpayments, percent_postpayments).annuity_calc()
            # amount_postpayment_monthly      = annuity_pair[0]
            # total_amount_postpayments       = annuity_pair[1]
            # postpayment_percent_amount_list = annuity_pair[2]
            # credit_base_cover_list          = annuity_pair[3]
            # credit_base_list                = annuity_pair[4]

            df.loc[k, column_id_user]                           = id_user
            df.loc[k, column_auto_type]                         = auto_type
            df.loc[k, column_price_auto_client]                  = price_auto_client
            df.loc[k, column_price_auto_company]                 = price_auto_company
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

        cost_prepayment_t           = 0
        cost_payment_onboard_t      = 0
        cost_payment_notary_t       = 0
        cost_payment_tax_t            = 0
        cost_payment_bank_t           = 0


        # ВЫДАЧА АВТО ==========================================================================================================================
        ### ==================================================================================================================================

        for i in range(COUNT_SELLS):
            # print('i = ', i)

            period_payments_start_i         = df[column_period_payments_start][i]

            # _i = df[column_][i]

            if period_payments_start_i == t:
                id_user_i                   = df[column_id_user][i]
                client_status_i             = df[column_client_status][i]
                price_auto_client_i          = df[column_price_auto_client][i]
                price_auto_company_i         = df[column_price_auto_company][i]
                prepayment_i                = df[column_prepayment][i]
                # _i = df[column_][i]
                # _i = df[column_][i]

                print('START id_user_i = ', id_user_i)
                print('price_auto_client_i = ', price_auto_client_i)

                # Расчет Deal income и cost - поступления и затрат при оформлении Клиенту Лизинга
                income_payments_t           += 0
                income_prepayment_t         += prepayment_i

                cost_prepayment_t           += price_auto_company_i * 25 / 100
                cost_payment_onboard_t      += price_auto_company_i * COST_ONBOARD_PAYMENT_PERCENT / 100
                cost_payment_notary_t       += price_auto_company_i * COST_NOTARY_PERCENT / 100
                cost_payment_tax_t          += price_auto_company_i * COST_TAX_PERCENT / 100
                cost_payment_bank_t         += price_auto_company_i * COST_BANK_FEE_PERCENT / 100


                # COST_ADMIN = 500  # Административные затраты в месяц
                # COST_MARKETING_PERCENT = 2  # Процент - Маркетинговые затраты
                #
                # COST_REALTOR_PERCENT = 1.5  # Процент - Риелтор - Затраты в момент оформления Лизинга
                # COST_NOTARY_PERCENT = 0.5  # Процент - Нотариус - Затраты в момент оформления Лизинга
                # COST_TAX_PERCENT = 1.25  # Процент - Налоги Пенсионный фонд - Затраты в момент оформления Лизинга
                # COST_BANK_FEE_PERCENT = 0.5  # Процент - Банковские комиссии - Затраты в момент оформления Лизинга

            #
            # income_buy_payment_t        += cost_flat_l * INCOME_BUY_FLAT_PAYMENT_PERCENT / 100
            # income_discount_t            = cost_flat_l * INCOME_FLAT_DISCOUNT_PERCENT / 100
            # cost_buy_payment_realtor_t  += cost_flat_l * COST_REALTOR_PERCENT / 100
            # cost_buy_payment_notary_t   += cost_flat_l * COST_NOTARY_PERCENT / 100
            # cost_buy_payment_tax_t      += cost_flat_l * COST_TAX_PERCENT / 100
            # cost_buy_payment_bank_t     += cost_flat_l * COST_BANK_FEE_PERCENT / 100
            #
            # cf_income_total,
            # cf_income_client,
            # cf_income_payments,
            # cf_income_prepayment,
            # cf_income_add,
            # cf_cost_total,
            # cf_cost_payments,
            # cf_cost_prepayment,
            # cf_cost_payment_onetime,
            # cf_cost_payment_notary,
            # cf_cost_payment_tax,
            # cf_cost_payment_bank,
            # cf_cost_admin,
            # cf_cost_market,
            # cf_cashflow_net,
            # cf_cashflow_accum,
            # pl_income_total,
            # pl_expenses_total,
            # pl_profit_net,
            # pl_income_total_acc,
            # pl_expenses_total_acc,
            # pl_profit_net_acc]







            # period_payments_start = p


            # print('id_user_i = ', id_user_i)
            # print('price_auto_client_i = ', price_auto_client_i)


            # df.loc[k, column_id_user]                           = id_user
            # df.loc[k, column_auto_type]                         = auto_type
            # df.loc[k, column_price_auto_client]                  = price_auto_client
            # df.loc[k, column_price_auto_company]                 = price_auto_company
            # df.loc[k, column_period_payments]                   = period_payments
            # df.loc[k, column_period_payments_start]             = period_payments_start
            # df.loc[k, column_period_payments_uplaned_stop]      = period_payments_uplaned_stop
            # df.loc[k, column_payment_monthly]                   = payment_monthly
            # df.loc[k, column_prepayment]                        = prepayment
            # df.loc[k, column_client_status]                     = client_status
            # df.loc[k, column_rank]                              = rank
            # df.loc[k, column_cashflow_client_plan]              = cashflow_client_plan
            # df.loc[k, column_cashflow_company_plan]             = cashflow_company_plan
            # df.loc[k, column_cashflow_client_fact]              = cashflow_client_fact
            # df.loc[k, column_cashflow_company_fact]             = cashflow_company_fact
            # df.loc[k, column_fair_value_auto_client]            = fair_value_auto_client
            # df.loc[k, column_fair_value_aut_company]            = fair_value_aut_company
            # df.loc[k, column_accum_payments_amount_client]      = accum_payments_amount_client
            # df.loc[k, column_accum_payments_amount_company]     = accum_payments_amount_company








#
#
#
#         # # ПЕРЕВОД КЛИЕНТА В СТАТУТ ПОСТОПЛАТ В СЛУЧАЕ ПОЛУЧЕНИЯ КВАРТИРЫ В ПРЕДЫДУЩЕМ МЕСЯЦЕ
#         # for i in range(COUNT_SELLS):
#         #     client_status_i = df[column_client_status][i]
#         #     if client_status_i == CLIENT_STATUS_FLAT_RECEIVED:
#         #         df.loc[i, column_client_status]                 = CLIENT_STATUS_POSTPAYMENT
#         #         df.loc[i, column_period_postpayments_start]     = t
#
#         # # ШАГ ОПРЕДЕЛЕНИЯ РЕЙТИНГА
#         # ### ==================================================================================================================================
#         #
#         # rank_list = []
#         # waiting_list =[]
#         # for i in range(COUNT_SELLS):
#         #     client_status_i = df[column_client_status][i]
#         #     if client_status_i == CLIENT_STATUS_WAITING_FLAT:
#         #         # if df[column_waiting_period][i] < PERIOD_WAITING_MAX_LIMIT:
#         #         rank_i = round(calc_user_utility(i, df), 0)  #todo пересмотреть расчет процентов за период
#         #         df.loc[i, column_waiting_period]         = df[column_waiting_period][i] + 1
#         #         # else:
#         #         #     rank_i = 1
#         #         waiting_list.append(i)
#         #
#         #         if df[column_waiting_period][i] >= PERIOD_WAITING_MAX_LIMIT:  #  Определяем, обязаны ли выдать по Максимальному периоду ожидания
#         #             df.loc[i, column_waiting_max_status]  = 1
#         #
#         #     else:
#         #         rank_i = 0
#         #     rank_list.append(rank_i)
#         #     df.loc[i, column_rank] = rank_i
#         #
#         #
#         #
#         #     # print(i, 'client_status_i', client_status_i)
#         # # print('df[column_rank]', df[column_rank])
#         #
#         # rank_list_weight                    = [x / (max(rank_list)+1) for x in rank_list]
#         # rank_sum                            = sum(rank_list)
#         # # print('rank_list_weight', rank_list_weight)
#         # df_summary[column_waiting_list][t]  = waiting_list
#         # df_summary[column_rank_list][t]     = rank_list
#
#
#         # Новый шаг по ВЫДАЧЕ КВАРТИР
#         ### ==================================================================================================================================
#         # Механизм Выдачи квартиры - надо держать информацию о Сумме в Фонде на Квартиры
#
#         # print(t)
#         # print(df_summary[column_accum_savings_total][t])
#         funds_ready_to_spend_t  = df_summary[column_funds_ready_to_spend][t]
#         print('funds_ready_to_spend_t', funds_ready_to_spend_t)
#         funds_spent_t           = 0
#         cost_next_flat          = 0
#         l                       = True
#         id_receivers_step_list  = []
#         id_next                 = df_summary[column_id_next][t]
#
#
#         if rank_sum > 0:
#             indicatot_fund_spending = True  # Индикатораразрешающий тратить фонды в первой части, еще есть Фонды funds_ready_to_spend
#
#             while l is True:
#                 # определяем номер следующего клиента - с наибольшим рейтингом
#
#
#                 if df[column_rank].max() == 0:  # Отсекаем случай, если Оборотные есть, а в рейтинге никого
#                     indicatot_fund_spending = False
#                     print('indicatot_fund_spending', indicatot_fund_spending)
#                     # break
#                 else:
#                     id_user_first_order = \
#                         df.loc[(df[column_rank] == df[
#                             column_rank].max()).idxmax(), column_id_user]  # todo упростить idxmax
#
#                     print('id_user_first_order', id_user_first_order)
#                     cost_next_flat      = df[column_cost_vehicle][id_user_first_order]  # определяем стоимость квартиры следующего на очереди
#                     id_next             = id_user_first_order
#
#
#                 # ВЫДАЧА КВАРТИРЫ ==========================================================================================================================
#
#                 if indicatot_fund_spending is True and cost_next_flat <= funds_ready_to_spend_t + SENSITIVITY_FLAT_COAST:  # если хватает финансов в общем накопленном Фонде
#
#                     cost_flat_l = cost_next_flat
#                     funds_ready_to_spend_t -= cost_flat_l  # уменьшаем накопленных Фонд на сумму покупки квартиры дождавщемуся
#                     funds_spent_t += cost_flat_l
#                     print('funds_spent_t', funds_spent_t)
#                     df.loc[id_user_first_order, column_rank]                        = 0
#                     df.loc[id_user_first_order, column_accum_amount_saving_spent]   = \
#                         df[column_accum_amount_saving][id_user_first_order]  # записываем, что дождавщийся уже израсходовал все свои накопления
#                     df.loc[id_user_first_order, column_client_status]               = CLIENT_STATUS_FLAT_RECEIVED
#                     df.loc[id_user_first_order, column_flat_received]               = 1
#                     id_receivers_step_list.append(id_user_first_order)
#
#                     df.loc[id_user_first_order, column_waiting_max_status]          = 0
#
#                     # Расчет buy income и cost - поступления и затрат при покупке и оформлении Клиенту Квартиры
#                     income_buy_payment_t        += cost_flat_l * INCOME_BUY_FLAT_PAYMENT_PERCENT / 100  # Доп. платеж 5% при оформлении приобретения Квартиры
#                     income_discount_t            = cost_flat_l * INCOME_FLAT_DISCOUNT_PERCENT / 100  # Доп. выгода в виде Дисконта от приобретаемой Квартиры
#                     cost_buy_payment_realtor_t  += cost_flat_l * COST_REALTOR_PERCENT / 100
#                     cost_buy_payment_notary_t   += cost_flat_l * COST_NOTARY_PERCENT / 100
#                     cost_buy_payment_tax_t      += cost_flat_l * COST_TAX_PERCENT / 100
#                     cost_buy_payment_bank_t     += cost_flat_l * COST_BANK_FEE_PERCENT / 100
#
#                 elif indicatot_fund_spending is False or cost_next_flat > funds_ready_to_spend_t + SENSITIVITY_FLAT_COAST:
#                     # Перебираем всех оставщихся с Максимальным уровнем Ожидания
#                     # (только оставшиеся после первой процедуры
#                     print('Проверка на Mаx Waiting')
#                     for u in range(COUNT_SELLS):
#                         if df[column_waiting_max_status][u] == 1:
#                             print('Проверка на Mаx Waiting - подтвержден клиент с Макс Вейтингом', u)
#                             cost_flat_l                                     = df[column_cost_vehicle][u]
#                             funds_ready_to_spend_t                         -= cost_flat_l  # уменьшаем накопленных Фонд на сумму покупки квартиры дождавщемуся
#                             funds_spent_t                                  += cost_flat_l
#                             print('funds_spent_t', funds_spent_t)
#                             df.loc[u, column_rank]                          = 0
#                             df.loc[u, column_accum_amount_saving_spent]     = df[column_accum_amount_saving][u]  # записываем, что дождавщийся уже израсходовал все свои накопления
#                             df.loc[u, column_client_status]                 = CLIENT_STATUS_FLAT_RECEIVED
#                             df.loc[u, column_flat_received]                 = 1
#                             id_receivers_step_list.append(u)
#
#                             df.loc[u, column_waiting_max_status] = 0
#
#                             # Расчет buy income и cost - поступления и затрат при покупке и оформлении Клиенту Квартиры
#                             income_buy_payment_t        += cost_flat_l * INCOME_BUY_FLAT_PAYMENT_PERCENT / 100  # Доп. платеж 5% при оформлении приобретения Квартиры
#                             income_discount_t            = cost_flat_l * INCOME_FLAT_DISCOUNT_PERCENT / 100  # Доп. выгода в виде Дисконта от приобретаемой Квартиры
#                             cost_buy_payment_realtor_t  += cost_flat_l * COST_REALTOR_PERCENT / 100
#                             cost_buy_payment_notary_t   += cost_flat_l * COST_NOTARY_PERCENT / 100
#                             cost_buy_payment_tax_t      += cost_flat_l * COST_TAX_PERCENT / 100
#                             cost_buy_payment_bank_t     += cost_flat_l * COST_BANK_FEE_PERCENT / 100
#
#                             df.loc[u, column_waiting_max_status] = 0
#
#                         l = False # Выходим з цикла после записи всех полей
#                 else:
#
#                     l = False # Выходим з цикла после записи всех полей
#         else:
#             id_next = 'NaN'
#
#         df_summary.loc[t, column_id_receivers_step_list]    = id_receivers_step_list
#         df_summary.loc[t, column_funds_spent]               = funds_spent_t
#         if t > 0:
#             funds_spent_total   = df_summary[column_funds_spent_total][t - 1] + funds_spent_t
#         else:
#             funds_spent_total   = funds_spent_t
#         df_summary.loc[t, column_funds_spent_total] = funds_spent_total
#         # print('df_summary[column_funds_spent_total][t]', t, df_summary[column_funds_spent_total][t])
#
#
#         # Новый шаг по НАКОПЛЕНИЯМ
#         ### ==================================================================================================================================
#
#         for i in range(COUNT_SELLS):
#             client_status_i         = df[column_client_status][i]
#             period_saving_start_i   = df[column_period_saving_start][i]
#             period_saving_i         = df[column_period_saving][i]
#             period_prewaiting_i     = df[column_prewaiting_period][i]
#
#             # print('status:', client_status_i, '| from', period_saving_start_i, 'period_saving', period_saving_i)
#
#             if client_status_i == CLIENT_STATUS_BEFORE_START:
#                 if period_saving_start_i == t: # самый Первый платеж
#                     amount_saving_i                         = df[column_amount_saving_monthly][i]
#                     df.loc[i, column_accum_amount_saving]   = amount_saving_i
#                     df.loc[i, column_client_status]         = CLIENT_STATUS_SAVING
#                     # расчет Вступительного взноса Клиента в начале стадии Накопления
#                     income_onboard_payment_t               += df[column_cost_vehicle][i] * \
#                                                               INCOME_ONBOARD_PAYMENT_PERCENT / 100
#                     cost_market_t                           = df[column_cost_vehicle][i] * COST_MARKETING_PERCENT / 100
#                     amount_saving_t                        += amount_saving_i
#
#             if client_status_i == CLIENT_STATUS_SAVING:
#                 if period_saving_start_i + period_saving_i > t: # Случай Накопления
#                     amount_saving_i                         = df[column_amount_saving_monthly][i]
#                     df.loc[i, column_accum_amount_saving]   = round(df[column_accum_amount_saving][i] +
#                                                                     amount_saving_i, 2)
#                     amount_saving_t                         += amount_saving_i
#                 else:
#                     # df.loc[i, column_client_status] = CLIENT_STATUS_WAITING_FLAT
#                     df.loc[i, column_client_status]         = CLIENT_STATUS_PREWAITING_FLAT
#
#             # Новый шаг по переходу с ПРЕОЖИДАНИЯ на ОЖИДАЖИЕ
#             ### ==================================================================================================================================
#
#             if client_status_i == CLIENT_STATUS_PREWAITING_FLAT:
#                 if period_prewaiting_i < PERIOD_PREWAITING:
#                     df.loc[i, column_prewaiting_period]   += 1
#                 else:
#                     df.loc[i, column_client_status]        = CLIENT_STATUS_WAITING_FLAT
#
#             # print(df[column_total_amount_saving][i], df[column_accum_amount_saving][i])
#
#
#
#
#         # Новый шаг по ПОСТВЫПЛАТАМ
#         ### ==================================================================================================================================
#
#         for i in range(COUNT_SELLS):
#             client_status_i                 = df[column_client_status][i]
#             period_postpayments_start_i     = df[column_period_postpayments_start][i]
#             period_postpayments_i           = df[column_period_postpayments][i]
#
#             if client_status_i == CLIENT_STATUS_POSTPAYMENT:
#                 if period_postpayments_start_i == t:  # Первая ПостВыплата
#                     amount_postpayment_i                        = df[column_amount_postpayment_monthly][i]
#                     amount_postpayment_percent_i                = df[column_postpayment_percent_amount_list][i][0]
#                     amount_postpayment_base_cover_i             = df[column_credit_base_cover_list][i][0]
#                     cost_bank_percent_i                         = df[column_credit_base_list][i][0] * \
#                                                                   BANK_PERCENT_FOR_FLAT / 12 /  100
#                     df.loc[i, column_accum_amount_postpayments] = round(amount_postpayment_i, 2)
#                     # print('Старт column_accum_amount_postpayments', amount_postpayment_i)
#                     amount_postpayments_t                      += amount_postpayment_i
#                     amount_postpayment_percent_t               += amount_postpayment_percent_i
#                     amount_postpayment_base_cover_t            += amount_postpayment_base_cover_i
#                     cost_bank_percent_t                        += cost_bank_percent_i
#
#                 elif period_postpayments_start_i + period_postpayments_i > t:  # Случай ПостВыплат
#                     pp_time                                     = t - period_postpayments_start_i
#                     amount_postpayment_i                        = df[column_amount_postpayment_monthly][i]
#                     amount_postpayment_percent_i                = df[column_postpayment_percent_amount_list][i][pp_time]
#                     amount_postpayment_base_cover_i             = df[column_credit_base_cover_list][i][pp_time]
#                     cost_bank_percent_i                         = df[column_credit_base_list][i][pp_time] * \
#                                                                   BANK_PERCENT_FOR_FLAT / 12 / 100
#                     accum_amount_postpayments_pending           = df[column_accum_amount_postpayments][i]
#                     df.loc[i, column_accum_amount_postpayments] = accum_amount_postpayments_pending + \
#                                                                   amount_postpayment_i
#                     # print('accum_amount_postpayments_pending', accum_amount_postpayments_pending, '=>', df[column_accum_amount_postpayments][i])
#                     amount_postpayments_t                      += amount_postpayment_i
#                     amount_postpayment_percent_t               += amount_postpayment_percent_i
#                     amount_postpayment_base_cover_t            += amount_postpayment_base_cover_i
#                     cost_bank_percent_t                        += cost_bank_percent_i
#
#                 else:
#                     df.loc[i, column_client_status]             = CLIENT_STATUS_FINISHED
#
#
#         # Подсчет СВОДНОЙ ИНФОРМАЦИИ ПО КЛИЕНТАМ в одном эксперименте
#         ## ==================================================================================================================================
#
#         mean_value          = lambda x: mean(list(x))
#         percent_value       = lambda x: round(x.count() / COUNT_SELLS * 100, 2)
#
#         agg_funcs = \
#             {column_id_user:                ['size', percent_value],
#              column_cost_vehicle:              [mean_value, 'min', 'max'],
#              column_period_saving:          [mean_value, 'min', 'max'],
#              column_period_postpayments:    [mean_value, 'min', 'max'],
#              column_percent_postpayments:   [mean_value, 'min', 'max'],
#              column_waiting_period:         [mean_value, 'min', 'max']}
#
#         df_unit_sort                    = df.groupby(column_client_type, as_index=False).agg(agg_funcs)
#         client_type_recent_list         = df_unit_sort[column_client_type].tolist()
#         df_unit_sort.sort_values(column_client_type)
#         df_unit_sort.insert(3, column_client_type_plan, 0)
#         for s in range(len(df_unit_sort)):
#             for r in CLIENT_TYPE_BY_SAVING_SIGN:
#                 if client_type_recent_list[s] == r:
#                     df_unit_sort.loc[s, column_client_type_plan] = EXPERT_CLIENT_TYPE_BY_SAVING_PAIR_DISTR[
#                         CLIENT_TYPE_BY_SAVING_SIGN.index(r)]
#         print(df_unit_sort.to_string())
#
#
#         # Подсчет ИСХОДЯЩИХ САЛЬДО по общим фондам
#         ### ==================================================================================================================================
#
#         accum_amount_saving         = df[column_accum_amount_saving].sum()
#         accum_amount_postpayments   = df[column_accum_amount_postpayments].sum()
#         accum_ALL                   = accum_amount_saving + accum_amount_postpayments
#
#         count_flat_received         = df.loc[(df[column_flat_received] == 1), column_flat_received].sum()
#         count_waiting               = df.loc[(df[column_client_status] ==
#                                               CLIENT_STATUS_WAITING_FLAT), column_client_status].count()
#
#         if t == 0:
#             income_add_percent_t  = 0
#         else:
#             income_add_percent_t  = df_cashflow[cf_cashflow_accum][t - 1] * INCOME_ADDITIONAL_DEPOSIT_PERCENT / 12 / 100  # Пополнительный процент на остаток
#
#         income_client_t                         = amount_saving_t + \
#                                                   amount_postpayments_t + \
#                                                   income_onboard_payment_t + \
#                                                   income_buy_payment_t
#
#         income_postpayments_percent_t           = amount_postpayment_percent_t
#         income_postpayments_body_recover_t      = amount_postpayment_base_cover_t
#
#         # income_discount_t = 0
#         income_add_t                    = income_add_percent_t + income_discount_t
#         income_total_t                  = income_client_t + income_add_t
#
#         cost_buy_payment_t              = cost_buy_payment_realtor_t + \
#                                           cost_buy_payment_notary_t + \
#                                           cost_buy_payment_tax_t + \
#                                           cost_buy_payment_bank_t
#
#         cost_admin_t                    = COST_ADMIN
#         cost_total_t                    = cost_buy_payment_t + \
#                                           cost_bank_percent_t + \
#                                           funds_spent_t + \
#                                           cost_admin_t + \
#                                           cost_market_t
#
#         cashflow_net_t                  = income_total_t - cost_total_t
#         cashflow_accum_buttom_t         = cashflow_accum_t - cost_total_t  # дно остатков
#         cashflow_accum_t               += cashflow_net_t
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
#
#         df_cashflow.loc[t, cf_income_savings]                       = round(amount_saving_t, 0)
#         df_cashflow.loc[t, cf_income_postpayments]                  = round(amount_postpayments_t, 0)
#         df_cashflow.loc[t, cf_income_postpayments_percent]          = round(income_postpayments_percent_t, 0)
#         df_cashflow.loc[t, cf_income_postpayments_body_recover]     = round(income_postpayments_body_recover_t, 0)
#         df_cashflow.loc[t, cf_income_onboard_payment]               = round(income_onboard_payment_t, 0)
#         df_cashflow.loc[t, cf_income_buy_payment]                   = round(income_buy_payment_t, 0)
#
#         df_cashflow.loc[t, cf_income_add_percent]                   = round(income_add_percent_t, 0)
#         df_cashflow.loc[t, cf_income_discount]                      = round(income_discount_t, 0)
#
#         df_cashflow.loc[t, cf_income_client]                        = round(income_client_t, 0)
#         df_cashflow.loc[t, cf_income_add]                           = round(income_add_t, 0)
#         df_cashflow.loc[t, cf_income_total]                         = round(income_total_t, 0)
#
#         df_cashflow.loc[t, cf_cost_buy_payment_total]               = round(-cost_buy_payment_t, 0)
#         df_cashflow.loc[t, cf_cost_buy_payment_realtor]             = round(-cost_buy_payment_realtor_t, 0)
#         df_cashflow.loc[t, cf_cost_buy_payment_notary]              = round(-cost_buy_payment_notary_t, 0)
#         df_cashflow.loc[t, cf_cost_buy_payment_tax]                 = round(-cost_buy_payment_tax_t, 0)
#         df_cashflow.loc[t, cf_cost_buy_payment_bank]                = round(-cost_buy_payment_bank_t, 0)
#         df_cashflow.loc[t, cf_cost_bank_percent]                    = round(-cost_bank_percent_t, 0)
#         df_cashflow.loc[t, cf_cost_flat]                            = round(-funds_spent_t, 0)
#         df_cashflow.loc[t, cf_cost_admin]                           = round(-cost_admin_t, 0)
#         df_cashflow.loc[t, cf_cost_market]                          = round(-cost_market_t, 0)
#
#         df_cashflow.loc[t, cf_cost_total]                           = round(-cost_total_t, 0)
#
#         df_cashflow.loc[t, cf_cashflow_net]                         = round(cashflow_net_t, 0)
#         df_cashflow.loc[t, cf_cashflow_accum_buttom]                = round(cashflow_accum_buttom_t, 0)
#         df_cashflow.loc[t, cf_cashflow_accum]                       = round(cashflow_accum_t, 0)
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

        df_cashflow.loc[t, cf_cost_prepayment]                      = round(-cost_prepayment_t, 0)
        df_cashflow.loc[t, cf_cost_payment_onboard]                 = round(-cost_payment_onboard_t, 0)
        df_cashflow.loc[t, cf_cost_payment_notary]                  = round(-cost_payment_notary_t, 0)
        df_cashflow.loc[t, cf_cost_payment_tax]                     = round(-cost_payment_tax_t, 0)
        df_cashflow.loc[t, cf_cost_payment_bank]                    = round(-cost_payment_bank_t, 0)

        # income_payments_t           = 0
        # income_prepayment_t         = 0
        #
        # cost_prepayment_t           = 0
        # cost_payment_onboard_t      = 0
        # cost_payment_notary_t       = 0
        # cost_payment_tax            = 0
        # cost_payment_bank           = 0

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
#
#     # # Запись в файл CF результатов эксперимента
#     # path_file_j = path_file(path_folder + 'units', j + 1)  # файл экспериманта j
#     # file_clear(path_file_j)
#     # df.to_csv(path_file_j, sep=',', index=False, )
#     # print("Файл создан: ", path_file_j)
#     #
#     # path_file_j = path_file(path_folder + 'summary', j + 1)  # файл экспериманта j
#     # file_clear(path_file_j)
#     # df_summary.to_csv(path_file_j, sep=',', index=False, )
#     # print("Файл создан: ", path_file_j)
#     #
#     # path_file_j = path_file(path_folder + 'cashflow', j + 1)  # файл экспериманта j
#     # file_clear(path_file_j)
#     # df_cashflow.to_csv(path_file_j, sep=',', index=False, )
#     # print("Файл создан: ", path_file_j)
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