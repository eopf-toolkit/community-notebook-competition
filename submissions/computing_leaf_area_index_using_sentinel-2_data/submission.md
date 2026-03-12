---
contact_name: "David Meaux" 
email_address: "david.meaux@geomatys.com"
notebook_authors: ["David Meaux"]
notebook_title: "Computing Leaf Area Index Using Sentinel-2 Data"
docker_image_used: "Python"
makes_use_of_eopf_zarr_sample_service_data: true # Must be true
incorporates_one_or_more_eopf_plugins: true # Either true or false
data_sources_used: ["Sentinel-2"] # Must contain at least one of "Sentinel-1", "Sentinel-2", or "Sentinel-3"
had_challenges_working_with_sample_service_data: true # Either true or false - If true, please leave feedback!
all_declarations_affirmed: true # Must be true
---

# Submission

## Abstract (100 words)

This notebook presents a Python re-implementation of ESA's SNAP BiophysicalOp processor for computing Leaf Area Index (LAI) from Sentinel-2 Level-2A data. It leverages cloud-native EOPF Zarr archives accessed via the STAC API, eliminating multi-gigabyte SAFE downloads. A two-layer neural network takes 11 inputs (eight spectral reflectance bands plus cosines of view/sun zenith and relative azimuth angles) to predict LAI across full Sentinel-2 tiles. Input validation combines per-band range checks and a convex hull domain test; outputs are quality-flagged and exported as CF-compliant Zarr stores. Batch processing of an entire growing season requires minutes rather than the hours needed by SNAP.

## AI Disclosure: Describe how you used AI in authoring this notebook (100 words)

Claude Code was used to refine and refactor code I had previously created for executing the LAI inference pipeline included with this project. In addition, Claude Code was used to summarize previously written documentation into the steps explained here. All code and documentation was reviewed and tested line-by-line, word-by-word. In addition, I added significant chunks of my own content and rephrased sections according to my own style. AI was used as a tool to accelerate development and documentation, not as the creator of this project.

## References: Provide the URLs of all code sources that you used in authoring this notebook

- [SeNtinel Application Platform (SNAP) Engine](https://github.com/senbox-org/snap-engine)
- [Optical Toolbox (OptTbx)](https://github.com/senbox-org/optical-toolbox)

## Feedback (If you answered `true` to `had_challenges_working_with_sample_service_data` please provide feedback here!)

There were inconsitencies in the data structure of various source data. For example, the data type for the detector data arrays were integers in some datasets and strings in others. Also, the overviews (quality/l2a_quicklook/{r10m, r20m, r60m}), specifically the true-color composite image (TCI) arrays, were present in some datasets but not all, which caused me to have to implement my own functions for creating true-color composites.

## Declarations
By submitting this notebook:
- I/we agree to abide by the competition rules.
- I/we confirm this submission is my/our own original work.
- I/we grant the European Space Agency and thriveGEO GmbH a non-exclusive license to use, reproduce, modify, and display my/our work for promotional and educational purposes, including featuring it in the EOPF 101 online book.
- I/we confirm that the code submitted may be published under the Apache 2 license.

## Notes (optional)
