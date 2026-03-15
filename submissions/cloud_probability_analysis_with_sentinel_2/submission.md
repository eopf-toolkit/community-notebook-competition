---
contact_name: "Erik Hass"
email_address: "erik.hass@xarvio.com"
notebook_authors:
  - "Erik Hass"
  - "Zhan Li"
notebook_title: "Cloud Probability Analysis with EOPF Sentinel-2 Data"
docker_image_used: "Python"
makes_use_of_eopf_zarr_sample_service_data: true
incorporates_one_or_more_eopf_plugins: true
data_sources_used: ["Sentinel-2"]
had_challenges_working_with_sample_service_data: false
all_declarations_affirmed: true
---

# Submission

## Abstract (100 words)

This notebook demonstrates time-series analysis of cloud probability using EOPF Sentinel-2 L2A data accessed via STAC API. We implement Dask distributed computing for parallel processing of multiple scenes, enabling efficient analysis of cloud patterns over agricultural areas. The workflow includes STAC-based data discovery, parallel scene loading with native Zarr chunking, NoData masking, and comprehensive quality inspection. Key analyses include temporal aggregations, seasonal pattern detection, and interactive scene visualization. The notebook provides educational insights into cloud-optimized data access, parallel computing strategies, and best practices for handling missing data in satellite imagery analysis.

## AI Disclosure: Describe how you used AI in authoring this notebook (100 words)

AI assistance (GitHub Copilot) was used throughout notebook development for code generation, optimization, and documentation. The AI helped implement Dask parallel processing patterns, optimize chunking strategies for Zarr access, resolve timezone handling issues in xarray operations, and develop comprehensive data quality inspection tools. AI also assisted in creating visualization code, writing educational markdown documentation, and implementing error handling for STAC API edge cases. All code was reviewed, tested, and modified by the authors to ensure correctness and alignment with EOPF best practices. The AI served as a collaborative tool for accelerating development and improving code quality.

## References: Provide the URLs of all code sources that you used in authoring this notebook

- EOPF Documentation: https://eopf.readthedocs.io/
- STAC API Specification: https://stacspec.org/
- PySTAC Client: https://pystac-client.readthedocs.io/
- Xarray Documentation: https://docs.xarray.dev/
- Dask Distributed: https://distributed.dask.org/
- Zarr Python: https://zarr.readthedocs.io/
- EODC STAC Catalog: https://stac.core.eopf.eodc.eu/
- Sentinel-2 MSI Technical Guide: https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-2-msi

## Feedback (If you answered `true` to `had_challenges_working_with_sample_service_data` please provide feedback here!)


## Declarations

By submitting this notebook:
- I/we agree to abide by the competition rules.
- I/we confirm this submission is my/our own original work.
- I/we grant the European Space Agency and thriveGEO GmbH a non-exclusive license to use, reproduce, modify, and display my/our work for promotional and educational purposes, including featuring it in the EOPF 101 online book.
- I/we confirm that the code submitted may be published under the Apache 2 license.

## Notes (optional)

