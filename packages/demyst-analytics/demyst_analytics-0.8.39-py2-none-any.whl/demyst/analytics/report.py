import pandas as pd
import numpy as np
import re
import json
from demyst.common import is_na, is_value

# These pseudo-attributes are removed from the final report
PSEUDO_ATTRS=["client_id", "error", "is_hit", "row_id"]

# For each product, maintain one product report.  It stores the number
# of matching rows and error rows, and also one attribute report for
# each attribute.
class ProductReport(object):
    def __init__(self):
        self.match_ct = 0
        self.error_ct = 0
        self.attrs = {} # name -> AttrReport

# For each attribute of a product, maintain one attribute report.
# For list attributes like provider.list[0], only one attribute report,
# named provider.list[*] is kept.
class AttrReport(object):
    def __init__(self):
        # Number of rows that have at least one value for that
        # attribute.  We keep track of this to compute the accurate
        # fill rate in the face of list attributes, which can have
        # more than one value.
        self.fill_ct = 0
        # All non-NaN values of that attribute are collected in this
        # list for computations like min/max value, variance, etc.
        self.values = []

# Input DF must contain just output columns (this is ensured by
# report(), which calls this function).
#
# The basic idea is to step through all rows, look at every column,
# and update the ProductReport and AttrReport data structures.
#
# Finally, output the report DF using the data from these structures.
def do_report(df):

    # Preprocess rows into a list of nested dictionaries for easier
    # handling.  For each row, there is one list element, called
    # product row.  It is a dictionary with a key for each product in
    # that row.  It contains the attributes for that product from that
    # row.  List attributes (attr[0], attr[1], ...)  are collapsed
    # into a single entry (attr[*]), therefore the attribute values
    # are stored as a list.
    #                     |-------------- product row -----------------|
    product_rows = [] # [ { product_name -> { attr_name -> [ value ] } } ]
    #                                       | attributes for product |
    for _, df_row in df.iterrows():
        product_row = {}
        for key, value in df_row.items():
            re_product_name = re.search('^([^\\.]*)\\.(.*)$', key)
            product_name = re_product_name.group(1)
            attr_name = re_product_name.group(2)
            # Strip out nesting from the attribute name
            attr_name = re.sub('\\[\d+\\]', '[*]', attr_name)
            if not (product_name in product_row):
                product_row[product_name] = {}
            if not (attr_name in product_row[product_name]):
                product_row[product_name][attr_name] = []
            product_row[product_name][attr_name].append(value)
        product_rows.append(product_row)

    # Process individual product rows into product reports
    product_reports = {} # product_name -> ProductReport
    # Counter of rows that match all products
    matches_all = 0
    for product_row in product_rows:
        # For calculation of matches_all:
        num_products = len(product_row)
        matches_products = 0 # How many products does this row match?
        for product_name, attrs in product_row.items():
            # Get or create product report
            if product_name in product_reports:
                product_report = product_reports[product_name]
            else:
                product_report = ProductReport()
                product_reports[product_name] = product_report
            # Product's .error is non-NaN and not False: increase error count for that product.
            # (Stupid way of writing this is needed because attr values are arrays.)
            if ("error" in attrs) and any((is_value(val) and val) for val in attrs["error"]):
                product_report.error_ct += 1
            # Row is a match for that product: increase match count
            elif is_match(attrs):
                product_report.match_ct += 1
                matches_products += 1
            # Process attributes.
            #
            # Note that we do this even if the row is an error.  The
            # reason for that is that we still need to get information
            # about all attributes for that provider.  The values and
            # fill rate for the attributes will be empty, but at least
            # we register that the attributes exist, so they will show
            # up in the final report DF.
            for attr_name, attr_values in attrs.items():
                # Ignore pseudo-attributes
                if not attr_name in PSEUDO_ATTRS:
                    # Get or create attribute report
                    if attr_name in product_report.attrs:
                        attr_report = product_report.attrs[attr_name]
                    else:
                        attr_report = AttrReport()
                        product_report.attrs[attr_name] = attr_report
                    # Process (only non-NaN) values
                    values = [v for v in attr_values if is_value(v)]
                    if len(values) > 0:
                        # Only increase fill count for attribute
                        # if there are non-NaN values in this row.
                        #
                        # Note: we don't increase the fill count by
                        # the number of values, just by 1.
                        # Otherwise we would get wrong fill rate
                        # results for list attributes with more than
                        # one value.
                        attr_report.fill_ct += 1
                        attr_report.values.extend(values)
        # If the row matched all providers, increase total count.
        if matches_products == num_products:
            matches_all += 1

    # Final step: produce report DF from product reports
    out_rows = [] # list of rows of report DF
    total_ct = len(df)
    for product_name, product_report in product_reports.items():
        for attr_name, attr_report in product_report.attrs.items():
            # Construct a single column DF holding the attribute
            # values.  The reason we don't use a series here is
            # because dataframes implement all the utility methods
            # like std and variance that we need, and series don't.
            values = pd.DataFrame(attr_report.values, columns=["col"])[["col"]]
            # Round to 2 places
            rnd = lambda x: round(x, 2)
            out_row = {
                "product_name": product_name,
                "product_match_rate": rnd(float(product_report.match_ct) / float(total_ct) * 100.0),
                "product_error_rate": rnd(float(product_report.error_ct) / float(total_ct) * 100.0),
                "attribute_name": attr_name,
                "attribute_fill_rate": rnd(float(attr_report.fill_ct) / float(total_ct) * 100.0),
                "std": do_standard_method(values, "std"),
                "median": do_standard_method(values, "median"),
                "mean": do_standard_method(values, "mean"),
                "max_value": do_standard_method(values, "max"),
                "min_value": do_standard_method(values, "min"),
                "variance": do_standard_method(values, "var"),
                "attribute_type": values["col"].dtypes,
                "unique_values": values["col"].nunique(),
                "most_common_values": values["col"].value_counts().head(5).to_dict(),
                "cardinality": cardinality(values),
                "matches_all": matches_all
                }
            out_rows.append(out_row)
    # Put columns into proper order
    return pd.DataFrame(out_rows)[['product_name', 'product_match_rate', 'product_error_rate', 'attribute_name', 'attribute_fill_rate', 'attribute_type', 'unique_values', 'most_common_values', 'cardinality', 'std', 'median', 'mean', 'max_value', 'min_value', 'variance', 'matches_all']]

# Check if a row is considered a match.
#
# It has to have either:
# - a non-False is_hit pseudo-attribute, or
# - a value* for any attribute (excluding pseudo-attributes)
#
# (* per is_value)
def is_match(attrs):
    if ("is_hit" in attrs):
        # Stupid way of writing this due to attribute values being arrays.
        return any((is_value(val) and val) for val in attrs["is_hit"])
    else:
        for attr_name, attr_values in attrs.items():
            # Ignore pseudo-columns
            if not attr_name in PSEUDO_ATTRS:
                if any(is_value(val) for val in attr_values):
                    return True
        return False

def do_standard_method(values, name):
    result = getattr(values, name)(numeric_only=True)
    if len(result) > 0:
        return result.iloc[0]
    else:
        return np.nan

def cardinality(values):
    ct = values["col"].count()
    if ct == 0:
        return 0
    else:
        return values["col"].nunique() / values["col"].count() * 100.00

def filter_columns(attributes, columns):
    re_product_name = [re.search('^([^\\.]*)\\.(.*)$', a) for a in columns]
    rows = []
    for regex in re_product_name:
        product_name = regex.group(1)
        attribute_name = regex.group(2)
        row = attributes.loc[(attributes['product_name'] == product_name) & (attributes['attribute_name'] == attribute_name)]
        rows.append(row)
    return pd.concat(rows).reset_index()

def report(enriched, columns=[]):
    # Make sure every output column contains a dot, i.e. is of the form "provider.column".
    # Ignore columns without a dot.
    # https://github.com/DemystData/demyst-python/issues/555
    output_cols = [c for c in enriched.columns if (not c.startswith("inputs.")) and ("." in c)]
    
    attributes = do_report(enriched[output_cols])

    if len(columns) > 0:
        attributes = filter_columns(attributes, columns)

    return attributes
