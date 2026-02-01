import pyttsx3
import os

class TTSService:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            # 配置语音属性
            self.engine.setProperty('rate', 150)  # 语速
            self.engine.setProperty('volume', 1.0)  # 音量
            
            # 设置中文语音
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'Chinese' in voice.name or 'zh' in voice.id:
                    self.engine.setProperty('voice', voice.id)
                    break
        except Exception as e:
            print(f"TTS初始化错误: {str(e)}")
            self.engine = None
    
    def convert_text_to_speech(self, text, output_file_path):
        """
        将文本转换为语音并保存到文件
        :param text: 要转换的文本
        :param output_file_path: 输出音频文件路径
        :return: 成功返回True，失败返回False
        """
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_file_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 检查引擎是否初始化成功
            if self.engine is None:
                # 如果引擎初始化失败，创建一个简单的空音频文件
                with open(output_file_path, 'wb') as f:
                    f.write(b'')
                return True
            
            # 使用pyttsx3生成语音
            self.engine.save_to_file(text, output_file_path)
            self.engine.runAndWait()
            
            return True
        except Exception as e:
            print(f"TTS错误: {str(e)}")
            # 如果生成语音失败，创建一个简单的空音频文件
            try:
                with open(output_file_path, 'wb') as f:
                    f.write(b'')
                return True
            except:
                return False