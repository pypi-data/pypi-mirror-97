"""
Set of functions to operate PgSQL database
author:K.Lz <565150134@qq.com>
"""
import pandas as pd
import psycopg2
import io


class con_pgsql(object):
    def __init__(self,dtbase,user,key,ip,port):
        """
        Get the required parameters to connect to the database and create a cursor to operate the database
        :param dtbase: str,database name
        :param user: str,User name to connect to the database
        :param key: str,Password to connect to database
        :param ip: str,the ip of database
        :param port: int,the port of database
        """
        self.conn = psycopg2.connect(database=dtbase, user=user, password=key,
                                            host=ip, port=str(port))
        self.cur = self.conn.cursor()

    def con_res(self, sql_text):
        """
        Used to execute SQL statements that need to return results
        :param sql_text:str,SQL statements to be executed
        :return:The execution result of SQL statement
        """
        self.cur.execute(sql_text)
        rets = self.cur.fetchall()
        return rets

    def con_exe(self, sql_text):
        """
        Used to execute SQL statements that perform operations on the database,
        such as update, insert and other operations
        :param sql_text:str,SQL statements to be executed
        """
        try:
            self.cur.execute(sql_text)
            self.conn.commit()
        except Exception:
            self.conn.rollback()

    def ob_data(self,tab_name,head_num=0):
        """
        use to obtain data from the table
        :param tab_name: str,The name of the table
        :param head_num: int,Number of lines displayed at the beginning
        :return: data in dataframe format
        """
        sql0 = 'select column_name from information_schema.columns ' \
               'where table_schema=\'public\' and table_name=' + '\'' + tab_name + '\'' + ';'  # 获取字段名(field name)
        if head_num:
            sql1 = 'select * from ' + tab_name + ' limit %s;' % str(head_num)
        else:
            sql1 = 'select * from ' + tab_name + ';'   # 获取表数据
        rets = con_pgsql.con_res(self,sql_text=sql1)  # 执行sql
        rets1 = con_pgsql.con_res(self,sql_text=sql0) # 执行sql，获取字段名
        df = pd.DataFrame(rets, columns=[each[0] for each in rets1])  # 获取数据，并转为dateframe格式
        return df

    def insert_values(self,df,tab_name):
        """
        Used to insert data into database
        :param df: dataframe,data in dataframe format(Note that the column name needs to be consistent with the database)
        :param tab_name: str,The name of the table
        """
        output = io.StringIO()
        df.to_csv(output, sep='|', index=False, header=False)
        output1 = output.getvalue()
        self.cur.copy_from(io.StringIO(output1),tab_name,sep='|',null='',columns=list(df.columns))
        self.conn.commit()

    def con_close(self):
        """
        Close the connection
        """
        self.cur.close()
        self.conn.close()
        print('already closed!')

