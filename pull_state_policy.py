import pandas as pd
import pyreadstat


# .dta to DataFrame and CSV
df_dta = pd.read_stata("energy_policy_dataset/utwind09_14_09b_labels_stata.dta")
df_dta.to_csv("energy_policy_dataset/utwind09_14_09b_labels_stata.csv", index=False)

# .sav to DataFrame and CSV
df_sav, meta = pyreadstat.read_sav("energy_policy_dataset/utwind09_14_09b_labels.sav")
df_sav.to_csv("energy_policy_dataset/utwind09_14_09b_labels.csv", index=False)

