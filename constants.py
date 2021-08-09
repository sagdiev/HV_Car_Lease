GLOBAL_EXPERIMENT_NAME = 'exp_01_2021.07'

COUNT_EXPERIMENTS = 1  # К-во экспериментов

# Индикатор: Контролтируется ли модель через seed (ядро случайного выбора)
IS_RANDOM_CONTROLLED_BY_SEED = True  # Если "True" - контролируется, если "False" -модель абсолютно случайна

# Фиксатор seed (ядро случайного выбора) в случае, если IS_RANDOM_CONTROLLED_BY_SEED = True
RANDOM_SEED_START = 1

PERCENT_DISCOUNT_VEHICLE_FOR_COMPANY = 7  # Процент скидки на новое авто у Компании
PERCENT_FIRST_PAYMENT_VEHICLE_FOR_COMPANY = 28  # Процент первого платежя, который Компания вносит в Банк

DICT_Toyota_RAV = {
    'price'    : 42000,
    'cost_tires' : 17,
    'cost_tires_fitting': 7,
    'cost_TO'  : 33,
    'cost_cashflow_company_plan_list_without_discount': {
        'leasing': [],
    } ,
}

DICT_AUTO = {
    'Toyota RAV'    : DICT_Toyota_RAV,
    'Peugeot 3008'  : 32000}

DISCOUNT_AUTO_FOR_CONPANY = 7  # Процент скидки на авто у лизинговой компании

PERIOD_PAYMENTS = 36  # К-во периодов Платежей клиентов

GROSS_MARGIN = 40  # Процент заложенного зароботка на платеже в месяц

COUNT_PREPAYMENTS = 2  # К-во месячных платежей в качестве Залога

# Статусы Клиентов для таблиц
CLIENT_STATUS_START = 'start'
CLIENT_STATUS_PAYMENTS = 'saving'
CLIENT_STATUS_FINISHED = 'finished'

RANK_START = 1  # Рейтинг Клиента на старте


# # Типы Клиентов - желательно не менять самостоятельно
# CLIENT_TYPE_BY_SAVING_SIGN = \
#     ['10% + 40%',
#      '20% + 30%',
#      '30% + 20%',
#      '40% + 10%',
#      '50% + 0%']
#
# # Проценты у каждого типа Клиентов - желательно не менять самостоятельно
# CLIENT_TYPE_BY_SAVING_PAIR = \
#     [[10, 40],
#     [20, 30],
#     [30, 20],
#     [40, 10],
#     [50, 0 ]]   # пары первых выплат - пример, 10% готовы сразу, а 40% еще надо собирать

# Статусы Клиентов для таблиц
CLIENT_STATUS_BEFORE_START = 'before start'
CLIENT_STATUS_SAVING = 'saving'
CLIENT_STATUS_PREWAITING_FLAT = 'prewaiting flat'
CLIENT_STATUS_WAITING_FLAT = 'waiting flat'
CLIENT_STATUS_FLAT_RECEIVED = 'flat received'
CLIENT_STATUS_POSTPAYMENT = 'postpayment'
CLIENT_STATUS_FINISHED = 'finished'

# Распределение клиентов по типу (в сумме  должно равнятся 100)
# EXPERT_CLIENT_TYPE_BY_SAVING_PAIR_DISTR = [10, 15, 40, 20, 15]
# EXPERT_CLIENT_TYPE_BY_SAVING_PAIR_DISTR = [15, 25, 40, 20, 0]

EXPERT_CLIENT_TYPE_BY_SAVING_PAIR_DISTR = [5, 10, 40, 25, 20]

# Распределение периодов Накопления (в зависимости от Типа Клиента и Вектора вероятности)
EXPERT_PERIOD_SAVING_WEIGHTS = [10, 30, 60] # Вектор вероятности Распределение периодов Накопления
EXPERT_PERIOD_SAVING_OPTIONS_BY_CLIENT_TYPE = \
    [[36, 48, 60],
    [24, 36, 48],
    [12, 24, 36],
    [ 9, 12,  6],
    [ 9,  6,  3]]  # к-во месяцев Накопления - распределенеие периодов по типам клиентов

# Распределение периодов ПостОплат (в зависимости от Типа Клиента и Вектора вероятности)
EXPERT_PERIOD_POSTPAYMENT_WEIGHTS = [50, 30, 20] # Вектор вероятности Распределение периодов ПостОплат
EXPERT_PERIOD_POSTPAYMENT_OPTIONS_BY_CLIENT_TYPE = \
    [[60, 48, 36],
    [48, 36, 30],
    [42, 30, 24],
    [36, 24, 12],
    [24, 36, 60]]  # к-во месяцев ПостВыплат - распределенеие периодов по типам клиентов

# Распределение Стоимости Квартир (в зависимости от Типа Клиента и Матрицы вероятности)
EXPERT_FLAT_COST_OPTIONS = [35000, 50000, 75000, 100000]  # Варианты стоимостей квартир
EXPERT_FLAT_COST_WEIGHTS_BY_CLIENT_TYPE = \
    [[70, 20, 10, 0],
    [60, 25, 10, 5],
    [50, 30, 15, 5],
    [40, 30, 20, 10],
    [35, 30, 20, 15]]  # Матрица вероятности - распределенеие стоимостей квартир по типам клиентов


COUNT_SELLS_DICT_1 = {
    'y1q1': 7,
    'y1q2': 12,
    'y1q3': 17,
    'y1q4': 20,
    'y2':   25,
    'y3':   40,
    'y4':   40,
    'y5':   40
}

COUNT_SELLS_DICT_2 = {
    'y1q1': 5,
    'y1q2': 1,
    'y1q3': 0,
    'y1q4': 0,
    'y2': 0,
    'y3': 0,
    'y4': 0,
    'y5': 10
}


COUNT_SELLS_DICT_3 = {
    'y1q1': 1,
    'y1q2': 2,
    'y1q3': 2,
    'y1q4': 3,
    'y2': 5,
    'y3': 5,
    'y4': 5,
    'y5': 5
}

COUNT_SELLS_DICT = COUNT_SELLS_DICT_3  # Выбрать один из вариантов

y1_list = [COUNT_SELLS_DICT['y1q1']] * 3 + [COUNT_SELLS_DICT['y1q2']] * 3 \
        + [COUNT_SELLS_DICT['y1q3']] * 3 + [COUNT_SELLS_DICT['y1q4']] * 3
y2_list = [COUNT_SELLS_DICT['y2']] * 12
y3_list = [COUNT_SELLS_DICT['y3']] * 12
y4_list = [COUNT_SELLS_DICT['y4']] * 12
y5_list = [COUNT_SELLS_DICT['y5']] * 12

COUNT_SELLS_BY_MONTHS = y1_list + y2_list + y3_list + y4_list + y5_list  # Количество продаж по месяцам

print(COUNT_SELLS_BY_MONTHS)

# COUNT_SELLS_BY_MONTHS = COUNT_SELLS_BY_MONTHS_7  # Выбрать один из вариантов

# Дополнительное к-во месяцев для расчетов - Добавляется к месяцу привлечения последнего клиента - "Временной хвост"
COUNT_ADDITIONAL_MONTHS_CALC = 20

# Дополнительные расчеты констант
COUNT_SELLS = sum(COUNT_SELLS_BY_MONTHS)  # количество продаж за все время
COUNT_MONTHS_OF_SELLS = len(COUNT_SELLS_BY_MONTHS)  # количество месяцев
COUNT_MONTHS_OF_CALC = COUNT_MONTHS_OF_SELLS + COUNT_ADDITIONAL_MONTHS_CALC

# Соотношение Процентов в зависимости от Периода ПостВыплат
PERIOD_POSTPAYMENTS =  [  12,   24,   30,   36,   42,   48,   54,   60]  # периоды ПостВыплат в месяцах
PERCENT_POSTPAYMENTS = [3.75, 3.75, 4.08, 4.42, 4.75, 5.08, 5.42, 5.75]  # проценты для ПостВыплат в зависимости от периода

# Период Обязательного Ожидания до выдачи Квартиры
PERIOD_PREWAITING = 0

# Период Максимального Ожидания до выдачи Квартиры
PERIOD_WAITING_MAX_LIMIT = 6

PERCENT_SAVING = 50  # Все выплачивают 50% перед получение квартиры

# Средний оценочный годовой Процент депозитов - для подсчета рейтинга ожидания
BANK_PERCENT_MARKET = 10

SENSITIVITY_FLAT_COAST = 0  # у.е. чувствительности сравнения сумм Общих накоплений и Стоимости следующей квартиры
# необходимо для того, чтобы не "зависать" на дополнительные месяцы, хотя из-за округления сумма еще не набиралась - особенно на последних шагах

PATH_FOLDER = 'data_analytic'
PATH_FILE = 'exp'
PATH_FILE_UNIT_START = 'data_analytic/source/fact_clients_00.csv'

INCOME_ONBOARD_PAYMENT_PERCENT = 2.5  # Первый платеж - Оплата Вступительного взноса - 2,5%
INCOME_BUY_FLAT_PAYMENT_PERCENT = 5  # Платеж в момент Покупки Квртиры - 5%

INCOME_ADDITIONAL_DEPOSIT_PERCENT = 3.5  # Процент - Дополнительный заработок на привлеченном капитале
INCOME_FLAT_DISCOUNT_PERCENT = 1.5  # Процент - Зарадобок на Дисконте от квартир

COST_ADMIN = 500  # Административные затраты в месяц
COST_MARKETING_PERCENT = 2  # Процент - Маркетинговые затраты

COST_ONBOARD_PAYMENT_PERCENT = 1.5  # Процент - Единоразовый платеж за Сделку - Затраты в момент оформления Лизинга
COST_NOTARY_PERCENT = 0.5  # Процент - Нотариус - Затраты в момент оформления Лизинга
COST_TAX_PERCENT = 1.25  # Процент - Налоги Пенсионный фонд - Затраты в момент оформления Лизинга
COST_BANK_FEE_PERCENT = 0.5  # Процент - Банковские комиссии - Затраты в момент оформления Лизинга

BANK_PERCENT_FOR_FLAT = 1.5  # Затраты на Банковские Проценты за Квартиру

