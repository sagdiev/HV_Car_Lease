
# Названия Колонок для одного Эксперимента - Client - каждая строка = один клиент

column_id_user = 'ID User'
# column_client_type = 'Client Type'
column_auto_type = 'Auto Type'

column_price_auto_client = 'Price Auto Client'
column_price_auto_company = 'Price Auto Company'

column_period_payments = 'Period Payments'  # Общий плановый период Выплат
column_period_payments_start = 'Period Payments Start'  # Номер месяца начала Выплат
column_date_payments_start = 'Date Payments Start' # Дата начала Выплат (начало месяца)
column_period_payments_uplaned_stop = 'Period Payments Uplaned Stop'  # Номер месяца незапланированной остановки

column_payment_monthly = 'Payments Monthly'  # Размер платежа в месяц
column_prepayment = 'Prepayment'  # Размер Залога

column_client_status = 'Status'
column_rank = 'Rank'

column_cashflow_client_plan = 'CashFlow Client Plan'
column_cashflow_company_plan = 'CashFlow Company Plan'

column_cashflow_client_fact = 'CashFlow Client Fact'
column_cashflow_company_fact = 'CashFlow Company Fact'

column_fair_value_auto_client = 'Fair Value Client'
column_fair_value_aut_company = 'Fair Value Company'

column_accum_payments_amount_client = 'Payments Accumulated Client'  # Накопленные платежи Клиента
column_accum_payments_amount_company = 'Payments Accumulated Company'  # Накопленные платежи Компания


COLUMN_UNIT_NAMES = [
    column_id_user,
    # column_client_type,
    column_auto_type,
    column_price_auto_client,
    column_price_auto_company,
    column_period_payments,
    column_period_payments_start,
    column_date_payments_start,
    column_period_payments_uplaned_stop,
    column_payment_monthly,
    column_prepayment,
    column_client_status,
    column_rank,
    column_fair_value_auto_client,
    column_fair_value_aut_company,
    column_accum_payments_amount_client,
    column_accum_payments_amount_company,
    column_cashflow_client_plan,
    column_cashflow_company_plan,
    column_cashflow_client_fact,
    column_cashflow_company_fact]


# Названия Колонок для одного Эксперимента - UNITS_SUMMARY - каждая строка = один месяц совместного ивестирования

column_accum_savings_total = 'Savings Accumulated Funds'  # Накопленные Фонды на закупку Квартир - Общая сумма за все время
column_funds_ready_to_spend = 'Funds Ready to Spend'  # Фонд готовый для закупки Квартир - входящее сальдо такого фонда
column_funds_spent = 'Funds Spent'  # Фонд потраченный на звкупку Квартир на конкретном шаге
column_funds_spent_total = 'Funds Spent Total'  # Фонды направленные на закупку Квартир за все время

column_cost_next_flat = 'Next Flat'  # Стоимость следующей квартиры в очереди
column_id_next = 'Next ID'  # Стоимость следующей квартиры в очереди
column_id_receivers_step_list = 'Receivers List'

column_count_flat_received = 'Flat Received'
column_count_waiting = 'Waiting Count'
column_waiting_list = 'Waiting List'
column_rank_list = 'Rank List SUM'

column_accum_amount_postpayments_total = 'Postpayment Accumulated Total'
column_accum_ALL = 'Accumulated ALL'  # Accumulated Funds + Postpayment Accumulated Total

COLUMN_UNITS_SUMMARY_NAMES = [
    column_accum_savings_total,
    column_accum_amount_postpayments_total,
    column_accum_ALL,
    column_funds_ready_to_spend,
    column_funds_spent,
    column_funds_spent_total,
    column_cost_next_flat,
    column_id_next,
    column_id_receivers_step_list,
    column_count_flat_received,
    column_count_waiting,
    column_waiting_list,
    column_rank_list]


# Названия Колонок для всех Экспериментов - Сбор результатов Эксперимента в виде Строки

column_id_experiment = 'ID Experiment'

column_accum_ALL = 'Accumulated ALL'  # Accumulated Funds + Postpayment Accumulated Total
column_funds_spent_total = 'Funds Spent Total'  # Фонды направленные на закупку Квартир за все время

column_max_waiting_period = 'MAX Waiting Period'
column_max_waiting_count = 'MAX Waiting Count'

COLUMN_EXPERIMENTS_NAMES = [
    column_id_experiment,
    column_accum_ALL,
    column_funds_spent_total,
    column_max_waiting_period,
    column_max_waiting_count]


# Названия Колонок для всех Экспериментов - Сводный результат всех Экспериментов

COLUMN_EXPERIMENTS_RESULT_NAMES = []

# Названия Колонок для таблички сравнения фактических рузультатов выборки с плановыми по Типу Клиентов

column_percent_client_type_plan = 'Percent Client Type Plan'
column_percent_client_type_fact = 'Percent Client Type Fact'

COLUMN_RESULT_CLIENT_NAMES = [
    column_percent_client_type_plan,
    column_percent_client_type_fact]

