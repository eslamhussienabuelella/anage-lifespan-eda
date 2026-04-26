# Analysis summary

## Dataset inspection

- Raw dataset shape: **4,645 rows × 31 columns**.
- Animalia records with known maximum longevity: **4,135**.
- Four most represented classes: **Aves, Mammalia, Teleostei, Reptilia**.

## Species representation by class

| Class     |   species_count |
|:----------|----------------:|
| Aves      |            1394 |
| Mammalia  |            1029 |
| Teleostei |             798 |
| Reptilia  |             526 |

## Weight–longevity relationship

The log-log scatter plots show a generally positive association between adult body weight and maximum longevity, but the strength varies by class. Larger animals often live longer, especially within mammals and birds, although the relationship is not deterministic and several biological exceptions appear.

The strongest class-level log-scale correlation in this run is **Mammalia** (r = 0.706), while the weakest is **Teleostei** (r = 0.286).

## Class-level metrics

| Class     |    n |   median_adult_weight_g |   median_max_longevity_yrs | max_adult_weight_species   |   max_adult_weight_g | max_longevity_species   |   max_longevity_yrs |   log10_weight_longevity_corr |   log10_weight_longevity_slope |
|:----------|-----:|------------------------:|---------------------------:|:---------------------------|---------------------:|:------------------------|--------------------:|------------------------------:|-------------------------------:|
| Aves      | 1375 |                   99    |                      14.6  | Ostrich                    |        111000        | Pink cockatoo           |                  83 |                      0.661946 |                       0.213391 |
| Mammalia  | 1023 |                 1900    |                      17.1  | Blue whale                 |             1.36e+08 | Bowhead whale           |                 211 |                      0.705832 |                       0.159452 |
| Reptilia  |  368 |                  742.25 |                      18.65 | Leatherback sea turtle     |        420000        | Aldabra tortoise        |                 152 |                      0.539241 |                       0.140401 |
| Teleostei |  346 |                 2640    |                      16    | Horse mackerel             |        376200        | Rougheye rockfish       |                 205 |                      0.285956 |                       0.132716 |

## Notable outliers

The IQR rule identifies unusually large or long-lived species within each class. Key examples include long-lived birds such as parrots and condors, very large mammals such as whales, and long-lived reptiles such as giant tortoises. These species are useful for ageing research because they may highlight biological mechanisms linked to slow ageing, body-size scaling, metabolic strategy, and exceptional longevity.

The complete outlier table is saved at `outputs/tables/iqr_outliers_top4_classes.csv`.
