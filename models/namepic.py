import os

def save_image_paths_to_txt(folder_path, output_txt_path, is_absolute=True):
    """
    将文件夹中所有图片的路径写入到指定的txt文件中。
    """
    # 定义常见的图片扩展名，支持大小写（例如 .JPG 也会被统一转小写后匹配）
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    # 检查输入的文件夹路径是否存在
    if not os.path.isdir(folder_path):
        print(f"错误：找不到指定的文件夹路径 -> {folder_path}")
        return

    try:
        # 打开（或创建）TXT文件用于写入
        with open(output_txt_path, 'w', encoding='utf-8') as file:
            
            # 使用 os.walk 遍历文件夹（包括所有子文件夹）
            for root, dirs, files in os.walk(folder_path):
                for filename in files:
                    # 获取文件扩展名并转为小写进行匹配
                    ext = os.path.splitext(filename)[1].lower()
                    
                    if ext in valid_extensions:
                        # 拼接完整的文件路径
                        full_path = os.path.join(root, filename)
                        
                        if is_absolute:
                            # 转换为绝对路径
                            final_path = os.path.abspath(full_path)
                        else:
                            # 转换为相对于目标文件夹的相对路径
                            final_path = os.path.relpath(full_path, start=folder_path)
                        
                        # 写入文件，并在末尾添加换行符
                        file.write(f"{final_path}\n")
                        
        print(f"✅ 成功！图片路径已全部写入到 -> {output_txt_path}")
        
    except Exception as e:
        print(f"❌ 处理过程中发生错误: {e}")

# ==========================================
# 你的专属配置
# ==========================================
if __name__ == "__main__":
    # 1. 你的图片文件夹地址
    TARGET_FOLDER = "/home/jojo/LLZ/models/dataset" 
    
    # 2. 生成的 txt 文件地址
    OUTPUT_TXT = "/home/jojo/LLZ/models/dataset.txt"
    
    # 3. 运行函数 
    # 如果你想要绝对路径 (如 /home/jojo/LLZ/models/dataset/img1.png)，保持 is_absolute=True
    # 如果你想要相对路径 (如 img1.png 或者 subfolder/img1.png)，将 is_absolute 改为 False
    save_image_paths_to_txt(
        folder_path=TARGET_FOLDER, 
        output_txt_path=OUTPUT_TXT, 
        is_absolute=True  
    )