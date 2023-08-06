# _*_ coding:utf-8 _*_
"""
tky组件 测试
\n测试文件，包含部分示例...
"""

from tky import t_sql, t_jde, t_dev, t_gui, t_msg, t_file, t_tsg


# 验证APP——GUI组件方法功能
def app_gui_test():
    appPackage = "com.xxx.app.addressbook"  # 包名
    appActivity = "com.xxx.app.addressbook.activity.WelcomeActivity"  # 包入口
    dri = t_dev.app_dev('Android', '7.1.2', 'device', appPackage, appActivity)
    print(dri)

    omr_app = "com.xxx.app.addressbook:id/Wisdom_pie_layout"  # 元素
    print(omr_app)
    t_gui.t_click('id', omr_app, dri)


# 验证PC-GUI组件方法功能
def pc_gui_test():
    url = 'https://www.baidu.com'
    dri = t_dev.pc_dev('g', url)  # 打开浏览器并进入url网页
    print(dri)
    t_gui.t_send_keys('id', 'kw', 'IP', dri)
    t_gui.t_click('xpath', '//*[@id="su"]', dri)


# 验证msg组件方法功能
def msg_test():
    wurl = 'http://localhost/service/sys/qx/send'  # 要推送的url地址
    code = '123456'  # 推送对象
    msg = '123456789123456789'  # 推送内容
    t_msg.we_msg(wurl, code, msg)


# 验证随机数生成
def test_mg():
    filename = 'test.txt'  # write txt
    # 每条信息包括：姓名、性别、年龄、籍贯、电话号码、地址、电子邮件、数学成绩、英语成绩）
    vla = '赵钱孙李周吴郑王唐余赢杜梁刘汪徐时'
    vls = '相思叶图样图森破旱田杳加盟楼主'
    vll = ('方言', '数学', '物理', '化学')
    from .t_tsg import test_msg
    with open(filename, 'w', encoding='utf-8') as fp:
        # fp.write('学号,名称,性别,年龄,籍贯,联系方式,地址,邮箱,课程,期中,期末\n')
        print('学号,名称,性别,年龄,籍贯,联系方式,地址,邮箱,课程,期中,期末\n')
        for i in range(100):
            id = test_msg.tst_num(num=6)
            name = test_msg.tst_val(vla) + test_msg.tst_val(self=vls, z_max=2)
            sex = test_msg.tst_val()
            age = test_msg.tst_num(z_min=15, z_max=30, num=1)
            native = test_msg.tst_one()
            telno = test_msg.tst_num('1', z_min=3, z_max=9)
            address = test_msg.tst_one() + test_msg.tst_val(self=vls, z_min=5, z_max=8) + '路' + test_msg.tst_num(
                num=3) + '号'
            email = test_msg.tst_email()
            student = test_msg.tst_one(vll)
            nuber1 = test_msg.tst_num(z_min=5, z_max=100, num=1)
            nuber2 = test_msg.tst_num(z_min=5, z_max=100, num=1)
            line = ','.join([id, name, sex, age, native, telno, address, email, student, nuber1, nuber2]) + '\n'
            print(line)


# 验证文件夹方法
def file_test():
    file_url = r'G:\web\test'
    furl = r'G:\web\test\test.txt'
    a = t_file.File_val.path_val(file_url, 0)
    # a = t_file.File_val.path_val(file_url)
    print(a)
    b = t_file.File_val.last_val(furl, -2)
    # b = t_file.File_val.last_val(furl )
    print(b)


# 验证文件夹方法
def excel_test():
    frl = r'G:\web\test\test.xlsx'
    # a = t_file.Excel.read_data(file_url)
    # print(a)
    b = t_file.Excel.write_data(frl, stn='Sheet1', row_n=1, dow_n=1, value='name')
    c = t_file.Excel.write_data(frl, stn='Sheet1', row_n=3, dow_n=1, value='test')
    d = t_file.Excel.write_data(frl, stn='Sheet1', row_n=1, dow_n=2, value='values')
    e = t_file.Excel.write_data(frl, stn='Sheet1', row_n=3, dow_n=2, value='test1')
    # e = t_file.Excel.write_data(file_url,stn='Sheet1',dow_n=2,value='test1')
    # e = t_file.Excel.write_data(file_url,stn='Sheet1',row_n=3,value='test1')
    print(b, c, d, e)


# 验证数据匹配方法
def msg_tst():
    b = ",'O123/one','O111/tt','t11/omm',"
    a = '123'
    c = t_jde.val_list(b, a)
    print(c)


# 验证数据SQL方法
def msg_sql():
    name = 'xxxx'
    pwd = 'xxx'
    url = 'xx.xxx.xxx.xx'
    db = 'xxxxxxx'
    cod = 3306
    p = 'xx'
    ou = 'xxx.xxx.xxx.xxx:1521/xxx'
    # 注意事项：错误1193, "Unknown system variable 'tx_isolation'"（可能是插件与数据库版本不一致导致）；1045应该是数据库账号未开通外链；
    # a = t_sql.SQL.M_conn(url, cod, name, pwd, db)
    # c = t_sql.SQL.O_conn(p, p, ou)
    # print(a)
    # osql = 'select * from xxx.xxxxxx'
    # sql = 'select * from xxx'
    # print(sql)
    # one = t_sql.SQL.set_all(sql, a)
    # one = t_sql.SQL.set_one(osql, c)
    # onel = cursor.execute(sql)
    # print(one)
    # print(onel)
    # for each in cursor.fetchone():
    #     print(each)


if __name__ == '__main__':
    # app_gui_test()
    # pc_gui_test()
    # msg_test()
    # test_mg()
    # file_test()
    # excel_test()
    msg_tst()
    # msg_sql()
