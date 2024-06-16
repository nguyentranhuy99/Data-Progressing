
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# NOTE: YOU NEED TO COMMAND OTHER PARTS IF YOU WANT TO RUN A PART

# MONTHLY COMMITS

# Read the CSV file
df = pd.read_csv('commits.csv')

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])
# Extract the month and year from the 'date' column
df['YearMonth'] = df['date'].dt.to_period('M')
# Group by 'YearMonth' and count the number of commits per month
monthly_commits = df.groupby('YearMonth').size()

# Step 5: Plot the line chart
plt.figure(figsize=(10, 6))
plt.plot(monthly_commits.index.astype(str), monthly_commits.values, marker='o')


# Add titles and labels
plt.title('Number of Commits over time')
plt.xlabel('Month')
plt.ylabel('Number of Commits')

# Optional: Improve the x-axis labels
plt.xticks(rotation=45)
plt.grid(True)

# Show the plot
print(df)
plt.tight_layout()
plt.show()

# 2023

# Đọc dữ liệu từ file CSV
df = pd.read_csv('commits.csv')

# Chuyển đổi cột 'date' sang kiểu datetime
df['date'] = pd.to_datetime(df['date'])

# Lọc dữ liệu để chỉ lấy các commit trong năm 2023
df_2023 = df[df['date'].dt.year == 2023]

# Tạo cột 'month' để nhóm theo tháng
df_2023['month'] = df_2023['date'].dt.to_period('M')

# Đếm số commit theo từng tháng
commits_per_month = df_2023.groupby('month').size()

# Tạo DataFrame với tất cả các tháng trong năm 2023
all_months = pd.period_range(start='2023-01', end='2023-12', freq='M')
all_months_df = pd.DataFrame(all_months, columns=['month'])
all_months_df.set_index('month', inplace=True)

# Kết hợp dữ liệu commits với DataFrame chứa tất cả các tháng
commits_per_month = all_months_df.join(commits_per_month.to_frame(name='commits')).fillna(0)

# Chuyển đổi index sang kiểu datetime để vẽ biểu đồ
commits_per_month.index = commits_per_month.index.to_timestamp()

# Vẽ biểu đồ đường
plt.figure(figsize=(10, 6))
plt.plot(commits_per_month.index, commits_per_month['commits'], marker='o', linestyle='-')
plt.title('Number of Commits per Month in 2023')
plt.xlabel('Month')
plt.ylabel('Number of Commits')
plt.grid(True)
plt.xticks(ticks=commits_per_month.index, labels=commits_per_month.index.strftime('%B'), rotation=45)
plt.tight_layout()
plt.show()

# LABELS

# Đọc dữ liệu từ file CSV
df = pd.read_csv('issues.csv')

# Thay thế các giá trị rỗng bằng giá trị NaN (nếu cần)
df['labels'].replace('', pd.NA, inplace=True)

# Tách các nhãn thành các nhãn riêng lẻ
df['labels'] = df['labels'].str.split(', ')

# Chuyển đổi DataFrame từ dạng rộng sang dạng dài
labels_exploded = df.explode('labels')

# Đếm số lần xuất hiện của từng nhãn
label_counts = labels_exploded['labels'].value_counts()

# Vẽ biểu đồ cột cho tất cả các nhãn
plt.figure(figsize=(12, 8))
label_counts.plot(kind='bar', color='skyblue')
plt.title('Number of Issues and Pull Requests by Labels')
plt.xlabel('Labels')
plt.ylabel('Number of Issues and Pull Requests')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# In số lượng của từng nhãn
print("\nLabel Counts:")
print(label_counts)

# Pull request

# Đọc dữ liệu từ file CSV
df = pd.read_csv('pull_requests.csv')

# Đếm số lần xuất hiện của từng trạng thái
status_counts = df['state'].value_counts()

# Tạo biểu đồ pie chart
plt.figure(figsize=(8, 8))
plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Pull Request States')
plt.show()

# Contributor

# Đọc dữ liệu từ file CSV
df = pd.read_csv('commits.csv')

# Kiểm tra đầu vào và loại bỏ các dòng có giá trị thiếu
df.dropna(subset=['author', 'date'], inplace=True)

# Chuyển đổi cột 'date' sang định dạng datetime
df['date'] = pd.to_datetime(df['date'])

# Tạo cột 'month_year' để nhóm theo tháng
df['month_year'] = df['date'].dt.to_period('M')

# Đếm số lượng contributor duy nhất theo từng tháng
contributors_per_month = df.groupby('month_year')['author'].nunique()

# Vẽ biểu đồ đường
plt.figure(figsize=(12, 6))
plt.plot(contributors_per_month.index.astype(str), contributors_per_month.values, marker='o', linestyle='-')
plt.title('Number of Contributors over time')
plt.xlabel('Month')
plt.ylabel('Number of Contributors')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Growth

#Đọc dữ liệu từ file CSV
df = pd.read_csv('commits.csv')

# Kiểm tra đầu vào và loại bỏ các dòng có giá trị thiếu
df.dropna(subset=['author', 'date'], inplace=True)

# Chuyển đổi cột 'date' sang định dạng datetime
df['date'] = pd.to_datetime(df['date'])

# Tạo cột 'month_year' để nhóm theo tháng
df['month_year'] = df['date'].dt.to_period('M')

# Đếm số lượng contributor duy nhất theo từng tháng
contributors_per_month = df.groupby('month_year')['author'].nunique()
monthly_commits = df.groupby('month_year').size()

# Vẽ biểu đồ đường
plt.figure(figsize=(12, 6))
plt.plot(contributors_per_month.index.astype(str), contributors_per_month.values, marker='o', linestyle='-', label='Number of Commits')
plt.plot(monthly_commits.index.astype(str), monthly_commits.values, marker='o', linestyle='-', label='Number of Contributors')
plt.legend(loc='best')
plt.title('Repository Growth')
plt.xlabel('Month')
plt.ylabel('Number of commits/contributors')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Backend vs Frontend

# Đọc dữ liệu từ file CSV
df = pd.read_csv('issues.csv')

# Kiểm tra đầu vào và loại bỏ các dòng có giá trị thiếu
df.dropna(subset=['labels', 'updated_at'], inplace=True)

# Chuyển đổi cột 'date' sang định dạng datetime
df['updated_at'] = pd.to_datetime(df['updated_at'])

# Tạo cột 'month_year' để nhóm theo tháng
df['month_year'] = df['updated_at'].dt.to_period('M')

# Lọc các hàng có chứa nhãn 'frontend'
df_frontend = df[df['labels'].str.contains('frontend', na=False)]
df_backend = df[df['labels'].str.contains('backend', na=False)]

# Đếm số lượng theo từng tháng
frontend_per_month = df_frontend.groupby('month_year').size()
backend_per_month = df_backend.groupby('month_year').size()

# Tạo một chuỗi thời gian với tất cả các tháng trong khoảng thời gian từ tháng đầu tiên đến tháng cuối cùng
all_months = pd.period_range(start=df['updated_at'].min(), end=df['updated_at'].max(), freq='M')

# Chuyển đổi index sang kiểu datetime để vẽ biểu đồ
frontend_per_month.index = frontend_per_month.index.to_timestamp()
backend_per_month.index = backend_per_month.index.to_timestamp()

# Chuyển đổi all_months sang kiểu timestamp để phù hợp với index của frontend_per_month
all_months = all_months.to_timestamp()

# Vẽ biểu đồ đường
plt.figure(figsize=(10, 6))
plt.plot(frontend_per_month.index, frontend_per_month.values, marker='o', linestyle='-', label="frontend")
plt.plot(backend_per_month.index, backend_per_month.values, marker='o', linestyle='-', label="backend")
plt.title('Number of Issues and Pull Requests with Labels Backend vs Fronted over Months')
plt.xlabel('Month')
plt.ylabel('Number of Issues and Pull Requests')
plt.grid(True)

plt.legend(loc='best')

# Định dạng trục x để hiển thị chỉ tháng và năm
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))

plt.xticks(frontend_per_month.index, rotation=45)
plt.tight_layout()
plt.show()

# Addtions vs Deletions

# Đọc dữ liệu từ file CSV
df = pd.read_csv('pull_requests.csv')

# Chuyển đổi cột 'date' sang định dạng datetime
df['updated_at'] = pd.to_datetime(df['updated_at'])

# Tạo cột 'month_year' để nhóm theo tháng
df['month_year'] = df['updated_at'].dt.to_period('M')

# Đếm số lượng theo từng tháng
additions_per_month = df.groupby('month_year')['additions'].sum()
deletions_per_month = df.groupby('month_year')['deletions'].sum()

all_months = pd.period_range(start=df['updated_at'].min(), end=df['updated_at'].max(), freq='M')

# Chuyển đổi index sang kiểu datetime để vẽ biểu đồ
additions_per_month.index = additions_per_month.index.to_timestamp()
deletions_per_month.index = deletions_per_month.index.to_timestamp()

# Chuyển đổi all_months sang kiểu timestamp để phù hợp với index của frontend_per_month
all_months = all_months.to_timestamp()

# Vẽ biểu đồ đường
plt.figure(figsize=(10, 6))
plt.plot(additions_per_month.index, additions_per_month.values, marker='o', linestyle='-', label="additons")
plt.plot(deletions_per_month.index, deletions_per_month.values, marker='o', linestyle='-', label="deletions")
plt.title('Number of additions vs deletions over Months')
plt.xlabel('Month')
plt.ylabel('Lines of code')
plt.grid(True)

plt.legend(loc='best')

# Định dạng trục x để hiển thị chỉ tháng và năm
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))

plt.xticks(additions_per_month.index, rotation=45)
plt.tight_layout()
plt.show()


# LANGUAGES

# Read the CSV file
df = pd.read_csv('languages.csv')

# Sum of lines of code
total_lines_of_code = df['Lines of Code'].sum()
# Calculate threshold
threshold = 0.005 * total_lines_of_code
# Indentify small languages
small_languages = df[df['Lines of Code'] < threshold]['Language']
# replace 'Language' by 'Other'
df.loc[df['Language'].isin(small_languages), 'Language'] = 'Other'
# Group
df = df.groupby('Language', as_index=False)['Lines of Code'].sum()
# Sort
df = df.sort_values(by='Lines of Code', ascending=False)

# Extract data for the pie chart
labels = df['Language']
sizes = df['Lines of Code']

# Plot the pie chart
plt.figure(figsize=(5, 5))  # Optional: to make the figure a bit larger
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)

# Add a title
plt.title('Pie Chart of programming languages')

# Show the plot
plt.show()

# Passes test percentage

# Bước 1: Đọc dữ liệu từ file CSV
df = pd.read_csv('pull_requests.csv')  # Thay 'your_file.csv' bằng tên file CSV của bạn

# Bước 2: Loại bỏ các hàng có total_test bằng 0
df = df[df['total_tests'] != 0]

# Bước 3: Tính toán phần trăm các bài kiểm tra đã qua
df['percent_passed'] = (df['passed_tests'] / df['total_tests']) * 100

# Bước 4: Tạo các khoảng xác suất (bins) cách nhau 10%
bins = [i for i in range(0, 101, 10)]  # Tạo các khoảng từ 0 đến 100 với bước nhảy là 10
labels = [f'{bins[i]}-{bins[i+1]}' for i in range(len(bins)-1)]

# Bước 5: Đếm số lượng test trong mỗi khoảng xác suất
df['binned'] = pd.cut(df['percent_passed'], bins=bins, labels=labels, include_lowest=True)
count_per_bin = df['binned'].value_counts().sort_index()

# Bước 6: Vẽ biểu đồ cột
plt.figure(figsize=(12, 6))
count_per_bin.plot(kind='bar', color='blue', edgecolor='black')
plt.xlabel('Probability Range (%)')
plt.ylabel('Number of Pull Requests')
plt.title('Number of Tests per Probability Range')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Hiển thị biểu đồ
plt.tight_layout()
plt.show()

# Contributors network

# Bước 1: Đọc dữ liệu từ file CSV
# Giả sử file CSV có các cột: pr_id, author, reviewers
df = pd.read_csv('pull_requests.csv')

# Bước 2: Xây dựng mạng lưới cộng tác
G = nx.Graph()

# Thêm các nút và cạnh vào đồ thị
for index, row in df.iterrows():
    author = row['author']
    reviewers = row['reviewers']

    # Kiểm tra nếu cột reviewers không trống
    if pd.notna(reviewers):
        reviewers_list = reviewers.split(',')  # Giả sử reviewers được lưu dưới dạng chuỗi phân tách bằng dấu phẩy

        # Thêm tác giả vào mạng lưới nếu chưa có
        if author not in G:
            G.add_node(author)

        # Thêm reviewers vào mạng lưới và tạo các cạnh giữa author và reviewers
        for reviewer in reviewers_list:
            reviewer = reviewer.strip()  # Loại bỏ khoảng trắng thừa
            if reviewer:
                if reviewer not in G:
                    G.add_node(reviewer)
                G.add_edge(author, reviewer)

# Bước 3: Vẽ biểu đồ mạng lưới
plt.figure(figsize=(30, 30))
pos = nx.spring_layout(G, k=0.5)

# Vẽ các nút và cạnh
nx.draw_networkx_nodes(G, pos, node_size=400, node_color='skyblue', alpha=0.7)
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.7)
nx.draw_networkx_labels(G, pos, font_size=7, font_family='sans-serif')

plt.title('Collaboration Network of Contributors')
plt.show()

