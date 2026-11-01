"""Student Performance Analytics System - main program."""

import pandas as pd
import functions as fn

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


def heading(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    # Step 1: Load data
    df = fn.load_data("students.csv")
    heading("1. DATASET OVERVIEW")
    print(f"Records : {df.shape[0]}")
    print(f"Columns : {list(df.columns)}")
    print("\nFirst 5 records:")
    print(df.head())
    print(f"\nMissing values: {df.isnull().sum().sum()}")

    # Step 2: Process data
    df = fn.calculate_total_and_average(df)
    df = fn.assign_grades(df)
    df = fn.assign_pass_fail(df)

    heading("2. STUDENT RESULTS (Total, Average, Grade, Result)")
    print(df[["Student_ID", "Name", "Department", "Total",
              "Average", "Grade", "Result", "Attendance"]].to_string(index=False))

    # Step 3: Class statistics
    stats = fn.class_statistics(df)
    heading("3. CLASS STATISTICS")
    print(f"Highest average : {stats['highest']['Name']} ({stats['highest']['Average']})")
    print(f"Lowest average  : {stats['lowest']['Name']} ({stats['lowest']['Average']})")
    print(f"Class average   : {stats['class_average']}")
    print(f"Students passed : {stats['passed']}")
    print(f"Students failed : {stats['failed']}")

    # Step 4: Grade distribution
    heading("4. GRADE DISTRIBUTION")
    print(df["Grade"].value_counts().sort_index().to_string())

    # Step 5: Subject-wise analysis
    subject_df = fn.subject_analysis(df)
    heading("5. SUBJECT-WISE ANALYSIS")
    print(subject_df.to_string(index=False))
    best = subject_df.loc[subject_df["Average"].idxmax()]
    weakest = subject_df.loc[subject_df["Average"].idxmin()]
    print(f"\nBest subject    : {best['Subject']} (avg {best['Average']})")
    print(f"Weakest subject : {weakest['Subject']} (avg {weakest['Average']})")

    # Step 6: Top performers
    heading("6. TOP 3 PERFORMERS")
    print(fn.top_performers(df, 3)[["Name", "Department", "Average", "Grade"]]
          .to_string(index=False))

    # Step 7: Department analysis
    heading("7. DEPARTMENT-WISE ANALYSIS")
    print(fn.department_analysis(df))

    # Step 8: Failed students and low attendance
    heading("8. STUDENTS NEEDING ATTENTION")
    failed = df[df["Result"] == "Fail"]
    print("Failed students:")
    print(failed[["Name", "Average"]].to_string(index=False))
    low_att = df[df["Attendance"] < 75]
    print("\nAttendance below 75%:")
    print(low_att[["Name", "Attendance"]].to_string(index=False))

    # Save the processed results
    df.to_csv("results.csv", index=False)
    print("\nProcessed data saved to results.csv")


if __name__ == "__main__":
    main()
