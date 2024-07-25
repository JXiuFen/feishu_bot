#!/bin/bash

# 检查并终止已存在的 python main.py 进程
process_id=$(pgrep -f "python main.py")
if [ ! -z "$process_id" ]; then
    echo "结束进程 PID: $process_id"
    kill -9 $process_id
fi

# 激活 conda 环境
source /root/anaconda3/etc/profile.d/conda.sh  # 根据实际情况修改路径
conda activate feishu

# 获取当前日期并格式化为 YYYYMMDD
current_date=$(date +"%Y%m%d")

# 使用 nohup 后台运行 python main.py，并将日志文件命名为当前日期
nohup python main.py > "${current_date}.log" 2>&1 &

echo "开始程序，文件log: ${current_date}.log"
