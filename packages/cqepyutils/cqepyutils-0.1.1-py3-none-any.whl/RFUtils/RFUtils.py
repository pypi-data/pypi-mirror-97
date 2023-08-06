from robot.api import ExecutionResult, ResultVisitor
import robot
import csv
import pandas as pd
from datetime import datetime


def email_trigger(xml_file, csv_file, html_file):

    class TestMetrics(ResultVisitor):

        def visit_test(self, test):
            # wr.writerow([test.name, test.doc, test.status, test.message, test.elapsedtime / float(1000)])
            wr.writerow([test.name, test.doc, test.status, test.message, test.elapsedtime / float(1000)])

    class SuiteMetrics(ResultVisitor):

        def visit_suite(self, suite):

            if robot.__version__ == '4.0rc1':
                stats = result.suite.statistics
                wr1.writerow(
                    [suite.name, suite.status, stats.passed + stats.failed, stats.passed, stats.failed,
                     round((suite.elapsedtime / float(60000)), 2)])
            # round((suite.elapsedtime / float(60000)), 2)
            else:
                stats = result.suite.statistics.all
                wr1.writerow(
                    [suite.name, suite.status, stats.total, stats.passed, stats.failed,
                     suite.elapsedtime / float(60000)])

    op_f = open(csv_file, 'w')
    wr = csv.writer(op_f)

    wr.writerow(['TESTCASE_NAME', 'DOCUMENTATION', 'TESTCASE_STATUS', 'FAILURE_ANALYSIS', 'TESTCASE_ELAPSEDTIME'])
    result = ExecutionResult(xml_file)
    result.visit(TestMetrics())
    op_f.close()

    suite_csv = csv_file.replace('.csv', '_suite.csv')
    op_f1 = open(suite_csv, 'w')
    wr1 = csv.writer(op_f1)
    wr1.writerow(['SUITE_NAME', 'SUITE_STATUS', 'TOTAL_TESTCASES', 'TESTCASES_PASSED', 'TESTCASES_FAILED',
                  'EXECUTION_TIME'])

    result.visit(SuiteMetrics())
    op_f1.close()
    csv_to_html(csv_file, suite_csv, html_file, 'TESTCASE_STATUS')


def csv_to_html(csv_file, suite_csv, html_file, highlight_column_name):
    df = pd.read_csv(csv_file, index_col=False)
    df = df[~df.TESTCASE_NAME.str.contains("Placeholder Test")]
    df.fillna('', inplace=True)
    print(df)
    df2 = pd.DataFrame([])
    df1 = pd.read_csv(suite_csv, index_col=False)
    tmp_df = pd.read_csv(csv_file, index_col=False)
    tmp_df = tmp_df[tmp_df.TESTCASE_NAME.str.contains("Placeholder Test")]

    if len(tmp_df) > 0:
        suite_name = df1['SUITE_NAME']
        suite_status = df1['SUITE_STATUS']
        total_tc = df1['TOTAL_TESTCASES'] - 1
        total_tc_passed = df1['TESTCASES_PASSED'] - 1
        total_tc_failed = df1['TESTCASES_FAILED']
        execution_time = df1['EXECUTION_TIME']

        df2['SUITE_NAME'] = suite_name
        df2['SUITE_STATUS'] = suite_status
        df2['TOTAL_TESTCASES'] = total_tc
        df2['TESTCASES_PASSED'] = total_tc_passed
        df2['TESTCASES_FAILED'] = total_tc_failed
        df2['EXECUTION_TIME'] = execution_time
        df1 = df2
    print(df1)
    print(df2)

    html = df.style.applymap(highlight_vals, subset=[highlight_column_name]).\
        applymap(center_vals, subset=['TESTCASE_STATUS']).\
        applymap(center_vals, subset=['TESTCASE_ELAPSEDTIME']).\
        applymap(left_vals, subset=['DOCUMENTATION']).set_table_styles(
        [{'selector': 'tr.hover td', 'props': [('background-color', 'lightyellow')]},
         {'selector': 'th, td', 'props': [('border', '1px solid black'),
                                          ('padding', '4px'), ('text-align', 'left')]},
         {'selector': 'th', 'props': [('font-family', 'Century Gothic'), ('font-size', '9pt')]},
         {'selector': 'thead', 'props': [('background-color', 'lightblue')]},
         {'selector': '', 'props': [('border-collapse', 'collapse'),
                                    ('border', '1px solid black')]},
         ]).set_properties(**{'font-size': '10pt', 'font-family': 'Century Gothic'}).render()
    html = html.replace('<th class="blank level0" ></th>', '<th class="blank level0">S_NO</th>')

    html1 = df1.style.applymap(highlight_cols_red, subset=['TESTCASES_FAILED']). \
        applymap(highlight_cols_green, subset=['TESTCASES_PASSED']). \
        applymap(center_vals, subset=['SUITE_STATUS']).\
        applymap(center_vals, subset=['TOTAL_TESTCASES']). \
        applymap(center_vals, subset=['TESTCASES_PASSED']). \
        applymap(center_vals, subset=['TESTCASES_FAILED']).\
        applymap(center_vals, subset=['EXECUTION_TIME']).set_table_styles(
        [{'selector': 'tr.hover td', 'props': [('background-color', 'lightyellow')]},
         {'selector': 'th, td', 'props': [('border', '1px solid black'),
                                          ('padding', '4px'), ('text-align', 'left')]},
         {'selector': 'th', 'props': [('font-family', 'Century Gothic'), ('font-size', '9pt')]},
         {'selector': 'thead', 'props': [('background-color', 'lightblue')]},
         {'selector': '', 'props': [('border-collapse', 'collapse'),
                                    ('border', '1px solid black')]},
         ]).set_properties(**{'font-size': '10pt', 'font-family': 'Century Gothic'}).render()
    html1 = html1.replace('<th class="blank level0" ></th>', '<th class="blank level0">S_NO</th>')

    html_content = "<b>Automation Execution Summary: Test Suite Level</br></br>" + html1 + \
                   "</br><b>Automation Execution Summary: Test Case Level</br></br>" + html
    with open(html_file, 'w') as f:
        f.write(html_content)
    f.close()


def highlight_vals(val, color='lightgreen'):
    if val == 'PASS':
        return 'background-color: %s' % color
    else:
        return 'background-color: red'


def center_vals(val):
    return 'text-align: center'


def highlight_cols_green(val, color='lightgreen'):
    return 'background-color: %s' % color


def highlight_cols_red(val, color='red'):
    return 'background-color: %s' % color


def left_vals(val):
    return 'text-align: left'
