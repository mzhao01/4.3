class QAService:
    def __init__(self):
        # 简单的问答规则库
        self.qa_rules = {
            "你好": "你好！有什么可以帮助你的吗？",
            "你好你好": "你好！有什么可以帮助你的吗？",
            "嗨": "你好！有什么可以帮助你的吗？",
            "嗨嗨": "你好！有什么可以帮助你的吗？",
            "再见": "再见！祝你有愉快的一天！",
            "谢谢": "不客气，很高兴能帮到你！",
            "你是谁": "我是智能语音助手，专门为你提供帮助。",
            "你叫什么名字": "我是智能语音助手，专门为你提供帮助。",
            "天气怎么样": "抱歉，我目前还不支持天气查询功能。",
            "时间": "抱歉，我目前还不支持时间查询功能。",
            "你能做什么": "我可以回答你的问题，和你聊天，提供一些基本的信息。"
        }
    
    def get_answer(self, question):
        """
        根据问题获取回答
        :param question: 问题文本
        :return: 回答文本
        """
        try:
            # 确保问题是字符串
            if not isinstance(question, str):
                question = str(question)
            
            # 首先尝试匹配规则库
            for key, value in self.qa_rules.items():
                if key in question:
                    return value
            
            # 如果没有匹配到规则，返回默认回答
            return "抱歉，我不太理解你的问题。你可以尝试问我其他问题。"
        except Exception as e:
            print(f"QA错误: {str(e)}")
            return "抱歉，我在处理你的问题时遇到了错误。"