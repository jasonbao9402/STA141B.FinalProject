# Dataset + Policy Feature Guide (for EIA integration)

## 1) currently have

### A. `energy_policy_dataset/utwind09_14_09b_labels_stata.csv`
Use this as the main working file.
- Shape: utility-firm by year (not already state-year)
- Coverage in file: 1997-2007
- Geography: U.S. states (state abbreviation in `state_firm`)
- Good for: renewable generation, emissions proxy, policy indicators, and controls in one table

### B. `energy_policy_dataset/utwind09_14_09b_labels.csv`
Same content, but shorter/raw-style column names.
- Prefer the `_stata.csv` version because labels are clearer.

### C. EIA pull outputs from your scripts (`extract_eia.py`)
You are already pulling:
- Renewable generation: `state`, `date`, `renewable_energy_type`, `renewable_energy_output`
- Carbon emissions: `state`, `date`, `carbon_emissions_type`, `carbon_emissions_value`

These are state-year level and should be the external reference panel.

## 2) Unit of analysis you should use

For your research question, use **state-year** as the final unit.

From `utwind..._stata.csv`, aggregate by:
- `state_firm`
- `year`

Then merge with EIA pulls on:
- `state_firm` <-> `state`
- `year` <-> `date`

## 3) Most important columns/features

## A. Core outcome
- `t_co2`
  - State-level carbon metric already present in the file.
  - Keep as your internal CO2 outcome.
- `carbon_emissions_value` (from EIA pull)
  - External CO2 outcome; useful for validation/robustness.

## B. Core treatment variables (renewables)
- `gen_wnd` (wind generation)
- `gen_sun` (solar generation)
- Optional denominator: `net_generation` (to build shares)

## C. State policy features (highest priority)
1. `rps_enact`
- Indicator/intensity for Renewable Portfolio Standard policy enactment.
- Use as core policy feature.

2. `rps_eff`
- RPS effective status/timing.
- Use with `rps_enact` for policy timing dynamics.

3. `rps_plant`
- RPS design component tied to in-state plant generation.

4. `rps_noplant`
- RPS design component not tied to plant requirement.

5. `deregulation`
- Electricity market restructuring indicator.

6. `disc_enact`
- Retail competition/distribution policy enactment timing.

7. `disc_eff`
- Effective timing of competition/distribution policy.

8. `green_policy_en`
- General state green policy indicator.

## D. Secondary policy/political controls (good to keep)
- `governor`
- `p_rep_house_gen`
- `p_rep_senate_gen`
- `lcv` (environmental ideology proxy)

## E. Economic controls 
- `gdp_capita`
- `cap_personal_income`
- `unemployment_rate`
- `sale_tax`, `corp_tax`, `prop_tax` (optional fiscal controls)

