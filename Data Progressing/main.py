
import pandas as pd

import pandas as pd

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
