from constants import *
from constants_columns import *
from functions_classes import *


def calc_user_utility (user_index, df):
    period_saving_i = df[column_period_saving][user_index]
    period_waiting_i = df[column_waiting_period][user_index] + df[column_prewaiting_period][user_index]
    total_amount_saving = df[column_total_amount_saving][user_index]
    monthly_amount_saving = total_amount_saving / period_saving_i
    base_deposit_j = total_amount_saving
    percent_saving_part = 0

    for j in range(period_saving_i):
        percent_j = base_deposit_j * j * BANK_PERCENT_MARKET/100/12
        # print('total_amount_saving', total_amount_saving, 'base_deposit_j', base_deposit_j, 'percent_j', percent_j, 'period_saving_i', period_saving_i, 'j', j)
        base_deposit_j -= monthly_amount_saving
        percent_saving_part += percent_j

    percent_waiting_part = total_amount_saving * period_waiting_i * BANK_PERCENT_MARKET / 100 / 12

    rank_user = percent_saving_part + percent_waiting_part

    return rank_user


def calc_annuity_payments_company(total_amount_payments, period_payments, percent_payments):
    annuity = BankInterest(total_amount_payments, period_payments, percent_payments).annuity_calc()

    return annuity



#
# def df_create_cash_flow_client (months_port, clients_portfolio):
#     columnss = []
#
#     for i in range(months_port + 1):
#         columnss.append(i + 1)
#     df = pd.DataFrame(0, index=np.arange(months_port), columns=columnss)
#
#     for i in range(count_sells):
#         cp = clients_portfolio[i]
#         for j in range(months_port + 1):
#             month_fact = j + cp.month_sell
#             if j < len(cp.payments):
#                 df.loc[i, month_fact] = cp.payments[j]
#             # print(len(cp.payments)+cp.month_sell
#     # print("Таблица (оглавление) (после добавления столбцов): \n", df.head(), "\n")
#     return df
#
# def df_create_cash_flow_seller(months_port, clients_portfolio):
#     columnss = []
#
#     for i in range(months_port + 1):
#         columnss.append(i + 1)
#     df = pd.DataFrame(0, index=np.arange(months_port), columns=columnss)
#
#     for i in range(count_sells):
#         cp = clients_portfolio[i]
#         for j in range(months_port + 1):
#             month_fact = j + cp.month_sell
#             if j < len(cp.payments_seller):
#                 df.loc[i, month_fact] = cp.payments_seller[j]
#             # print(len(cp.payments)+cp.month_sell
#     # print("Таблица (оглавление) (после добавления столбцов): \n", df.head(), "\n")
#     return df
#
#
# def df_create_cash_flow_bank (months_bank_port, months_port, clients_portfolio):
#     columnss = []
#
#     for i in range(months_port + 1):
#         columnss.append(i + 1)
#     df = pd.DataFrame(0, index=np.arange(months_port), columns=columnss)
#
#     for i in range(count_sells):
#         cp = clients_portfolio[i]
#         for j in range(months_bank_port + 1):
#             month_fact = j + cp.month_sell
#             if j < len(cp.payments_bank):
#                 df.loc[i, month_fact] = cp.payments_bank[j]
#             # print(len(cp.payments)+cp.month_sell
#     # print("Таблица (оглавление) (после добавления столбцов): \n", df.head(), "\n")
#     return df
#
#
# def month_sell_calc(order_num):
#     """Расчет месяца начала выплат. По сути это месяц первого платежа"""
#     count_sells_accumulative = count_sells_by_months[0]
#     month_number = 1
#
#     for i in range(order_num):
#         if i + 1 >= count_sells_accumulative:
#             count_sells_accumulative += count_sells_by_months[month_number]
#             month_number += 1
#     # print('номер месяца =', month_number)
#
#     return month_number
#
#
# def print_clients_portfolio (clients_portfolio):
#     print('Портфель клиентов: ', 'clients_portfolio')  # печать времени работы алгоритма
#     for i in range(len(clients_portfolio)):
#         cp = clients_portfolio[i]
#         # print(vars(clients_portfolio[i])) # печать всех аргументов каждого юнита клиента
#         print(cp.flat_by_room, 'r,',
#               cp.sum_flat, 'K,',
#               cp.period, 'm,',
#               cp.first_payment_perc, '%,',
#               cp.payment_first,'К,',
#               round(cp.payment_in_month, 3), '*', len(cp.payments) - 2 ,',',
#               round(- cp.payment_bank_in_month, 3), '*', len(cp.payments_bank) - 2 , ',',
#               round(sum(cp.payments), 3), 'К,',
#               round(- sum(cp.payments_bank), 3), 'К,',
#               'start', cp.month_sell, 'month')
#     return
