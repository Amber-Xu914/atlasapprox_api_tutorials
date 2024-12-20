#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install atlasapprox


# In[2]:


import atlasapprox

api = atlasapprox.API()


# In[3]:


# Call API function with params
avg_gene_expr_lung = api.average(
    organism = "h_sapiens", 
    organ = "lung", 
    features = ["COL13A1", "COL14A1", "TGFBI", "PDGFRA", "GZMA"], 
    measurement_type = "gene_expression"
)

# Display the result
avg_gene_expr_lung


# In[4]:


cell_types = api.celltypes(organism="h_sapiens", organ="lung")
print(cell_types)

