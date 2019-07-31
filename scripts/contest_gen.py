# coding: utf-8
import os
import sys, getopt


# 读取文件
def read_file_content(file_name):
	content = None
	with open(file_name, "r", encoding="utf-8") as f:
		content = f.read()
		f.close()
	return content

# 写入文件
def write_file_content(file_name, content):
	with open(file_name, "w", encoding="utf-8") as f:
		f.write(content)
		f.close()
	return

# 主程序
def main(argv):
	contest_list = read_file_content("../metadata/list/contest-problems.txt").split("\n")
	problem_list = read_file_content("../metadata/list/title.txt").split("\n")
	# print(contest_list)
	d = dict()
	for i, p in enumerate(problem_list):
		d[p.strip()] = i
	# print(d)
	ids = []
	contest_id = None
	for i in range(len(contest_list)):
		if i % 5 == 0:
			contest_id = int(contest_list[i])
			if contest_id > 141:
				break
			print(contest_id)
			ids = []
		else:
			ids.append(str(d[contest_list[i]]))
		if i % 5 == 4:
			content = '\n'.join(ids)
			# print(content)
			write_file_content("weekly.contest." + str(contest_id) + ".md", content)
			write_file_content("weekly.contest." + str(contest_id) + ".evaluation.md", "本周比赛，等算法。")


if __name__ == "__main__":
	main(sys.argv[1:])

