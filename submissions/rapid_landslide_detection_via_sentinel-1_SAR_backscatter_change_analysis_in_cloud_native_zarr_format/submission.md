---
contact_name: "Mark Lelaono" 
email_address: "marklelaono933@gmail.com"
notebook_authors: [ Mark Lelaono
]
notebook_title: "Rapid Landslide Detection via Sentinel-1 SAR Backscatter Change Analysis in Cloud-Native Zarr Format"
docker_image_used: "Python"
makes_use_of_eopf_zarr_sample_service_data: true
incorporates_one_or_more_eopf_plugins: true
data_sources_used: ["Sentinel-1", "Sentinel-3"]
had_challenges_working_with_sample_service_data: false
all_declarations_affirmed: true
---

# Submission

## Abstract (100 words)
This notebook presents an end-to-end educational workflow for detecting landslides using Sentinel-1 GRD Interferometric Wide (IW) swath backscatter data accessed in cloud-native Zarr format via the EOPF Sample Service. The pipeline combines multi-temporal log-ratio
change index (LCI) computation, z-score normalisation against a stable background, and cumulative sum (CUSUM) temporal analysis to produce a fused change-evidence image. Otsu adaptive thresholding and morphological post-processing delineate individual landslide scars,
validated with precision, recall, F1, IoU, and Cohen's Kappa metrics. A Bududa District, Uganda case study contextualises the workflow within operational early warning systems for the Greater Horn of Africa.
## AI Disclosure: Describe how you used AI in authoring this notebook (100 words)
All scientific decisions — including algorithm selection, case study choice were made independently by the author based on domain expertise in ML-based early warning systems.
## References: Provide the URLs of all code sources that you used in authoring this notebook
Zarr Python Documentation — https://zarr.readthedocs.io/en/stable/
Xarray Zarr Backend — https://docs.xarray.dev/en/stable/user-guide/io.html#zarr
EOPF Sample Service & Zarr Format Overview — https://eopf.copernicus.eu/
Copernicus Data Space Ecosystem (CDSE) — Sentinel-1 Access — https://dataspace.copernicus.eu/explore-data/data-collections/sentinel-data/sentinel-1
Sentinel-1 SAR Technical Guide (ESA) — https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-1-sar
scikit-image regionprops & morphology — https://scikit-image.org/docs/stable/api/skimage.morphology.html
Dask Array Documentation — https://docs.dask.org/en/stable/array.html
Folium Documentation — https://python-visualization.github.io/folium/
NASA COOLR Global Landslide Catalog — https://coolr.landslidedb.com
Mondini et al. (2021) — SAR amplitude change for landslide detection — https://doi.org/10.1016/j.rse.2021.112442
Burrows et al. (2020) — SAR-based landslide characterisation — https://doi.org/10.1029/2020GL088024
## Feedback (If you answered `true` to `had_challenges_working_with_sample_service_data` please provide feedback here!)

## Declarations
By submitting this notebook:
- I/we agree to abide by the competition rules.
- I/we confirm this submission is my/our own original work.
- I/we grant the European Space Agency and thriveGEO GmbH a non-exclusive license to use, reproduce, modify, and display my/our work for promotional and educational purposes, including featuring it in the EOPF 101 online book.
- I/we confirm that the code submitted may be published under the Apache 2 license.

## Notes (optional)
While Sentinel-1 is the primary data source for the core change detection methodology, the notebook is structured to accommodate Sentinel-3 OLCI-derived vegetation condition indices (NDVI anomaly) as an ancillary trigger condition layer, accessed from the same EOPF Zarr store. This dual-sensor design strengthens confidence in detected events by cross-referencing SAR-detected scars with antecedent vegetation stress signals.