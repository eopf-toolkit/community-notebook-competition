---
contact_name: "Hillary Koros"
email_address: "hillary.koros@igad.int"
notebook_authors: ["Hillary Koros"]
notebook_title: "Sentinel-1 SAR Flood Detection and Mapping Using Change Detection"
docker_image_used: "Python"
makes_use_of_eopf_zarr_sample_service_data: true
incorporates_one_or_more_eopf_plugins: false
data_sources_used: ["Sentinel-1"]
had_challenges_working_with_sample_service_data: false
all_declarations_affirmed: true
---

# Submission

## Abstract (100 words)

This notebook demonstrates an end-to-end SAR-based flood detection and impact assessment workflow using Sentinel-1 Level-1 GRD data accessed through the EOPF Zarr Sample Service. Targeting the documented Tana River flood event of November 22–23, 2025 near Hola, Kenya, we implement the UN-SPIDER Recommended Practice for flood mapping using a matched Sentinel-1 image pair just 12 days apart (November 11 pre-flood vs November 23 post-flood). The workflow covers STAC-based data discovery, radiometric calibration, speckle filtering, ratio-based change detection with automatic threshold optimization (Otsu's method), flood extent refinement, and impact assessment including population exposure, cropland damage, and urban area effects. The cloud-native EOPF Zarr format enables direct spatial subsetting without downloading entire 860 MB products.

## AI Disclosure: how AI is used in authoring this notebook (100 words)

AI tools (Claude) were used to assist with structuring the notebook narrative, adapting the UN-SPIDER Google Earth Engine methodology to Python/xarray for EOPF Zarr data, refining code documentation, and ensuring educational clarity. The core methodology, parameter choices, and scientific interpretation are based on the established UN-SPIDER Recommended Practice and the author's expertise in geospatial systems and flood monitoring. All AI-generated suggestions were reviewed, tested, and validated.

## References: All code sources  used in authoring this notebook

- UN-SPIDER Recommended Practice - SAR Flood Mapping: https://www.un-spider.org/advisory-support/recommended-practices/recommended-practice-google-earth-engine-flood-mapping/step-by-step
- EOPF STAC API: https://stac.core.eopf.eodc.eu
- EOPF 101 Book: https://eopf-toolkit.github.io/eopf-101/
- ESA Sentinel-1 User Guide: https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-1-sar
- GHSL Population Grid: https://ghsl.jrc.ec.europa.eu/ghs_pop2023.php


## Declarations
By submitting this notebook:
- I/we agree to abide by the competition rules.
- I/we confirm this submission is my/our own original work.
- I/we grant the European Space Agency and thriveGEO GmbH a non-exclusive license to use, reproduce, modify, and display my/our work for promotional and educational purposes, including featuring it in the EOPF 101 online book.
- I/we confirm that the code submitted may be published under the Apache 2 license.

## Notes 
Author background: Hillary Koros - DevOps Engineer at CIPAC / System Developer / Geospatial Researcher at IGAD, with expertise in flood monitoring systems and geospatial infrastructure across East Africa.
