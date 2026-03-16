---
contact_name: "Bibiana Rivadeneira"
email_address: "brivadeneira@protonmail.com"
notebook_authors: [
    "Bibiana Rivadeneira"
]
notebook_title: " 🐆Wildfire *(Panthera onca/Yaguareté)* health vegetation corridors monitoring: a multi-collection & multi-datasets *("popurrí")* fusion approach"
docker_image_used: "Python"
makes_use_of_eopf_zarr_sample_service_data: true
incorporates_one_or_more_eopf_plugins: true
data_sources_used: ["Sentinel-2"]
had_challenges_working_with_sample_service_data: true
all_declarations_affirmed: true
---

# Submission

## Abstract (100 words)
This notebook presents a cloud-native workflow for monitoring the vegetation vigor of *Panthera onca* (Yaguareté) corridors across the American continent. By fusing Sentinel-2 L2A and L1C Zarr data accessed via the EOPF STAC API, for the "habitat pulse" calc using NDVI statistics for over 1,000 scenes. The methodology integrates ecological thresholds, utilizing distributed lazy-loading, SCL quality masking, and spatial clipping. Results identify habitat degradation and connectivity loss, providing a scalable tool for conservationists or us, who love Yaguarete.

## AI Disclosure: Describe how you used AI in authoring this notebook (100 words)
AI tools were utilized to choose proper emojies in the documentation.

## References: Provide the URLs of all code sources that you used in authoring this notebook
- EOPF STAC API: https://stac.core.eopf.eodc.eu 
- EOPF 101 Community Guide: https://eopf-toolkit.github.io/eopf-101/
- Natural Earth Map Data: https://www.naturalearthdata.com 
- ESA Sentinel-2 L2A Specifications: https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S2L2A.html
- EOPF Zarr Sentinel-2 Reflectance Scaling: https://zarr.eopf.copernicus.eu
- Jupyter fo Edu: https://jupyter4edu.github.io/jupyter-edu-book/

## Feedback (If you answered `true` to `had_challenges_working_with_sample_service_data` please provide feedback here!)
When using te BBOX map in the API, world is duplicated 3 times, if a zoom is done in other that is not the midde one, the coordenates sent are wrong and there is no error detail. (No critical)

## Declarations
By submitting this notebook:
- I/we agree to abide by the competition rules.
- I/we confirm this submission is my/our own original work.
- I/we grant the European Space Agency and thriveGEO GmbH a non-exclusive license to use, reproduce, modify, and display my/our work for promotional and educational purposes, including featuring it in the EOPF 101 online book.
- I/we confirm that the code submitted may be published under the Apache 2 license.

## Notes (optional)

- The project was desinged for being split in at least 3 parts.

**Future Development Roadmap:**
- TODO: fix clip 
- TODO: Improve pipeline efficiency with Dask and parallelism
- TODO: Plot monthly
- TODO: detect water 
- TODO: correlate with GBIF occurrence data (thanks to Sabrina <3) 
- TODO: part 3, vis ndvi + water monthly + correlated with yaguarete occurrence intersects scenes 

> This project merges ancestral and archaeological identity, showing and urgent issue of a threatened animal, with modern remote sensing, honoring the yaguarete as a pillar of America (the continent).
