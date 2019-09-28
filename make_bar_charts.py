"""

Code used for processing the data
in order to create bar charts of the occurence
of technologies based on chart use.



"""


import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib
import seaborn as sns


def make_count_dict(count_list) : 

	item_set = list(set(count_list))
	count_dict = {}
	for item in item_set :
		count_dict[item] = count_list.count(item )

	return count_dict

def count_list_items(count_list) : 

	"""

	Parameters
	------------

	count_list : list 

	list of strs / things we want to count.

	Returns
	------------

	count_data : pandas dataframe
	
	contains the individual elements
	and the count of them within the list

	"""
	
	count_dict = make_count_dict(count_list)
	
	keys = list(count_dict.keys())
	values = list(count_dict.values())
	
	count_data = pd.DataFrame({'Item' : keys, 'Count' : values})
	
	return count_data



if __name__ == "__main__" : 

	df=pd.read_csv("cleaned_survey_results_2019.csv")
	df = df[['Which of these charts have you used in production in the last 6 months? Select all that apply.','What technologies do you use to visualize data? Select all that apply.','What does your audience use your data visualization for? Select all that apply.']].dropna()


	#simpler names for the columns:
	df.columns = [ 'charts','techs','use']


	#Pull out counts of audience use:
	audience_uses = list(df['use'])
	all_audience_uses = [ ]
	for k in audience_uses :
		if isinstance(k,str) : 
			for l in k.split(', ') : 
				all_audience_uses.append(l)
	audience_use_count = count_list_items(all_audience_uses).sort_values(by='Count',ascending=False)
	audience_use_count = audience_use_count.loc[audience_use_count['Count']>100] #Filter the most used technologies.
	audience_use_set = list(set(list(audience_use_count['Item'])))


	#Make a plot for each of the technologies:
	what_to_compare = 'techs'
	for use_case in audience_use_set : 
		this_use_df = df[ df['use'].str.contains(use_case)]
		tech_types = list(this_use_df[what_to_compare])

		#Multiple answers so we have to split up the strings.
		all_tech_types = [ ]
		for k in tech_types :
			if isinstance(k,str) : 
				for l in k.split(',') : 
					all_tech_types.append(l)
		tech_type_count = count_list_items(all_tech_types)


		#Make the plot:
		plt.rcParams['figure.figsize']=[10,10]
		tech_data = tech_type_count.loc[tech_type_count['Count'] > 10 ].sort_values(by='Count',ascending=False)[0:7]
		sns.barplot(y='Item',x='Count',data=tech_data,orient='h',palette="Blues")
		plt.ylabel("Technology",fontsize=20)
		plt.xlabel("Users",fontsize=20)
		plt.xticks(fontsize=20)
		plt.yticks(fontsize=20)
		#Removes the box:
		for spine in plt.gca().spines.values():
			spine.set_visible(False)
		plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='on', labelbottom='on')
		plt.title(use_case,fontsize=20)
		plt.savefig("counts_{}_{}".format(use_case.replace('/','&'),what_to_compare),bbox_inches='tight')


