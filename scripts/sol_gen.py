# coding: utf-8
import os
import sys, getopt


# 题目难度颜色表
color = {
	'Easy': "#5CB85C",
	'Medium': "#F0AD4E",
	'Hard': "#D9534F"
}
font_color_prefix = "<font color=color_code>**"
font_color_suffix = "**</font>\n\n"
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
	# 按照题号生成题解
	problem_id = None
	# 按照竞赛生成题解
	contest_id = None
	# 双周赛题解
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
			contest_id = arg
			print('bicontest_id: ', bicontest_id)

	# 如果没有参数则输出提示并退出
	if not problem_id and not contest_id and not bicontest_id:
		print('please input problem_id or contest_id or bicontest_id')
		sys.exit()

	file_name = None
	if contest_id:
		file_name = "../metadata/contest/weekly.contest." + str(contest_id) + ".md"
		problem_list = read_file_content(file_name)
		if problem_list:
			problem_list = problem_list.split()
		print("problem_list: ", problem_list)
		solution_file_name = "Weekly Contest " + contest_id + " Solution.md"
		solution_file_content = "## Weekly Contest " + contest_id + " Solution\n\n"
		contest_evaluation = read_file_content("../metadata/contest/weekly.contest." + str(contest_id) + ".evaluation.md")
		if contest_evaluation:
			solution_file_content += contest_evaluation + "\n\n"
		for problem_id in problem_list:
			prefix = "../metadata/problems/" + problem_id + "/" + problem_id
			title = read_file_content(prefix + ".title.md")
			url = read_file_content(prefix + ".url.md")
			description = read_file_content(prefix + ".description.md")
			level = read_file_content(prefix + ".level.md")
			examples = read_file_content(prefix + ".examples.md")
			notes = read_file_content(prefix + ".notes.md")
			tags = read_file_content(prefix + ".tags.md")
			thoughts = read_file_content(prefix + ".thoughts.md")
			code_python3 = read_file_content(prefix + ".code.python3.md")
			solution_file_content += "### [" + problem_id + '.' + title + "](" + url + ")\n\n"
			solution_file_content += "**题目难度**" + font_color_prefix.replace("color_code", color[level]) + level + font_color_suffix
			solution_file_content += description + "\n" + examples + "\n" + notes + "\n" + thoughts + "\n" + code_python3 + "\n"
		print(solution_file_content)
		write_file_content(solution_file_name, solution_file_content)
	elif bicontest_id:
		file_name = "../metadata/contest/biweekly.contest." + str(bicontest_id) + ".md"
	elif problem_id:
		folder_name = "../metadata/problems/" + str(problem_id) + "/"


if __name__ == "__main__":
	main(sys.argv[1:])

