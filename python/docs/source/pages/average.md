# Exploring average gene expression

Investigating cell atlases often involves exploring gene expression patterns across different cell types and organs. 
This tutorial guides you through using the [atlasapprox API](https://atlasapprox.readthedocs.io/en/latest/python/index.html)
to explore gene expression data effectively. You will gain a general idea of how to query average expression, discover 
patterns of similar genes, identify marker genes, and visualize the data.

### Contents

- [Querying average expression data for a single organ](#querying-average-expression-data-for-a-single-organ)
- [Querying expression data for multiple organs](#querying-expression-data-for-multiple-organs)
- [Identifying expression patterns of similar genes](#identifying-expression-patterns-of-similar-genes)
- [Querying expression data for marker genes](#querying-expression-data-for-marker-genes)


### Initialize the API
To begin, import the *atlasapprox* Python package and create an API object:

```{jupyter-execute}
import os
os.environ["ATLASAPPROX_HIDECREDITS"] = "yes"
import atlasapprox

api = atlasapprox.API()
```

For complete setup instructions, see the [Quick Start Tutorial](https://github.com/Amber-Xu914/atlasapprox_api_tutorials/blob/main/python/quick_start.ipynb).

### Required packages
To follow along with the data visualization in this tutorial, first install the following packages using `pip`, and then import them by running this command in your terminal or Jupyter notebook:

```{jupyter-execute}
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
```

## **Querying average expression data for a single organ**
<a id="querying-average-expression-data-for-a-single-organ"></a>

The `average` method allows you to retrieve average gene expression of selected genes across cell types within a specific organ of a species. 

Use the following code to get the average gene expression data for four exmaple genes (*PRDM1*, *PTPRC*, *ACTB*, *GAPDH*) in the human lung across cell types:

```{jupyter-execute}
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

```

#### Output
This method returns a *Pandas DataFrame* where:

* Each row represents a gene.
* Each column corresponds to a cell type.
* The values indicate the average gene expression, measured in counts per ten thousand (cptt).

### Visualizing the data

To visualize the average expression data of the queried genes, a heatmap is an effective starting point. The Python visualization libraries [Seaborn](https://seaborn.pydata.org/) and [Matplotlib](https://matplotlib.org/) offer powerful tools for creating such heatmaps. 

Here is a way to create one using Seaborn's `heatmap` method with custom colours and labels:

```{jupyter-execute}
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
```
From the color gradient, it is easier to compare the expression levels across different cell types. By looking at the heatmap, it is clear that *ACTB* exhibits consistently high gene expression across all cell types compared to the other genes. In contrast, *PRDM1* shows very low expression overall.

## **Querying expression data for multiple organs**
<a id="querying-expression-data-for-multiple-organs"></a>

The following example demonstrates the average gene expression of four genes (same as above) across three human organs (*bladder*, *blood*, and *colon*).

*Atlasapprox* API doesn't have any method to explore multiple organs at the same time, you can use the following code to make a for loop. At the same time, a plotted data always better then numbers, try to call sns `heatmap` to display the data:
```{jupyter-execute}
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
```
By comparing these three heatmaps, *ACTB* exhibits consistently high expression across all the selected organs, indicating a similar expression pattern among them.

## **Identifying expression patterns of similar genes**
<a id="identifying-expression-patterns-of-similar-genes"></a>

When you have a gene of interest, you might want to find genes with similar expression patterns. This example shows you how to use the `similar_features` method to retrieve the top 10 genes with expression patterns similar to *TP53* in the human lung:
```{jupyter-execute}
similar_features = api.similar_features(
    organism='h_sapiens', 
    organ='lung', 
    feature='TP53',
    method='correlation',
    number=10
)

similar_features
```
#### Output

`similar_features` returns a *pandas.Series* where the **index** contains gene names, and the corresponding **data** represents their distance to *TP53*.

In this series, the **Pearson correlation** method is used to calculate the distance. This method produces a value between -1 and 1, where -1 signifies a perfect negative linear relationship, and 1 signifies a perfect positive linear relationship. From the resulting pandas.Series, the top 10 genes with the greatest similarity to *TP53* all exhibit positive linear relationships, with *TRA2A* showing the highest similarity. These genes may potentially be co-regulated with *TP53*.

Additionally, `similar_features` supports the following methods for distance calculation:
- **cosine**: Computes cosine similarity/distance based on the fraction detected.
- **euclidean**: Measures Euclidean distance based on average measurements (e.g., expression levels).
- **manhattan**: Calculates the taxicab/Manhattan/L1 distance of average measurements.
- **log-euclidean**: Applies a logarithmic transformation to the average measurement (with a pseudocount of 0.001) before calculating the Euclidean distance, which highlights sparsely measured features.

### Get average gene expression for similar features

You can then use the `average` method to retrieve the average gene expression of these similar genes. Use **similar_features.index** to extract the gene names returned by `similar_features`, and pass them as the parameter (features) to the `average` method. 

You can either use `print` method to directly display the resulting *pandas.DataFrame*, or, as shown in the example below, use Seaborn’s `heatmap` method to present a more intuitive graphical representation:

```{jupyter-execute}
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
```

## **Querying expression data for marker genes**
<a id="querying-expression-data-for-marker-genes"></a>
If you're unsure which genes to explore, marker genes can be a helpful starting point. The following example demonstrates how to retrieve marker genes for your organ and cell type of interest, followed by querying the average expression of these genes.

First, use the `markers` method to obtain the top 5 marker genes for neutrophils in the human lung:

```{jupyter-execute}
markers_in_human_lung_neu = api.markers(
    organism='h_sapiens', 
    organ='lung', 
    cell_type='neutrophil', 
    number=5
)

markers_in_human_lung_neu
```

### Retrieve and plot
Next, use the `average` method to retrieve the average gene expression of these genes, then, use Seaborn’s `heatmap` to visualize your data:
```{jupyter-execute}
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
```
#### Output

This heatmap displays the gene expression levels of five neutrophil marker genes across all cell types. 

A significant portion of the heatmap appears black, indicating that these genes have very low expression levels (between 0-20 cptt) in most cell types. Due to the wide range of gene expression values, the current scale is too broad to effectively show differences within the 0-20 range. In this case, applying a logarithmic transformation helps compress the range, making smaller expression differences more visible while minimizing the impact of extremely high values. You can use the following code:

```{jupyter-execute}
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
```
To avoid division by zero, this example uses avg_gene_expr_markers + 1 instead of avg_gene_expr_markers. This addresses any potential blank cell issues while keeping the log scale consistent.

Comparing this heatmap with the original one, in this heatmap, all blank cells represent areas with no gene expression, while the other genes show low levels of expression across most cell types. It can be observed that *G0S2* is also expressed in *monocytes*, *dendritic cells*, *alveolar fibroblasts*, and *vascular smooth muscle*. Additionally, *IL1R2* shows expression in two other cell types as well. 

## **Conclusion** 
This tutorial introduces several methods for retrieving average gene expression using different API methods and how to use different packages for visualizing the data.

Thank you for using the *atlasapprox* API. For more detailed information, please refer to the [official documentation](https://atlasapprox.readthedocs.io/en/latest/python/index.html).