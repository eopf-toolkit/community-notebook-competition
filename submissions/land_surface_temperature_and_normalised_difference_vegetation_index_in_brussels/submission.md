---
contact_name: "Ellen Brock" 
email_address: "ellenarun@gmail.com"
notebook_authors: [ # Must contain at least one entry
    "Ellen Brock"
]
notebook_title: "Land Surface Temperature and Normalised Difference Vegetation Index in Brussels"
docker_image_used: "Python"
makes_use_of_eopf_zarr_sample_service_data: true # Must be true
incorporates_one_or_more_eopf_plugins: true # Either true or false
data_sources_used: ["Sentinel-2", "Sentinel-3"] # Must contain at least one of "Sentinel-1", "Sentinel-2", or "Sentinel-3"
had_challenges_working_with_sample_service_data: true # Either true or false - If true, please leave feedback!
all_declarations_affirmed: true # Must be true
---

# Submission

## Abstract (100 words)

In this notebook, we investigate the link between the Land Surface Temperature (LST) and the Normalised Difference Vegetation Index (NDVI) for Brussels, the capital city of Belgium.
LST and NDVI are obtained from the Sentinel-2 and Sentinel-3 missions respectively, using the newly adapted zarr data format from the EOPF Sentinel Zarr Samples project. We learn how to clip LST and NDV using a GeoJSON file for the Area Of Interest.
In our exploratory analysis, we find some evidence that higher NDVI is related to lower LST. 


## AI Disclosure: Describe how you used AI in authoring this notebook (100 words)

No AI was used in this notebook as the code follows a lot the scripts of URLs both from the EOPF itself and from other sources (please see below). Whenever code was used, the URL was given. 

## References: Provide the URLs of all code sources that you used in authoring this notebook

- https://eopf-toolkit.github.io/eopf-101/

- https://eopf-toolkit.github.io/eopf-101/04_eopf_and_stac/44_eopf_stac_xarray_tutorial.html#prerequisites

- https://eopf-toolkit.github.io/eopf-101/04_eopf_and_stac/43_eopf_stac_connection.html

- https://eopf-toolkit.github.io/eopf-101/06_eopf_zarr_in_action/62_sardinia_s3_lst.html

- https://sentiwiki.copernicus.eu/__attachments/1672112/OMPC.ACR.HBK.002%20-%20Sentinel%203%20SLSTR%20Land%20Handbook%202024%20-%201.4.pdf?inst-v=96021aea-734a-44d2-9ca8-2228c7de7290#:~:text=Land%20surface%20temperature%20products,ice%20and%20inland%20water%20pixels.

- https://www.geopythontutorials.com/notebooks/dask_median_composite.html from Ujaval Gandhi

- https://stacspec.org/en/tutorials/reading-stac-planetary-computer/

- https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/scene-classification/

- https://www.geopythontutorials.com/notebooks/xarray_processing_satellite_images.html

- [Mapping and Data Visualization with Python Course](https://spatialthoughts.com/courses/python-dataviz/) by Ujaval Gandhi www.spatialthoughts.com

- https://pystac-client.readthedocs.io/en/latest/api.html

- https://eopf-sample-service.github.io/eopf-sample-notebooks/

- https://eopf-sample-service.github.io/eopf-sample-notebooks/sentinel-3-heatwave-mapping/

- https://stackoverflow.com/questions/72215741/add-projection-to-rioxarray-dataset-in-python

- https://corteva.github.io/rioxarray/stable/

- https://docs.xarray.dev/en/stable/



## Feedback (If you answered `true` to `had_challenges_working_with_sample_service_data` please provide feedback here!)

I am very thankful to the entire EOPF team in general for opening the zar project to the wider public as working with it is really awewsome. Also, I also would like to thank the organisers of this competition as I am learning (still in progress!) a lot. 

The main challenges were:

- There were missing data and/or deprecated data. I found a workaround using a filter in pystac itself. My main challenge was that I had to find matching data for Sentinel-2 and Sentinel-3 both in terms of Area of Interest and time period. I ended up changing the ROI (from India to Europe eventually). Although it was easier to work on Europe, initially I found it difficult dealing with the missing/deprecated data as the visual explorer was not an option. There may be other options than the filter in Pystac (in EOPF having missing URLs or something).

- I noticed that there was no "quicklook" available so I wrote extra code for the True Colour Composites although some of the examples in the EOPF 101 had the quicklook option in the data. 

- One thing I felt a bit missing too (either in pystac or in the zar files unless I missed something) is that I did not find a record for partial data coverage. In the code, I ended up plotting a True Colour Negative that did not have full data coverage. If you have this variable, this could narrow the search quicker. 

- Since I needed to clip, I had to find the EPSG codes in Pystac itself and could not find any information (e.g. in the attributes) that shows the EPSG codes. 

I fully understand that the EOPF zar project is still work in progress so the above it not an issue as such as I really learnt a lot! Thank you very much for everything. 


## Declarations
By submitting this notebook:
- I/we agree to abide by the competition rules.
- I/we confirm this submission is my/our own original work.
- I/we grant the European Space Agency and thriveGEO GmbH a non-exclusive license to use, reproduce, modify, and display my/our work for promotional and educational purposes, including featuring it in the EOPF 101 online book.
- I/we confirm that the code submitted may be published under the Apache 2 license.

## Notes (optional)

There are some warnings still in the code and I hope to resolve them soon. The code needs to be scrubbed a bit too especially in the last part. 


