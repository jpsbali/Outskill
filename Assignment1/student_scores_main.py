from student_scores_analysis import read_and_find_toppers, add_summary_columns_and_save, export_summary_stats

CSV_FILE = 'student_scores.csv'

if __name__ == '__main__':
    # 1. Find subject-wise and overall toppers
    toppers = read_and_find_toppers(CSV_FILE)
    print('Toppers (with >=60% attendance and project submitted):')
    for key, names in toppers.items():
        print(f'{key} Topper(s): {", ".join(names)}')

    # 2. Add summary columns and save extended summary
    df_extended = add_summary_columns_and_save(CSV_FILE)
    print('\nSummary_Extended.csv created with additional columns.')
    print(df_extended.head())

    # 3. Export summary statistics
    stats = export_summary_stats(CSV_FILE)
    print('\nSummary_Stats.csv created with subject and attendance statistics:')
    print(stats)
