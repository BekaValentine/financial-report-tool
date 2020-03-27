# Financial Report Tool

This is a relatively simple tool for building financial reports on how you're spending money.

## Command Line Usage

```
python3 build_report.py <input-file> <output-file>
```

## Interactive Usage

This tool interactively builds up a collection of categories and criteria for categorizing transactions based on their descriptions.

Any uncategorized transactions in the input file will need to be categorized before the report is saved.

During categorization, you can choose from previously added categories or add new ones.

The criteria for a category are just substrings that can be found in the transaction description. For example, if you wish to indicate that any transaction containing the word "pizza" should be categorized as food, then you would select the category `food` and give the substring `pizza`. All matching of substrings is case insensitive.

If you need to edit the categorization criteria, edit `categories.json`. See [Categories File](#categoriesfile) for more information.

## Input File

The input file should be a CSV consisting of a header row and some number of transaction rows.

By default, there should be columns named 'Date', 'Amount', and 'Description'. See [Table Settings](#tablesettings) for alternative options.

## Output File

The output file will contain the report broken into categories.

## Table Settings

The `table_settings.json` file contains a dictionary object where the keys are the names of the transaction properties that are expected to exist within the input file, and the values are the corresponding column names that are actually used within the input file.

By default, these are `"Date"` for the `date` property, `"Amount"` for the `amount` property, and `"Description"` for the `description` property.

If your bank uses different names for these transaction properties, simply edit this file to replace the values accordingly. For example, if your bank uses `"AMT"` as the name for the transaction `amount` property, then your settings file would have `"AMT"` for the value of the `amount` key.

## Categories File

The `categories.json` file contains the categorization criteria for your reports. If it does not exist, it will be created when you initially run the tool.

The file contains a JSON dictionary which has category names as keys, and lists of criterion substrings as values.

If the key `"food"` has the value `["pizza", "tacos"]` as its value, then this means that a transaction can be categorized as food if its description contains either the substring `"pizza"` or the substring `"tacos"`.

If you entered the wrong substring as a criterion, simply edit the string to correct it before you run the tool again.

If you entered the wrong category name, simply edit the relevant key.

If you accidentally created a category you didn't want, simply merge it's list with the correct category's list as needed.
