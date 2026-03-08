---
contact_name: "Wietze Suijker"
email_address: "PLACEHOLDER@email.com"
notebook_authors: [
    "Wietze Suijker"
]
notebook_title: "Under the Hood: Cloud-Native Crop Monitoring with EOPF Zarr"
docker_image_used: "Python"
makes_use_of_eopf_zarr_sample_service_data: true
incorporates_one_or_more_eopf_plugins: false
data_sources_used: ["Sentinel-2"]
had_challenges_working_with_sample_service_data: true
all_declarations_affirmed: true
---

# Submission

## Abstract (100 words)

This notebook detects spring green-up across a 2,000 m elevation gradient in NE Italy, from the Po Plain to the Julian Alps, transferring under 100 MB from a multi-terabyte archive. Each analysis step teaches a specific EOPF Zarr v3 concept by needing it: consolidated metadata for single-request discovery, sharding for fewer HTTP requests, multi-resolution groups for progressive zoom, and co-located SCL masks for quality filtering. We compute NDVI (10m) and NDRE (20m) change between autumn and spring, revealing altitude-dependent phenology. A real-world v2/v3 media type mismatch in STAC metadata demonstrates why format probing matters for robust implementations.

## AI Disclosure: Describe how you used AI in authoring this notebook (100 words)

Claude (Anthropic) was used as a coding assistant throughout development. It helped with code iteration (debugging AOI positioning within the autumn swath coverage, SCL class selection for valid pixels), matplotlib figure styling, and structuring the notebook narrative to align with the competition template. All scientific decisions (study area selection, index choice, elevation zone placement, interpretation of results) were made by the author. The v2/v3 format mismatch discovery and the architecture explanations draw on the author's direct experience contributing to the GDAL Zarr driver, GeoZarr conformance tests, and QGIS GeoZarr plugin.

## References: Provide the URLs of all code sources that you used in authoring this notebook

- EOPF Zarr Sample Service: https://explorer.eopf.copernicus.eu
- EOPF STAC API: https://api.explorer.eopf.copernicus.eu/stac
- Zarr Python documentation: https://zarr.readthedocs.io/
- pystac-client documentation: https://pystac-client.readthedocs.io/
- EOPF 101 book: https://eopf-toolkit.github.io/eopf-101/
- GeoZarr spec conformance tests: https://github.com/zarr-developers/geozarr-spec/pull/127
- GDAL Zarr vlen-utf8 PR: https://github.com/OSGeo/gdal/pull/14072
- QGIS GeoZarr plugin: https://github.com/wietzesuijker/qgis-geozarr

## Feedback (If you answered `true` to `had_challenges_working_with_sample_service_data` please provide feedback here!)

The STAC metadata declares `application/vnd+zarr; version=2; profile=multiscales` but the actual data is Zarr v3 (zarr_format=3 in zarr.json). This media type mismatch causes clients that trust the STAC declaration to use a v2 reader, which fails on v3 data. Robust implementations need to probe zarr.json directly. Updating the STAC media type to reflect v3 would prevent this class of errors.

## Declarations
By submitting this notebook:
- I/we agree to abide by the competition rules.
- I/we confirm this submission is my/our own original work.
- I/we grant the European Space Agency and thriveGEO GmbH a non-exclusive license to use, reproduce, modify, and display my/our work for promotional and educational purposes, including featuring it in the EOPF 101 online book.
- I/we confirm that the code submitted may be published under the Apache 2 license.
