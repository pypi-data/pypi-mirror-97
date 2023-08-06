# -*- coding: UTF-8 -*-
import os

"""配置文件模板"""
option_template = """
# ======== 运行相关 =============================
# run_path: - 运行路径，要执行的用例库/用例文件/用例的路径，主要用于快速执行某个用例或某类用例；
#           - 若要在命令行分类运行不同文件下的不同用例，请使用tag参数；若要持久化参数，请在option.yml中；
#           - 使用tag、select和exculde参数组合设置要执行的部分用例；
#  e.g. 相对路径: 'data/test/'
#  e.g. 绝对路径: 'C:/Users/admin/Desktop/test'
#  e.g. 用例文件: 'data/test/TestLogin.yml'
run_path: ~
# driver_path: 浏览器驱动的所在位置，程序会先查看driver_path的值，不为空则用path指定的值，空时先查找测试用例根目录下是否还有driver，
#              最后查找python安装目录下，建议放在用例的根目录下，默认值为空，
driver_path: ~
#
# run_mode: 运行模式
#  - default: 默认模式，单线程执行用例，适用于本地测试所有用例 <默认项>
#  - debug: 调试模式，提供逐步执行用例，适用于编写用例后的调试，
#  - effect: - 高效模式，多线程并行和多用例并发执行；
#            - 适用于部署到流水线的自动化测试，对性能有一定要求;
#            - 请在miss：XX，XX参数设置并发和并行的规则；
run_mode: 'default'
# run_time: 执行次数，用于指定测试执行轮数，不得低于1，大于10
#  - 1: <默认项>
run_time: 1
#
# rerun: 重跑用例，提供在执行一遍用例后的重跑行为，重跑轮数可在rerun_time参数中设定
#  - None: 不执行重跑 <默认项>
#  - All: 无论结果如何都重跑全部用例
#  - Fail: 只重新执行失败用例
#  - Fail_All: 只要出现失败用例即重跑全部用例
rerun: 'None'
#
# rerun_time重跑次数: 用于指定重跑轮数，不得低于1，大于10，若要禁止重跑应该设置rerun参数
#   - 1: <默认项>
rerun_time: 1
#=====================================================
# ===== 筛选用例 =======================================
# 用例筛选优先级：run_path > select > exclude > tag
# select: - 选择要执行的用例，用例选择范围为run_path参数下目录/文件，优先级见分类描述；
#         - 若目录下有多个目录层级结构，则必须指定相应的目录/文件名；
#         - 若选择的范围无效则报错；
#  e.g. 假设当前run_path为 'data/test'
#  e.g. 选择单用例: 'TestLogin::TestLoginSuccess'(上一级Suite名::Suite名::用例名)
#  e.g. 选择多用例: 'TestLogin::TestLoginSuccess, TestPhoneLoginSuccess'
#  e.g. 选择多文件下多用例: ['TestLogin::TestLoginSuccess, TestPhoneLoginSuccess', 'TestIssue::TestCreateIssue']
#  e.g. 选择多文件: ['TestLogin', 'TestIssue', 'TestWiki']
#  e.g. 选择一个在多重目录下的文件: 'mail::TestHomePage::TestLogin'(其中前两个为目录，最后一个为文件)
#  - 'All': 执行全部用例 <默认项>
select: 'All'
#
# exclude: - 排除不要执行的用例，用例排除范围为run_path参数下目录/文件，优先级见分类描述；
#          - 若目录下有多个目录层级结构，则必须指定相应的目录/文件名；
#          - 若排除的范围无效，同选择相反则会忽略；
#  e.g. 同上
#  - 'None': 不排除任何用例 <默认项>
exclude: 'None'
#
# tag标签: 选择一类标签作为用例的筛选条件
#  - 'None': 无标签 <默认项>
tag: 'None'
#========================================================
#===== 输出相关 ==========================================
# report: 输出报告的形式
#  - 'Console': 只在控制台输出结果 <默认项>
#  - 'Html_Only': 只输出html格式的测试报告
#  - 'Json_Only': 只输出json格式的结果文件
#  - 'Con_Html': 控制台和html格式都输出
report: 'Console'
#
# report_path: - 存储结果/报告文件的路径，无效路径或者文件路径则会报错；
#            - 如果report参数为'Console'，则该参数不生效；
#   - '#run_path': 同run_path相同 <默认项>
report_path: '#run_path'
# Console_mode: 控制台输出信息的风格
#  - quiet
#  - detail
#  - default
Console_mode: 'default'
"""
"""测试用例文件模板"""
suite_template = """
case: # 用例
  - name: 'test_login_success'     # name字段：用于指定用例的名称，不限制语言和格式，若经常要通过cli指令筛选用例建议用英文命名；
    desc: '测试登录某网站成功'     # description字段：用于详细描述用例，建议填写，在测试结果、报告或者错误提示中会出现；
    tag:  'smoke'     # tag字段：用于分类用例，在cli指令或option配置文件中筛选要执行的用例或标记特殊行为；
    setup:     # setup字段：用于用例前的前置条件准备，若其中的步骤执行失败，则用例直接失败，不会执行用例体，但teardown后置处理一定会执行；
      - keyword: 'open_url'     # 步骤的格式见下面case里的step
        desc: '打开要测试的网址'
        arg: '在这替换你要测试的网站'
    teardown:     # teardown字段：用于用例执行后的后置处理，无论用例的setup或步骤执行失败，teardown后置处理一定会执行；
      - keyword: 'del_cookies'     # 如该步骤，无论该用例执行失败还是成功，都要清除cookies，防止下个测试登录的用例打开的网页保留了登录状态
        desc: '清除登录状态'
    step:     # step字段：用例执行的步骤，格式如下，setup和teardown也使用同样的步骤
      - keyword: 'open_url'     # 第一种类型的step: keyword, 代表一次操作，keyword的值代表做了什么操作，可选列表见参考文档；
        desc: '打开某个网站'     # description字段： 同样用于描述为什么要做该步骤，建议填写，在测试结果、报告或者错误提示中会出现；
        arg: '在这替换你要测试的网站'     # arg字段：给出执行上述keyword操作所需要的参数，详见参考文档；
        return: 'div'    # return字段：用于给上述操作中返回的值或变量定义名称，方便在后续操作中使用，详见参考文档；
      - keyword: 'click'
        desc: '打开登录页面'
        arg: [ 'xpath', '//a[@href="/login"]', 'timeout=10' ]     # 参数分两种，1.顺序参数，大都是必要参数，即按参考文档给出的顺序直接指定的参数；
      - keyword: 'send_key'                                       #           2.关键字参数，都为非必要参数，用于指定某些特殊值，在特定情况下使用，格式如前；
        desc: '输入用户名'                                          # 参数值分三种，1. 常量，即用字符串直接给出；
        arg: [ 'id', 'user_login', 'ui_test' ]                    #            2. 引用变量，引用定义于var字段的变量，多用于引用一些多次被使用的常量或执行“数据驱动”；
      - keyword: 'send_key'                                       #            3. 运行时变量，即由关键字操作返回的变量，在执行用例时才被定义，如第二个步骤中的return字段就返回该操作查找的元素的变量；
        desc: '输入密码'
        arg: [ 'id', 'user_password', 'qwe123' ]
      - keyword: 'click'
        desc: '点击登录'
        arg: [ 'name', 'commit' ]
      - assert: 'if_title_contains'     # 第二种类型的step: assert, 代表一次断言，assert的值代表做了什么断言，可选列表见参考文档；
        desc: '验证标题变化'
        arg: '我的工作台'
var:
  - group: 'default'
    desc: '默认分组'
    remark: ~
    var:
      - name: 'prid'
        desc: '要测试的prid'
        value: '11845'
      - name: 'test_url'
        desc: '测试地址'
        value: 'https://...com'
      - name: 'api_url'
        desc: 'pi的地址'
        value: 'https://...com'
      - name: 'default_import_github_url'
        desc: '一个github仓库，用于新建导入'
        value: 'https://github.com/xxxxx'
tag: ['test', 'Regress']  # tag字段：给整个suite指定标签；
# templates:
# setup: ~
# teardown: ~
# case_setup: ~
# case_teardown: ~
"""


def create_template():
    option = 'option.yml'
    suite = 'example.yml'
    if os.path.exists(option) or os.path.exists(suite):
        print('当前已存在同名文件option.yml或suite.yml，是否覆盖!y/n')
        answer = input()
        if answer == 'y' or answer.startswith('y'):
            with open(option, 'w', encoding='utf-8') as f:
                f.write(option_template)
                print("创建了文件{}".format(option))
            with open(suite, 'w', encoding='utf-8') as f:
                f.write(suite_template)
                print("创建了文件{}".format(suite))
        else:
            print('byebye!')
    else:
        with open(option, 'w', encoding='utf-8') as f:
            f.write(option_template)
            print("创建了文件{}".format(option))
        with open(suite, 'w', encoding='utf-8') as f:
            f.write(suite_template)
            print("创建了文件{}".format(suite))
    exit()
