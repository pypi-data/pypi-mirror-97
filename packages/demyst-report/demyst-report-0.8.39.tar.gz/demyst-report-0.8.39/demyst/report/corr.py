import re
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
from demyst.analytics.report import PSEUDO_ATTRS
from scipy import stats
from functools import partial
import itertools

#
# DATAFRAME PREPARATION
#

def corr_prepare(df, rep):
    print("Preparing data for correlations")
    df = drop_pseudo_columns(df)
    df = drop_low_fill_rate_columns(df, rep)
    df = drop_columns_not_in_report(df, rep)
    df = convert_object_columns_to_numeric(df)
    df = replace_space_and_null_with_nan(df)
    df = replace_nan_with_empty_string(df)
    return df

LOW_FILL_RATE=30.0

# Drop columns that have all nan or less than LOW_FILL_RATE% fill rate
def drop_low_fill_rate_columns(df, rep):
    columns_to_drop = []
    for _, row in rep.iterrows():
        if row["attribute_fill_rate"] < LOW_FILL_RATE:
            columns = find_matching_columns(df, row["product_name"] + "." + row["attribute_name"])
            columns_to_drop.extend(columns)
    return df.drop(columns=columns_to_drop)

# Report attributes may contain [*], this function finds actual
# instances [0], [1] etc in the DF.
def find_matching_columns(df, rep_col_name):
    results = []
    for col_name in list(df):
        if rep_col_name == re.sub("\\[\d+\\]", "[*]", col_name):
            results.append(col_name)
    return results

REPORT_PSEUDO_ATTRS=["transaction"]
REPORT_PSEUDO_ATTRS.extend(PSEUDO_ATTRS) # Reuse list of pseudo attrs from demyst-analytics

# Drop columns that contain client_id, row_id, is_hit, error, transaction
def drop_pseudo_columns(df):
    columns_to_drop = []
    for col in list(df):
        for p in REPORT_PSEUDO_ATTRS:
            if re.search(p, col):
                columns_to_drop.append(col)
    return df.drop(columns=columns_to_drop)

# Drop columns that are not in the report DF (for quality_report(df=..., rep=...))
def drop_columns_not_in_report(df, rep):
    rep_columns = [] # all columns in report
    for _, row in rep.iterrows():
        rep_columns.append(row["product_name"] + "." + row["attribute_name"])
    columns_to_drop = []
    for col in list(df):
        if not re.sub("\\[\d+\\]", "[*]", col) in rep_columns:
            columns_to_drop.append(col)
    return df.drop(columns=columns_to_drop)

def replace_space_and_null_with_nan(df):
    def repl(val):
        if (isinstance(val, str) and ((val.lower() == "null") or (val.strip() == ""))):
            return np.nan
        else:
            return val
    return df.applymap(repl)

def replace_nan_with_empty_string(df):
    def repl(val):
        if pd.isna(val):
            return ""
        else:
            return val
    return df.applymap(repl)

CONVERT_OBJECT_THRESHOLD=75.0

# Loop through every value in a column of type object, and try to
# parse the value as a number. If this works for more than
# CONVERT_OBJECT_THRESHOLD% of the values, then convert the whole
# column to numeric type (turning other values into NaN), otherwise
# keep object type for column.
def convert_object_columns_to_numeric(df):
    for col_name, col_type in df.dtypes.items():
        if col_type == np.object:
            # Coerce means turn parse errors into NaN
            numeric_col = pd.to_numeric(df[col_name], errors="coerce")
            numeric_pct = numeric_col.count() / len(numeric_col) * 100.0
            if numeric_pct >= CONVERT_OBJECT_THRESHOLD:
                df[col_name] = numeric_col
    return df

#
# SPLIT INTO NUMERICAL / OTHER COLUMNS
#

# Split DF into numerical and other columns, transforming categorical
# columns into numerical ones, and ignoring a bunch of other columns.
def corr_split(df, rep):
    numeric_df = pd.DataFrame({})
    other_df = pd.DataFrame({})
    for col_name, col_type in df.dtypes.items():
        if is_numeric_dtype(col_type):
            numeric_df[col_name] = df[col_name]
        elif is_cat_column(col_name, get_cardinality(rep, col_name)):
            numeric_df[col_name] = cat_column_to_numeric(df[col_name])
        elif not should_ignore_column(col_name):
            other_df[col_name] = df[col_name]
    return numeric_df, other_df

# If it contains this -> categorical
CAT_COLUMNS=["state",
             "country",
             "code"]
# But if it contains this -> not categorical
NOT_CAT_COLUMNS=["description",
                 "desc",
                 "first_name",
                 "last_name",
                 "full_name",
                 "business_name",
                 "middle_name",
                 "full_name"]
# If it contains this -> column is ignored
IGNORE_COLUMNS=["first_name",
                "last_name",
                "full_name",
                "business_name",
                "middle_name",
                "full_name",
                "ssn",
                "email",
                "phone",
                "website",
                "street"]

CARDINALITY_THRESHOLD=40.0

def is_cat_column(col_name, card):
    if card <= CARDINALITY_THRESHOLD:
        return True
    for s in NOT_CAT_COLUMNS:
        if re.search(s, col_name):
            return False
    for s in CAT_COLUMNS:
        if re.search(s, col_name):
            return True
    return False

def cat_column_to_numeric(col):
    labels = col.astype("category").cat.categories.tolist()
    replace_map = { k: v for k,v in zip(labels, list(range(1, len(labels) + 1))) }
    return col.replace(replace_map)

def should_ignore_column(col_name):
    for s in IGNORE_COLUMNS:
        if re.search(s, col_name):
            return True
    return False

def get_cardinality(report_df, col_name):
    product_name, attr_name = col_name.split(".", 1)
    attr_name = re.sub("\\[\d+\\]", "[*]", attr_name)
    return get_report_attr_field(report_df, product_name, attr_name, "cardinality")

def get_report_attr_field(report_df, product_name, attr_name, field_name):
    return report_df.loc[(report_df["product_name"] == product_name) & (report_df["attribute_name"] == attr_name), field_name].values[0]

#
# CORRELATION COMPUTATION
#

def corr_compute(df, rep):
    if (len(list(df)) < 2):
        raise RuntimeError("Not enough columns for generating correlation.")
    df = corr_prepare(df, rep)
    numeric_df, other_df = corr_split(df, rep)
    correlations = {}
    corr_numerical(numeric_df, correlations)
    corr_other(other_df, correlations)
    return correlations

def corr_numerical(df, correlations):
    for correlation_name in ["pearson", "spearman"]:
        try:
            print("Computing correlation: " + correlation_name)
            correlation = df.corr(method=correlation_name)
            if len(correlation) > 0:
                correlations[correlation_name] = correlation
        except (ValueError, AssertionError) as e:
            print(str(e), file=sys.stderr)

def corr_other(df, correlations):
    variables = {}
    for item in list(df.columns):
        variables[item] = df[item].dtype
    categorical_correlations = {"cramers": cramers_matrix}
    for correlation_name, get_matrix in categorical_correlations.items():
        try:
            print("Computing correlation: " + correlation_name)
            correlation = get_matrix(df, variables)
            if len(correlation) > 0:
                correlations[correlation_name] = correlation
        except (ValueError, ZeroDivisionError) as e:
            pass

def categorical_matrix(df, variables, correlation_function):
    categoricals = {
        column_name: df[column_name]
        for column_name, variable_type in variables.items()
        if variable_type == np.dtype('O')
        # TODO: add filter for unique number of records in column
    }

    correlation_matrix = pd.DataFrame(
        np.ones((len(categoricals), len(categoricals))),
        index=categoricals.keys(),
        columns=categoricals.keys(),
        )

    for (name1, data1), (name2, data2) in itertools.combinations(categoricals.items(), 2):
        confusion_matrix = pd.crosstab(data1, data2, dropna=False)
        correlation_matrix.loc[name2, name1] = correlation_matrix.loc[
            name1, name2
            ] = correlation_function(confusion_matrix)
    return correlation_matrix

def cramers_matrix(df, variables):
    return categorical_matrix(df, variables, partial(cramers_corrected_stat, correction=True))

def cramers_corrected_stat(confusion_matrix, correction):
    chi2 = stats.chi2_contingency(confusion_matrix, correction=correction)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0.0, phi2 - ((k - 1.0) * (r - 1.0)) / (n - 1.0))
    rcorr = r - ((r - 1.0) ** 2.0) / (n - 1.0)
    kcorr = k - ((k - 1.0) ** 2.0) / (n - 1.0)
    return np.sqrt(phi2corr / min((kcorr - 1.0), (rcorr - 1.0)))
