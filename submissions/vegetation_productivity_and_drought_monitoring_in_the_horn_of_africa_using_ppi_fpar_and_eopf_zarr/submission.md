---
contact_name: "Ezra Kiplimo"
email_address: "ezralimo548@gmail.com"
notebook_authors: [
    "Ezra Kiplimo"
]
notebook_title: "Vegetation Productivity and Drought Monitoring in the Horn of Africa Using PPI, fPAR, and EOPF Zarr"
docker_image_used: "Python"
makes_use_of_eopf_zarr_sample_service_data: true
incorporates_one_or_more_eopf_plugins: false
data_sources_used: ["Sentinel-2", "Sentinel-3"]
had_challenges_working_with_sample_service_data: true
all_declarations_affirmed: true
---

# Submission

## Abstract (100 words)

This notebook presents a cloud-native workflow for vegetation productivity and drought monitoring in the Horn of Africa using the EOPF Zarr Sample Service. Focused on the Southern Ethiopia–Northern Kenya border region, it demonstrates how to discover and access Sentinel-2 L2A and Sentinel-3 OLCI data via STAC, apply cloud masking using the Scene Classification Layer, and compute NDVI, the Plant Phenology Index (PPI), and biophysical variables (fPAR, LAI, fCover) in pure Python. Multi-date composites and time-integrated PPI (TPROD) are derived to support drought early warning and crop yield estimation for the IGAD region.

## AI Disclosure: Describe how you used AI in authoring this notebook (100 words)

Claude AI (Anthropic) was used to assist with code structure, documentation wording, and review of the notebook. All scientific methodology — including the PPI algorithm implementation, biophysical variable estimation (fPAR, LAI, fCover, TPROD), cloud masking strategy, and the EOPF Zarr data access workflow — was designed and authored by the human author based on peer-reviewed literature. AI assistance was limited to code formatting suggestions and prose refinement. All algorithms are cited to original published sources.

## References: Provide the URLs of all code sources that you used in authoring this notebook

- Jin, H. & Eklundh, L. (2014). A physically based vegetation index for improved monitoring of plant phenology. *Remote Sensing of Environment*, 152, 512–525. https://doi.org/10.1016/j.rse.2014.07.010
- Müller, M. et al. (2025). Using Sentinel-2 data to quantify the impacts of drought on crop yields. *Agricultural and Forest Meteorology*, 373, 110789. https://doi.org/10.1016/j.agrformet.2025.110789
- Weiss, M. & Baret, F. (2016). S2ToolBox Level 2 products: LAI, FAPAR, FCOVER. ESA, Version 1.1. https://step.esa.int/docs/extra/ATBD_S2ToolBox_L2B_V1.1.pdf
- Xiao, Z. et al. (2024). A global dataset of the fraction of absorbed photosynthetically active radiation for 1982–2022. *Scientific Data*, 11, 543. https://doi.org/10.1038/s41597-024-03561-0
- Bai, Y. et al. (2023). An assessment of relations between vegetation green FPAR and vegetation indices through a radiative transfer model. *Plants*, 12(10), 1927. https://doi.org/10.3390/plants12101927
- Jia, K. et al. (2020). Remote sensing algorithms for estimation of fractional vegetation cover using pure vegetation index values: A review. *ISPRS Journal*, 159, 364–377. https://doi.org/10.1016/j.isprsjprs.2019.11.018
- Myneni, R.B. & Williams, D.L. (1994). On the relationship between FAPAR and NDVI. *Remote Sensing of Environment*, 49(3), 200–211.
- EOPF-101: https://eopf-toolkit.github.io/eopf-101/

## Feedback (If you answered `true` to `had_challenges_working_with_sample_service_data` please provide feedback here!)

The `zarr` engine was not recognized by `xarray.open_datatree` in the provided Docker environment (`tf215gpu` conda env), causing a `ValueError`. The installed xarray backends did not include zarr (`['netcdf4', 'h5netcdf', 'scipy', 'cfgrib', 'rasterio', 'store']`). This prevented the notebook from opening any EOPF Zarr products. It would be helpful if the sample service documentation or competition Docker image explicitly listed the required package versions (e.g. `zarr`, `xarray-datatree`, `fsspec`) needed to open products with `engine="zarr"`.

## Declarations
By submitting this notebook:
- I/we agree to abide by the competition rules.
- I/we confirm this submission is my/our own original work.
- I/we grant the European Space Agency and thriveGEO GmbH a non-exclusive license to use, reproduce, modify, and display my/our work for promotional and educational purposes, including featuring it in the EOPF 101 online book.
- I/we confirm that the code submitted may be published under the Apache 2 license.

## Notes (optional)

The notebook is designed for the Southern Ethiopia–Northern Kenya border region monitored by ICPAC for drought early warning across the IGAD region (300M+ people). All biophysical algorithms (PPI, fPAR, LAI, fCover, TPROD) are implemented in pure Python using peer-reviewed, published methods — no ESA SNAP Java toolbox required.
