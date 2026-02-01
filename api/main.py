from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import sys
import tempfile

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from asr.asr_service import ASRService
from tts.tts_service import TTSService
from qa.qa_service import QAService

# 创建服务实例
asr_service = ASRService()
tts_service = TTSService()
qa_service = QAService()

# 创建FastAPI应用
app = FastAPI(title="智能语音助手API", description="提供语音识别、问答和语音合成功能")

# 创建临时目录用于存储音频文件
TEMP_DIR = tempfile.gettempdir()

@app.post("/api/asr")
async def speech_to_text(file: UploadFile = File(...)):
    """
    语音转文本接口
    """
    try:
        # 保存上传的音频文件
        file_path = os.path.join(TEMP_DIR, f"{file.filename}")
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # 使用ASR服务识别文本
        text = asr_service.convert_audio_to_text(file_path)
        
        # 清理临时文件
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ASR处理错误: {str(e)}")

@app.post("/api/qa")
async def question_answer(question: str):
    """
    问答接口
    """
    try:
        answer = qa_service.get_answer(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QA处理错误: {str(e)}")

@app.post("/api/tts")
async def text_to_speech(text: str):
    """
    文本转语音接口
    """
    try:
        # 生成临时输出文件路径
        output_file = os.path.join(TEMP_DIR, f"output_{os.urandom(8).hex()}.wav")
        
        # 使用TTS服务生成语音
        success = tts_service.convert_text_to_speech(text, output_file)
        
        if not success:
            raise HTTPException(status_code=500, detail="TTS处理失败")
        
        # 返回音频文件
        return FileResponse(output_file, media_type="audio/wav", filename="output.wav")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS处理错误: {str(e)}")

@app.post("/api/process")
async def process_audio(file: UploadFile = File(...)):
    """
    完整的语音问答流程接口
    """
    try:
        # 1. 保存上传的音频文件
        file_path = os.path.join(TEMP_DIR, f"{file.filename}")
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # 2. 使用ASR服务识别文本
        question = asr_service.convert_audio_to_text(file_path)
        
        # 3. 使用QA服务获取回答
        answer = qa_service.get_answer(question)
        
        # 4. 使用TTS服务生成语音
        output_file = os.path.join(TEMP_DIR, f"response_{os.urandom(8).hex()}.wav")
        success = tts_service.convert_text_to_speech(answer, output_file)
        
        # 5. 清理临时文件
        if os.path.exists(file_path):
            os.remove(file_path)
        
        if not success:
            # 如果TTS失败，只返回文本回答
            return {
                "question": question,
                "answer": answer,
                "audio_url": None
            }
        
        # 6. 返回结果
        return {
            "question": question,
            "answer": answer,
            "audio_url": f"/api/audio/{os.path.basename(output_file)}"
        }
    except Exception as e:
        # 捕获所有异常，返回友好的错误信息
        return {
            "question": "语音识别失败",
            "answer": f"处理错误: {str(e)}",
            "audio_url": None
        }

@app.get("/api/audio/{filename}")
async def get_audio(filename: str):
    """
    获取生成的音频文件
    """
    file_path = os.path.join(TEMP_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="音频文件不存在")
    
    return FileResponse(file_path, media_type="audio/wav", filename=filename)

@app.get("/")
async def root():
    """
    根路径
    """
    return {"message": "智能语音助手API服务运行正常"}