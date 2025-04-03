import os

unpaired = []

# 遍历根目录及其所有子目录
for root, _, files in os.walk('.'):
    mp4_files = {}
    jpg_files = {}
    
    # 收集当前目录下的MP4和JPG文件
    for filename in files:
        filepath = os.path.join(root, filename)
        basename, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext == '.mp4':
            mp4_files[basename] = filepath
        elif ext == '.jpg':
            jpg_files[basename] = filepath
    
    # 检查当前目录中的不成对文件
    # 没有对应JPG的MP4文件
    for basename, path in mp4_files.items():
        if basename not in jpg_files:
            unpaired.append(path)
    # 没有对应MP4的JPG文件
    for basename, path in jpg_files.items():
        if basename not in mp4_files:
            unpaired.append(path)

# 输出结果
if unpaired:
    print("以下文件不成对:")
    for path in unpaired:
        print(f"• {path}")
else:
    print("所有MP4和JPG文件都成对存在！")