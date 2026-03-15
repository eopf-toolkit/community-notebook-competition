GENERAL:

The data you have downloaded falls under the IUCN Red List Terms and Conditions of Use which can be viewed on the IUCN Red List website at www.iucnredlist.org/terms/terms-of-use.



SPATIAL DATA DOWNLOADS

For species that are mapped, spatial data may be provided as polygons, HydroShed tables (for selected freshwater species) or as point data.

The polygon data is stored in shapefiles, the Esri native format.

Point data, if available, is provided in CSV format.

Please check the meta-data document attached for more information about the spatial data. This document is updated regularly, so always make sure to check on the www.iucnredlist.org website, under 'Resources / Resources and Publications -> Spatial Data download' for the latest version.

Please note that not all species assessed for the Red List have spatial data. There are a number of reasons for spatial data not being available e.g. assessments were done before maps were a requirement, the range could not be mapped, maps may have been deliberately withheld, etc. It is also important to note that for most polygon maps, the original point data used to construct these is not available.




NON-SPATIAL DATA DOWNLOADS

Depending on the type of non-spatial download you requested, the zip file that you receive will contain multiple data tables in Comma Delimited, CSV text file format. Although this file format allows for the data table(s) to be easily imported into a variety of applications, they are best viewed within one that will allow easy manipulation of data that is in columnar format. Common examples of such applications are those that are used to create spreadsheets (e.g. MS-Excel) and databases (e.g. MS-Access).

If you do not have access to either a spreadsheet or a database application, you can also import the data table(s) into either an ASCII text-editing or a word-processing application. However, since neither of these two application types has the facility to easily format the width of the data columns, a lot of manual reformatting will be required to properly view the data. The latter approach should also only be used with the simple_summary table.

To view multiple csv tables properly, they should be imported into a database application and the different tables joined using the "internalTaxonId" when viewing taxon information, or the "assessmentID" field to see assessment information, especially in cases where downloads include multiple assesments for a taxon (e.g. regional and global assessments).


IMPORTANT ISSUES TO NOTE:

- When importing the csv files you need to specifiy that the files are in UTF-8 format otherwise the extended characters will not import and display correctly.

- Many fields (especially text fields) will contain html coding to render the text properly on The IUCN Red List website; it is imposible to strip this out of the exports. In some cases, the html coding may be very lengthy with many formatting commands; this usually happens when the original data entry was done by copying and pasting from a heavily formatted PDF or word-processed document directly into the Species Information Service database (the system used to store the Red List data) without first eliminating the formatting by pasting into an intermediate text editor. Please let us know if you encounter any cases with excessive html formatting.


CONTENTS OF THE ZIP FILES:

- simple_summary.csv [a flat table containing the taxonomy for each taxon, Red List Category, Red List Criteria, version of criteria used, and current population trend].
- additional csv tables [these contain much more information as specified by the type of download selected and by the settings selected under your user profile. These tables need to be imported into an appropriate Application (see below) and joined using the "internalTaxonId" and/or "assessmentId" fields (see above)].


TO IMPORT A DATA TABLE INTO A SPREADSHEET APPLICATION OR IMPORT THE DATA TABLE INTO A DATABASE APPLICATION:

- Importing into a spreadsheet application: proceed with the steps that you normally go through to open a new spreadsheet and import the data from the external csv file (this is usually through the import from text option).

- Importing into a database: import the data table file into a new database table. In MS-Access this is done by opening the External Data option, selecting Text File, browsing to the data file, and following the data import instructions.

Note that because the data table is formatted as a CSV Text Document, you should be prompted to set the file import options, which will ensure that the data is properly formatted when the file is retrieved into the spreadsheet or imported into the database table. The key file import options and their associated values are listed below.

IMPORT OPTION 		VALUE
Data Type 		Comma Delimited
File Origin 		Unicode (UTF-8)
Text Qualifier 		{"}
Field Delimiter 	{,}
Multi-value Delimiter	{|}
First Row 		Field Names


For any questions, please contact the IUCN Red List Unit <redlist@iucn.org>
