"""

Code used to prcoess the DVS Survey
Data from 2019 in order to produce a
heatmap of the most commonly co-occuring
technologies and chart types.

"""


from make_bar_charts import *
from tqdm import tqdm as tqdm

#Read in the data:
df=pd.read_csv("cleaned_survey_results_2019.csv")
df = df[['Which of these charts have you used in production in the last 6 months? Select all that apply.','What technologies do you use to visualize data? Select all that apply.']].dropna()

#Count chart tupes:
chart_types = list(df['Which of these charts have you used in production in the last 6 months? Select all that apply.'])
#Multiple answers so we have to split up the strings:
all_chart_types = [ ]
for k in chart_types :
    if isinstance(k,str) : 
        for l in k.split(', ') : 
            #The 'Flow diagram entry has brackets and commas.'
            #Remove these manually.
            if l == 'Flow Diagram (Sankey' : 
                all_chart_types.append('Flow Diagram')
            elif l == 'DAGRE' :
                pass
            elif l == 'Flow Chart)' : 
                pass
            else : 
                all_chart_types.append(l)
            
chart_type_count = count_list_items(all_chart_types).sort_values(by='Count',ascending=False)
chart_type_set = list(set(all_chart_types))
print("Found {} chart types".format(len(chart_type_set)))


#Count the technologies:
tech_choices = list(df['What technologies do you use to visualize data? Select all that apply.'])
#Multiple answers so we have to split up the strings:
all_technologies = [ ]
for k in tech_choices :
    if isinstance(k,str) : 
        for l in k.split(', ') : 
            all_technologies.append(l)
tech_count = count_list_items(all_technologies).sort_values(by='Count',ascending=False)

tech_set = list(set(all_technologies))
print("Found {} technologies".format(len(tech_set)))


#Focus on charts and technologies which occur at least 50 times:
high_count_tech_set = list(tech_count.loc[tech_count['Count']>50]['Item'])
high_count_chart_set = list(chart_type_count.loc[chart_type_count['Count']>50]['Item'])

#Now combine the two counts into a dataframe of coocurences:
co_occerence_data = pd.DataFrame()
for tech in tqdm(high_count_tech_set) :
    for chart in high_count_chart_set : 
        count=0
        for chartz,techz in zip(chart_types,tech_choices) :
            if tech in techz and chart in chartz :
                count += 1
        df_to_append = pd.DataFrame({"Chart" : [chart],"Tech" : [tech] , 'Co-occurence' : [count]})
        co_occerence_data=co_occerence_data.append(df_to_append)       
tech_count.columns=['Item','Tech_Count']
chart_type_count.columns = [ 'Item','Chart_Count']
co_occerence_data = co_occerence_data.merge(tech_count,left_on='Tech',right_on='Item')
co_occerence_data = co_occerence_data.merge(chart_type_count,left_on='Chart',right_on='Item')
co_occerence_data = co_occerence_data.drop(columns=['Item_x','Item_y'])
co_occerence_data = co_occerence_data.sort_values(by='Co-occurence')

#Compute the 'co-occurence index' : 
Cooc_fracs = [ ]
for index, row in co_occerence_data.iterrows():
    Cooc_fracs.append(float(row['Co-occurence'])/(row['Tech_Count']*row['Chart_Count']))
co_occerence_data['Cooc_frac']=Cooc_fracs
Normed_Cooc_fracs = [ i/max(Cooc_fracs) for i in Cooc_fracs]
co_occerence_data['Normed_cooc']=Normed_Cooc_fracs 
co_occerence_data=co_occerence_data.sort_values(by='Normed_cooc',ascending=False)


#Make a new dataframe to focus on the top two most
#commonly occuring techs for each chart.
remade_cooc_df = pd.DataFrame()
for chart in high_count_chart_set : 
    for_this_chart = co_occerence_data.loc[co_occerence_data['Chart']==chart]
    top_tech = list(for_this_chart['Tech'])[0]
    second_tech = list(for_this_chart['Tech'])[1]
    techs_in_this = list(for_this_chart['Tech'])
    
    is_top_array = [ ]
    for k in techs_in_this :
        if k == top_tech :
            is_top_array.append(2)
        elif k == second_tech :
            is_top_array.append(1)
        else :
            is_top_array.append(0)
    
    for_this_chart['is_top_tech']=  is_top_array
    remade_cooc_df = remade_cooc_df.append(for_this_chart)
    
#Remove the chart tools we found that were not included in pairings.
remade_cooc_df=remade_cooc_df.loc[~remade_cooc_df['Tech'].isin(['Canvas','D3','Excel'])]

#Make the pivot table using a heat map:
piv=remade_cooc_df.pivot(index='Chart', columns='Tech', values='is_top_tech')
plt.rcParams['figure.figsize']=[10,10]
ax = sns.heatmap(piv, square=True,cmap='Blues',cbar=False)
plt.setp( ax.xaxis.get_majorticklabels(), rotation=90 )
plt.tight_layout()
plt.xlabel("")
plt.ylabel("")
plt.savefig("finding_right_tool_heatmap")







