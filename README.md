# SIMPLE COVID-19 API
Simple covid-19 statistics api. https://c19api.herokuapp.com

## GET /world
Get all covid19 statistics.
__Example Response__:
```json
{
    "active_cases": 18404546,
    "critical_cases": 109628,
    "new_cases": 329867,
    "new_deaths": 5313,
    "total_cases": 143874047,
    "total_deaths": 3062294,
    "total_recovered": 122407207
}
```

## GET /countries
Get covid19 statistics of all countries
__Example Response__:
```json
[
    ...
    {
        "active_cases": 6856823,
        "continent": "North America",
        "country": "USA",
        "critical_cases": 10036,
        "new_cases": 9036,
        "new_deaths": 143,
        "population": 332558517,
        "total_cases": 32545506,
        "total_deaths": 582599,
        "total_recovered": 25106084,
        "total_tests": 432026438
    },
    {
        "active_cases": 2236207,
        "continent": "Asia",
        "country": "India",
        "critical_cases": 8944,
        "new_cases": 122562,
        "new_deaths": 518,
        "population": 1390864355,
        "total_cases": 15731566,
        "total_deaths": 183088,
        "total_recovered": 13312271,
        "total_tests": 271053392
    },
    ...
]
```

## GET /countries/:country
Get covid19 statistics of a country.
__Example Response__:
```json
{
    "active_cases": 2236207,
    "continent": "Asia",
    "country": "India",
    "critical_cases": 8944,
    "new_cases": 122562,
    "new_deaths": 518,
    "population": 1390864355,
    "total_cases": 15731566,
    "total_deaths": 183088,
    "total_recovered": 13312271,
    "total_tests": 271053392
}
```

## GET /continents/
Get covid19 statistics of all continents.
__Example Response__:
```json
{
    ...
    "africa": {
        "active_cases": 358906,
        "continent": "Africa",
        "critical_cases": 3810,
        "new_cases": 1308,
        "new_deaths": 16,
        "total_cases": 4490521,
        "total_deaths": 118935,
        "total_recovered": 4012680
        },
        "asia": {
        "active_cases": 4205330,
        "continent": "Asia",
        "critical_cases": 29960,
        "new_cases": 210467,
        "new_deaths": 1823,
        "total_cases": 34861018,
        "total_deaths": 476380,
        "total_recovered": 30179308
        },
    ...
}
```

## GET /continents/:continent
Get covid19 statistics of a continent.
__Example Response__:
```json
{
    "active_cases": 4205330,
    "continent": "Asia",
    "critical_cases": 29960,
    "new_cases": 210467,
    "new_deaths": 1823,
    "total_cases": 34861018,
    "total_deaths": 476380,
    "total_recovered": 30179308
}
```