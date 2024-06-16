
import pandas as pd

# NOTE: YOU NEED TO COMMAND OTHER PARTS IF YOU WANT TO RUN A PART

# Đọc dữ liệu từ các file CSV
commits_df = pd.read_csv('commits.csv')
issues_df = pd.read_csv('issues.csv')

# Chuyển đổi cột thời gian sang định dạng datetime
commits_df['date'] = pd.to_datetime(commits_df['date'])
issues_df['created_at'] = pd.to_datetime(issues_df['created_at'])

# Tạo cột 'month_year' để nhóm theo tháng
commits_df['month_year'] = commits_df['date'].dt.to_period('M')
issues_df['month_year'] = issues_df['created_at'].dt.to_period('M')

# Tạo danh sách hợp nhất hoạt động của contributors
activity_data = []

# Lấy dữ liệu từ commits
for _, row in commits_df.iterrows():
    activity_data.append({
        "contributor": row['author'],
        "activity_type": "commit",
        "month_year": row['month_year']
    })

# Lấy dữ liệu từ issues
for _, row in issues_df.iterrows():
    activity_data.append({
        "contributor": row['author'],
        "activity_type": "issue",
        "month_year": row['month_year']
    })

# Chuyển đổi danh sách thành DataFrame để dễ dàng phân tích
activity_df = pd.DataFrame(activity_data)

# Tính số lần hoạt động của mỗi contributor theo tháng
activity_counts_by_month = activity_df.groupby(['contributor', 'month_year']).size().reset_index(name='activity_count')

# Tính số tháng hoạt động của mỗi contributor
months_active = activity_counts_by_month.groupby('contributor').size().reset_index(name='months_active')

# Tính tổng số hoạt động của mỗi contributor
total_activity = activity_df['contributor'].value_counts().reset_index()
total_activity.columns = ['contributor', 'total_activity']

# Kết hợp dữ liệu số tháng hoạt động và tổng số hoạt động
activity_summary = pd.merge(months_active, total_activity, on='contributor')

# Tính sự đều đặn trong hoạt động (số hoạt động trung bình mỗi tháng)
activity_summary['average_activity_per_month'] = activity_summary['total_activity'] / activity_summary['months_active']

# Tìm contributor có average_activity_per_month lớn nhất
most_active_contributor = activity_summary.loc[activity_summary['average_activity_per_month'].idxmax()]
most_contribute_contributor = activity_summary.loc[activity_summary['months_active'].idxmax()]

# In ra contributor có average_activity_per_month lớn nhất
print("Contributor hoạt động đều đặn nhất:")
print(most_active_contributor)
print("Contributor hoạt động đều đặn nhất:")
print(most_contribute_contributor)
# Lưu DataFrame vào file CSV nếu cần
activity_summary.to_csv('contributor_activity_summary.csv', index=False)
print("Dữ liệu tóm tắt hoạt động của các contributors đã được lưu vào CSV.")


# Đọc dữ liệu từ file CSV
commits_df = pd.read_csv('commits.csv')

# Giả sử cột 'author' chứa tên của contributors
# Tính số lượng commits của mỗi contributor
commit_counts = commits_df['author'].value_counts().reset_index()
commit_counts.columns = ['contributor', 'commit_count']

# Hiển thị kết quả
print(commit_counts)

# Lưu DataFrame vào file CSV nếu cần
commit_counts.to_csv('commit_counts.csv', index=False)
print("Dữ liệu số lượng commits của các contributors đã được lưu vào CSV.")

# Calculate the averange time of pull request

# Bước 1: Đọc dữ liệu từ file CSV
df = pd.read_csv('pull_requests.csv')

# Bước 2: Chuyển đổi cột 'created_at' và 'updated_at' sang định dạng datetime
df['created_at'] = pd.to_datetime(df['created_at'])
df['updated_at'] = pd.to_datetime(df['updated_at'])

# Bước 3: Lọc các PR đã được merged
merged_prs = df[df['state'] == 'merged']

# Bước 4: Tính thời gian từ khi tạo đến khi được merged cho mỗi PR
merged_prs['time_to_merge'] = merged_prs['updated_at'] - merged_prs['created_at']

# Bước 5: Tính trung bình thời gian để PR được merged
average_time_to_merge = merged_prs['time_to_merge'].mean()

print(f"Thời gian trung bình để một PR được merged: {average_time_to_merge}")

# Calculate the averange time of issues

# Bước 1: Đọc dữ liệu từ file CSV
df = pd.read_csv('issues.csv')

# Bước 2: Chuyển đổi cột 'created_at' và 'updated_at' sang định dạng datetime
df['created_at'] = pd.to_datetime(df['created_at'])
df['updated_at'] = pd.to_datetime(df['updated_at'])

# Bước 3: Lọc các PR đã được merged
closed_issues = df[df['state'] == 'closed']

# Bước 4: Tính thời gian từ khi tạo đến khi được merged cho mỗi PR
closed_issues['time_to_complete'] = closed_issues['updated_at'] - closed_issues['created_at']

# Bước 5: Tính trung bình thời gian để PR được merged
average_time_to_complete = closed_issues['time_to_complete'].mean()

print(f"Thời gian trung bình để một PR được merged: {average_time_to_complete}")


df = pd.read_csv('file_data.csv')
max_commits = df['commits_count'].max()
mean_size = df['file_size'].mean()
# Filter
df_filtered = df[df['commits_count'] == max_commits]
# Take file path
file_paths = df_filtered['file_path'].values
# Print file path
print("Files have most commits")
for file_path in file_paths:
    print(file_path)
# Print mean value
print(f"The mean value of size: {mean_size} byte")
