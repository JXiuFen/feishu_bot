from program_entry import start

try:
    start.program_entry()
except KeyboardInterrupt:
    print('程序结束...')


# nohup python main.py > output.log 2>&1 &
