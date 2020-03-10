# Bank-system-by-ZZQ
Here are 2 versions for the banksystem. Download the file or just copy the code to your local system so that you can have a try.

Banksystem v1.1.py can be used directly with the excel file 'account_info.xlsx'. Asure that they are put in the same path!
You can log in the system by the accounts and passwords in the excel file.

The code is refactored in Banksystem v2.0.py. Two Mysql tables are new source of data, while excel file is not used any more.
Also, some interesting function is added into Banksystem v2.0.py.
Before you use the Banksystem v2.0.py, you should create a local mysql(yes, only mysql) table.
The mysql preparation code is in the text file 'mysql_preparation.txt'. 
Just login your own mysql system, choose a database, copy the code and run, and the accout info will be there.
After that, please update the mysql infomation in line 9 - 14 to your own's.

总共有2个版本的银行系统。直接复制代码到本地就可以运行。

1.1版本可以直接下载并使用，注意要与excel文件'account_info.xlsx'一同下载，并放在同一个目录下。

我将1.1版本的代码进行了重构，数据源摒弃了Excel表格，改成了Mysql中的两张表，
并且加入了一些有趣的功能，比如多级管理员、中文大写显示数字等，形成了2.0版本的银行系统。
在测试银行系统v2.0之前，你需要先建立2张mysql表作为它的数据源。
建表的语句已经放在'mysql_preparation.txt'文件中了，你只需要选择一个database，把代码复制过去然后运行就可以了。
建完表之后，记得在代码的9到14行输入你自己的数据库信息！

Thank you for your attention!
