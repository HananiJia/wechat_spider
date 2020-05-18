import codecs, markdown

input_file = codecs.open(
    '/home/hanani/code/personal/wechat_spider/articles_md/中国传媒大学/防控疫情，中传官微新增“防疫E站”，请收好！.md',
    mode="r",
    encoding='utf-8')
text = input_file.read()

html = markdown.markdown(text)

output_file = codecs.open('/home/hanani/code/personal/wechat_spider/test.html',
                          mode='w',
                          encoding='utf-8')
output_file.write(html)
