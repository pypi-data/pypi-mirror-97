# 统计基金表现的def

import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine
import pymysql
from hbshare.quant.load_data import load_funds_data

pymysql.install_as_MySQLdb()


def ret(data_df):
    funds = data_df.columns.tolist()
    date_col = 't_date'
    if 't_date' in funds:
        funds.remove(date_col)
    elif '日期' in funds:
        date_col = '日期'
        funds.remove('日期')

    result_all = data_df['t_date']

    for i in funds:
        single_df = data_df[[date_col, i]].copy()
        single_df['ret'] = single_df[i] / single_df[i].shift(1) - 1

        result_all = pd.merge(result_all, single_df[['t_date', 'ret']], on='t_date').rename(columns={'ret': i})

    return result_all


# 计算每只产品的年化收益，年华波动，夏普，最大回撤等指标
def performance_analysis(
        data_df,
        risk_free=0.015,
        start_date=datetime(2019, 1, 1).date(),
        end_date=datetime(2099, 12, 31).date(),
        ret_num_per_year=52,
        monthly_funds=None
):

    if monthly_funds is None:
        monthly_funds = []
    funds = data_df.columns.tolist()
    date_col = 't_date'
    if 't_date' in funds:
        funds.remove(date_col)
    elif '日期' in funds:
        date_col = '日期'
        funds.remove('日期')
    # data_df['ret'] = data_df['nav'] / data_df['nav'].shift(1)

    result_all = pd.DataFrame()
    dd_all = data_df[[date_col]].copy()
    ret_all = data_df[[date_col]].copy()
    for i in funds:
        single_df = data_df[[date_col, i]]
        data_before = single_df[single_df[date_col] < start_date][date_col].tolist()
        if len(data_before) > 0:
            start_date_lag1 = data_before[-1]
        else:
            start_date_lag1 = start_date
        single_df = single_df[
            np.array(single_df[date_col] >= start_date_lag1) & np.array(single_df[date_col] <= end_date)
            ].reset_index(drop=True)

        single_data = single_df[single_df[i] > 0]
        if len(single_data) > 1:
            print('\t计算 ' + i + ' 指标')
            start_index = single_data.index[0]
            single_df = single_df.iloc[start_index:].reset_index(drop=True)

            # 剔除最新净值之后的空置（若产品最新净值未按时更新）
            single_df = single_df[single_df[i] > 0].reset_index(drop=True)

            single_df['ret'] = single_df[i] / single_df[i].shift(1) - 1
            single_df['highest'] = single_df[i].cummax()
            single_df['dd'] = (single_df[i] - single_df['highest']) / single_df['highest']
            max_dd = min(single_df['dd'])

            fund_last_days = single_df[date_col][len(single_df) - 1] - single_df[date_col][0]
            annualized_return = (single_df[i][len(single_df) - 1] / single_df[i][0]) ** (365 / fund_last_days.days) - 1
            annualized_return_mean = np.mean(single_df['ret'][1:] + 1) ** ret_num_per_year - 1  # 复利年化
            annualized_return_mean_simple = np.mean(single_df['ret'][1:]) * ret_num_per_year
            annualized_vol = np.std(single_df['ret'][1:], ddof=1) * np.sqrt(ret_num_per_year)

            single_df['downside_risk'] = single_df['ret'] #- risk_free
            single_df.loc[
                single_df['downside_risk'] > ((1 + risk_free) ** (1 / ret_num_per_year) - 1),
                'downside_risk'
            ] = 0
            downside_vol = np.std(single_df['downside_risk'][1:], ddof=1) * np.sqrt(ret_num_per_year)
            sharpe = (annualized_return - risk_free) / annualized_vol
            if downside_vol != 0:
                sortino = (annualized_return - risk_free) / downside_vol
            else:
                sortino = np.nan

            if max_dd < 0:
                calmar = annualized_return / -max_dd
            else:
                calmar = None

            win_rate = sum(single_df['ret'] > 0) / (len(single_df) - 1)
            win_loss = (
                    np.average(single_df[single_df['ret'] > 0]['ret'])
                    / np.average(-single_df[single_df['ret'] < 0]['ret'])
            )

            if i in monthly_funds:
                annualized_return_mean = np.nan
                annualized_vol = np.nan
                sharpe = np.nan
                sortino = np.nan
                win_rate = np.nan
                win_loss = np.nan
        else:
            annualized_return = np.nan
            annualized_return_mean = np.nan
            annualized_return_mean_simple = np.nan
            annualized_vol = np.nan
            max_dd = np.nan
            sharpe = np.nan
            sortino = np.nan
            calmar = np.nan
            win_rate = np.nan
            win_loss = np.nan

        result_single = pd.DataFrame(
            {
                start_date.strftime('%Y%m%d') + '以来年化': annualized_return,
                '平均周收益年化': annualized_return_mean,
                # '平均年化收益(单利)': annualized_return_mean_simple,
                '年化波动率': annualized_vol,
                '最大回撤': max_dd,
                'Sharpe': sharpe,
                'Sortino': sortino,
                # '收益峰度': single_df['ret'][1:].kurt(),
                # '收益偏度': single_df['ret'][1:].skew(),
                'Calmar': calmar,
                '投资胜率': win_rate,
                '平均损益比': win_loss

            }, index={i}
        ).T.reset_index()
        if len(result_all) == 0:
            result_all = result_single
        else:
            result_all = result_all.merge(result_single, on='index')

        # if len(dd_all) == 0:
        #     dd_all = single_df[['t_date', 'dd']].rename(columns={'dd': i})
        # else:
        dd_all = dd_all.merge(single_df[[date_col, 'dd']].rename(columns={'dd': i}), on=date_col, how='left')

        # if len(ret_all) == 0:
        #     ret_all = single_df[['t_date', 'ret']].rename(columns={'ret': i})
        # else:
        ret_all = ret_all.merge(single_df[[date_col, 'ret']].rename(columns={'ret': i}), on=date_col, how='left')

    return result_all, dd_all, ret_all


# 计算每只产品每月收益
def performance_monthly_ret(data_df):
    funds = data_df.columns.tolist()
    date_col = 't_date'
    if 't_date' in funds:
        funds.remove(date_col)
    elif '日期' in funds:
        date_col = '日期'
        funds.remove('日期')

    result_all = pd.DataFrame(
        {
            't_date': data_df[date_col][1:]
        }
    )

    for i in funds:
        ret = data_df[i] / data_df[i].shift(1) - 1
        result_all[i] = ret[1:]

    return result_all.iloc[::-1]


# 按类型计算产品平均收益率
def performance_ret_per_type(start_date, end_date, keyword='type', freq='w', db_work=''):
    fund_list = pd.read_sql_query(
        'select * from fund_list where class=="cta"', create_engine(db_work)
    )
    type_list = fund_list[keyword].drop_duplicates().tolist()
    type_ret = pd.DataFrame()
    for i in type_list:
        funds = fund_list[fund_list[keyword] == i].reset_index(drop=True)
        funds_data = load_funds_data(
            fund_list=funds,
            first_date=start_date,
            end_date=end_date,
            freq=freq
        )
        funds_ret = performance_monthly_ret(data_df=funds_data)
        funds_ret.to_excel('rwewe.xlsx')
        funds_ret[i] = funds_ret[funds['name'].tolist()].mean(axis=1)
        if len(type_ret) == 0:
            type_ret = funds_ret[['t_date', i]]
        else:
            type_ret = pd.merge(type_ret, funds_ret[['t_date', i]], on='t_date', how='left')

    return type_ret.iloc[::-1]


# 每只产品固定数据
# 收益（本周，近四周，近八周，2020年度，2019年度）
# data_df传入产品净值升序序列
def performance_specific_ret(data_df, form=True, monthly_funds=None):
    if monthly_funds is None:
        monthly_funds = []
    funds = data_df.columns.tolist()
    date_col = 't_date'
    if 't_date' in funds:
        funds.remove(date_col)
    elif '日期' in funds:
        date_col = '日期'
        funds.remove('日期')

    ret_this_week = []
    ret_last_week = []
    ret_this_4 = []
    ret_this_8 = []
    ret_2021 = []
    ret_2020 = []  # 年化
    ret_2019 = []  # 年化
    ret_2018 = []  # 年化

    for i in funds:
        print('\t computing specific index: ' + i)
        single_df = data_df[[date_col, i]]
        # single_df['ret'] = data_df[i] / data_df[i].shift(1)
        if i not in monthly_funds:
            ret_this_week.append(single_df[i][len(single_df) - 1] / single_df[i][len(single_df) - 2] - 1)
            ret_last_week.append(single_df[i][len(single_df) - 2] / single_df[i][len(single_df) - 3] - 1)
            ret_this_4.append(single_df[i][len(single_df) - 1] / single_df[i][len(single_df) - 5] - 1)
            ret_this_8.append(single_df[i][len(single_df) - 1] / single_df[i][len(single_df) - 9] - 1)
        else:
            ret_this_week.append(None)
            ret_last_week.append(None)
            ret_this_4.append(None)
            ret_this_8.append(None)

        nav_2018 = single_df[
            np.array(single_df[date_col] < datetime(2019, 1, 1).date())
            & np.array(single_df[date_col] >= datetime(2017, 12, 29).date())
        ].reset_index(drop=True)
        nav_2018 = nav_2018[nav_2018[i] > 0].reset_index(drop=True)

        nav_2019 = single_df[
            np.array(single_df[date_col] < datetime(2020, 1, 1).date())
            & np.array(single_df[date_col] >= datetime(2018, 12, 28).date())
        ].reset_index(drop=True)
        nav_2019 = nav_2019[nav_2019[i] > 0].reset_index(drop=True)

        nav_2020 = single_df[
            np.array(single_df[date_col] < datetime(2021, 1, 1).date())
            & np.array(single_df[date_col] >= datetime(2019, 12, 27).date())
        ].reset_index(drop=True)
        nav_2020 = nav_2020[nav_2020[i] > 0].reset_index(drop=True)

        nav_2021 = single_df[
            np.array(single_df[date_col] >= datetime(2020, 12, 31).date())
        ].reset_index(drop=True)
        nav_2021 = nav_2021[nav_2021[i] > 0].reset_index(drop=True)

        if len(nav_2018) > 1:
            ret_2018.append(nav_2018[i].tolist()[-1] / nav_2018[nav_2018[i] > 0][i].tolist()[0] - 1)
        else:
            ret_2018.append(None)

        if len(nav_2019) > 1:
            ret_2019.append(nav_2019[i].tolist()[-1] / nav_2019[nav_2019[i] > 0][i].tolist()[0] - 1)
        else:
            ret_2019.append(None)

        if len(nav_2020) > 1:
            ret_2020.append(nav_2020[i].tolist()[-1] / nav_2020[nav_2020[i] > 0][i].tolist()[0] - 1)
        else:
            ret_2020.append(None)

        if len(nav_2021) > 1:
            ret_2021.append(nav_2021[i].tolist()[-1] / nav_2021[nav_2021[i] > 0][i].tolist()[0] - 1)
        else:
            ret_2021.append(None)

        # try:
        #     ret_2021.append(
        #         nav_2021[i].tolist()[-1] / nav_2021[nav_2021[i] > 0][i].tolist()[0] - 1
        #     )
        # except:
        #     ret_2021.append(None)
        #
        # try:
        #     fund_2020_days = nav_2020[date_col][len(nav_2020) - 1] - nav_2020[date_col][0]
        #     ret_2020.append(
        #         (nav_2020[i].tolist()[-1] / nav_2020[nav_2020[i] > 0][i].tolist()[0]) ** (365 / fund_2020_days.days) - 1
        #     )
        # except IndexError:
        #     ret_2020.append(None)
        #
        # try:
        #     fund_2019_days = nav_2019[date_col][len(nav_2019) - 1] - nav_2019[date_col][0]
        #     if fund_2019_days.days < 90:
        #         ret_2019.append(None)
        #     else:
        #         ret_2019.append(
        #             (
        #                     nav_2019[i].tolist()[-1] / nav_2019[nav_2019[i] > 0][i].tolist()[0]
        #             ) ** (365 / fund_2019_days.days) - 1
        #         )
        # except:
        #     ret_2019.append(None)
        #
        # if len(nav_2018) > 1:
        #     fund_2018_days = nav_2018[date_col][len(nav_2018) - 1] - nav_2018[date_col][0]
        #     # 运行超过半年才计算年化
        #     if fund_2018_days.days < 90:
        #         ret_2018.append(None)
        #     else:
        #         ret_2018.append(
        #             (
        #                     nav_2018[i].tolist()[-1] / nav_2018[nav_2018[i] > 0][i].tolist()[0]
        #             ) ** (365 / fund_2018_days.days) - 1
        #         )
        # else:
        #     ret_2018.append(None)

    if form:
        result_df = pd.DataFrame(
            {
                '本周收益': ret_this_week,
                '上周收益': ret_last_week,
                '近四周收益': ret_this_4,
                '近八周收益': ret_this_8,
                '2021累计': ret_2021,
                '2020收益': ret_2020,
                '2019收益': ret_2019,
                '2018收益': ret_2018
            }, index=funds
        )

        return result_df.T.reset_index()

    else:
        result_df = pd.DataFrame(
            {
                '本周收益': ret_this_week,
                '上周收益': ret_last_week,
                '近四周收益': ret_this_4
            }, index=funds
        ).sort_values(by='本周收益', ascending=True)

        return result_df.T.reset_index()



