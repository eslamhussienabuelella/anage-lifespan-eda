# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 01:37:16 2025

@author: agno3
"""


# Do lab work sheet 7 & 8 before it

# Task 3

# Import necessary libraries (pandas, matplotlib/seaborn)
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# import/read the AnAge dataset as dataframe
raw_anage = pd.read_csv("anage.txt", sep="\t") 
print(raw_anage)
# Familirise my self with data ==> (EDA)
# Define data frame shape
print("\nDataFrame shape==>",raw_anage.shape)
# Define data frame columns
print("\nDataFrame Columns")
print(raw_anage.columns)

# Subset Task 3 relevant columns
anage = raw_anage[["Kingdom", "Class", 
                   "Common name", "Adult weight (g)", 
                   "Maximum longevity (yrs)"]]
# Checking data types
print("\nDataFrame Columns data types")
print(anage.dtypes)

# Exploring the categorical variables 
print("\nKingdom\n",anage["Kingdom"].unique())
print("\nNo of Kingdoms ==>",anage["Kingdom"].nunique())
print("\nClass\n",anage["Class"].unique())
print("\nNo of Classes ==>",anage["Class"].nunique())
print("\nCommon name\n",anage["Common name"].unique())
print("\nNo of Common names ==>",anage["Common name"].nunique())
# Summary statistics of quatitative variables
print("\nDataFrame description (summary statistics) Quntitative")
print(anage.describe())
# Investigate extreme values from summary statistics
# minimum life span of an organism that lives for 0.01 years?? 
# maximum life span of an organism that lives for 15000 years?? 
print("\n\n",anage[(anage["Maximum longevity (yrs)"] == 15000.000000) |
                 (anage["Maximum longevity (yrs)"] == 0.010)]
                   [["Class","Common name", "Maximum longevity (yrs)"]])

# print(anage.query("`Maximum longevity (yrs)` == 15000"))
# there maximum adult weight of an organism 136 tons??
print("\n\n",anage[(anage["Adult weight (g)"] == 1.360000e+08) | 
            (anage["Adult weight (g)"] == 5.000000e-01)]
              [["Class", "Common name","Adult weight (g)"]])



# inspect if there is null in the dataframe
print("\nDataFrame info")
print(anage.info())

# find the dataframe length to compare after filterin out the data
print(len(anage))

########################### Task 3 (a) ###########################
print("########################### Task 3 (a) ###########################")
########################### Shorter Approach ###########################
print("########################### Shorter Approach ###########################")

# To create a summary table we can go ahead directly with this very short code  or follow the upcoming detailed approach
anage_filtered = (anage[(anage["Kingdom"] == "Animalia")&
                       (anage["Maximum longevity (yrs)"]
                        .notna())].groupby("Class")["Common name"]
                          .count().sort_values(ascending=False))
print(anage_filtered)

########################### Detailed Approach ###########################
print("########################### Detailed Approach ###########################")
animalia_df  = anage.query("Kingdom == 'Animalia'")
animalia_max_long_df  = animalia_df.dropna(subset=["Maximum longevity (yrs)"])
print(animalia_max_long_df.dropna(subset=["Adult weight (g)"]).info())
# Group the filtered dataset by animal Class
class_grouped  = animalia_max_long_df.groupby("Class")
# Count the number of common names for each Class
names_per_class = class_grouped["Common name"].count()
# Sort the the summary table in descending order to identify Classes with the most species
sorted_common_names_table = names_per_class.sort_values(ascending=False)
print(sorted_common_names_table)

########################### Bar chart by Detailed Approach ###########################
print("########################### Bar chart by Detailed Approach ###########################")

plt.figure()
sorted_common_names_chart = names_per_class.sort_values()
# Generate colour palette by seaborn
colors = sns.color_palette("Blues", len(sorted_common_names_chart))
sorted_common_names_chart.plot.barh(color=colors)
plt.title("Number of Species per Class with Longevity Data")
# Add labels using a for loop and iloc / .index
for i in range(len(sorted_common_names_chart)):
    value = sorted_common_names_chart.iloc[i]
    label = sorted_common_names_chart.index[i]
    plt.text(value + 0.1, i, value, va = 'center', fontsize=9)
plt.ylabel("Classes")
plt.xlabel("Number of Species")
plt.xscale('log')

plt.xlim(0, sorted_common_names_table.max() + 1000)
plt.show()



########################### Task 3 (b) ###########################
print("########################### Task 3 (b) ###########################")

# preparing the data of top 4 classes 

# check dataframe if it has any nulls 
print(animalia_max_long_df.info())

scatter_df = animalia_max_long_df[animalia_max_long_df["Class"].isin(sorted_common_names_table.head(4).index)]
print(scatter_df.info())

# Drop the NaN from Adults weight

# animalia_max_long_df.dropna(subset=["Adult weight (g)"]
scatter_df = scatter_df.dropna(subset=["Adult weight (g)"])
print(scatter_df.info())

##################################### All classes charts ####################################


# Generally we will plot all the 4 classes on the same scatter plot together to explore what we have


# Sort the DataFrame once by adult weight and once by maximum longevity
scatter_df_age_sorted=scatter_df.sort_values(by=[ "Maximum longevity (yrs)"], ascending=False)
scatter_df_weight_sorted=scatter_df.sort_values(by=[ "Adult weight (g)"], ascending=False)
# Extract the data points that will be annotated in the plot
scatter_labels_df = pd.concat([scatter_df_age_sorted.head(3),
                       scatter_df_weight_sorted.head(3),
                       scatter_df_age_sorted.tail(3),
                       scatter_df_weight_sorted.tail(3)]).drop_duplicates()



# dreate the figure canvas and define the subplots layout 
fig=plt.figure(figsize=(12,6)) #
ax0=fig.add_subplot(1,2,1)
ax1=fig.add_subplot(1,2,2)

# draw the exploratory box plot to visualise data distribution
scatter_df.plot.box(ax=ax0)
ax0.set_yscale("log")
ax0.set_title("Quatitative variable disribution")


# label the highest longevity outlier across all classes 
ax0.text(x=2.05, y=scatter_df.sort_values(by=["Maximum longevity (yrs)"], 
        ascending=False).iloc[0]["Maximum longevity (yrs)"], 
        s=scatter_df.sort_values(by=["Maximum longevity (yrs)"], 
        ascending=False).iloc[0]["Common name"], fontsize=8, color="r")

# label the highest weight outlier across all classes
ax0.text(x=1.05,y=scatter_df.sort_values(by=["Adult weight (g)"], 
         ascending=False).iloc[0]["Adult weight (g)"], 
         s=scatter_df.sort_values(by=["Adult weight (g)"], 
         ascending=False).iloc[0]["Common name"], fontsize=8, color="r")

# draw the scatter plot for top 4 classes with unique colour & marker for each class
sns.scatterplot(data=scatter_df,
    x="Adult weight (g)",
    y="Maximum longevity (yrs)",
    hue="Class",
    style="Class",
    alpha=0.4,
    ax=ax1)
ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.grid(True, which="both", linestyle='--', linewidth=0.2)

# loop to labele top 3 and bottom 3 species in each variable
for i in range(len(scatter_labels_df)):
    ax1.text((scatter_labels_df.iloc[i]["Adult weight (g)"])*1.05,
              (scatter_labels_df.iloc[i]["Maximum longevity (yrs)"])*1.05,
              scatter_labels_df.iloc[i]["Common name"],
              fontsize=6)
# general plot formating
ax1.set_title("Longevity vs. Adult Weight (Top 4 Classes) 1")
ax1.set_xlabel("Adult Weight (g) [log scale]")
ax1.set_ylabel("Maximum Longevity (yrs) [log scale]")
ax1.legend(loc='lower right')
plt.show()


# plt.figure() 
# sns.scatterplot(data=scatter_df,
#     x="Adult weight (g)",
#     y="Maximum longevity (yrs)",
#     hue="Class",
#     style="Class",
#     alpha=0.4)
# plt.xscale("log")
# plt.yscale("log")
# plt.grid(True, which="both", linestyle='--', linewidth=0.2)
# for i in range(len(labels_df)):
#     plt.text((labels_df.iloc[i]["Adult weight (g)"])*1.05,
#               (labels_df.iloc[i]["Maximum longevity (yrs)"])*1.05,
#               labels_df.iloc[i]["Common name"],
#               fontsize=6)
# plt.title("Longevity vs. Adult Weight (Top 4 Classes) 1")
# plt.xlabel("Adult Weight (g) [log scale]")
# plt.ylabel("Maximum Longevity (yrs) [log scale]")
# plt.show()


for animal_class in scatter_df["Class"].unique():
    plotting_df = scatter_df[scatter_df["Class"]== animal_class]
    plotting_df_stats = plotting_df.describe()
    min_age = plotting_df_stats.loc["min", "Maximum longevity (yrs)"]
    min_weight = plotting_df_stats.loc["min", "Adult weight (g)"]
    print(min_age)
    LQ_weight = plotting_df_stats.loc["25%", "Adult weight (g)"]
    LQ_years = plotting_df_stats.loc["25%", "Maximum longevity (yrs)"]

    UQ_weight = plotting_df_stats.loc["75%", "Adult weight (g)"]
    UQ_years = plotting_df_stats.loc["75%", "Maximum longevity (yrs)"]

    LQR_weight = UQ_weight - LQ_weight
    LQR_years = UQ_years - LQ_years

    low_limit_weight = LQ_weight - (1.5* LQR_weight)
    high_limit_weight = UQ_weight + (1.5* LQR_weight)
    low_limit_years = LQ_years - (1.5* LQR_years)
    high_limit_years = UQ_years + (1.5* LQR_years)
    fig=plt.figure(figsize=(12,6)) #
    ax0=fig.add_subplot(1,2,1)
    ax1=fig.add_subplot(1,2,2)
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.axvline(high_limit_weight, color="c", linestyle="--",linewidth=0.8)
    ax1.axhline(high_limit_years, color="m", linestyle="--",linewidth=0.8)

    ax1.text(high_limit_weight * 1.05, min_age, "Weight outliers upper limit", fontsize=7.5, rotation=90, color="k")

    # Label horizontal line (above the line)
    ax1.text(min_weight, high_limit_years * 1.1, "Age outliers upper limit",fontsize=7.5,  color="k")

    age_wheight_outliers = plotting_df[(plotting_df["Maximum longevity (yrs)"]>high_limit_years) & #>>
                             (plotting_df["Adult weight (g)"]>high_limit_weight)]
    non_outliers = plotting_df[(plotting_df["Maximum longevity (yrs)"]<high_limit_years) & #<<
                              (plotting_df["Adult weight (g)"]<high_limit_weight)]
    
    age_outliers = plotting_df[(plotting_df["Maximum longevity (yrs)"]>high_limit_years) & #><
                              (plotting_df["Adult weight (g)"]<high_limit_weight)]
   
    wheight_outliers = plotting_df[(plotting_df["Maximum longevity (yrs)"]<high_limit_years) & #<>
                              (plotting_df["Adult weight (g)"]>high_limit_weight)]

    plotting_df.plot.box(ax=ax0)
    
    # plotting the non-outliers on the scatter plot
    non_outliers.plot.scatter("Adult weight (g)","Maximum longevity (yrs)", s=0.5, color ="g", ax=ax1)
    # plotting the weight & age outliers on the scatter plot
    age_wheight_outliers.plot.scatter("Adult weight (g)","Maximum longevity (yrs)", s=0.5, color ="r", ax=ax1)
    # plotting the weight & age outliers on the scatter plot
    age_outliers.plot.scatter("Adult weight (g)","Maximum longevity (yrs)", s=0.5, color ="b", ax=ax1)
    # plotting the weight & age outliers on the scatter plot
    wheight_outliers.plot.scatter("Adult weight (g)","Maximum longevity (yrs)", s=0.5, color ="k", ax=ax1)
    
    age_sorted_plotting_df = plotting_df.sort_values(by=["Maximum longevity (yrs)"])
    weight_sorted_plotting_df = plotting_df.sort_values(by=["Adult weight (g)"])
    age_wheight_outliers_sorted= pd.concat([age_sorted_plotting_df.head(3),
                                            age_sorted_plotting_df.tail(3),
                                            weight_sorted_plotting_df.head(3),
                                            weight_sorted_plotting_df.tail(3)]).drop_duplicates()

    # label extreme outliers on the scatter plot
    for i in range(len(age_wheight_outliers_sorted)):
        ax1.text((age_wheight_outliers_sorted.iloc[i]["Adult weight (g)"])*1.05,
                  (age_wheight_outliers_sorted.iloc[i]["Maximum longevity (yrs)"])*1.05,
                  age_wheight_outliers_sorted.iloc[i]["Common name"],
                  fontsize=6)
    # label extreme age outliers on the box plot
    ax0.text(x=2.05, y=age_wheight_outliers_sorted.sort_values(by=["Maximum longevity (yrs)"]
            , ascending=False).iloc[0]["Maximum longevity (yrs)"]
            , s=age_wheight_outliers_sorted.sort_values(by=["Maximum longevity (yrs)"]
            , ascending=False).iloc[0]["Common name"], fontsize=8, color="r")
    # label extreme weight outliers on the box plot

    ax0.text(x=1.05, y=age_wheight_outliers_sorted.sort_values(by=["Adult weight (g)"]
            , ascending=False).iloc[0]["Adult weight (g)"]
            , s=age_wheight_outliers_sorted.sort_values(by=["Adult weight (g)"]
            , ascending=False).iloc[0]["Common name"], fontsize=8, color="r")
    
    ax0.set_yscale("log")
    # set title for the scater plot (subplot 1)
    ax1.set_title("Adult weight (g) Vs. Maximum longevity (yrs)")
    # set title for the box plot (subplot 2)
    ax0.set_title("Adult weight & Maximum longevity distribution")
    # set title for the whole figure
    fig.suptitle(animal_class)
    plt.legend(("Weight outlier threshold","Age outlier threshold","Non outliers","Comobined outliers","Age outliers","Weight outliers"),loc="center left", bbox_to_anchor=(0.85, 0.15), fontsize=8,borderaxespad=0)
    plt.show()

    # validate the data output
    print(age_wheight_outliers_sorted[["Common name","Adult weight (g)","Maximum longevity (yrs)"]].sort_values(by=["Adult weight (g)"], ascending=False).head())
    
    print(age_wheight_outliers_sorted[["Common name","Adult weight (g)","Maximum longevity (yrs)"]].sort_values(by=["Maximum longevity (yrs)"], ascending=False).head())
    
    
    print(age_wheight_outliers_sorted[["Common name","Adult weight (g)","Maximum longevity (yrs)"]].sort_values(by=["Adult weight (g)"], ascending=False).tail())
    
    print(age_wheight_outliers_sorted[["Common name","Adult weight (g)","Maximum longevity (yrs)"]].sort_values(by=["Maximum longevity (yrs)"], ascending=False).tail())




# Backup code
# for animal_class in scatter_df["Class"].unique():
#     plotting_df = scatter_df[scatter_df["Class"]== animal_class]
#     plotting_df_stats = plotting_df.describe()
#     min_age = plotting_df_stats.loc["min", "Maximum longevity (yrs)"]
#     min_weight = plotting_df_stats.loc["min", "Adult weight (g)"]
#     print(min_age)
#     LQ_weight = plotting_df_stats.loc["25%", "Adult weight (g)"]
#     LQ_years = plotting_df_stats.loc["25%", "Maximum longevity (yrs)"]

#     UQ_weight = plotting_df_stats.loc["75%", "Adult weight (g)"]
#     UQ_years = plotting_df_stats.loc["75%", "Maximum longevity (yrs)"]

#     LQR_weight = UQ_weight - LQ_weight
#     LQR_years = UQ_years - LQ_years

#     low_limit_weight = LQ_weight - (1.5* LQR_weight)
#     high_limit_weight = UQ_weight + (1.5* LQR_weight)
#     low_limit_years = LQ_years - (1.5* LQR_years)
#     high_limit_years = UQ_years + (1.5* LQR_years)
#     fig=plt.figure(figsize=(12,6)) #
#     ax0=fig.add_subplot(1,2,1)
#     ax1=fig.add_subplot(1,2,2)
    
#     # plotting_df.plot.scatter("Adult weight (g)","Maximum longevity (yrs)", s=0.25, color ="b", ax=ax1)
#     ax1.set_xscale("log")
#     ax1.set_yscale("log")
#     ax1.axvline(high_limit_weight, color="m", linestyle="--",linewidth=0.8)
#     ax1.axhline(high_limit_years, color="m", linestyle="--",linewidth=0.8)
#     # ax1.axvline(low_limit_weight, color="k", linestyle="--",linewidth=0.8)
#     # ax1.axhline(low_limit_years, color="g", linestyle="--",linewidth=0.8)
#     ax1.text(high_limit_weight * 1.05, min_age, "Weight outliers upper limit", fontsize=7.5, rotation=90, color="k")

#     # Label horizontal line (above the line)
#     ax1.text(min_weight, high_limit_years * 1.1, "Age outliers upper limit",fontsize=7.5,  color="k")
#     # ax1.set_xlim(-10000,10000)
#     # ax1.set_ylim(-10000,10000)
#     age_wheight_outliers = plotting_df[(plotting_df["Maximum longevity (yrs)"]>high_limit_years) & #>>
#                              (plotting_df["Adult weight (g)"]>high_limit_weight)]
#     non_outliers = plotting_df[(plotting_df["Maximum longevity (yrs)"]<high_limit_years) & #<<
#                               (plotting_df["Adult weight (g)"]<high_limit_weight)]
    
    
#     # non_outliers = plotting_df[(plotting_df["Maximum longevity (yrs)"]<high_limit_years) & #<<
#     #                          (plotting_df["Adult weight (g)"]<high_limit_weight)]
    
#     age_outliers = plotting_df[(plotting_df["Maximum longevity (yrs)"]>high_limit_years) & #><
#                               (plotting_df["Adult weight (g)"]<high_limit_weight)]
   
#     wheight_outliers = plotting_df[(plotting_df["Maximum longevity (yrs)"]<high_limit_years) & #<>
#                               (plotting_df["Adult weight (g)"]>high_limit_weight)]
    
#     # outliers_lables = outliers["Common name"]

#     # plotting the boxplot
#     plotting_df.plot.box(ax=ax0)
    
#     # plotting the non-outliers on the scatter plot
#     non_outliers.plot.scatter("Adult weight (g)","Maximum longevity (yrs)", s=0.5, color ="g", ax=ax1)
#     # plotting the weight & age outliers on the scatter plot
#     age_wheight_outliers.plot.scatter("Adult weight (g)","Maximum longevity (yrs)", s=0.5, color ="r", ax=ax1)
#     # plotting the weight & age outliers on the scatter plot
#     age_outliers.plot.scatter("Adult weight (g)","Maximum longevity (yrs)", s=0.5, color ="b", ax=ax1)
#     # plotting the weight & age outliers on the scatter plot
#     wheight_outliers.plot.scatter("Adult weight (g)","Maximum longevity (yrs)", s=0.5, color ="k", ax=ax1)
    
#     age_sorted_plotting_df = plotting_df.sort_values(by=["Maximum longevity (yrs)"])
#     weight_sorted_plotting_df = plotting_df.sort_values(by=["Adult weight (g)"])
    
    
#     # # find the highest outlier in both sorted by age
#     # age_sorted_outliers = (age_wheight_outliers.sort_values(by=[ "Maximum longevity (yrs)"], ascending=False)).head(2)
#     # # find the highest outlier in both sorted by weight 
#     # weight_sorted_outliers = (age_wheight_outliers.sort_values(by=["Adult weight (g)"], ascending=False)).head(2)
#     # # find the the highest weight outlier 
#     # weight_only_sorted_outliers = (wheight_outliers.sort_values(by=["Adult weight (g)"], ascending=False)).head(2)
#     # # find the the highest age outlier 
#     # age_only_sorted_outliers = (age_outliers.sort_values(by=["Maximum longevity (yrs)"], ascending=False)).head(2)

#     # # find the highest outlier in both sorted by age
#     # age_sorted_non_outliers = (non_outliers.sort_values(by=[ "Maximum longevity (yrs)"])).head(2)
#     # # find the highest outlier in both sorted by weight 
#     # weight_sorted_non_outliers = (non_outliers.sort_values(by=["Adult weight (g)"])).head(2)

#     # remove duplicates
#     # age_wheight_outliers_sorted= pd.concat([age_sorted_non_outliers,weight_sorted_non_outliers,age_sorted_outliers, weight_sorted_outliers,weight_only_sorted_outliers,age_only_sorted_outliers]).drop_duplicates()
#     age_wheight_outliers_sorted= pd.concat([age_sorted_plotting_df.head(3),age_sorted_plotting_df.tail(3),
#                                             weight_sorted_plotting_df.head(3),weight_sorted_plotting_df.tail(3)]).drop_duplicates()

#     # label extreme outliers on the scatter plot (top 5 without duplication)
#     for i in range(len(age_wheight_outliers_sorted)):
#         ax1.text((age_wheight_outliers_sorted.iloc[i]["Adult weight (g)"])*1.05,
#                   (age_wheight_outliers_sorted.iloc[i]["Maximum longevity (yrs)"])*1.05,
#                   age_wheight_outliers_sorted.iloc[i]["Common name"],
#                   fontsize=6)
        
#     ax0.text(
#     x=2.05,  # x-position just to the right of box 2 (index=1)
#     y=age_wheight_outliers_sorted.sort_values(by=["Maximum longevity (yrs)"], ascending=False).iloc[0]["Maximum longevity (yrs)"],
#     s=age_wheight_outliers_sorted.sort_values(by=["Maximum longevity (yrs)"], ascending=False).iloc[0]["Common name"],
#     fontsize=8,
#     color="r")
    
#     ax0.text(
#     x=1.05,  # x-position just to the right of box 2 (index=1)
#     y=age_wheight_outliers_sorted.sort_values(by=["Adult weight (g)"], ascending=False).iloc[0]["Adult weight (g)"],
#     s=age_wheight_outliers_sorted.sort_values(by=["Adult weight (g)"], ascending=False).iloc[0]["Common name"],
#     fontsize=8,
#     color="r")
#     # age_outliers.plot.scatter("Adult weight (g)","Maximum longevity (yrs)", s=0.25, color ="g", ax=ax1)
#     # wheight_outliers.plot.scatter("Adult weight (g)","Maximum longevity (yrs)", s=0.25, color ="m", ax=ax1)

    

#     ax0.set_yscale("log")
    
    
#     # set title for the scater plot (subplot 1)
#     ax1.set_title("Adult weight (g) Vs. Maximum longevity (yrs)")
#     # set title for the box plot (subplot 2)
#     ax0.set_title("Adult weight & Maximum longevity distribution")
    
#     # set title for the whole figure
#     fig.suptitle(animal_class)
#     # fig.suptitle(("Adult weight (g) Vs. Max longevity (yrs) for", animal_class, " and their box plots"))
#     plt.show()

