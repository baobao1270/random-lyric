import os
import re
import sys
import json
import shutil
import argparse

class FILENAMES:
    SOURCE_DATABASE       = 'database.txt'
    TEMPLATE_SHELL_SCRIPT = 'template.sh'
    DIST_SHELL            = 'dist/fortune-lyric.sh'
    DIST_SHELL_MULTILINE  = 'dist/fortune-lyric-multiline.sh'
    DIST_JSON             = 'dist/fortune-lyric.json'
    DIST_JSON_MINIFIED    = 'dist/fortune-lyric.min.json'
    DIST_TEXT             = 'dist/fortune-lyric.txt'
    DIST_DB               = 'dist/database.txt'

def colored(color: str, text: str) -> str:
    colors = {
        'red': '\033[1;31m',
        'green': '\033[1;32m',
        'yellow': '\033[1;33m',
        'blue': '\033[1;34m',
    }
    return colors[color] + text + '\033[0m'


def print_ident(indent: int, lines: list[str], prefix: str = '',
                color = None, ident_first_line: bool = False):
    if color is not None:
        lines = [colored(color, line) for line in lines]
    for i, line in enumerate(lines):
        if i == 0 and ident_first_line:
            print(' ' * 0      + prefix+ line)
        else:
            print(' ' * indent + prefix + line)


def print_file_size(filename: str):
    size = os.stat(filename).st_size
    size_kb = f"{size / 1024:.2f} KB"
    color = 'green' if size < 1024 * 10 else 'yellow'
    size_kb = "[" + colored(color, size_kb) + "]"
    print(colored('green', 'Success:'), f"{filename:<35}", f"{size_kb:>30}")


def load():
    with open(FILENAMES.SOURCE_DATABASE, "rb") as f:
        if b'\r' in f.read():
            print(colored('red', 'Error:'), '数据库文件中不得包含 CR (\\r) 字符')
            sys.exit(-2)
    with open(FILENAMES.SOURCE_DATABASE, encoding='utf-8') as f:
        database = f.read()
        if not database.endswith('\n'):
            print(colored('red', 'Error:'), '数据库文件应该以 LF (\\n) 结尾')
            sys.exit(-2)
        database = database.strip()
        database = [i.strip() for i in database.split('-' * 30)]
        if (database[0] == '') or (database[-1] == ''):
            print(colored('red', 'Error:'), '遇到了空的歌词块 (quoteblock)')
            print_ident(len('Error: '), [
                '数据库文件的开头和结尾不应该有横线 (\'---...---\')，请移除之。',
            ])
            sys.exit(-2)
    result = []
    for quoteblock in database:
        quoteblock_lines = [i.strip() for i in quoteblock.split('\n')]
        lyric_lines, lyric_metadata = quoteblock_lines[:-1], quoteblock_lines[-1]
        metadata_re = re.compile(r"^-- (.+) 《(.+)》, (\d{4})$")
        if not metadata_re.match(lyric_metadata):
            print(colored('red', 'Error:'), '歌词块 (quoteblock) 作者、歌名或年份格式错误')
            print_ident(len('Error: '), [
                '歌词块 (quoteblock) 的最后一行应该为歌词作者、歌名和年份，格式为：',
                '> ' + colored('green', '-- 作者 《歌名》, 年份'),
                '发生错误的数据为：',
                '> ' + colored('yellow', lyric_metadata),
                '请检查该行是否符合格式。',
            ])
            print("Lyric: ", end='')
            print_ident(len('Lyric: '), quoteblock_lines, prefix='> ', color="yellow", ident_first_line=True)
            sys.exit(-2)
        lyric_author, lyric_title, lyric_year = metadata_re.match(lyric_metadata).groups()
        lyric_author = [i.strip() for i in lyric_author.strip().split('/')]
        lyric_year = int(lyric_year)
        for i, line in enumerate(lyric_lines):
            if line == '':
                print(colored('red', 'Error:'), '遇到了空的歌词行')
                print_ident(len('Error: '), [f'在第 {i + 1} 行',])
                print("Lyric: ", end='')
                print_ident(len('Lyric: '), quoteblock_lines, prefix='> ', color="yellow", ident_first_line=True)
                sys.exit(-2)
            if line.startswith('-') or line.endswith('-'):
                print(colored('red', 'Error:'), '歌词行不能以 \'-\' 开头或结尾')
                print_ident(len('Error: '), [f'在第 {i + 1} 行',])
                print("Lyric: ", end='')
                print_ident(len('Lyric: '), quoteblock_lines, prefix='> ', color="yellow", ident_first_line=True)
                sys.exit(-2)
            if len(line.encode('gb18030')) > 30:
                print(colored('red', 'Error:'), f'歌词单行不能超过 30 个字节 (GB18030 编码)，该行为 {len(line.encode("gb18030"))} 个字节')
                print_ident(len('Error: '), [f'在第 {i + 1} 行', colored('blue', line)])
                print("Lyric: ", end='')
                print_ident(len('Lyric: '), quoteblock_lines, prefix='> ', color="yellow", ident_first_line=True)
                sys.exit(-2)
            if len(' '.join(lyric_lines).encode('gb18030')) > 80:
                print(colored('red', 'Error:'), f'歌词行总字数不能超过 80 个字节 (GB18030 编码)，该行为 {len(" ".join(lyric_lines).encode("gb18030"))} 个字节')
                print_ident(len('Error: '), [colored('blue', ' '.join(lyric_lines))])
                print("Lyric: ", end='')
                print_ident(len('Lyric: '), quoteblock_lines, prefix='> ', color="yellow", ident_first_line=True)
                sys.exit(-2)
            if len(lyric_lines) > 4:
                print(colored('red', 'Error:'), f'歌词行数不能超过 4 行，该块为 {len(lyric_lines)} 行')
                print("Lyric: ", end='')
                print_ident(len('Lyric: '), quoteblock_lines, prefix='> ', color="yellow", ident_first_line=True)
                sys.exit(-2)
        result.append({
            'author': lyric_author,
            'title': lyric_title,
            'year': lyric_year,
            'lines': lyric_lines,
        })
    return result


def build_json(database: list[dict]):
    os.makedirs(os.path.dirname(FILENAMES.DIST_JSON), exist_ok=True)
    with open(FILENAMES.DIST_JSON, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(database, ensure_ascii=False, indent=4))
    print_file_size(FILENAMES.DIST_JSON)
    with open(FILENAMES.DIST_JSON_MINIFIED, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(database, ensure_ascii=True))
    print_file_size(FILENAMES.DIST_JSON_MINIFIED)


def build_text(database: list[dict]):
    lines = [
        ' '.join(quote['lines']).replace(' ', '\u3000')
        for quote in database
    ]
    lines = '\n'.join(lines)
    os.makedirs(os.path.dirname(FILENAMES.DIST_TEXT), exist_ok=True)
    with open(FILENAMES.DIST_TEXT, 'w+', encoding='utf-8') as f:
        f.write(lines)
    print_file_size(FILENAMES.DIST_TEXT)


def build_bash(database: list[dict]):
    lines = [
        "    \"" + ' '.join(quote['lines']) + "\""
        for quote in database
    ]
    lines = '\n'.join(lines)
    os.makedirs(os.path.dirname(FILENAMES.DIST_SHELL), exist_ok=True)
    with open(FILENAMES.TEMPLATE_SHELL_SCRIPT, encoding='utf-8') as f:
        tmpl = f.read().strip()
    with open(FILENAMES.DIST_SHELL, 'w+', encoding='utf-8') as f:
        f.write(tmpl.replace('%%DATABASE%%', lines) + "\n")
    print_file_size(FILENAMES.DIST_SHELL)
    os.chmod(FILENAMES.DIST_SHELL, 0o755)


def build_bash_multiline(database: list[dict]):
    lines = [
        "    \"" + '\\n'.join(quote['lines']) + "\\n\\n" +
        (" " * (max([len(i.encode("gb18030")) for i in quote['lines']]) - 8)) +
        f"-- " + "/".join(quote['author']) + f"《{quote['title']}》 ({quote['year']})\\n" + "\""
        for quote in database
    ]
    lines = '\n'.join(lines)
    os.makedirs(os.path.dirname(FILENAMES.DIST_SHELL_MULTILINE), exist_ok=True)
    with open(FILENAMES.TEMPLATE_SHELL_SCRIPT, encoding='utf-8') as f:
        tmpl = f.read().strip()
    with open(FILENAMES.DIST_SHELL_MULTILINE, 'w+', encoding='utf-8') as f:
        f.write(tmpl.replace('%%DATABASE%%', lines) + "\n")
    print_file_size(FILENAMES.DIST_SHELL_MULTILINE)
    os.chmod(FILENAMES.DIST_SHELL_MULTILINE, 0o755)


def build_copy():
    shutil.copy(FILENAMES.SOURCE_DATABASE, FILENAMES.DIST_DB)
    print_file_size(FILENAMES.DIST_DB)


def build_publish(namespace_id: str):
    if not os.path.exists(FILENAMES.DIST_JSON):
        print(colored('red', 'Error:'), f"文件 {FILENAMES.DIST_JSON} 不存在, build_publish 必须在 build_json 之后执行")
        sys.exit(-2)
    result = os.system(f"wrangler kv:key put --namespace-id {namespace_id} fortune-lyric --path {FILENAMES.DIST_JSON}")
    if result != 0:
        print(colored('yellow', 'Info:'), "命令返回值：", result)
        print(colored('red', 'Error:'), 'wrangler kv:key put 执行失败')
        sys.exit(-2)
    print(colored('green', 'Success:'), 'wrangler kv:key put 执行成功')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--publish', action='store_true', help='发布到 Cloudflare KV')
    args = parser.parse_args()

    if not args.publish:
        print(colored('yellow', 'Info:'), '如需发布到 Cloudflare KV，请使用 --publish 参数。')

    database = load()
    build_json(database)
    build_text(database)
    build_bash(database)
    build_bash_multiline(database)
    build_copy()
    if args.publish:
        build_publish("0addc370401c4b77b57c9d40fddf9ad6")
