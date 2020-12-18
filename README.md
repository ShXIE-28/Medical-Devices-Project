# Medical-Devices-Project

_Due to company privacy, the data results in this repository is hidden._

The purpose of this project is to built a structure of medical device data wrangling and plotting using python and Tableau dashboards. The results can be statistical evidences on market share comparison and help company make decision on business expand.

_The language of the dataset is Spanish_

____
Here I will explain key variables in the dataset.

    POSICION ARANCELARIA: Harmonized System (HS) Codes, a standardized numerical method of classifying traded products which are commonly used throughout the export process for goods
    HS_4: The first 4 digit of HS code
    HS_6: The first 6 digit of HS code
    keyword: Categories of merchandise based on the first 6 digit of HS code
    PAIS: The import country
    PAIS DE ORIGEN: Country of manufacture
    PAIS DE PROCEDENCIA: Country of shipment
    FECHA: Date of dispatch
    FOB: FOB value of the transaction
    CIF: CIF value of the transaction
    CANTIDAD: Number of unit of merchandise
    unit_fob: Unit FOB value of the transaction
    unit_cif: Unit CIF value of the transaction
    diff_unit_cif_fob: difference between unit_cif and unit_fob
    RAZON SOCIAL: The name of the importer
    Longitude Ori: the longitude of the export country(Pais De Origen)
    Longitude Pro: the longitude of the manufacutre country(Pais De Procedencia)
    Longitude Pais: the longitude of the import country(Pais)
    Latitude Ori: the latitude of the export country(Pais De Origen)
    Latitude Pro: the latitude of the manufacutre country(Pais De Procedencia)
    Latitude Pais: the latitude of the import country(Pais)

____
Promed_data.py is the process of data wrangling. Promed_unit_price.py is the calculation of unit price.

Please go to Report.pdf to see Tableau dashboards.
