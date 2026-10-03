import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. LOAD DATA
# ==========================================

assessments = pd.read_csv("data/raw/assessments.csv")
courses = pd.read_csv("data/raw/courses.csv")

print("========== DATA LOADING ==========")
print("Raw assessment rows:", len(assessments))
print("Course rows:", len(courses))

# Confirm numeric types
assessments["assessment_id"] = pd.to_numeric(
    assessments["assessment_id"]
)

assessments["score"] = pd.to_numeric(
    assessments["score"]
)

assessments["attendance_pct"] = pd.to_numeric(
    assessments["attendance_pct"]
)

print("\nData types:")
print(assessments.dtypes)


# ==========================================
# 2. REMOVE EXACT DUPLICATE
# ==========================================

assessments = assessments.drop_duplicates()

print("\n========== CLEANING ==========")
print("Rows after removing duplicate:", len(assessments))


# ==========================================
# 3. MERGE WITH COURSES
# ==========================================

df = assessments.merge(
    courses,
    on="course_id",
    how="left"
)

# Required validation
assert len(df) == 12
assert df["department"].isna().sum() == 0

print("\n========== MERGE VALIDATION ==========")
print("Merged rows:", len(df))
print(
    "Unmatched course IDs:",
    df["department"].isna().sum()
)

print("\nMerge successful!")


# ==========================================
# 4. CREATE PASS FLAG
# ==========================================

df["pass_flag"] = (
    df["score"] >= 50
).astype(int)

print("\n========== PASS FLAG ==========")
print(df[
    ["assessment_id", "score", "pass_flag"]
])


# ==========================================
# 5. DEPARTMENT SUMMARY
# ==========================================

department_summary = (
    df.groupby("department")
    .agg(
        total_assessments=("assessment_id", "count"),
        passing_count=("pass_flag", "sum")
    )
    .reset_index()
)

department_summary["pass_rate"] = (
    department_summary["passing_count"]
    / department_summary["total_assessments"]
    * 100
)

department_summary["pass_rate"] = (
    department_summary["pass_rate"].round(2)
)

print("\n========== DEPARTMENT SUMMARY ==========")
print(department_summary)


# ==========================================
# 6. COURSE PASS RATE
# ==========================================

course_summary = (
    df.groupby(["course_id", "course"])
    .agg(
        passing_count=("pass_flag", "sum"),
        total_assessments=("assessment_id", "count")
    )
    .reset_index()
)

course_summary["pass_rate"] = (
    course_summary["passing_count"]
    / course_summary["total_assessments"]
    * 100
)

course_summary["pass_rate"] = (
    course_summary["pass_rate"].round(2)
)

print("\n========== COURSE PASS RATE ==========")
print(course_summary)


# ==========================================
# 7. LOWEST PASS RATE COURSE
# ==========================================

lowest_rate = course_summary["pass_rate"].min()

lowest_courses = course_summary[
    course_summary["pass_rate"] == lowest_rate
]

print("\n========== LOWEST PASS RATE ==========")
print(lowest_courses)

print(
    "\nLowest pass rate:",
    lowest_rate,
    "%"
)

print(
    "Passing count:",
    lowest_courses["passing_count"].tolist()
)

print(
    "Total assessments:",
    lowest_courses["total_assessments"].tolist()
)


# ==========================================
# 8. MONTHLY AVERAGE SCORE
# ==========================================

month_order = ["Jan", "Feb", "Mar"]

monthly_avg = (
    df.groupby("month")["score"]
    .mean()
    .reindex(month_order)
    .round(2)
)

print("\n========== MONTHLY AVERAGE ==========")
print(monthly_avg)


# ==========================================
# 9. CREATE OUTPUT FOLDER
# ==========================================

os.makedirs("outputs", exist_ok=True)


# ==========================================
# 10. MONTHLY CHART
# ==========================================

plt.figure(figsize=(8, 5))

monthly_avg.plot(kind="bar")

plt.title("Monthly Average Score")
plt.xlabel("Month")
plt.ylabel("Average Score")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "outputs/python_chart.png"
)

plt.close()


# ==========================================
# 11. EXPORT CLEAN DATA
# ==========================================

df.to_csv(
    "outputs/clean_data.csv",
    index=False
)


# ==========================================
# 12. EXPORT DEPARTMENT SUMMARY
# ==========================================

department_summary.to_csv(
    "outputs/python_summary.csv",
    index=False
)


# ==========================================
# 13. FINAL MESSAGE
# ==========================================

print("\n======================================")
print("PYTHON ANALYSIS COMPLETED SUCCESSFULLY")
print("======================================")

print("\nCreated files:")

print("outputs/clean_data.csv")
print("outputs/python_summary.csv")
print("outputs/python_chart.png")