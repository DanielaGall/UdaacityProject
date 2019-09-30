{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import re\n",
    "import pandas as pd\n",
    "import operator \n",
    "\n",
    "# Add 'datatype' column that indicates if the record is original wiki answer as 0, training data 1, test data 2, onto \n",
    "# the dataframe - uses stratified random sampling (with seed) to sample by task & plagiarism amount \n",
    "\n",
    "# Use function to label datatype for training 1 or test 2 \n",
    "def create_datatype(df, train_value, test_value, datatype_var, compare_dfcolumn, operator_of_compare, value_of_compare,\n",
    "                    sampling_number, sampling_seed):\n",
    "    # Subsets dataframe by condition relating to statement built from:\n",
    "    # 'compare_dfcolumn' 'operator_of_compare' 'value_of_compare'\n",
    "    df_subset = df[operator_of_compare(df[compare_dfcolumn], value_of_compare)]\n",
    "    df_subset = df_subset.drop(columns = [datatype_var])\n",
    "\n",
    "    # Prints counts by task and compare_dfcolumn for subset df\n",
    "    #print(\"\\nCounts by Task & \" + compare_dfcolumn + \":\\n\", df_subset.groupby(['Task', compare_dfcolumn]).size().reset_index(name=\"Counts\") )\n",
    "\n",
    "    # Sets all datatype to value for training for df_subset\n",
    "    df_subset.loc[:, datatype_var] = train_value\n",
    "\n",
    "    # Performs stratified random sample of subset dataframe to create new df with subset values \n",
    "    df_sampled = df_subset.groupby(['Task', compare_dfcolumn], group_keys=False).apply(lambda x: x.sample(min(len(x), sampling_number), random_state = sampling_seed))\n",
    "    df_sampled = df_sampled.drop(columns = [datatype_var])\n",
    "    # Sets all datatype to value for test_value for df_sampled\n",
    "    df_sampled.loc[:, datatype_var] = test_value\n",
    "\n",
    "    # Prints counts by compare_dfcolumn for selected sample\n",
    "    #print(\"\\nCounts by \"+ compare_dfcolumn + \":\\n\", df_sampled.groupby([compare_dfcolumn]).size().reset_index(name=\"Counts\") )\n",
    "    #print(\"\\nSampled DF:\\n\",df_sampled)\n",
    "\n",
    "    # Labels all datatype_var column as train_value which will be overwritten to \n",
    "    # test_value in next for loop for all test cases chosen with stratified sample\n",
    "    for index in df_sampled.index: \n",
    "        # Labels all datatype_var columns with test_value for straified test sample\n",
    "        df_subset.loc[index, datatype_var] = test_value\n",
    "\n",
    "    #print(\"\\nSubset DF:\\n\",df_subset)\n",
    "    # Adds test_value and train_value for all relevant data in main dataframe\n",
    "    for index in df_subset.index:\n",
    "        # Labels all datatype_var columns in df with train_value/test_value based upon \n",
    "        # stratified test sample and subset of df\n",
    "        df.loc[index, datatype_var] = df_subset.loc[index, datatype_var]\n",
    "\n",
    "    # returns nothing because dataframe df already altered \n",
    "\n",
    "def train_test_dataframe(clean_df, random_seed=100):\n",
    "\n",
    "    new_df = clean_df.copy()\n",
    "\n",
    "    # Initialize datatype as 0 initially for all records - after function 0 will remain only for original wiki answers\n",
    "    new_df.loc[:,'Datatype'] = 0\n",
    "\n",
    "    # Creates test & training datatypes for plagiarized answers (1,2,3)\n",
    "    create_datatype(new_df, 1, 2, 'Datatype', 'Category', operator.gt, 0, 1, random_seed)\n",
    "\n",
    "    # Creates test & training datatypes for NON-plagiarized answers (0)\n",
    "    create_datatype(new_df, 1, 2, 'Datatype', 'Category', operator.eq, 0, 2, random_seed)\n",
    "\n",
    "    # creating a dictionary of categorical:numerical mappings for plagiarsm categories\n",
    "    mapping = {0:'orig', 1:'train', 2:'test'} \n",
    "\n",
    "    # traversing through dataframe and replacing categorical data\n",
    "    new_df.Datatype = [mapping[item] for item in new_df.Datatype] \n",
    "\n",
    "    return new_df\n",
    "\n",
    "\n",
    "# helper function for pre-processing text given a file\n",
    "def process_file(file):\n",
    "    # put text in all lower case letters \n",
    "    all_text = file.read().lower()\n",
    "\n",
    "    # remove all non-alphanumeric chars\n",
    "    all_text = re.sub(r\"[^a-zA-Z0-9]\", \" \", all_text)\n",
    "    # remove newlines/tabs, etc. so it's easier to match phrases, later\n",
    "    all_text = re.sub(r\"\\t\", \" \", all_text)\n",
    "    all_text = re.sub(r\"\\n\", \" \", all_text)\n",
    "    all_text = re.sub(\"  \", \" \", all_text)\n",
    "    all_text = re.sub(\"   \", \" \", all_text)\n",
    "\n",
    "    return all_text\n",
    "\n",
    "\n",
    "def create_text_column(df, file_directory='data/'):\n",
    "    '''Reads in the files, listed in a df and returns that df with an additional column, `Text`. \n",
    "       :param df: A dataframe of file information including a column for `File`\n",
    "       :param file_directory: the main directory where files are stored\n",
    "       :return: A dataframe with processed text '''\n",
    "\n",
    "    # create copy to modify\n",
    "    text_df = df.copy()\n",
    "\n",
    "    # store processed text\n",
    "    text = []\n",
    "\n",
    "    # for each file (row) in the df, read in the file \n",
    "    for row_i in df.index:\n",
    "        filename = df.iloc[row_i]['File']\n",
    "        #print(filename)\n",
    "        file_path = file_directory + filename\n",
    "        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:\n",
    "\n",
    "            # standardize text using helper function\n",
    "            file_text = process_file(file)\n",
    "            # append processed text to list\n",
    "            text.append(file_text)\n",
    "\n",
    "    # add column to the copied dataframe\n",
    "    text_df['Text'] = text\n",
    "\n",
    "    return text_df\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from unittest.mock import MagicMock, patch\n",
    "import sklearn.naive_bayes\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import re\n",
    "\n",
    "# test csv file\n",
    "TEST_CSV = 'data/test_info.csv'\n",
    "\n",
    "class AssertTest(object):\n",
    "    '''Defines general test behavior.'''\n",
    "    def __init__(self, params):\n",
    "        self.assert_param_message = '\\n'.join([str(k) + ': ' + str(v) + '' for k, v in params.items()])\n",
    "\n",
    "    def test(self, assert_condition, assert_message):\n",
    "        assert assert_condition, assert_message + '\\n\\nUnit Test Function Parameters\\n' + self.assert_param_message\n",
    "\n",
    "def _print_success_message():\n",
    "    print('Tests Passed!')\n",
    "\n",
    "# test clean_dataframe\n",
    "def test_numerical_df(numerical_dataframe):\n",
    "\n",
    "    # test result\n",
    "    transformed_df = numerical_dataframe(TEST_CSV)\n",
    "\n",
    "    # Check type is a DataFrame\n",
    "    assert isinstance(transformed_df, pd.DataFrame), 'Returned type is {}.'.format(type(transformed_df))\n",
    "\n",
    "    # check columns\n",
    "    column_names = list(transformed_df)\n",
    "    assert 'File' in column_names, 'No File column, found.'\n",
    "    assert 'Task' in column_names, 'No Task column, found.'\n",
    "    assert 'Category' in column_names, 'No Category column, found.'\n",
    "    assert 'Class' in column_names, 'No Class column, found.'\n",
    "\n",
    "    # check conversion values\n",
    "    assert transformed_df.loc[0, 'Category'] == 1, '`heavy` plagiarism mapping test, failed.'\n",
    "    assert transformed_df.loc[2, 'Category'] == 0, '`non` plagiarism mapping test, failed.'\n",
    "    assert transformed_df.loc[30, 'Category'] == 3, '`cut` plagiarism mapping test, failed.'\n",
    "    assert transformed_df.loc[5, 'Category'] == 2, '`light` plagiarism mapping test, failed.'\n",
    "    assert transformed_df.loc[37, 'Category'] == -1, 'original file mapping test, failed; should have a Category = -1.'\n",
    "    assert transformed_df.loc[41, 'Category'] == -1, 'original file mapping test, failed; should have a Category = -1.'\n",
    "\n",
    "    _print_success_message()\n",
    "\n",
    "\n",
    "def test_containment(complete_df, containment_fn):\n",
    "\n",
    "    # check basic format and value \n",
    "    # for n = 1 and just the fifth file\n",
    "    test_val = containment_fn(complete_df, 1, 'g0pA_taske.txt')\n",
    "\n",
    "    assert isinstance(test_val, float), 'Returned type is {}.'.format(type(test_val))\n",
    "    assert test_val<=1.0, 'It appears that the value is not normalized; expected a value <=1, got: '+str(test_val)\n",
    "\n",
    "    # known vals for first few files\n",
    "    filenames = ['g0pA_taska.txt', 'g0pA_taskb.txt', 'g0pA_taskc.txt', 'g0pA_taskd.txt']\n",
    "    ngram_1 = [0.39814814814814814, 1.0, 0.86936936936936937, 0.5935828877005348]\n",
    "    ngram_3 = [0.0093457943925233638, 0.96410256410256412, 0.61363636363636365, 0.15675675675675677]\n",
    "\n",
    "    # results for comparison\n",
    "    results_1gram = []\n",
    "    results_3gram = []\n",
    "\n",
    "    for i in range(4):\n",
    "        val_1 = containment_fn(complete_df, 1, filenames[i])\n",
    "        val_3 = containment_fn(complete_df, 3, filenames[i])\n",
    "        results_1gram.append(val_1)\n",
    "        results_3gram.append(val_3)\n",
    "\n",
    "    # check correct results\n",
    "    assert all(np.isclose(results_1gram, ngram_1, rtol=1e-04)), \\\n",
    "    'n=1 calculations are incorrect. Double check the intersection calculation.'\n",
    "    # check correct results\n",
    "    assert all(np.isclose(results_3gram, ngram_3, rtol=1e-04)), \\\n",
    "    'n=3 calculations are incorrect.'\n",
    "\n",
    "    _print_success_message()\n",
    "\n",
    "def test_lcs(df, lcs_word):\n",
    "\n",
    "    test_index = 10 # file 10\n",
    "\n",
    "    # get answer file text\n",
    "    answer_text = df.loc[test_index, 'Text'] \n",
    "\n",
    "    # get text for orig file\n",
    "    # find the associated task type (one character, a-e)\n",
    "    task = df.loc[test_index, 'Task']\n",
    "    # we know that source texts have Class = -1\n",
    "    orig_rows = df[(df['Class'] == -1)]\n",
    "    orig_row = orig_rows[(orig_rows['Task'] == task)]\n",
    "    source_text = orig_row['Text'].values[0]\n",
    "\n",
    "    # calculate LCS\n",
    "    test_val = lcs_word(answer_text, source_text)\n",
    "\n",
    "    # check type\n",
    "    assert isinstance(test_val, float), 'Returned type is {}.'.format(type(test_val))\n",
    "    assert test_val<=1.0, 'It appears that the value is not normalized; expected a value <=1, got: '+str(test_val)\n",
    "\n",
    "    # known vals for first few files\n",
    "    lcs_vals = [0.1917808219178082, 0.8207547169811321, 0.8464912280701754, 0.3160621761658031, 0.24257425742574257]\n",
    "\n",
    "    # results for comparison\n",
    "    results = []\n",
    "\n",
    "    for i in range(5):\n",
    "        # get answer and source text\n",
    "        answer_text = df.loc[i, 'Text'] \n",
    "        task = df.loc[i, 'Task']\n",
    "        # we know that source texts have Class = -1\n",
    "        orig_rows = df[(df['Class'] == -1)]\n",
    "        orig_row = orig_rows[(orig_rows['Task'] == task)]\n",
    "        source_text = orig_row['Text'].values[0]\n",
    "        # calc lcs\n",
    "        val = lcs_word(answer_text, source_text)\n",
    "        results.append(val)\n",
    "\n",
    "    # check correct results\n",
    "    assert all(np.isclose(results, lcs_vals, rtol=1e-05)), 'LCS calculations are incorrect.'\n",
    "\n",
    "    _print_success_message()\n",
    "\n",
    "def test_data_split(train_x, train_y, test_x, test_y):\n",
    "\n",
    "    # check types\n",
    "    assert isinstance(train_x, np.ndarray),\\\n",
    "        'train_x is not an array, instead got type: {}'.format(type(train_x))\n",
    "    assert isinstance(train_y, np.ndarray),\\\n",
    "        'train_y is not an array, instead got type: {}'.format(type(train_y))\n",
    "    assert isinstance(test_x, np.ndarray),\\\n",
    "        'test_x is not an array, instead got type: {}'.format(type(test_x))\n",
    "    assert isinstance(test_y, np.ndarray),\\\n",
    "        'test_y is not an array, instead got type: {}'.format(type(test_y))\n",
    "\n",
    "    # should hold all 95 submission files\n",
    "    assert len(train_x) + len(test_x) == 95, \\\n",
    "        'Unexpected amount of train + test data. Expecting 95 answer text files, got ' +str(len(train_x) + len(test_x))\n",
    "    assert len(test_x) > 1, \\\n",
    "        'Unexpected amount of test data. There should be multiple test files.'\n",
    "\n",
    "    # check shape\n",
    "    assert train_x.shape[1]==2, \\\n",
    "        'train_x should have as many columns as selected features, got: {}'.format(train_x.shape[1])\n",
    "    assert len(train_y.shape)==1, \\\n",
    "        'train_y should be a 1D array, got shape: {}'.format(train_y.shape)\n",
    "\n",
    "    _print_success_message()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "conda_python3",
   "language": "python",
   "name": "conda_python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
