# Vaccine-Stats-Ohio
Vaccine-Stats-Ohio is a Python library for accessing and summarizing Ohio COVID vaccine statistics.

> ### **Disclaimer**
> The content provided in this module is for educational purposes only. It is not intended to substitute for professional medical advice, diagnosis, or treatment. Effort was made to ensure data accuracy and reliability, however no guarantee can be made to this effect.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install vaccine-stats-ohio
```

# Usage

## Initialize data

To get started, import the `Vax_Stats` class and initialize it. Vaccine statistics are automatically downloaded from the [Ohio Department of Health website](https://coronavirus.ohio.gov/wps/portal/gov/covid-19/dashboards/covid-19-vaccine/covid-19-vaccination-dashboard) and stored in a temporary file.

```python
from vaccine_stats import Vax_Stats

with Vax_Stats() as data:
    ...
```

Note that you may also want to import the date class, as it is used frequently in data lookups.

```python
from datetime import date
```

## Find the latest date for which data is published

ODH updates their data approximately daily. You can use the `odh_latest` function to determine what day the latest data is for. Note that data for the current day is usually incomplete, therefore it is wise to look back at least a day or two for accurate statistics.

```python
with Vax_Stats() as data:
    latest_date = data.odh_latest()
print(latest_date)

# Output: 2021-02-23
```

## Look up vaccination data

Vaccine data can be browsed by county and date using the `lookup` function. Statistics are returned as a tuple of integers mirroring the ODH data file. The first item is the number of vaccines started (i.e., the number of people who got their first dose) and the second item is the number of vaccines completed (i.e., the number of people who got their second dose). It is unclear how results will be reported if a vaccine that only requires one dose is distributed (we can cross that bridge when we get to it).

By default, data is returned cumulatively for all counties up through the current date.

```python
with Vax_Stats() as data:
    n = data.lookup()
print(n)

# Output: (1474872, 707396)
# There were 1.47 million vaccination series started, with 0.71 million having been completed, in the state of Ohio as of the date this was run.
```

Data can also be returned for inidividual counties and/or through a past date.

```python
with Vax_Stats() as data:
    n = data.lookup(county="Cuyahoga", date=date(2021, 2, 1))
print(n)

# Output: (94757, 24969)
# There were a total of 95k vaccination series started, with 25k having been completed, in Cuyahoga county as of February 1, 2021.
```

Data can also be displayed for an individual date (not cumulatively) using the `cumulative=False` argument.

```python
with Vax_Stats() as data:
    n = data.lookup(
        county="Cuyahoga",
        date=date(2021, 2, 1),
        cumulative=False
        )
print(n)

# Output: (2065, 2804)
# There were 2,065 first vaccines and 2,804 second vaccines given in Cuyahoga county on February 1, 2021.
```

## See changes over time

The `delta` function takes two dates and returns a tuple in the same format as the `lookup` function, but with numbers indicating the percent change in *cumulative* vaccinations between two dates.

```python
with Vax_Stats() as data:
    p = data.delta(
        back_date=date(2021, 2, 7),
        front_date=date(2021, 2, 14)
        )
print(p)

# Output: (18.4, 48.6)
# There were 18.4% more vaccination series started and 48.6% more vaccination series completed on February 14 compared to a week prior.
```

The `delta` function can also output raw vaccination numbers instead of percentages using the `percent=False` argument.

```python
with Vax_Stats() as data:
    n = data.delta(
        back_date=date(2021, 2, 7),
        front_date=date(2021, 2, 14),
        percent=False
        )
print(n)

# Output: (208761, 162962)
# There were 209k more vaccination series started and 163k more vaccination series completed on February 14 compared to a week prior.
```

The `delta` function also takes `county` as an argument, defaulting to `county="All"`.

## Find the percentage of the population that has been vaccinated

The percentage of the population that has been vaccinated can be found using the `percent_vaccinated` function. This defaults to showing the current totals for all counties. The function can be customized using the `county` and `date` arguments as per above.

```python
with Vax_Stats() as data:
    p = data.percent_vaccinated()
print(p)

# Output: 6.1
# A total of 6.1% of Ohio's population has completed their COVID vaccine series as of the date the program was run.
```

Data can also be displayed based on the number of people who received at least one dose of the vaccine rather than just those who have completed a vaccination series using the `fully_vaccinated=False` argument. 

```python
with Vax_Stats() as data:
    p = data.percent_vaccinated(fully_vaccinated=False)
print(p)

# Output: 12.6
# A total of 12.6% of Ohio's population has received at least one COVID vaccine as of the date the program was run.
```

## Predict when herd immunity will be reached

The `predict_herd_immunity` function attempts to estimate a date at which herd immunity will be significantly reached based on current vaccination trends.

> ### **Caution**
> This function makes a number of assumptions that must be carefully considered.
>
> * The `r_0` (r<sub>0</sub>) argument defaults to 2.5. This is based on an estimate from the CDC in the absence of widespread masking and social distancing measures.<sup>1</sup> This value was calculated early in the pandemic and is subject to error due to lack of available data at that time. The r<sub>0</sub> of COVID-19 in Ohio with mitigating measures has been closer to 1.0.<sup>1</sup>
> * The use of r<sub>0</sub> is inherently flawed because if assumes a completely susceptible population.<sup>2</sup> In other words, it does not account for individuals becoming less susceptible due to previous infection or vaccination. Previous estimates of r<sub>0</sub> also do not account for changes in transmissibility due to emerging vaccine variants.
> * The model currently assumes that a complete vaccination series confers 95% protection against COVID-19 (`full_efficacy=0.95`) whereas a single dose confers 50% protection (`started_efficacy=0.5`).<sup>3,4</sup> Some estimates suggest that a single dose of the vaccine could provide higher levels of protection than previously thought.<sup>5</sup> The model does not take into account the time it takes for immunity to be reached after vaccination and does not account for immunity waning over time.
> * The model calculates the rate at which people are being vaccinated using the `delta` function and extrapolates this into the future assuming a linear vaccination rate. In reality, vaccination rates may be nonlinear or otherwise fluctuate based on a number of factors including product availability, emergency use authorization of novel vaccines, and prevailing attitudes towards vaccination.
> * Because data is analyzed in aggregate for the state of Ohio, the assumption is that vaccination pravalence and incidence are homogenous across the state. This is not the case. Because of differences in geographic vaccination rates, many areas may see herd immunity slower than predicted.
>
> Because of these limitations, output from this function should be viewed with a high degree of skepticism. It constitutes a best effort attempt at predicting when herd immunity will be reached, but with a high degree of variability that is itself difficult to quantify. See Disclaimer above.

```python
with Vax_Stats() as data:
    d = data.predict_herd_immunity()
print(d)

# Output: 2022-01-13
# The predicted immunity date is January 13, 2022 as of the date the program was run.
```

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

# License
This software is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

# References

1. https://coronavirus.ohio.gov/wps/portal/gov/covid-19/resources/news-releases-news-you-can-use/basic-reproduction-number-pop-up-sites
1. Delamater PL, Street EJ, Leslie TF, Yang YT, Jacobsen KH. Complexity of the Basic Reproduction Number (R<sub>0</sub>). *Emerging Infectious Diseases*. 2019;25(1):1–4.
1. Polack FP, Thomas SJ, Kitchin N, Absalon J, Gurtman A, Lockhart S, et al. Safety and Efficacy of the BNT162b2 mRNA Covid-19 Vaccine. *New England Journal of Medicine*. 2020;383(27):2603–15.
1. Baden LR, El Sahly HM, Essink B, Kotloff K, Frey S, Novak R, et al. Efficacy and Safety of the mRNA-1273 SARS-CoV-2 Vaccine. *New England Journal of Medicine*. 2021;384(5):403–16.
1. Skowronski DM, De Serres G. Safety and Efficacy of the BNT162b2 mRNA Covid-19 Vaccine. *New England Journal of Medicine*. Published online February 17, 2021.