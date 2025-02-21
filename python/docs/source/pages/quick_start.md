# **Quick start: atlasapprox in Python**
The [*atlasapprox*](https://atlasapprox.readthedocs.io/en/latest/index.html) API provides access to approximated single-cell data across 28 species, including both animals and plants. You can explore data from species such as *Homo sapiens* (humans), *Mus musculus* (mice), *Arabidopsis thaliana* (thale cress), and *Zea mays* (corn). Follow this guide to get started with installation, basic usage, and example queries.

### **Create virtual environment**
To ensure consistent dependencies, setting up a virtual environment is recommended before installing the package. Here's one way to do it:

```{code}
# Create a virtual environment
python -m venv myenv

# Activate your environment (use the appropriate command for your OS)

# For macOS/Linux users
source myenv/bin/activate

# For Windows users
myenv\Scripts\activate 
```

### **Installation**
Use *pip* to install the *atlasapprox* Python package:

```{jupyter-execute}
pip install atlasapprox
```

### **Initialize the API**
Import the *atlasapprox* Python package and create an API object:
```{jupyter-execute}
import os
os.environ["ATLASAPPROX_HIDECREDITS"] = "yes"
import atlasapprox

api = atlasapprox.API()
```
## **Getting average gene expression**
The `average` function allows you to retrieve the average gene expression data for selected genes within an organism's specific organ.

The following example shows how to examine the average expression of five genes (*COL13A1*, *COL14A1*, *TGFBI*, *PDGFRA*, *GZMA*) in the human lung:

```{jupyter-execute}
# Call API function with params
avg_gene_expr_lung = api.average(
    organism = "h_sapiens", 
    organ = "lung", 
    features = ["COL13A1", "COL14A1", "TGFBI", "PDGFRA", "GZMA"], 
    measurement_type = "gene_expression"
)

# Display the result
avg_gene_expr_lung
```
### **Output**
The function returns a *Pandas DataFrame* where:
* Each row represents a gene.  
* Each column corresponds to a cell type.
* The values indicate the average gene expression (measured in counts per ten thousand, or cptt).


## **Start from scratch**
If you're starting from scratch, the following steps will help you explore the API.
1. Ask about available organisms:
```{jupyter-execute}
organisms = api.organisms()
print(organisms)
```
2. Ask about available organs within your organism of interest:
```{jupyter-execute}
organs = api.organs(organism="h_sapiens")
print(organs)
```
3. Ask about available cell types within your organism and organ of interest:
```{jupyter-execute}
cell_types = api.celltypes(organism="h_sapiens", organ="lung")
print(cell_types)
```

## **More tutorials (coming soon)**
- average gene expression
- cell type abundance
- highest measurements by cell type across an organism
- marker genes
- gene coexpression
- gene homologs
- neighborhoods
- gene interaction partners
- ...

## **Conclusion**
This tutorial provided a quick start guide to use the *atlasapprox* Python package. For more detailed information, refer to the official [documentation](https://atlasapprox.readthedocs.io/en/latest/python/index.html). 