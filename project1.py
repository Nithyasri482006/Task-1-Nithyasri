import pandas as pd
from sklearn.impute import KNNImputer

# -----------------------------
# LOAD DATASET
# -----------------------------
df = pd.read_excel("project1 dataset.xlsx")

# -----------------------------
# MISSING VALUE HANDLING
# -----------------------------

# Mean Imputation (numeric demo column)
df_mean = df.copy()
if "TotalPrice" in df_mean.columns:
    df_mean["TotalPrice"] = df_mean["TotalPrice"].fillna(df_mean["TotalPrice"].mean())

# Median Imputation
df_median = df.copy()
if "TotalPrice" in df_median.columns:
    df_median["TotalPrice"] = df_median["TotalPrice"].fillna(df_median["TotalPrice"].median())

# KNN Imputation (advanced)
df_knn = df.copy()
num_cols = df_knn.select_dtypes(include=["number"]).columns

imputer = KNNImputer(n_neighbors=3)
df_knn[num_cols] = imputer.fit_transform(df_knn[num_cols])

# -----------------------------
# FINAL WORKING DATASET (use original cleaned approach)
# -----------------------------
df = df.copy()

# Fill categorical missing values
if "CouponCode" in df.columns:
    df["CouponCode"] = df["CouponCode"].fillna("No Coupon")

# -----------------------------
# OUTLIER REMOVAL (IQR)
# -----------------------------
if "TotalPrice" in df.columns:
    Q1 = df["TotalPrice"].quantile(0.25)
    Q3 = df["TotalPrice"].quantile(0.75)
    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    df = df[
        (df["TotalPrice"] >= lower_limit) &
        (df["TotalPrice"] <= upper_limit)
    ]

# -----------------------------
# FEATURE ENGINEERING (3 FEATURES)
# -----------------------------

if "TotalPrice" in df.columns and "Quantity" in df.columns:
    df["PricePerItem"] = df["TotalPrice"] / df["Quantity"]

if "CouponCode" in df.columns:
    df["DiscountApplied"] = df["CouponCode"].apply(
        lambda x: "Yes" if x != "No Coupon" else "No"
    )

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["OrderMonth"] = df["Date"].dt.month_name()

# -----------------------------
# SAVE FINAL OUTPUT
# -----------------------------
df.to_excel("cleaned_dataset.xlsx", index=False)

print("Project 1 Completed Successfully 🚀")