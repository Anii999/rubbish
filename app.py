from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_from_directory
import mysql.connector
import base64
from io import BytesIO
from PIL import Image
import numpy as np
from datetime import datetime
import os
from waste_detector import WasteDetector
import cv2
from werkzeug.utils import secure_filename
import time
from flask_cors import CORS
import io

# 获取当前工作目录的绝对路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 创建 Flask 应用实例
app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 设置静态文件夹路径
app.static_folder = os.path.join(BASE_DIR, '40')
app.template_folder = os.path.join(BASE_DIR, '40')

# 设置上传和结果文件夹路径
UPLOAD_FOLDER = os.path.join(BASE_DIR, '40', 'uploads')
RESULTS_FOLDER = os.path.join(BASE_DIR, '40', 'results')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保必要的目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 初始化检测器
detector = WasteDetector()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)  # 启用CORS支持

# MySQL配置
db_config = {
    'user': 'root',
    'password': '66666666',
    'host': 'localhost',
    'database': 'rubbish',
}

# 连接数据库
def get_db_connection():
    return mysql.connector.connect(**db_config)

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 环保知识页面
@app.route('/knowledge')
def knowledge():
    
    articles = [
        {
            'id': 1,
            'title': '如何减少塑料使用',
            'date': '2023-10-01',
            'description': '减少使用一次性塑料制品，使用可重复使用的购物袋和水杯，减少塑料污染。'
        },
        {
            'id': 2,
            'title': '节约用水的方法',
            'date': '2023-09-15',
            'description': '修理漏水的水龙头，洗澡时间控制在10分钟以内，收集雨水用于浇花。'
        },
        {
            'id': 3,
            'title': '家庭垃圾分类指南',
            'date': '2023-11-05',
            'description': '详细介绍可回收物、厨余垃圾、有害垃圾和其他垃圾的分类标准和处理方法。'
        },
        {
            'id': 4,
            'title': '节能减排小贴士',
            'date': '2023-08-20',
            'description': '使用节能灯具，合理设置空调温度，选择公共交通出行等日常节能方法。'
        },
        {
            'id': 5,
            'title': '电子废弃物处理',
            'date': '2023-07-10',
            'description': '正确处理废旧电子产品的方法和回收渠道，避免环境污染。'
        },
        {
            'id': 6,
            'title': '绿色出行方式',
            'date': '2023-06-25',
            'description': '步行、骑行、公共交通等环保出行方式的优点和实用建议。'
        },
        {
            'id': 7,
            'title': '厨余垃圾堆肥',
            'date': '2023-05-15',
            'description': '家庭厨余垃圾堆肥的简易方法和注意事项，变废为宝。'
        },
        {
            'id': 8,
            'title': '环保购物指南',
            'date': '2023-04-08',
            'description': '选择环保产品、减少包装浪费、支持可持续发展的购物建议。'
        },
    ]

    qas = [
        {
            'question': '如何正确进行垃圾分类?',
            'answer': '可回收物、厨余垃圾、有害垃圾和其他垃圾需要分别投放到对应的垃圾桶中。'
        },
        {
            'question': '如何减少家庭能源消耗?',
            'answer': '使用节能灯具，不用电器时拔掉插头，合理设置空调温度。'
        },
        {
            'question': '电子废弃物该如何处理?',
            'answer': '应送至专门的电子废弃物回收点，不可随意丢弃以免污染环境。'
        },
        {
            'question': '如何减少塑料污染?',
            'answer': '使用可重复使用的购物袋、水杯，避免使用一次性塑料制品。'
        },
        # 更多问答...
    ]

    return render_template('knowledge.html', articles=articles, qas=qas)

# 文章详情页
@app.route('/article/<int:article_id>')
def article_detail(article_id):
    articles = {
        1: {
            'title': '如何减少塑料使用',
            'date': '2023-10-01',
            'content': '''
                <p>塑料污染已成为全球最严重的环境问题之一。据统计，全球每年产生约3亿吨塑料垃圾，其中仅有9%被回收利用。塑料制品在自然环境中需要数百年才能降解，对海洋生态系统和人类健康造成严重威胁。以下是一些实用且有效的减少塑料使用的方法：</p>
                
                <h3>1. 使用可重复使用的购物袋</h3>
                <p>随身携带环保袋是减少塑料污染最简单有效的方法之一。一个普通的塑料袋平均使用时间仅12分钟，但却需要数百年才能降解。建议在家中、办公室和车内都备有环保袋，养成出门前检查是否携带的习惯。可以选择棉质、帆布或可折叠的轻便环保袋，既环保又时尚。</p>
                
                <h3>2. 选择无包装产品</h3>
                <p>现代商品过度包装问题严重，特别是塑料包装。我们可以优先选择散装商品，如散装谷物、坚果、调味品等。许多城市已出现"零废弃商店"，顾客可自带容器购买商品。即使普通超市，也可选择大包装替代多个小包装，减少塑料用量。</p>
                
                <h3>3. 使用可重复使用的水杯</h3>
                <p>全球每分钟消费约100万个塑料瓶。使用不锈钢、玻璃或环保材质的水杯不仅能减少塑料垃圾，还能避免塑料中的有害物质渗入饮用水。许多咖啡店为自带杯顾客提供折扣，这也是额外的经济激励。</p>
                
                <h3>4. 拒绝一次性餐具</h3>
                <p>外卖和快餐产生大量塑料餐具垃圾。建议随身携带便携式餐具套装，包括筷子、勺子和可折叠的叉子。不锈钢或竹子材质都是不错的选择。对于公司午餐或野餐，可准备可重复使用的餐具，既环保又卫生。</p>
                
                <h3>5. 选择天然纤维衣物</h3>
                <p>合成纤维衣物在洗涤时会释放微塑料。选择棉、麻、羊毛等天然纤维衣物，减少微塑料污染。洗涤时使用专门的微塑料过滤袋也能有效减少微塑料进入水体。</p>
                
                <h3>6. 自制清洁用品</h3>
                <p>许多家用清洁剂使用塑料瓶包装。可以用白醋、小苏打等天然原料自制清洁剂，装入可重复使用的玻璃瓶中。这不仅能减少塑料垃圾，还能避免化学清洁剂对环境的污染。</p>
            '''
        },
        2: {
            'title': '节约用水的方法',
            'date': '2023-09-15',
            'content': '''
                <p>水是生命之源，但全球淡水资源仅占地球总水量的2.5%，其中可供人类使用的不足1%。随着人口增长和气候变化，水资源短缺问题日益严重。节约用水不仅是个人的环保行为，更是对子孙后代负责的表现。以下是一些科学有效的节水方法：</p>
                
                <h3>1. 修理漏水</h3>
                <p>一个滴水的水龙头每天可浪费30升水，而一个漏水的马桶每天可能浪费高达700升水。定期检查家中水管、水龙头和马桶是否漏水。修理漏水不仅能节约水资源，还能减少水费支出。安装自动关闭的水龙头也能有效防止忘记关水造成的浪费。</p>
                
                <h3>2. 缩短洗澡时间</h3>
                <p>普通淋浴每分钟消耗约10升水，10分钟的淋浴就会用掉100升水。建议将淋浴时间控制在5-7分钟，安装节水型淋浴头可减少30-50%的用水量。洗澡时可以先打湿身体，关闭水龙头涂抹沐浴露，然后再开水冲洗，这样能显著减少用水量。</p>
                
                <h3>3. 收集雨水</h3>
                <p>雨水是免费的自然资源，可用于浇灌植物、冲洗地面甚至冲厕所。安装雨水收集系统，即使是简单的桶或水箱也能收集大量雨水。在降雨量大的地区，一个100平方米的屋顶一年可收集约10万升雨水。使用雨水浇灌植物还能避免自来水中的氯对植物生长的影响。</p>
                
                <h3>4. 使用节水器具</h3>
                <p>现代节水技术已非常成熟。节水型马桶每次冲水仅需3-4升，比传统马桶节约50%以上。节水型洗衣机每次可节约30-50升水。安装水流调节器在水龙头上可减少水流速度而不影响使用体验。选择具有节水认证的家电和卫浴产品是长期节水的有效方法。</p>
                
                <h3>5. 改变洗衣习惯</h3>
                <p>洗衣机是家庭用水大户之一。建议积攒足够衣物再进行洗涤，选择适当的水位和节水模式。现代洗衣粉在冷水中同样有效，不必每次都使用热水。对于不太脏的衣物，可以缩短洗涤时间或减少洗涤剂用量。</p>
                
                <h3>6. 合理浇灌植物</h3>
                <p>园艺用水占家庭用水的很大比例。早晨或傍晚浇水能减少蒸发损失。使用滴灌系统比喷洒更节水。选择本地耐旱植物，减少草坪面积，使用覆盖物保持土壤湿度都是有效的园艺节水方法。</p>
            '''
        },
        5: {
            'title': '电子废弃物处理',
            'date': '2023-07-10',
            'content': '''
                <p>电子废弃物是全球增长最快的垃圾类别，每年产生约5000万吨，其中仅20%被正规回收。电子设备中含有铅、汞、镉等有毒物质，同时也含有金、银、铜等有价值的金属。正确处理电子废弃物既能保护环境，又能回收宝贵资源。以下是详细的处理方法：</p>
                
                <h3>1. 回收渠道</h3>
                <p>寻找正规的电子废弃物回收点是关键。许多电子产品制造商(如苹果、华为)提供回收服务，部分还提供以旧换新优惠。社区回收站、环保部门指定的回收点也是可靠选择。注意：小商贩回收可能造成二次污染，1吨废旧手机可提取150克黄金，但非正规提炼过程会释放大量有毒物质。</p>
                
                <h3>2. 数据清除</h3>
                <p>数据安全是首要考虑。对于智能手机和电脑，应进行出厂重置并加密擦除。机械硬盘需物理销毁或使用专业擦除软件重复写入7次以上。固态硬盘建议使用安全擦除命令。云账户要记得注销，SIM卡要取出销毁。一台未妥善处理的电脑平均会导致价值2000元的个人信息泄露。</p>
                
                <h3>3. 分类处理</h3>
                <p>不同电子元件处理方式各异：电池需单独回收(特别是锂电池)；显示屏中的液晶需专业处理；电路板可提取贵金属；塑料外壳可回收再造。一台笔记本电脑约含0.05克黄金、0.3克银和90克铜。专业回收企业能实现95%以上的材料回收率，而填埋处理会造成永久性污染。</p>
                
                <h3>4. 避免随意丢弃</h3>
                <p>一块手机电池可污染6万升水，相当于3个标准游泳池。CRT显示器含2-4公斤铅，会污染土壤和地下水。电子废弃物中的阻燃剂会干扰内分泌系统。许多国家已立法禁止电子废弃物填埋，违规可能面临高额罚款。</p>
                
                <h3>5. 延长使用寿命</h3>
                <p>减少电子废弃物最有效的方法是延长设备使用时间。定期清理内存、更换电池、升级系统都能延长设备寿命。二手交易平台可以让旧设备继续发挥作用。一台智能手机平均使用2-3年，但实际寿命可达5年以上。</p>
                
                <h3>6. 购买环保产品</h3>
                <p>选择易维修、可升级的电子产品，优先考虑提供回收服务的品牌。查看产品的环保认证，如EPEAT、Energy Star等。模块化设计的手机比传统手机减少30%的电子垃圾。</p>
            '''
        },
        6: {
            'title': '绿色出行方式',
            'date': '2023-06-25',
            'content': '''
                <p>交通排放占全球二氧化碳排放的24%，其中私家车占比最大。绿色出行不仅能减少碳排放，还能缓解交通拥堵、改善空气质量。研究表明，采用绿色出行方式的城市居民比驾车者平均每年多消耗300卡路里，健康状况更好。以下是详细的绿色出行指南：</p>
                
                <h3>1. 步行</h3>
                <p>步行是最环保的出行方式，适合3公里以内的短途出行。成年人每天步行8000-10000步有益健康。规划步行路线时，可选择林荫道或专用步道，使用计步器记录运动量。一个放弃开车选择步行的人，每年可减少约2吨碳排放，相当于种植50棵树。</p>
                
                <h3>2. 骑行</h3>
                <p>自行车是3-10公里出行的理想选择，速度是步行的3倍，碳排放为零。电动自行车适合10-20公里出行，能耗仅为电动车的1/10。许多城市已建立自行车专用道和共享单车系统。骑行时佩戴头盔、使用车灯能提高安全性。每周骑行30公里可降低50%心脏病风险。</p>
                
                <h3>3. 公共交通</h3>
                <p>地铁、公交等公共交通的人均碳排放仅为私家车的1/10。早高峰时段，一列地铁可替代500辆私家车。使用公交APP规划路线、办理电子月票能提高便利性。许多城市对公交专用道进行信号优先，实际速度可能快于私家车。选择靠窗座位并开窗通风能降低病毒传播风险。</p>
                
                <h3>4. 拼车共享</h3>
                <p>拼车可将单车碳排放降低50-75%。使用拼车APP匹配路线相似的乘客，一辆4人拼车每年可减少约3吨碳排放。公司内部组织班车、邻里拼车上学都是有效方式。长途出行可选择顺风车，许多高速公路设有拼车专用通道。拼车时注意安全，选择正规平台并核实司机信息。</p>
                
                <h3>5. 新能源车辆</h3>
                <p>必须开车时，选择电动车或混合动力车。电动车每公里碳排放比燃油车低60%，使用夜间低谷充电更经济。氢燃料电池车是长途运输的未来选择。保持适当胎压、定期保养能提高燃油效率10-20%。避免急加速急刹车，平稳驾驶可节省15%燃油。</p>
                
                <h3>6. 出行规划</h3>
                <p>合并多个行程、避开高峰时段能减少30%的出行时间。远程办公每周1-2天可减少20%通勤排放。视频会议替代商务差旅，一次跨国航班相当于全年开车排放量。度假选择火车而非飞机，北京到上海的高铁碳排放仅为飞机的1/4。</p>
            '''
        },
        7: {
            'title': '厨余垃圾堆肥',
            'date': '2023-05-15',
            'content': '''
                <p>家庭厨余垃圾约占生活垃圾总量的50%，通过堆肥可将其转化为宝贵的有机肥料，减少垃圾填埋量30%以上。一个四口之家每年可产生约500公斤厨余垃圾，通过堆肥可转化为100公斤优质肥料。以下是详细的家庭堆肥指南：</p>
                
                <h3>1. 准备堆肥箱</h3>
                <p>选择容量50-100升的堆肥箱，底部需有通风孔和接液盘。市售堆肥箱价格在200-500元不等，也可自制：用塑料桶钻孔(直径1cm，间距10cm)或木箱内衬铁丝网。阳台使用可选择带密封盖的款式，避免异味和虫害。专业堆肥箱带有温度计和通风调节装置，能加速分解过程。</p>
                
                <h3>2. 分层堆放</h3>
                <p>按照"三明治"法则分层：底层铺5cm干物质(枯叶、碎纸板)，中间放厨余垃圾(厚度不超过10cm)，上层再覆盖3cm干物质。理想碳氮比为25-30:1，厨余垃圾(氮源)与干物质(碳源)体积比1:2。适合堆肥的厨余包括：果皮菜叶、咖啡渣、茶包、蛋壳(需碾碎)；避免肉类、油脂、乳制品等易腐坏物质。</p>
                
                <h3>3. 定期翻动</h3>
                <p>每周翻动一次使堆体温度保持在50-60℃(可杀灭病原菌和杂草种子)。使用堆肥叉从底部向上翻动，确保氧气均匀分布。堆体应保持湿润如拧干的海绵，过干时喷水，过湿时添加干物质。添加EM菌或成熟堆肥作为接种剂可加速分解，缩短堆肥周期30%。</p>
                
                <h3>4. 使用成品</h3>
                <p>2-3个月后堆肥呈深褐色、松软、有泥土清香时即可使用。过筛去除未分解物质回填继续堆制。成品堆肥含氮1.5-2%、磷0.5-1%、钾1-1.5%，是化学肥料的理想替代品。用于盆栽按1:3与土壤混合，地栽每平方米施用2-3公斤。堆肥液稀释10倍可作为叶面肥，含多种微量元素和有益微生物。</p>
                
                <h3>5. 问题解决</h3>
                <p>异味表明缺氧或氮过多，应翻动并添加干物质；虫害可加盖或表面覆盖5cm干土；分解慢可能因碳氮比失衡或水分不当。冬季堆肥速度减慢，可包裹保温材料或移至室内。蚯蚓堆肥是另一种高效方式，红蚯蚓每天可消耗相当于自身体重的厨余。</p>
                
                <h3>6. 进阶技巧</h3>
                <p>使用双层堆肥箱交替填装；添加粉碎的蛋壳补充钙质；咖啡渣调节酸碱度；香蕉皮提供钾元素；定期检测堆肥温度(理想范围40-65℃)。社区共享堆肥系统能处理更多厨余，10户家庭共享系统每年可减少2吨垃圾填埋。</p>
            '''
        },
        8: {
            'title': '环保购物指南',
            'date': '2023-04-08',
            'content': '''
                <p>消费选择直接影响环境，全球每年因消费产生的碳排放占总量的60%以上。环保购物不仅能减少个人碳足迹，还能推动企业采用可持续生产方式。一个家庭通过环保购物每年可减少约1.5吨碳排放，节省2000元不必要的开支。以下是全面的环保购物指南：</p>
                
                <h3>1. 选择环保产品</h3>
                <p>认准权威环保认证：中国环境标志(十环)、欧盟生态标签、FSC森林认证、有机认证等。优先选择本地产品，运输距离每减少100公里可降低5%碳足迹。电子产品看能效等级，一级比五级年省电200度。纺织品优选有机棉、天丝等环保面料，传统棉花种植使用全球16%的杀虫剂。</p>
                
                <h3>2. 减少包装浪费</h3>
                <p>全球包装废弃物每年达1.5亿吨。选择散装商品可减少30%包装垃圾，自带容器购买粮油干货。拒绝过度包装，一个豪华月饼盒的包装成本可达产品价值的50%。选择可回收包装材料，铝罐回收率高达95%，而塑料仅9%。购买大包装替代多个小包装，1升装洗发水比200ml装减少40%塑料用量。</p>
                
                <h3>3. 自带购物袋</h3>
                <p>全球每分钟消耗100万个塑料袋，平均使用时间仅12分钟。使用棉布袋需重复使用131次、无纺布袋11次才能抵销环境影响。折叠购物袋可随身携带，车内、办公室常备备用袋。购买海鲜肉类可使用硅胶保鲜盒，避免使用超市提供的塑料袋。选择可降解垃圾袋时，注意真正可堆肥的PLA材质而非仅添加降解剂的伪环保产品。</p>
                
                <h3>4. 支持可持续品牌</h3>
                <p>选择有明确环保承诺的品牌，如Patagonia将1%销售额用于环保，Interface地毯实现碳中和。关注企业ESG(环境、社会、治理)报告，优先选择评级高的公司。支持采用循环经济模式的企业，如提供产品回收、以旧换新服务的商家。小众环保品牌往往更注重可持续性，可通过绿色消费APP发现优质选择。</p>
                
                <h3>5. 购物计划与习惯</h3>
                <p>制定购物清单避免冲动消费，30%的家庭物品最终未被使用。选择多功能产品减少购买数量，如二合一洗发沐浴露。季节性购物，反季水果的碳足迹是应季的3倍。参加二手交易平台，一件二手衣服可减少5.7公斤碳排放。建立"30天规则"：非急需品放入购物车30天后再决定是否购买。</p>
                
                <h3>6. 数字工具辅助</h3>
                <p>使用碳足迹计算APP扫描商品条码；安装浏览器插件显示产品环保评级；关注可持续消费公众号获取最新资讯；加入环保购物社群分享经验。部分超市已推出"碳标签"商品，明确标注生产运输过程中的碳排放量。</p>
            '''
        },
    }

    article = articles.get(article_id, None)
    if article:
        return render_template('article_detail.html', article=article)
    else:
        return '文章不存在', 404

# 游戏页面
@app.route('/game')
def game():
    return render_template('game.html')

# 用户登录
@app.route('/userlogin', methods=['GET','POST'])
def userlogin():
    if request.method == 'GET':
        return render_template('userlogin.html')
        
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        session['user_id'] = user['user_id']
        session['username'] = user['username']
        session['points'] = user['points']
        return jsonify({'success': True, 'redirect': url_for('game')})
    else:
        flash('用户名或密码错误！')
        return redirect(url_for('userlogin'))

# 用户注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
        
    user_id = request.form['userId']
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 检查用户ID是否已存在
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('用户ID已存在！请使用其他用户ID')
            return redirect(url_for('register'))
        
        # 插入新用户
        cursor.execute("INSERT INTO users (user_id, username, password) VALUES (%s, %s, %s)", (user_id, username, password))
        conn.commit()
        flash('注册成功！请登录')
        return jsonify({'success': True, 'redirect': url_for('userlogin')})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

#修改用户信息
@app.route('/update-user', methods=['POST'])
def update_user():
    user_id = request.form['userId']
    current_username = request.form['currentUserName']
    new_username = request.form['newUserName']
    original_password = request.form['originalPassword']
    new_password = request.form['newPassword']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 检查用户是否存在
        cursor.execute("SELECT * FROM users WHERE user_id = %s AND password = %s", (user_id, original_password))
        user = cursor.fetchone()

        if not user:
            return jsonify({'success': False, 'message': '用户不存在或原始密码错误！'})

        # 检查新用户名是否已被占用
        cursor.execute("SELECT * FROM users WHERE username = %s AND user_id != %s", (new_username, user_id))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'success': False, 'message': '新用户名已被占用！'})

        # 更新用户名和密码
        cursor.execute("UPDATE users SET username = %s, password = %s WHERE user_id = %s", (new_username, new_password, user_id))
        conn.commit()

        return jsonify({'success': True, 'message': '用户信息更新成功'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

# 积分商城
@app.route('/score')
def score():
    if 'user_id' not in session:
        return redirect(url_for('userlogin'))
    return render_template('score.html')

# 获取排行榜
@app.route('/get_ranking')
def get_ranking():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, username, points FROM users ORDER BY points DESC LIMIT 5")
    ranking = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(ranking)

# 提交游戏分数
@app.route('/submit_score', methods=['POST'])
def submit_score():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录'})
    
    score = request.json.get('score')
    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO game_scores (user_id, score) VALUES (%s, %s)", (user_id, score))
        cursor.execute("UPDATE users SET points = points + %s WHERE user_id = %s", (score, user_id))
        conn.commit()
        session['points'] += score
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()
    
    return jsonify({'success': True, 'message': '分数提交成功', 'new_points': session['points']})

# 获取礼品
@app.route('/gifts')
def gifts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gifts")  # 确保你的表中有 image_path 字段
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(items)

# 兑换礼品
@app.route('/exchange', methods=['POST'])
def exchange():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录'})
    
    gift_id = request.form['gift_id']
    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gifts WHERE gift_id = %s", (gift_id,))
    gift = cursor.fetchone()
    
    if not gift:
        return jsonify({'success': False, 'message': '礼品不存在'})
    
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    
    if user['points'] < gift['points_required']:
        return jsonify({'success': False, 'message': '积分不足'})
    
    try:
        cursor.execute("UPDATE users SET points = points - %s WHERE user_id = %s", (gift['points_required'], user_id))
        cursor.execute("INSERT INTO exchanges (user_id, gift_id) VALUES (%s, %s)", (user_id, gift_id))
        conn.commit()
        session['points'] = user['points'] - gift['points_required']
        return jsonify({'success': True, 'message': '兑换成功'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': '兑换失败: ' + str(e)})
    finally:
        cursor.close()
        conn.close()

# 兑换记录
@app.route('/get_exchange_records')
def get_exchange_records():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            e.created_at,
            u.user_id,
            u.username,
            g.gift_name
        FROM exchanges e
        JOIN users u ON e.user_id = u.user_id
        JOIN gifts g ON e.gift_id = g.gift_id
        ORDER BY e.created_at DESC
    """)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(records)

# 用户管理页面
@app.route('/user_manage')
def user_manage():
    return render_template('user_manage.html')

# 获取用户信息
@app.route('/user_info')
def get_user_info():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录'})
    
    return jsonify({
        'success': True,
        'user_id': session['user_id'],
        'username': session['username'],
        'points': session['points']
    })


# 处理静态文件请求
@app.route('/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.static_folder, filename)


# 示例API - 获取垃圾分类统计数据
@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    data = {
        "recyclable": 150,
        "kitchen": 200,
        "harmful": 50,
        "other": 100
    }
    return jsonify(data)


# 示例API - 获取当前时间
@app.route('/api/current_time', methods=['GET'])
def get_current_time():
    return jsonify({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


@app.route('/detection', methods=['GET', 'POST'])
def detection():
    if request.method == 'GET':
        return render_template('detection.html')
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({'error': '没有文件上传'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件格式，请上传 PNG、JPG、JPEG 或 GIF 图片'}), 400

        # 保存上传的文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        filename = f"upload_{timestamp}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            # 读取文件内容
            file_content = file.read()

            # 验证图片格式
            try:
                image = Image.open(io.BytesIO(file_content))
                image.verify()  # 验证图片完整性
                image.close()
            except Exception as e:
                print(f"图片验证失败: {str(e)}")
                return jsonify({'error': '图片格式错误或文件损坏'}), 400

            # 保存文件
            with open(filepath, 'wb') as f:
                f.write(file_content)

            print(f"文件已保存: {filepath}")
        except Exception as e:
            print(f"保存文件失败: {str(e)}")
            return jsonify({'error': '文件保存失败'}), 500

        if not os.path.exists(filepath):
            return jsonify({'error': '文件保存失败，请重试'}), 500

        # 记录开始时间
        start_time = time.time()

        try:
            # 进行检测
            result = detector.detect_image(filepath)
            if result is None:
                raise Exception("检测失败，未能获取结果")

            # 计算用时（毫秒）
            detection_time = int((time.time() - start_time) * 1000)

            # 处理检测结果
            if result.get('results') and len(result['results']) > 0:
                # 使用第一个检测结果
                first_result = result['results'][0]
                response = {
                    'type': first_result.get('type', '未知'),
                    'category': first_result.get('category', '未知'),
                    'confidence': first_result.get('confidence', 0),
                    'time': detection_time,
                    'count': result.get('count', 0)
                }
            else:
                response = {
                    'type': '未检测到物体',
                    'category': '未知',
                    'confidence': 0,
                    'time': detection_time,
                    'count': 0
                }

            return jsonify(response)

        except Exception as e:
            print(f"检测过程错误: {str(e)}")
            return jsonify({'error': f'检测失败: {str(e)}'}), 500

        finally:
            # 清理临时文件
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    print(f"已清理临时文件: {filepath}")
            except Exception as e:
                print(f"清理临时文件失败: {str(e)}")

    except Exception as e:
        print(f"请求处理错误: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/categories')
def get_categories():
    categories = detector.get_waste_categories()
    return jsonify(categories)


@app.route('/api/category/<waste_type>')
def get_category_info(waste_type):
    info = detector.get_waste_type_info(waste_type)
    if info:
        return jsonify(info)
    return jsonify({'error': '未找到该垃圾类型'}), 404


# 获取垃圾分类月度统计数据
@app.route('/api/statistics/monthly', methods=['GET'])
def get_monthly_statistics():
    try:
        year = request.args.get('year', None)
        if year:
            year = int(year)
        stats = detector.record_db.get_monthly_statistics(year)
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# 获取垃圾分类处理量趋势数据
@app.route('/api/statistics/trend', methods=['GET'])
def get_trend_statistics():
    try:
        # 获取最近7天的数据
        stats = detector.record_db.get_trend_statistics()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
