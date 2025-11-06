import os
import subprocess

# 定义主文件夹路径
main_folder = "E:\\ysw_xml"

# 定义子文件夹列表
subfolders = ["CK_XML", "DL_XML", "SL_XML", "UL_XML"]

# 定义Smetana脚本的路径
smetana_script_path = "D:\\Software02\\Anaconda3\\envs\\smetana_env\\Scripts\\smetana"

# 遍历每个主文件夹
for folder in subfolders:
    folder_path = os.path.join(main_folder, folder)
    
    # 遍历每个子文件夹
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        
        # 检查是否是文件夹
        if os.path.isdir(subfolder_path):
            print(f"正在处理文件夹: {subfolder_path}")
            
            # 激活conda环境并运行Smetana命令
            command = f"conda activate smetana_env && cd {subfolder_path} && python {smetana_script_path} *.xml -c communities.tsv"
            
            # 使用subprocess运行命令
            subprocess.run(command, shell=True)
