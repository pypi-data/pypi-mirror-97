# -*- coding: utf-8 -*-
import git
import os
import argparse
import re


def print_head_and_body(prev, head, lines):
    GREEN = '\033[34m'
    END = '\033[0m'
    print(GREEN + prev + '..' + head + END)
    for line in lines:
        print(line)
    print('\n')


def generate_body(prev, head):
    root = get_git_root('./')
    repo_name = os.path.basename(root)
    repo = git.Repo(root)
    lines = []
    for item in repo.iter_commits(prev + '..' + head, min_parents=2):
        if ('Merged in' in item.message and 'pull request #' in item.message and 'Approved-by:' in item.message) or (
                'Merge pull request #' in item.message):
            splitlines = item.message.splitlines()
            message = "Commit message is empty" if (len(splitlines) < 3) else splitlines[2]
            result = re.search(r'#\d+', splitlines[0])
            pullreq_no = result.group()[1:]
            author = item.author.name
            if 'Merged in' in item.message and 'pull request #' in item.message and 'Approved-by:' in item.message:
                lines.append(
                    '- [{0}](https://bitbucket.org/uzabase/{1}/pull-requests/{2}) @{3}'.format(message,
                                                                                               repo_name,
                                                                                               pullreq_no,
                                                                                               author))
            if 'Merge pull request #' in item.message:
                lines.append(
                    '- [{0}](https://github.com/newspicks/{1}/pull/{2}) @{3}'.format(message,
                                                                                     repo_name,
                                                                                     pullreq_no,
                                                                                     author))
    return lines


def get_git_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root


def main():
    parser = argparse.ArgumentParser(description='reldoc is tool to list git commit messages',
                                     usage='reldoc [--match=<regex> | -m=<regex>]')
    parser.add_argument('-m', '--match', action='store',
                        help='specify regex to get previous release tag. "git describe --match <regex> --abbrev=0". default is "*[^(infra)]"')
    args = parser.parse_args()
    match = '*[^(infra)]' if args.match is None else args.match

    g = git.Git('./')
    prev_tag = g.execute(['git', 'describe', '--tags', '--match', match, '--abbrev=0'])
    body = generate_body(prev_tag, 'HEAD')
    print_head_and_body(prev_tag, 'HEAD', body)

if __name__ == '__main__':
    main()
