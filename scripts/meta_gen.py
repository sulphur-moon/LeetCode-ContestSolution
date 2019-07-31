# coding: utf-8
import os
import sys, getopt

content = {
	'title': '',
	'url': '',
	'level': '',
	'tags': '',
	'thoughts': '**思路：**',
	'code.python3': '**代码：**\n```python\n\n```'
}

level = {
	'简单': 'Easy',
	'中等': 'Medium',
	'困难': 'Hard'
}

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

# 根据题号生成元数据
def gen_meta_by_problem_id(problem_id):
	problem_dir = "../metadata/problems/" + str(problem_id)
	if os.path.exists(problem_dir):
		print('dir: "' + problem_dir + '" exists')
	else:
		print('mkdir: "' + problem_dir + '"')
		os.makedirs(problem_dir)
		items = ['title', 'url', 'level', 'tags', 'thoughts', 'code.python3']
		index = -1
		try:
			index = list_problem_id.index(int(problem_id))
		except Exception as e:
			print("problem_id not in list")
		if index != -1:
			content['title'] = list_problem_title[index]
			content['url'] = list_problem_url[index].split("/")[-1]
			content['level'] = level[list_problem_level[index]]
		for item in items:
			file_name = problem_dir + '/' + str(problem_id) + '.' + item + '.md'
			write_file_content(file_name, content[item])

# 读取所有题号、标题、链接和难度
list_problem_id = read_file_content("../metadata/list/id.txt").split("\n")
list_problem_id = list(map(int, list_problem_id))
list_problem_title = read_file_content("../metadata/list/title.txt").split("\n")
list_problem_title = list(map(str.strip, list_problem_title))
list_problem_url = read_file_content("../metadata/list/url.txt").split("\n")
list_problem_level = read_file_content("../metadata/list/level.txt").split("\n")

# 主程序
def main(argv):
	# 按照题号生成元数据
	problem_id = None
	# 按照题号生成元数据
	contest_id = None
	# 按照题号生成元数据
	bicontest_id = None
	# 获取命令行下参数
	try:
		opts, args = getopt.getopt(argv,"hi:c:b:",["id=", "contest=", "bicontest="])
	except getopt.GetoptError:
		print('sol_gen.py -i <problem_id>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('sol_gen.py -i <problem_id>')
			sys.exit()
		elif opt in ("-i", "--id"):
			problem_id = arg
			print('problem_id: ', problem_id)
		elif opt in ("-c", "--contest"):
			contest_id = arg
			print('contest_id: ', contest_id)
		elif opt in ("-b", "--bicontest"):
			bicontest_id = arg
			print('bicontest_id: ', bicontest_id)

	# 如果没有参数则输出提示并退出
	if not (problem_id or contest_id or bicontest_id):
		print('please input problem_id or contest_id or bicontest_id')
		sys.exit()
	elif problem_id:
		gen_meta_by_problem_id(problem_id)
	elif contest_id:
		print("contest:", contest_id)
		contest_list = read_file_content("../metadata/contest/weekly.contest." + str(contest_id) + ".md").split("\n")
		for p in contest_list:
			gen_meta_by_problem_id(int(p))
	elif bicontest_id:
		pass


if __name__ == "__main__":
	main(sys.argv[1:])

