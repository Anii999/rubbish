# 这段代码实现了一个简单的垃圾分类查询工具。它定义了四种垃圾类型（其他垃圾、有害垃圾、可回收物、厨余垃圾），
# 并根据输入的垃圾名称返回对应的垃圾类型和详细描述
qita=['xie','canjinzhi','suliaodai','naicha','zhiniaoku','kouxiangtang','zhibei','yantou','baoxianmo','wazi','huoji','yaqian','kouzhao']
chuyu=['jidanke','xia','qingcai','xiguapi','qiaokeli','diliao','jidankedddaa','mifan','neizang','xiangjiaopi','mianbao']
kehuishou=['shuibei','dao','wanou','chongdianbao','guo','baozhi','chazuo','bao','jiuping','yilaguan','dingzi']
youhai=['wenduji','dengpao','yao']


def main(name):
    if name in qita :
        tp='其他垃圾'
        content='其他垃圾，指除可回收物、有害垃圾、餐厨垃圾外的其他生活垃圾。即现环卫体系主要收集和处理的垃圾，' \
                '一般都采取填埋、焚烧等方法处理，部分还可以使用生物分解的方法解决，如放蚯蚓等。其他垃圾是可回收物、' \
                '厨余垃圾、有害垃圾剩余下来的一种垃圾种类。'
        return [name, tp, content]

    if name in youhai :
        tp = '有害垃圾'
        content = '有害垃圾，指生活垃圾中对人体健康或自然环境造成直接或潜在危害的物质。\
                  必须单独收集、运输、存贮，由环保部门认可的专业机构进行特殊安全处理。' \
                  '常见的有害垃圾包括废灯管、废油漆、杀虫剂、废弃化妆品、过期药品、废电池、' \
                  '废灯泡、废水银温度计等，有害垃圾需按照特殊正确的方法安全处理。'
        return [name, tp, content]
    if name in kehuishou:
        tp = '可回收物'
        content = '可回收物就是再生资源，指生活垃圾中未经污染、适宜回收循环利用的废物。' \
                  ' 主要包括废弃电器电子产品、废纸张、废塑料、废玻璃、废金属等五类，' \
                  '是现阶段生活垃圾分类的主要工作和影响垃圾减量的重要因素。'
        return [name, tp, content]
    if name in chuyu:
        tp = '厨余垃圾'
        content = '厨余垃圾是指居民日常生活及食品加工、饮食服务、单位供餐等活动中产生的垃圾，' \
                  '包括丢弃不用的菜叶、剩菜、剩饭、果皮、蛋壳、茶渣、骨头（鸡骨、鱼刺类）等，其' \
                  '主要来源为家庭厨房、餐厅、饭店、食堂、市场及其他与食品加工有关的行业。'
        return [name, tp, content]



if __name__ == '__main__':
    res=main('香蕉')
    for i in res:
        print(i)

