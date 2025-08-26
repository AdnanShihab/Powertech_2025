"""
Investment cost function

stage1 = 2023-2025
stage2 = 2026-2028
stage3 = 2028-2031
"""

# Fixed parameters
cost_pv_installation = 1020000  # [EUR] per 1 MW PV farm installation Source: MANGO
cost_pv_installation_2023 = 110000     # EUR/MW
cost_pv_installation_2024 = 108000     # EUR/kW
cost_pv_installation_2025 = 106000     # EUR/kW
cost_pv_installation_2026 = 104000     # EUR/kW
cost_pv_installation_2027 = 102000     # EUR/kW
cost_pv_installation_2028 = 100000     # EUR/kW
cost_pv_installation_2029 = 97000     # EUR/kW
cost_pv_installation_2030 = 95000     # EUR/kW
cost_pv_installation_2031 = 94000     # EUR/kW

cost_bess_installation_2023 = 227000     # EUR/MWh Source: MANGO --> includes battery cost + installation cost
cost_bess_installation_2024 = 222000     # EUR/MWh
cost_bess_installation_2025 = 218000     # EUR/MWh

cost_chp_installation_2023 = 782000     # EUR/MW Source: MANGO
cost_chp_installation_2024 = 778000     # EUR/MW
cost_chp_installation_2025 = 774000     # EUR/MW

cost_land_industry_2023 = 44  # [EUR/m2] # Source: Onenote PSCC + Excel file on Dropbox/PSC2024
cost_land_industry_2024 = 44*1.05
cost_land_industry_2025 = (44*1.05)*1.05
cost_land_industry_2026 = ((44*1.05)*1.05)*1.05
cost_land_industry_2027 = ((44*1.05)*1.05)*1.05
cost_land_industry_2028 = (((44*1.05)*1.05)*1.05)*1.05
cost_land_industry_2029 = ((((44*1.05)*1.05)*1.05)*1.05)*1.05
cost_land_industry_2030 = (((((44*1.05)*1.05)*1.05)*1.05)*1.05)*1.05
cost_land_industry_2031 = ((((((44*1.05)*1.05)*1.05)*1.05)*1.05)*1.05)*1.05

cost_land_business_2023 = 45
cost_land_business_2024 = 45*1.05
cost_land_business_2025 = (45*1.05)*1.05
cost_land_business_2026 = ((45*1.05)*1.05)*1.05
cost_land_business_2027 = (((45*1.05)*1.05)*1.05)*1.05
cost_land_business_2028 = ((((45*1.05)*1.05)*1.05)*1.05)*1.05
cost_land_business_2029 = (((((45*1.05)*1.05)*1.05)*1.05)*1.05)*1.05
cost_land_business_2030 = ((((((45*1.05)*1.05)*1.05)*1.05)*1.05)*1.05)*1.05
cost_land_business_2031 = (((((((45*1.05)*1.05)*1.05)*1.05)*1.05)*1.05)*1.05)*1.05

cost_land_residential_2023 = 214
cost_land_residential_2024 = 214*1.05
cost_land_residential_2025 = (214*1.05)*1.05
cost_land_residential_2026 = ((214*1.05)*1.05)*1.05

cost_land_residential_business_2023 = 182
cost_land_residential_business_2024 = 182*1.05
cost_land_residential_business_2025 = (182*1.05)*1.05
cost_land_residential_business_2026 = ((182*1.05)*1.05)*1.05
cost_land_residential_business_2027 = (((182*1.05)*1.05)*1.05)*1.05
cost_land_residential_business_2028 = ((((182*1.05)*1.05)*1.05)*1.05)*1.05
cost_land_residential_business_2029 = (((((182*1.05)*1.05)*1.05)*1.05)*1.05)*1.05
cost_land_residential_business_2030 = ((((((182*1.05)*1.05)*1.05)*1.05)*1.05)*1.05)*1.05
cost_land_residential_business_2031 = (((((((182*1.05)*1.05)*1.05)*1.05)*1.05)*1.05)*1.05)*1.05

land_area_pv = 9000  # [m2 per 1 MW solar] --> source: OneNote/PowerTech/Calculations
land_area_bess = 25  # [m2 per 1 MWh utility scale battery installation] --> source: OneNote/PowerTech/Calculations

# Capital recovery factor (CRF)
r = 0.0326  # interest rate [%]
q_PV = 20  # [years]
q_bat = 5  # [years]

crf_PV = (r * (1 + r) ** q_PV) / ((1 + r) ** q_PV - 1)
crf_bat = (r * (1 + r) ** q_bat) / ((1 + r) ** q_bat - 1)


class investment_cost:

    def __init__(self, pv_bus, pv_size, **kwargs):  # bess_size_mwh
        # self.net = net
        # self.bus_bar = bus_bar
        self.pv_bus = pv_bus
        self.pv_size = pv_size
        # self.bess_size_mwh = bess_size_mwh

    def cost_inv_pv_test(self):  # INV cost

        if self.pv_bus == 5:   # Ind area
            cost_inv_pv = ((self.pv_size * cost_pv_installation_2023) +
                               (self.pv_size * cost_land_industry_2023 * land_area_pv) * crf_PV)
            print('cost_inv_pv Ind area =', cost_inv_pv)
            return cost_inv_pv

        elif self.pv_bus == 6:   # Business area
            cost_inv_pv = ((self.pv_size * cost_pv_installation_2023) +
                               (self.pv_size * cost_land_business_2023 * land_area_pv) * crf_PV)
            print('cost_inv_pv Busin area =', cost_inv_pv)
            return cost_inv_pv

        else:   # bus = 7
            cost_inv_pv = ((self.pv_size * cost_pv_installation_2023) +
                               (self.pv_size * cost_land_residential_business_2023 * land_area_pv) * crf_PV)
            print('cost_inv_pv Res area =', cost_inv_pv)
            return cost_inv_pv

    def capital_cost_pv_2023(self):     # INV cost
        if self.pv_bus == 14:   # Ind area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2023) +
                               (self.pv_size * cost_land_industry_2023 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 13:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2023) +
                               (self.pv_size * cost_land_industry_2023 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 12:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2023) +
                               (self.pv_size * cost_land_industry_2023 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 7:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2023) +
                               (self.pv_size * cost_land_business_2023 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 6:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2023) +
                               (self.pv_size * cost_land_business_2023 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 8:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2023) +
                               (self.pv_size * cost_land_business_2023 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 9:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2023) +
                               (self.pv_size * cost_land_business_2023 * land_area_pv) * crf_PV)

            return capital_cost_pv

        else:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2023) +
                               (self.pv_size * cost_land_residential_business_2023 * land_area_pv) * crf_PV)

            return capital_cost_pv

    def capital_cost_pv_2024(self):
        if self.pv_bus == 14:  # Ind area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2024) +
                               (self.pv_size * cost_land_industry_2024 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 13:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2024) +
                               (self.pv_size * cost_land_industry_2024 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 12:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2024) +
                               (self.pv_size * cost_land_industry_2024 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 7:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2024) +
                               (self.pv_size * cost_land_business_2024 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 6:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2024) +
                               (self.pv_size * cost_land_business_2024 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 8:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2024) +
                               (self.pv_size * cost_land_business_2024 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 9:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2024) +
                               (self.pv_size * cost_land_business_2024 * land_area_pv) * crf_PV)

            return capital_cost_pv

        else:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2024) +
                               (self.pv_size * cost_land_residential_business_2024 * land_area_pv) * crf_PV)

            return capital_cost_pv

    def capital_cost_pv_2025(self):  # Y3
        if self.pv_bus == 14:  # Ind area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2025) +
                               (self.pv_size * cost_land_industry_2025 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 13:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2025) +
                               (self.pv_size * cost_land_industry_2025 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 12:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2025) +
                               (self.pv_size * cost_land_industry_2025 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 7:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2025) +
                               (self.pv_size * cost_land_business_2025 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 6:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2025) +
                               (self.pv_size * cost_land_business_2025 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 8:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2025) +
                               (self.pv_size * cost_land_business_2025 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 9:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2025) +
                               (self.pv_size * cost_land_business_2025 * land_area_pv) * crf_PV)

            return capital_cost_pv

        else:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2025) +
                               (self.pv_size * cost_land_residential_business_2025 * land_area_pv) * crf_PV)

            return capital_cost_pv

    def capital_cost_pv_2026(self):
        if self.pv_bus == 14: # Ind area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2026) +
                               (self.pv_size * cost_land_industry_2026 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 13:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2026) +
                               (self.pv_size * cost_land_industry_2026 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 12:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2026) +
                               (self.pv_size * cost_land_industry_2026 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 7:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2026) +
                               (self.pv_size * cost_land_business_2026 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 6:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2026) +
                               (self.pv_size * cost_land_business_2026 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 8:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2026) +
                               (self.pv_size * cost_land_business_2026 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 9:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2026) +
                               (self.pv_size * cost_land_business_2026 * land_area_pv) * crf_PV)

            return capital_cost_pv

        else:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2026) +
                               (self.pv_size * cost_land_residential_business_2026 * land_area_pv) * crf_PV)

            return capital_cost_pv

    def capital_cost_pv_2027(self):
        if self.pv_bus == 14:   # Ind area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2027) +
                               (self.pv_size * cost_land_industry_2027 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 13:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2027) +
                               (self.pv_size * cost_land_industry_2027 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 12:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2027) +
                               (self.pv_size * cost_land_industry_2027 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 7:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2027) +
                               (self.pv_size * cost_land_business_2027 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 6:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2027) +
                               (self.pv_size * cost_land_business_2027 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 8:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2027) +
                               (self.pv_size * cost_land_business_2027 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 9:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2027) +
                               (self.pv_size * cost_land_business_2027 * land_area_pv) * crf_PV)

            return capital_cost_pv

        else:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2027) +
                               (self.pv_size * cost_land_residential_business_2027 * land_area_pv) * crf_PV)

            return capital_cost_pv

    def capital_cost_pv_2028(self):
        if self.pv_bus == 14:   # Ind area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2028) +
                               (self.pv_size * cost_land_industry_2028 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 13:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2028) +
                               (self.pv_size * cost_land_industry_2028 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 12:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2028) +
                               (self.pv_size * cost_land_industry_2028 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 7:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2028) +
                               (self.pv_size * cost_land_business_2028 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 6:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2028) +
                               (self.pv_size * cost_land_business_2028 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 8:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2028) +
                               (self.pv_size * cost_land_business_2028 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 9:    # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2028) +
                               (self.pv_size * cost_land_business_2028 * land_area_pv) * crf_PV)

            return capital_cost_pv

        else:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2028) +
                               (self.pv_size * cost_land_residential_business_2028 * land_area_pv) * crf_PV)

            return capital_cost_pv

    def capital_cost_pv_2029(self):
        if self.pv_bus == 14:  # Ind area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2029) +
                               (self.pv_size * cost_land_industry_2029 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 13:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2029) +
                               (self.pv_size * cost_land_industry_2029 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 12:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2029) +
                               (self.pv_size * cost_land_industry_2029 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 7:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2029) +
                               (self.pv_size * cost_land_business_2029 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 6:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2029) +
                               (self.pv_size * cost_land_business_2029 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 8:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2029) +
                               (self.pv_size * cost_land_business_2029 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 9:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2029) +
                               (self.pv_size * cost_land_business_2029 * land_area_pv) * crf_PV)

            return capital_cost_pv

        else:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2029) +
                               (self.pv_size * cost_land_residential_business_2029 * land_area_pv) * crf_PV)

            return capital_cost_pv

    def capital_cost_pv_2030(self):
        if self.pv_bus == 14:  # Ind area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2030) +
                               (self.pv_size * cost_land_industry_2030 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 13:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2030) +
                               (self.pv_size * cost_land_industry_2030 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 12:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2030) +
                               (self.pv_size * cost_land_industry_2030 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 7:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2030) +
                               (self.pv_size * cost_land_business_2030 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 6:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2030) +
                               (self.pv_size * cost_land_business_2030 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 8:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2030) +
                               (self.pv_size * cost_land_business_2030 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 9:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2030) +
                               (self.pv_size * cost_land_business_2030 * land_area_pv) * crf_PV)

            return capital_cost_pv

        else:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2030) +
                               (self.pv_size * cost_land_residential_business_2030 * land_area_pv) * crf_PV)

            return capital_cost_pv

    def capital_cost_pv_2031(self):
        if self.pv_bus == 14:  # Ind area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2031) +
                               (self.pv_size * cost_land_industry_2031 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 13:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2031) +
                               (self.pv_size * cost_land_industry_2031 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 12:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2031) +
                               (self.pv_size * cost_land_industry_2031 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 7:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2031) +
                               (self.pv_size * cost_land_business_2031 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 6:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2031) +
                               (self.pv_size * cost_land_business_2031 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 8:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2031) +
                               (self.pv_size * cost_land_business_2031 * land_area_pv) * crf_PV)

            return capital_cost_pv

        elif self.pv_bus == 9:  # Business area
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2031) +
                               (self.pv_size * cost_land_business_2031 * land_area_pv) * crf_PV)

            return capital_cost_pv

        else:
            capital_cost_pv = ((self.pv_size * cost_pv_installation_2031) +
                               (self.pv_size * cost_land_residential_business_2031 * land_area_pv) * crf_PV)

            return capital_cost_pv

    # ....................... BESS ....................................
    def capital_cost_bess_2023(self):
        capital_cost_bess_2023 = self.bess_size_mwh * cost_bess_installation_2023
        return capital_cost_bess_2023

    def capital_cost_bess_2024(self):
        capital_cost_bess_2024 = self.bess_size_mwh * cost_bess_installation_2024
        return capital_cost_bess_2024

    def capital_cost_bess_2025(self):
        capital_cost_bess_2025 = self.bess_size_mwh * cost_bess_installation_2025
        return capital_cost_bess_2025

