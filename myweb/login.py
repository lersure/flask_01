import subprocess

res = subprocess.Popen("mkdir newfile", shell=True, stdout=subprocess.PIPE)
# 检查命令有没有执行完毕，没有执行完返回None，执行完毕返回结果的状态
print(res.poll())
res.stdout.close()
