Surgical-Python (soap) is a collection of Python commands intended to be used for Surgical Outcome Data Analysis, from data importing, cleaning-up, merging data-frame, analysis and visualization. (from SURPY import soap as sp)
Data importing from Excel file, followed by data exploration. (sp.soapsheetin(path))
Data scan. (sp.soapplore(data, oc))
Comparison of parametric/non-parametric data between 2 groups of the outcome (sp.soaptu(data,oc,var)) and (sp.soapvarin() followed by sp.soaptumulti(data,oc,factors))
Comparison of distribution between groups. (sp.soapbivarin(data) followed by sp.soapxtab(data, var_a, var_b)) and (sp.soapxtabax(data,outcome))
Survival curve drawing (sp.single_kmc(data, status, interval)) and survival comparisons (sp.compare_kmc(data, factor, status, interval) 

for manual, go to:
https://github.com/sasurasa/Surgical-Outcome-Analysis-on-Python/blob/SURPY/SURPY%20manual%20040321SS.pdf