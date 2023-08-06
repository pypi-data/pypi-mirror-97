#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/1/26 下午10:13
@File    : import_data.py
@contact : mmmaaaggg@163.com
@desc    : 用于将办公室与家里的数据通过邮件方式进行同步
"""
import logging
import os
import tarfile
from datetime import date
from io import BytesIO

import pandas as pd
from peewee import IntegrityError

from vnpy_extra.db.orm import database
from vnpy_extra.utils.get_email import download_email_attachment

logger = logging.getLogger()


@database.atomic()
def import_data_2_tables(email_title, password, ignore_error=True):
    attachment_dic = download_email_attachment(email_title, password=password)

    tio = BytesIO()
    keys = sorted(attachment_dic.keys())
    for key in keys:
        tio.write(attachment_dic[key].read())
    tio.seek(0)
    tar = tarfile.open(fileobj=tio)
    # use "tar" as a regular TarFile object
    dir_name = f'data/{date.today()}'
    os.makedirs(dir_name, exist_ok=True)
    tar.extractall(path=dir_name)
    data_len = len(os.listdir(dir_name))
    num = 0
    error_count = 0
    for file_name in os.listdir(dir_name):
        table_name = file_name.split('.')[0]
        num = num + 1
        table_path = os.path.join(dir_name, file_name)  # 将路径与文件名结合起来就是每个文件的完整路径
        df = pd.read_csv(table_path)
        fields = list(df.columns)
        fields_str = "`" + "`,`".join(fields) + "`"
        values_str = ",".join(["%s" for _ in fields])
        update_str = ",".join([f"{_}=%s" for _ in fields])
        sql_str = f"insert into {table_name} ({fields_str}) values({values_str}) " \
                  f"on duplicate key update {update_str}"
        for row in df.to_dict(orient='record'):
            if 'id_name' in fields and pd.isna(row['id_name']):
                # some dirty data has to be clean
                continue
            param = [None if pd.isna(row[_]) else row[_] for _ in fields]
            param.extend([None if pd.isna(row[_]) else row[_] for _ in fields])
            try:
                database.execute_sql(sql_str, params=param)
            except IntegrityError as exp:
                if ignore_error:
                    error_count += 1
                else:
                    raise exp from exp

        logger.info("%d/%d) %s 同步完成 %d 条数据。%s",
                    num, data_len, table_name, df.shape[0],
                    "" if error_count == 0 else f"{error_count} 条记录冲突"
                    )


@database.atomic()
def csv_2_tables(dir_path, ignore_error=True):
    file_name_list = os.listdir(dir_path)
    data_len = len(file_name_list)
    error_count = 0
    for num, file_name in enumerate(file_name_list, start=1):
        table_name, ext = os.path.splitext(file_name)
        if ext != '.csv':
            continue
        df = pd.read_csv(os.path.join(dir_path, file_name))
        fields = list(df.columns)
        fields_str = "`" + "`,`".join(fields) + "`"
        values_str = ",".join(["%s" for _ in fields])
        update_str = ",".join([f"{_}=%s" for _ in fields])
        sql_str = f"insert into {table_name} ({fields_str}) values({values_str}) " \
                  f"on duplicate key update {update_str}"
        for row in df.to_dict(orient='record'):
            if 'id_name' in fields and pd.isna(row['id_name']):
                # some dirty data has to be clean
                continue
            param = [None if pd.isna(row[_]) else row[_] for _ in fields]
            param.extend([None if pd.isna(row[_]) else row[_] for _ in fields])
            try:
                database.execute_sql(sql_str, params=param)
            except IntegrityError as exp:
                if ignore_error:
                    error_count += 1
                else:
                    raise exp from exp

        logger.info("%d/%d) %s 同步完成 %d 条数据。%s",
                    num, data_len, table_name, df.shape[0],
                    "" if error_count == 0 else f"{error_count} 条记录冲突"
                    )


if __name__ == "__main__":
    # import_data_2_tables('exports 2021-02-26', '****')
    csv_2_tables(r'C:\Users\zerenhe-lqb\Downloads\email_data')
