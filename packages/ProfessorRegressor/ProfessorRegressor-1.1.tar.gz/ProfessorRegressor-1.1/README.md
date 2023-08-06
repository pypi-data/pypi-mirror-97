# professorRegressor
Statistical python model for comparison of species using pairwise regression.

### Usage
It's import to provide PR with a 2xn pandas matrix where the first column contains a categorical variable, like the species or the specimens that your study wishes to compare, and the second containing non-null numerical observations relating to the first variable.

You need at least 2 observations per specimen/species and more will provide greater statistical accuracies.

Note: at the time of first publication, there are no failsafes for null values in the dataset. Please remove these as part of pre-processing.

To install, use pip:
pip install professorRegressor

To use in your program, first initialise by passing your pandas dataset. Thereafter you can export using the getDataFrame method. Here is an example:

import professorRegressor
pr = professorRegressor(iris)
pr_df = pr.getDataFrame()