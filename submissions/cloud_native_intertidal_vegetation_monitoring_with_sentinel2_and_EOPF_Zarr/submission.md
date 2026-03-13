---
contact_name: "Fernando García-González"
email_address: "f.garcia@ieo.csic.es"
notebook_authors: [
    "Fernando García-González, Seagrass Ecology Group (IEO-CSIC, Spain)",
    "Pablo González, Artificial Intelligence Center (University of Oviedo, Spain)"
]
notebook_title: "Cloud-Native Intertidal Vegetation Monitoring with Sentinel-2 and EOPF Zarr"
docker_image_used: "Python"
makes_use_of_eopf_zarr_sample_service_data: true
incorporates_one_or_more_eopf_plugins: false
data_sources_used: ["Sentinel-2"]
had_challenges_working_with_sample_service_data: true
all_declarations_affirmed: true
---

# Submission

## Abstract (100 words)

This notebook presents a fully cloud-native workflow for monitoring intertidal vegetation in the Villaviciosa Ramsar estuary (Asturias, Spain) using Sentinel-2 L2A data served through the EOPF Zarr Sample Service. Without downloading any imagery, the workflow queries the EOPF STAC catalogue, streams Zarr stores lazily via the `eopf-zarr` xarray engine, and computes a multi-temporal water-frequency map from the Scene Classification Layer to automatically delineate the intertidal zone. Per-scene NDVI is then computed for cloud-free exposed intertidal pixels and normalised by tidal exposure to obtain a tide-independent vegetation cover metric, aggregated into seasonal phenological summaries.

## AI Disclosure: Describe how you used AI in authoring this notebook (100 words)

GitHub Copilot (Claude Sonnet) was used as a coding assistant during development of this notebook. It helped draft and refine Python code cells, improve markdown documentation, and structure educational explanations of the methods. All scientific decisions — choice of study site, methodology (water-frequency intertidal mapping, tide-normalised NDVI), threshold values, and ecological interpretations — were made by the authors. All code was reviewed, tested, and validated by the authors before submission.

## References: Provide the URLs of all code sources that you used in authoring this notebook

- EOPF Zarr Sample Service STAC endpoint: https://stac.core.eopf.eodc.eu
- EOPF 101 book: https://eopf-toolkit.github.io/eopf-101/
- pystac-client documentation: https://pystac-client.readthedocs.io/
- rioxarray documentation: https://corteva.github.io/rioxarray/
- contextily documentation: https://contextily.readthedocs.io/

## Feedback (If you answered `true` to `had_challenges_working_with_sample_service_data` please provide feedback here!)

Overall the EOPF Zarr Sample Service was very useful and we appreciate the work behind it. We did encounter some occasional inconsistencies when accessing certain Zarr stores — a number of STAC items could not be opened, which we handled by implementing fault-tolerant scene loading in our workflow. We also experimented with the `xcube-eopf` plugin and ran into some issues, which we reported to the development team (see [xcube-eopf#53](https://github.com/EOPF-Sample-Service/xcube-eopf/issues/53)). The team was responsive and helpful. We understand these are early-stage tools and expect the experience to improve as the ecosystem matures.

## Declarations
By submitting this notebook:
- I/we agree to abide by the competition rules.
- I/we confirm this submission is my/our own original work.
- I/we grant the European Space Agency and thriveGEO GmbH a non-exclusive license to use, reproduce, modify, and display my/our work for promotional and educational purposes, including featuring it in the EOPF 101 online book.
- I/we confirm that the code submitted may be published under the Apache 2 license.

## Notes (optional)

