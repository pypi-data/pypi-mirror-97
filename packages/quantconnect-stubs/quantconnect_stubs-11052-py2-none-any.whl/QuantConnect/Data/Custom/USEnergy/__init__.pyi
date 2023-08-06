import datetime

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Custom.USEnergy
import System
import System.Collections.Generic


class USEnergy(QuantConnect.Data.BaseData):
    """United States Energy Information Administration (EIA). This loads U.S. Energy data from QuantConnect's cache."""

    class Petroleum(System.Object):
        """Petroleum"""

        class UnitedStates(System.Object):
            """United States"""

            WeeklyRefinerAndBlenderAdjustedNetProductionOfFinishedMotorGasoline: str = "PET.WGFRPUS2.W"
            """U.S. Refiner and Blender Adjusted Net Production of Finished Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfFinishedMotorGasoline: str = "PET.WGFSTUS1.W"
            """U.S. Ending Stocks of Finished Motor Gasoline in Thousand Barrels (Mbbl)"""

            WeeklyProductSuppliedOfFinishedMotorGasoline: str = "PET.WGFUPUS2.W"
            """U.S. Product Supplied of Finished Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfCrudeOilInSpr: str = "PET.WCSSTUS1.W"
            """U.S. Ending Stocks of Crude Oil in SPR in Thousand Barrels (Mbbl)"""

            WeeklyRefinerAndBlenderNetProductionOfDistillateFuelOilGreaterThan500PpmSulfur: str = "PET.WDGRPUS2.W"
            """U.S.  Refiner and Blender Net Production of Distillate Fuel Oil Greater than 500 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfDistillateFuelOilGreaterThan500PpmSulfur: str = "PET.WDGSTUS1.W"
            """U.S. Ending Stocks of Distillate Fuel Oil, Greater Than 500 ppm Sulfur in Thousand Barrels (Mbbl)"""

            WeeklyExportsOfTotalDistillate: str = "PET.WDIEXUS2.W"
            """U.S. Exports of Total Distillate in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfDistillateFuelOil: str = "PET.WDIIMUS2.W"
            """U.S. Imports of Distillate Fuel Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerAndBlenderNetProductionOfDistillateFuelOil: str = "PET.WDIRPUS2.W"
            """U.S. Refiner and Blender Net Production of Distillate Fuel Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfKeroseneTypeJetFuel: str = "PET.WKJSTUS1.W"
            """U.S. Ending Stocks of Kerosene-Type Jet Fuel in Thousand Barrels (Mbbl)"""

            WeeklyProductSuppliedOfKeroseneTypeJetFuel: str = "PET.WKJUPUS2.W"
            """U.S. Product Supplied of Kerosene-Type Jet Fuel in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfTotalGasoline: str = "PET.WGTIMUS2.W"
            """U.S. Imports of Total Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfTotalGasoline: str = "PET.WGTSTUS1.W"
            """U.S. Ending Stocks of Total Gasoline in Thousand Barrels (Mbbl)"""

            WeeklyGrossInputsIntoRefineries: str = "PET.WGIRIUS2.W"
            """U.S. Gross Inputs into Refineries in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfReformulatedMotorGasoline: str = "PET.WGRIMUS2.W"
            """U.S. Imports of Reformulated Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerAndBlenderNetProductionOfReformulatedMotorGasoline: str = "PET.WGRRPUS2.W"
            """U.S. Refiner and Blender Net Production of Reformulated Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfReformulatedMotorGasoline: str = "PET.WGRSTUS1.W"
            """U.S. Ending Stocks of Reformulated Motor Gasoline in Thousand Barrels (Mbbl)"""

            WeeklyEndingStocksOfDistillateFuelOil: str = "PET.WDISTUS1.W"
            """U.S. Ending Stocks of Distillate Fuel Oil in Thousand Barrels (Mbbl)"""

            WeeklyProductSuppliedOfDistillateFuelOil: str = "PET.WDIUPUS2.W"
            """U.S. Product Supplied of Distillate Fuel Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerAndBlenderNetProductionOfMilitaryKeroseneTypeJetFuel: str = "PET.WKMRPUS2.W"
            """U.S.  Refiner and Blender Net Production of Military Kerosene-Type Jet Fuel in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyOperableCrudeOilDistillationCapacity: str = "PET.WOCLEUS2.W"
            """U. S. Operable Crude Oil Distillation Capacity in Thousand Barrels per Calendar Day (Mbbl/d)"""

            WeeklyPropyleneNonfuelUseStocksAtBulkTerminals: str = "PET.WPLSTUS1.W"
            """U.S. Propylene Nonfuel Use Stocks at Bulk Terminals in Thousand Barrels (Mbbl)"""

            WeeklyEndingStocksOfPropaneAndPropylene: str = "PET.WPRSTUS1.W"
            """U.S. Ending Stocks of Propane and Propylene in Thousand Barrels (Mbbl)"""

            WeeklyPercentUtilizationOfRefineryOperableCapacity: str = "PET.WPULEUS3.W"
            """U.S. Percent Utilization of Refinery Operable Capacity in Percent (%)"""

            WeeklyExportsOfResidualFuelOil: str = "PET.WREEXUS2.W"
            """U.S. Exports of Residual Fuel Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfResidualFuelOil: str = "PET.WREIMUS2.W"
            """U.S. Imports of Residual Fuel Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerAndBlenderNetProductionOfCommercialKeroseneTypeJetFuel: str = "PET.WKCRPUS2.W"
            """U.S.  Refiner and Blender Net Production of Commercial Kerosene-Type Jet Fuel in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyExportsOfKeroseneTypeJetFuel: str = "PET.WKJEXUS2.W"
            """U.S. Exports of Kerosene-Type Jet Fuel in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfKeroseneTypeJetFuel: str = "PET.WKJIMUS2.W"
            """U.S. Imports of Kerosene-Type Jet Fuel in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerAndBlenderNetProductionOfKeroseneTypeJetFuel: str = "PET.WKJRPUS2.W"
            """U.S. Refiner and Blender Net Production of Kerosene-Type Jet Fuel in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksExcludingSprOfCrudeOil: str = "PET.WCESTUS1.W"
            """U.S. Ending Stocks excluding SPR of Crude Oil in Thousand Barrels (Mbbl)"""

            WeeklyExportsOfCrudeOil: str = "PET.WCREXUS2.W"
            """U.S. Exports of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyFieldProductionOfCrudeOil: str = "PET.WCRFPUS2.W"
            """U.S. Field Production of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfCrudeOil: str = "PET.WCRIMUS2.W"
            """U.S. Imports of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyNetImportsOfCrudeOil: str = "PET.WCRNTUS2.W"
            """U.S. Net Imports of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetInputOfCrudeOil: str = "PET.WCRRIUS2.W"
            """U.S. Refiner Net Input of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerAndBlenderNetProductionOfResidualFuelOil: str = "PET.WRERPUS2.W"
            """U.S. Refiner and Blender Net Production of Residual Fuel Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfResidualFuelOil: str = "PET.WRESTUS1.W"
            """U.S. Ending Stocks of Residual Fuel Oil in Thousand Barrels (Mbbl)"""

            WeeklyProductSuppliedOfResidualFuelOil: str = "PET.WREUPUS2.W"
            """U.S. Product Supplied of Residual Fuel Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyExportsOfTotalPetroleumProducts: str = "PET.WRPEXUS2.W"
            """U.S. Exports of Total Petroleum Products in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfTotalPetroleumProducts: str = "PET.WRPIMUS2.W"
            """U.S. Imports of Total Petroleum Products in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyNetImportsOfTotalPetroleumProducts: str = "PET.WRPNTUS2.W"
            """U.S. Net Imports of Total Petroleum Products in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyProductSuppliedOfPetroleumProducts: str = "PET.WRPUPUS2.W"
            """U.S. Product Supplied of Petroleum Products in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksExcludingSprOfCrudeOilAndPetroleumProducts: str = "PET.WTESTUS1.W"
            """U.S. Ending Stocks excluding SPR of Crude Oil and Petroleum Products in Thousand Barrels (Mbbl)"""

            WeeklyExportsOfCrudeOilAndPetroleumProducts: str = "PET.WTTEXUS2.W"
            """U.S. Exports of Crude Oil and Petroleum Products in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfCrudeOilAndPetroleumProducts: str = "PET.WTTIMUS2.W"
            """U.S. Imports of Crude Oil and Petroleum Products in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyNetImportsOfCrudeOilAndPetroleumProducts: str = "PET.WTTNTUS2.W"
            """U.S. Net Imports of Crude Oil and Petroleum Products in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfCrudeOilAndPetroleumProducts: str = "PET.WTTSTUS1.W"
            """U.S. Ending Stocks of Crude Oil and Petroleum Products in Thousand Barrels (Mbbl)"""

            WeeklyEndingStocksOfUnfinishedOils: str = "PET.WUOSTUS1.W"
            """U.S. Ending Stocks of Unfinished Oils in Thousand Barrels (Mbbl)"""

            WeeklyRefinerAndBlenderNetProductionOfOtherFinishedConventionalMotorGasoline: str = "PET.WG6TP_NUS_2.W"
            """U.S. Refiner and Blender Net Production of Other Finished Conventional Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerAndBlenderNetProductionOfDistillateFuelOil0To15PpmSulfur: str = "PET.WD0TP_NUS_2.W"
            """U.S. Refiner and Blender Net Production of Distillate Fuel Oil, 0 to 15 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfDistillateFuelOilGreaterThan15To500PpmSulfur: str = "PET.WD1ST_NUS_1.W"
            """U.S. Ending Stocks of Distillate Fuel Oil, Greater than 15 to 500 ppm Sulfur in Thousand Barrels (Mbbl)"""

            WeeklyProductionOfDistillateFuelOilGreaterThan15To500PpmSulfur: str = "PET.WD1TP_NUS_2.W"
            """U.S. Production of Distillate Fuel Oil, Greater than 15 to 500 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfReformulatedMotorGasolineWithFuelAlcohol: str = "PET.WG1ST_NUS_1.W"
            """U.S. Ending Stocks of Reformulated Motor Gasoline with Fuel ALcohol in Thousand Barrels (Mbbl)"""

            WeeklyEndingStocksOfCrudeOil: str = "PET.WCRSTUS1.W"
            """U.S. Ending Stocks of Crude Oil in Thousand Barrels (Mbbl)"""

            WeeklyCrudeOilImportsBySpr: str = "PET.WCSIMUS2.W"
            """U.S. Crude Oil Imports by SPR in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfGasolineBlendingComponents: str = "PET.WBCIMUS2.W"
            """U.S. Imports of Gasoline Blending Components in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfGasolineBlendingComponents: str = "PET.WBCSTUS1.W"
            """U.S. Ending Stocks of Gasoline Blending Components in Thousand Barrels (Mbbl)"""

            WeeklyCommercialCrudeOilImportsExcludingSpr: str = "PET.WCEIMUS2.W"
            """U.S. Commercial Crude Oil Imports Excluding SPR in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerBlenderAndGasPlantNetProductionOfPropaneAndPropylene: str = "PET.WPRTP_NUS_2.W"
            """U.S. Refiner, Blender, and Gas Plant Net Production of Propane and Propylene in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerAndBlenderNetProductionOfFinishedReformulatedMotorGasolineWithEthanol: str = "PET.WG1TP_NUS_2.W"
            """U.S. Refiner and Blender Net Production of Finished Reformulated Motor Gasoline with Ethanol in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfReformulatedMotorGasolineNonOxygentated: str = "PET.WG3ST_NUS_1.W"
            """U.S. Ending Stocks of Reformulated Motor Gasoline, Non-Oxygentated in Thousand Barrels (Mbbl)"""

            WeeklyEndingStocksOfConventionalMotorGasoline: str = "PET.WG4ST_NUS_1.W"
            """U.S. Ending Stocks of Conventional Motor Gasoline in Thousand Barrels (Mbbl)"""

            WeeklyRefinerAndBlenderNetProductionOfConventionalMotorGasoline: str = "PET.WG4TP_NUS_2.W"
            """U.S. Refiner and Blender Net Production of Conventional Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfConventionalMotorGasolineWithFuelEthanol: str = "PET.WG5ST_NUS_1.W"
            """U.S. Ending Stocks of Conventional Motor Gasoline with Fuel Ethanol in Thousand Barrels (Mbbl)"""

            WeeklyRefinerAndBlenderNetProductionOfFinishedConventionalMotorGasolineWithEthanol: str = "PET.WG5TP_NUS_2.W"
            """U.S. Refiner and Blender Net Production of Finished Conventional Motor Gasoline with Ethanol in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfOtherConventionalMotorGasoline: str = "PET.WG6ST_NUS_1.W"
            """U.S. Ending Stocks of Other Conventional Motor Gasoline in Thousand Barrels (Mbbl)"""

            WeeklyRefinerAndBlenderNetInputOfConventionalCbobGasolineBlendingComponents: str = "PET.WO6RI_NUS_2.W"
            """U.S. Refiner and Blender Net Input of Conventional CBOB Gasoline Blending Components in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfConventionalCbobGasolineBlendingComponents: str = "PET.WO6ST_NUS_1.W"
            """U.S. Ending Stocks of Conventional CBOB Gasoline Blending Components in Thousand Barrels (Mbbl)"""

            WeeklyRefinerAndBlenderNetInputOfConventionalGtabGasolineBlendingComponents: str = "PET.WO7RI_NUS_2.W"
            """U.S. Refiner and Blender Net Input of Conventional GTAB Gasoline Blending Components in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfConventionalGtabGasolineBlendingComponents: str = "PET.WO7ST_NUS_1.W"
            """U.S. Ending Stocks of Conventional GTAB Gasoline Blending Components in Thousand Barrels (Mbbl)"""

            WeeklyRefinerAndBlenderNetInputOfConventionalOtherGasolineBlendingComponents: str = "PET.WO9RI_NUS_2.W"
            """U.S. Refiner and Blender Net Input of Conventional Other Gasoline Blending Components in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfConventionalOtherGasolineBlendingComponents: str = "PET.WO9ST_NUS_1.W"
            """U.S. Ending Stocks of Conventional Other Gasoline Blending Components in Thousand Barrels (Mbbl)"""

            WeeklyNo2HeatingOilWholesaleResalePrice: str = "PET.W_EPD2F_PWR_NUS_DPG.W"
            """U.S. No. 2 Heating Oil Wholesale/Resale Price in Dollars per Gallon ($/gal)"""

            WeeklyCrudeOilStocksInTransitOnShipsFromAlaska: str = "PET.W_EPC0_SKA_NUS_MBBL.W"
            """U.S. Crude Oil Stocks in Transit (on Ships) from Alaska in Thousand Barrels (Mbbl)"""

            WeeklyDaysOfSupplyOfCrudeOilExcludingSpr: str = "PET.W_EPC0_VSD_NUS_DAYS.W"
            """U.S. Days of Supply of Crude Oil excluding SPR in Number of Days (Days)"""

            WeeklyDaysOfSupplyOfTotalDistillate: str = "PET.W_EPD0_VSD_NUS_DAYS.W"
            """U.S. Days of Supply of Total Distillate in Number of Days (Days)"""

            WeeklyWeeklyNo2HeatingOilResidentialPrice: str = "PET.W_EPD2F_PRS_NUS_DPG.W"
            """U.S. Weekly No. 2 Heating Oil Residential Price in Dollars per Gallon ($/gal)"""

            WeeklyProductSuppliedOfPropaneAndPropylene: str = "PET.WPRUP_NUS_2.W"
            """U.S. Product Supplied of Propane and Propylene in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyProductSuppliedOfOtherOils: str = "PET.WWOUP_NUS_2.W"
            """U.S. Product Supplied of Other Oils in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerAndBlenderNetInputOfGasolineBlendingComponents: str = "PET.WBCRI_NUS_2.W"
            """U.S. Refiner and Blender Net Input of Gasoline Blending Components in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfDistillateFuelOil0To15PpmSulfur: str = "PET.WD0ST_NUS_1.W"
            """U.S. Ending Stocks of Distillate Fuel Oil, 0 to 15 ppm Sulfur in Thousand Barrels (Mbbl)"""

            WeeklyDaysOfSupplyOfKeroseneTypeJetFuel: str = "PET.W_EPJK_VSD_NUS_DAYS.W"
            """U.S. Days of Supply of Kerosene-Type Jet Fuel in Number of Days (Days)"""

            WeeklyDaysOfSupplyOfTotalGasoline: str = "PET.W_EPM0_VSD_NUS_DAYS.W"
            """U.S. Days of Supply of Total Gasoline in Number of Days (Days)"""

            WeeklyEndingStocksOfAsphaltAndRoadOil: str = "PET.W_EPPA_SAE_NUS_MBBL.W"
            """U.S. Ending Stocks of Asphalt and Road Oil in Thousand Barrels (Mbbl)"""

            WeeklyEndingStocksOfKerosene: str = "PET.W_EPPK_SAE_NUS_MBBL.W"
            """U.S. Ending Stocks of Kerosene in Thousand Barrels (Mbbl)"""

            WeeklySupplyAdjustmentOfDistillateFuelOilGreaterThan15To500PpmSulfur: str = "PET.W_EPDM10_VUA_NUS_2.W"
            """U.S. Supply Adjustment of Distillate Fuel Oil, Greater than 15 to 500 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfConventionalMotorGasolineWithFuelEthanol: str = "PET.WG5IM_NUS-Z00_2.W"
            """U.S. Imports of Conventional Motor Gasoline with Fuel Ethanol in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfOtherConventionalMotorGasoline: str = "PET.WG6IM_NUS-Z00_2.W"
            """U.S. Imports of Other Conventional Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfDistillateFuelOil0To15PpmSulfur: str = "PET.WD0IM_NUS-Z00_2.W"
            """U.S. Imports of Distillate Fuel Oil, 0 to 15 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfDistillateFuelOilGreaterThan15To500PpmSulfur: str = "PET.WD1IM_NUS-Z00_2.W"
            """U.S. Imports of Distillate Fuel Oil, Greater than 15 to 500 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfDistillateFuelOilGreaterThan500To2000PpmSulfur: str = "PET.WD2IM_NUS-Z00_2.W"
            """U.S. Imports of Distillate Fuel Oil, Greater than 500 to 2000 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfPropaneAndPropylene: str = "PET.WPRIM_NUS-Z00_2.W"
            """U.S. Imports of Propane and Propylene in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfConventionalGtabGasolineBlendingComponents: str = "PET.WO7IM_NUS-Z00_2.W"
            """U.S. Imports of Conventional GTAB Gasoline Blending Components in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfDistillateFuelOilGreaterThan2000PpmSulfur: str = "PET.WD3IM_NUS-Z00_2.W"
            """U.S. Imports of Distillate Fuel Oil, Greater than 2000 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfReformulatedMotorGasolineWithFuelAlcohol: str = "PET.WG1IM_NUS-Z00_2.W"
            """U.S. Imports of Reformulated Motor Gasoline with Fuel ALcohol in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfConventionalMotorGasoline: str = "PET.WG4IM_NUS-Z00_2.W"
            """U.S. Imports of Conventional Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfConventionalOtherGasolineBlendingComponents: str = "PET.WO9IM_NUS-Z00_2.W"
            """U.S. Imports of Conventional Other Gasoline Blending Components in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfConventionalCbobGasolineBlendingComponents: str = "PET.WO6IM_NUS-Z00_2.W"
            """U.S. Imports of Conventional CBOB Gasoline Blending Components in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyBlenderNetProductionOfKerosene: str = "PET.W_EPPK_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Kerosene in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfKerosene: str = "PET.W_EPPK_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Kerosene in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfOtherOilsExcludingFuelEthanol: str = "PET.W_EPPO6_SAE_NUS_MBBL.W"
            """U.S. Ending Stocks of Other Oils (Excluding Fuel Ethanol) in Thousand Barrels (Mbbl)"""

            WeeklyRefinerNetProductionOfResidualFuelOil: str = "PET.W_EPPR_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Residual Fuel Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyBlenderNetProductionOfReformulatedMotorGasoline: str = "PET.W_EPM0R_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Reformulated Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfReformulatedMotorGasoline: str = "PET.W_EPM0R_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Reformulated Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfFuelEthanol: str = "PET.W_EPOOXE_SAE_NUS_MBBL.W"
            """U.S. Ending Stocks of Fuel Ethanol in Thousand Barrels (Mbbl)"""

            WeeklyBlenderNetProductionOfDistillateFuelOil: str = "PET.W_EPD0_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Distillate Fuel Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfDistillateFuelOil: str = "PET.W_EPD0_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Distillate Fuel Oil in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyBlenderNetProductionOfKeroseneTypeJetFuel: str = "PET.W_EPJK_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Kerosene-Type Jet Fuel in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfKeroseneTypeJetFuel: str = "PET.W_EPJK_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Kerosene-Type Jet Fuel in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyPropaneResidentialPrice: str = "PET.W_EPLLPA_PRS_NUS_DPG.W"
            """U.S. Propane Residential Price in Dollars per Gallon ($/gal)"""

            WeeklyPropaneWholesaleResalePrice: str = "PET.W_EPLLPA_PWR_NUS_DPG.W"
            """U.S. Propane Wholesale/Resale Price in Dollars per Gallon ($/gal)"""

            WeeklyRefinerAndBlenderNetInputOfMotorGasolineBlendingComponentsRbob: str = "PET.W_EPOBGRR_YIR_NUS_MBBLD.W"
            """U.S. Refiner and Blender Net Input of Motor Gasoline Blending Components, RBOB in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfNgplsLrgsExcludingPropanePropylene: str = "PET.W_EPL0XP_SAE_NUS_MBBL.W"
            """U.S. Ending Stocks of NGPLs/LRGs (Excluding Propane/Propylene) in Thousand Barrels (Mbbl)"""

            WeeklyDaysOfSupplyOfPropanePropylene: str = "PET.W_EPLLPZ_VSD_NUS_DAYS.W"
            """U.S. Days of Supply of Propane/Propylene in Number of Days (Days)"""

            WeeklyBlenderNetProductionOfConventionalMotorGasoline: str = "PET.W_EPM0C_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Conventional Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfConventionalMotorGasoline: str = "PET.W_EPM0C_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Conventional Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklySupplyAdjustmentOfFinishedMotorGasoline: str = "PET.W_EPM0F_VUA_NUS_MBBLD.W"
            """U.S. Supply Adjustment of Finished Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyBlenderNetProductionOfFinishedMotorGasoline: str = "PET.W_EPM0F_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Finished Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerAndBlenderNetProductionOfFinishedMotorGasoline: str = "PET.W_EPM0F_YPR_NUS_MBBLD.W"
            """U.S. Refiner and Blender Net Production of Finished Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfFinishedMotorGasoline: str = "PET.W_EPM0F_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Finished Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyBlenderNetProductionOfDistillateFuelOilGreaterThan500PpmSulfur: str = "PET.W_EPD00H_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Distillate Fuel Oil, Greater Than 500 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfDistillateFuelOilGreaterThan500PpmSulfur: str = "PET.W_EPD00H_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Distillate Fuel Oil, Greater Than 500 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyBlenderNetProductionOfDistillateFuelOilGreaterThan15To500PpmSulfur: str = "PET.W_EPDM10_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Distillate Fuel Oil, Greater than 15 to 500 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfDistillateFuelOilGreaterThan15To500PpmSulfur: str = "PET.W_EPDM10_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Distillate Fuel Oil, Greater than 15 to 500 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyBlenderNetProductionOfDistillateFuelOil0To15PpmSulfur: str = "PET.W_EPDXL0_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Distillate Fuel Oil, 0 to 15 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfDistillateFuelOil0To15PpmSulfur: str = "PET.W_EPDXL0_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Distillate Fuel Oil, 0 to 15 ppm Sulfur in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyBlenderNetProductionOfConventionalMotorGasolineWithFuelEthanol: str = "PET.W_EPM0CA_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Conventional Motor Gasoline with Fuel Ethanol in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfConventionalMotorGasolineWithFuelEthanol: str = "PET.W_EPM0CA_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Conventional Motor Gasoline with Fuel Ethanol in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyBlenderNetProductionOfOtherConventionalMotorGasoline: str = "PET.W_EPM0CO_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Other Conventional Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfOtherConventionalMotorGasoline: str = "PET.W_EPM0CO_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Other Conventional Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyBlenderNetProductionOfReformulatedMotorGasolineWithFuelAlcohol: str = "PET.W_EPM0RA_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Reformulated Motor Gasoline with Fuel ALcohol in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfReformulatedMotorGasolineWithFuelAlcohol: str = "PET.W_EPM0RA_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Reformulated Motor Gasoline with Fuel ALcohol in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyOxygenatePlantProductionOfFuelEthanol: str = "PET.W_EPOOXE_YOP_NUS_MBBLD.W"
            """U.S. Oxygenate Plant Production of Fuel Ethanol in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyBlenderNetProductionOfMotorGasolineFinishedConventionalEd55AndLower: str = "PET.W_EPM0CAL55_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Motor Gasoline, Finished, Conventional, Ed55 and Lower in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerAndBlenderNetProductionOfFinishedConventionalMotorGasolineEd55AndLower: str = "PET.W_EPM0CAL55_YPT_NUS_MBBLD.W"
            """U.S. Refiner and Blender Net Production of Finished Conventional Motor Gasoline, Ed 55 and Lower in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfMotorGasolineFinishedConventionalEd55AndLower: str = "PET.W_EPM0CAL55_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Motor Gasoline, Finished, Conventional, Ed55 and Lower in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyExportsOfFinishedMotorGasoline: str = "PET.W_EPM0F_EEX_NUS-Z00_MBBLD.W"
            """U.S. Exports of Finished Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfFinishedMotorGasoline: str = "PET.W_EPM0F_IM0_NUS-Z00_MBBLD.W"
            """U.S. Imports of Finished Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyBlenderNetProductionOfOtherReformulatedMotorGasoline: str = "PET.W_EPM0RO_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Other Reformulated Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerAndBlenderNetProductionOfOtherFinishedReformulatedMotorGasoline: str = "PET.W_EPM0RO_YPT_NUS_MBBLD.W"
            """U.S. Refiner and Blender Net Production of Other Finished Reformulated Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfOtherReformulatedMotorGasoline: str = "PET.W_EPM0RO_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Other Reformulated Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfMotorGasolineBlendingComponentsRbob: str = "PET.W_EPOBGRR_SAE_NUS_MBBL.W"
            """U.S. Ending Stocks of Motor Gasoline Blending Components, RBOB in Thousand Barrels (Mbbl)"""

            WeeklyRefinerAndBlenderNetInputOfFuelEthanol: str = "PET.W_EPOOXE_YIR_NUS_MBBLD.W"
            """U.S. Refiner and Blender Net Input of Fuel Ethanol in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfMotorGasolineFinishedConventionalGreaterThanEd55: str = "PET.W_EPM0CAG55_IM0_NUS-Z00_MBBLD.W"
            """U.S. Imports of Motor Gasoline, Finished, Conventional, Greater than Ed55 in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfMotorGasolineFinishedConventionalEd55AndLower: str = "PET.W_EPM0CAL55_IM0_NUS-Z00_MBBLD.W"
            """U.S. Imports of Motor Gasoline, Finished, Conventional, Ed55 and Lower in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyCrudeOilImportsForSprByOthers: str = "PET.W_EPC0_IMU_NUS-Z00_MBBLD.W"
            """U.S. Crude Oil Imports for SPR by Others in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfConventionalMotorGasolineGreaterThanEd55: str = "PET.W_EPM0CAG55_SAE_NUS_MBBL.W"
            """U.S. Ending Stocks of Conventional Motor Gasoline, Greater than Ed55 in Thousand Barrels (Mbbl)"""

            WeeklyImportsOfFuelEthanol: str = "PET.W_EPOOXE_IM0_NUS-Z00_MBBLD.W"
            """U.S. Imports of Fuel Ethanol in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfLiquefiedPetroleumGassesLessPropanePropylene: str = "PET.W_EPL0XP_IM0_NUS-Z00_MBBLD.W"
            """U.S. Imports of Liquefied Petroleum Gasses Less Propane/Propylene in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyExportsOfPropaneAndPropylene: str = "PET.W_EPLLPZ_EEX_NUS-Z00_MBBLD.W"
            """U.S. Exports of Propane and Propylene in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfOtherReformulatedMotorGasoline: str = "PET.W_EPM0RO_IM0_NUS-Z00_MBBLD.W"
            """U.S. Imports of Other Reformulated Motor Gasoline in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyBlenderNetProductionOfMotorGasolineFinishedConventionalGreaterThanEd55: str = "PET.W_EPM0CAG55_YPB_NUS_MBBLD.W"
            """U.S. Blender Net Production of Motor Gasoline, Finished, Conventional, Greater Than Ed55 in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerAndBlenderNetProductionOfFinishedConventionalMotorGasolineGreaterThanEd55: str = "PET.W_EPM0CAG55_YPT_NUS_MBBLD.W"
            """U.S. Refiner and Blender Net Production of Finished Conventional Motor Gasoline, Greater than Ed 55 in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRefinerNetProductionOfFinishedConventionalMotorGasolineGreaterThanEd55: str = "PET.W_EPM0CAG55_YPY_NUS_MBBLD.W"
            """U.S. Refiner Net Production of Finished Conventional Motor Gasoline, Greater than Ed 55 in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfConventionalMotorGasolineEd55AndLower: str = "PET.W_EPM0CAL55_SAE_NUS_MBBL.W"
            """U.S. Ending Stocks of Conventional Motor Gasoline, Ed55 and Lower in Thousand Barrels (Mbbl)"""

            WeeklyImportsOfKerosene: str = "PET.W_EPPK_IM0_NUS-Z00_MBBLD.W"
            """U.S. Imports of Kerosene in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyExportsOfOtherOils: str = "PET.W_EPPO4_EEX_NUS-Z00_MBBLD.W"
            """U.S. Exports of Other Oils in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfOtherOilsExcludingFuelEthanol: str = "PET.W_EPPO6_IM0_NUS-Z00_MBBLD.W"
            """U.S. Imports of Other Oils (Excluding Fuel Ethanol) in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsFromAllCountriesOfMotorGasolineBlendingComponentsRbob: str = "PET.W_EPOBGRR_IM0_NUS-Z00_MBBLD.W"
            """U.S. Imports from  All Countries of Motor Gasoline Blending Components, RBOB in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyRegularAllFormulationsRetailGasolinePrices: str = "PET.EMM_EPMR_PTE_NUS_DPG.W"
            """U.S. Regular All Formulations Retail Gasoline Prices in Dollars per Gallon ($/gal)"""

            WeeklyMidgradeAllFormulationsRetailGasolinePrices: str = "PET.EMM_EPMM_PTE_NUS_DPG.W"
            """U.S. Midgrade All Formulations Retail Gasoline Prices in Dollars per Gallon ($/gal)"""

            WeeklyPremiumAllFormulationsRetailGasolinePrices: str = "PET.EMM_EPMP_PTE_NUS_DPG.W"
            """U.S. Premium All Formulations Retail Gasoline Prices in Dollars per Gallon ($/gal)"""

            WeeklyAllGradesAllFormulationsRetailGasolinePrices: str = "PET.EMM_EPM0_PTE_NUS_DPG.W"
            """U.S. All Grades All Formulations Retail Gasoline Prices in Dollars per Gallon ($/gal)"""

            WeeklyAllGradesReformulatedRetailGasolinePrices: str = "PET.EMM_EPM0R_PTE_NUS_DPG.W"
            """U.S. All Grades Reformulated Retail Gasoline Prices in Dollars per Gallon ($/gal)"""

            WeeklyMidgradeReformulatedRetailGasolinePrices: str = "PET.EMM_EPMMR_PTE_NUS_DPG.W"
            """U.S. Midgrade Reformulated Retail Gasoline Prices in Dollars per Gallon ($/gal)"""

            WeeklyPremiumReformulatedRetailGasolinePrices: str = "PET.EMM_EPMPR_PTE_NUS_DPG.W"
            """U.S. Premium Reformulated Retail Gasoline Prices in Dollars per Gallon ($/gal)"""

            WeeklyRegularConventionalRetailGasolinePrices: str = "PET.EMM_EPMRU_PTE_NUS_DPG.W"
            """U.S. Regular Conventional Retail Gasoline Prices in Dollars per Gallon ($/gal)"""

            WeeklyRegularReformulatedRetailGasolinePrices: str = "PET.EMM_EPMRR_PTE_NUS_DPG.W"
            """U.S. Regular Reformulated Retail Gasoline Prices in Dollars per Gallon ($/gal)"""

            WeeklyNo2DieselRetailPrices: str = "PET.EMD_EPD2D_PTE_NUS_DPG.W"
            """U.S. No 2 Diesel Retail Prices in Dollars per Gallon ($/gal)"""

            WeeklyPremiumConventionalRetailGasolinePrices: str = "PET.EMM_EPMPU_PTE_NUS_DPG.W"
            """U.S. Premium Conventional Retail Gasoline Prices in Dollars per Gallon ($/gal)"""

            WeeklyMidgradeConventionalRetailGasolinePrices: str = "PET.EMM_EPMMU_PTE_NUS_DPG.W"
            """U.S. Midgrade Conventional Retail Gasoline Prices in Dollars per Gallon ($/gal)"""

            WeeklyAllGradesConventionalRetailGasolinePrices: str = "PET.EMM_EPM0U_PTE_NUS_DPG.W"
            """U.S. All Grades Conventional Retail Gasoline Prices in Dollars per Gallon ($/gal)"""

            WeeklyNo2DieselUltraLowSulfur015PpmRetailPrices: str = "PET.EMD_EPD2DXL0_PTE_NUS_DPG.W"
            """U.S. No 2 Diesel Ultra Low Sulfur (0-15 ppm) Retail Prices in Dollars per Gallon ($/gal)"""

            WeeklyEndingStocksExcludingSprAndIncludingLeaseStockOfCrudeOil: str = "PET.W_EPC0_SAX_NUS_MBBL.W"
            """U.S. Ending Stocks excluding SPR and including Lease Stock of Crude Oil in Thousand Barrels (Mbbl)"""

            WeeklyNo2DieselLowSulfur15500PpmRetailPrices: str = "PET.EMD_EPD2DM10_PTE_NUS_DPG.W"
            """U.S. No 2 Diesel Low Sulfur (15-500 ppm) Retail Prices in Dollars per Gallon ($/gal)"""

            WeeklyImportsOfReformulatedRbobWithAlcoholGasolineBlendingComponents: str = "PET.WO3IM_NUS-Z00_2.W"
            """U.S. Imports of Reformulated RBOB with Alcohol Gasoline Blending Components in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyImportsOfReformulatedRbobWithEtherGasolineBlendingComponents: str = "PET.WO4IM_NUS-Z00_2.W"
            """U.S. Imports of Reformulated RBOB with Ether Gasoline Blending Components in Thousand Barrels per Day (Mbbl/d)"""

            WeeklyEndingStocksOfReformulatedGtabGasolineBlendingComponents: str = "PET.WO2ST_NUS_1.W"
            """U.S. Ending Stocks of Reformulated GTAB Gasoline Blending Components in Thousand Barrels (Mbbl)"""

            WeeklyEndingStocksOfReformulatedRbobWithAlcoholGasolineBlendingComponents: str = "PET.WO3ST_NUS_1.W"
            """U.S. Ending Stocks of Reformulated RBOB with Alcohol Gasoline Blending Components in Thousand Barrels (Mbbl)"""

            WeeklyEndingStocksOfReformulatedRbobWithEtherGasolineBlendingComponents: str = "PET.WO4ST_NUS_1.W"
            """U.S. Ending Stocks of Reformulated RBOB with Ether Gasoline Blending Components in Thousand Barrels (Mbbl)"""

        class EquatorialGuinea(System.Object):
            """Equatorial Guinea"""

            WeeklyImportsFromEquatorialGuineaOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NEK_MBBLD.W"
            """U.S. Imports from Equatorial Guinea of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Iraq(System.Object):
            """Iraq"""

            WeeklyImportsFromIraqOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NIZ_MBBLD.W"
            """U.S. Imports from Iraq of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Kuwait(System.Object):
            """Kuwait"""

            WeeklyImportsFromKuwaitOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NKU_MBBLD.W"
            """U.S. Imports from Kuwait of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Mexico(System.Object):
            """Mexico"""

            WeeklyImportsFromMexicoOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NMX_MBBLD.W"
            """U.S. Imports from Mexico of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Nigeria(System.Object):
            """Nigeria"""

            WeeklyImportsFromNigeriaOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NNI_MBBLD.W"
            """U.S. Imports from Nigeria of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Norway(System.Object):
            """Norway"""

            WeeklyImportsFromNorwayOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NNO_MBBLD.W"
            """U.S. Imports from Norway of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Russia(System.Object):
            """Russia"""

            WeeklyImportsFromRussiaOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NRS_MBBLD.W"
            """U.S. Imports from Russia of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class SaudiArabia(System.Object):
            """Saudi Arabia"""

            WeeklyImportsFromSaudiArabiaOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NSA_MBBLD.W"
            """U.S. Imports from Saudi Arabia of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class UnitedKingdom(System.Object):
            """United Kingdom"""

            WeeklyImportsFromUnitedKingdomOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NUK_MBBLD.W"
            """U.S. Imports from United Kingdom of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Venezuela(System.Object):
            """Venezuela"""

            WeeklyImportsFromVenezuelaOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NVE_MBBLD.W"
            """U.S. Imports from Venezuela of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Algeria(System.Object):
            """Algeria"""

            WeeklyImportsFromAlgeriaOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NAG_MBBLD.W"
            """U.S. Imports from Algeria of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Angola(System.Object):
            """Angola"""

            WeeklyImportsFromAngolaOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NAO_MBBLD.W"
            """U.S. Imports from Angola of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Brazil(System.Object):
            """Brazil"""

            WeeklyImportsFromBrazilOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NBR_MBBLD.W"
            """U.S. Imports from Brazil of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Canada(System.Object):
            """Canada"""

            WeeklyImportsFromCanadaOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NCA_MBBLD.W"
            """U.S. Imports from Canada of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Congo(System.Object):
            """Congo"""

            WeeklyImportsFromCongoBrazzavilleOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NCF_MBBLD.W"
            """U.S. Imports from Congo (Brazzaville) of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Colombia(System.Object):
            """Colombia"""

            WeeklyImportsFromColombiaOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NCO_MBBLD.W"
            """U.S. Imports from Colombia of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

        class Ecuador(System.Object):
            """Ecuador"""

            WeeklyImportsFromEcuadorOfCrudeOil: str = "PET.W_EPC0_IM0_NUS-NEC_MBBLD.W"
            """U.S. Imports from Ecuador of Crude Oil in Thousand Barrels per Day (Mbbl/d)"""

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Determines the location of the data
        
        :param config: Subscription configuration
        :param date: Date
        :param isLiveMode: Is live mode
        :returns: Location of the data as a SubscriptionDataSource.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Parses the data from the line provided and loads it into LEAN
        
        :param config: Subscription configuration
        :param line: Line of data
        :param date: Date
        :param isLiveMode: Is live mode
        :returns: New instance of USEnergy.
        """
        ...

    def Clone(self) -> QuantConnect.Data.BaseData:
        """
        Clones the data
        
        :returns: A clone of the object.
        """
        ...

    def RequiresMapping(self) -> bool:
        """
        Indicates whether the data source is tied
        to an underlying symbol and requires that corporate
        events be applied to it as well, such as renames and delistings
        
        :returns: false.
        """
        ...

    def IsSparseData(self) -> bool:
        """
        Indicates whether the data is sparse.
        If true, we disable logging for missing files
        
        :returns: true.
        """
        ...

    def ToString(self) -> str:
        """Converts the instance to string"""
        ...

    def DefaultResolution(self) -> int:
        """
        Gets the default resolution for this data and security type
        
        :returns: This method returns the int value of a member of the QuantConnect.Resolution enum.
        """
        ...

    def SupportedResolutions(self) -> System.Collections.Generic.List[QuantConnect.Resolution]:
        """Gets the supported resolution for this data and security type"""
        ...


