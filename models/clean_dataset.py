import os

# 你的数据集绝对路径
DATASET_DIR = "/home/jojo/LLZ/models/dataset"
TXT_PATH = "/home/jojo/LLZ/models/dataset.txt"

def main():
    if not os.path.exists(DATASET_DIR):
        print(f"[错误] 找不到目录: {DATASET_DIR}")
        return

    print("第一步：正在强力清洗文件名中的空格与特殊字符...")
    count = 0
    for filename in os.listdir(DATASET_DIR):
        old_path = os.path.join(DATASET_DIR, filename)
        if os.path.isdir(old_path):
            continue

        # 1. 把空格替换为下划线，去掉括号、问号和感叹号
        new_filename = (filename.replace(" ", "_")
                                .replace("(", "")
                                .replace(")", "")
                                .replace("？", "")
                                .replace("！", "")
                                .replace("?", "")
                                .replace("!", ""))
        new_path = os.path.join(DATASET_DIR, new_filename)

        # 2. 执行物理重命名
        if old_path != new_path:
            os.rename(old_path, new_path)
            count += 1

    print(f"成功重命名了 {count} 个刺客文件！")

    print("\n第二步：正在重新生成绝对纯净的 dataset.txt...")
    valid_images = []
    for filename in os.listdir(DATASET_DIR):
        # 只抓取真正的图片
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # 写入绝对路径，瑞芯微最喜欢绝对路径
            valid_images.append(os.path.join(DATASET_DIR, filename))

    with open(TXT_PATH, "w") as f:
        for img_path in valid_images:
            f.write(img_path + "\n")

    print(f"成功！写入了 {len(valid_images)} 张合规校准图片到 {TXT_PATH}")

if __name__ == "__main__":
    main()