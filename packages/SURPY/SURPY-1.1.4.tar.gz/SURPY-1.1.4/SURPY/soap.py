import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import shapiro
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import sksurv
from sksurv.nonparametric import kaplan_meier_estimator
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

pd.set_option('display.max_columns', None)

def soapsheetin(path):
	data = pd.read_excel(path, sheet_name='Sheet1', parse_dates=True, engine='openpyxl')
	return data
	
def sexplore(data):
	size = data.size
	dimension = data.shape
	variables = data.columns.values.tolist()
	print('===============================================================================================================')
	print('\nThe dataframe has',size, 'cells, with',dimension,'(row x column) dimension.\n')
	print('All the variables include;',variables,'\n')
	print('===============================================================================================================')
	print('Types and numbers of each variables are;')
	print(data.info())

def shapif(data):
    d1 = {}
    for factor in data.columns.values.tolist():
        if data[factor].dtypes == 'float64':
        	x = data[factor].dropna()
        	s = stats.shapiro(x)
        	d1[factor] = s
    df1 = pd.DataFrame(d1.items(), columns=['variable', 'Shapiro-Wilk result'])
    print(df1)

def shapii(data):
    d2 = {}
    for factor in data.columns.values.tolist():
        if data[factor].dtypes == 'int64':
        	x = data[factor]
        	s = stats.shapiro(x)
        	d2[factor] = s
    df2 = pd.DataFrame(d2.items(), columns=['variable', 'Shapiro-Wilk result'])
    print(df2)

def describe(data):
	dat = []
	for var in data.columns.values.tolist():
		if data[var].nunique() > 2 and data[var].dtypes != 'O':
			des = (data[var].describe())
			dat.append(des)
	dsc = pd.concat(dat, axis=1)
	print(dsc.fillna('-'))				

def countbi(data):
	dat = []
	for var in data.columns.values.tolist():
		if data[var].nunique() == 2:
			des = data.groupby(var)[var].count()
			dat.append(des)
	dsc = pd.concat(dat, axis = 1)
	sum = dsc.aggregate('sum', axis = 0)
	dsc = dsc.append(sum, ignore_index=True)
	lst_a = dsc.index.tolist()
	lst_a[-1] = 'vertisum'
	dsc.index = lst_a

	cols = dsc.columns.tolist()
	for i in cols:
		dsc['%'+i] = dsc[i]/dsc[i].vertisum*100
	print(dsc.fillna('-'))

def mbo(data, oc):
	mbo = []
	for var in data.columns.values.tolist():
		if data[var].nunique() > 2 and data[var].dtypes != 'O':
			mbo.append(data.groupby(oc).mean()[var])
	des = pd.concat(mbo, axis = 1)
	print(des)

def soaplore(data, oc):
	sexplore(data)
	print('\n')
	shapif(data)
	print('\n')
	shapii(data)
	print('\n')
	print('General summary statistics:\n')	
	describe(data)
	print('Count binary data:\n')
	countbi(data)
	print ('Mean by group \n')
	mbo(data, oc)
	
def soap_TU(data, oc, var):
	if data[oc].nunique() != 2:
		print('The outcome', oc, 'is non-binary')
	else:
		var_by_outcome = data.groupby(oc)[var].describe()
		print(var,'\n', var_by_outcome)
		cat1 = data[data[oc] == 0]
		cat2 = data[data[oc] == 1]
		print('-----------------------------------------------------------------\n')
		print(stats.ttest_ind(cat1[var].dropna(), cat2[var].dropna()))
		print(stats.mannwhitneyu(cat1[var].dropna(), cat2[var].dropna()))
			
		plt.boxplot([cat1[var].dropna(), cat2[var].dropna()], showmeans = True)
		plt.show()

def soap_multi_T(data, oc):
	factors = list(map(str, input('Enter a list of factors to be analysed,separated by a space: ').split()))
	for var in factors:
		if data[oc].nunique() != 2:
			print('The outcome', oc, 'is non-binary')
			continue
		else:
			var_by_outcome = data.groupby(oc)[var].describe()
			print(var,'\n', '----------------------------------------------------------------')
			print(var_by_outcome)
			cat1 = data[data[oc] == 0]
			cat2 = data[data[oc] == 1]
			print('---------------------------------------------------------------')
			print(stats.ttest_ind(cat1[var].dropna(), cat2[var].dropna()))
			print(stats.mannwhitneyu(cat1[var].dropna(), cat2[var].dropna()))
			print('\n')

def soaptbivar(data, bivar, var):
	edb = []
	for i in range(len(bivar)):
		eb = data.groupby(bivar[i])[var].mean()
		edb.append(eb)
		cat1 = data[data[bivar[i]] == 0]
		cat2 = data[data[bivar[i]] == 1]
		print('T-test for '+ var + ' by ' + bivar[i])
		print(stats.ttest_ind(cat1[var].dropna(), cat2[var].dropna()))
	a = pd.concat(edb, axis =1)
	a.columns = bivar
	a = a.add_prefix(var+'_')
	print ('=============================================================================')
	print('Mean '+ var + ' by each binary factors')
	print(a)

def soapubivar(data, bivar, var):
	edb2 = []	
	for i in range(len(bivar)):
		eb2 = data.groupby(bivar[i])[var].median()
		edb2.append(eb2)
		cat1 = data[data[bivar[i]] == 0]
		cat2 = data[data[bivar[i]] == 1]
		print('Ranksum-test for '+ var + ' by ' + bivar[i])
		print(stats.mannwhitneyu(cat1[var].dropna(), cat2[var].dropna()))
	b = pd.concat(edb2, axis =1)
	b.columns = bivar
	b = b.add_prefix(var+'_')
	print ('=============================================================================')
	print('Median '+ var + ' by each binary factors')
	print(b)

def soap_T_for_multibinary(data, var):
	bivar = list(map(str, input('Enter a list of binary variables to be used for comparisons of fixed continuous var,separated by a space: ').split()))
	for v in bivar:
		if data[v].nunique() != 2:
			bivar.remove(v)
			print('The variable', v, 'is non-binary')
	soaptbivar(data, bivar, var)
	print('\n')
	soapubivar(data, bivar, var)

def soap_x_tab(data, var_a, var_b):
	table = pd.crosstab(data[var_b], data[var_a])
	c, p, dof, expected = chi2_contingency(table)
	print('=================================================================================\n')
	print('Data dimension: ', table.shape)
	print('Chi-square value = ',c)
	print('Chisquare p-value =',p)
	print('=================================================================================\n')	
	twosub = data[[var_a, var_b]]
	var_b_list = data[var_b].unique().tolist()
	all_col_list = []
	for i in var_b_list:
		Bi = twosub[data[var_b] == i]
		Ci = Bi.groupby(var_a).count()
		dict = {Ci.columns[0]:Ci.columns[0]+str(i)}
		Ci = Ci.rename(columns=dict)
		all_col_list.append(Ci)
	d = pd.concat(all_col_list, axis=1, join='outer').fillna(0)
	sum = d.aggregate('sum', axis = 1)
	e = pd.concat([d, sum], axis=1, join='inner')
	e = e.rename(columns={0:'horizonsum'})
	sum = e.aggregate('sum', axis = 0)
	e = e.append(sum, ignore_index=True)
	lst_a = data[var_a].unique()
	lst_a.sort()
	lst_a = lst_a.tolist()
	lst_a.append('vertisum')
	e[var_a] = lst_a
	cols = e.columns.tolist()
	cols = cols[-1:] + cols[:-1]
	e = e[cols]
	cols = list(e.columns)
	h = cols[1:-1]
	h.sort()
	cols[1:-1]=h
	e = e[cols]
	i = e.iloc[:,1:].astype(int)
	e = e.iloc[:,:1]
	e = pd.concat([e,i], axis = 1, join = 'inner')
	print('\n')
	for i in cols:
		if i == 'horizonsum':
			continue
		if i == var_a:
			continue
		else:
			e['%'+i] = e[i]/e['horizonsum']*100
	print(e)
	if data[var_b].nunique()==2:
		f = e.columns.tolist()
		var = e.iloc[0:-1][f[0]]
		outc = e.iloc[0:-1][f[-1]]
		fig = plt.figure(figsize =(10, 5))
		plt.bar(var,outc, label=var.name)
		plt.xlabel(var.name)
		plt.xticks(range(var.min(),var.max()+1))
		plt.ylabel(outc.name)
		plt.title('Chi-square p-value: '+ str(p))
		plt.show()

def chi_pv(data, outcome, factor):
	table = pd.crosstab(data[outcome], data[factor])
	c, p, dof, expected = chi2_contingency(table)
	return p

def soap_x_across(data, outcome):
    d = {}
    for factor in data.columns.values.tolist():
        if data[factor].nunique() > 5:
            continue
        elif factor == outcome:
            continue
        else:
            pv=chi_pv(data, outcome, factor)
            d[factor] = pv
    df = pd.DataFrame(d.items(), columns=['variable', 'Chisquare p-value'])
    print(df)

def single_kmc(data, status, interval):

	sta = []
	for i in data[status]:
		b = bool(i)
		sta.append(b)
	interv = data[interval]
	time, survival_prob = kaplan_meier_estimator(sta, interv)
	plt.step(time, survival_prob)
	plt.ylabel("est. probability of survival")
	plt.xlabel("time $(days)$")


def compare_kmc(data, factor, status, interval):
	f = data[factor].drop_duplicates().tolist()
	f.sort()
	
	for i in f:
		group_i = data[data[factor] == i]
		interv_i = group_i[interval]
		interv_i.reset_index(drop=True)
		interv_i = interv_i.tolist()
		interv_i.append(0)
	
		sta_i = []
		for j in group_i[status]:
			c = bool(j)
			sta_i.append(c)
		sta_i.append(False)

	
	

		time, survival_prob = kaplan_meier_estimator(sta_i, interv_i)
		plt.step(time, survival_prob, where='post', label=str(factor)+'=%s' % i)
	plt.ylabel("est. probability of survival")
	plt.xlabel("time $(days)$")
	plt.legend(loc='best')

	if data[factor].nunique() != 2:
		print('The factor', factor, 'is non-binary, so the Logrank statistics is not calculated')
	else:
		f = data[factor].drop_duplicates().tolist()
		f.sort()
		time = []
		censor = []
		
		for i in f:
			interv_i = []
			group_i = df[df[factor] == i]
			for j in group_i[interval]:
				interv_i.append(j)
			time.append(interv_i)
				
			censor_i = []
			for k in group_i[status]:
				censor_i.append(k)
			censor.append(censor_i)
		T = time[0]
		T1 = time[1]
		E = censor[0]
		E1 = censor[1]

		results = logrank_test(T, T1, E, E1)
		results.print_summary()
        


