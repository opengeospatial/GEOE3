# Run the program

Run the **__main__.py** program. It will ask for :
- the path of source files ;
- a service ID.

The data from the availability API is downloaded into a temp file located in the temp folder. This file should be automatically deleted after the program is run.


## Starting point

Start implementation with a subset of metrics and a single service. The service chosen is the Norwegian building service.

Service metadata: `https://www.geonorge.no/geonetwork/srv/nor/xml_iso19139?uuid=dc0f80e3-3f4d-486b-9393-da8244f37e47`

Dataset metadata: `https://www.geonorge.no/geonetwork/srv/nor/xml_iso19139?uuid=8b4304ea-4fb0-479c-a24d-fa225e2c6e97`

Endpoint: `https://wfs.geonorge.no/skwms1/wfs.inspire-bu-core2d_limited?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities`

Spatineo Directory: `https://directory.spatineo.com/service/164572/`
