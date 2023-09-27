TABLE_SCHEMA = \
    """
    Each line is a column name followed by a list of values. Example of table with columns col1_name, col2_name, col3_name:
    
        col1_name:value1_1,value2_1
        col2_name:value1_2,value2_2
        col3_name:value1_3,value2_3
    """

MATCHING_RESULT_NAME = "matching_result"
MATCHING_RESULT_PREFIX = 'MATCHING_RESULT_PREFIX'
MATCHING_RESULT_POSTFIX = 'MATCHING_RESULT_POSTFIX'
# MATCHING_RESULT_REGEX = f'{MATCHING_RESULT_PREFIX}([^{MATCHING_RESULT_POSTFIX}]){MATCHING_RESULT_POSTFIX}'
MATCHING_RESULT_REGEX = f"(?<={MATCHING_RESULT_PREFIX}\n)([\s\S]*?)(?={MATCHING_RESULT_POSTFIX})"
MATCHING_RESULT_SCHEMA = \
    """
    Each line is a columns name followed by a list of values. Template columns, then corresponding Source column.
    In other words, Each column of the template table is followed by the column of the source table that best matches it.
    If there is no match, the column name is followed by None.
    MANDATORY: Write {MATCHING_RESULT_PREFIX} once in the beginning. Will be used for output parsing. 
    MANDATORY: Template column must be followed by relevant source column, in other words you placed relevant columns closely.
    Example, if the template have `tcol` column names and `tval` values and source have `scol` column names and tval values:
    [Just for example, not real output: this is for column 1 in the template table]
    (template) tcol1: tval1, tval2,
    (source) scol1: sval1, sval2,
    
    [Just for example, not real output: this is for column 2 in the template table]
    (template) tcol2: tval1, tval2,
    (source) scol2: sval1, sval2,
    
    [Just for example, not real output: this is for column 3 in the template table, you can see that there is no match for tcol3]
    (template) tcol3: tval1, tval2,
    (source) None
    MANDATORY: Write {MATCHING_RESULT_POSTFIX} once in the end. Will be used for output parsing.
    MANDATORY: Do not include anything else between {MATCHING_RESULT_PREFIX} and {MATCHING_RESULT_POSTFIX}.
    """.format(MATCHING_RESULT_PREFIX=MATCHING_RESULT_PREFIX, MATCHING_RESULT_POSTFIX=MATCHING_RESULT_POSTFIX)

VALIDATION_RESULT_SCHEMA = \
    """
    
    """

CONCLUSION_RESULT_SCHEMA = \
    """
    You should give the output in JSON format. Example:
    [template_column_name1: [source_column_name1: str, template_column_data_type1: str, transformation_func1: str], 
    template_column_name2: [source_column_name2: str, template_column_data_type2: str, transformation_func2: str],]
    transformation_func is a python function that 
    1. have pandas df: pd.DataFrame as input,
    2. transforms column data (from source input format to template input format), 
    3. return pd.Series with transformed values column as output.
    Example of transformation_func:
    "lambda df: df[source_column_name1].astype(int)"
    "lambda df: df[source_column_name2].apply(lambda x: x.split(' ')[0])"
    
    Important: Do not confuse template_column_data_type with source_column_data_type. 
    Solution: You need to write functions that transforms source_column_data_type.
    Important: Despite data could look like datetime/categorical, in dataframe it is always string. 
    Solution: So you need to convert it to datetime/categorical first, to use certain methods of this dtypes.
    Important: All values in output should be embedded in double quotes "output_value" to be parsed properly.
    
    DO NOT CHANGE THE FORMAT OF THE OUTPUT TEMPLATE.
    DO NOT INCLUDE ANYTHING ELSE IN THE OUTPUT.
    """

matching_template = \
    """
    Your task is to match the source table to the template table. 
    Both tables are given in the following format:
    {TABLE_SCHEMA}
    
    Tables:
    Template table:
    {{template_table}}
    ----------------------------------------
    Input table:
    {{source_table}}
    
    For each column in the template table, find the column in the source table that best matches it.
    Here is some likelihood checklist how to find the best matching column, keep in mind:
    0. Compare the column names and columns values, select this column with the most similarity from perspective of column names and column values.
    1. Important: If columns have similar names, but different values, this is not the correct answer, consider other source table column,
    2. Important: If there is some column in template table that is more relevant to chosen column in source table, consider other source table column,
    3. If there are several relevant columns, just select the any and ignore others.
    4. Likelihood could come from the range of values in the column, in case of numerical values,
    5. Also Number of letters and digits in the value, similar patterns of arrangement,
    6. Also values can be similar to some common formats, like date, time, phone number, MCC, postal codes, etc.,
    7. If there is finally no relevant column in the source table founded, just write None,
    
    MANDATORY: Prove you answer by writing the thoughts, why do you think this is the right answer.
    
    For each column in the template table, write matched column in the source table in the following format:
    template_column_name1: source_column_name1,
    template_column_name2: source_column_name2,
    ...
    
    Then, write the final output in the following format:
    
    {MATCHING_RESULT_SCHEMA}
    
    IMPORTANT NOTES ABOUT OUTPUT FORMAT:
    1. This is important that template column must be followed by relevant source column, in other words you placed relevant columns closely. 
    2. Make sure that you placed Values after columns name both for template and source in each column.
    
    Prove your answer by writing the thoughts, why do you think this is the right answer.
    
    """.format(TABLE_SCHEMA=TABLE_SCHEMA, MATCHING_RESULT_SCHEMA=MATCHING_RESULT_SCHEMA,
               MATCHING_RESULT_PREFIX=MATCHING_RESULT_PREFIX)

validation_template = \
"""
    Your task is to check the matching results.
    Remember Matching results:
    
    {{matching_result}}
    
    They was generated by neural network based on the next data:
    Both tables are given in the following format:
    {TABLE_SCHEMA}
    
    Tables:
    Template table:
    {{template_table}}
    ----------------------------------------
    Input table:
    {{source_table}}
    
    ----------------------------------------
    You need to validate Matching results. Matching results should match the following format:
    {MATCHING_RESULT_SCHEMA}
    
    What do you need to do:
    1. Check whether the first column is going from the template table.
    2. IMPORTANT: Check that the template table column have prefix (template). This will be used to distinguish template columns from source columns.
    3. Check that template column name are followed by values. If not, substitute the values from corresponding column in template table.
    4. Check whether the following second column is going from the source table.
    5. IMPORTANT: Check that the source table column have prefix (source). This will be used to distinguish template columns from source columns.
    6. Check that source column names are followed by values. If not, substitute the values from source table.
    7. Check six previous conditions work for all columns in Matching results (the divided by double line break symbol).
    
    IMPORTANT: Generate Matching results output again, embed it with {MATCHING_RESULT_PREFIX} before
    and {MATCHING_RESULT_POSTFIX} after.    
""".format(TABLE_SCHEMA=TABLE_SCHEMA, MATCHING_RESULT_SCHEMA=MATCHING_RESULT_SCHEMA,
           MATCHING_RESULT_PREFIX=MATCHING_RESULT_PREFIX, MATCHING_RESULT_POSTFIX=MATCHING_RESULT_POSTFIX)

conclusion_template = \
    """
    Your task is to write code that transforms source table to the template table format.
    
    Matching results:
    {{matching_result}}
    
    For each column in the template table, find the code that transforms 
    the relevant column in the source table into the template table column.
    
    {CONCLUSION_RESULT_SCHEMA}
    """.format(MATCHING_RESULT_SCHEMA=MATCHING_RESULT_SCHEMA, CONCLUSION_RESULT_SCHEMA=CONCLUSION_RESULT_SCHEMA)
