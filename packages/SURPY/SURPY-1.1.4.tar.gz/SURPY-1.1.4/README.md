Surgical-Python (soap) is a collection of Python commands intended to be used for Surgical Outcome Data Analysis, from data importing, cleaning-up, merging data-frame, analysis and visualization. (from SURPY import soap as sp)
\n
Data importing from Excel file, followed by data exploration. (sp.soapsheetin(path))
\n
Data scan. (sp.soapplore(data, oc))
\n
Comparison of parametric/non-parametric data between 2 groups of the outcome (sp.soap_TU(data,oc,var)), soap_multi_T(data, oc) [fixed binary outcome tested on multiple continuous var] and soap_T_for_multibinary(data, var) [fixed continuous var tested against multiple binary variables at a time].
\n
Comparison of distribution between groups using Chi-square test. (sp.soap_x_tab(data, var_a, var_b)) and (sp.soap_x_across(data,outcome))
\n
Survival curve drawing (sp.single_kmc(data, status, interval)) and survival comparisons (sp.compare_kmc(data, factor, status, interval)) 
\n
for manual, go to:
https://github.com/sasurasa/Surgical-Outcome-Analysis-on-Python/blob/SURPY/SURPY%20manual%20070321SS.pdf