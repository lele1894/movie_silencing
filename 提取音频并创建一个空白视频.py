"""
视频音频提取与空白视频生成工具

功能说明:
1. 从视频文件中提取音频
2. 生成一个只有音频的空白视频文件
3. 有效减小视频文件大小，便于网页视频编辑器处理

使用方法:
- 直接运行: python 提取音频并创建一个空白视频.py <输入视频文件>
- 指定输出: python 提取音频并创建一个空白视频.py <输入视频文件> <输出视频文件>
"""

import subprocess
import os
import sys

def extract_audio(input_video, output_audio):
    """
    使用ffmpeg从视频中提取音频
    """
    # 使用双引号包围文件路径，确保包含空格或特殊字符的路径能被正确处理
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-vn',  # 禁用视频
        '-acodec', 'copy',  # 直接复制音频编解码器
        output_audio,
        '-y'  # 覆盖输出文件
    ]
    
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE, encoding='utf-8')
        print(f"成功提取音频: {output_audio}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"提取音频失败: {e.stderr}")
        return False

def create_blank_video_with_audio(audio_file, output_video, duration=None):
    """
    创建一个空白画面的视频文件，只包含音频
    """
    # 使用一个持续时间较长的视频流，然后使用音频的长度作为最终视频长度
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', 'color=c=black:s=1280x720:d=999999',  # 创建一个很长的黑色背景视频
        '-i', audio_file,  # 输入音频
        '-c:v', 'libx264',  # 视频编码器
        '-c:a', 'copy',     # 直接复制音频流，避免重新编码导致时长变化
        '-shortest',        # 以最短的输入（音频）为准
        '-y',               # 覆盖输出文件
        output_video
    ]
    
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE, encoding='utf-8')
        print(f"成功创建空白视频: {output_video}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"创建空白视频失败: {e.stderr}")
        return False

def get_audio_duration(audio_file):
    """
    获取音频文件的时长
    """
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-show_entries', 'format=duration',
        '-of', 'csv=p=0',
        audio_file
    ]
    
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        duration = float(result.stdout.strip())
        return duration
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"获取音频时长失败: {e}")
        # 如果ffprobe失败，尝试从原始视频获取时长
        print("尝试从原始视频获取时长...")
        return get_video_duration(audio_file)

def get_video_duration(video_file):
    """
    从视频文件获取时长
    """
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-show_entries', 'format=duration',
        '-of', 'csv=p=0',
        video_file
    ]
    
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        duration = float(result.stdout.strip())
        return duration
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"获取视频时长失败: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("使用方法: python extract_audio_and_create_blank_video.py <输入视频文件> [输出视频文件]")
        return
    
    input_video = sys.argv[1]
    
    # 检查输入文件是否存在
    try:
        if not os.path.exists(input_video):
            print(f"错误: 找不到输入文件 {input_video}")
            return
    except UnicodeError:
        # 如果直接检查失败，尝试使用短路径或其他方式
        print(f"错误: 无法访问输入文件 {input_video}")
        return
    
    # 默认输出文件名
    if len(sys.argv) >= 3:
        output_video = sys.argv[2]
    else:
        name, ext = os.path.splitext(input_video)
        output_video = f"{name}_blank{ext}"
    
    # 临时音频文件
    name, ext = os.path.splitext(input_video)
    temp_audio = f"{name}.aac"
    
    print(f"处理文件: {input_video}")
    
    # 步骤1: 提取音频
    if not extract_audio(input_video, temp_audio):
        return
    
    # 步骤2: 创建空白视频
    if not create_blank_video_with_audio(temp_audio, output_video):
        return
    
    # 清理临时文件
    try:
        os.remove(temp_audio)
        print(f"已清理临时文件: {temp_audio}")
    except:
        pass
    
    # 显示文件大小对比
    try:
        original_size = os.path.getsize(input_video) / (1024 * 1024)  # MB
        new_size = os.path.getsize(output_video) / (1024 * 1024)     # MB
        reduction = ((original_size - new_size) / original_size) * 100
        
        print(f"\n文件大小对比:")
        print(f"原始视频: {original_size:.2f} MB")
        print(f"空白视频: {new_size:.2f} MB")
        print(f"减小了: {reduction:.1f}%")
    except:
        pass
    
    print(f"\n完成! 输出文件: {output_video}")

if __name__ == "__main__":
    main()