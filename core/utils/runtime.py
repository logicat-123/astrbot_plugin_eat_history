import pathlib
def get_resource_path(*file_path):
    """
    获取运行时的资源文件路径
    
    :file_path 资源文件路径(相对于插件根目录)
    """
    return pathlib.Path(__file__).parent.parent.parent.joinpath(*file_path)