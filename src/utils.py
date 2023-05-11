# %%
import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 

# %%
def my_histogram(df, column_name):
    fig, (ax_box, ax_hist) = plt.subplots(2, sharex = True, gridspec_kw = {"height_ratios": (.2, .8)}, figsize = (10, 7))

    sns.boxplot(x = df[column_name], ax = ax_box, showfliers = False)
    sns.histplot(x = df[column_name], ax = ax_hist, kde = True)

    plt.grid()
    plt.xlabel(column_name, fontsize = 16)
    plt.ylabel("Count", fontsize = 16)
    ax_box.set_xlabel("")

    plt.show()
    
# %%
def make_stacked_table(df, target_col, y, dummy_col):
    res_tab = df.groupby([target_col, y]).count()[dummy_col].unstack().reset_index()
    res_tab = res_tab.rename_axis(None, axis = 1)
    
    y_val_1 = df["Outcome"].unique()[0]
    y_val_2 = df["Outcome"].unique()[1]
    
    # res_tab.rename(columns = {y_val_1: str(y_val_1), 
    #                           y_val_2: str(y_val_2)}, inplace = True)
    
    res_tab["total"] = res_tab[y_val_1] + res_tab[y_val_1]
    res_tab["ratio"] = np.round(res_tab[y_val_2] / res_tab.total, 2)
    res_tab = res_tab.sort_values("total", ascending = False)
    res_tab = res_tab.reset_index().drop("index", axis = 1)

    return res_tab

# %%
def my_stacked_barplot(stacked_table, target_col, y, stacked_col,
                       x_start_coord = -0.05, y_coord = 100):
    plt.figure(figsize = (14, 8))
    
    # bar graph for total observations
    color = "darkblue"
    ax1 = sns.barplot(x = target_col, y = "total", color = color, alpha = 0.8, \
                      data = stacked_table)
    top_bar = mpatches.Patch(color = color, label = 'Num of total observations')
    
    # bar graph for stacked column
    color = "lightblue"
    ax2 = sns.barplot(x = target_col, y = stacked_col,  color = color, alpha = 0.8, \
                      data = stacked_table)
    ax2.set_xlabel(target_col, fontsize = 16)
    ax2.set_ylabel("Number of observations", fontsize = 16)
    low_bar = mpatches.Patch(color = color, label = f'Num of {y} = {stacked_col} observations')
    
    # ratio
    x_coord = x_start_coord
    
    for i in range(stacked_table.shape[0]):
        s = round(stacked_table.ratio[i] * 100)
        plt.text(s = f"{s}%", x = x_coord, y = y_coord, fontsize = 16)

        x_coord += 1

    plt.legend(handles=[top_bar, low_bar])
    plt.show()