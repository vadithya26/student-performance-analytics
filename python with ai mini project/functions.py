"""Reusable functions for the Student Performance Analytics System."""

import numpy as np
import pandas as pd

# Subject columns present in students.csv
SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computer_Science"]

# Pass rule: student must score at least this in EVERY subject
PASS_MARK = 35


def load_data(file_path):
    """Read the CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)


def calculate_total_and_average(df):
    """Add Total and Average columns using NumPy on the subject marks."""
    marks = df[SUBJECTS].to_numpy()               # DataFrame -> NumPy array
    df["Total"] = np.sum(marks, axis=1)           # row-wise sum
    df["Average"] = np.round(np.mean(marks, axis=1), 2)  # row-wise mean
    return df


def get_grade(average):
    """Grading rule based on average marks."""
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    elif average >= 40:
        return "E"
    else:
        return "F"


def assign_grades(df):
    """Apply the grading rule to every student (loop over averages)."""
    grades = []
    for avg in df["Average"]:
        grades.append(get_grade(avg))
    df["Grade"] = grades
    return df


def assign_pass_fail(df):
    """Pass only if the student scored >= PASS_MARK in every subject."""
    results = []
    for _, row in df.iterrows():
        if all(row[subject] >= PASS_MARK for subject in SUBJECTS):
            results.append("Pass")
        else:
            results.append("Fail")
    df["Result"] = results
    return df


def class_statistics(df):
    """Highest, lowest and overall average performance."""
    averages = df["Average"].to_numpy()
    return {
        "highest": df.loc[df["Average"].idxmax()],
        "lowest": df.loc[df["Average"].idxmin()],
        "class_average": round(float(np.mean(averages)), 2),
        "passed": int((df["Result"] == "Pass").sum()),
        "failed": int((df["Result"] == "Fail").sum()),
    }


def subject_analysis(df):
    """Average, highest and lowest marks for each subject."""
    rows = []
    for subject in SUBJECTS:
        column = df[subject].to_numpy()
        rows.append({
            "Subject": subject,
            "Average": round(float(np.mean(column)), 2),
            "Highest": int(np.max(column)),
            "Lowest": int(np.min(column)),
            "Pass %": round(float(np.mean(column >= PASS_MARK) * 100), 1),
        })
    return pd.DataFrame(rows)


def top_performers(df, n=3):
    """Return the top n students by average marks."""
    return df.sort_values("Average", ascending=False).head(n)


def department_analysis(df):
    """Average marks and attendance for each department."""
    return df.groupby("Department")[["Average", "Attendance"]].mean().round(2)
