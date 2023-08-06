import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from statsmodels.tools.eval_measures import mse, rmse
import statsmodels.api as sm
import math
import statistics

class professorRegressor(object) :

	def __init__ (self,df,study=None) :
		self.pr = pd.DataFrame()
		if study==None: study = "Comparison of the LogSEM values for Pairwise regression"
		if df.shape[1] != 2 :
			print("invalid object - please provide in a nx2 matrix where the second column is numeric and the first is a classifier")
		else :
			df.rename(columns={ df.columns[0]: "category" }, inplace = True)
			for i in df.iloc[:,0].drop_duplicates().tolist():
				for j in df.iloc[:,0].drop_duplicates().tolist():
					if i != j:
						# print(i,j)
						X = df.loc[df.iloc[:,0] == i].reset_index().drop(["index","category"],axis=1)
						Y = df.loc[df.iloc[:,0] == j].reset_index().drop(["index","category"],axis=1)
						if X.shape[0] != Y.shape[0] : print('warning: the number of observations for '+i+' vs '+j+' are not equal')
						rs = min(X.shape[0],Y.shape[0])
						X = X[:rs]
						Y = Y[:rs]
						m = sm.OLS(Y, X).fit()
						m_1 = sm.OLS(X,Y).fit()
						try: m_logSEM = math.log10(m.bse)
						except: m_logSEM = -300
						try: m_1_logSEM = math.log10(m_1.bse)
						except: m_1_logSEM = -300
						self.pr = self.pr.append(pd.DataFrame({
							"Study":[study],
							"Specimen A":[i],
							"Specimen B":[j],
							"Comparison":[str(i)+' vs '+str(j)],
							"# of Observations":[rs],
							"LogSEM Primary":m_logSEM,
							"LogSEM Secondary":m_1_logSEM,
							"Min LogSEM":min(m_logSEM,m_1_logSEM),
							"Mean LogSEM":(m_logSEM+m_1_logSEM)/2,
							"STDEV LogSEM":statistics.stdev([m_logSEM,m_1_logSEM]),
							"Max LogSEM":max(m_logSEM,m_1_logSEM),
							"LogSEM Delta":abs(m_logSEM-m_1_logSEM),
							"Model Primary":m,
							"Model Inverse":m_1
						}))

	def getDataFrame (self) :
		return self.pr


