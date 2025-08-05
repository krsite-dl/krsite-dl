import re
import subprocess
import sys
import argparse

def get_previous_tag(current_tag):
    """Get the tag before the current one."""
    try:
        cmd = ['git', 'describe', '--tags', '--abbrev=0', f'{current_tag}^']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        try:
            first_commit_cmd = ['git', 'rev-list', '--max-parents=0', 'HEAD']
            first_commit_result = subprocess.run(first_commit_cmd, capture_output=True, text=True, check=True)
            return first_commit_result.stdout.strip()
        except subprocess.CalledProcessError:
            return ''

def get_commits(from_rev, to_rev):
    """Get commits in a given range."""
    if not from_rev:
        cmd = ['git', 'log', '--pretty=format:%s', to_rev]
    else:
        cmd = ['git', 'log', '--pretty=format:%s', f'{from_rev}..{to_rev}']
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return [line for line in result.stdout.strip().split('\n') if line]

def format_changelog(commits):
    """Format commits into a changelog."""
    changelog = []
    commit_map = {
        'feat': '### Features',
        'fix': '### Bug Fixes',
        'docs': '### Documentation',
        'refactor': '### Refactor',
        'chore': '### Miscellaneous Tasks',
        'style': '### Styling',
        'test': '### Testing',
        'perf': '### Performance',
        'revert': '### Reverts',
        'build': '### Build',
    }
    grouped_commits = {key: [] for key in commit_map.values()}
    other_commits = []

    for commit in commits:
        match = re.match(r'^(\w+)(?:\((.+)\))?!?: (.+)', commit)
        if not match:
            other_commits.append(f'- {commit}')
            continue
        commit_type, scope, message = match.groups()
        group = commit_map.get(commit_type)

        formatted_message = f'- {message.strip()}'
        if scope:
            formatted_message = f'- **{scope.strip()}**: {message.strip()}'

        if group:
            grouped_commits[group].append(formatted_message)
        else:
            other_commits.append(formatted_message)

    for group, messages in grouped_commits.items():
        if messages:
            changelog.append(group)
            changelog.extend(sorted(messages))
            changelog.append('')

    if other_commits:
        changelog.append('### Other')
        changelog.extend(sorted(other_commits))
        changelog.append('')

    return '\n'.join(changelog)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a changelog for a git tag.')
    parser.add_argument('--tag', help='The tag to generate the changelog for. Defaults to the latest tag.')
    parser.add_argument('--package-name', help='The name of the package for PyPI link.')
    args = parser.parse_args()

    if args.tag:
        current_tag = args.tag
    else:
        try:
            latest_tag_cmd = ['git', 'describe', '--tags', '--abbrev=0']
            current_tag = subprocess.run(latest_tag_cmd, capture_output=True, text=True, check=True).stdout.strip()
        except subprocess.CalledProcessError:
            sys.exit("Error: Could not determine the latest tag. Please create a tag first or provide one with --tag.")

    previous_tag = get_previous_tag(current_tag)
    print(f"Generating changelog for {current_tag} (since {previous_tag})...", file=sys.stderr)

    commits = get_commits(previous_tag, current_tag)
    if not commits:
        print(f"No new commits found for tag {current_tag} since {previous_tag}.", file=sys.stderr)
        changelog_content = "No changes in this release."
    else:
        changelog_content = format_changelog(commits)

    with open('CHANGELOG.md', 'w', encoding='utf-8') as f:
        f.write(f"# Changelog for {current_tag}\n\n")
        if args.package_name:
            pypi_link = f"https://pypi.org/project/{args.package_name}/{current_tag}/"
            f.write(f"[![PyPI - Version](https://img.shields.io/pypi/v/{args.package_name}?style=for-the-badge)]({pypi_link})\n\n")
        f.write(changelog_content)

    print("CHANGELOG.md generated successfully.")
