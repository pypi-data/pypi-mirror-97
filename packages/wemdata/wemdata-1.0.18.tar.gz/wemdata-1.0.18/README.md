# Data for the Wholesale Electricity Market of Western Australia

This package extracts the Wholesale Electricity Market (WEM) data.  The WEM is the electricity market of the Southwest Interconnected System (SWIS) of Western Australia.
The package consists of a series of functions to extract the data into a Pandas dataframe.

### Prerequisites

* Python 3.6 or later
* pandas
* requests
* It is also assumed that the user has an understanding of the WEM Rules

## Usage
This section sets out the functions for this package.  Before using the functions, import the package with the following command:

```
from wemdata import wemdatafunctions as wem
```

### comm_test(year)
The *comm_test function* gives the list of **Commissioning Test plans** of generation systems in the SWIS over a **year**. See below for an example of the usage of this function.

```
df_comm_test_2020 = wem.comm_test(year=2020)
```

### load_forecast()
The *load_forecast function* gives the **load forecast** for each of the Trading Interval in the current Trading Day. See below for an example of the usage of this function.

```
df_forecast = wem.load_forecast()
```

### extended_load_forecast()
The **'Extended Load Forecast'** report may include load forecast values beyond the next two Trading Days. The *extended_load_forecast function* gives the **extended load forecast** for each of the Trading Interval from the current Trading Day. See below for an example of the usage of this function.

```
df_extended_load_forecast = wem.extended_load_forecast()
```

### hist_load_forecast(year)
The *hist_load_forecast function* gives the **historical load forecast** for each of the Trading Interval over a **year**. See below for an example of the usage of this function.

```
df_hist_load_forecast = wem.hist_load_forecast(2019)
```
### ncs_dispatch()
The *ncs_dispatch function* gives the **network control services dispatch** for each of the Trading Interval by Facility over a year. See below for an example of the usage of this function.

```
df_ncs_dispatch = wem.ncs_dispatch()
```
### non_bal_dmo(year, month)
The *non_bal_dmo function* gives the **Non Balancing Dispatch Merit Order** for each of the Trading Interval by Facility over a **month** in a **year**. See below for an example of the usage of this function.

```
df_non_bal_dmo = wem.non_bal_dmo(year=2020,month=5)
```

### dsm_prices(year)
The *dsm_prices function* gives the **Demand Side Management (DSM) prices** for each Trading Day by Facility over a **year**. See below for an example of the usage of this function.

```
df_dsm_prices = wem.dsm_prices(2020)
```
### ops_measurements(year)
The *ops_measurements function* gives the **Operational measurement data** for each Trading Interval over a **year**. See below for an example of the usage of this function.

```
df_ops_measurements = wem.ops_measurements(2019)
```

### facility_scada(year, month)
The *facility_scada function* gives the **Facility SCADA data** for each Facility for each Trading Interval over a **month** of a **year**. See below for an example of the usage of this function.

```
df_facility_scada = wem.facility_scada(2020,4)
```
### load_summary(year)
The *load_summary function* gives the **Load summary** over a **year**. See below for an example of the usage of this function.

```
df_load_summary = wem.load_summary(2020)
```

### lfas_summary(year)
The *lfas_summary function* gives the **LFAS (Load Following Ancillary Service) summary** over a **year**. See below for an example of the usage of this function.

```
df_lfas_summary_2020 = wem.lfas_summary(2020)
```

### lfas_submissions(year)
The *lfas_submissions function* gives the **LFAS (Load Following Ancillary Service) submissions** over a **year**. See below for an example of the usage of this function.

```
df_lfas_submissions = wem.lfas_submissions(2020)
```
### outages(year)
The *outages function* gives the list of **Outages** over a **year**. See below for an example of the usage of this function.

```
df_outages = wem.outages(2020)
```

### ircr_ratios()
The *ircr_ratios function* gives the list of **IRCR (Individual Reserve Capacity Requirement) ratios**. See below for an example of the usage of this function.

```
df_ircr_ratios = wem.ircr_ratios()
```

### peak_trading_intervals()
The *peak_trading_intervals function* gives the list of **peak trading intervals**. See below for an example of the usage of this function.

```
df_peak_trading_intervals = wem.peak_trading_intervals()
```

### real_time_outages()
The *real_time_outages function* gives the list of **peak time outages**. See below for an example of the usage of this function.

```
df_real_time_outages = wem.real_time_outages()
```

### repo_count()
The *repo_count function* gives the list of **Refund exempt planned outages count** for each Facility. See below for an example of the usage of this function.

```
df_repo_count = wem.repo_count()
```

### balancing_summary(year)
The *balancing_summary function* gives the **Balancing Market summary** over a **year**. See below for an example of the usage of this function.

```
df_balancing_summary = wem.balancing_summary(2020)
```


### balancing_submissions(year, month)
The *balancing_submissions function* gives the **Balancing submission** for each Facility for each Trading Interval over a **month** of a **year**. See below for an example of the usage of this function.

```
df_balancing_submissions = wem.balancing_submissions(2020,5)
```

### STEM_summary(year)
The *STEM_summary function* gives the **STEM summary** for each Trading Interval over a **year**. See below for an example of the usage of this function.

```
df_STEM_summary = wem.STEM_summary(2020)
```

### STEM_participant_activity(year, month)
The *STEM_participant_activity function* gives the **STEM participant activity** data for each Facility for each Trading Interval over a **month** of a **year**. See below for an example of the usage of this function.

```
df_STEM_participant_activity = wem.STEM_participant_activity(2020,4)
```

### STEM_bids_and_offers(year, month)
The *STEM_bids_and_offers function* gives the **STEM bids and offers** data for each Facility for each Trading Interval over a **month** of a **year**. See below for an example of the usage of this function.

```
df_STEM_bids_and_offers = wem.STEM_bids_and_offers(2020,4)
```

### STEM_facilities_declarations(year, month)
The *STEM_facilities_declarations function* gives the **STEM facilities declarations** data for each Facility for each Trading Interval over a **month** of a **year**. See below for an example of the usage of this function.

```
df_STEM_facilities_declarations = wem.STEM_facilities_declarations(2020,4)
```

### total_sent_out_gen(year)
The *total_sent_out_gen function* gives the **total sent out generation** for each Trading Interval over a **year**. See below for an example of the usage of this function.

```
df_total_sent_out_gen = wem.total_sent_out_gen(2020)
```

## Authors

* **Ignatius Chin** 

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2020 igchin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

```
