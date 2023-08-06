from demyst.analytics.report import report
from demyst.report.corr import corr_compute

import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import numpy as np
import seaborn as sns
import os
import shutil
from matplotlib import font_manager
from matplotlib import rcParams
import html
import platform
from yattag import Doc
import re

import warnings
warnings.filterwarnings("ignore", 'invalid value encountered')
warnings.filterwarnings("ignore", 'divide by zero encountered in double_scalars')

# This is a Windows workaround for a bug in wkhtmltopdf:
# https://github.com/wkhtmltopdf/wkhtmltopdf/issues/3081
# On Unix-like systems, use `ulimit -n 2048`.
def maximize_number_of_file_descriptors():
    if platform.system() == "Windows":
        import win32file
        win32file._setmaxstdio(2048)

# If DF is not supplied, no histograms are generated.
def quality_report(analytics, df=None, rep=None, show_correlations=True):
    maximize_number_of_file_descriptors()
    # Need this so it finds custom fonts
    font_manager._rebuild()
    # Set default font
    rcParams['font.family'] = 'Roboto Mono'
    rcParams['font.weight'] = 'bold'
    rcParams['text.color'] = '#DEE2EA'
    rcParams['axes.labelcolor'] = '#DEE2EA'
    rcParams['axes.edgecolor'] = '#222733'
    rcParams['xtick.color'] = '#DEE2EA'
    rcParams['ytick.color'] = '#DEE2EA'

    if not isinstance(rep, pd.DataFrame):
        rep = analytics.report(df)

    here_dir = os.path.dirname(os.path.realpath(__file__))
    try:
        os.mkdir("report")
    except Exception:
        pass

    all_stats = analytics.product_stats(provider_names_from_report(rep))
    data_stats_diagram(analytics, rep)
    distribution_diagrams(analytics, rep, all_stats)
    generate_html(analytics, df, rep, all_stats, show_correlations)
    copy_files(here_dir)
    pdf_from_html("report/index.html", "report/report.pdf")
    print("Done.")

def pdf_from_html(html_file, pdf_file):
    ret = os.system("wkhtmltopdf -L 0mm -T 0mm -R 0mm -B 0mm {} {}".format(html_file, pdf_file))
    if ret != 0:
        raise RuntimeError("wkhtmltopdf error: {}".format(ret))

def save_figure(filename):
    plt.savefig("report/" + filename + ".svg", format='svg', bbox_inches='tight', transparent=True)
    plt.close()

def extract_data_for_match_rate_plot_from_report(rep):
    return rep[["product_name", "product_match_rate", "product_error_rate"]].drop_duplicates().sort_values(by=['product_match_rate'], ascending=False).reset_index(drop=True)

def data_stats(analytics, rep):
    outputs = analytics.product_outputs(provider_names_from_report(rep))
    temp = pd.DataFrame({'attribute' : list(rep['attribute_name'])})
    temp['attribute'] = temp['attribute'].replace(r"\[(\w+)\]", '[]', regex=True)
    data_types = pd.merge(temp, outputs, on="attribute", how="left")
    numerical = len(list(data_types[data_types['type'] == 'Number']['type']))
    datetime = len(list(data_types[data_types['type'] == 'DateTime']['type']))
    bools = len(list(data_types[data_types['type'] == 'Boolean']['type']))
    st = data_types[data_types['type'] == 'String']
    categorical = len(st) - len(st[st['attribute'].str.contains('description')])
    desc = len(data_types) - numerical - datetime - bools - categorical
    return (['Numerical', 'Categorical Text', 'Descriptive Text', 'Date', 'Boolean'], [numerical, categorical, desc, datetime, bools])

def data_stats_colors():
    return ["#b39ddb", "#1de9B6", "#2e3951", "#00acc1", "#7283a7"]
    
def data_stats_diagram(analytics, rep):
    print("Creating data stats diagram")
    types, values = data_stats(analytics, rep)
    patches, texts = plt.pie(values, colors=data_stats_colors())
    return save_figure("data_stats")

def generate_html(analytics, df, rep, all_stats, show_correlations):
    doc = Doc()
    with doc.tag("html"):
        with doc.tag("head"):
            doc.stag("meta", charset="utf-8")
            doc.stag("link", rel="stylesheet", href="style.css")
        with doc.tag("body"):
            cover(doc)
            page_break(doc)
            header(doc)
            product_stats_section(analytics, df, rep, all_stats, doc)
            page_break(doc)
            header(doc)
            data_stats_section(analytics, rep, doc)
            # Only plot correlations if we have a DF and correlations flag is True.
            if isinstance(df, pd.DataFrame) and (len(df) >= 2) and show_correlations:
                page_break(doc)
                header(doc)
                correlations_section(analytics, df, rep, doc)
            page_break(doc)
            header(doc)
            attr_stats_section(analytics, rep, doc)
            page_break(doc)
            header(doc)
            details_section(analytics, df, rep, all_stats, doc)
    text_file = open("report/index.html", "w+")
    text_file.write(doc.getvalue())
    text_file.close()

# Non-breaking space Unicode character
NBSP="\u00a0"

def nbsp(string):
    return string.replace(" ", NBSP)

def cover(doc):
    with doc.tag("div", klass="cover"):
        doc.stag("img", klass="cover_logo", src="demyst_logo_gray.svg")
        with doc.tag("h1"):
            doc.line("div", "Data")
            doc.line("div", "Quality")
            doc.line("div", "Report", klass="dq")

def correlations_section(a, df, rep, doc):
    corr_matrixes = corr_compute(df, rep)
    res = pd.DataFrame({})
    for name, matrix in corr_matrixes.items():
        print("Threshold computation: " + name)
        df_highcorr = threshold_computation(df, matrix)
        # Merge df into result, ignoring any columns already in result
        res = pd.concat([res, df_highcorr.drop(list(res), axis="columns", errors="ignore")], sort=False)
    plot_correlations(res)
    doc.line("h2", "Correlations")
    doc.stag("img", src="corrplot.svg", width="100%")

def threshold_computation(df, corr_matrix):
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
    threshold = 0.95
    to_keep = [column for column in upper.columns if any(upper[column] > 0.90)]
    while True:
        if len(to_keep) < 31:
            break
        if threshold == 0.998:
            to_keep = [column for column in upper.columns[0:29]]
            break
        threshold = threshold + 0.001
        to_keep = [column for column in upper.columns if any(upper[column] > threshold)]
    df_highcorr = df[to_keep]
    return df_highcorr

def plot_correlations(df):
    corrmat = df.corr().abs()
    # Drop all-NaN rows and columns
    corrmat = corrmat.dropna(axis="columns", how="all")
    corrmat = corrmat.dropna(axis="rows", how="all")
    mask = np.zeros_like(corrmat)
    mask[np.triu_indices_from(mask)] = True
    plt.subplots(figsize=(12, 9))
    sns.heatmap(corrmat, square=True, cmap="YlGnBu", linewidths=.5, mask=mask, cbar=False)
    save_figure("corrplot")

def legend_item(doc, color):
    doc.line("span", NBSP, klass="legend_item", style="background-color: " + color)

def product_stats_section(a, df, rep, all_stats, doc):
    doc.line("h2", "Data Products")
    # Legend
    with doc.tag("div", klass="product_stats_legend"):
        legend_item(doc, "#1de9B6")
        doc.text(" Match ")
        legend_item(doc, "#29b6f6")
        doc.text(" No Match ")
        legend_item(doc, "#b39ddb")
        doc.text(" Error ")
    with doc.tag("div", klass="product_stats"):
        # Diagram
        data = extract_data_for_match_rate_plot_from_report(rep)
        for _, row in data.iterrows():
            pid = row["product_name"]
            with doc.tag("div", klass="product_stat"):
                p = a._Analytics__config.lookup_provider(pid)
                if p:
                    name = p["aegean_data_source"]["name"]
                    doc.line("h3", name, klass="product_name")
                doc.line("h3", pid, klass="product_code")
                if p:
                    tags = " \u25aa ".join([t["name"] for t in p["tags"]])
                    doc.line("div", p["description"], klass="product_desc")
                    doc.line("div", tags, klass="product_tags")
                with doc.tag("table", style="width: 100%"):
                    with doc.tag("tr"):
                        doc.line("td", nbsp("\u25B6 Results for this Job: "), klass="product_field")
                        with doc.tag("td"):
                            product_stat_bar(doc, row["product_match_rate"], row["product_error_rate"])
                    pstats = product_stats_from_all_stats(all_stats, pid)
                    if not pstats.empty:
                        with doc.tag("tr"):
                            doc.line("td", nbsp("\u25B6 Overall Results for this Product: "), klass="product_field")
                            with doc.tag("td"):
                                product_stat_bar(doc, pstats["product_match_rate"].iloc[0], pstats["product_error_rate"].iloc[0])
    doc.line("h3", "More Statistics")
    with doc.tag("table"):
        if isinstance(df, pd.DataFrame):
            with doc.tag("tr"):
                doc.line("td", "\u25B6 Number of Records: ")
                doc.line("td", str(len(df)))
        with doc.tag("tr"):
            doc.line("td", "\u25B6 Number of Products: ")
            doc.line("td", str(len(provider_names_from_report(rep))))
        with doc.tag("tr"):
            doc.line("td", "\u25B6 Records that Match All Products: ")
            doc.line("td", str(rep["matches_all"].values[0]))

def product_stats_from_all_stats(all_stats, pid):
    if all_stats.empty:
        return pd.DataFrame({})
    else:
        return all_stats.loc[all_stats["product_name"] == pid].sort_values("stats_updated_on", ascending=False)

def product_stat_bar(doc, match_rate, error_rate):
    with doc.tag("table", klass="product_stats_diagram", cellpadding="0", cellspacing="0"):
        with doc.tag("tr"):
            if match_rate >= 0.01:
                s = "%.2f%%" % match_rate
                doc.line("td", s, width=s, style="background-color: #1de9B6")
            no_match_rate = 100 - match_rate - error_rate
            if no_match_rate >= 0.01:
                s = "%.2f%%" % no_match_rate
                doc.line("td", s, width=s, style="background-color: #29b6f6")
            if error_rate >= 0.01:
                s = "%.2f%%" % error_rate
                doc.line("td", s, width=s, style="background-color: #b39ddb")

def distribution_diagrams(a, rep, all_stats):
    print("Creating distribution diagrams")
    products = provider_names_from_report(rep)
    for p in products:
        # per-job hist
        numattr = len(rep.loc[rep['product_name'] == p])
        x = rep.loc[rep['product_name'] == p]['attribute_fill_rate'].to_numpy()
        arr = plt.hist(x, 100)
        plt.gcf().set_size_inches(5, 2)
        plt.xlabel('Fill Rate (%)')
        plt.ylabel('# of Attributes', rotation='90')
        plt.tight_layout()
        save_figure(p + "_fill")
        # overall hist
        pstats = product_stats_from_all_stats(all_stats, p)
        if not pstats.empty:
            pstats['attribute_name'] = pstats['attribute_name'].str.replace(r"\[(\d+)\]", '[*]', regex=True)
            pstats = pstats.drop_duplicates(subset="attribute_name")
            numattr = len(pstats.loc[pstats['product_name'] == p])
            x = pstats.loc[pstats['product_name'] == p]['attribute_fill_rate'].to_numpy()
            arr = plt.hist(x, 100)
            plt.gcf().set_size_inches(5, 2)
            plt.xlabel('Fill Rate (%)')
            plt.ylabel('# of Attributes', rotation='90')
            plt.tight_layout()
            save_figure(p + "_fill2")

def data_stats_section(a, rep, doc):
    doc.line("h2", "Data Types")
    with doc.tag("table", klass="data_stats"):
        with doc.tag("tr"):
            with doc.tag("td"):
                doc.stag("img", klass="data_stats_diagram", src="data_stats.svg")
            with doc.tag("td", klass="data_stats_legend"):
                types, values = data_stats(a, rep)
                colors = data_stats_colors()
                for type, value, color in zip(types, values, colors):
                    with doc.tag("p"):
                        legend_item(doc, color)
                        doc.text(" " + type + ": " + str(value))

def attr_stats_section(a, rep, doc):
    doc.line("h2", "Attributes")
    most_filled_rep = filter_report(rep).head(10)
    least_filled_rep = filter_report(rep)[::-1].head(10)
    doc.line("h3", "Most Filled Attributes")
    for _, row in most_filled_rep.iterrows():
        render_attr(doc, row)
    page_break(doc)
    header(doc)
    doc.line("h2", "Attributes")
    doc.line("h3", "Least Filled Attributes")
    for _, row in least_filled_rep.iterrows():
        render_attr(doc, row)

def render_attr(doc, row):
    doc.line("h4", "\u25B6 " + row["product_name"] + "." + row["attribute_name"], klass="attr_name")
    render_attr_bar(doc, row["attribute_fill_rate"])

def render_attr_bar(doc, fill_rate):
    with doc.tag("table", klass="attr_stats_diagram", cellpadding="0", cellspacing="0"):
        with doc.tag("tr"):
            if fill_rate >= 0.01:
                s = "%.2f%%" % fill_rate
                # For fill rates less than 1, use 1% as the HTML
                # display width, otherwise the bar will not be drawn
                # properly (due to HTML not supporting widths lower than 1%).
                # https://github.com/DemystData/demyst-python/issues/733
                if fill_rate < 1:
                    html_width = "1%"
                else:
                    html_width = s
                doc.line("td", s, width=html_width, style="background-color: #1de9B6")
                if s != "100.00%":
                    doc.line("td", NBSP, style="background-color: #2e3951")
            else:
                s = "%.2f%%" % fill_rate
                doc.line("td", s, style="background-color: #2e3951; color: #dee2ea; text-align: left;")

def details_section(a, df, rep, all_stats, doc):
    for pid in provider_names_from_report(rep):
        p = a._Analytics__config.lookup_provider(pid)
        if p:
            doc.line("h2", p["aegean_data_source"]["name"])
            doc.line("h3", pid, klass="product_code")
            doc.line("h3", "Fill Rate")
            doc.line("h4", "\u25B6 Results for this Job: ")
            doc.stag("img", src=pid + "_fill.svg", style="width: 50%")
            pstats = product_stats_from_all_stats(all_stats, pid)
            if not pstats.empty:
                doc.line("h4", "\u25B6 Overall Results for this Product: ")
                doc.stag("img", src=pid + "_fill2.svg", style="width: 50%")
                pstats['attribute_name'] = pstats['attribute_name'].str.replace(r"\[(\d+)\]", '[*]', regex=True)
                pstats = pstats.drop_duplicates(subset="attribute_name")
            attrs = rep.loc[(rep['product_name'] == pid)]
            doc.line("h3", "Attributes")
            for idx, row in attrs.iterrows():
                with doc.tag("div", style="page-break-inside: avoid"):
                    doc.line("h4", row["product_name"] + "." + row["attribute_name"], klass="attr_name")
                    with doc.tag("table", style="width: 100%"):
                        with doc.tag("tr"):
                            doc.line("td", nbsp("\u25B6 Results for this Job: "), klass="attr_field")
                            with doc.tag("td", klass="attr_field_value"):
                                render_attr_bar(doc, row["attribute_fill_rate"])
                        if not pstats.empty:
                            astats = pstats.loc[(pstats['attribute_name'] == row["attribute_name"])]
                            if not astats.empty:
                                astat = astats.iloc[0]
                                with doc.tag("tr"):
                                    doc.line("td", nbsp("\u25B6 Overall Results for this Attribute: "), klass="attr_field")
                                    with doc.tag("td", klass="attr_field_value"):
                                        render_attr_bar(doc, astat["attribute_fill_rate"])
                        if isinstance(df, pd.DataFrame) and (row["attribute_type"] == np.dtype("float64")):
                            with doc.tag("tr"):
                                doc.line("td", nbsp("\u25B6 Attribute Histogram: "), klass="attr_field")
                                with doc.tag("td", klass="attr_field_value"):
                                    attr_hist_diagram(row, df, pid, idx)
                                    doc.stag("img", src=pid + "_hist_" + str(idx) + ".svg")
#                    with doc.tag("tr"):
#                        doc.line("td", nbsp("Unique Values: "), style="width: 10%")
#                        doc.line("td", row["unique_values"])
            page_break(doc)
            header(doc)

def attr_hist_diagram(row, df, pid, idx):
    # Note: uses only first element of list attr
    attr_name = row['attribute_name'].replace('[*]', '[0]')
    full_name = row['product_name'] + '.' + attr_name
    x = df[full_name].to_numpy()
    plt.gcf().set_size_inches(5, 2)
    plt.hist(x)
    plt.xlabel('Numerical Value')
    plt.ylabel('# of Rows', rotation='90')
    plt.tight_layout()
    save_figure(pid + "_hist_" + str(idx))

def provider_names_from_report(rep):
    return rep[["product_name"]].drop_duplicates()["product_name"].tolist()

def header(doc):
    with doc.tag("table", klass="header"):
        with doc.tag("tr"):
            doc.line("th", "Data Quality Report")
            with doc.tag("td"):
                doc.stag("img", klass="header_logo", src="demyst_logo_gray.svg")

def page_break(doc):
    doc.line("div", NBSP, klass="page_break")
    doc.line("div", NBSP, klass="page_break_spacer")

def copy_files(here_dir):
    shutil.copy(here_dir + "/files/style.css", "report/style.css")
    shutil.copy(here_dir + "/files/header.html", "report/header.html")
    shutil.copy(here_dir + "/files/footer.html", "report/footer.html")
    shutil.copy(here_dir + "/files/demyst_logo_gray.svg", "report/demyst_logo_gray.svg")

def filter_report(rep):
    rep = rep[~rep['attribute_name'].isin(['client_id', 'row_id', 'error', 'is_hit'])]
    col = ['product_name', 'attribute_name', 'attribute_fill_rate']
    rep = rep[col].sort_values(by='attribute_fill_rate', ascending=False, na_position='last')
    return rep

