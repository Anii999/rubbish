import cv2
import numpy as np
from PIL import Image
from yolo import YOLO
from waste_category import main as type_inf
import datetime
import os
import tempfile
from models import DetectionRecord

class WasteDetector:
    def __init__(self):
        self.yolo = YOLO()
        self.name_dict = {
            'xie': '废旧鞋子', 'jidanke': '鸡蛋壳','shuibei': '水杯', 'xia': '虾壳',
            'qingcai': '青菜', 'canjinzhi': '餐巾纸','dao': '刀', 'wanou': '毛绒玩偶',
            'xiguapi': '西瓜皮', 'chongdianbao': '充电宝', 'suliaodai': '塑料袋', 'qiaokeli': '巧克力',
            'wenduji': '温度计', 'naicha': '奶茶', 'zhiniaoku': '纸尿裤', 'diliao': '火锅底料',
            'guo': '铁锅', 'baozhi': '报纸杂志','jidankedddaa': '鸡蛋壳','mifan': '米饭',
            'kouxiangtang': '口香糖','zhibei': '纸杯','dengpao': '灯泡','yantou': '烟头',
            'yao': '药片','chazuo': '插座','baoxianmo': '保鲜膜','bao': '包','jiuping': '酒瓶',
            'neizang': '内脏','yilaguan': '易拉罐','wazi': '袜子','huoji': '打火机','dingzi': '铁钉',
            'xiangjiaopi': '香蕉皮','mianbao': '面包','yaqian': '牙签','kouzhao': '口罩'
        }
        self.record_db = DetectionRecord()
        
    def detect_image(self, image_path):
        """检测单张图片"""
        temp_result_path = None
        try:
            if not os.path.exists(image_path):
                print(f"输入图片不存在: {image_path}")
                return None
                
            # 获取当前工作目录
            base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            
            # 创建临时文件用于存储检测结果
            temp_result_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
            temp_result_path = temp_result_file.name
            temp_result_file.close()
            
            # 打开并检测图片
            try:
                image = Image.open(image_path)
                # 传入临时文件路径给YOLO检测
                r_image = self.yolo.detect_image(image, crop=False, count=False, result_path=temp_result_path)
                if r_image is None:
                    raise Exception("YOLO检测返回空结果")
            except Exception as e:
                print(f"图片检测失败: {str(e)}")
                if temp_result_path and os.path.exists(temp_result_path):
                    os.unlink(temp_result_path)
                return None
            
            # 保存检测结果图片
            try:
                # 构建结果保存路径
                results_dir = os.path.join(base_dir, '40', 'results')
                os.makedirs(results_dir, exist_ok=True)
                
                # 生成唯一的文件名
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                result_filename = f'result_{timestamp}.png'
                result_path = os.path.join(results_dir, result_filename)
                
                # 保存图片
                r_image.save(result_path, 'PNG')
                
                if not os.path.exists(result_path):
                    print(f"结果图片保存失败: {result_path}")
                    if temp_result_path and os.path.exists(temp_result_path):
                        os.unlink(temp_result_path)
                    return None
                    
                print(f"结果图片已保存: {result_path}")
            except Exception as e:
                print(f"保存结果图片失败: {str(e)}")
                if temp_result_path and os.path.exists(temp_result_path):
                    os.unlink(temp_result_path)
                return None
            
            # 读取检测结果
            results = []
            try:
                if temp_result_path and os.path.exists(temp_result_path):
                    with open(temp_result_path, 'r', encoding='utf-8') as f:
                        data = f.readlines()
                        
                    for item in data:
                        try:
                            item = item.strip().split('+')
                            if len(item) >= 2:
                                waste_type = self.name_dict.get(item[0], '未知')
                                confidence = float(item[1])
                                position = item[2:] if len(item) > 2 else []
                                
                                category = type_inf(item[0])[1] if item[0] in self.name_dict else '未知'
                                
                                # 保存检测记录到数据库
                                try:
                                    self.record_db.add_record(waste_type, category, confidence)
                                except Exception as e:
                                    print(f"保存检测记录失败: {str(e)}")
                                
                                results.append({
                                    'type': waste_type,
                                    'confidence': round(confidence * 100, 2),  # 转换为百分比
                                    'position': position,
                                    'category': category
                                })
                        except Exception as e:
                            print(f"处理检测结果项失败: {str(e)}")
                            continue
            except Exception as e:
                print(f"读取检测结果文件失败: {str(e)}")
            finally:
                # 清理临时文件
                try:
                    if temp_result_path and os.path.exists(temp_result_path):
                        os.unlink(temp_result_path)
                except:
                    pass
                    
            # 如果没有检测到任何结果，返回空结果
            if not results:
                return {
                    'image_path': os.path.join('results', result_filename),
                    'results': [],
                    'count': 0
                }
                    
            return {
                'image_path': os.path.join('results', result_filename),
                'results': results,
                'count': len(results)
            }
            
        except Exception as e:
            print(f"检测过程发生错误: {str(e)}")
            # 确保清理临时文件
            if temp_result_path and os.path.exists(temp_result_path):
                try:
                    os.unlink(temp_result_path)
                except:
                    pass
            return None
        
    def detect_video_frame(self, frame):
        """检测视频帧"""
        try:
            # 将OpenCV格式转换为PIL格式
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            # 进行检测
            r_image = self.yolo.detect_image(pil_image, crop=False, count=False)
            
            # 将PIL格式转回OpenCV格式
            result_frame = cv2.cvtColor(np.array(r_image), cv2.COLOR_RGB2BGR)
            
            # 读取检测结果
            with open('res.txt', 'r', encoding='utf-8') as f:
                data = f.readlines()
                
            results = []
            for item in data:
                item = item.strip().split('+')
                if len(item) >= 2:
                    waste_type = self.name_dict.get(item[0], '未知')
                    confidence = float(item[1])
                    position = item[2:] if len(item) > 2 else []
                    
                    results.append({
                        'type': waste_type,
                        'confidence': confidence,
                        'position': position,
                        'category': type_inf(item[0])[1]
                    })
                    
            return {
                'frame': result_frame,
                'results': results,
                'count': len(results)
            }
        except Exception as e:
            print(f"视频帧检测失败: {str(e)}")
            return None
        
    def get_waste_categories(self):
        """获取所有垃圾类别"""
        return list(self.name_dict.values())
        
    def get_waste_type_info(self, waste_type):
        """获取特定垃圾类型的详细信息"""
        try:
            for key, value in self.name_dict.items():
                if value == waste_type:
                    return type_inf(key)
            return None
        except Exception as e:
            print(f"获取垃圾类型信息失败: {str(e)}")
            return None 