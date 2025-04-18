import pandas as pd

def read_and_find_toppers(csv_file):
    """
    Reads the CSV and returns subject-wise topper(s) and overall topper(s)
    with at least 60% attendance and project submitted.
    Returns: dict {subject: [names]}, 'Overall': [names]
    """
    df = pd.read_csv(csv_file)
    eligible = df[(df['Attendance (%)'] >= 60) & (df['Project Submitted'] == True)]
    toppers = {}
    subjects = ['Math', 'Science', 'English']
    for subj in subjects:
        max_score = eligible[subj].max()
        toppers[subj] = eligible[eligible[subj] == max_score]['Name'].tolist()

    # Overall topper: highest average among eligible
    eligible['Avg'] = eligible[subjects].mean(axis=1)
    max_avg = eligible['Avg'].max()
    toppers['Overall'] = eligible[eligible['Avg'] == max_avg]['Name'].tolist()
    return toppers

def add_summary_columns_and_save(csv_file, output_file='Summary_Extended.csv'):
    """
    Adds 'Average Score', 'Grade', 'Performance' columns and saves to output_file.
    Returns: DataFrame with new columns.
    """
    df = pd.read_csv(csv_file)
    subjects = ['Math', 'Science', 'English']
    df['Average Score'] = df[subjects].mean(axis=1)
    # Grade assignment
    def grade(avg):
        if avg >= 90:
            return 'A'
        elif avg >= 75:
            return 'B'
        elif avg >= 60:
            return 'C'
        else:
            return 'D'
    df['Grade'] = df['Average Score'].apply(grade)
    
    # Performance assignment
    def performance(row):
        if row['Grade'] == 'A' and row['Attendance (%)'] > 90 and row['Project Submitted']:
            return 'Excellent'
        elif row['Grade'] == 'D' or not row['Project Submitted'] or row['Attendance (%)'] < 60:
            return 'Needs Attention'
        else:
            return 'Satisfactory'
    df['Performance'] = df.apply(performance, axis=1)
    df.to_csv(output_file, index=False)
    return df

def export_summary_stats(csv_file, output_file='Summary_Stats.csv'):
    """
    Exports summary stats (describe) for subject marks and attendance.
    """
    df = pd.read_csv(csv_file)
    stats = df[['Math', 'Science', 'English', 'Attendance (%)']].describe()
    stats.to_csv(output_file)
    return stats
