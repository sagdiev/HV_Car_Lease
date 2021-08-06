
# Названия Колонок для одного Эксперимента - UNIT - каждая строка = один клиент

column_id_user = 'ID User'
column_client_type = 'Type'

column_cost_vehicle_client = 'Cost Vehicle Client'
column_cost_vehicle_company = 'Cost Vehicle Company'

column_period_payments = 'Payments'  # Общий плановый период Выплат
column_period_payments_start = 'Period Payments Start'  # Номер месяца начала Выплат



column_period_saving = 'Period Saving'  # Общий плановый период накоплений
column_period_saving_start = 'Period Saving Start'  # Номер месяца начала накоплений
column_amount_saving_monthly = 'Saving Monthly'  # Накопления в месяц
column_amount_percent_saving_monthly = 'Percent Monthly'  # Проценты Накопления в месяц
column_total_amount_saving = 'Saving Total'  # Общая плановая сумма накоплений
column_accum_amount_saving = 'Saving Accumulated'  # Сумма собранных накоплений
column_accum_amount_saving_spent = 'Saving Spent'  # Сумма уже израсходованных накоплений

column_prewaiting_period = 'PreWaiting'  # Период фиксированного ожидания
column_waiting_period = 'Waiting'  # Период ожидания между концом накопления и получением квартиры
column_waiting_max_status = 'Status Max Waiting'  # Временный Индикатор ожиданни в "красной зоне" после Максимального периода

column_flat_received = 'Is Flat'  # Получена ли Квартира. 1 - получена, 0 - еще нет

column_period_postpayments = 'PostPayments'
column_period_postpayments_start = 'Period PostPayments Start'  # Номер месяца начала ПостВыплат

column_percent_postpayments = 'Percent PostPayments'
column_amount_postpayment_monthly = 'Postpayment Monthly'  # Ежемесячный платеж Поствыплат

column_total_amount_postpayments_base = 'PostPayments Total Base'  # База Кредита ПостВыплаты
column_accum_amount_postpayments = 'Postpayment Accumulated'
column_total_amount_postpayments = 'PostPayments Total'

column_postpayment_percent_amount_list = 'Annuity PostPayment Percent Amount List'  # Проценты по Аннуитету
column_credit_base_cover_list = 'Annuity Credit Base Cover'  # Покрываемая Сумма тела Кредита в конкретный месяц
column_credit_base_list = 'Annuity Credit Base'  # База Кредита ПостПеймента по Аннуитету

column_rank = 'Rank'
column_client_status = 'Status'
column_cashflow = 'Unit CashFlow'

COLUMN_UNIT_NAMES = [
    column_id_user,
    column_client_type,
    column_cost_vehicle,
    column_period_saving,
    column_period_saving_start,
    column_amount_saving_monthly,
    column_total_amount_saving,
    column_accum_amount_saving,
    column_accum_amount_saving_spent,
    column_prewaiting_period,
    column_waiting_period,
    column_waiting_max_status,
    column_flat_received,
    column_period_postpayments,
    column_period_postpayments_start,
    column_percent_postpayments,
    column_total_amount_postpayments_base,
    column_amount_postpayment_monthly,
    column_accum_amount_postpayments,
    column_total_amount_postpayments,
    column_rank,
    column_client_status,
    column_cashflow,
    column_postpayment_percent_amount_list,
    column_credit_base_cover_list,
    column_credit_base_list]

column_client_type_plan = 'Type Plan'

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

