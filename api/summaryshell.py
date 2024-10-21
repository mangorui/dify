import os


def read_file(file_path):
    try:
        with open(file_path, encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {str(e)}")
        return ""


def write_summary(output_file, content):
    try:
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(content + '\n\n')
    except Exception as e:
        print(f"写入输出文件时出错: {str(e)}")


def summarize_project(project_path, output_file):
    print(f"开始分析项目: {project_path}")
    print(f"输出文件: {output_file}")

    file_count = 0
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'build', 'dist', 'venv', '.idea', '.vscode', '__pycache__', '.husky', '.next']]
        for file in files:
            if file.endswith(('.js', '.ts', '.tsx', '.py', '.json', '.md')):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_path)
                print(f"正在处理文件: {relative_path}")
                content = f"File: {relative_path}\n\n{read_file(file_path)}\n{'=' * 80}\n"
                write_summary(output_file, content)
                file_count += 1

    print(f"项目分析完成。共处理 {file_count} 个文件。")


def main():
    # 在这里直接指定项目路径和输出文件
    project_path = '/Users/mango/work/Dify/dify/web'
    output_file = '/Users/mango/work/Dify/dify/web/project_summary.txt'

    if not os.path.exists(project_path):
        print(f"错误: 项目路径 '{project_path}' 不存在")
        return

    try:
        summarize_project(project_path, output_file)
        print(f"摘要已成功保存到文件: {output_file}")
    except Exception as e:
        print(f"在处理过程中遇到错误: {str(e)}")


if __name__ == "__main__":
    main()