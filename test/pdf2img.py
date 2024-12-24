from pdf2image import convert_from_path
import os

# 确保 Poppler 已正确安装。如果 Poppler 不在环境变量中，需要指定路径：
# POPPLER_PATH =  "/mnt/afs/yaotiankuo/8tools8/poppler-24.12.0"

def test_pdf2image():
    # 测试用 PDF 文件路径
    pdf_path = "test.pdf"  # 替换为实际 PDF 路径
    output_dir = "output_images"  # 输出目录

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    try:
        # 将 PDF 转换为图像
        images = convert_from_path(pdf_path, dpi=300)

        # 保存每一页为单独的图片
        for i, image in enumerate(images):
            output_file = os.path.join(output_dir, f"page_{i + 1}.jpg")
            image.save(output_file, "JPEG")
            print(f"Page {i + 1} saved as {output_file}")

        print("PDF 转换为图像成功！")
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == "__main__":
    test_pdf2image()
