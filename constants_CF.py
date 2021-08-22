
# CASH FLOW ПОСТУПЛЕНИЯ

cf_period = 'Period'
cf_date = 'Date'

cf_income_total = 'Income Total'

cf_income_client = 'Income Client'

cf_income_payments = "Income Payments"  # Выплаты Клиента
cf_income_prepayment = "Income PrePayments"  # Залог Клиента

# cf_income_onboard_payment = "FP 2.5%"  # Первый платеж - Оплата Вступительного взноса - 2,5%
# cf_income_buy_payment = "BP 5%"  # Платеж в момент Покупки Квртиры - 5%

cf_income_add = 'Income Add'

# cf_income_add_percent = "AP"  # Дополнительны проценты - Дополнительный заработок на привлеченном капитале
# cf_income_discount = "D"  # Зарадобок на Дисконте от квартир

# CASH FLOW ВЫПЛАТЫ

cf_cost_total = 'Cost Total'

cf_cost_payments = 'Cost Payments'  # Лизинговый Ежемесячный Платеж - Затраты ежемесячные по компенсациии Лизинга
cf_cost_prepayment = 'Cost First Payments'  # Первый Платеж по Лизингу - Затраты в момент оформления Лизинга
cf_cost_payment_insurance = 'Cost Insurance'  # Страхование авто Компанией
cf_cost_payment_onboard = 'Cost onboard'  # Единоразовая оплата сделки % - Затраты в момент оформления Лизинга
cf_cost_payment_notary = 'Cost Notary'  # Нотариус - Затраты в момент оформления Лизинга
cf_cost_payment_tax = 'Cost Tax'  # Налоги Пенсионный фонд - Затраты в момент оформления Лизинга
cf_cost_payment_bank_deal = 'Cost Bank deal'  # Банковские услуги - Затраты в момент оформления Лизинга

cf_cost_tires = 'Cost Tires'
cf_cost_tires_fitting = 'Cost Tires Fitting'
cf_cost_TO = 'Cost TO'

cf_cost_payment_credit_line_percents = 'Cost Bank Credit Line'  #Затраты на банковские проценты по Кредитной линии

# cf_cost_bank_percent = 'BPC 1.5%'  # Затраты на Банковские Проценты
# cf_cost_flat = 'FlatC'  # Затраты на приобретение Квартиры

cf_cost_admin = 'AC'  # Административные затраты
cf_cost_market = 'MC'  # Маркетинговые затраты

cf_cost_buy_total = 'Cost Buy Total'

cf_cashflow_net = 'CashFlow Net'  # Суммарное Движение денег за период
cf_cashflow_accum_buttom = 'CashFlow Buttom'  # Дно остатков в период
cf_cashflow_accum = 'CashFlow Accum'  # Суммарное Движение денег за период

pl_income_total = 'P&L Income'
pl_expenses_total = 'P&L Expenses'
pl_profit_net = 'P&L Net Profit'

pl_income_total_acc = 'P&L Income Acc'
pl_expenses_total_acc = 'P&L Expenses Acc'
pl_profit_net_acc = 'P&L Net Profit Acc'

bl_credit_line = "BL Credit Line"  #Остаток (баланс) обязанности по Кредитной линии

COLUMN_CASH_FLOW = [
    cf_period,
    cf_date,
    cf_income_total,
    cf_income_client,
    cf_income_payments,
    cf_income_prepayment,
    cf_income_add,
    cf_cost_total,
    cf_cost_payments,
    cf_cost_prepayment,
    cf_cost_payment_onboard,
    cf_cost_payment_notary,
    cf_cost_payment_tax,
    cf_cost_payment_bank_deal,
    cf_cost_payment_credit_line_percents,
    cf_cost_admin,
    cf_cost_market,
    cf_cashflow_net,
    cf_cashflow_accum,
    pl_income_total,
    pl_expenses_total,
    pl_profit_net,
    pl_income_total_acc,
    pl_expenses_total_acc,
    pl_profit_net_acc,
    bl_credit_line]


