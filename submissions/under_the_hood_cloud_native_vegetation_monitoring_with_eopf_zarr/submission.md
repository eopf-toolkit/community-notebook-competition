---
contact_name: "Wietze Suijker"
email_address: "wietze.suijker@gmail.com"
notebook_authors: [
    "Wietze Suijker"
]
notebook_title: "Under the Hood: Cloud-Native Vegetation Monitoring with EOPF Zarr"
docker_image_used: "Python"
makes_use_of_eopf_zarr_sample_service_data: true
incorporates_one_or_more_eopf_plugins: false
data_sources_used: ["Sentinel-2"]
had_challenges_working_with_sample_service_data: true
all_declarations_affirmed: true
---

# Submission

## Abstract (100 words)

This notebook dissects an EOPF Zarr v3 store from the inside out — sharding, codec chains, consolidated metadata, multi-resolution groups — while answering a real scientific question: can spring green-up across a 2,000 m Alpine-to-lowland elevation gradient be detected with partial cloud-native reads from a 2 TB archive? Using three Sentinel-2 scenes over Friuli-Venezia Giulia, NE Italy, it builds a complete NDVI/NDRE monitoring workflow with SCL cloud masking and a performance waterfall audit. The elevation gradient analysis reveals that by peak spring, lowland fields gain 2.8× more NDVI than Alpine meadows — confirmed from 106 MB of partial reads against a 2,351 MB full-tile equivalent.

## AI Disclosure: Describe how you used AI in authoring this notebook (100 words)

Claude (Anthropic) was used as a coding assistant throughout development for code iteration, styling, and structuring the notebook narrative to align with the competition template. All scientific decisions (study area selection, index choice, elevation zone placement, three-date arc design, interpretation of results) were made by the author. The v2/v3 format mismatch discovery and the architecture explanations draw on the author's direct experience contributing to the GDAL Zarr driver, GeoZarr conformance tests, and QGIS GeoZarr plugin.

## References: Provide the URLs of all code sources that you used in authoring this notebook

- EOPF Zarr Sample Service: https://explorer.eopf.copernicus.eu
- EOPF STAC API: https://api.explorer.eopf.copernicus.eu/stac
- Zarr Python documentation: https://zarr.readthedocs.io/
- pystac-client documentation: https://pystac-client.readthedocs.io/
- EOPF 101 book: https://eopf-toolkit.github.io/eopf-101/
- GeoZarr spec conformance tests: https://github.com/zarr-developers/geozarr-spec/pull/127
- GDAL Zarr vlen-utf8 PR: https://github.com/OSGeo/gdal/pull/14072
- QGIS GeoZarr plugin: https://github.com/wietzesuijker/qgis-geozarr
- EOPF Explorer media type fix: https://github.com/EOPF-Explorer/data-pipeline/pull/94
- xarray-eopf (EOPF xarray backend): https://github.com/EOPF-Sample-Service/xarray-eopf

## Feedback (If you answered `true` to `had_challenges_working_with_sample_service_data` please provide feedback here!)

The STAC metadata declares `application/vnd+zarr; version=2; profile=multiscales` but the actual data is Zarr v3 (zarr_format=3 in zarr.json). This media type mismatch causes clients that trust the STAC declaration to use a v2 reader, which fails on v3 data. Robust implementations need to probe zarr.json directly. This has been addressed in [data-pipeline#94](https://github.com/EOPF-Explorer/data-pipeline/pull/94), though existing STAC items haven't been re-registered yet.

## Declarations
By submitting this notebook:
- I/we agree to abide by the competition rules.
- I/we confirm this submission is my/our own original work.
- I/we grant the European Space Agency and thriveGEO GmbH a non-exclusive license to use, reproduce, modify, and display my/our work for promotional and educational purposes, including featuring it in the EOPF 101 online book.
- I/we confirm that the code submitted may be published under the Apache 2 license.

## Notes (optional)

The notebook is designed to run end-to-end on the EOPF JupyterHub (launch button in cell 2). All data is accessed live from the EOPF Zarr Sample Service — no local files required.
