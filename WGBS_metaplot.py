#!/usr/bin/python

import sys, getopt
import numpy as np
import seaborn as sns
import pandas as pd


def main(argv):
	bedfile = ''
	methfile = ''
	try:
		opts, args = getopt.getopt(argv,"hb:m:",["bed=","meth="])
	except getopt.GetoptError:
		print('Usage: WGBS_metaplot.py -b <bedfile> -m <methfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('Usage: WGBS_metaplot.py -b <bedfile> -m <methfile>')
			sys.exit()
		elif opt in ("-b", "--bed"):
			bedfile = arg
		elif opt in ("-m", "--meth"):
			methfile = arg
		if not opt:
			print('Usage: WGBS_metaplot.py -b <bedfile> -m <methfile>')
			sys.exit(2)
	print('bedfile is', bedfile)
	print('methfile is', methfile)

if __name__ == "__main__":
   main(sys.argv[1:])


np.seterr(invalid='ignore')

file = open(bedfile)

in_file1 = pd.read_csv(methfile, sep = "\t")
in_file2 = pd.read_csv(bedfile, sep = "\t", header=None)

meth_type = ["CG", "CHG", "CHH"]

initial = {}

bin_file = {}
C_total = {}
CT_total = {}

up_file = {}
up_C_total = {}
up_CT_total = {}

down_file = {}
down_C_total = {}
down_CT_total = {}

all_df_methlevel = pd.DataFrame()
all_df_upmethlevel = pd.DataFrame()
all_df_downmethlevel = pd.DataFrame()

track = 0

for line in file: 
    line = line.rstrip()
    elements = line.split("\t")
    length = int(elements[2]) - int(elements[1]) + 1
    bin_size = length / 20
    for methtype in meth_type:
        methlevel = {}
        up_methlevel = {}
        down_methlevel = {}
        for i in range(1, 21):
            if (elements[6] == '+'): 
                bin_file[elements[3], methtype, i] = in_file1.loc[(in_file1['context'] == methtype) & (in_file1['pos'].astype(int) > int(elements[1])+bin_size*(i-1)) & (in_file1['pos'].astype(int) <= int(elements[1])+bin_size*(i))]
                C_total[elements[3], methtype, i] = bin_file[elements[3], methtype, i]['C_count'].sum()
                CT_total[elements[3], methtype, i] = bin_file[elements[3], methtype, i]['eff_CT_count'].sum()
                methlevel[elements[3], methtype, i] = C_total[elements[3], methtype, i] / CT_total[elements[3], methtype, i]
                methlevel_values = methlevel.values()
                methlevel_list = list(methlevel_values)
                df_methlevel = pd.DataFrame(methlevel_list).T
            else: 
                bin_file[elements[3], methtype, i] = in_file1.loc[(in_file1['context'] == methtype) & (in_file1['pos'].astype(int) < int(elements[2])-bin_size*(i-1)) & (in_file1['pos'].astype(int) >= int(elements[1])-bin_size*(i))]
                C_total[elements[3], methtype, i] = bin_file[elements[3], methtype, i]['C_count'].sum()
                CT_total[elements[3], methtype, i] = bin_file[elements[3], methtype, i]['eff_CT_count'].sum()
                methlevel[elements[3], methtype, i] = C_total[elements[3], methtype, i] / CT_total[elements[3], methtype, i]
                methlevel_values = methlevel.values()
                methlevel_list = list(methlevel_values)
                df_methlevel = pd.DataFrame(methlevel_list).T
        all_df_methlevel = all_df_methlevel.append(df_methlevel, ignore_index = True)
        for i in range(1, 21):
            if (elements[6] == '+'): 
                up_file[elements[3], methtype, i] = in_file1.loc[(in_file1['context'] == methtype) & (in_file1['pos'].astype(int) > int(elements[1])-1000+50*(i-1)) & (in_file1['pos'].astype(int) <= int(elements[1])-1000+50*i)]
                up_C_total[elements[3], methtype, i] = up_file[elements[3], methtype, i]['C_count'].sum()
                up_CT_total[elements[3], methtype, i] = up_file[elements[3], methtype, i]['eff_CT_count'].sum()
                up_methlevel[elements[3], methtype, i] = up_C_total[elements[3], methtype, i] / up_CT_total[elements[3], methtype, i]
                up_methlevel_values = up_methlevel.values()
                up_methlevel_list = list(up_methlevel_values)
                df_up_methlevel = pd.DataFrame(up_methlevel_list).T
            else: 
                up_file[elements[3], methtype, i] = in_file1.loc[(in_file1['context'] == methtype) & (in_file1['pos'].astype(int) < int(elements[2])+1000-50*(i-1)) & (in_file1['pos'].astype(int) >= int(elements[2])+1000-50*i)]
                up_C_total[elements[3], methtype, i] = up_file[elements[3], methtype, i]['C_count'].sum()
                up_CT_total[elements[3], methtype, i] = up_file[elements[3], methtype, i]['eff_CT_count'].sum()
                up_methlevel[elements[3], methtype, i] = up_C_total[elements[3], methtype, i] / up_CT_total[elements[3], methtype, i]
                up_methlevel_values = up_methlevel.values()
                up_methlevel_list = list(up_methlevel_values)
                df_up_methlevel = pd.DataFrame(up_methlevel_list).T 
        all_df_upmethlevel = all_df_upmethlevel.append(df_up_methlevel, ignore_index = True)
        for i in range(1, 21):
            if (elements[6] == '+'): 
                down_file[elements[3], methtype, i] = in_file1.loc[(in_file1['context'] == methtype) & (in_file1['pos'].astype(int) > int(elements[2])+50*(i-1)) & (in_file1['pos'].astype(int) <= int(elements[2])+50*i)]
                down_C_total[elements[3], methtype, i] = down_file[elements[3], methtype, i]['C_count'].sum()
                down_CT_total[elements[3], methtype, i] = down_file[elements[3], methtype, i]['eff_CT_count'].sum()
                down_methlevel[elements[3], methtype, i] = down_C_total[elements[3], methtype, i] / down_CT_total[elements[3], methtype, i]
                down_methlevel_values = down_methlevel.values()
                down_methlevel_list = list(down_methlevel_values)
                df_down_methlevel = pd.DataFrame(down_methlevel_list).T
            else: 
                down_file[elements[3], methtype, i] = in_file1.loc[(in_file1['context'] == methtype) & (in_file1['pos'].astype(int) < int(elements[1])-50*(i-1)) & (in_file1['pos'].astype(int) >= int(elements[1])-50*i)]
                down_C_total[elements[3], methtype, i] = down_file[elements[3], methtype, i]['C_count'].sum()
                down_CT_total[elements[3], methtype, i] = down_file[elements[3], methtype, i]['eff_CT_count'].sum()
                down_methlevel[elements[3], methtype, i] = down_C_total[elements[3], methtype, i] / down_CT_total[elements[3], methtype, i]
                down_methlevel_values = down_methlevel.values()
                down_methlevel_list = list(down_methlevel_values)
                df_down_methlevel = pd.DataFrame(down_methlevel_list).T
        all_df_downmethlevel = all_df_downmethlevel.append(df_down_methlevel, ignore_index = True)
        
        initial[elements[3], methtype, i] = [elements[0], elements[1], elements[2], elements[3], elements[6], methtype]
        df_initial = pd.DataFrame.from_dict(initial, orient='index', columns = ['Chr', 'Start', 'End', 'Gene', 'Strand', 'Type'])
    track += 1
    if (track % 10 == 0):
        print("Lines that are completed: ", track)

df_r = df_initial.reset_index(drop=True)
merged = pd.concat([all_df_upmethlevel, all_df_methlevel, all_df_downmethlevel], axis=1)
final = pd.concat([df_r, merged], axis=1)

CG_file = final[final['Type'].str.contains('CG')]
CHG_file = final[final['Type'].str.contains('CHG')]
CHH_file = final[final['Type'].str.contains('CHH')]

CG_mean_list = []
CHG_mean_list = []
CHH_mean_list = []

for i in range(7, 67):
    CG_mean = CG_file.iloc[:, i].mean()
    CG_mean_list.append(CG_mean)
    df_CG_mean = pd.DataFrame(CG_mean_list).T

for i in range(7, 67):
    CHG_mean = CHG_file.iloc[:, i].mean()
    CHG_mean_list.append(CHG_mean)
    df_CHG_mean = pd.DataFrame(CHG_mean_list).T

for i in range(7, 67):
    CHH_mean = CHH_file.iloc[:, i].mean()
    CHH_mean_list.append(CHH_mean)
    df_CHH_mean = pd.DataFrame(CHH_mean_list).T
    
alldata = pd.concat([df_CG_mean, df_CHG_mean, df_CHH_mean], ignore_index = True)
alldata_t = alldata.T
alldata_t.columns =['CG', 'CHG', 'CHH']

final.to_csv("methylation_level_of_genes.txt", sep='\t', index=True)
p = sns.lineplot(data = alldata_t)
fig = p.get_figure()
fig.savefig("result_plot.pdf")

