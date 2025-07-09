import os
def write_file(file_path, content, mode="w", encoding="utf-8"):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    # 如果是字符串写入，需要指定字符集为utf-8
    encoding = None
    if "b" in mode:
        encoding = None
    with open(file=file_path, mode=mode, encoding=encoding) as f:
        f.write(content)
        
        
def read_file(file_path, mode="r", encoding="utf-8"):
    try:
        if "b" in mode:
            encoding = None
        with open(file_path, mode=mode, encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"读取文件{file_path}遭遇异常{str(e)}")