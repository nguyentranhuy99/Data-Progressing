import requests
from github import Github
import pandas as pd
import os

# Tạo một instance Github với access token
access_token = "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"
g = Github(access_token)

# Chi tiết repository
repo_owner = 'monkeytypegame'
repo_name = 'monkeytype'

# Lấy đối tượng repository
repo = g.get_repo(f"{repo_owner}/{repo_name}")

# Lấy tất cả pull requests mở và đóng
pull_prs = repo.get_pulls(state='all')

# Hàm để lấy số lượng test đã vượt qua cho một pull request
def get_tests_passed(pr):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{pr.head.sha}/check-suites"
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(url, headers=headers)
    check_suites = response.json().get('check_suites', [])

    total_tests = 0
    passed_tests = 0

    for suite in check_suites:
        suite_id = suite['id']
        check_runs_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/check-suites/{suite_id}/check-runs"
        check_runs_response = requests.get(check_runs_url, headers=headers)
        check_runs = check_runs_response.json().get('check_runs', [])

        for check in check_runs:
            total_tests += 1
            if check['conclusion'] == "success":
                passed_tests += 1

    return passed_tests, total_tests

# Hàm để chuyển đổi pull request thành dictionary
def pr_to_dict(pr):
    labels = [label.name for label in pr.labels]  # Lấy tên của các labels
    passed_tests, total_tests = get_tests_passed(pr)
    pr_state = "merged" if pr.merged else "closed" if pr.state == "closed" else "open"
    reviewers = [reviewer.login for reviewer in pr.get_review_requests()[0]]

    return {
        "number": pr.number,
        "title": pr.title,
        "created_at": pr.created_at,
        "updated_at": pr.updated_at,
        "additions": pr.additions,
        "deletions": pr.deletions,
        "commits": pr.commits,
        "author": pr.user.login,
        "labels": ", ".join(labels),  # Chuyển danh sách labels thành chuỗi
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "state": pr_state,
        "reviewers": ", ".join(reviewers)  # Chuyển danh sách reviewers thành chuỗi
    }

# Tạo danh sách chứa thông tin của các pull requests mở và đóng
pull_prs_data = [pr_to_dict(pr) for pr in pull_prs]

# Kiểm tra xem danh sách có rỗng không
if pull_prs_data:
    # Chuyển đổi danh sách thành DataFrame
    pull_prs_df = pd.DataFrame(pull_prs_data)
    # Lưu DataFrame vào file CSV
    pull_prs_df.to_csv('pull_requests.csv', index=False)
    print("Dữ liệu pull requests đã được lưu vào CSV.")
else:
    print("Không có pull requests nào.")

# Lấy tất cả các issues
issues = repo.get_issues(state='all')

def issue_to_dict(issue):
    labels = [label.name for label in issue.labels]  # Lấy tên của các labels
    issues_state = "closed" if issue.state == "closed" else "open"
    return {
        "number": issue.number,
        "title": issue.title,
        "created_at": issue.created_at,
        "updated_at": issue.updated_at,
        "comments": issue.comments,
        "author": issue.user.login,
        "labels": ", ".join(labels),  # Chuyển danh sách labels thành chuỗi
        "state": issues_state
    }

# Tạo danh sách chứa thông tin của các issues mở và đóng
issues_data = [issue_to_dict(issue) for issue in issues]

# Kiểm tra xem danh sách có rỗng không
if issues_data:
    # Chuyển đổi danh sách thành DataFrame
    issues_df = pd.DataFrame(issues_data)
    # Lưu DataFrame vào file CSV
    issues_df.to_csv('issues.csv', index=False)
    print("Dữ liệu issues đã được lưu vào CSV.")
else:
    print("Không có issues nào.")

# Lấy tất cả các commit
commits = repo.get_commits()

# Hàm để chuyển đổi commit thành dictionary
def commit_to_dict(commit):
    return {
        "sha": commit.sha,
        "author": commit.commit.author.name,
        "author_login": commit.author.login if commit.author else "N/A",
        "author_email": commit.commit.author.email,
        "date": commit.commit.author.date,
        "message": commit.commit.message,
        "url": commit.html_url
    }

# Tạo danh sách chứa thông tin của các commit
commits_data = [commit_to_dict(commit) for commit in commits]

# Chuyển đổi danh sách thành DataFrame
commits_df = pd.DataFrame(commits_data)

# Lưu DataFrame vào file CSV
commits_df.to_csv('commits.csv', index=False)

# In ra thông báo hoàn tất
print("Dữ liệu commits đã được lưu vào CSV.")

# Lấy danh sách contributors
contributors = repo.get_contributors()

# Hàm để chuyển đổi contributor thành dictionary
def contributor_to_dict(contributor):
    return {
        "login": contributor.login,
        "contributions": contributor.contributions,
        "url": contributor.html_url
    }

# Tạo danh sách chứa thông tin của các contributors
contributors_data = [contributor_to_dict(contributor) for contributor in contributors]

# Chuyển đổi danh sách thành DataFrame
contributors_df = pd.DataFrame(contributors_data)

# Lưu DataFrame vào file CSV
contributors_df.to_csv('contributors.csv', index=False)

# In ra thông báo hoàn tất
print("Dữ liệu contributors đã được lưu vào CSV.")

# Lấy thông tin ngôn ngữ lập trình
languages = repo.get_languages()

# Chuyển đổi dictionary thành DataFrame
languages_df = pd.DataFrame(list(languages.items()), columns=['Language', 'Lines of Code'])

# Lưu DataFrame vào file CSV
languages_df.to_csv('languages.csv', index=False)

# In ra thông báo hoàn tất
print("Thông tin ngôn ngữ lập trình đã được lưu vào CSV.")


# Tạo header chứa access token
headers = {
    'Authorization': f'token {access_token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Lấy danh sách người đóng góp
contributors_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contributors"
response = requests.get(contributors_url, headers=headers)
contributors = response.json()

# Lưu danh sách các cặp người đóng góp có mối quan hệ
contributors_edges = {}

# Lấy danh sách pull requests
pulls_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
response = requests.get(pulls_url, headers=headers)
pulls = response.json()

# Duyệt qua từng pull request và lấy thông tin về người tạo và người đánh giá (reviewers)
for pull in pulls:
    creator = pull['user']['login']
    reviewers_url = pull['url'] + "/reviews"
    response = requests.get(reviewers_url, headers=headers)
    reviewers = response.json()
    for reviewer in reviewers:
        if reviewer['user']['login'] != creator:  # Loại bỏ trường hợp người tạo đánh giá chính mình
            contributor_pair = (creator, reviewer['user']['login'])
            contributors_edges[contributor_pair] = contributors_edges.get(contributor_pair, 0) + 1

# Tạo DataFrame từ danh sách các cặp người đóng góp có mối quan hệ
df = pd.DataFrame(list(contributors_edges.items()), columns=['contributor_pair', 'collaborations'])

# Tách cột contributor_pair thành hai cột riêng biệt
df[['contributor', 'activity_with_contributor']] = pd.DataFrame(df['contributor_pair'].tolist(), index=df.index)

# Loại bỏ cột contributor_pair không cần thiết
df = df.drop(columns=['contributor_pair'])

# Lưu DataFrame vào file CSV
df.to_csv('contributors_activity.csv', index=False)

print("Dữ liệu đã được lưu vào file contributors_activity.csv")

# Kiểm tra và in ra đường dẫn của thư mục hiện tại
print("Current working directory:", os.getcwd())

Sử dụng token của bạn để kết nối với GitHub API

Lấy tất cả các tệp trong repository
files = repo.get_contents("")

file_data = []

def get_files(files):
    for file in files:
        if file.type == "dir":
            get_files(repo.get_contents(file.path))
        else:
            file_commits = repo.get_commits(path=file.path)
            commit_count = file_commits.totalCount
            file_data.append({
                "file_path": file.path,
                "file_size": file.size,
                "commits_count": commit_count
            })

get_files(files)

# Chuyển đổi danh sách thành DataFrame để dễ dàng phân tích
file_df = pd.DataFrame(file_data)

# Lưu DataFrame vào file CSV
file_df.to_csv('file_data.csv', index=False)
print("Dữ liệu các tệp, commits liên quan và kích thước đã được lưu vào CSV.")
