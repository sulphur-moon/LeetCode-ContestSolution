# coding: utf-8
import os
import sys, getopt

# 写入文件
def write_file_content(file_name, content):
	with open(file_name, "w", encoding="utf-8") as f:
		f.write(content)
		f.close()
	return

# 主程序
def main(argv):
	for i in range(7, 21):
		file_name = "biweekly.contest." + str(i) + ".md"
		write_file_content(file_name, "")
		file_name = "biweekly.contest." + str(i) + ".evaluation.md"
		write_file_content(file_name, "本周比赛，等算法。")

if __name__ == "__main__":
	main(sys.argv[1:])

