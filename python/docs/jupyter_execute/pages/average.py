#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
os.environ["ATLASAPPROX_HIDECREDITS"] = "yes"
import atlasapprox

api = atlasapprox.API()


# In[2]:


import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


# In[3]:


avg_gene_expr_lung = api.average(
    organism='h_sapiens', 
    organ='lung', 
    features=['PRDM1', 'PTPRC', 'ACTB', 'GAPDH'],
    measurement_type='gene_expression'
)

# Set displayed pandas dataframe size
pd.set_option('display.max_rows', 10)       # Limit to 10 rows
pd.set_option('display.max_columns', 7)     # Limit to 7 columns

# display results
avg_gene_expr_lung


# In[4]:


# Create a figure with a specific size (width=8, height=4)
plt.figure(figsize=(8,4))

sns.heatmap(
        avg_gene_expr_lung, 
        # yellow-to-red color map
        cmap='YlOrRd', 
        # add label to calour bar
        cbar_kws={'label': 'Expression Level'}
)

# Customize labels
plt.title('Average gene expression across cell types in the human lung')
plt.xlabel('Cell types')
plt.ylabel('Genes')

# Keep gene names horizontal
plt.yticks(rotation=0)

# Prevent label cutoff
plt.tight_layout()

plt.show()


# In[5]:


# Define the target organs.
organ_list = ['bladder','blood','colon']

# create a dictionary to store each avg_gene_expr
avg_gene_expr_dic = {}

# Loop through organ_list and display the results
for organ in organ_list: 
    avg_gene_expr = api.average(
        organism='h_sapiens', 
        organ=organ, 
        features=['PRDM1', 'PTPRC', 'ACTB', 'GAPDH'],
    )

    # Store results into dictionary
    avg_gene_expr_dic[organ] = avg_gene_expr

    # Set up figure and display heatmap
    plt.figure(figsize=(6,2))
    plt.title(f'Average gene expression across cell types in the human {organ}')

    sns.heatmap(
        avg_gene_expr, 
        # yellow-to-red color map
        cmap='YlOrRd', 
        # add label to calour bar
        cbar_kws={'label': 'Expression Level'}
    )

    # Show the plot
    plt.show()


# In[6]:


similar_features = api.similar_features(
    organism='h_sapiens', 
    organ='lung', 
    feature='TP53',
    method='correlation',
    number=10
)

similar_features


# In[7]:


# Get average gene expression 
avg_similar_features = api.average(
    organism='h_sapiens',
    organ='lung',
    features=similar_features.index
)

# Display the heatmap
sns.heatmap(
    avg_similar_features, 
    # yellow-to-red color map
    cmap='YlOrRd', 
    # add label to calour bar
    cbar_kws={'label': 'Expression Level'}
)


# In[8]:


markers_in_human_lung_neu = api.markers(
    organism='h_sapiens', 
    organ='lung', 
    cell_type='neutrophil', 
    number=5
)

markers_in_human_lung_neu


# In[9]:


# Getting average gene expression for marker genes
avg_gene_expr_markers = api.average(
    organism='h_sapiens',
    organ='lung',
    features=markers_in_human_lung_neu
)

plt.figure(figsize=(8,2))

sns.heatmap(
    avg_gene_expr_markers, 
    # yellow-to-red color map
    cmap='YlOrRd', 
    # add label to calour bar
    cbar_kws={'label': 'Expression Level'}
)


# In[10]:


# Call log method in numpy to get all numbers logged
# add 1 to avoid "devide by 0"
avg_gene_expr_markers_log = np.log(avg_gene_expr_markers + 1)

# Display heatmap
plt.figure(figsize=(8,2))

sns.heatmap(
    avg_gene_expr_markers_log, 
    # yellow-to-red color map
    cmap='YlOrRd', 
    # add label to calour bar
    cbar_kws={'label': 'Expression Level'}
)

