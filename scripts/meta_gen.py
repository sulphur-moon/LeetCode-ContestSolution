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
	# 按照题号生成元数据
	problem_id = None

	content = {
		'title': '',
		'url': '',
		'level': 'Easy\nMedium\nHard',
		'description': '',
		'examples': '',
		'notes': '',
		'tags': '',
		'thoughts': '**思路：**',
		'code.python3': '**代码：**\n```python\n\n```'
	}

	# 获取命令行下参数
	try:
		opts, args = getopt.getopt(argv,"hi:",["id="])
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

	# 如果没有参数则输出提示并退出
	if not problem_id:
		print('please input problem_id')
		sys.exit()
	else:
		problem_dir = "../metadata/problems/" + str(problem_id)
		if os.path.exists(problem_dir):
			print('dir: "' + problem_dir + '" exists')
		else:
			os.makedirs(problem_dir)
			items = ['title', 'url', 'level', 'description', 'examples', 'notes', 'tags', 'thoughts', 'code.python3']
			for item in items:
				file_name = problem_dir + '/' + str(problem_id) + '.' + item + '.md'
				write_file_content(file_name, content[item])

if __name__ == "__main__":
	main(sys.argv[1:])

