import sys  # 导入sys模块
from os.path import join, dirname, abspath, isfile
parent_folder_path = abspath(dirname(dirname(__file__)))
sys.path.append(parent_folder_path)
sys.path.append(join(parent_folder_path, 'lib'))
sys.path.append(join(parent_folder_path, 'plugin'))
sys.path.append(join(parent_folder_path, 'test'))


if __name__ == '__main__':
    from plugin.main import VscodeOpen
    print(VscodeOpen().query("test"))
