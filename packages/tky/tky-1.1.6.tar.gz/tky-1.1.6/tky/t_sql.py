# _*_ coding:utf-8 _*_
"""
常用SQL类集合
\n 目前支持的有：
\n SQL(O_conn/M_conn/set_one/set_all/upd_del) (SQL类，依赖cx_Oracle/pymysql)
\n Es(read_es) （ES类，依赖elasticsearch）
\n @author: 'TangKaiYue'
"""
from .t_jde import null


# SQL数据相关集合
class SQL:
    """
    【SQL数据相关集合】\n
    \n 目前已支持方法：
    \n 1、O_conn | Oracle数据库连接配置(依赖cx_Oracle)
    \n 2、M_conn | Mysql数据库连接配置(依赖pymysql)
    \n 3、set_one | 查询数据表的第一条数据
    \n 4、set_all | 查询数据表的所有数据
    \n 5、upd_del | 修改/删除数据表的数据
    """

    # Oracle数据库连接配置
    def O_conn(self: str = 'null', pwd: str = 'null', url: str = 'null'):
        """
        【Oracle数据库连接配置】（依赖cx_Oracle）\n
        :param self: str 用户名；
        :param pwd: str 密码；
        :param url: str 数据库连接(含服务名)；
        :return: 输出数据库连接结果；
        """
        try:
            # 判断必要入参
            if null(self) == 'N' or null(pwd) == 'N' or null(url) == 'N':
                return print("入参异常：连接数据库 账号、密码、URL 都不能为空...")
            else:
                import cx_Oracle  # 模块引用
                cs = cx_Oracle.connect(str(self), str(pwd), str(url), encoding="UTF-8")
                return cs
        except EnvironmentError as err:
            return '发生异常：%s' % err

    # Mysql数据库连接配置
    def M_conn(self: str = 'null', code: int = '3306', name: str = 'null', pwd: str = 'null', db: str = 'null'):
        """
        【Mysql数据库连接配置】（依赖pymysql）\n
        :param self: str 连接地址/IP；
        :param code: int 端口号，默认3306；
        :param name: str 用户名；
        :param pwd: str 密码；
        :param db: str  数据库名称；
        :return: 输出数据库连接结果；
        """
        try:
            # 判断必要入参
            if null(self) == 'N' or null(name) == 'N' or null(pwd) == 'N' or null(db) == 'N':
                return print("入参异常：连接数据库 地址、用户、密码、库名 都不能为空...")
            else:
                import pymysql
                conn = pymysql.connect(host=str(self), port=int(code), user=str(name), passwd=str(pwd), db=str(db),
                                       charset='utf8')
                return conn
        except EnvironmentError as err:
            return '发生异常：%s' % err

    # 查询数据表的第一条数据
    def set_one(self: str = 'null', conn: str = 'null'):
        """
        【查询数据表的第一条数据】\n
        :param self: str sql语句；
        :param conn: str 数据库连接,如：SQL.O_conn()；
        :return:  输出结果；
        """
        try:
            # 判断必要入参
            if null(conn) == 'N' or null(self) == 'N':
                return print("异常：SQL语句、数据库连接值 不能为空！！！（PS:连接值可参考连接方法SQL.O_conn()）")
            else:
                if self:
                    # 获取游标
                    with conn.cursor() as cursor:
                        try:
                            cursor.execute(self)
                        except Exception as e:
                            cursor.close()  # 关闭游标
                            return print('发生异常:%s \n传入的SQL：%s; 数据连接：%s' % (e, self, conn))
                        else:
                            val_one = cursor.fetchone()
                            return val_one
        except EnvironmentError as err:
            return '发生异常：%s' % err

    # 查询数据表的所有数据
    def set_all(self: str = 'null', conn: str = 'null'):
        """
        【查询数据表的所有数据】\n
        使用注意：大量数据查询不建议使用此项功能；\n
        :param self: str sql语句；
        :param conn: str 数据库连接,如：SQL.O_conn()；
        :return:  输出结果；
        """
        try:
            # 判断必要入参
            if null(conn) == 'N' or null(self) == 'N':
                return "异常：SQL语句、数据库连接值 不能为空！！！（PS:连接值可参考连接方法SQL.O_conn()）"
            else:
                if self:
                    # 获取游标
                    with conn.cursor() as cursor:
                        try:
                            cursor.execute(self)
                        except Exception as e:
                            cursor.close()  # 关闭游标
                            return print('发生异常:%s \n传入的SQL：%s; 数据连接：%s' % (e, self, conn))
                        else:
                            val_one = cursor.fetchall()
                            v_list = list(val_one)
                            return v_list
        except EnvironmentError as err:
            return '发生异常：%s' % err

    # 修改/删除数据表的数据
    def upd_del(self: str = 'null', conn: str = 'null'):
        """
        【修改数据表的数据】\n
        :param self: str sql语句；
        :param conn: str 数据库连接,如：SQL.O_conn()；
        :return:  输出结果；
        """
        try:
            # 判断必要入参
            if null(conn) == 'N' or null(self) == 'N':
                return "异常：SQL语句、数据库连接值 都不能为空！！！（PS:连接值可参考连接方法SQL.O_conn()）"
            else:
                if self:
                    # 获取游标
                    with conn.cursor() as cursor:
                        try:
                            cursor.execute(self)  # 执行SQL
                        except Exception as err:
                            conn.rollback()  # 事务回滚（发生错误则回滚）
                            cursor.close()  # 关闭游标
                            return print('传入的SQL：%s; 数据连接：%s \n 执行异常:%s ' % (self, conn, err))
                        else:
                            conn.commit()  # 事务提交
                            update_nums = cursor.rowcount
                            return print('执行成功：', update_nums)
        except EnvironmentError as err:
            return '发生异常：%s' % err


# ES数据相关集合
class Es:
    """
    【ES数据相关集合】\n
    \n 目前已支持方法：
    \n 1、read_es | 链接ES数据并查询(依赖elasticsearch)
    """

    # 链接ES并查询
    def read_es(self, port, index, querys: str = '{ "query": { "match_all": {} } }'):
        """
        【连接es数据】\n
        :param self: es的host；
        :param port: 连接端口；
        :param index: 索引名；
        :param querys: 查询条件；
        :return: 查询结果
        """
        try:
            if null(self) == 'N' or null(port) == 'N' or null(index) == 'N':
                return print('入参异常：ES的host、端口、索引名 不可为空...')
            else:
                from elasticsearch import Elasticsearch, helpers
                url = {"host": self, "port": port, "timeout": 150}
                es = Elasticsearch([url])
                if es.ping():
                    print("Successfully connect!")
                    query = querys
                    res = helpers.scan(es, index=index, scroll="20m", query=query)
                    return res
                else:
                    print("Failed.....")
                    exit()
        except EnvironmentError as err:
            return '发生异常：%s' % err
