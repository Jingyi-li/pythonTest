import requests
from requests.auth import HTTPBasicAuth
import re
import json
from urllib.parse import urlencode
from faker import Factory
import datetime

from lxml import etree

SERVER_IP = 'http://localhost:8000/'
USER_NAME = 'admin'
USER_PASSWORD = 'skw12345'

'''
    获取html原始数据，通过keyword和regionCode，返回html文本
    返回值:
        
'''


def get_raw_html(keyword, regionCode):
    # 通过关键词获取html数据
    # http://s.weibo.com/weibo/1111&region=custom:22:1&typeall=1&suball=1&timescope=custom:2016-11-15:2016-11-16&Refer=g
    today_time = datetime.datetime.now().strftime('%Y-%m-%d')
    # print(today_time)

    # 这里面的keyword是从数据库获取过来的utf8的编码文本，类似’\u5835‘，如果直接print输出可以显示中文，但参数内部无法显示中文，需要使用quote函数进行url编码
    # keyword = urlencode(keyword).encode('utf-8')
    url = 'http://s.weibo.com/weibo/' + keyword + '&region=custom:' + regionCode + '&typeall=1&suball=1&timescope=custom:' + today_time + ':' + today_time + '&Refer=g'
    print(url)
    # 使用faker虚拟useragent
    ua = Factory.create().chrome()
    headers = {'User-Agent': ua,
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as e:
        print(datetime.datetime.now() + ' get_raw_html发生异常了:', e)

    if r.status_code == 200:
        # print(r.text)
        return r.text
    else:
        return False


'''
    分析原始数据，查看是否找到相关数据,如果找到了'noresult_tit',则证明没有搜索到数据
    返回值:
            False:未搜索到相关内容
            True:搜索到相关内容
'''


def analysis_relevant_data(html_raw_data):
    if html_raw_data:
        # noresult_tit为未找到相关结果标识
        pat = re.compile(r'noresult_tit')
        m = pat.search(html_raw_data)
        pass
        if m:
            # 没有搜索到相关结果
            # print(str(datetime.datetime.now()) + u' 没有检索到相关结果!')
            return False
        else:
            # 搜索到相关结果了
            # print(str(datetime.datetime.now()) + u' 检索到相关结果，正在分析，请稍后......')
            return True
    else:
        return False


'''
    将script中包含的json代码分割出来进行分析
'''


def split_script_html(html_raw_data):
    page = etree.HTML(html_raw_data)
    html_texts_array = page.xpath(r'//script')
    # print(html_texts_array[21].text)
    # 将额外的字串替换掉,剩下json标准格式的字串返回
    html_texts = html_texts_array[21].text.replace('STK && STK.pageletM && STK.pageletM.view(', '')[:-1]
    return html_texts


'''
    解析出包含在json代码中的html代码
'''


def get_script_html(script_json_data):
    json_dict = json.loads(script_json_data)
    return json_dict['html']


'''
    分析微博各种数据
    weibo_time:该条微博发布的时间
    weibo_unique_id:该条微博的唯一ID(该条微博的访问地址)
    phone_model:手机型号
    weibo_user_nick_name:用户昵称
    weibo_user_id:用户微博主页ID
    weibo_content_detail:微博详细内容
'''


def analysis_weibo_data(content_html_text):
    content_array = content_html_text.split('<div class="WB_feed_detail clearfix">')
    del (content_array[0])  # 删除第一段无用的代码
    weibo_time_list = []
    weibo_unique_id_list = []
    weibo_user_nick_name_list = []
    weibo_user_id_list = []
    phone_model_list = []
    weibo_content_detail_list = []

    for content in content_array:
        content = '<div class="WB_feed_detail clearfix">' + content
        page = etree.HTML(content)

        # **获取微博发布的时间 和 该条微博的唯一ID 和 手机型号
        weibo_data_t_i = page.xpath(r'//a[@class="W_textb"]')
        # 获取时间需要判断一下列表长度,如果微博有引用的话,列表长度会是2,这样需要分析第二个数据
        if len(weibo_data_t_i) == 1:
            weibo_time = weibo_data_t_i[0].attrib['title']
            weibo_unique_id = weibo_data_t_i[0].attrib['href'].split('?')[0]
        elif len(weibo_data_t_i) == 2:
            weibo_time = weibo_data_t_i[1].attrib['title']
            weibo_unique_id = weibo_data_t_i[1].attrib['href'].split('?')[0]
        else:
            print('获取微博发布时间和该条微博的唯一ID时出现错误,list列表长度有问题')

        # **获取微博发布的 手机型号
        weibo_data_p = page.xpath(r'//a[@rel="nofollow"]')
        # 获取时间需要判断一下列表长度,如果微博有引用的话,列表长度会是2,这样需要分析第二个数据
        if len(weibo_data_p) == 1:
            phone_model = weibo_data_p[0].text
        elif len(weibo_data_p) == 2:
            phone_model = weibo_data_p[1].text
        else:
            print('获取微博发布所使用的手机型号时出现错误,list列表长度有问题')

        # **获取用户ID
        weibo_data_u = page.xpath(r'//a[@class="W_texta W_fb"]')
        weibo_user_nick_name = weibo_data_u[0].attrib['nick-name']
        weibo_user_id = weibo_data_u[0].attrib['href'].split('?')[0].split('/')[-1]

        # **获取微博内容
        # 获取第一段的内容
        weibo_data_c_1 = page.xpath(r'//div[@class="feed_content wbcon"]/p[@class="comment_txt"]')
        # 获取下面的内容
        weibo_data_c_2 = page.xpath(r'//div[@class="feed_content wbcon"]/p[@class="comment_txt"]/*')
        weibo_content_detail = ''
        for temp_item in weibo_data_c_2:
            if temp_item.tag == 'a':  # 获取下面'em'元素中的内容
                if not temp_item.text: temp_item.text = ''  # 如果是NULL则将字符串置空
                if not temp_item.tail: temp_item.tail = ''  # 如果是NULL则将字符串置空
                weibo_content_detail = weibo_content_detail + temp_item.text.strip() + temp_item.tail.strip() + ' '
            if temp_item.tag == 'em':  # 获取下面'em'元素中的内容
                if not temp_item.text: temp_item.text = ''  # 如果是NULL则将字符串置空
                if not temp_item.tail: temp_item.tail = ''  # 如果是NULL则将字符串置空
                weibo_content_detail = weibo_content_detail + temp_item.text.strip() + temp_item.tail.strip() + ' '
            if temp_item.tag == 'br':  # 获取下面'br'元素中的内容
                if not temp_item.text: temp_item.text = ''
                if not temp_item.tail: temp_item.tail = ''
                weibo_content_detail = weibo_content_detail + temp_item.text.strip() + temp_item.tail.strip() + ' '
            if temp_item.tag == 'img':  # 获取下面'br'元素中的内容
                if not temp_item.text: temp_item.text = ''
                if not temp_item.tail: temp_item.tail = ''
                weibo_content_detail = weibo_content_detail + temp_item.text.strip() + temp_item.tail.strip() + ' '

        weibo_content_detail = weibo_data_c_1[0].text + weibo_content_detail

        # print(weibo_time, weibo_content_unique_id, weibo_user_nick_name, weibo_user_id, phone_model, weibo_content_detail)
        weibo_time_list.append(weibo_time)
        weibo_unique_id_list.append(weibo_unique_id)
        weibo_user_nick_name_list.append(weibo_user_nick_name)
        weibo_user_id_list.append(weibo_user_id)
        phone_model_list.append(phone_model)
        weibo_content_detail_list.append(weibo_content_detail)
    return (weibo_time_list, weibo_unique_id_list, weibo_user_nick_name_list, weibo_user_id_list, phone_model_list, weibo_content_detail_list)


'''
    获取server信息
'''


def get_server_data():
    r = requests.get('http://127.0.0.1:8000/keyword/?time=20', auth=HTTPBasicAuth(USER_NAME, USER_PASSWORD))
    print(r.text)


if __name__ == '__main__':
    html_raw_data = get_raw_html('1', '22:1')
    r = analysis_relevant_data(html_raw_data)
    if r:
        script_json_data = split_script_html(html_raw_data)
        content_html_text = get_script_html(script_json_data)
        weibo_time_list, weibo_unique_id_list, weibo_user_nick_name_list, weibo_user_id_list, phone_model_list, weibo_content_detail_list = analysis_weibo_data(content_html_text)
        for weibo_time, weibo_unique_id, weibo_user_nick_name, weibo_user_id, phone_model, weibo_content_detail in zip(weibo_time_list, weibo_unique_id_list, weibo_user_nick_name_list, weibo_user_id_list, phone_model_list, weibo_content_detail_list):
            print(weibo_time, weibo_unique_id, weibo_user_nick_name, weibo_user_id, phone_model, weibo_content_detail)
    else:
        print('该关键词未获取到相关数据')


    # get_server_data()
