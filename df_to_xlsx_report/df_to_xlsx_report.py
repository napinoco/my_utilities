import pandas as pd
import xlsxwriter as xl


def main():
    wb = xl.Workbook('output.xlsx', options={'constant_memory': True})

    # create worksheet
    ws = wb.add_worksheet('test')

    # write to the worksheet
    df_config = pd.read_csv('config.csv', skiprows=1)
    df_data = pd.read_csv('data.csv')
    wb_format_dict = write_df_to_worksheet(df_config, df_data, wb, ws)

    wb.close()


def write_df_to_worksheet(df_config: pd.DataFrame,
                          df_data: pd.DataFrame,
                          wb: xl.Workbook,
                          ws: xl.worksheet.Worksheet,
                          wb_format_dict: dict = None) -> dict:
    # prepare
    if wb_format_dict is None:
        wb_format_dict = dict()  # to avoid duplicated format

    if 'left1' in wb_format_dict:
        last_col_format = wb_format_dict['left1']
    else:
        last_col_format = wb.add_format({'left': 1})
        wb_format_dict.update({'left1': last_col_format})

    # create & write header format
    max_lvl = df_config['level'].max()
    for i in range(max_lvl + 1):
        j = -1
        cur_top, cur_bg = None, None
        for j, (level, left, bg, name) in enumerate(
                zip(*(df_config[k].to_list() for k in ['level', 'left', 'bg_color', 'logical_name']))):
            if i > level:
                cur_top, cur_left, cur_bg, cur_name = None, left, bg, None
            elif i == level:
                cur_top, cur_left, cur_bg, cur_name = left, left, bg, name
            else:
                cur_left, cur_name = None, None
            kv_str = ''.join(
                str(k) + str(v) for k, v in zip(['top', 'left', 'bg_color'], [cur_top, cur_left, cur_bg]) if
                v is not None)
            if kv_str in wb_format_dict:
                wb_format = wb_format_dict[kv_str]
            else:
                wb_format = wb.add_format(
                    {k: v for k, v in zip(['top', 'left', 'bg_color'], [cur_top, cur_left, cur_bg]) if v is not None})
                wb_format_dict.update({kv_str: wb_format})
            ws.write(i, j, None if pd.isna(cur_name) else cur_name, wb_format)
        ws.write(i, j + 1, None, last_col_format)
    ws.freeze_panes(max_lvl + 1, 0)
    ws.autofilter(max_lvl, 0, max_lvl, j)

    # create data format
    data_format_list = []
    data_format_keys = ['left', 'num_format']
    for vals in zip(*(df_config[k].to_list() for k in data_format_keys)):
        kv_str = ''.join(str(k) + str(v)
                         for k, v in zip(data_format_keys, vals) if v is not None)
        if kv_str in wb_format_dict:
            wb_format = wb_format_dict[kv_str]
        else:
            wb_format = wb.add_format(
                {k: v for k, v in zip(data_format_keys, vals) if v is not None})
            wb_format_dict.update({kv_str: wb_format})
        data_format_list.append(wb_format)
    df_config['data_format'] = data_format_list

    # write data
    col_names = df_config['physical_name'].to_list()
    data_format_list = df_config['data_format'].to_list()
    df_data = df_data.reindex(columns=col_names).copy()
    for i, row in enumerate(zip(*(df_data[col].to_list() for col in col_names))):
        j = -1
        for j, v in enumerate(row):
            ws.write(i + max_lvl + 1, j, None if pd.isna(v)
                     else v, data_format_list[j])
        ws.write(i + max_lvl + 1, j + 1, None, last_col_format)

    # set column width
    for j, col_width in enumerate(df_config['width'].to_list()):
        ws.set_column(j, j, col_width)
    return wb_format_dict


if __name__ == '__main__':
    main()
