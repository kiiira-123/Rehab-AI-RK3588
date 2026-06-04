import os
import sys

# 设置基础路径 (请确保这些路径与你的实际目录结构一致)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = ROOT_DIR  # 因为脚本已经在 models 文件夹里了，直接用当前目录
PT_PATH   = os.path.join(MODELS_DIR, "yolov8s-pose.pt")
ONNX_PATH = os.path.join(MODELS_DIR, "yolov8s-pose.onnx")
RKNN_PATH = os.path.join(MODELS_DIR, "yolov8s-pose-int8.rknn") # 新的 INT8 模型名
DATASET_PATH = os.path.join(MODELS_DIR, "dataset.txt") # 校准数据集路径

def step1_pt_to_onnx():
    """步骤1: PyTorch → ONNX"""
    from ultralytics import YOLO

    print("\n[Step 1/2] 加载 PyTorch 模型...")
    model = YOLO(PT_PATH)

    print("[Step 1/2] 导出 ONNX (opset=12, imgsz=640)...")
    # 注意：导出时强制输入尺寸为 640x640
    result = model.export(format="onnx", opset=12, imgsz=640)
    print(f"[Step 1/2] ONNX 导出完成 → {result}")

def step2_onnx_to_rknn():
    """步骤2: ONNX → RKNN (开启 INT8 量化)"""
    try:
        from rknn.api import RKNN
    except ImportError:
        print("\n[致命错误] 未找到 rknn-toolkit2 环境！")
        sys.exit(1)

    print("\n[Step 2/2] 正在转换 ONNX → RKNN (激活 INT8 量化引擎)...")
    rknn = RKNN(verbose=False) # 如果你想看满屏的日志，可以改成 True

    # 这里的 mean 和 std 必须和 YOLOv8 训练时的预处理保持一致
    rknn.config(
        mean_values=[[0, 0, 0]],
        std_values=[[255, 255, 255]],
        target_platform="rk3588",
        optimization_level=3 # 开启最高级别图优化
    )

    ret = rknn.load_onnx(model=ONNX_PATH)
    if ret != 0:
        print(f"[错误] ONNX 加载失败! ret={ret}")
        return

    # 【核心开关】：开启量化，并传入校准数据集！
    print("           正在进行激活值校准与量化，这可能需要几分钟...")
    ret = rknn.build(do_quantization=True, dataset=DATASET_PATH)
    if ret != 0:
        print(f"[错误] RKNN 量化构建失败! 请检查 dataset.txt 是否正确。ret={ret}")
        return

    ret = rknn.export_rknn(RKNN_PATH)
    if ret == 0:
        print(f"[Step 2/2] INT8 量化版 RKNN 导出成功 → {RKNN_PATH}")
    else:
        print(f"[错误] RKNN 导出失败! ret={ret}")

    rknn.release()

def main():
    if not os.path.exists(PT_PATH):
        print(f"[错误] 找不到权重文件: {PT_PATH}")
        sys.exit(1)
        
    if not os.path.exists(DATASET_PATH):
        print(f"[错误] 找不到校准文件: {DATASET_PATH}")
        sys.exit(1)

    step1_pt_to_onnx()
    step2_onnx_to_rknn()
    print("\n>>> 转换彻底完成！你可以开始推送到板子上了！ <<<")

if __name__ == "__main__":
    main()