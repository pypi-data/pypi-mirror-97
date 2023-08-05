import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from hbshare.quant.cons import sql_write_path_hb, properties_fin_k, db, db_tables
from hbshare.quant.load_data import load_calendar_extra
import hbshare as hbs
import pymysql

pymysql.install_as_MySQLdb()

page_size_con = 99999


def wind_product_index_perc(
        start_date, end_date,
        db_path=sql_write_path_hb['daily'],
        table='commodities_index_wind',
        min_volume=10000
):
    engine = create_engine(db_path)
    data = pd.read_sql_query(
        'select `code`, `name`, `t_date`, `close`, `product`, `volume` from ' + table
        + ' where `t_date`<=' + end_date.strftime('%Y%m%d')
        + ' and `t_date`>=' + start_date.strftime('%Y%m%d')
        + ' and `product` not in (\'index\') order by `t_date` desc',
        engine
    )

    products = data.drop_duplicates(['product'])['product'].reset_index(drop=True)

    price_perc = []
    name_list = []
    for i in range(len(products)):
        product_data = data[data['product'] == products[i]].reset_index(drop=True)
        if product_data['volume'][:60].mean() < min_volume:
            continue

        product_price_perc = (
                                product_data['close'][0] - min(product_data['close'])
                             ) / (
                                max(product_data['close']) - min(product_data['close'])
                            )
        price_perc.append(product_price_perc)
        name_list.append(product_data['name'][0].replace('指数', ''))

    result = pd.DataFrame(
        {
            'name': name_list,
            'price_perc': price_perc
        }
    )

    return result.sort_values(by='price_perc', ascending=False).reset_index(drop=True)


def wind_product_index_sigma_xs(
        start_date, end_date,
        db_path=sql_write_path_hb['daily'], table='nh_index_wind', freq=''
):
    engine = create_engine(db_path)
    data_raw = pd.read_sql_query(
        'select `code`, `name`, `t_date`, `close`, `product`, `volume` from ' + table
        + ' where `t_date`<=' + end_date.strftime('%Y%m%d')
        + ' and `t_date`>=' + start_date.strftime('%Y%m%d')
        + ' and `product` not in (\'index\') order by `t_date`',
        engine
    )

    calendar = load_calendar_extra(freq=freq, start_date=start_date, end_date=end_date, db_path=db_path)
    result = calendar.copy()

    products = data_raw.drop_duplicates(['product'])['product'].tolist()
    names = []
    for i in products:
        print(i)
        data = data_raw[data_raw['product'] == i].reset_index(drop=True)
        data_clean = calendar.merge(data[['t_date', 'close']], on='t_date')
        data_clean['ret'] = data_clean['close'] / data_clean['close'].shift(1) - 1
        result = result.merge(
            data_clean[['t_date', 'ret']].rename(
                columns={'ret': data['name'][0].replace('指数', '').replace('南华', '')}
            ),
            on='t_date', how='left'
        )
        names.append(data['name'][0].replace('指数', '').replace('南华', ''))
    result['sigma'] = result[names].apply(lambda x: np.std(x, ddof=1), axis=1)
    result['mean'] = result[names].apply(lambda x: np.nanmean(x), axis=1)
    return result


def wind_com_fut_sec_index_amount(
        db_path,
        start_date=datetime(2015, 1, 1).date(),
        end_date=datetime.now().date(),
        table='commodities_index_wind',
        decimal=100000000,
        freq='',
):
    engine = create_engine(db_path)
    data = pd.read_sql_query(
        'select `code`, `name`, `t_date`, `close`, `product`, `volume`, `amount` from ' + table
        + ' where `t_date`<=' + end_date.strftime('%Y%m%d')
        + ' and `t_date`>=' + start_date.strftime('%Y%m%d')
        + ' and `product` in (\'index\') and `code`!=\'CCFI.WI\' order by `t_date`',
        engine
    )
    code_list = data['name'].drop_duplicates().tolist()
    date_df = data[['t_date']].drop_duplicates().reset_index(drop=True)
    if freq == '':
        amount_df = date_df.copy(deep=True)
        for i in code_list:
            data_i = data[data['name'] == i].reset_index().rename(columns={'amount': i})
            data_i[i] = data_i[i] / decimal
            data_i.loc[
                data_i['t_date'] < datetime(2020, 1, 1).date(), i
            ] = data_i[
                        data_i['t_date'] < datetime(2020, 1, 1).date()
                    ][i] / 2
            amount_df = amount_df.merge(data_i[['t_date', i]], on='t_date', how='left')

    else:
        amount_df = None
        for i in code_list:
            data_i = data[data['name'] == i].reset_index().rename(columns={'amount': i})[[i, 't_date']]
            data_i[i] = data_i[i] / decimal
            data_i.loc[
                data_i['t_date'] < datetime(2020, 1, 1).date(), i
            ] = data_i[
                    data_i['t_date'] < datetime(2020, 1, 1).date()
                    ][i] / 2
            data_i_s = pd.Series(data_i[i].tolist(), index=pd.to_datetime(data_i['t_date']))
            data_i_ranged = pd.DataFrame(data_i_s.resample(freq).mean().round(2)).rename(columns={0: i})
            if amount_df is None:
                amount_df = data_i_ranged
            else:
                amount_df = pd.concat([amount_df, data_i_ranged], axis=1)
        amount_df['t_date'] = pd.to_datetime(amount_df.reset_index()['t_date']).dt.date.tolist()
        amount_df = amount_df.reset_index(drop=True)
    return amount_df


def wind_index_fut_amount(
        db_path,
        start_date=datetime(2015, 1, 1).date(),
        end_date=datetime.now().date(),
        table='futures_wind',
        decimal=100000000,
        freq='',
):
    engine = create_engine(db_path)
    data = pd.read_sql_query(
        'select `code`, `symbol`, `t_date`, `close`, `product`, `volume`, `amount` from ' + table
        + ' where `t_date`<=' + end_date.strftime('%Y%m%d')
        + ' and `t_date`>=' + start_date.strftime('%Y%m%d')
        + ' and `product` in (\'IC\', \'IF\', \'IH\') order by `t_date`, `product`',
        engine
    )
    code_list = data['product'].drop_duplicates().tolist()
    date_df = data[['t_date']].drop_duplicates().reset_index(drop=True)
    if freq == '':
        amount_df = date_df.copy(deep=True)
        for i in code_list:
            data_i = data[data['product'] == i].reset_index().rename(columns={'amount': i})
            data_i[i] = data_i[i] / decimal
            data_i_grouped = data_i[['t_date', i]].groupby('t_date').sum().round(2).reset_index()
            amount_df = amount_df.merge(data_i_grouped[['t_date', i]], on='t_date', how='left')
    else:
        amount_df = None
        for i in code_list:
            data_i = data[data['product'] == i].reset_index().rename(columns={'amount': i})
            data_i[i] = data_i[i] / decimal
            data_i_grouped = data_i[['t_date', i]].groupby('t_date').sum().round(2).reset_index()
            data_i_s = pd.Series(data_i_grouped[i].tolist(), index=pd.to_datetime(data_i_grouped['t_date']))
            data_i_ranged = pd.DataFrame(data_i_s.resample(freq).mean().round(2)).rename(columns={0: i})
            if amount_df is None:
                amount_df = data_i_ranged
            else:
                amount_df = pd.concat([amount_df, data_i_ranged], axis=1)
        amount_df['t_date'] = pd.to_datetime(amount_df.reset_index()['t_date']).dt.date.tolist()
        amount_df = amount_df.reset_index(drop=True)

    return amount_df


def fin_fut_daily_k_by_contracts(contract_list, start_date=None, end_date=None, page_size=None):
    if start_date is None:
        start_date = datetime(2010, 1, 1).date()
    if end_date is None:
        end_date = datetime.now().date()
    if page_size is None:
        page_size = page_size_con

    if len(contract_list) == 0:
        raise ValueError('code_list 未传入参数')
    elif len(contract_list) > 1:
        sql_contract = 'ContractInnerCode in ' + str(tuple(contract_list))
    elif len(contract_list) > 999:
        raise ValueError('code_list 参数过多')
    else:
        sql_contract = 'ContractInnerCode=' + str(contract_list[0])

    sql = 'select ' + ', '.join(properties_fin_k) + ' from ' + db_tables['hsjy_fin_daily_quote'] \
          + ' where ' + sql_contract + ' and TradingDay<=TRUNC(to_date(' + end_date.strftime('%Y%m%d') \
          + ', \'yyyymmdd\')) and TradingDay>=TRUNC(to_date(' + start_date.strftime('%Y%m%d') \
          + ', \'yyyymmdd\')) order by TradingDay, ContractInnerCode'

    data = hbs.db_data_query(db=db, sql=sql, page_size=page_size)
    if data['pages'] > 1:
        for p in range(2, data['pages'] + 1):
            data['data'] = data['data'] + hbs.db_data_query(db=db, sql=sql, page_size=page_size, page_num=p)['data']

    return data


