"""
A collection of simple methods to operate mysql, sqlserver and Oracle Database
author:K.Lz <565150134@qq.com>
"""

import pymysql
import pymssql
import cx_Oracle
import pandas as pd


class db_query(object):
    def __init__(self,db_type,ip,port,user,key,dborsv_name):
        """
        Get the required parameters to connect to the database and create a cursor to operate the database
        :param db_type:str,the type of database
        :param ip:str,the ip of database
        :param port:int,the port of database
        :param user:str,User name to connect to the database
        :param key:str,Password to connect to database
        :param dborsv_name:str,database name or a combination of service name and schema name
        """
        self.db_type = db_type
        self.ip = ip
        self.port = port
        self.user = user
        self.key = key
        self.dborsv_name = dborsv_name
        if self.db_type == 'mysql':
            self.conn = pymysql.connect(host=ip,
                       port=port,
                       user=user,
                       passwd=key,
                       db=dborsv_name)  # Connect to mysql
            self.schema_name = dborsv_name
        elif self.db_type == 'oracle':
            self.schema_name = dborsv_name.split('/')[1]
            addres = ip+':'+str(port)+'/'+dborsv_name.split('/')[0]
            self.conn = cx_Oracle.connect(user, key,addres)  # Connect to oracle
        else:
            ipparam = ip + ':' +str(port)
            self.conn = pymssql.connect(server=ipparam,
                       user=user,password=key,database=dborsv_name) # Connect to sqlserver
            self.schema_name = dborsv_name
        self.cur = self.conn.cursor()

    def con_ok(self):
        """
        Check whether the connection is successful
        """
        if self.conn:
            print('Connected successfully.')
        else:
            print('Failed to connect successfully.')

    def con_res(self,sql_text):
        """
        Used to execute SQL statements that need to return results
        :param sql_text:str,SQL statements to be executed
        :return:The execution result of SQL statement
        """
        self.cur.execute(sql_text)
        rets = self.cur.fetchall()
        return rets

    def con_exe(self,sql_text):
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

    def ob_table_list(self):
        """
        Get all table names in the database
        :return:A list containing all table names
        """
        if self.db_type == 'mysql':
            self.cur.execute('show tables')  # 返回的元组
        elif self.db_type == 'oracle':
            sql_text = 'select object_name from dba_objects where ' \
                       'owner = \'%s\' and (object_type=\'TABLE\' ' \
                       'or object_type=\'VIEW\')'%self.schema_name
            self.cur.execute(sql_text)  # 返回的列表，列表中各表名为元组形式eg:[('gs_etps_app',)]
        else:
            self.cur.execute('SELECT Name FROM SysObjects '
                             'Where XType=\'U\' or XType=\'V\' ORDER BY Name') # 返回列表
        res0 = self.cur.fetchall()
        res = [each[0] for each in res0]
        print(res)
        return res

    def ob_recnum(self,tab_name):
        """
        Query the amount of data in the table
        :param tab_name: str,The name of the table to be queried
        :return:the amount of data in the table
        """
        if self.db_type == 'oracle':
            sql_text = 'select count(1) from %s.%s' % (self.schema_name,tab_name)
        else:
            sql_text = 'select count(1) from %s' % (tab_name)
        self.cur.execute(sql_text)
        tab_num = self.cur.fetchall()
        total_num = tab_num[0][0]
        return total_num

    def ob_colinfo(self,tab_name):
        """
        Used to get field information in the table, including field name, field type,
        and comment information
        :param tab_name: str,The name of the table to be queried
        :return:A table containing field names, field types, and comment information
        """
        if self.db_type == 'mysql':
            # Get field name and field type and field description
            sql_text0 = 'select column_name,data_type,column_comment from ' \
                        'information_schema.columns where ' \
                        'table_schema=\'%s\' ' \
                        'and table_name=\'%s\';' % (self.schema_name, tab_name)
            self.cur.execute(sql_text0)
            column_need = self.cur.fetchall()
            df_col = pd.DataFrame(list(column_need))
        elif self.db_type == 'oracle':
            # Get field name and field type
            sql_text0 = 'SELECT column_name,data_type FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = \'%s\'' \
                        'and OWNER=\'%s\' order by column_id' % (tab_name,self.schema_name)
            self.cur.execute(sql_text0)
            column_need = self.cur.fetchall()
            df_col0 = pd.DataFrame(column_need)
            # Get field description
            sql_text1 = 'select comments from all_col_comments WHERE TABLE_NAME = \'%s\' ' \
                        'and OWNER=\'%s\'' % (tab_name,self.schema_name)
            self.cur.execute(sql_text1)
            comment_need = self.cur.fetchall()
            df_comments = pd.DataFrame(comment_need)
            df_col = pd.concat([df_col0,df_comments],axis=1, ignore_index=True)
        else:
            # Get field name and field type
            sql_text0 = 'select sc.name,st.name from syscolumns sc,systypes st ' \
                        'where sc.xtype=st.xtype and sc.id in(select id from sysobjects ' \
                        'where name=\'%s\') order by sc.colid;' % (tab_name)
            self.cur.execute(sql_text0)
            column_need = self.cur.fetchall()
            df_col0 = pd.DataFrame(column_need)
            # Get field description
            sql_text1 = 'select com.value from sys.columns as col left join ' \
                        'sys.extended_properties as com on col.object_id=com.major_id ' \
                        'and col.column_id=com.minor_id ' \
                        'where col.object_id = object_id (\'%s\' );' % (tab_name)
            self.cur.execute(sql_text1)
            comment_need = self.cur.fetchall()
            comment_need1 = [each[0] if isinstance(each[0], str) or each[0] is None
                             else each[0].decode('utf-8') for each in comment_need]
            df_comments = pd.DataFrame(comment_need1)
            df_col = pd.concat([df_col0, df_comments], axis=1, ignore_index=True)

        df_col = df_col.drop_duplicates(subset=[0], keep='first').reset_index()

        return df_col

    def ob_tabcom(self,tab_name):
        """
        Used to get table comments
        :param tab_name:str,The name of the table to be queried
        :return:the table comments
        """
        if self.db_type == 'mysql':
            sql_text2 = 'SELECT TABLE_COMMENT FROM ' \
                        'information_schema.TABLES WHERE ' \
                        'table_schema=\'%s\' ' \
                        'and table_name=\'%s\';' % (self.schema_name, tab_name)
            self.cur.execute(sql_text2)
            comment_tab = self.cur.fetchall()
            comments_tab = comment_tab[0][0] if isinstance(comment_tab[0][0], str) or comment_tab[0][0] is None else \
            comment_tab[0][0].decode('utf-8')
        elif self.db_type == 'oracle':
            sql_text2 = 'select comments from all_tab_comments WHERE TABLE_NAME = \'%s\' ' \
                        'and OWNER=\'%s\'' % (tab_name, self.schema_name)
            self.cur.execute(sql_text2)
            comment_tab = self.cur.fetchall()
            comments_tab = comment_tab[0][0]
        else:
            sql_text2 = 'select value from sys.extended_properties ' \
                        'where major_id=(select id from sysobjects where name=\'%s\') ' \
                        'and minor_id=0;' % (tab_name)
            self.cur.execute(sql_text2)
            comment_tab = self.cur.fetchall()
            comments_tab = str()
            if comment_tab:
                comments_tab = comment_tab[0][0] if isinstance(comment_tab[0][0], str) \
                                                    or comment_tab[0][0] is None \
                    else comment_tab[0][0].decode('utf-8')

        return comments_tab

    def ob_data(self,tab_name,head_num=0):
        '''
        use to obtain data from the table
        :param tab_name: str,The name of the table
        :param head_num: int,Number of lines displayed at the beginning
        :return: data in dataframe format
        '''
        if head_num:
            # get the first few rows of data
            if self.db_type == 'mysql':
                sql = 'SELECT * FROM ' + tab_name + ' limit %s;'%str(head_num)
            elif self.db_type == 'oracle':
                sql = 'SELECT * FROM ' + self.schema_name + '.' + tab_name + ' WHERE ROWNUM<%s'%str(head_num+1)
            else:
                sql = 'SELECT top %s * FROM '%str(head_num) + tab_name + ' ;'
        else:
            # Get all the data
            if self.db_type == 'mysql':
                sql = 'SELECT * FROM ' + tab_name + ' ;'  # 获取表数据
            elif self.db_type == 'oracle':
                sql = 'SELECT * FROM ' + self.schema_name+'.'+tab_name + ' ;'  # 获取表数据
            else:
                sql = 'SELECT * FROM ' + tab_name + ' ;'  # 获取表数据
        self.cur.execute(sql)
        rets = self.cur.fetchall()
        # print(rets)
        # get the column name
        col_name = list(db_query.ob_colinfo(self,tab_name)[0])
        if len(rets):
            ob_tabdata = pd.DataFrame(list(rets), columns=col_name)  # Get the data and convert it to dateframe format
        else:
            ob_tabdata = pd.DataFrame(columns=col_name) # If there is no data, an empty dataframe is generated

        # This function is used to solve the problem of SqlServer data coding.
        def deal_str(x):
            if isinstance(x,str):
                return x.encode('latin-1').decode('gbk')
        if self.db_type == 'sqlserver':
            df_col = db_query.ob_colinfo(self, tab_name)
            print('df_col',df_col)
            data_type_tran = list(df_col[df_col[1]!='nvarchar'][0]) # Exclude nvarchar types
            ob_tabdata = ob_tabdata[data_type_tran].applymap(deal_str)

        return ob_tabdata

    def create_hivetab(self,tab_name,table_type):
        """
        When you want to put data from other databases into hive,
        it is used to generate SQL statements to build tables in hive.
        :param tab_name:str,table name in the original database
        :param table_type:int,0 means to build an intermediate table in hive,
        1 means to build a transaction table in hive
        :return:SQL statement
        """
        if table_type == 0:
            sql_create1 = 'CREATE TABLE IF NOT EXISTS `%s_M`(' % tab_name
        else:
            sql_create1 = 'CREATE TABLE IF NOT EXISTS `%s`(' % tab_name

        related_dic = {'int': 'INT', 'varchar': 'STRING', 'text': 'STRING',
                       'datetime': 'TIMESTAMP', 'longtext': 'STRING',
                       'bigint': 'BIGINT', 'timestamp': 'TIMESTAMP',
                       'char': 'STRING', 'decimal': 'DECIMAL',
                       'number': 'INT', 'varchar2': 'STRING',
                       'date': 'TIMESTAMP','float':'FLOAT','nvarchar':'STRING',
                       'nvarchar2':'STRING'}  # Dictionary of corresponding field type
        # Get field information
        df_col = db_query.ob_colinfo(self,tab_name)

        temp = df_col[0].map(lambda x: '`' + x + '`')
        temp1 = df_col[1].map(lambda x: related_dic[x.lower()])
        temp2 = df_col[2].map(lambda x: 'comment' + ' \'' + x + '\',' if x is not None else ',')

        sql_create2 = str()
        for i in range(temp.shape[0]):
            sql_create2 += temp[i] + ' ' + temp1[i] + ' ' + temp2[i] + '\n'

        # Gets the comment for the table
        comments_tab = db_query.ob_tabcom(self,tab_name)

        if comments_tab:
            sql_create = sql_create1 + sql_create2[:-2] + ')comment \'%s\'' % comments_tab
        else:
            sql_create = sql_create1 + sql_create2[:-2] + ')'

        sql_end0 = "ROW FORMAT DELIMITED FIELDS TERMINATED BY \",\""
        sql_end1 = "CLUSTERED BY (*column_name*) INTO *bucket_num* BUCKETS " \
                   "STORED AS ORC TBLPROPERTIES (\"transactional\"=\"true\")"

        if table_type == 0:
            sql_create_end = sql_create + sql_end0
        else:
            sql_create_end = sql_create + sql_end1

        return sql_create_end

    def con_close(self):
        """
        Close the connection
        """
        self.cur.close()
        self.conn.close()
        print('already closed!')


