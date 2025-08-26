"""
13.01.2025
"""

import time
start_time = time.time()  # Start the simulation

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

import pandas as pd
import numpy as np

# ........................ PandaPower and Pymoo ........................

import pandapower.networks as pn
from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Real, Integer, Binary

# ........................ Functions ........................
from e_net_mv_20240725 import power_system
from cost_fuct_20240814_CAPEX import PRICE
from cost_func_om_2025_20240816_ubuntu import OPEX
from chp_model_20240716 import CHP
from hp_model_20240718 import hp_model
from tes_dhnet_lp_storage_20240723 import TES
from p2g_model import P2G
from h2_storage_20240724 import HyES
from emission_func_20240909 import emission_calc

# ........................ Power grid ........................
net = pn.create_cigre_network_mv(with_der=False)
net.load.drop(index=net.load.index, inplace=True)
net.sgen.drop(index=net.sgen.index, inplace=True)
net.gen.drop(index=net.gen.index, inplace=True)
net.xward.drop(net.xward.index, inplace=True)
net.shunt.drop(index=net.shunt.index, inplace=True)

# ........................ Fixed Parameters ........................
discount_rate = 0.08

g2025_re_share_max_limit = 0.0
g2026_re_share_max_limit = 0.1
g2027_re_share_max_limit = 0.2
g2028_re_share_max_limit = 0.3
g2029_re_share_max_limit = 0.3
g2030_re_share_max_limit = 0.5
g2031_re_share_max_limit = 0.5
g2032_re_share_max_limit = 0.6
g2033_re_share_max_limit = 0.7
g2034_re_share_max_limit = 0#0.7
g2035_re_share_max_limit = 0#0.7
g2036_re_share_max_limit = 0#0.8
g2037_re_share_max_limit = 0#0.8
g2038_re_share_max_limit = 0#1.0

min_v_drop = 0.05
max_v_drop = 1.05

# ........................ Optimization Function ........................


class MyProblem(ElementwiseProblem):

    def __init__(self, year, stage, **kwargs):
        variables = dict()

        self.year = year
        self.stage = stage
        # self.carried_capacity = carried_capacity
        # self.carried_capacity_pv = carried_capacity_pv
        # self.carried_cap_pv_array_mw = carried_cap_pv_array_mw

        # ************************** PV **************************
        # bus-bars for the PV generators in industrial area
        for k in range(0, 2):
            variables[f"x{k:01}"] = Integer(bounds=(1, 2))
        for k in range(2, 5):
            variables[f"x{k:01}"] = Integer(bounds=(12, 14))

        # bus-bars for the PV generators in commercial/small industry area
        for k in range(5, 8):
            variables[f"x{k:01}"] = Integer(bounds=(3, 5))
        for k in range(8, 13):
            variables[f"x{k:01}"] = Integer(bounds=(7, 11))

        # bus-bars for the PV generators in residential area
        for k in range(13, 14):
            variables[f"x{k:01}"] = Integer(bounds=(6, 6))

        # size of PV generators for all bus-bars
        for k in range(14, 28):
            variables[f"x{k:01}"] = Real(bounds=(0, 1))  # [MW]

        # *********************** WT ****************************
        # bus-bars for the Wind generators
        for k in range(28, 29):
            variables[f"x{k:01}"] = Integer(bounds=(0, 0))

        # size of WT generators at bus 0
        for k in range(29, 30):
            variables[f"x{k:01}"] = Real(bounds=(0, 100))  # [MW]

        # *********************** CHP ****************************
        # CHP bus-bar
        for k in range(30, 31):
            variables[f"x{k:01}"] = Integer(bounds=(6, 6))  # CHP locations is fixed at bus = 6

        # Size of the CHP
        if year == 2025:
            for k in range(31, 32):
                variables[f"x{k:01}"] = Real(bounds=(0.6, 0.6))  # [MW]
        else:
            for k in range(31, 32):
                variables[f"x{k:01}"] = Real(bounds=(0, 0.6))  # [MW]

        # *********************** HP ****************************
        # HP bus-bar
        for k in range(32, 33):
            variables[f"x{k:01}"] = Integer(bounds=(6, 6))      # HP locations is fixed at bus = 6

        # Size of the HP
        if year == 2025:
            for k in range(33, 34):
                variables[f"x{k:01}"] = Real(bounds=(0, 0))  # [MW]
        else:
            for k in range(33, 34):
                variables[f"x{k:01}"] = Real(bounds=(0, 6))  # [MW]

        # *********************** TES ****************************
        # Thermal energy storage (TES)
        for k in range(34, 35):
            variables[f"x{k:01}"] = Real(bounds=(0, 0))  # [MW]

        # *********************** P2G ****************************
        for k in range(35, 36):
            variables[f"x{k:01}"] = Real(bounds=(0, 35))  # [MW]

        # *********************** H2 Storage **********************
        for k in range(36, 37):
            variables[f"x{k:01}"] = Real(bounds=(0, 0))  # [MW]

        # ********************** BESS *****************************
        # Bus 1, 2 & 12 --> big industry
        for k in range(37, 38):
            variables[f"x{k:01}"] = Integer(bounds=(1, 14))

        # Charge/Discharge power rating per hr at bus 1, 2 & 12
        for k in range(38, 39):
            variables[f"x{k:01}"] = Real(bounds=(0, 5))  # [MW]

        # ********************** Gas Gen/Industrial CHP *****************************
        # Bus-bar = 12
        for k in range(39, 40):
            variables[f"x{k:01}"] = Integer(bounds=(12, 12))

        # Size Gas Gen
        if year == 2025:
            for k in range(40, 41):
                variables[f"x{k:01}"] = Real(bounds=(15, 15))  # [MW]
        else:
            for k in range(40, 41):
                variables[f"x{k:01}"] = Real(bounds=(0, 15))  # [MW]

        # Bus-bar = 1
        for k in range(41, 42):
            variables[f"x{k:01}"] = Integer(bounds=(1, 1))

        # Size Gas Gen
        if year == 2025:
            for k in range(42, 43):
                variables[f"x{k:01}"] = Real(bounds=(0.5, 0.5))  # [MW]
        else:
            for k in range(42, 43):
                variables[f"x{k:01}"] = Real(bounds=(0, 0.5))  # [MW]

        super().__init__(vars=variables, n_obj=2, n_ieq_constr=60, **kwargs)

    def _evaluate(self, x, out, *args, **kwargs):

        x = np.array([x[f"x{k:01}"] for k in range(0, 43)])
        # print("X =", x)
        print("stage =", self.stage)

        # ----------------------------- Define x values -----------------------------
        x_pv_bus = x[0:14]
        x_pv_size = x[14:28]
        x_wt_bus = x[28:29]
        x_wt_mw = x[29]
        x_chp_bus = x[30]
        x_chp_mw = x[31]
        x_hp_bus = x[32]
        x_hp_size = x[33]  # mw

        x_storage_th_size = x[34]  # [mwh]
        x_p2g_size_mw = x[35]
        x_storage_h2_mwh = x[36]
        x_bess_bus = x[37]
        x_bess_mw = x[38]

        x_gen_bus_12 = x[39]
        x_gen_bus_12_mw = x[40]
        x_gen_bus_1 = x[41]
        x_gen_bus_1_mw = x[42]

        if self.year == 2025:
            year = 1

            # ******************** CHP ********************
            chp = CHP(chp_mw=x_chp_mw)
            chp_res = chp.chp_calc_new()  # [MW*1h=MWh & m3/hr]
            res_chp_p_mw = chp_res[0]
            res_chp_th_mw = chp_res[1]
            res_chp_gas_import_mw = chp_res[2]  # I will have to change it, because it is counting only one step?
            # print('chp_rated_cap_mw =', x_chp_mw)
            # print("res_chp_p_mw =", res_chp_p_mw)
            # print("res_chp_th_mw =", res_chp_th_mw)
            # print("res_chp_gas_import_mw =", res_chp_gas_import_mw)

            # ******************** HP ********************
            hp_res = hp_model(hp_bus=x_hp_bus, hp_mw=x_hp_size)
            res_hp_th_mw = hp_res.hp()
            # print("x_hp_input_mw=", x_hp_size)
            # print("res_hp_th_mw =", res_hp_th_mw)

            # ******************** Thermal Energy System, Storage Management & Heat Flow ********************
            # -------------------------- 2025 Jan ----------------------------------
            # either produce th_energy from CHP or HP - 2025 only CHP - rest years CHP or HP.
            # how to integrate in the TES function?
            tes_res = TES(chp_th_mwh=res_chp_th_mw, chp_gas_import_mwh=res_chp_gas_import_mw,
                          hp_th_mwh=res_hp_th_mw, storage_th_max_mwh=x_storage_th_size)

            res_tes_jan = tes_res.th_management_system_2025_jan_update()
            res_tes_ch4_import_2025_jan_mwh = res_tes_jan['gas_import_mwh'].sum()
            res_tes_th_loss_2025_jan_mwh = res_tes_jan['th_energy_loss_mwh'].sum()
            res_tes_th_deficit_2025_jan_mwh = np.abs(res_tes_jan['th_energy_deficit_mwh'].sum())  # values are negative,
            # so I am making them +Ve to calculate the Penalty price.

            # print("x_storage_th_size =", x_storage_th_size)
            # print(res_tes_jan)
            # print(res_tes_ch4_import_2025_jan_mwh)
            # print(res_tes_th_loss_2025_jan_mwh)
            # print(res_tes_th_deficit_2025_jan_mwh)

            # -------------------------- 2025 Jul ----------------------------------
            # print("TES 2025 July:")
            res_tes_2025_jul = tes_res.th_management_system_2025_jul_update()
            res_tes_ch4_import_2025_jul_mwh = res_tes_2025_jul['gas_import_mwh'].sum()
            res_tes_th_loss_2025_jul_mwh = res_tes_2025_jul['th_energy_loss_mwh'].sum()
            res_tes_th_deficit_2025_jul_mwh = np.abs(res_tes_2025_jul['th_energy_deficit_mwh'].sum())

            # NEW from 20241116
            res_tes_th_balance_jan = res_tes_jan['heat_balance'].sum()
            res_tes_th_balance_jul = res_tes_2025_jul['heat_balance'].sum()

            # ************************* P2G *********************************
            # print("P2G:")
            p2g_model = P2G(p2g_input_mw=x_p2g_size_mw)
            # h2_production_m3_s = p2g_model.p2g_model()[0]
            # h2_production_m3_hr = p2g_model.p2g_model()[1]
            h2_production_mwh = p2g_model.p2g_model()[2]

            # ************************* H2 Energy System, Storage Management & Hy Flow *****************************
            # print("GES:")
            ges_res = HyES(p2g_input_mw=x_p2g_size_mw, h2_production_mwh=h2_production_mwh,
                           storage_h2_max_mwh=x_storage_h2_mwh)

            # -------------------------- 2025 Jan ----------------------------------
            res_ges_2025_jan = ges_res.h2_management_system_2025_jan_update()
            h2_blue_import_2025_jan_mwh = np.abs(res_ges_2025_jan['blue_h2_mwh'].sum())  # Covert to +Ve
            h2_energy_loss_2025_jan_mwh = res_ges_2025_jan['h2_energy_loss_mwh'].sum()
            # print(res_ges_2025_jan)
            # print(h2_blue_import_2025_jan_mwh)

            # -------------------------- 2025 Jul ----------------------------------
            res_ges_2025_jul = ges_res.h2_management_system_2025_jul()
            h2_blue_import_2025_jul_mwh = np.abs(res_ges_2025_jul['blue_h2_mwh'].sum())  # Covert to +Ve
            h2_energy_loss_2025_jul_mwh = res_ges_2025_jul['h2_energy_loss_mwh'].sum()
            # print(res_ges_2025_jul)
            # print(h2_blue_import_2025_jul_mwh)

            # ***************************************** POWER SYSTEM & BESS ****************************************
            # print("Power System 2025 Jan:")
            p_sys = power_system(net=net, x=x, x_pv_bus=x_pv_bus, x_pv_mw=x_pv_size,
                                 x_wt_bus=x_wt_bus, x_wt_mw=x_wt_mw,
                                 chp_bus=x_chp_bus, chp_p_mw=res_chp_p_mw,
                                 hp_bus=x_hp_bus, hp_cap_mw=x_hp_size,
                                 p2g_input_mw=x_p2g_size_mw, bess_bus=x_bess_bus, bess_p_mw=x_bess_mw,
                                 x_gen_bus_12=x_gen_bus_12, x_gen_bus_12_mw=x_gen_bus_12_mw,
                                 x_gen_bus_1=x_gen_bus_1, x_gen_bus_1_mw=x_gen_bus_1_mw)
            res_p_sys_2025_jan = p_sys.power_flow_2025_jan_NEW()
            vm_jan = res_p_sys_2025_jan.iloc[:, 6:20]
            # print("vm =", vm)
            power_balance_2025_jan = res_p_sys_2025_jan.iloc[:, 0:7]
            res_line_loss_mw_2025_jan_mwh = res_p_sys_2025_jan['line_loss_mw'].sum()
            print(power_balance_2025_jan)
            # print(res_line_loss_mw_2025_jan_mwh)

            p_sys.remove_sgen()
            p_sys.remove_gen()
            p_sys.remove_load()
            p_sys.remove_bess()

            # ------------------------- POWER SYSTEM July 2025 -------------------------
            res_p_sys_2025_jul = p_sys.power_flow_2025_jul()
            vm_jul = res_p_sys_2025_jul.iloc[:, 6:20]
            power_balance_2025_jul = res_p_sys_2025_jul.iloc[:, 0:6]
            res_line_loss_mw_2025_jul_mwh = power_balance_2025_jul['line_loss_mw'].sum()

            # print(power_balance_2025_jul)

            p_sys.remove_sgen()
            p_sys.remove_gen()
            p_sys.remove_load()
            p_sys.remove_bess()

            # ================================================= F1 2025 ===========================================
            # --------------------------------------- CAPEX 2025 --------------------------------------
            # print("CAPEX for 19 years:")
            cost = PRICE(stage=self.stage, year=year,
                         x_pv_bus=x_pv_bus, x_pv_size=capex_x_pv_mw,
                         x_wt_bus=x_wt_bus, x_wt_mw=capex_x_wt_mw,
                         x_chp_bus=x_chp_bus, x_chp_mw=capex_x_chp_mw,
                         x_hp_bus=x_hp_bus, x_hp_size=capex_x_hp_mw,
                         x_storage_th_size=capex_x_storage_th_mw,
                         x_p2g_size_mw=capex_x_p2g_mw,
                         x_storage_h2_mwh=capex_x_storage_h2_mwh,
                         x_bess_bus=x_bess_bus, x_bess_mw=capex_x_bess_mw
                         )

            price_invest_pv_2025 = cost.price_capex_pv_2025()
            price_invest_wt_2025 = cost.price_capex_wt_2025()
            price_invest_chp_2025 = cost.price_capex_chp_2025()
            price_invest_hp_2025 = cost.price_capex_hp_2025()
            price_invest_storage_th_2025 = cost.price_capex_storage_th_2025()
            price_invest_p2g_2025 = cost.price_capex_p2g_2025()
            price_invest_storage_h2_2025 = cost.price_capex_h2_storage_2025()
            price_invest_bess_2025 = cost.price_capex_bess_2025()
            # print("capex_pv_2025_eur =", price_invest_pv_2025)
            # print("capex_chp_2025_eur =", price_invest_chp_2025)

            price_invest_2025_tot = price_invest_pv_2025 + price_invest_wt_2025 + price_invest_chp_2025 + price_invest_hp_2025 + \
                                    price_invest_storage_th_2025 + price_invest_p2g_2025 + price_invest_storage_h2_2025 \
                                    + price_invest_bess_2025
            # print("price_invest_2025_tot =", price_invest_2025_tot)

            capex_2025_pv = price_invest_2025_tot * (1 / (1 + discount_rate) ** self.stage)
            # print("capex_pv_2025 =", price_invest_2025_tot)
            # capex_pv_2025_eac = price_invest_pv_2025 / ((1-(1/(1+discount_rate)**stage_num))/discount_rate)

        elif self.year == 2026:
            year = 2
        elif self.year == 2027:
            year = 3


# ----------------------------------------------- Optimization Function ------------------------------------------------
from pymoo.algorithms.moo.nsga2 import NSGA2, RankAndCrowdingSurvival
from pymoo.core.mixed import MixedVariableMating, MixedVariableGA, MixedVariableSampling, \
    MixedVariableDuplicateElimination
from pymoo.optimize import minimize
from pymoo.factory import get_termination

from pymoo.operators.crossover.sbx import SimulatedBinaryCrossover
from pymoo.operators.mutation.pm import PolynomialMutation

# Simulated Binary Crossover (SBX) with a custom eta and probability
crossover = SimulatedBinaryCrossover(prob=0.9, eta=15)
mutation = PolynomialMutation(prob=0.1, eta=20)  # prob is the mutation probability, eta controls mutation spread

pop_size = 1
gen_size = 1

stages = {
    1: [2025, 2026, 2027],    # Stage 1
    # 2: [2028, 2029, 2030],    # Stage 2
    # 3: [2031, 2032, 2033],    # Stage 3
}
years = list(range(2025, 2028))

for year in years:
    print("----------------- YEAR: ----------------------")
    print('------------------', year, '---------------------')
    print("----------------------------------------------")

    if year == 2025 and 2026 and 2027:
        stage = 1
    # elif year == 2028 and 2029 and 2030:
    #     stage = 2
    # elif year == 2031 and 2032 and 2033:
    #     stage = 3

    prob = MyProblem(year=year, stage=stage)

    algorithm = MixedVariableGA(pop_size=pop_size,
                                Sampling=MixedVariableSampling(),
                                mating=MixedVariableMating(eliminate_duplicates=MixedVariableDuplicateElimination()),
                                element_duplicates=MixedVariableDuplicateElimination(),
                                survival=RankAndCrowdingSurvival(),
                                crossover=crossover,
                                mutation=mutation,
                                eliminate_duplicates=False
                                )

    termination = get_termination("n_gen", gen_size)

    res = minimize(prob,
                   algorithm,
                   termination,
                   seed=1,
                   # output=MyOutput(),
                   save_history=True,
                   verbose=True)

    X = res.X
    F = res.F

    # best_idx = np.argmin(F[:, 0])
    # best_solution = X[best_idx]  # old: X
    # best_objective = F[best_idx]

    # print("Best Solution:", best_solution)
    print("Best Objective Value:", F)