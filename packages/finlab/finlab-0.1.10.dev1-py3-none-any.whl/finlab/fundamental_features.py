import numpy as np
import pandas as pd
from finlab.data import get


def to_seasonal(df):
    season4 = df[df.index.month == 3]
    season1 = df[df.index.month == 5]
    season2 = df[df.index.month == 8]
    season3 = df[df.index.month == 11]

    season1.index = season1.index.year
    season2.index = season2.index.year
    season3.index = season3.index.year
    season4.index = season4.index.year - 1

    newseason1 = season1
    newseason2 = season2 - season1.reindex_like(season2)
    newseason3 = season3 - season2.reindex_like(season3)
    newseason4 = season4 - season3.reindex_like(season4)

    newseason1.index = pd.to_datetime(newseason1.index.astype(str) + '-05-15')
    newseason2.index = pd.to_datetime(newseason2.index.astype(str) + '-08-14')
    newseason3.index = pd.to_datetime(newseason3.index.astype(str) + '-11-14')
    newseason4.index = pd.to_datetime((newseason4.index + 1).astype(str) + '-03-31')
    return newseason1.append(newseason2).append(newseason3).append(newseason4).sort_index()


def fundamental_features():
    收盤價 = get('price:收盤價')

    T3900繼續營業部門稅前純益 = get('tw_financial_statements:繼續營業單位損益')
    T3900繼續營業部門稅前純益 = T3900繼續營業部門稅前純益[T3900繼續營業部門稅前純益.columns & 收盤價.columns]

    T3970經常稅後淨利 = get('tw_financial_statements:合併總損益')
    T3970經常稅後淨利 = T3970經常稅後淨利[T3970經常稅後淨利.columns & 收盤價.columns]

    T2000權益總計 = get('tw_financial_statements:股東權益總額')
    T2000權益總計 = T2000權益總計[T2000權益總計.columns & 收盤價.columns]

    T3295營業毛利 = get('tw_financial_statements:營業毛利')
    T3295營業毛利 = T3295營業毛利[T3295營業毛利.columns & 收盤價.columns]

    T3100營業收入淨額 = get("tw_financial_statements:營業收入淨額")
    T3100營業收入淨額 = T3100營業收入淨額[T3100營業收入淨額.columns & 收盤價.columns]

    T3700營業外收入及支出 = get("tw_financial_statements:營業外收入及支出")
    T3700營業外收入及支出 = T3700營業外收入及支出[T3700營業外收入及支出.columns & 收盤價.columns]

    T3910所得稅費用 = get("tw_financial_statements:所得稅費用")
    T3910所得稅費用 = T3910所得稅費用[T3910所得稅費用.columns & 收盤價.columns]

    T3300營業費用 = get("tw_financial_statements:營業費用")
    T3300營業費用 = T3300營業費用[T3300營業費用.columns & 收盤價.columns]

    T7211折舊 = to_seasonal(get('tw_financial_statements:折舊費用'))
    T7211折舊 = T7211折舊[T7211折舊.columns & 收盤價.columns]

    T7212攤提 = to_seasonal(get('tw_financial_statements:攤銷費用'))
    T7212攤提 = T7212攤提[T7212攤提.columns & 收盤價.columns]

    T3920繼續營業部門純益 = T3900繼續營業部門稅前純益.fillna(0) - T3910所得稅費用.fillna(0)
    T3920繼續營業部門純益[T3920繼續營業部門純益 == 0] = np.nan

    T0170存貨 = get("tw_financial_statements:存貨")
    T0170存貨 = T0170存貨[T0170存貨.columns & 收盤價.columns]

    股本 = get('股本')
    股本 = 股本[股本.columns & 收盤價.columns]

    T0400不動產廠房設備合計 = get("tw_financial_statements:不動產廠房及設備")
    T0400不動產廠房設備合計 = T0400不動產廠房設備合計[T0400不動產廠房設備合計.columns & 收盤價.columns]

    T0960非流動資產 = get("tw_financial_statements:非流動資產")
    T0960非流動資產 = T0960非流動資產[T0960非流動資產.columns & 收盤價.columns]

    T0180預付費用及預付款 = get('tw_financial_statements:預付投資款')
    T0180預付費用及預付款 = T0180預付費用及預付款[T0180預付費用及預付款.columns & 收盤價.columns]

    T1800非流動負債 = get("tw_financial_statements:非流動負債")
    T1800非流動負債 = T1800非流動負債[T1800非流動負債.columns & 收盤價.columns]

    T0190其他流動資產 = get('tw_financial_statements:其他流動資產')
    T0190其他流動資產 = T0190其他流動資產[T0190其他流動資產.columns & 收盤價.columns]

    T1100流動負債 = get("tw_financial_statements:流動負債")
    T1100流動負債 = T1100流動負債[T1100流動負債.columns & 收盤價.columns]

    T0100流動資產 = get("tw_financial_statements:流動資產")
    T0100流動資產 = T0100流動資產[T0100流動資產.columns & 收盤價.columns]

    T3501財物成本 = get('tw_financial_statements:財務成本')
    T3501財物成本 = T3501財物成本[T3501財物成本.columns & 收盤價.columns]

    T0010資產總額 = get('tw_financial_statements:負債及股東權益總額')
    T0010資產總額[T0010資產總額 == 0] = np.nan

    T3971本期綜合損益總額 = get("tw_financial_statements:本期綜合損益總額")
    T3971本期綜合損益總額 = T3971本期綜合損益總額[T3971本期綜合損益總額.columns & 收盤價.columns]

    T3395營業利益 = get('tw_financial_statements:營業利益')
    T3395營業利益 = T3395營業利益[T3395營業利益.columns & 收盤價.columns]

    T2403稅前息前折舊前淨利 = T3900繼續營業部門稅前純益.fillna(0) + T3501財物成本.fillna(0) + T7211折舊.fillna(0) + T7212攤提.fillna(0)
    T2403稅前息前折舊前淨利[T2403稅前息前折舊前淨利 == 0] = np.nan

    T2402稅前息前淨利 = T3900繼續營業部門稅前純益.fillna(0) + T3501財物成本.fillna(0)
    T2402稅前息前淨利[T2402稅前息前淨利 == 0] = np.nan

    R202用人費用率 = get("tw_financial_statements:管理費用")
    R202用人費用率 = R202用人費用率[R202用人費用率.columns & 收盤價.columns]

    T3356研究發展費 = get("tw_financial_statements:研究發展費")
    T3356研究發展費 = T3356研究發展費[T3356研究發展費.columns & 收盤價.columns]

    T7210營運現金流 = to_seasonal(get("tw_financial_statements:營業活動之淨現金流入_流出"))
    T7210營運現金流 = T7210營運現金流[T7210營運現金流.columns & 收盤價.columns]

    T3950歸屬母公司淨利 = get('tw_financial_statements:綜合損益歸屬母公司')
    T3950歸屬母公司淨利 = T3950歸屬母公司淨利[T3950歸屬母公司淨利.columns & 收盤價.columns]

    T1000負債總額 = get("tw_financial_statements:負債總額")
    T1000負債總額 = T1000負債總額[T1000負債總額.columns & 收盤價.columns]

    T3200營業成本 = get("tw_financial_statements:營業成本")
    T3200營業成本 = T3200營業成本[T3200營業成本.columns & 收盤價.columns]

    T7324取得不動產廠房及設備 = to_seasonal(get("tw_financial_statements:取得不動產_廠房及設備"))
    T7324取得不動產廠房及設備 = T7324取得不動產廠房及設備[T7324取得不動產廠房及設備.columns & 收盤價.columns]

    應收帳款與票據 = get('tw_financial_statements:應收帳款與票據')
    應收帳款與票據 = 應收帳款與票據[應收帳款與票據.columns & 收盤價.columns]

    應收帳款週轉率 = T3100營業收入淨額 / ((應收帳款與票據 + 應收帳款與票據.shift(1)) / 2)

    # 2018年(含)以後所得稅率為20%
    # 2010年(含)至2017年(含)期間所得稅率為17%
    # 2009年(含)以前所得稅率為25%

    import pandas as pd
    所得稅率 = pd.DataFrame(0.2, index=T3501財物成本.index, columns=T3501財物成本.columns)
    所得稅率.loc[:'2017'] = 17
    所得稅率.loc[:'2009'] = 25

    # 獲利能力指標

    R101_ROA稅後息前 = (T3920繼續營業部門純益 + T3501財物成本 * (1 - 所得稅率)) / (T0010資產總額 + T0010資產總額.shift()) * 2 * 100
    R11V_ROA綜合損益 = T3971本期綜合損益總額 / (T0010資產總額 + T0010資產總額.shift()) * 2 * 100
    R103_ROE稅後 = T3920繼續營業部門純益 / (T2000權益總計 + T2000權益總計.shift()).abs() * 2 * 100
    R11U_ROE綜合損益 = (T3971本期綜合損益總額 / ((T2000權益總計 + T2000權益總計.shift()) / 2)) * 100

    R145_稅前息前折舊前淨利率 = T2403稅前息前折舊前淨利 / T3100營業收入淨額 * 100
    R105_營業毛利率 = T3295營業毛利 / T3100營業收入淨額 * 100
    R106_營業利益率 = T3395營業利益 / T3100營業收入淨額 * 100
    R107_稅前淨利率 = T3900繼續營業部門稅前純益 / T3100營業收入淨額 * 100
    R108_稅後淨利率 = T3970經常稅後淨利 / T3100營業收入淨額 * 100
    R112_業外收支營收率 = T3700營業外收入及支出 / T3100營業收入淨額 * 100
    R179_貝里比率 = T3295營業毛利 / T3300營業費用 * 100

    # 成本費用率指標

    R203_研究發展費用率 = T3356研究發展費 / T3300營業費用 * 100
    R205_現金流量比率 = T7210營運現金流 / T1100流動負債 * 100
    R207_稅率 = (T3910所得稅費用 / T3900繼續營業部門稅前純益 * 100)
    R207_稅率[(T3900繼續營業部門稅前純益 <= 0) | (T3910所得稅費用 <= 0)] = 0

    # 償債能力指標
    R304_每股營業額 = T3100營業收入淨額 / 股本 * 10
    R305_每股營業利益 = T3395營業利益 / 股本 * 10
    R303_每股現金流量 = T7210營運現金流 / (股本 + 股本.shift()) * 2 * 10
    R306_每股稅前淨利 = T3900繼續營業部門稅前純益 / 股本 * 10
    R314_每股綜合損益 = T3971本期綜合損益總額 / 股本 * 10
    R315_每股稅前淨利 = T3900繼續營業部門稅前純益 / 股本 * 10
    R316_每股稅後淨利 = T3950歸屬母公司淨利 / 股本 * 10
    R504_總負債除總淨值 = T1000負債總額 / T2000權益總計 * 100
    R505_負債比率 = T1000負債總額 / T0010資產總額 * 100
    R506_淨值除資產 = T2000權益總計 / T0010資產總額 * 100

    # 成長率指標
    def 成長率(s):
        return (s / s.shift(4).abs() - 1) * 100

    R401_營收成長率 = 成長率(T3100營業收入淨額)
    R402_營業毛利成長率 = 成長率(T3295營業毛利)
    R403_營業利益成長率 = 成長率(T3395營業利益)
    R404_稅前淨利成長率 = 成長率(T3900繼續營業部門稅前純益)
    R405_稅後淨利成長率 = 成長率(T3970經常稅後淨利)
    R406_經常利益成長率 = 成長率(T3920繼續營業部門純益)
    R408_資產總額成長率 = 成長率(T0010資產總額)
    R409_淨值成長率 = 成長率(T2000權益總計)

    # 償債能力指標
    R501_流動比率 = T0100流動資產 / T1100流動負債 * 100
    速動資產 = T0100流動資產.fillna(0) - T0170存貨.fillna(0) - T0180預付費用及預付款.fillna(0) - T0190其他流動資產.fillna(0)
    速動資產[速動資產 == 0] = np.nan
    R502_速動比率 = 速動資產 / T1100流動負債 * 100

    繼續營業部門稅前純益加財務成本 = T3920繼續營業部門純益.fillna(0) + T3501財物成本.fillna(0) * (1 - 所得稅率.fillna(0))
    繼續營業部門稅前純益加財務成本[繼續營業部門稅前純益加財務成本 == 0] = np.nan
    R503_利息支出率 = T3501財物成本 / 繼續營業部門稅前純益加財務成本 * 100

    R678_營運資金 = T0100流動資產.fillna(0) - T1100流動負債.fillna(0)
    R678_營運資金[R678_營運資金 == 0] = np.nan

    R607_總資產週轉次數 = T3100營業收入淨額 / ((T0010資產總額 + T0010資產總額.shift(1)) / 2)

    R610_存貨週轉率 = T3200營業成本 / ((T0170存貨 + T0170存貨.shift(1)) / 2)

    R612_固定資產週轉次數 = T3100營業收入淨額 / ((T0400不動產廠房設備合計 + T0400不動產廠房設備合計.shift(1)) / 2)

    R613_淨值週轉率次 = T3100營業收入淨額 / ((T2000權益總計 + T2000權益總計.shift(1)) / 2)

    R69B_自由現金流量 = T3970經常稅後淨利.fillna(0) + T7211折舊.fillna(0) - T7212攤提.fillna(0) - T7324取得不動產廠房及設備.fillna(0) - ((
                                                                                                                       T0100流動資產.fillna(
                                                                                                                           0) - T1100流動負債.fillna(
                                                                                                                   0)) - (
                                                                                                                       T0100流動資產.fillna(
                                                                                                                           0).shift() - T1100流動負債.fillna(
                                                                                                                   0).shift()))
    R69B_自由現金流量[R69B_自由現金流量 == 0] = np.nan
    fundamental_data = {

        # checked
        'T3395營業利益': T3395營業利益,
        'T7210營運現金流': T7210營運現金流,
        'T3950歸屬母公司淨利': T3950歸屬母公司淨利,
        'T7211折舊': T7211折舊,
        'T0100流動資產': T0100流動資產,
        'T1100流動負債': T1100流動負債,
        'T7324取得不動產廠房及設備': T7324取得不動產廠房及設備,
        'T7210營運現金流': T7210營運現金流,

        # 獲利能力指標
        'T3970經常稅後淨利': T3970經常稅後淨利,
        'T7210營運現金流': T7210營運現金流,
        'R101_ROA稅後息前': R101_ROA稅後息前,
        'R11V_ROA綜合損益': R11V_ROA綜合損益,
        'R103_ROE稅後': R103_ROE稅後,
        'R11U_ROE綜合損益': R11U_ROE綜合損益,
        'R145_稅前息前折舊前淨利率': R145_稅前息前折舊前淨利率,
        'R105_營業毛利率': R105_營業毛利率,
        'R106_營業利益率': R106_營業利益率,
        'R107_稅前淨利率': R107_稅前淨利率,
        'R108_稅後淨利率': R108_稅後淨利率,
        'R112_業外收支營收率': R112_業外收支營收率,
        'R179_貝里比率': R179_貝里比率,

        # 成本費用率指標
        'R203_研究發展費用率': R203_研究發展費用率,
        'R205_現金流量比率': R205_現金流量比率,
        'R207_稅率': R207_稅率,

        # 償債能力指標
        'R304_每股營業額': R304_每股營業額,
        'R305_每股營業利益': R305_每股營業利益,  # checked
        'R303_每股現金流量': R303_每股現金流量,  # checked
        'R306_每股稅前淨利': R306_每股稅前淨利,  # checked
        'R314_每股綜合損益': R314_每股綜合損益,  # checked
        #         'R315_每股稅前淨利': R315_每股稅前淨利, # checked
        'R316_每股稅後淨利': R316_每股稅後淨利,  #
        'R504_總負債除總淨值': R504_總負債除總淨值,
        'R505_負債比率': R505_負債比率,  # checked
        'R506_淨值除資產': R506_淨值除資產,  #

        # 成長率指標
        'R401_營收成長率': R401_營收成長率,
        'R402_營業毛利成長率': R402_營業毛利成長率,
        'R403_營業利益成長率': R403_營業利益成長率,
        'R404_稅前淨利成長率': R404_稅前淨利成長率,
        'R405_稅後淨利成長率': R405_稅後淨利成長率,
        'R406_經常利益成長率': R406_經常利益成長率,
        'R408_資產總額成長率': R408_資產總額成長率,
        'R409_淨值成長率': R409_淨值成長率,

        # 償債能力指標
        'R501_流動比率': R501_流動比率,
        'R502_速動比率': R502_速動比率,  # check
        'R503_利息支出率': R503_利息支出率,
        'R678_營運資金': R678_營運資金,
        'R607_總資產週轉次數': R607_總資產週轉次數,
        'R610_存貨週轉率': R610_存貨週轉率,
        'R612_固定資產週轉次數': R612_固定資產週轉次數,
        'R613_淨值週轉率次': R613_淨值週轉率次,
        'R69B_自由現金流量': R69B_自由現金流量,
        #         '應收帳款週轉率':應收帳款週轉率,
    }
    ret = pd.DataFrame({name: df.unstack() for name, df in fundamental_data.items()})
    ret.index = ret.index.set_names(['stock_id', 'date'])
    return ret
