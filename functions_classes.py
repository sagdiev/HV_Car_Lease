from constants import *
from constants_columns import *



class BankInterest():
    """Class contains two functions to calculate different interests for loans.
    Input parameters are loan amount, loan period in years, and interests on the loan.
    Example: 10000, 12, 18 => (916.8, 11001.6)
    Взято с https://www.prolinux.org/post/2013/01/pishem-kreditnyi-kalkulyator/ - там пояснения"""


    def __init__(self, amount, period, perc):
        self.amount = amount
        self.period = period
        self.perc = perc


    def annuity_calc(self):
        """Аннуитетная формула - Annuity formula"""
        period_annuity = self.period  # mp_cnt
        perc_month = self.perc / 12 / 100.0
        annuity_coef = (perc_month * (1 + perc_month) ** period_annuity) / (((1 + perc_month) ** period_annuity) - 1)
        annuity_payment = self.amount * annuity_coef
        annuity_total = annuity_payment * period_annuity
        credit_base_i = self.amount
        percent_amount_list = []
        credit_base_list = []
        credit_base_cover_list = []
        for i in range(period_annuity):
            percent_amount_i = credit_base_i * perc_month
            percent_amount_list.append(round(percent_amount_i, 2))  # Список процентов в этом месяце
            credit_base_cover_i = annuity_payment - percent_amount_i
            credit_base_cover_list.append(round(credit_base_cover_i, 2))  # Список Сумма базы кредита, которая выплачмвается в этом месяце
            credit_base_list.append(round(credit_base_i, 2))  # Список База на начало месяца (именно поэтому сначала добавление, а потом пересчет)
            credit_base_i = credit_base_i - annuity_payment + percent_amount_i

        return round(annuity_payment, 2), \
               round(annuity_total, 2), \
               percent_amount_list, \
               credit_base_cover_list, \
               credit_base_list


    def diff_calc(self):
        """Дифференциируемая формула - Differentiated formula"""
        arr = []
        mp_cnt = self.period
        rest = self.amount
        mp_real = self.amount / self.period
        while mp_cnt != 0:
            mp = mp_real + (rest * self.perc / 100)
            arr.append(round(mp, 3))
            rest = rest - mp_real
            mp_cnt = mp_cnt - 1
        return arr, round(sum(arr), 3), round(sum(arr), 3) - self.amount

