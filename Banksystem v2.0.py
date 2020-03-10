from enum import Enum, unique
import pymysql      # 连接数据库
import os           # i = os.systen('cls')清空屏幕


# input your mysql info here
@unique
class Mysql_info(Enum):
    host = '***'		
    user = '***'
    password = '***'
    db = '***'
    port = ***
    charset = 'utf8'

class User(object):
    '''用户类'''
    user_dic = {}
    def __init__ (self, account, password,\
                  balance, identity = 0, frozen = 0):       # 初始化信息，
        self.account = account      # 账户
        self.password = password    # 密码
        self.balance = balance      # 余额
        self.identity = identity    # 身份认证，0 - 普通；1 - 贵宾
        self.frozen = frozen        # 冻结账户，0 - 正常；1 - 冻结
        self.user_dic[account] = self   # 储存自身信息，以便再次调用。

    def check_user(self, check_account):
        # 检查用户名是否存在列表中
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        sql = '''
        select name from user
        '''     # SQL语句，选出所有的账户名
        user_list = []
        my_cursor.execute(sql)
        info = my_cursor.fetchall()
        for i in info:
            user_list.append(i[0])
        if check_account in user_list:        # 如果存在这个用户名
            sql2 = '''
            select * from user
            where name = '%s'
            ''' %check_account
            my_cursor.execute(sql2)
            account_info = my_cursor.fetchall()
            account = account_info[0][1]
            password = account_info[0][2]
            balance = account_info[0][3]
            identity = account_info[0][4]
            frozen = account_info[0][5]
            my_cursor.close()
            bankdb.close()
            return account, password, balance, identity, frozen
            # 如果存在，返回账户所有信息
        else:
            my_cursor.close()
            bankdb.close()
            return None, None, None, None, None        # 如果不存在，返回全部为None

    def show_money(self, money):
        # print(money)
        # 大写展示金额
        num_dic = {
        1: '壹',2: '贰',3: '叁',4: '肆',5: '伍',
        6: '陆',7: '柒',8: '捌',9: '玖',0: '〇'
        }
        smallunit_list = ['', '十', '百', '千']
        bigunit_dic = {0:'', 1:'万', 2:'亿', 3:'兆', 4:'京', 5:'垓'}
        str = money.split('.')[0]
        str_dot = money.split('.')[1]
        list1 = list(str[::-1]) # 一个倒序数列
        # print(list1)
        list2 = []  # 逗号分隔的数字
        for i in range(len(list1)):
            list2.append(list1[i])
            if i % 3 == 2 and i != len(list1) - 1:
                list2.append(',')
        str2 = ''.join(list2)[::-1]+'.'+str_dot # 用逗号分隔的数字
        # print(str2)

        list3 = []  # 大写的数字
        times = int(len(list1)/4)
        for i in range(times + 1):
            if i != 0:
                list3.append(' ')
                list3.append(bigunit_dic[i])
            list_new = list1[i * 4: i * 4 + 4]
            for j in range(len(list_new)):
                # print(j)
                if j != 0 and list_new[j] != '0':
                    list3.append(smallunit_list[j])
                list3.append(num_dic[int(list_new[j])])
        list3 = list3[::-1]
        # print(list3)
        pop_list = []
        if list3[0] in ['万', '亿', '兆', '京', '垓']:
            pop_list.append(0)
        for i in range(len(list3)):
            # print(list3[i])
            if list3[i] == list3[i - 1]:
                pop_list.append(i-1)
            if list3[i] in ['万', '亿', '兆'] and list3[i - 1] == '〇':
                pop_list.append(i-1)
            if list3[i] == '零' and list3[i-1] in ['十', '百', '千']:
                pop_list.append(i-1)
            if i == len(list3) and list3[i] == '〇':
                pop_list.append(i)
        list_new = [list3[i] for i in range(len(list3)) if i not in pop_list]
        if list_new[-1] == '〇':
            list_new.pop()
        list_new.append('元 ')
        if str_dot[0] == '0' and str_dot[1] == '0':
            s = '整'
            list_new.append(s)
        elif str_dot[0] != '0' and str_dot[1] == '0':
            s = num_dic[int(str_dot[0])] + '角'
            list_new.append(s)
        elif str_dot[0] == '0' and str_dot[1] != '0':
            s = num_dic[int(str_dot[1])] + '分'
            list_new.append(s)
        else:
            s = num_dic[int(str_dot[0])] + '角' + num_dic[int(str_dot[1])] + '分'
            list_new.append(s)
        str3 = ''.join(list_new)
        return str2, str3

    def log_in(self):
        # 登陆
        i = os.system('cls')
        account = input('请输入账户，输入“exit”退出：')
        if account == 'exit':       # 输入exit拦截函数并跳出
            return
        account, correct_password, balance, identity, frozen_status = self.check_user(account)
        # 读取用户名，密码，余额，身份认证，冻结状态
        if account != None:
            count = 0       # 登陆次数计数器，超过3次跳出。
            while count < 3:
                # correct_password, frozen_status = self.get_password(account)
                i = os.system('cls')
                print('请输入账户，输入“exit”退出：%s' %account)
                if frozen_status == 1:
                    print('对不起，您的账户已被冻结。详情请咨询管理员。')
                    input('输入回车继续。')
                    return      # 如果账户被冻结，拦截函数并返回。
                input_password = input('请输入密码，输入“exit”退出：')
                if input_password == 'exit':
                    return      # 输入exit，拦截函数并退出。
                if input_password == correct_password:  # 登陆成功
                    # print(gLog_in_status)         # 调试检测专用
                    input('登陆成功！输入回车继续。')
                    return account, correct_password, balance, identity, frozen_status
                    # 登陆成功，拦截函数
                    # 登陆成功后返回帐号信息，用于在menu菜单创建对象。
                else:   # 密码错误
                    print('密码错误，请重试。\n------------------------------')
                    input('输入回车继续')
                    count += 1
            else:
                input('密码输入错误3次，账户锁定。输入回车退出。')
                exit()      # 锁定账户并直接退出程序
        else:
            input('账户不存在，请先注册。输入回车继续。')
            return      # 账户不存在，拦截函数，跳出函数。

    def regist(self):
        # 注册
        i = os.system('cls')
        count = 0
        while True:        # 用户名确认循环，尝试3次跳出循环
            new_account = input('请输入账户，输入“exit”退出：')
            account = self.check_user(new_account)[0]
            if new_account == 'exit':
                return      # exit拦截函数，跳出函数
            if new_account == '' or new_account == None:    # new_account为空时拦截
                i = os.system('cls')
                print('对不起，账户名不能为空。请重试。\n------------------------------')
                continue                            # 拦截循环，重新输入。
            if account != None:        # new_account已存在时拦截
                i = os.system('cls')
                print('抱歉，用户名已存在，请重新输入。\n------------------------------')
                continue                            # 拦截循环，重新输入
            else:
                break       # 如用户名没问题则跳出循环

        count_1 = 0
        while count_1 < 3:      # 密码确认循环，尝试3次跳出循环
            i = os.system('cls')
            print('请输入账户，输入“exit”退出：%s\n------------------------------' %new_account)
            password = input('请输入密码，输入“exit”退出：')
            if password == 'exit':
                return      # 输入exit拦截函数并退出
            if len(password) < 6 or len(password) > 32:
                input('密码不能小于6位或大于32位，输入回车继续。')
                count_1 += 1
                if count_1 == 3:
                    break       # 如果错误达3次，提前拦截
                continue        # 如果密码小于6位，拦截函数并重新进入循环。
            cpssword = input('请确认密码：')
            if password == cpssword:
                input('注册成功！输入回车继续。')
                # print(new_account, password)      # 调试检测专用
                break       # 注册成功调处循环，进入数据储存模块。
            else:
                input('两次输入密码不一致，输入回车继续。')
                count_1 += 1
                if count_1 == 3:
                    break       # 如果错误达3次，提前拦截
                continue
        if count_1 == 3:        # 当count_1 = 3时拦截
            input('------------------------------\n错误已达3次，强制退出。输入回车继续。')
            return      # 错误达到3次，拦截函数并退出。

        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        sql = '''
        insert into user(name, password, balance, identity, frozen)
        values
        ('%s', '%s', 0, 0, 0)
        ''' %(new_account, password)    # SQL语句，选出所有的账户名
        try:
            my_cursor.execute(sql)
            bankdb.commit()
        except:
            bankdb.rollback()
        my_cursor.close()
        bankdb.close()
        return

    def top_up(self):
        # 存款
        while True:     # 输入检验循环
            i = os.system('cls')
            print('存款')
            print('注意：输入的数额必须为100的整数倍，输入“0”退出。')
            amount_input = input('请输入存入的数额：')
            if amount_input == '0':
                return      # 输入0拦截函数并跳出
            try:
                amount = int(amount_input)
            except:
                input('------------------------------\n输入有误。输入回车继续。')
                continue        # 输入有误时，拦截函数，回到循环开头。
            if amount % 100 != 0 or amount < 0:
                input('------------------------------\n必须为100的整数倍，且必须大于0。输入回车继续。')
                continue        # 输入有误时，拦截函数，回到循环开头。
            else:
                number, chnumber = self.show_money(format(amount, '.2f'))
                print('------------------------------\n您要存款的金额为%s\n大写：%s\n'%(number, chnumber))
                choice = input('输入"Y"确认取款，输入其它重新输入金额：')
                if choice == 'Y':
                    break
                    # 通过检测循环，进入取款环节。
                else:
                    continue
        # 如果函数未被拦截，进入更改余额环节。
        self.balance += amount
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        sql = '''
        update user set balance = %s
        where name = '%s'
        '''%(self.balance, self.account)
        try:
            my_cursor.execute(sql)
            bankdb.commit()
            print('存款成功！您的余额为%s\n------------------------------' %self.balance)
            input('存款成功！输入回车继续。')
        except:
            # print(1)        # 测试检验专用
            input('存款失败！输入回车继续。')
            bankdb.rollback()
        my_cursor.close()
        bankdb.close()

    def draw(self):
        # 取款
        while True:         # 输入检测循环
            i = os.system('cls')
            print('存款')
            print('注意：输入的数额必须为100的整数倍，输入“0”退出。')
            amount_input = input('请输入取款的金额：')
            if amount_input == '0':
                return      # 输入0拦截函数并跳出
            try:
                amount = int(amount_input)
            except:
                input('------------------------------\n输入有误。输入回车继续。')
                continue        # 输入有误时，拦截循环。
            if amount % 100 != 0 or amount < 0:
                input('------------------------------\n必须为100的整数倍，且大于0。输入回车继续。')
                continue        # 输入有误时，拦截循环。
            if amount > self.balance:
                input('------------------------------\n您的余额不足。输入回车继续。')
                continue        # 余额不足时，拦截循环并重新开始
            else:
                number, chnumber = self.show_money(format(amount, '.2f'))
                print('------------------------------\n您要取款的金额为%s\n大写：%s\n'%(number, chnumber))
                choice = input('输入"Y"确认取款，输入其它重新输入金额：')
                if choice == 'Y':
                    break
                    # 通过检测循环，进入取款环节。
                else:
                    continue
        self.balance -= amount
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        sql = '''
        update user set balance = %s
        where name = '%s'
        '''%(self.balance, self.account)
        try:
            my_cursor.execute(sql)
            bankdb.commit()
            print('取款成功！您的余额为%s\n------------------------------'%self.balance)
            input('输入回车继续。')
        except:
            # print(1)        # 测试检验专用
            bankdb.rollback()
        my_cursor.close()
        bankdb.close()

    def show_balance(self):
        # 显示余额
        i = os.system('cls')
        print('显示余额')
        number, chnumber = self.show_money(format(self.balance, '.2f'))
        print('您的余额为：%s人民币\n大写：%s\n------------------------------'%(number, chnumber))
        input('输入回车继续。')

    def update_password(self):
        # 修改密码
        count = 0       # 修改次数计数
        while count < 3:
            i = os.system('cls')
            print('修改密码')
            old_password = input('请输入原密码，输入“exit”退出：')
            if old_password == 'exit':
                return      # 输入exit拦截函数并跳出
            if old_password != self.password:
                input('密码输入错误，请重试')
                count += 1
                continue    # 密码输入错误，拦截循环，重新开始。
            else:
                break   # 若密码正确，跳出循环，进入下一环节
        else:
            print('------------------------------\n密码输入错误超过3次，账户已锁定。')
            input('输入回车继续。')
            return      # 密码输入错误3次，拦截函数并退出。

        count_1 = 0
        while count_1 < 3:
            i = os.system('cls')
            print('修改密码')
            new_password = input('请输入新密码，输入“exit”退出：')
            if new_password == 'exit':
                return      # 输入exit拦截函数并跳出
            if len(new_password) < 6 or len(new_password) > 32:
                print('密码不能小于6位或大于32位，请重试。\n------------------------------')
                count_1 += 1
                input('输入回车继续')
                continue    # 输入错误，则拦截循环，重新开始。
            # 如果没有问题，进入确认密码环节
            new_cpssword = input('请确认新密码：')
            if new_cpssword != new_password:
                print('两次输入密码不一致，请重试。\n------------------------------')
                count_1 += 1
                input('输入回车继续')
                continue
            else:
                break   # 如果输入密码一致，跳出循环。
        else:
            input('输入失败超过3次，修改失败。输入回车继续。')
            return      # 失败3次后拦截函数并跳出。
        # 进入修改数据库密码环节
        self.password = new_password    # 修改自身对象密码
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        sql = '''
        update user set password = '%s'
        where name = '%s'
        '''%(self.password, self.account)
        try:
            my_cursor.execute(sql)
            print('密码修改成功！')
        except:
            bankdb.rollback()
        bankdb.commit()
        my_cursor.close()
        bankdb.close()
        return 1        # 修改成功返回1

    def transfer(self):
        # 转账
        while True:
            i = os.system('cls')
            print('转账')
            target_account = input('请输入对方账户，输入“exit”退出：')
            if target_account == 'exit':
                return  # 输入exit拦截函数并跳出
            account = self.check_user(target_account)[0]
            if account == None:
                print('该账户不存在，请确认后重新输入。')
                input('输入回车继续。')
                continue    # 账户不存在，回到循环开头。
            # 如果未被拦截，进入确认环节。
            i = os.system('cls')
            print('转账')
            check_account = input('请确认对方账户，输入“exit”退出：')
            if check_account != target_account:
                print('两次输入的账户不同，请确认。')
                input('------------------------------\n输入回车继续。')
                continue    # 如果两次输入账户不同，拦截循环，并回到开头。
            break   # 如果通过检测，则结束循环，进入转账环节。
        while True:
            i = os.system('cls')
            print('转账')
            print('您要转入的账户为：%s'%target_account)
            print('请再次确认目标账户，谨防转错或受骗上当！\n------------------------------')
            amount = input('请输入要转账的金额，输入“0”退出：')
            if amount == 'exit':
                return      # 输入0拦截函数并退出
            if len(amount.split('.')) == 2:
                # 如果有小数点，小数点后大于2位也拦截
                if len(amount.split('.')[1]) > 2:
                    print('------------------------------\n输入有误，必须输入正确的数字。')
                    input('输入回车继续。')
                    continue    # 输入有误则拦截函数，回到开头。
            try:
                money = float(amount)
                fmoney = format(money, '.2f')
            except:
                print('------------------------------\n输入有误，必须输入正确的数字。')
                input('输入回车继续。')
                continue    # 输入有误则拦截函数，回到开头。
            # 输入检测
            if money > self.balance:
                print('------------------------------\n余额不足，请确认。')
                input('输入回车继续')
                continue    # 输入有误则拦截函数，回到开头。
            number, chnumber = self.show_money(fmoney)
            print('------------------------------\n您要转账的金额为:%s\n大写：%s'%(number, chnumber))
            input('输入回车继续')
            break
            # 如果通过检验，则跳出循环，来到更新数据环节。
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        sql1 = '''
        update user set balance = balance - %s
        where name = '%s'
        '''%(money, self.account)
        sql2 = '''
        update user set balance = balance + %s
        where name = '%s'
        '''%(money, target_account)
        try:
            my_cursor.execute(sql1)
            my_cursor.execute(sql2)
            bankdb.commit()
            print('转账成功！您的余额为%s'%(self.balance - money))
            input('输入回车继续。')
        except:
            input('转账失败，请检查！输入回车继续。')
            bankdb.rollback()
        self.balance = self.balance - money
        my_cursor.close()
        bankdb.close()

    def log_out(self):
        # 登出
        pass

class Manager(object):
    '''管理员类'''
    manager_dic = {}
    def __init__ (self, account, password, balance = 0, identity = None, frozen = 0):
        self.account = account
        self.password = password
        self.balance = balance
        self.identity = identity
        self.frozen = frozen
        self.manager_dic[account] = self

    def check_manager(self, manager_account):
        # 检查管理员用户名否存在列表中
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        sql = '''
        select name from manager
        '''     # SQL语句，选出所有的账户名
        manager_list = []       # 储存管理员用户名的列表
        my_cursor.execute(sql)
        info = my_cursor.fetchall()
        for i in info:  # 将提取的用户名储存入列表
            manager_list.append(i[0])
        if manager_account in manager_list:        # 如果存在这个用户名
            sql2 = '''
            select * from manager
            where name = '%s'
            ''' %manager_account
            my_cursor.execute(sql2)
            account_info = my_cursor.fetchall()
            account = account_info[0][1]
            password = account_info[0][2]
            identity = account_info[0][4]
            frozen = account_info[0][5]
            my_cursor.close()
            bankdb.close()
            return account, password, identity, frozen        # 如果存在，返回1
        else:
            my_cursor.close()
            bankdb.close()
            return None, None, None, None        # 如果不存在，返回全部为None

    def check_user(self):
        # 检索所有用户
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        sql = '''
        select name from user
        '''
        my_cursor.execute(sql)
        info = my_cursor.fetchall()
        user_list = []
        for i in info:
            user_list.append(i[0])
        my_cursor.close()
        bankdb.close()
        return user_list    # 返回一个用户名组成的列表

    def log_in(self):
        i = os.system('cls')
        login_account = input('请输入管理员名，输入“exit”退出：')
        if login_account == 'exit':
            return      # 输入exit拦截函数
        account, correct_password, identity, frozen = self.check_manager(login_account)
        # 提取管理员名，正确密码，身份认证，冻结状态。
        if account == None:
            input('该管理员不存在。输入回车继续。')
            return      # 管理员不存在，拦截函数并退出
        if frozen == 1:
            print('对不起，该管理员账户已被冻结。请向张子奇咨询。')
            input('输入回车继续。')
            return      # 账户被冻结，拦截函数并退出。
        count = 0   # 密码输入计数器
        while count < 3:
            i = os.system('cls')
            print('请输入管理员名，输入“exit”退出：%s' %login_account)
            input_password = input('请输入密码，输入“exit”退出：')
            if input_password == 'exit':
                return
                # 接收到exit，拦截函数并退出
            if input_password == correct_password:
                input('------------------------------\n登陆成功！输入回车继续。')
                return account, correct_password, identity, frozen
                # 登陆成功，返回账户信息，用以在菜单中创建类
            else:
                input('------------------------------\n密码错误，请重试。输入回车继续。')
                count += 1
                continue
        else:
            input('------------------------------\n错误达3次，账户已被锁定。')
            return
        # 密码输错3次，锁定账户并退出。

    def show_infos(self, identity):
        # 显示所有用户信息
        # 只有等级为30显示密码
        i = os.system('cls')
        print('显示用户信息')
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        sql = '''
        select name, password, balance, identity, frozen from user
        '''
        my_cursor.execute(sql)
        info = my_cursor.fetchall()
        my_cursor.close()
        bankdb.close()
        # print(info)       # 调试检测专用

        # 提取各字段长度
        def get_lenth(column):
            list = []
            if column == 0:
                list.append(4)
            elif column == 1:
                list.append(8)
            elif column == 2:
                list.append(7)
            for i in info:
                list.append(len(str(i[column])))
            return max(list)
        name_lenth = get_lenth(0)
        password_lenth = get_lenth(1)
        balance_lenth = get_lenth(2)
        # print(name_lenth, password_lenth, balance_lenth)      # 调试检测专用
        # print(len(str(info[0][2])))                           # 调试检测专用

        # 数据显示模块
        if identity == 30:  # 权限为30时
            width = '+' + '-'*(name_lenth + 2) + '+' + '-'*(password_lenth + 2) \
                     + '+' + '-'*(balance_lenth + 2) + '+' + '-'*10 + '+' + '-'*8 + '+'
            title = '|' + ' name' + ' '*(name_lenth - 3) + \
                    '|' + ' password' + ' '*(password_lenth - 7) +\
                    '|' + ' balance' + ' '*(balance_lenth - 6) +\
                    '| identity | frozen |'
            print(width)
            print(title)
            print(width)

            #
            for i in info:
                content = '| ' + i[0] + ' '*(name_lenth - len(i[0]) + 1) +\
                          '| ' + i[1] + ' '*(password_lenth - len(i[1]) + 1) +\
                          '| ' + str(i[2]) + ' '*(balance_lenth - len(str(i[2])) + 1) +\
                          '| ' + str(i[3]).center(9, ' ') +\
                          '| ' + str(i[4]).center(7, ' ') + '|'

                print(content)
            print(width)
        else:       # 权限不为30时
            width = '+' + '-'*(name_lenth + 2) + '+' + '-'*10 \
                     + '+' + '-'*(balance_lenth + 2) + '+' + '-'*10 + '+' + '-'*8 + '+'
            title = '|' + ' name' + ' '*(name_lenth - 3) + \
                    '|' + ' password' + ' ' +\
                    '|' + ' balance' + ' '*(balance_lenth - 6) +\
                    '| identity | frozen |'
            print(width)
            print(title)
            print(width)

            for i in info:
                content = '| ' + i[0] + ' '*(name_lenth - len(i[0]) + 1) +\
                          '| ' + ' ******  ' +\
                          '| ' + str(i[2]) + ' '*(balance_lenth - len(str(i[2])) + 1) +\
                          '| ' + str(i[3]).center(9, ' ') +\
                          '| ' + str(i[4]).center(7, ' ') + '|'
                print(content)
            print(width)
        print('| identity:   0 - 普通用户     1 - 贵宾'+' ' *(len(width) -40) + '|' +\
            '\n| frozen:     0 - 正常         1 - 冻结'+' ' *(len(width) -40) + '|')
        print('+' + '-'* (len(width)-2) + '+')
        input('输入回车继续。')

    def freeze_user(self, identity):
        i = os.system('cls')
        if identity == 10:
            print('您没有冻结用户的权限。')
            input('输入回车继续。')
            return  # 如果没有权限，拦截函数并退出
        user_list = self.check_user()
        # 进入用户状态查询
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        while True:
            i = os.system('cls')
            print('冻结用户')
            target_account = input('请输入要冻结的账户名，输入“exit”退出：')
            if target_account == 'exit':
                my_cursor.close()
                bankdb.close()
                return      # 输入“exit”退出
            if target_account not in user_list:
                print('该账户不存在，请确认。\n------------------------------')
                input('输入回车继续。')
                my_cursor.close()
                bankdb.close()
                return  # 输入的账户不存在，拦截函数并退出
            sql1 = '''
            select frozen from user where name = '%s'
            '''%target_account
            my_cursor.execute(sql1)
            info = my_cursor.fetchall()
            if info[0][0] == 1:
                print('该账户已被冻结。\n------------------------------')
                input('输入回车继续。')
                my_cursor.close()
                bankdb.close()
                return  # 查询到账户已被冻结，拦截函数并退出。
            break   # 如果未被拦截，则跳出循环，进入确认环节。
        while True:     # 冻结对象确认
            i = os.system('cls')
            print('冻结用户')
            print('请输入要冻结的账户名，输入“exit”退出：%s'%target_account)
            check_account = input('请确认要冻结的账户名：')
            if target_account != check_account:
                print('------------------------------\n两次输入账户不一致，请确认。')
                input('输入回车继续。')
                continue    # 输入不一致，则重新开始循环。
            break   # 如无问题，跳出循环
        # 进入修改状态环节
        sql2 = '''
        update user set frozen = 1 where name = '%s'
        ''' %target_account
        try:
            my_cursor.execute(sql2)
            input('------------------------------\n冻结成功！输入回车继续。')
        except:
            bankdb.rollback()
            input('------------------------------\n冻结失败，请查询权限。')
        bankdb.commit()
        my_cursor.close()
        bankdb.close()

    def unfreeze_user(self, identity):
        # 解冻账户
        i = os.system('cls')
        if identity == 10:
            print('您没有解冻用户的权限。')
            input('输入回车继续。')
            return      # 没有权限，则拦截函数并退出。
        user_list = self.check_user()
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        while True:
            i = os.system('cls')
            print('解冻用户')
            target_account = input('请输入要解冻的账户名，输入“exit”退出：')
            if target_account == 'exit':
                my_cursor.close()
                bankdb.close()
                return  # 输入exit，拦截函数并退出
            if target_account not in user_list:
                print('该账户不存在，请确认。\n------------------------------')
                input('输入回车继续。')
                my_cursor.close()
                bankdb.close()
                return  # 账户不存在，拦截函数并退出
            sql1 = '''
            select frozen from user where name = '%s'
            '''%target_account
            info = my_cursor.execute(sql1)
            info = my_cursor.fetchall()
            if info[0][0] == 0:
                print('该账户状态为正常。\n------------------------------')
                input('输入回车继续')
                my_cursor.close()
                bankdb.close()
                return      # 状态正常，拦截函数并退出。
            break   # 如果未被拦截，则跳出循环，进入确认环节
        while True:     # 解冻对象确认
            i = os.system('cls')
            print('解冻用户')
            print('请输入要解冻的账户名，输入“exit”退出：%s'%target_account)
            check_account = input('请确认要解冻的账户名：')
            if check_account != target_account:
                print('------------------------------\n两次输入账户不一致，请确认。')
                input('输入回车继续。')
                continue    # 输入不一致，则重新开始循环。
            break       # 如无问题，跳出循环，来到数据修改环节。
        sql2 = '''
        update user set frozen = 0 where name = '%s'
        '''%target_account
        try:
            my_cursor.execute(sql2)
            bankdb.commit()
            input('------------------------------\n解冻成功！输入回车继续。')
        except:
            bankdb.rollback()
            input('------------------------------\n解冻失败，请查询权限。')
        my_cursor.close()
        bankdb.close()

    def update_password(self):
        # 修改密码
        count = 0       # 密码输入次数计数
        while count < 3:
            i = os.system('cls')
            print('修改密码')
            old_password = input('请输入原密码，输入“exit”退出：')
            if old_password == 'exit':
                return      # 输入exit拦截函数并跳出
            if old_password != self.password:
                input('密码输入错误，请重试')
                count += 1
                continue    # 密码输入错误，拦截循环，重新开始。
            else:
                break   # 若密码正确，跳出循环，进入下一环节
        else:
            print('------------------------------\n密码输入错误超过3次，账户已锁定。')
            input('输入回车继续。')
            return      # 密码输入错误3次，拦截函数并退出。

        count_1 = 0
        while count_1 < 3:
            i = os.system('cls')
            print('修改密码')
            new_password = input('请输入新密码，输入“exit”退出：')
            if new_password == 'exit':
                return      # 输入exit拦截函数并跳出
            if len(new_password) < 6 or len(new_password) > 32:
                print('密码不能小于6位或大于32位，请重试。\n------------------------------')
                count_1 += 1
                input('输入回车继续')
                continue    # 输入错误，则拦截循环，重新开始。
            # 如果没有问题，进入确认密码环节
            new_cpssword = input('请确认新密码：')
            if new_cpssword != new_password:
                print('两次输入密码不一致，请重试。\n------------------------------')
                count_1 += 1
                input('输入回车继续')
                continue
            else:
                break   # 如果输入密码一致，跳出循环。
        else:
            input('输入失败超过3次，修改失败。输入回车继续。')
            return      # 失败3次后拦截函数并跳出。
        # 进入修改数据库密码环节
        self.password = new_password    # 修改自身对象密码
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        sql = '''
        update manager set password = '%s'
        where name = '%s'
        '''%(self.password, self.account)
        try:
            my_cursor.execute(sql)
            print('------------------------------\n密码修改成功！')
        except:
            bankdb.rollback()
        input('输入回车继续。')
        bankdb.commit()
        my_cursor.close()
        bankdb.close()
        return 1        # 修改成功返回1

    def log_out(self):
        # 登出
        pass

class Boss(Manager):
    # boss类，继承Manager的方法
    # 多出增加、冻结、解冻管理员方法。
    boss_dic = {}
    def __init__ (self, account, password, balance = 0, identity = 30, frozen = 0):
        self.account = account
        self.password = password
        self.balance = balance
        self.identity = identity
        self.frozen = frozen
        self.boss_dic[account] = self

    def show_managers(self):
        i = os.system('cls')
        print('显示管理员')
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        sql = '''
        select name, password, identity, frozen from manager
        '''
        my_cursor.execute(sql)
        info = my_cursor.fetchall()
        def get_lenth(column):
            # 提取各字段长度
            list = []
            if column == 1: # 账户名长度
                list.append(4)
            elif column == 2:   # 密码长度
                list.append(8)
            elif column == 3:   # 权限长度
                list.append(7)
            elif column == 4:   # 冻结状态长度
                list.append(6)
            for i in info:
                list.append(len(i[column - 1]))
            return max(list)    # 返回单列最大值
        name_lenth = get_lenth(1)
        password_lenth = get_lenth(2)
        width = '+' + '-' * (name_lenth + 2) +\
                '+' + '-' * (password_lenth + 2) +\
                '+' + '-' * 10  +\
                '+' + '-' * 8 + '+'
        head = '|' + ' name' + ' ' * (name_lenth - 3) +\
               '|' + ' password' + ' ' * (password_lenth  - 7) +\
               '| identity | frozen |'
        print(width)
        print(head)
        print(width)
        for i in info:
            content = '| ' + i[0] + ' ' * (name_lenth - len(i[0])+1) +\
                      '| ' + i[1] + ' ' * (password_lenth - len(i[1])+1) +\
                      '|' + str(i[2]).center(10, ' ') +\
                      '| ' + str(i[3]).center(7, ' ') + '|'
            print(content)
        print(width)
        tip = '| identity:  10 - 初级    20 - 中级' + ' ' * (len(width) - 36) + '|\n' +\
              '| frozen:     0 - 正常     1 - 冻结' + ' ' * (len(width) - 36) + '|'
        print(tip)
        print('+' + '-' * (len(width) - 2) + '+')
        my_cursor.close()
        bankdb.close()
        input('输入回车继续。')

    def check_manager(self):
        # 检索所有用户
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        sql = '''
        select name from manager
        '''
        my_cursor.execute(sql)
        info = my_cursor.fetchall()
        manager_list = []
        for i in info:
            manager_list.append(i[0])
        my_cursor.close()
        bankdb.close()
        return manager_list    # 返回一个用户名组成的列表

    def add_manager(self):
        manager_list = self.check_manager()
        while True:     # 输入账户循环
            i = os.system('cls')
            new_manager = input('请输入新的管理员名，输入“exit”退出：')
            if new_manager == 'exit':
                return  # 输入exit拦截函数并跳出
            if new_manager in manager_list: # 判断账户名是否存在
                print('该管理员名已存在，请重新输入。\n------------------------------')
                input('输入回车继续。')
                continue    # 检测到管理员名已存在，拦截循环回到开头
            if len(new_manager) < 3:    # 检测账户名长度
                print('管理员名必须大于3位，请重新输入。\n------------------------------')
                input('输入回车继续。')
                continue    # 检测到管理员名小鱼3位，拦截循环回到开头。
            break   # 如果未被拦截，则跳出输入管理员名的循环。

        while True:     # 密码输入循环
            i = os.system('cls')
            print('请输入新的管理员名，输入“exit”退出：%s'%new_manager)
            new_password = input('请输入密码，输入“exit”退出：')
            if new_password == 'exit':
                return  # 输入exit拦截函数并跳出
            if len(new_password) < 6 or len(new_password) > 32:   # 检测密码长度
                print('密码必须大于6位，小于32位。请重新输入。\n------------------------------')
                input('输入回车继续。')
                continue    # 如果密码长度小于6位，拦截循环，回到输入密码
            check_password = input('请确认密码：')
            if check_password != new_password:  # 检查两次密码输入是否一致
                print('两次输入密码不一致，请重新输入。\n------------------------------')
                input('输入回车继续。')
                continue    # 如果两次密码不一致，拦截循环，回到输入密码
            break   # 如果未被拦截，则跳出密码循环

        while True:     # 权限设置循环
            i= os.system('cls')
            print('新管理员名：%s\n请输入密码，输入“exit”退出：%s\n请确认密码：%s\n------------------------------'%(new_manager, new_password, new_password))
            print('请赋予管理员权限，10：初级管理员；20：中级管理员；30：高级管理员。')
            choice = input('请输入权限对应的编码，输入“exit”退出：')
            if choice == 'exit':
                return  # 输入exit拦截函数并跳出
            if choice == '10' or choice == '20' or choice == '30':
                new_identity = choice
                break   # 输入正确，给new_identity赋值，跳出循环
            else:
                print('输入有误，请重新输入。\n------------------------------')
                input('输入回车继续。')
                continue    # 输入有误，回到循环开头。

        # 进入数据储存环节
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        sql = '''
        insert into manager (name, password, identity, frozen) values
        ('%s', '%s', %s, 0)
        '''%(new_manager, new_password, new_identity)
        my_cursor.execute(sql)
        bankdb.commit()
        my_cursor.close()
        bankdb.close()
        print('管理员添加成功！\n------------------------------')
        input('输入回车继续。')

    def freeze_manager(self):
        # 冻结管理员权限
        i = os.system('cls')
        print('冻结管理员')
        manager_list = self.check_manager()
        bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                    db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
        my_cursor = bankdb.cursor()
        while True:
            # 确认账户权限
            target_account = input('请输入要冻结的管理员名，输入“exit”退出：')
            if target_account == 'exit':
                my_cursor.close()
                bankdb.close()
                return  # 输入exit拦截函数
            if target_account not in manager_list:  # 检测管理员是否存在。
                print('------------------------------\n该管理员不存在，请确认。')
                input('输入回车继续。')
                my_cursor.close()
                bankdb.close()
                return  # 管理员不存在，拦截函数并退出。
            sql1 = '''
            select frozen from manager where name = '%s'
            '''%target_account
            my_cursor.execute(sql1)
            info = my_cursor.fetchall()
            if info[0][0] == 1:
                print('------------------------------\n该管理员已冻结。')
                input('输入回车继续')
                my_cursor.close()
                bankdb.close()
                return  # 管理员已冻结，则拦截函数并退出。
            # 如果未被拦截，进入确认环节。
            check_target = input('请确认要冻结的管理员名：')
            if check_target != target_account:
                print('------------------------------\n两次输入的管理员名不同，请确认。')
                input('输入回车继续。')
                break   # 两次输入不一致，拦截循环，回到开头。
            break       # 如果未被拦截，跳出循环，来到修改环节。
        sql2 = '''
        update manager set frozen = 1 where name = '%s'
        '''%target_account
        try:
            my_cursor.execute(sql2)
            bankdb.commit()
            input('------------------------------\n权限冻结成功！输入回车继续。')
        except:
            bankdb.rollback()
            input('------------------------------\n冻结失败，请确认权限。输入回车继续。')
        my_cursor = bankdb.cursor()
        bankdb.close()

    def unfreeze_manager(self):
        # 解冻管理员权限
        while True:
            # 输入目标账户循环
            i = os.system('cls')
            print('解冻管理员')
            target_account = input('请输要解冻的管理员账户，输入“exit”退出：')
            if target_account == 'exit':
                return  # 输入exit拦截函数并退出
            if target_account not in self.check_manager():
                print('------------------------------\n该管理员不存在，请确认。')
                input('输入回车继续。')
                return  # 如果目标管理员不存在，拦截函数并退出。
            bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                        db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
            my_cursor = bankdb.cursor()
            sql = '''
            select frozen from manager where name = '%s'
            '''%target_account
            my_cursor.execute(sql)
            info = my_cursor.fetchall()[0][0]
            if info == 0:
                print('------------------------------\n该管理员状态正常。')
                input('输入回车继续。')
                my_cursor.close()
                bankdb.close()
                return  # 如果管理员状态正常，拦截函数并退出
            break   # 如未被拦截，跳出循环，进入修改环节。
        sql2 = '''
        update manager set frozen = 0 where name = '%s'
        '''%target_account
        try:
            my_cursor.execute(sql2)
            bankdb.commit()
            print('------------------------------\n解冻成功！')
        except:
            bankdb.rollback()
            print('------------------------------\n解冻失败，请查询权限。')
        input('输入回车继续。')
        my_cursor.close()
        bankdb.close()

    def alter_manager(self):
        # 修改管理员权限
        while True:
            i = os.system('cls')
            print('修改权限')
            target_account = input('请输入要修改权限的管理员，输入“exit”退出：')
            if target_account == 'exit':
                return  # 输入exit拦截函数并退出
            if target_account not in self.check_manager():
                print('------------------------------\n该管理员不存在，请确认。')
                input('输入回车继续。')
                return  # 用户不存在，拦截函数并退出。
            break   # 如果未被拦截，进入修改环节。
        while True:
            i = os.system('cls')
            print('修改权限')
            print('请输入要修改权限的管理员，输入“exit”退出：%s'%target_account)
            bankdb = pymysql.connect(   host = Mysql_info.host.value, user = Mysql_info.user.value, password = Mysql_info.password.value,
                                        db = Mysql_info.db.value, port = Mysql_info.port.value, charset = Mysql_info.charset.value)
            my_cursor = bankdb.cursor()
            sql = '''
            select identity from manager where name = '%s'
            '''%target_account
            my_cursor.execute(sql)
            info = my_cursor.fetchall()
            identity_dic = {
            10:'10 - 初级管理员',
            20:'20 - 中级管理员',
            30:'30 - BOSS'
            }
            print('%s目前的权限为%s'%(target_account, identity_dic[info[0][0]]))
            if info[0][0] == 30:
                print('------------------------------\n您无权修改对方的权限。')
                input('输入回车继续。')
                my_cursor.close()
                bankdb.close()
                return  # 检测到最高权限者，无权修改，退出函数。
            print('\t10 - 初级管理员\n\t20 - 中级管理员')
            new_identity = input('------------------------------\n请输入新的权限对应的编号，输入“exit”退出：')
            if new_identity == 'exit':
                my_cursor.close()
                bankdb.close()
                return
            if new_identity not in ['10', '20']:
                print('------------------------------\n输入有误，请重新输入。')
                input('输入回车继续。')
                my_cursor.close()
                bankdb.close()
                continue    # 输入有误，拦截循环，重新开始循环。
            # 如果未被拦截，进入修改环节。
            sql2 = '''
            update manager set identity = '%s' where name = '%s'
            '''%(new_identity, target_account)
            try:
                my_cursor.execute(sql2)
                bankdb.commit()
                print('------------------------------\n修改成功！')
            except:
                bankdb.rollback()
                print('------------------------------\n修改失败，请查询权限。')
            input('输入回车继续。')
            my_cursor.close()
            bankdb.close()
            return  # 修改成功，退出。

    def log_out(self):
        # 登出
        pass

class Menu(object):
    # 菜单
    def __init__(self, account = None, status = 0, identity = None):
        self.account = account          # 登陆账户，默认为None
        self.status = status            # 登陆状态，默认为0
        self.identity = identity        # 身份认证，0 - 普通会员；1 - 贵宾；
                                        # 10 - 低级管理员；20 - 中级管理员；30 - 高级管理员

    def greeting(self):
        greeting_dic = {
        0: '',
        1: '尊敬的贵宾',
        10: '1级管理员',
        20: '2级管理员',
        30: 'BOSS张子奇先生'
        }
        if self.account == None:
            return      # 如果没有账户登陆，拦截函数并退出。
        else:
            if self.identity == 30:
                if self.account == 'wyh':
                    print('亲爱的昊昊大嫂，欢迎来到张子奇的神秘世界！')
                else:
                    print('尊敬的BOSS张子奇先生，欢迎来到您创造的世界！')
            else:
                print('%s%s，您好！欢迎来到张子奇的神秘银行。' %(greeting_dic[self.identity], self.account))

    def start_menu(self):
        # 初始界面
        # 启动程序打开此界面
        while True:
            i = os.system('cls')
            print('''您好，欢迎来到张子奇的神秘银行。\n\t1、用户登陆\n\t2、用户注册\n\t3、管理员登陆\n\t0、退出\n------------------------------''')
            choice = input('请输入相应功能前的数字：')
            if choice == '1':
                user = User(account = 'guest', password = 'guest', balance = 0, identity = None, frozen = None)
                # 先创建一个临时User对象，以引用方法
                info = user.log_in()
                if info == None:
                    continue       # 如果没有返回值，返回循环开头
                else:       # 如果有返回值，接收返回值
                    user = User(info[0], info[1], info[2], info[3], info[4])
                    # 以获取到的数据创建一个user对象
                    self.account = info[0]
                    self.identity = info[3]
                    # 将登陆的帐号、登陆的身份认赋值给主菜单
                    self.user_menu()
                    # 进入用户操作界面
            elif choice == '2':
                # 用户注册
                user = User(account = 'guest', password = 'guest', balance = 0, identity = None, frozen = None)
                # 创建一个临时对象，用于执行注册程序。
                user.regist()

            elif choice == '3':
                # 管理员登陆
                manager = Manager(account = 'guest', password = 'guest', balance = 0, identity = None, frozen = 0)
                # 创建一个临时对象，用于执行登陆程序。
                info = manager.log_in()
                if info == None:
                    continue    # 如果没有返回值，返回循环开头
                else:
                    manager = Manager(account = info[0], password = info[1], balance = 0, identity = info[2], frozen = info[3])
                    # 以获取到的数据创建一个manager对象
                    self.account = info[0]
                    self.identity = info[2]
                    # 将登陆的帐号、身份认证赋值给主菜单
                    if self.identity == 30:
                        boss = Boss(account = 'zzq', password = '666666', identity = 30)
                        self.boss_menu()
                        continue       # 登出后拦截循环，回到开头
                    self.manager_menu()
                    # 进入管理员操作界面
            elif choice == '0':
                # 退出
                break
            else:
                input('输入有误，请重试。输入回车继续。')

    def user_menu(self):
        # 用户界面
        # 用户登陆跳转到此界面
        while True:
            i = os.system('cls')
            self.greeting()
            # print(User.user_dic[self.account].balance)    # 测试检验专用
            print('\t1、查询余额\n\t2、存款\n\t3、取款\n\t4、转账\n\t5、更改密码\n\t0、登出\n------------------------------')
            choice = input('请输入相应功能前的数字：')
            if choice == '1':
                # 显示余额
                User.user_dic[self.account].show_balance()
            elif choice == '2':
                # 存款
                User.user_dic[self.account].top_up()
            elif choice == '3':
                # 取款
                User.user_dic[self.account].draw()
            elif choice == '4':
                # 转账
                User.user_dic[self.account].transfer()
            elif choice == '5':
                # 更改密码
                result = User.user_dic[self.account].update_password()
                if result == 1:
                    input('修改密码后，您需要重新登陆。输入回车继续。')
                    return  # 修改密码后回到初始界面
                else:
                    pass
            elif choice == '0':
                # 登出
                User.user_dic = {}  # 清空登陆信息
                self.account = None
                self.status = 0
                self.identity = None
                return  # 拦截函数，返回初始界面
            else:
                input('输入有误，请重试。输入回车继续。')

    def manager_menu(self):
        # 管理员界面
        # 管理员登陆跳转到此界面
        while True:
            i = os.system('cls')
            self.greeting()
            print('\t1、查询用户信息（初级权限）\n\t2、冻结用户（中级权限）\n\t3、解冻用户（中级权限）\n\t4、修改密码\n\t0、登出\n------------------------------')
            choice = input('请输入相应功能对应的数字：')
            if choice == '1':
                # 查询用户信息
                Manager.manager_dic[self.account].show_infos(self.identity)
            elif choice == '2':
                # 冻结用户
                Manager.manager_dic[self.account].freeze_user(self.identity)
            elif choice == '3':
                # 解冻用户
                Manager.manager_dic[self.account].unfreeze_user(self.identity)
            elif choice == '4':
                # 修改密码
                Manager.manager_dic[self.account].update_password()
            elif choice == '0':
                # 登出
                Manager.manager_dic = {}
                self.account = None
                self.status = 0
                self.identity = None
                return      # 输入4拦截函数并退出
            else:
                input('输入有误，请重试。输入回车继续')

    def boss_menu(self):
        # 最高权限者界面
        # 检测到最高权限跳转到此界面
        while True:
            i = os.system('cls')
            self.greeting()
            # print('这里是Boss')        # 测试检验专用
            print('\t1、查询用户信息\n\t2、冻结用户\n\t3、解冻用户\n\t4、查询管理员\n\t5、管理管理员\n\t6、修改密码\n\t0、登出\n------------------------------')
            choice = input('请输入相应功能对应的数字：')
            if choice == '1':
                # 查询用户信息
                Manager.manager_dic[self.account].show_infos(self.identity)
            elif choice == '2':
                # 冻结用户
                Manager.manager_dic[self.account].freeze_user(self.identity)
            elif choice == '3':
                # 解冻用户
                Manager.manager_dic[self.account].unfreeze_user(self.identity)
            elif choice == '4':
                # 添加、冻结管理员，更改管理员权限。
                Boss.boss_dic[self.account].show_managers()
            elif choice == '5':
                # 管理管理员
                # 添加、冻结、解冻、修改权限
                while True:
                    i = os.system('cls')
                    print('操作管理员')
                    print('\t1、添加管理员\n\t2、冻结管理员\n\t3、解冻管理员\n\t4、修改管理员权限\n\t0、退出')
                    choice = input('------------------------------\n请输入相应功能前的数字。')
                    if choice == '1':
                        # 添加管理员
                        Boss.boss_dic[self.account].add_manager()
                    elif choice == '2':
                        # 冻结管理员
                        Boss.boss_dic[self.account].freeze_manager()
                    elif choice == '3':
                        # 解冻管理员
                        Boss.boss_dic[self.account].unfreeze_manager()
                    elif choice == '4':
                        # 修改管理员权限
                        Boss.boss_dic[self.account].alter_manager()
                    elif choice == '5':
                        # 查询管理员
                        Boss.boss_dic[self.account].show_managers()
                    elif choice == '0':
                        break   # 输入0退出当前菜单
                    else:
                        input('输入有误，请重试。输入回车继续。')
                        continue
            elif choice == '6':
                # 修改密码
                Manager.manager_dic[self.account].update_password()
            elif choice == '0':
                return      # 输入6拦截函数并退出
            else:
                input('输入有误，请重试。输入回车继续。')

def main():
    # user = User(account = 'guest', password = 'guest', balance = 300000, identity = 0)
    # user.transfer()
    # manager = Manager(account = 'guest', password = 'guest', identity = 10, frozen = 0)
    menu = Menu()
    menu.start_menu()

if __name__ == '__main__':
    main()
