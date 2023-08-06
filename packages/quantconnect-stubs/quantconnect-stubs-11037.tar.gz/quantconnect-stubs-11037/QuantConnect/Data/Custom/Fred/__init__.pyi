import datetime

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Custom.Fred
import System
import System.Collections.Generic


class Fred(QuantConnect.Data.BaseData):
    """This class has no documentation."""

    class Wilshire(System.Object):
        """Wilshire Indexes help clients, investment professionals and researchers accurately measure and better understand the market. The Wilshire Index family leverages more than 40 years of Wilshire performance measurement expertise and employs unbiased construction rules."""

        USSmallCapValuePrice: str = "WILLSMLCAPVALPR"
        """Wilshire US Small-Cap Value Price Index (in Index)"""

        Price2500: str = "WILL2500PR"
        """Wilshire 2500 Price Index (in Index)"""

        Price4500: str = "WILL4500PR"
        """Wilshire 4500 Price Index (in Index)"""

        ValuePrice2500: str = "WILL2500PRVAL"
        """Wilshire 2500 Value Price Index (in Index)"""

        GrowthPrice2500: str = "WILL2500PRGR"
        """Wilshire 2500 Growth Price Index (in Index)"""

        USSmallCapPrice: str = "WILLSMLCAPPR"
        """Wilshire US Small-Cap Price Index (in Index)"""

        Price5000: str = "WILL5000PR"
        """Wilshire 5000 Price Index (in Index)"""

        USSmallCapGrowthPrice: str = "WILLSMLCAPGRPR"
        """Wilshire US Small-Cap Growth Price Index (in Index)"""

        USMidCapValuePrice: str = "WILLMIDCAPVALPR"
        """Wilshire US Mid-Cap Value Price Index (in Index)"""

        USRealEstateSecuritiesPrice: str = "WILLRESIPR"
        """Wilshire US Real Estate Securities Price Index (Wilshire US RESI) (in Index)"""

        USLargeCapPrice: str = "WILLLRGCAPPR"
        """Wilshire US Large-Cap Price Index (in Index)"""

        USMidCapPrice: str = "WILLMIDCAPPR"
        """Wilshire US Mid-Cap Price Index (in Index)"""

        USMidCapGrowthPrice: str = "WILLMIDCAPGRPR"
        """Wilshire US Mid-Cap Growth Price Index (in Index)"""

        USMicroCapPrice: str = "WILLMICROCAPPR"
        """Wilshire US Micro-Cap Price Index (in Index)"""

        USRealEstateInvestmentTrustPrice: str = "WILLREITPR"
        """Wilshire US Real Estate Investment Trust Price Index (Wilshire US REIT) (in Index)"""

        USLargeCapValuePrice: str = "WILLLRGCAPVALPR"
        """Wilshire US Large-Cap Value Price Index (in Index)"""

        USLargeCapGrowthPrice: str = "WILLLRGCAPGRPR"
        """Wilshire US Large-Cap Growth Price Index (in Index)"""

        FullCapPrice5000: str = "WILL5000PRFC"
        """Wilshire 5000 Full Cap Price Index (in Index)"""

        USMidCapValue: str = "WILLMIDCAPVAL"
        """Wilshire US Mid-Cap Value Total Market Index (in Index)"""

        USMidCapGrowth: str = "WILLMIDCAPGR"
        """Wilshire US Mid-Cap Growth Total Market Index (in Index)"""

        USMidCap: str = "WILLMIDCAP"
        """Wilshire US Mid-Cap Total Market Index (in Index)"""

        USRealEstateSecurities: str = "WILLRESIND"
        """Wilshire US Real Estate Securities Total Market Index (Wilshire US RESI) (in Index)"""

        Index4500: str = "WILL4500IND"
        """Wilshire 4500 Total Market Index (in Index)"""

        Index5000: str = "WILL5000IND"
        """Wilshire 5000 Total Market Index (in Index)"""

        USLargeCapGrowth: str = "WILLLRGCAPGR"
        """Wilshire US Large-Cap Growth Total Market Index (in Index)"""

        USMicroCap: str = "WILLMICROCAP"
        """Wilshire US Micro-Cap Total Market Index (in Index)"""

        Value2500: str = "WILL2500INDVAL"
        """Wilshire 2500 Value Total Market Index (in Index)"""

        USSmallCapGrowth: str = "WILLSMLCAPGR"
        """Wilshire US Small-Cap Growth Total Market Index (in Index)"""

        USSmallCapValue: str = "WILLSMLCAPVAL"
        """Wilshire US Small-Cap Value Total Market Index (in Index)"""

        USLargeCapValue: str = "WILLLRGCAPVAL"
        """Wilshire US Large-Cap Value Total Market Index (in Index)"""

        USRealEstateInvestmentTrust: str = "WILLREITIND"
        """Wilshire US Real Estate Investment Trust Total Market Index (Wilshire US REIT) (in Index)"""

        Index2500: str = "WILL2500IND"
        """Wilshire 2500 Total Market Index (in Index)"""

        USSmallCap: str = "WILLSMLCAP"
        """Wilshire US Small-Cap Total Market Index (in Index)"""

        USLargeCap: str = "WILLLRGCAP"
        """Wilshire US Large-Cap Total Market Index (in Index)"""

        Growth2500: str = "WILL2500INDGR"
        """Wilshire 2500 Growth Total Market Index (in Index)"""

        TotalMarketFullCap5000: str = "WILL5000INDFC"
        """Wilshire 5000 Total Market Full Cap Index (in Index)"""

    class LIBOR(System.Object):
        """This class has no documentation."""

        SpotNextBasedOnSwissFranc: str = "CHFONTD156N"
        """Spot Next London Interbank Offered Rate (LIBOR), based on Swiss Franc (in Percent)"""

        SpotNextBasedOnJapaneseYen: str = "JPYONTD156N"
        """Spot Next London Interbank Offered Rate (LIBOR), based on Japanese Yen (in Percent)"""

        SixMonthBasedOnJapaneseYen: str = "JPY6MTD156N"
        """6-Month London Interbank Offered Rate (LIBOR), based on Japanese Yen (in Percent)"""

        ThreeMonthBasedOnJapaneseYen: str = "JPY3MTD156N"
        """3-Month London Interbank Offered Rate (LIBOR), based on Japanese Yen (in Percent)"""

        SixMonthBasedOnUSD: str = "USD6MTD156N"
        """6-Month London Interbank Offered Rate (LIBOR), based on U.S. Dollar (in Percent)"""

        OneMonthBasedOnJapaneseYen: str = "JPY1MTD156N"
        """1-Month London Interbank Offered Rate (LIBOR), based on Japanese Yen (in Percent)"""

        TwelveMonthBasedOnJapaneseYen: str = "JPY12MD156N"
        """12-Month London Interbank Offered Rate (LIBOR), based on Japanese Yen (in Percent)"""

        TwelveMonthBasedOnBritishPound: str = "GBP12MD156N"
        """12-Month London Interbank Offered Rate (LIBOR), based on British Pound (in Percent)"""

        OneMonthBasedOnBritishPound: str = "GBP1MTD156N"
        """1-Month London Interbank Offered Rate (LIBOR), based on British Pound (in Percent)"""

        OneWeekBasedOnBritishPound: str = "GBP1WKD156N"
        """1-Week London Interbank Offered Rate (LIBOR), based on British Pound (in Percent)"""

        TwoMonthBasedOnBritishPound: str = "GBP2MTD156N"
        """2-Month London Interbank Offered Rate (LIBOR), based on British Pound (in Percent)"""

        ThreeMonthBasedOnBritishPound: str = "GBP3MTD156N"
        """3-Month London Interbank Offered Rate (LIBOR), based on British Pound (in Percent)"""

        OneWeekBasedOnJapaneseYen: str = "JPY1WKD156N"
        """1-Week London Interbank Offered Rate (LIBOR), based on Japanese Yen (in Percent)"""

        TwoMonthBasedOnJapaneseYen: str = "JPY2MTD156N"
        """2-Month London Interbank Offered Rate (LIBOR), based on Japanese Yen (in Percent)"""

        SixMonthBasedOnSwissFranc: str = "CHF6MTD156N"
        """6-Month London Interbank Offered Rate (LIBOR), based on Swiss Franc (in Percent)"""

        ThreeMonthBasedOnSwissFranc: str = "CHF3MTD156N"
        """3-Month London Interbank Offered Rate (LIBOR), based on Swiss Franc (in Percent)"""

        OneMonthBasedOnUSD: str = "USD1MTD156N"
        """1-Month London Interbank Offered Rate (LIBOR), based on U.S. Dollar (in Percent)"""

        TwelveMonthBasedOnSwissFranc: str = "CHF12MD156N"
        """12-Month London Interbank Offered Rate (LIBOR), based on Swiss Franc (in Percent)"""

        TwelveMonthBasedOnUSD: str = "USD12MD156N"
        """12-Month London Interbank Offered Rate (LIBOR), based on U.S. Dollar (in Percent)"""

        OneMonthBasedOnSwissFranc: str = "CHF1MTD156N"
        """1-Month London Interbank Offered Rate (LIBOR), based on Swiss Franc (in Percent)"""

        OneWeekBasedOnSwissFranc: str = "CHF1WKD156N"
        """1-Week London Interbank Offered Rate (LIBOR), based on Swiss Franc (in Percent)"""

        TwoMonthBasedOnSwissFranc: str = "CHF2MTD156N"
        """2-Month London Interbank Offered Rate (LIBOR), based on Swiss Franc (in Percent)"""

        TwelveMonthBasedOnEuro: str = "EUR12MD156N"
        """12-Month London Interbank Offered Rate (LIBOR), based on Euro (in Percent)"""

        SixMonthBasedOnBritishPound: str = "GBP6MTD156N"
        """6-Month London Interbank Offered Rate (LIBOR), based on British Pound (in Percent)"""

        OneMonthBasedOnEuro: str = "EUR1MTD156N"
        """1-Month London Interbank Offered Rate (LIBOR), based on Euro (in Percent)"""

        TwoMonthBasedOnEuro: str = "EUR2MTD156N"
        """2-Month London Interbank Offered Rate (LIBOR), based on Euro (in Percent)"""

        ThreeMonthBasedOnEuro: str = "EUR3MTD156N"
        """3-Month London Interbank Offered Rate (LIBOR), based on Euro (in Percent)"""

        SixMonthBasedOnEuro: str = "EUR6MTD156N"
        """6-Month London Interbank Offered Rate (LIBOR), based on Euro (in Percent)"""

        OvernightBasedOnEuro: str = "EURONTD156N"
        """Overnight London Interbank Offered Rate (LIBOR), based on Euro (in Percent)"""

        OneWeekBasedOnUSD: str = "USD1WKD156N"
        """1-Week London Interbank Offered Rate (LIBOR), based on U.S. Dollar (in Percent)"""

        TwoMonthBasedOnUSD: str = "USD2MTD156N"
        """2-Month London Interbank Offered Rate (LIBOR), based on U.S. Dollar (in Percent)"""

        ThreeMonthBasedOnUSD: str = "USD3MTD156N"
        """3-Month London Interbank Offered Rate (LIBOR), based on U.S. Dollar (in Percent)"""

        OvernightBasedOnUSD: str = "USDONTD156N"
        """Overnight London Interbank Offered Rate (LIBOR), based on U.S. Dollar (in Percent)"""

        OneWeekBasedOnEuro: str = "EUR1WKD156N"
        """1-Week London Interbank Offered Rate (LIBOR), based on Euro (in Percent)"""

        OvernightBasedOnBritishPound: str = "GBPONTD156N"
        """Overnight London Interbank Offered Rate (LIBOR), based on British Pound (in Percent)"""

    class CommercialPaper(System.Object):
        """
        Commercial paper (CP) consists of short-term, promissory notes issued primarily by corporations. Maturities range up to 270 days but average about 30 days. Many companies use CP to raise cash needed for current transactions, and many find it to be a lower-cost alternative to bank loans.
        The Federal Reserve Board disseminates information on CP primarily through its World Wide Web site. In addition, the Board publishes one-, two-, and three-month rates on AA nonfinancial and AA financial CP weekly in its H.15 Statistical Release.
        The Federal Reserve Board's CP release is derived from data supplied by The Depository Trust & Clearing Corporation (DTCC), a national clearinghouse for the settlement of securities trades and a custodian for securities. DTCC performs these functions for almost all activity in the domestic CP market. The Federal Reserve Board only considers maturities of 270 days or less. CP is exempt from SEC registration if its maturity does not exceed 270 days.
        Data on CP issuance rates and volumes typically are updated daily and typically posted with a one-day lag. Data on CP outstanding usually are available as of the close of business each Wednesday and as of the last business day of the month; these data are also posted with a one-day lag. The daily CP release will usually be available at 9:45 a.m. EST. However, the Federal Reserve Board makes no guarantee regarding the timing of the daily CP release. This policy is subject to change at any time without notice.
        """

        ThreeMonthAANonfinancialCommercialPaperRate: str = "DCPN3M"
        """3-Month AA Nonfinancial Commercial Paper Rate (in Percent)"""

        OneMonthAANonfinancialCommercialPaperRate: str = "DCPN30"
        """1-Month AA Nonfinancial Commercial Paper Rate (in Percent)"""

        TwoMonthAANonfinancialCommercialPaperRate: str = "DCPN2M"
        """2-Month AA Nonfinancial Commercial Paper Rate (in Percent)"""

        ThreeMonthAAFinancialCommercialPaperRate: str = "DCPF3M"
        """3-Month AA Financial Commercial Paper Rate (in Percent)"""

        TwoMonthAAFinancialCommercialPaperRate: str = "DCPF2M"
        """2-Month AA Financial Commercial Paper Rate (in Percent)"""

        OneMonthAAFinancialCommercialPaperRate: str = "DCPF1M"
        """1-Month AA Financial Commercial Paper Rate (in Percent)"""

        NumberOfIssuesWithMaturityBetween1and4DaysUsedForA2P2Nonfinancial: str = "NONFIN14A2P2VOL"
        """Number of Issues, with a Maturity Between 1 and 4 Days, Used in Calculating the A2/P2 Nonfinancial Commercial Paper Rates (in Number)"""

        NumberOfIssuesWithMaturityBetween5and9DaysUsedForA2P2Nonfinancial: str = "NONFIN59A2P2VOL"
        """Number of Issues, with a Maturity Between 5 and 9 Days, Used in Calculating the A2/P2 Nonfinancial Commercial Paper Rates (in Number)"""

        TotalValueOfIssuesWithMaturityBetween5and9DaysUsedForA2P2Nonfinancial: str = "NONFIN59A2P2AMT"
        """Total Value of Issues, with a Maturity Between 5 and 9 Days, Used in Calculating the A2/P2 Nonfinancial Commercial Paper Rates (in Millions of Dollars)"""

        NumberOfIssuesWithMaturityBetween41and80DaysUsedForAANonfinancial: str = "NONFIN4180AAVOL"
        """Number of Issues, with a Maturity Between 41 and 80 Days, Used in Calculating the AA Nonfinancial Commercial Paper Rates (in Number)"""

        TotalValueOfIssuesWithMaturityGreaterThan80DaysUsedForAAAssetBacked: str = "ABGT80AAAMT"
        """Total Value of Issues, with a Maturity Greater Than 80 Days, Used in Calculating the AA Asset-Backed Commercial Paper Rates (in Millions of Dollars)"""

        TotalValueOfIssuesWithMaturityBetween41and80DaysUsedForAANonfinancial: str = "NONFIN4180AAAMT"
        """Total Value of Issues, with a Maturity Between 41 and 80 Days, Used in Calculating the AA Nonfinancial Commercial Paper Rates (in Millions of Dollars)"""

        NumberOfIssuesWithMaturityBetween41and80DaysUsedForA2P2Nonfinancial: str = "NONFIN4180A2P2VOL"
        """Number of Issues, with a Maturity Between 41 and 80 Days, Used in Calculating the A2/P2 Nonfinancial Commercial Paper Rates (in Number)"""

        TotalValueOfIssuesWithMaturityBetween41and80DaysUsedForA2P2Nonfinancial: str = "NONFIN4180A2P2AMT"
        """Total Value of Issues, with a Maturity Between 41 and 80 Days, Used in Calculating the A2/P2 Nonfinancial Commercial Paper Rates (in Millions of Dollars)"""

        NumberOfIssuesWithMaturityBetween21and40DaysUsedForAANonfinancial: str = "NONFIN2140AAVOL"
        """Number of Issues, with a Maturity Between 21 and 40 Days, Used in Calculating the AA Nonfinancial Commercial Paper Rates (in Number)"""

        TotalValueOfIssuesWithMaturityBetween21and40DaysUsedForAANonfinancial: str = "NONFIN2140AAAMT"
        """Total Value of Issues, with a Maturity Between 21 and 40 Days, Used in Calculating the AA Nonfinancial Commercial Paper Rates (in Millions of Dollars)"""

        NumberOfIssuesWithMaturityBetween21and40DaysUsedForA2P2Nonfinancial: str = "NONFIN2140A2P2VOL"
        """Number of Issues, with a Maturity Between 21 and 40 Days, Used in Calculating the A2/P2 Nonfinancial Commercial Paper Rates (in Number)"""

        TotalValueOfIssuesWithMaturityBetween21and40DaysUsedForA2P2Nonfinancial: str = "NONFIN2140A2P2AMT"
        """Total Value of Issues, with a Maturity Between 21 and 40 Days, Used in Calculating the A2/P2 Nonfinancial Commercial Paper Rates (in Millions of Dollars)"""

        NumberOfIssuesWithMaturityBetween1and4DaysUsedForAANonfinancial: str = "NONFIN14AAVOL"
        """Number of Issues, with a Maturity Between 1 and 4 Days, Used in Calculating the AA Nonfinancial Commercial Paper Rates (in Number)"""

        NumberOfIssuesWithMaturityBetween10And20DaysUsedForA2P2Nonfinancial: str = "NONFIN1020A2P2VOL"
        """Number of Issues, with a Maturity Between 10 and 20 Days, Used in Calculating the A2/P2 Nonfinancial Commercial Paper Rates (in Number)"""

        TotalValueOfIssuesWithMaturityBetween10And20DaysUsedForAANonfinancial: str = "NONFIN1020AAAMT"
        """Total Value of Issues, with a Maturity Between 10 and 20 Days, Used in Calculating the AA Nonfinancial Commercial Paper Rates (in Millions of Dollars)"""

        TotalValueOfIssuesWithMaturityBetween21and40DaysUsedForAAAssetBacked: str = "AB2140AAAMT"
        """Total Value of Issues, with a Maturity Between 21 and 40 Days, Used in Calculating the AA Asset-Backed Commercial Paper Rates (in Millions of Dollars)"""

        NumberOfIssuesWithMaturityBetween10And20DaysUsedForAANonfinancial: str = "NONFIN1020AAVOL"
        """Number of Issues, with a Maturity Between 10 and 20 Days, Used in Calculating the AA Nonfinancial Commercial Paper Rates (in Number)"""

        TotalValueOfIssuesWithMaturityBetween1and4DaysUsedForA2P2Nonfinancial: str = "NONFIN14A2P2AMT"
        """Total Value of Issues, with a Maturity Between 1 and 4 Days, Used in Calculating the A2/P2 Nonfinancial Commercial Paper Rates (in Millions of Dollars)"""

        TotalValueOfIssuesWithMaturityBetween1and4DaysUsedForAANonfinancial: str = "NONFIN14AAAMT"
        """Total Value of Issues, with a Maturity Between 1 and 4 Days, Used in Calculating the AA Nonfinancial Commercial Paper Rates (in Millions of Dollars)"""

        TotalValueofCommercialPaperIssueswithaMaturityBetween1and4Days: str = "MKT14MKTAMT"
        """Total Value of Commercial Paper Issues with a Maturity Between 1 and 4 Days (in Millions of Dollars)"""

        TotalValueOfIssuesWithMaturityBetween10And20DaysUsedForA2P2Nonfinancial: str = "NONFIN1020A2P2AMT"
        """Total Value of Issues, with a Maturity Between 10 and 20 Days, Used in Calculating the A2/P2 Nonfinancial Commercial Paper Rates (in Millions of Dollars)"""

        NumberOfIssuesWithMaturityGreaterThan80DaysUsedForAAFinancial: str = "FINGT80AAVOL"
        """Number of Issues, with a Maturity Greater Than 80 Days, Used in Calculating the AA Financial Commercial Paper Rates (in Number)"""

        NumberOfIssuesWithMaturityBetween10And20DaysUsedForAAFinancial: str = "FIN1020AAVOL"
        """Number of Issues, with a Maturity Between 10 and 20 Days, Used in Calculating the AA Financial Commercial Paper Rates (in Number)"""

        TotalValueOfIssuesWithMaturityBetween1and4DaysUsedForAAFinancial: str = "FIN14AAAMT"
        """Total Value of Issues, with a Maturity Between 1 and 4 Days, Used in Calculating the AA Financial Commercial Paper Rates (in Millions of Dollars)"""

        NumberOfIssuesWithMaturityBetween1and4DaysUsedForAAFinancial: str = "FIN14AAVOL"
        """Number of Issues, with a Maturity Between 1 and 4 Days, Used in Calculating the AA Financial Commercial Paper Rates (in Number)"""

        TotalValueofCommercialPaperIssueswithaMaturityBetween10And20Days: str = "MKT1020MKTAMT"
        """Total Value of Commercial Paper Issues with a Maturity Between 10 and 20 Days (in Millions of Dollars)"""

        NumberofCommercialPaperIssueswithaMaturityBetween10And20Days: str = "MKT1020MKTVOL"
        """Number of Commercial Paper Issues with a Maturity Between 10 and 20 Days (in Number)"""

        TotalValueOfIssuesWithMaturityBetween21and40DaysUsedForAAFinancial: str = "FIN2140AAAMT"
        """Total Value of Issues, with a Maturity Between 21 and 40 Days, Used in Calculating the AA Financial Commercial Paper Rates (in Millions of Dollars)"""

        NumberofCommercialPaperIssueswithaMaturityBetween1and4Days: str = "MKT14MKTVOL"
        """Number of Commercial Paper Issues with a Maturity Between 1 and 4 Days (in Number)"""

        TotalValueofIssuersofCommercialPaperwithaMaturityBetween21and40Days: str = "MKT2140MKTAMT"
        """Total Value of Issuers of Commercial Paper with a Maturity Between 21 and 40 Days (in Millions of Dollars)"""

        NumberofCommercialPaperIssueswithaMaturityBetween21and40Days: str = "MKT2140MKTVOL"
        """Number of Commercial Paper Issues with a Maturity Between 21 and 40 Days (in Number)"""

        NumberOfIssuesWithMaturityBetween21and40DaysUsedForAAFinancial: str = "FIN2140AAVOL"
        """Number of Issues, with a Maturity Between 21 and 40 Days, Used in Calculating the AA Financial Commercial Paper Rates (in Number)"""

        TotalValueofIssuersofCommercialPaperwithaMaturityBetween41and80Days: str = "MKT4180MKTAMT"
        """Total Value of Issuers of Commercial Paper with a Maturity Between 41 and 80 Days (in Millions of Dollars)"""

        TotalValueOfIssuesWithMaturityBetween5and9DaysUsedForAANonfinancial: str = "NONFIN59AAAMT"
        """Total Value of Issues, with a Maturity Between 5 and 9 Days, Used in Calculating the AA Nonfinancial Commercial Paper Rates (in Millions of Dollars)"""

        NumberofCommercialPaperIssueswithaMaturityBetween41and80Days: str = "MKT4180MKTVOL"
        """Number of Commercial Paper Issues with a Maturity Between 41 and 80 Days (in Number)"""

        NumberofCommercialPaperIssueswithaMaturityBetween5and9Days: str = "MKT59MKTVOL"
        """Number of Commercial Paper Issues with a Maturity Between 5 and 9 Days (in Number)"""

        TotalValueofIssuersofCommercialPaperwithaMaturityGreaterThan80Days: str = "MKTGT80MKTAMT"
        """Total Value of Issuers of Commercial Paper with a Maturity Greater Than 80 Days (in Millions of Dollars)"""

        NumberofCommercialPaperIssueswithaMaturityGreaterThan80Days: str = "MKTGT80MKTVOL"
        """Number of Commercial Paper Issues with a Maturity Greater Than 80 Days (in Number)"""

        TotalValueOfIssuesWithMaturityBetween41and80DaysUsedForAAFinancial: str = "FIN4180AAAMT"
        """Total Value of Issues, with a Maturity Between 41 and 80 Days, Used in Calculating the AA Financial Commercial Paper Rates (in Millions of Dollars)"""

        NumberOfIssuesWithMaturityBetween41and80DaysUsedForAAFinancial: str = "FIN4180AAVOL"
        """Number of Issues, with a Maturity Between 41 and 80 Days, Used in Calculating the AA Financial Commercial Paper Rates (in Number)"""

        TotalValueOfIssuesWithMaturityBetween41and80DaysUsedForAAAssetBacked: str = "AB4180AAAMT"
        """Total Value of Issues, with a Maturity Between 41 and 80 Days, Used in Calculating the AA Asset-Backed Commercial Paper Rates (in Millions of Dollars)"""

        TotalValueOfIssuesWithMaturityBetween5and9DaysUsedForAAFinancial: str = "FIN59AAAMT"
        """Total Value of Issues, with a Maturity Between 5 and 9 Days, Used in Calculating the AA Financial Commercial Paper Rates (in Millions of Dollars)"""

        NumberOfIssuesWithMaturityBetween5and9DaysUsedForAAFinancial: str = "FIN59AAVOL"
        """Number of Issues, with a Maturity Between 5 and 9 Days, Used in Calculating the AA Financial Commercial Paper Rates (in Number)"""

        TotalValueOfIssuesWithMaturityGreaterThan80DaysUsedForAAFinancial: str = "FINGT80AAAMT"
        """Total Value of Issues, with a Maturity Greater Than 80 Days, Used in Calculating the AA Financial Commercial Paper Rates (in Millions of Dollars)"""

        TotalValueOfIssuesWithMaturityBetween10And20DaysUsedForAAFinancial: str = "FIN1020AAAMT"
        """Total Value of Issues, with a Maturity Between 10 and 20 Days, Used in Calculating the AA Financial Commercial Paper Rates (in Millions of Dollars)"""

        NumberOfIssuesWithMaturityBetween21and40DaysUsedForAAAssetBacked: str = "AB2140AAVOL"
        """Number of Issues, with a Maturity Between 21 and 40 Days, Used in Calculating the AA Asset-Backed Commercial Paper Rates (in Number)"""

        TotalValueofIssuersofCommercialPaperwithaMaturityBetween5and9Days: str = "MKT59MKTAMT"
        """Total Value of Issuers of Commercial Paper with a Maturity Between 5 and 9 Days (in Millions of Dollars)"""

        NumberOfIssuesWithMaturityGreaterThan80DaysUsedForAAAssetBacked: str = "ABGT80AAVOL"
        """Number of Issues, with a Maturity Greater Than 80 Days, Used in Calculating the AA Asset-Backed Commercial Paper Rates (in Number)"""

        NumberOfIssuesWithMaturityBetween5and9DaysUsedForAANonfinancial: str = "NONFIN59AAVOL"
        """Number of Issues, with a Maturity Between 5 and 9 Days, Used in Calculating the AA Nonfinancial Commercial Paper Rates (in Number)"""

        FifteenDayAAAssetbackedCommercialPaperInterestRate: str = "RIFSPPAAAD15NB"
        """15-Day AA Asset-backed Commercial Paper Interest Rate (in Percent)"""

        TotalValueOfIssuesWithMaturityBetween5and9DaysUsedForAAAssetBacked: str = "AB59AAAMT"
        """Total Value of Issues, with a Maturity Between 5 and 9 Days, Used in Calculating the AA Asset-Backed Commercial Paper Rates (in Millions of Dollars)"""

        NumberOfIssuesWithMaturityBetween41and80DaysUsedForAAAssetBacked: str = "AB4180AAVOL"
        """Number of Issues, with a Maturity Between 41 and 80 Days, Used in Calculating the AA Asset-Backed Commercial Paper Rates (in Number)"""

        FifteenDayA2P2NonfinancialCommercialPaperInterestRate: str = "RIFSPPNA2P2D15NB"
        """15-Day A2/P2 Nonfinancial Commercial Paper Interest Rate (in Percent)"""

        SevenDayA2P2NonfinancialCommercialPaperInterestRate: str = "RIFSPPNA2P2D07NB"
        """7-Day A2/P2 Nonfinancial Commercial Paper Interest Rate (in Percent)"""

        OvernightA2P2NonfinancialCommercialPaperInterestRate: str = "RIFSPPNA2P2D01NB"
        """Overnight A2/P2 Nonfinancial Commercial Paper Interest Rate (in Percent)"""

        NinetyDayAAFinancialCommercialPaperInterestRate: str = "RIFSPPFAAD90NB"
        """90-Day AA Financial Commercial Paper Interest Rate (in Percent)"""

        OvernightAAAssetbackedCommercialPaperInterestRate: str = "RIFSPPAAAD01NB"
        """Overnight AA Asset-backed Commercial Paper Interest Rate (in Percent)"""

        Three0DayA2P2NonfinancialCommercialPaperInterestRate: str = "RIFSPPNA2P2D30NB"
        """30-Day A2/P2 Nonfinancial Commercial Paper Interest Rate (in Percent)"""

        SixtyDayAAFinancialCommercialPaperInterestRate: str = "RIFSPPFAAD60NB"
        """60-Day AA Financial Commercial Paper Interest Rate (in Percent)"""

        Three0DayAAFinancialCommercialPaperInterestRate: str = "RIFSPPFAAD30NB"
        """30-Day AA Financial Commercial Paper Interest Rate (in Percent)"""

        TotalValueOfIssuesWithMaturityGreaterThan80DaysUsedForA2P2Nonfinancial: str = "NONFINGT80A2P2AMT"
        """Total Value of Issues, with a Maturity Greater Than 80 Days, Used in Calculating the A2/P2 Nonfinancial Commercial Paper Rates (in Millions of Dollars)"""

        Three0DayAAAssetbackedCommercialPaperInterestRate: str = "RIFSPPAAAD30NB"
        """30-Day AA Asset-backed Commercial Paper Interest Rate (in Percent)"""

        SixtyDayAAAssetbackedCommercialPaperInterestRate: str = "RIFSPPAAAD60NB"
        """60-Day AA Asset-backed Commercial Paper Interest Rate (in Percent)"""

        NinetyDayAAAssetbackedCommercialPaperInterestRate: str = "RIFSPPAAAD90NB"
        """90-Day AA Asset-backed Commercial Paper Interest Rate (in Percent)"""

        FifteenDayAAFinancialCommercialPaperInterestRate: str = "RIFSPPFAAD15NB"
        """15-Day AA Financial Commercial Paper Interest Rate (in Percent)"""

        SevenDayAAFinancialCommercialPaperInterestRate: str = "RIFSPPFAAD07NB"
        """7-Day AA Financial Commercial Paper Interest Rate (in Percent)"""

        SevenDayAAAssetbackedCommercialPaperInterestRate: str = "RIFSPPAAAD07NB"
        """7-Day AA Asset-backed Commercial Paper Interest Rate (in Percent)"""

        OvernightAAFinancialCommercialPaperInterestRate: str = "RIFSPPFAAD01NB"
        """Overnight AA Financial Commercial Paper Interest Rate (in Percent)"""

        SixtyDayA2P2NonfinancialCommercialPaperInterestRate: str = "RIFSPPNA2P2D60NB"
        """60-Day A2/P2 Nonfinancial Commercial Paper Interest Rate (in Percent)"""

        NumberOfIssuesWithMaturityBetween5and9DaysUsedForAAAssetBacked: str = "AB59AAVOL"
        """Number of Issues, with a Maturity Between 5 and 9 Days, Used in Calculating the AA Asset-Backed Commercial Paper Rates (in Number)"""

        NumberOfIssuesWithMaturityBetween1and4DaysUsedForAAAssetBacked: str = "AB14AAVOL"
        """Number of Issues, with a Maturity Between 1 and 4 Days, Used in Calculating the AA Asset-Backed Commercial Paper Rates (in Number)"""

        NumberOfIssuesWithMaturityGreaterThan80DaysUsedForA2P2Nonfinancial: str = "NONFINGT80A2P2VOL"
        """Number of Issues, with a Maturity Greater Than 80 Days, Used in Calculating the A2/P2 Nonfinancial Commercial Paper Rates (in Number)"""

        TotalValueOfIssuesWithMaturityBetween1and4DaysUsedForAAAssetBacked: str = "AB14AAAMT"
        """Total Value of Issues, with a Maturity Between 1 and 4 Days, Used in Calculating the AA Asset-Backed Commercial Paper Rates (in Millions of Dollars)"""

        NinetyDayA2P2NonfinancialCommercialPaperInterestRate: str = "RIFSPPNA2P2D90NB"
        """90-Day A2/P2 Nonfinancial Commercial Paper Interest Rate (in Percent)"""

        NumberOfIssuesWithMaturityBetween10And20DaysUsedForAAAssetBacked: str = "AB1020AAVOL"
        """Number of Issues, with a Maturity Between 10 and 20 Days, Used in Calculating the AA Asset-Backed Commercial Paper Rates (in Number)"""

        TotalValueOfIssuesWithMaturityGreaterThan80DaysUsedForAANonfinancial: str = "NONFINGT80AAAMT"
        """Total Value of Issues, with a Maturity Greater Than 80 Days, Used in Calculating the AA Nonfinancial Commercial Paper Rates (in Millions of Dollars)"""

        OvernightAANonfinancialCommercialPaperInterestRate: str = "RIFSPPNAAD01NB"
        """Overnight AA Nonfinancial Commercial Paper Interest Rate (in Percent)"""

        TotalValueOfIssuesWithMaturityBetween10And20DaysUsedForAAAssetBacked: str = "AB1020AAAMT"
        """Total Value of Issues, with a Maturity Between 10 and 20 Days, Used in Calculating the AA Asset-Backed Commercial Paper Rates (in Millions of Dollars)"""

        SevenDayAANonfinancialCommercialPaperInterestRate: str = "RIFSPPNAAD07NB"
        """7-Day AA Nonfinancial Commercial Paper Interest Rate (in Percent)"""

        NinetyDayAANonfinancialCommercialPaperInterestRate: str = "RIFSPPNAAD90NB"
        """90-Day AA Nonfinancial Commercial Paper Interest Rate (in Percent)"""

        FifteenDayAANonfinancialCommercialPaperInterestRate: str = "RIFSPPNAAD15NB"
        """15-Day AA Nonfinancial Commercial Paper Interest Rate (in Percent)"""

        Three0DayAANonfinancialCommercialPaperInterestRate: str = "RIFSPPNAAD30NB"
        """30-Day AA Nonfinancial Commercial Paper Interest Rate (in Percent)"""

        SixtyDayAANonfinancialCommercialPaperInterestRate: str = "RIFSPPNAAD60NB"
        """60-Day AA Nonfinancial Commercial Paper Interest Rate (in Percent)"""

        NumberOfIssuesWithMaturityGreaterThan80DaysUsedForAANonfinancial: str = "NONFINGT80AAVOL"
        """Number of Issues, with a Maturity Greater Than 80 Days, Used in Calculating the AA Nonfinancial Commercial Paper Rates (in Number)"""

        ThreeMonthCommercialPaperMinusFederalFundsRate: str = "CPFF"
        """3-Month Commercial Paper Minus Federal Funds Rate (in Percent)"""

    class ICEBofAML(System.Object):
        """This class has no documentation."""

        AAAAEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEM1BRRAAA2ACRPITRIV"
        """ICE BofAML AAA-A Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        AAAAUSEmergingMarketsLiquidCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEM1RAAA2ALCRPIUSTRIV"
        """ICE BofAML AAA-A US Emerging Markets Liquid Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        AsiaEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMRACRPIASIATRIV"
        """ICE BofAML Asia Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        AsiaUSEmergingMarketsLiquidCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMALLCRPIASIAUSTRIV"
        """ICE BofAML Asia US Emerging Markets Liquid Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        BandLowerEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEM4BRRBLCRPITRIV"
        """ICE BofAML B and Lower Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        BandLowerUSEmergingMarketsLiquidCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEM4RBLLCRPIUSTRIV"
        """ICE BofAML B and Lower US Emerging Markets Liquid Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        BBEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEM3BRRBBCRPITRIV"
        """ICE BofAML BB Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        BBUSEmergingMarketsLiquidCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEM3RBBLCRPIUSTRIV"
        """ICE BofAML BB US Emerging Markets Liquid Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        BBBEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEM2BRRBBBCRPITRIV"
        """ICE BofAML BBB Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        BBBUSEmergingMarketsLiquidCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEM2RBBBLCRPIUSTRIV"
        """ICE BofAML BBB US Emerging Markets Liquid Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        CrossoverEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEM5BCOCRPITRIV"
        """ICE BofAML Crossover Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        CrossoverUSEmergingMarketsLiquidCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMXOCOLCRPIUSTRIV"
        """ICE BofAML Crossover US Emerging Markets Liquid Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        EmergingMarketsCorporatePlusIndexTotalReturnIndexValue: str = "BAMLEMCBPITRIV"
        """ICE BofAML Emerging Markets Corporate Plus Index Total Return Index Value (in Index)"""

        EuroEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMEBCRPIETRIV"
        """ICE BofAML Euro Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        EMEAEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMRECRPIEMEATRIV"
        """ICE BofAML Europe, the Middle East, and Africa (EMEA) Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        EMEAUSEmergingMarketsLiquidCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMELLCRPIEMEAUSTRIV"
        """ICE BofAML Europe, the Middle East, and Africa (EMEA) US Emerging Markets Liquid Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        FinancialEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMFSFCRPITRIV"
        """ICE BofAML Financial Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        FinancialUSEmergingMarketsLiquidCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMFLFLCRPIUSTRIV"
        """ICE BofAML Financial US Emerging Markets Liquid Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        HighGradeEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMIBHGCRPITRIV"
        """ICE BofAML High Grade Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        HighGradeUSEmergingMarketsLiquidCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMHGHGLCRPIUSTRIV"
        """ICE BofAML High Grade US Emerging Markets Liquid Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        HighYieldEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMHBHYCRPITRIV"
        """ICE BofAML High Yield Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        HighYieldUSEmergingMarketsLiquidCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMHYHYLCRPIUSTRIV"
        """ICE BofAML High Yield US Emerging Markets Liquid Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        LatinAmericaEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMRLCRPILATRIV"
        """ICE BofAML Latin America Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        LatinAmericaUSEmergingMarketsLiquidCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMLLLCRPILAUSTRIV"
        """ICE BofAML Latin America US Emerging Markets Liquid Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        NonFinancialEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMNSNFCRPITRIV"
        """ICE BofAML Non-Financial Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        NonFinancialUSEmergingMarketsLiquidCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMNFNFLCRPIUSTRIV"
        """ICE BofAML Non-Financial US Emerging Markets Liquid Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        USCorporateMasterOptionAdjustedSpread: str = "BAMLC0A0CM"
        """ICE BofAML US Corporate Master Option-Adjusted Spread (in Percent)"""

        USHighYieldMasterIIOptionAdjustedSpread: str = "BAMLH0A0HYM2"
        """ICE BofAML US High Yield Master II Option-Adjusted Spread (in Percent)"""

        USCorporate1To3YearOptionAdjustedSpread: str = "BAMLC1A0C13Y"
        """ICE BofAML US Corporate 1-3 Year Option-Adjusted Spread (in Percent)"""

        USCorporate10To15YearOptionAdjustedSpread: str = "BAMLC7A0C1015Y"
        """ICE BofAML US Corporate 10-15 Year Option-Adjusted Spread (in Percent)"""

        USCorporateMoreThan15YearOptionAdjustedSpread: str = "BAMLC8A0C15PY"
        """ICE BofAML US Corporate 15+ Year Option-Adjusted Spread (in Percent)"""

        USCorporate3To5YearOptionAdjustedSpread: str = "BAMLC2A0C35Y"
        """ICE BofAML US Corporate 3-5 Year Option-Adjusted Spread (in Percent)"""

        USCorporate5To7YearOptionAdjustedSpread: str = "BAMLC3A0C57Y"
        """ICE BofAML US Corporate 5-7 Year Option-Adjusted Spread (in Percent)"""

        USCorporate7To10YearOptionAdjustedSpread: str = "BAMLC4A0C710Y"
        """ICE BofAML US Corporate 7-10 Year Option-Adjusted Spread (in Percent)"""

        PublicSectorIssuersUSEmergingMarketsLiquidCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMPUPUBSLCRPIUSTRIV"
        """ICE BofAML Public Sector Issuers US Emerging Markets Liquid Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        USEmergingMarketsCorporatePlusSubIndexTotalReturnIndexValue: str = "BAMLEMUBCRPIUSTRIV"
        """ICE BofAML US Emerging Markets Corporate Plus Sub-Index Total Return Index Value (in Index)"""

        USEmergingMarketsLiquidCorporatePlusIndexTotalReturnIndexValue: str = "BAMLEMCLLCRPIUSTRIV"
        """ICE BofAML US Emerging Markets Liquid Corporate Plus Index Total Return Index Value (in Index)"""

        EuroHighYieldIndexTotalReturnIndexValue: str = "BAMLHE00EHYITRIV"
        """ICE BofAML Euro High Yield Index Total Return Index Value (in Index)"""

        USCorp1To3YearsTotalReturnIndexValue: str = "BAMLCC1A013YTRIV"
        """ICE BofAML US Corp 1-3yr Total Return Index Value (in Index)"""

        USCorp10To15TotalReturnIndexValue: str = "BAMLCC7A01015YTRIV"
        """ICE BofAML US Corp 10-15yr Total Return Index Value (in Index)"""

        USCorpMoreThan15YearsTotalReturnIndexValue: str = "BAMLCC8A015PYTRIV"
        """ICE BofAML US Corp 15+yr Total Return Index Value (in Index)"""

        USCorpeTo5YearsTotalReturnIndexValue: str = "BAMLCC2A035YTRIV"
        """ICE BofAML US Corp 3-5yr Total Return Index Value (in Index)"""

        USCorp5To7YearsTotalReturnIndexValue: str = "BAMLCC3A057YTRIV"
        """ICE BofAML US Corp 5-7yr Total Return Index Value (in Index)"""

        USCorporate7To10YearsTotalReturnIndexValue: str = "BAMLCC4A0710YTRIV"
        """ICE BofAML US Corporate 7-10yr Total Return Index Value (in Index)"""

        USCorpATotalReturnIndexValue: str = "BAMLCC0A3ATRIV"
        """ICE BofAML US Corp A Total Return Index Value (in Index)"""

        USCorpAATotalReturnIndexValue: str = "BAMLCC0A2AATRIV"
        """ICE BofAML US Corp AA Total Return Index Value (in Index)"""

        USCorpAAATotalReturnIndexValue: str = "BAMLCC0A1AAATRIV"
        """ICE BofAML US Corp AAA Total Return Index Value (in Index)"""

        USHighYieldBTotalReturnIndexValue: str = "BAMLHYH0A2BTRIV"
        """ICE BofAML US High Yield B Total Return Index Value (in Index)"""

        USHighYieldBBTotalReturnIndexValue: str = "BAMLHYH0A1BBTRIV"
        """ICE BofAML US High Yield BB Total Return Index Value (in Index)"""

        USCorpBBBTotalReturnIndexValue: str = "BAMLCC0A4BBBTRIV"
        """ICE BofAML US Corp BBB Total Return Index Value (in Index)"""

        USHighYieldCCCorBelowTotalReturnIndexValue: str = "BAMLHYH0A3CMTRIV"
        """ICE BofAML US High Yield CCC or Below Total Return Index Value (in Index)"""

        USCorpMasterTotalReturnIndexValue: str = "BAMLCC0A0CMTRIV"
        """ICE BofAML US Corp Master Total Return Index Value (in Index)"""

        USHighYieldMasterIITotalReturnIndexValue: str = "BAMLHYH0A0HYM2TRIV"
        """ICE BofAML US High Yield Master II Total Return Index Value (in Index)"""

        AAAAEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEM1BRRAAA2ACRPIOAS"
        """ICE BofAML AAA-A Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        AAAAUSEmergingMarketsLiquidCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEM1RAAA2ALCRPIUSOAS"
        """ICE BofAML AAA-A US Emerging Markets Liquid Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        AsiaEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMRACRPIASIAOAS"
        """ICE BofAML Asia Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        AsiaUSEmergingMarketsLiquidCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMALLCRPIASIAUSOAS"
        """ICE BofAML Asia US Emerging Markets Liquid Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        BandLowerEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEM4BRRBLCRPIOAS"
        """ICE BofAML B and Lower Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        BandLowerUSEmergingMarketsLiquidCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEM4RBLLCRPIUSOAS"
        """ICE BofAML B and Lower US Emerging Markets Liquid Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        BBEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEM3BRRBBCRPIOAS"
        """ICE BofAML BB Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        BBUSEmergingMarketsLiquidCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEM3RBBLCRPIUSOAS"
        """ICE BofAML BB US Emerging Markets Liquid Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        BBBEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEM2BRRBBBCRPIOAS"
        """ICE BofAML BBB Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        BBBUSEmergingMarketsLiquidCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEM2RBBBLCRPIUSOAS"
        """ICE BofAML BBB US Emerging Markets Liquid Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        CrossoverEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEM5BCOCRPIOAS"
        """ICE BofAML Crossover Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        CrossoverUSEmergingMarketsLiquidCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMXOCOLCRPIUSOAS"
        """ICE BofAML Crossover US Emerging Markets Liquid Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        EmergingMarketsCorporatePlusIndexOptionAdjustedSpread: str = "BAMLEMCBPIOAS"
        """ICE BofAML Emerging Markets Corporate Plus Index Option-Adjusted Spread (in Percent)"""

        EuroEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMEBCRPIEOAS"
        """ICE BofAML Euro Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        EMEAEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMRECRPIEMEAOAS"
        """ICE BofAML Europe, the Middle East, and Africa (EMEA) Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        EMEAUSEmergingMarketsLiquidCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMELLCRPIEMEAUSOAS"
        """ICE BofAML Europe, the Middle East, and Africa (EMEA) US Emerging Markets Liquid Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        FinancialEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMFSFCRPIOAS"
        """ICE BofAML Financial Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        FinancialUSEmergingMarketsLiquidCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMFLFLCRPIUSOAS"
        """ICE BofAML Financial US Emerging Markets Liquid Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        HighGradeEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMIBHGCRPIOAS"
        """ICE BofAML High Grade Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        HighGradeUSEmergingMarketsLiquidCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMHGHGLCRPIUSOAS"
        """ICE BofAML High Grade US Emerging Markets Liquid Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        HighYieldEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMHBHYCRPIOAS"
        """ICE BofAML High Yield Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        HighYieldUSEmergingMarketsLiquidCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMHYHYLCRPIUSOAS"
        """ICE BofAML High Yield US Emerging Markets Liquid Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        LatinAmericaEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMRLCRPILAOAS"
        """ICE BofAML Latin America Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        LatinAmericaUSEmergingMarketsLiquidCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMLLLCRPILAUSOAS"
        """ICE BofAML Latin America US Emerging Markets Liquid Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        NonFinancialEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMNSNFCRPIOAS"
        """ICE BofAML Non-Financial Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        NonFinancialUSEmergingMarketsLiquidCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMNFNFLCRPIUSOAS"
        """ICE BofAML Non-Financial US Emerging Markets Liquid Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        PublicSectorIssuersUSEmergingMarketsLiquidCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMPUPUBSLCRPIUSOAS"
        """ICE BofAML Public Sector Issuers US Emerging Markets Liquid Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        USEmergingMarketsCorporatePlusSubIndexOptionAdjustedSpread: str = "BAMLEMUBCRPIUSOAS"
        """ICE BofAML US Emerging Markets Corporate Plus Sub-Index Option-Adjusted Spread (in Percent)"""

        USEmergingMarketsLiquidCorporatePlusIndexOptionAdjustedSpread: str = "BAMLEMCLLCRPIUSOAS"
        """ICE BofAML US Emerging Markets Liquid Corporate Plus Index Option-Adjusted Spread (in Percent)"""

        EuroHighYieldIndexOptionAdjustedSpread: str = "BAMLHE00EHYIOAS"
        """ICE BofAML Euro High Yield Index Option-Adjusted Spread (in Percent)"""

        USCorporateAOptionAdjustedSpread: str = "BAMLC0A3CA"
        """ICE BofAML US Corporate A Option-Adjusted Spread (in Percent)"""

        USCorporateAAOptionAdjustedSpread: str = "BAMLC0A2CAA"
        """ICE BofAML US Corporate AA Option-Adjusted Spread (in Percent)"""

        USCorporateAAAOptionAdjustedSpread: str = "BAMLC0A1CAAA"
        """ICE BofAML US Corporate AAA Option-Adjusted Spread (in Percent)"""

        USHighYieldBOptionAdjustedSpread: str = "BAMLH0A2HYB"
        """ICE BofAML US High Yield B Option-Adjusted Spread (in Percent)"""

        USHighYieldBBOptionAdjustedSpread: str = "BAMLH0A1HYBB"
        """ICE BofAML US High Yield BB Option-Adjusted Spread (in Percent)"""

        USCorporateBBBOptionAdjustedSpread: str = "BAMLC0A4CBBB"
        """ICE BofAML US Corporate BBB Option-Adjusted Spread (in Percent)"""

        USHighYieldCCCorBelowOptionAdjustedSpread: str = "BAMLH0A3HYC"
        """ICE BofAML US High Yield CCC or Below Option-Adjusted Spread (in Percent)"""

        AAAAEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEM1BRRAAA2ACRPIEY"
        """ICE BofAML AAA-A Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        AAAAUSEmergingMarketsLiquidCorporatePlusSubIndexEffectiveYield: str = "BAMLEM1RAAA2ALCRPIUSEY"
        """ICE BofAML AAA-A US Emerging Markets Liquid Corporate Plus Sub-Index Effective Yield (in Percent)"""

        AsiaEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEMRACRPIASIAEY"
        """ICE BofAML Asia Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        AsiaUSEmergingMarketsLiquidCorporatePlusSubIndexEffectiveYield: str = "BAMLEMALLCRPIASIAUSEY"
        """ICE BofAML Asia US Emerging Markets Liquid Corporate Plus Sub-Index Effective Yield (in Percent)"""

        BandLowerEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEM4BRRBLCRPIEY"
        """ICE BofAML B and Lower Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        BandLowerUSEmergingMarketsLiquidCorporatePlusSubIndexEffectiveYield: str = "BAMLEM4RBLLCRPIUSEY"
        """ICE BofAML B and Lower US Emerging Markets Liquid Corporate Plus Sub-Index Effective Yield (in Percent)"""

        BBEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEM3BRRBBCRPIEY"
        """ICE BofAML BB Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        BBUSEmergingMarketsLiquidCorporatePlusSubIndexEffectiveYield: str = "BAMLEM3RBBLCRPIUSEY"
        """ICE BofAML BB US Emerging Markets Liquid Corporate Plus Sub-Index Effective Yield (in Percent)"""

        BBBEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEM2BRRBBBCRPIEY"
        """ICE BofAML BBB Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        BBBUSEmergingMarketsLiquidCorporatePlusSubIndexEffectiveYield: str = "BAMLEM2RBBBLCRPIUSEY"
        """ICE BofAML BBB US Emerging Markets Liquid Corporate Plus Sub-Index Effective Yield (in Percent)"""

        CrossoverEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEM5BCOCRPIEY"
        """ICE BofAML Crossover Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        CrossoverUSEmergingMarketsLiquidCorporatePlusSubIndexEffectiveYield: str = "BAMLEMXOCOLCRPIUSEY"
        """ICE BofAML Crossover US Emerging Markets Liquid Corporate Plus Sub-Index Effective Yield (in Percent)"""

        EmergingMarketsCorporatePlusIndexEffectiveYield: str = "BAMLEMCBPIEY"
        """ICE BofAML Emerging Markets Corporate Plus Index Effective Yield (in Percent)"""

        EuroEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEMEBCRPIEEY"
        """ICE BofAML Euro Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        EuroHighYieldIndexEffectiveYield: str = "BAMLHE00EHYIEY"
        """ICE BofAML Euro High Yield Index Effective Yield (in Percent)"""

        EMEAEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEMRECRPIEMEAEY"
        """ICE BofAML Europe, the Middle East, and Africa (EMEA) Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        EMEAUSEmergingMarketsLiquidCorporatePlusSubIndexEffectiveYield: str = "BAMLEMELLCRPIEMEAUSEY"
        """ICE BofAML Europe, the Middle East, and Africa (EMEA) US Emerging Markets Liquid Corporate Plus Sub-Index Effective Yield (in Percent)"""

        FinancialEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEMFSFCRPIEY"
        """ICE BofAML Financial Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        FinancialUSEmergingMarketsLiquidCorporatePlusSubIndexEffectiveYield: str = "BAMLEMFLFLCRPIUSEY"
        """ICE BofAML Financial US Emerging Markets Liquid Corporate Plus Sub-Index Effective Yield (in Percent)"""

        HighGradeEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEMIBHGCRPIEY"
        """ICE BofAML High Grade Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        HighGradeUSEmergingMarketsLiquidCorporatePlusSubIndexEffectiveYield: str = "BAMLEMHGHGLCRPIUSEY"
        """ICE BofAML High Grade US Emerging Markets Liquid Corporate Plus Sub-Index Effective Yield (in Percent)"""

        HighYieldEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEMHBHYCRPIEY"
        """ICE BofAML High Yield Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        HighYieldUSEmergingMarketsLiquidCorporatePlusSubIndexEffectiveYield: str = "BAMLEMHYHYLCRPIUSEY"
        """ICE BofAML High Yield US Emerging Markets Liquid Corporate Plus Sub-Index Effective Yield (in Percent)"""

        LatinAmericaEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEMRLCRPILAEY"
        """ICE BofAML Latin America Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        LatinAmericaUSEmergingMarketsLiquidCorporatePlusSubIndexEffectiveYield: str = "BAMLEMLLLCRPILAUSEY"
        """ICE BofAML Latin America US Emerging Markets Liquid Corporate Plus Sub-Index Effective Yield (in Percent)"""

        NonFinancialEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEMNSNFCRPIEY"
        """ICE BofAML Non-Financial Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        NonFinancialUSEmergingMarketsLiquidCorporatePlusSubIndexEffectiveYield: str = "BAMLEMNFNFLCRPIUSEY"
        """ICE BofAML Non-Financial US Emerging Markets Liquid Corporate Plus Sub-Index Effective Yield (in Percent)"""

        PublicSectorIssuersUSEmergingMarketsLiquidCorporatePlusSubIndexEffectiveYield: str = "BAMLEMPUPUBSLCRPIUSEY"
        """ICE BofAML Public Sector Issuers US Emerging Markets Liquid Corporate Plus Sub-Index Effective Yield (in Percent)"""

        USCorporate1ThreeYearEffectiveYield: str = "BAMLC1A0C13YEY"
        """ICE BofAML US Corporate 1-3 Year Effective Yield (in Percent)"""

        USCorporate10To15YearEffectiveYield: str = "BAMLC7A0C1015YEY"
        """ICE BofAML US Corporate 10-15 Year Effective Yield (in Percent)"""

        USCorporateMoreThan15YearEffectiveYield: str = "BAMLC8A0C15PYEY"
        """ICE BofAML US Corporate 15+ Year Effective Yield (in Percent)"""

        USCorporate3To5YearEffectiveYield: str = "BAMLC2A0C35YEY"
        """ICE BofAML US Corporate 3-5 Year Effective Yield (in Percent)"""

        USCorporate5To7YearEffectiveYield: str = "BAMLC3A0C57YEY"
        """ICE BofAML US Corporate 5-7 Year Effective Yield (in Percent)"""

        USCorporate7To10YearEffectiveYield: str = "BAMLC4A0C710YEY"
        """ICE BofAML US Corporate 7-10 Year Effective Yield (in Percent)"""

        USCorporateAEffectiveYield: str = "BAMLC0A3CAEY"
        """ICE BofAML US Corporate A Effective Yield (in Percent)"""

        USCorporateAAEffectiveYield: str = "BAMLC0A2CAAEY"
        """ICE BofAML US Corporate AA Effective Yield (in Percent)"""

        USCorporateAAAEffectiveYield: str = "BAMLC0A1CAAAEY"
        """ICE BofAML US Corporate AAA Effective Yield (in Percent)"""

        USHighYieldBEffectiveYield: str = "BAMLH0A2HYBEY"
        """ICE BofAML US High Yield B Effective Yield (in Percent)"""

        USHighYieldBBEffectiveYield: str = "BAMLH0A1HYBBEY"
        """ICE BofAML US High Yield BB Effective Yield (in Percent)"""

        USCorporateBBBEffectiveYield: str = "BAMLC0A4CBBBEY"
        """ICE BofAML US Corporate BBB Effective Yield (in Percent)"""

        USHighYieldCCCorBelowEffectiveYield: str = "BAMLH0A3HYCEY"
        """ICE BofAML US High Yield CCC or Below Effective Yield (in Percent)"""

        USCorporateMasterEffectiveYield: str = "BAMLC0A0CMEY"
        """ICE BofAML US Corporate Master Effective Yield (in Percent)"""

        USEmergingMarketsCorporatePlusSubIndexEffectiveYield: str = "BAMLEMUBCRPIUSEY"
        """ICE BofAML US Emerging Markets Corporate Plus Sub-Index Effective Yield (in Percent)"""

        USEmergingMarketsLiquidCorporatePlusIndexEffectiveYield: str = "BAMLEMCLLCRPIUSEY"
        """ICE BofAML US Emerging Markets Liquid Corporate Plus Index Effective Yield (in Percent)"""

        USHighYieldMasterIIEffectiveYield: str = "BAMLH0A0HYM2EY"
        """ICE BofAML US High Yield Master II Effective Yield (in Percent)"""

        AAAAEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEM1BRRAAA2ACRPISYTW"
        """ICE BofAML AAA-A Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        AAAAUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEM1RAAA2ALCRPIUSSYTW"
        """ICE BofAML AAA-A US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        AsiaEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMRACRPIASIASYTW"
        """ICE BofAML Asia Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        AsiaUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMALLCRPIASIAUSSYTW"
        """ICE BofAML Asia US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        BandLowerEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEM4BRRBLCRPISYTW"
        """ICE BofAML B and Lower Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        BandLowerUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEM4RBLLCRPIUSSYTW"
        """ICE BofAML B and Lower US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        BBEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEM3BRRBBCRPISYTW"
        """ICE BofAML BB Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        BBUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEM3RBBLCRPIUSSYTW"
        """ICE BofAML BB US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        BBBEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEM2BRRBBBCRPISYTW"
        """ICE BofAML BBB Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        BBBUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEM2RBBBLCRPIUSSYTW"
        """ICE BofAML BBB US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        CrossoverEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEM5BCOCRPISYTW"
        """ICE BofAML Crossover Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        CrossoverUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMXOCOLCRPIUSSYTW"
        """ICE BofAML Crossover US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        EmergingMarketsCorporatePlusIndexSemiAnnualYieldtoWorst: str = "BAMLEMCBPISYTW"
        """ICE BofAML Emerging Markets Corporate Plus Index Semi-Annual Yield to Worst (in Percent)"""

        EuroEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMEBCRPIESYTW"
        """ICE BofAML Euro Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        EuroHighYieldIndexSemiAnnualYieldtoWorst: str = "BAMLHE00EHYISYTW"
        """ICE BofAML Euro High Yield Index Semi-Annual Yield to Worst (in Percent)"""

        EMEAEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMRECRPIEMEASYTW"
        """ICE BofAML Europe, the Middle East, and Africa (EMEA) Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        EMEAUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMELLCRPIEMEAUSSYTW"
        """ICE BofAML Europe, the Middle East, and Africa (EMEA) US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        FinancialEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMFSFCRPISYTW"
        """ICE BofAML Financial Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        FinancialUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMFLFLCRPIUSSYTW"
        """ICE BofAML Financial US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        HighGradeEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMIBHGCRPISYTW"
        """ICE BofAML High Grade Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        HighGradeUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMHGHGLCRPIUSSYTW"
        """ICE BofAML High Grade US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        HighYieldEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMHBHYCRPISYTW"
        """ICE BofAML High Yield Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        HighYieldUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMHYHYLCRPIUSSYTW"
        """ICE BofAML High Yield US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        LatinAmericaEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMRLCRPILASYTW"
        """ICE BofAML Latin America Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        LatinAmericaUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMLLLCRPILAUSSYTW"
        """ICE BofAML Latin America US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        NonFinancialEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMNSNFCRPISYTW"
        """ICE BofAML Non-Financial Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        NonFinancialUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMNFNFLCRPIUSSYTW"
        """ICE BofAML Non-Financial US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        PrivateSectorIssuersEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMPTPRVICRPISYTW"
        """ICE BofAML Private Sector Issuers Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        PrivateSectorIssuersUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMPVPRIVSLCRPIUSSYTW"
        """ICE BofAML Private Sector Issuers US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        PublicSectorIssuersEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMPBPUBSICRPISYTW"
        """ICE BofAML Public Sector Issuers Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        PublicSectorIssuersUSEmergingMarketsLiquidCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMPUPUBSLCRPIUSSYTW"
        """ICE BofAML Public Sector Issuers US Emerging Markets Liquid Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        USCorporate1To3YearSemiAnnualYieldtoWorst: str = "BAMLC1A0C13YSYTW"
        """ICE BofAML US Corporate 1-3 Year Semi-Annual Yield to Worst (in Percent)"""

        USCorporate10To15YearSemiAnnualYieldtoWorst: str = "BAMLC7A0C1015YSYTW"
        """ICE BofAML US Corporate 10-15 Year Semi-Annual Yield to Worst (in Percent)"""

        USCorporateMoreThan15YearSemiAnnualYieldtoWorst: str = "BAMLC8A0C15PYSYTW"
        """ICE BofAML US Corporate 15+ Year Semi-Annual Yield to Worst (in Percent)"""

        USCorporate3To5YearSemiAnnualYieldtoWorst: str = "BAMLC2A0C35YSYTW"
        """ICE BofAML US Corporate 3-5 Year Semi-Annual Yield to Worst (in Percent)"""

        USCorporate5To7YearSemiAnnualYieldtoWorst: str = "BAMLC3A0C57YSYTW"
        """ICE BofAML US Corporate 5-7 Year Semi-Annual Yield to Worst (in Percent)"""

        USCorporate7To10YearSemiAnnualYieldtoWorst: str = "BAMLC4A0C710YSYTW"
        """ICE BofAML US Corporate 7-10 Year Semi-Annual Yield to Worst (in Percent)"""

        USCorporateASemiAnnualYieldtoWorst: str = "BAMLC0A3CASYTW"
        """ICE BofAML US Corporate A Semi-Annual Yield to Worst (in Percent)"""

        USCorporateAASemiAnnualYieldtoWorst: str = "BAMLC0A2CAASYTW"
        """ICE BofAML US Corporate AA Semi-Annual Yield to Worst (in Percent)"""

        USCorporateAAASemiAnnualYieldtoWorst: str = "BAMLC0A1CAAASYTW"
        """ICE BofAML US Corporate AAA Semi-Annual Yield to Worst (in Percent)"""

        USHighYieldBSemiAnnualYieldtoWorst: str = "BAMLH0A2HYBSYTW"
        """ICE BofAML US High Yield B Semi-Annual Yield to Worst (in Percent)"""

        USHighYieldBBSemiAnnualYieldtoWorst: str = "BAMLH0A1HYBBSYTW"
        """ICE BofAML US High Yield BB Semi-Annual Yield to Worst (in Percent)"""

        USCorporateBBBSemiAnnualYieldtoWorst: str = "BAMLC0A4CBBBSYTW"
        """ICE BofAML US Corporate BBB Semi-Annual Yield to Worst (in Percent)"""

        USHighYieldCCCorBelowSemiAnnualYieldtoWorst: str = "BAMLH0A3HYCSYTW"
        """ICE BofAML US High Yield CCC or Below Semi-Annual Yield to Worst (in Percent)"""

        USCorporateMasterSemiAnnualYieldtoWorst: str = "BAMLC0A0CMSYTW"
        """ICE BofAML US Corporate Master Semi-Annual Yield to Worst (in Percent)"""

        USEmergingMarketsCorporatePlusSubIndexSemiAnnualYieldtoWorst: str = "BAMLEMUBCRPIUSSYTW"
        """ICE BofAML US Emerging Markets Corporate Plus Sub-Index Semi-Annual Yield to Worst (in Percent)"""

        USEmergingMarketsLiquidCorporatePlusIndexSemiAnnualYieldtoWorst: str = "BAMLEMCLLCRPIUSSYTW"
        """ICE BofAML US Emerging Markets Liquid Corporate Plus Index Semi-Annual Yield to Worst (in Percent)"""

        USHighYieldMasterIISemiAnnualYieldtoWorst: str = "BAMLH0A0HYM2SYTW"
        """ICE BofAML US High Yield Master II Semi-Annual Yield to Worst (in Percent)"""

    class TradeWeightedIndexes(System.Object):
        """This class has no documentation."""

        MajorCurrenciesGoods: str = "DTWEXM"
        """Trade Weighted U.S. Dollar Index: Major Currencies, Goods (in Index Mar 1973=100)"""

        OtherImportantTradingPartnersGoods: str = "DTWEXO"
        """Trade Weighted U.S. Dollar Index: Other Important Trading Partners, Goods (in Index Jan 1997=100)"""

        BroadGoods: str = "DTWEXB"
        """Trade Weighted U.S. Dollar Index: Broad, Goods (in Index Jan 1997=100)"""

        AdvancedForeignEconomiesGoodsAndServices: str = "DTWEXAFEGS"
        """Trade Weighted U.S. Dollar Index: Advanced Foreign Economies, Goods and Services (in Index Jan 2006=100)"""

        BroadGoodsAndServices: str = "DTWEXBGS"
        """Trade Weighted U.S. Dollar Index: Broad, Goods and Services (in Index Jan 2006=100)"""

        EmergingMarketsEconomiesGoodsAndServices: str = "DTWEXEMEGS"
        """Trade Weighted U.S. Dollar Index: Emerging Markets Economies, Goods and Services (in Index Jan 2006=100)"""

    class OECDRecessionIndicators(System.Object):
        """
        These time series is an interpretation of Organisation of Economic Development (OECD) Composite Leading Indicators: Reference Turning Points and Component Series data, which can be found at http://www.oecd.org/std/leading-indicators/oecdcompositeleadingindicatorsreferenceturningpointsandcomponentseries.htm. The OECD identifies months of turning points without designating a date within the month that turning points occurred. The dummy variable adopts an arbitrary convention that the turning point occurred at a specific date within the month. The arbitrary convention does not reflect any judgment on this issue by the OECD. Our time series is composed of dummy variables that represent periods of expansion and recession. A value of 1 is a recessionary period, while a value of 0 is an expansionary period. For this time series, the recession begins on the 15th day of the month of the peak and ends on the 15th day of the month of the trough. This time series is a disaggregation of the monthly series. For more options on recession shading, see the note and links below.
        The recession shading data that we provide initially comes from the source as a list of dates that are either an economic peak or trough. We interpret dates into recession shading data using one of three arbitrary methods. All of our recession shading data is available using all three interpretations. The period between a peak and trough is always shaded as a recession. The peak and trough are collectively extrema. Depending on the application, the extrema, both individually and collectively, may be included in the recession period in whole or in part. In situations where a portion of a period is included in the recession, the whole period is deemed to be included in the recession period.
        The first interpretation, known as the midpoint method, is to show a recession from the midpoint of the peak through the midpoint of the trough for monthly and quarterly data. For daily data, the recession begins on the 15th of the month of the peak and ends on the 15th of the month of the trough. Daily data is a disaggregation of monthly data. For monthly and quarterly data, the entire peak and trough periods are included in the recession shading. This method shows the maximum number of periods as a recession for monthly and quarterly data. The Federal Reserve Bank of St. Louis uses this method in its own publications. The midpoint method is used for this series.
        The second interpretation, known as the trough method, is to show a recession from the period following the peak through the trough (i.e. the peak is not included in the recession shading, but the trough is). For daily data, the recession begins on the first day of the first month following the peak and ends on the last day of the month of the trough. Daily data is a disaggregation of monthly data. The trough method is used when displaying data on FRED graphs. A version of this time series represented using the trough method can be found at:
        The third interpretation, known as the peak method, is to show a recession from the period of the peak to the trough (i.e. the peak is included in the recession shading, but the trough is not). For daily data, the recession begins on the first day of the month of the peak and ends on the last day of the month preceding the trough. Daily data is a disaggregation of monthly data. A version of this time series represented using the peak method can be found at:
        The OECD CLI system is based on the "growth cycle" approach, where business cycles and turning points are measured and identified in the deviation-from-trend series. The main reference series used in the OECD CLI system for the majority of countries is industrial production (IIP) covering all industry sectors excluding construction. This series is used because of its cyclical sensitivity and monthly availability, while the broad based Gross Domestic Product (GDP) is used to supplement the IIP series for identification of the final reference turning points in the growth cycle.
        Zones aggregates of the CLIs and the reference series are calculated as weighted averages of the corresponding zone member series (i.e. CLIs and IIPs).
        Up to December 2008 the turning points chronologies shown for regional/zone area aggregates or individual countries are determined by the rules established by the National Bureau of Economic Research (NBER) in the United States, which have been formalized and incorporated in a computer routine (Bry and Boschan) and included in the Phase-Average Trend (PAT) de-trending procedure. Starting from December 2008 the turning point detection algorithm is decoupled from the de-trending procedure, and is a simplified version of the original Bry and Boschan routine. (The routine parses local minima and maxima in the cycle series and applies censor rules to guarantee alternating peaks and troughs, as well as phase and cycle length constraints.)
        The components of the CLI are time series which exhibit leading relationship with the reference series (IIP) at turning points. Country CLIs are compiled by combining de-trended smoothed and normalized components. The component series for each country are selected based on various criteria such as economic significance; cyclical behavior; data quality; timeliness and availability.
        OECD data should be cited as follows: OECD Composite Leading Indicators, "Composite Leading Indicators: Reference Turning Points and Component Series", http://www.oecd.org/std/leading-indicators/oecdcompositeleadingindicatorsreferenceturningpointsandcomponentseries.htm
        """

        FourBigEuropeanCountriesFromPeakThroughTheTrough: str = "4BIGEURORECDM"
        """OECD based Recession Indicators for Four Big European Countries from the Peak through the Trough (in +1 or 0)"""

        AustraliaFromPeakThroughTheTrough: str = "AUSRECDM"
        """OECD based Recession Indicators for Australia from the Peak through the Trough (in +1 or 0)"""

        AustriaFromPeakThroughTheTrough: str = "AUTRECDM"
        """OECD based Recession Indicators for Austria from the Peak through the Trough (in +1 or 0)"""

        BelgiumFromPeakThroughTheTrough: str = "BELRECDM"
        """OECD based Recession Indicators for Belgium from the Peak through the Trough (in +1 or 0)"""

        BrazilFromPeakThroughTheTrough: str = "BRARECDM"
        """OECD based Recession Indicators for Brazil from the Peak through the Trough (in +1 or 0)"""

        CanadaFromPeakThroughTheTrough: str = "CANRECDM"
        """OECD based Recession Indicators for Canada from the Peak through the Trough (in +1 or 0)"""

        SwitzerlandFromPeakThroughTheTrough: str = "CHERECDM"
        """OECD based Recession Indicators for Switzerland from the Peak through the Trough (in +1 or 0)"""

        ChileFromPeakThroughTheTrough: str = "CHLRECDM"
        """OECD based Recession Indicators for Chile from the Peak through the Trough (in +1 or 0)"""

        ChinaFromPeakThroughTheTrough: str = "CHNRECDM"
        """OECD based Recession Indicators for China from the Peak through the Trough (in +1 or 0)"""

        CzechRepublicFromPeakThroughTheTrough: str = "CZERECDM"
        """OECD based Recession Indicators for the Czech Republic from the Peak through the Trough (in +1 or 0)"""

        GermanyFromPeakThroughTheTrough: str = "DEURECDM"
        """OECD based Recession Indicators for Germany from the Peak through the Trough (in +1 or 0)"""

        DenmarkFromPeakThroughTheTrough: str = "DNKRECDM"
        """OECD based Recession Indicators for Denmark from the Peak through the Trough (in +1 or 0)"""

        SpainFromPeakThroughTheTrough: str = "ESPRECDM"
        """OECD based Recession Indicators for Spain from the Peak through the Trough (in +1 or 0)"""

        EstoniaFromPeakThroughTheTrough: str = "ESTRECDM"
        """OECD based Recession Indicators for Estonia from the Peak through the Trough (in +1 or 0)"""

        EuroAreaFromPeakThroughTheTrough: str = "EURORECDM"

        FinlandFromPeakThroughTheTrough: str = "FINRECDM"
        """OECD based Recession Indicators for Finland from the Peak through the Trough (in +1 or 0)"""

        FranceFromPeakThroughTheTrough: str = "FRARECDM"
        """OECD based Recession Indicators for France from the Peak through the Trough (in +1 or 0)"""

        UnitedKingdomFromPeakThroughTheTrough: str = "GBRRECDM"
        """OECD based Recession Indicators for the United Kingdom from the Peak through the Trough (in +1 or 0)"""

        GreeceFromPeakThroughTheTrough: str = "GRCRECDM"
        """OECD based Recession Indicators for Greece from the Peak through the Trough (in +1 or 0)"""

        HungaryFromPeakThroughTheTrough: str = "HUNRECDM"
        """OECD based Recession Indicators for Hungary from the Peak through the Trough (in +1 or 0)"""

        IndonesiaFromPeakThroughTheTrough: str = "IDNRECDM"
        """OECD based Recession Indicators for Indonesia from the Peak through the Trough (in +1 or 0)"""

        IndiaFromPeakThroughTheTrough: str = "INDRECDM"
        """OECD based Recession Indicators for India from the Peak through the Trough (in +1 or 0)"""

        IrelandFromPeakThroughTheTrough: str = "IRLRECDM"
        """OECD based Recession Indicators for Ireland from the Peak through the Trough (in +1 or 0)"""

        IsraelFromPeakThroughTheTrough: str = "ISRRECDM"
        """OECD based Recession Indicators for Israel from the Peak through the Trough (in +1 or 0)"""

        ItalyFromPeakThroughTheTrough: str = "ITARECDM"
        """OECD based Recession Indicators for Italy from the Peak through the Trough (in +1 or 0)"""

        JapanFromPeakThroughTheTrough: str = "JPNRECDM"
        """OECD based Recession Indicators for Japan from the Peak through the Trough (in +1 or 0)"""

        KoreaFromPeakThroughTheTrough: str = "KORRECDM"
        """OECD based Recession Indicators for Korea from the Peak through the Trough (in +1 or 0)"""

        LuxembourgFromPeakThroughTheTrough: str = "LUXRECDM"
        """OECD based Recession Indicators for Luxembourg from the Peak through the Trough (in +1 or 0)"""

        MajorFiveAsiaFromPeakThroughTheTrough: str = "MAJOR5ASIARECDM"
        """OECD based Recession Indicators for Major 5 Asia from the Peak through the Trough (in +1 or 0)"""

        MexicoFromPeakThroughTheTrough: str = "MEXRECDM"
        """OECD based Recession Indicators for Mexico from the Peak through the Trough (in +1 or 0)"""

        MajorSevenCountriesFromPeakThroughTheTrough: str = "MSCRECDM"
        """OECD based Recession Indicators for Major Seven Countries from the Peak through the Trough (in +1 or 0)"""

        NAFTAAreaFromPeakThroughTheTrough: str = "NAFTARECDM"
        """OECD based Recession Indicators for NAFTA Area from the Peak through the Trough (in +1 or 0)"""

        NetherlandsFromPeakThroughTheTrough: str = "NDLRECDM"
        """OECD based Recession Indicators for Netherlands from the Peak through the Trough (in +1 or 0)"""

        NorwayFromPeakThroughTheTrough: str = "NORRECDM"
        """OECD based Recession Indicators for Norway from the Peak through the Trough (in +1 or 0)"""

        NewZealandFromPeakThroughTheTrough: str = "NZLRECDM"
        """OECD based Recession Indicators for New Zealand from the Peak through the Trough (in +1 or 0)"""

        OECDEuropeFromPeakThroughTheTrough: str = "OECDEUROPERECDM"
        """OECD based Recession Indicators for OECD Europe from the Peak through the Trough (in +1 or 0)"""

        OECDAndNonmemberEconomiesFromPeakThroughTheTrough: str = "OECDNMERECDM"
        """OECD based Recession Indicators for OECD and Non-member Economies from the Peak through the Trough (in +1 or 0)"""

        OECDTotalAreaFromPeakThroughTheTrough: str = "OECDRECDM"
        """OECD based Recession Indicators for the OECD Total Area from the Peak through the Trough (in +1 or 0)"""

        PolandFromPeakThroughTheTrough: str = "POLRECDM"
        """OECD based Recession Indicators for Poland from the Peak through the Trough (in +1 or 0)"""

        PortugalFromPeakThroughTheTrough: str = "PRTRECDM"
        """OECD based Recession Indicators for Portugal from the Peak through the Trough (in +1 or 0)"""

        RussianFederationFromPeakThroughTheTrough: str = "RUSRECDM"
        """OECD based Recession Indicators for Russian Federation from the Peak through the Trough (in +1 or 0)"""

        SlovakRepublicFromPeakThroughTheTrough: str = "SVKRECDM"
        """OECD based Recession Indicators for the Slovak Republic from the Peak through the Trough (in +1 or 0)"""

        SloveniaFromPeakThroughTheTrough: str = "SVNRECDM"
        """OECD based Recession Indicators for Slovenia from the Peak through the Trough (in +1 or 0)"""

        SwedenFromPeakThroughTheTrough: str = "SWERECDM"
        """OECD based Recession Indicators for Sweden from the Peak through the Trough (in +1 or 0)"""

        TurkeyFromPeakThroughTheTrough: str = "TURRECDM"
        """OECD based Recession Indicators for Turkey from the Peak through the Trough (in +1 or 0)"""

        UnitedStatesFromPeakThroughTheTrough: str = "USARECDM"
        """OECD based Recession Indicators for the United States from the Peak through the Trough (in +1 or 0)"""

        SouthAfricaFromPeakThroughTheTrough: str = "ZAFRECDM"
        """OECD based Recession Indicators for South Africa from the Peak through the Trough (in +1 or 0)"""

        FourBigEuropeanCountriesFromPeriodFollowingPeakThroughTheTrough: str = "4BIGEURORECD"
        """OECD based Recession Indicators for Four Big European Countries from the Period following the Peak through the Trough (in +1 or 0)"""

        AustraliaFromPeriodFollowingPeakThroughTheTrough: str = "AUSRECD"
        """OECD based Recession Indicators for Australia from the Period following the Peak through the Trough (in +1 or 0)"""

        AustriaFromPeriodFollowingPeakThroughTheTrough: str = "AUTRECD"
        """OECD based Recession Indicators for Austria from the Period following the Peak through the Trough (in +1 or 0)"""

        BelgiumFromPeriodFollowingPeakThroughTheTrough: str = "BELRECD"
        """OECD based Recession Indicators for Belgium from the Period following the Peak through the Trough (in +1 or 0)"""

        BrazilFromPeriodFollowingPeakThroughTheTrough: str = "BRARECD"
        """OECD based Recession Indicators for Brazil from the Period following the Peak through the Trough (in +1 or 0)"""

        CanadaFromPeriodFollowingPeakThroughTheTrough: str = "CANRECD"
        """OECD based Recession Indicators for Canada from the Period following the Peak through the Trough (in +1 or 0)"""

        SwitzerlandFromPeriodFollowingPeakThroughTheTrough: str = "CHERECD"
        """OECD based Recession Indicators for Switzerland from the Period following the Peak through the Trough (in +1 or 0)"""

        ChileFromPeriodFollowingPeakThroughTheTrough: str = "CHLRECD"
        """OECD based Recession Indicators for Chile from the Period following the Peak through the Trough (in +1 or 0)"""

        ChinaFromPeriodFollowingPeakThroughTheTrough: str = "CHNRECD"
        """OECD based Recession Indicators for China from the Period following the Peak through the Trough (in +1 or 0)"""

        CzechRepublicFromPeriodFollowingPeakThroughTheTrough: str = "CZERECD"
        """OECD based Recession Indicators for the Czech Republic from the Period following the Peak through the Trough (in +1 or 0)"""

        GermanyFromPeriodFollowingPeakThroughTheTrough: str = "DEURECD"
        """OECD based Recession Indicators for Germany from the Period following the Peak through the Trough (in +1 or 0)"""

        DenmarkFromPeriodFollowingPeakThroughTheTrough: str = "DNKRECD"
        """OECD based Recession Indicators for Denmark from the Period following the Peak through the Trough (in +1 or 0)"""

        SpainFromPeriodFollowingPeakThroughTheTrough: str = "ESPRECD"
        """OECD based Recession Indicators for Spain from the Period following the Peak through the Trough (in +1 or 0)"""

        EstoniaFromPeriodFollowingPeakThroughTheTrough: str = "ESTRECD"
        """OECD based Recession Indicators for Estonia from the Period following the Peak through the Trough (in +1 or 0)"""

        EuroAreaFromPeriodFollowingPeakThroughTheTrough: str = "EURORECD"
        """OECD based Recession Indicators for Euro Area from the Period following the Peak through the Trough (in +1 or 0)"""

        FinlandFromPeriodFollowingPeakThroughTheTrough: str = "FINRECD"
        """OECD based Recession Indicators for Finland from the Period following the Peak through the Trough (in +1 or 0)"""

        FranceFromPeriodFollowingPeakThroughTheTrough: str = "FRARECD"
        """OECD based Recession Indicators for France from the Period following the Peak through the Trough (in +1 or 0)"""

        UnitedKingdomFromPeriodFollowingPeakThroughTheTrough: str = "GBRRECD"
        """OECD based Recession Indicators for the United Kingdom from the Period following the Peak through the Trough (in +1 or 0)"""

        GreeceFromPeriodFollowingPeakThroughTheTrough: str = "GRCRECD"
        """OECD based Recession Indicators for Greece from the Period following the Peak through the Trough (in +1 or 0)"""

        HungaryFromPeriodFollowingPeakThroughTheTrough: str = "HUNRECD"
        """OECD based Recession Indicators for Hungary from the Period following the Peak through the Trough (in +1 or 0)"""

        IndonesiaFromPeriodFollowingPeakThroughTheTrough: str = "IDNRECD"
        """OECD based Recession Indicators for Indonesia from the Period following the Peak through the Trough (in +1 or 0)"""

        IndiaFromPeriodFollowingPeakThroughTheTrough: str = "INDRECD"
        """OECD based Recession Indicators for India from the Period following the Peak through the Trough (in +1 or 0)"""

        IrelandFromPeriodFollowingPeakThroughTheTrough: str = "IRLRECD"
        """OECD based Recession Indicators for Ireland from the Period following the Peak through the Trough (in +1 or 0)"""

        IsraelFromPeriodFollowingPeakThroughTheTrough: str = "ISRRECD"
        """OECD based Recession Indicators for Israel from the Period following the Peak through the Trough (in +1 or 0)"""

        ItalyFromPeriodFollowingPeakThroughTheTrough: str = "ITARECD"
        """OECD based Recession Indicators for Italy from the Period following the Peak through the Trough (in +1 or 0)"""

        JapanFromPeriodFollowingPeakThroughTheTrough: str = "JPNRECD"
        """OECD based Recession Indicators for Japan from the Period following the Peak through the Trough (in +1 or 0)"""

        KoreaFromPeriodFollowingPeakThroughTheTrough: str = "KORRECD"
        """OECD based Recession Indicators for Korea from the Period following the Peak through the Trough (in +1 or 0)"""

        LuxembourgFromPeriodFollowingPeakThroughTheTrough: str = "LUXRECD"
        """OECD based Recession Indicators for Luxembourg from the Period following the Peak through the Trough (in +1 or 0)"""

        MajorFiveAsiaFromPeriodFollowingPeakThroughTheTrough: str = "MAJOR5ASIARECD"
        """OECD based Recession Indicators for Major 5 Asia from the Period following the Peak through the Trough (in +1 or 0)"""

        MexicoFromPeriodFollowingPeakThroughTheTrough: str = "MEXRECD"
        """OECD based Recession Indicators for Mexico from the Period following the Peak through the Trough (in +1 or 0)"""

        MajorSevenCountriesFromPeriodFollowingPeakThroughTheTrough: str = "MSCRECD"
        """OECD based Recession Indicators for Major Seven Countries from the Period following the Peak through the Trough (in +1 or 0)"""

        NAFTAAreaFromPeriodFollowingPeakThroughTheTrough: str = "NAFTARECD"
        """OECD based Recession Indicators for NAFTA Area from the Period following the Peak through the Trough (in +1 or 0)"""

        NetherlandsFromPeriodFollowingPeakThroughTheTrough: str = "NDLRECD"
        """OECD based Recession Indicators for Netherlands from the Period following the Peak through the Trough (in +1 or 0)"""

        NorwayFromPeriodFollowingPeakThroughTheTrough: str = "NORRECD"
        """OECD based Recession Indicators for Norway from the Period following the Peak through the Trough (in +1 or 0)"""

        NewZealandFromPeriodFollowingPeakThroughTheTrough: str = "NZLRECD"
        """OECD based Recession Indicators for New Zealand from the Period following the Peak through the Trough (in +1 or 0)"""

        OECDEuropeFromPeriodFollowingPeakThroughTheTrough: str = "OECDEUROPERECD"
        """OECD based Recession Indicators for OECD Europe from the Period following the Peak through the Trough (in +1 or 0)"""

        OECDandNonmemberEconomiesFromPeriodFollowingPeakThroughTheTrough: str = "OECDNMERECD"
        """OECD based Recession Indicators for OECD and Non-member Economies from the Period following the Peak through the Trough (in +1 or 0)"""

        OECDTotalAreaFromPeriodFollowingPeakThroughTheTrough: str = "OECDRECD"
        """OECD based Recession Indicators for the OECD Total Area from the Period following the Peak through the Trough (in +1 or 0)"""

        PolandFromPeriodFollowingPeakThroughTheTrough: str = "POLRECD"
        """OECD based Recession Indicators for Poland from the Period following the Peak through the Trough (in +1 or 0)"""

        PortugalFromPeriodFollowingPeakThroughTheTrough: str = "PRTRECD"

        RussianFederationFromPeriodFollowingPeakThroughTheTrough: str = "RUSRECD"
        """OECD based Recession Indicators for Russian Federation from the Period following the Peak through the Trough (in +1 or 0)"""

        SlovakRepublicFromPeriodFollowingPeakThroughTheTrough: str = "SVKRECD"
        """OECD based Recession Indicators for the Slovak Republic from the Period following the Peak through the Trough (in +1 or 0)"""

        SloveniaFromPeriodFollowingPeakThroughTheTrough: str = "SVNRECD"
        """OECD based Recession Indicators for Slovenia from the Period following the Peak through the Trough (in +1 or 0)"""

        SwedenFromPeriodFollowingPeakThroughTheTrough: str = "SWERECD"
        """OECD based Recession Indicators for Sweden from the Period following the Peak through the Trough (in +1 or 0)"""

        TurkeyFromPeriodFollowingPeakThroughTheTrough: str = "TURRECD"
        """OECD based Recession Indicators for Turkey from the Period following the Peak through the Trough (in +1 or 0)"""

        UnitedStatesFromPeriodFollowingPeakThroughTheTrough: str = "USARECD"
        """OECD based Recession Indicators for the United States from the Period following the Peak through the Trough (in +1 or 0)"""

        SouthAfricaFromPeriodFollowingPeakThroughTheTrough: str = "ZAFRECD"
        """OECD based Recession Indicators for South Africa from the Period following the Peak through the Trough (in +1 or 0)"""

        FourBigEuropeanCountriesFromPeakThroughThePeriodPrecedingtheTrough: str = "4BIGEURORECDP"
        """OECD based Recession Indicators for Four Big European Countries from the Peak through the Period preceding the Trough (in +1 or 0)"""

        AustraliaFromPeakThroughThePeriodPrecedingtheTrough: str = "AUSRECDP"
        """OECD based Recession Indicators for Australia from the Peak through the Period preceding the Trough (in +1 or 0)"""

        AustriaFromPeakThroughThePeriodPrecedingtheTrough: str = "AUTRECDP"
        """OECD based Recession Indicators for Austria from the Peak through the Period preceding the Trough (in +1 or 0)"""

        BelgiumFromPeakThroughThePeriodPrecedingtheTrough: str = "BELRECDP"
        """OECD based Recession Indicators for Belgium from the Peak through the Period preceding the Trough (in +1 or 0)"""

        BrazilFromPeakThroughThePeriodPrecedingtheTrough: str = "BRARECDP"
        """OECD based Recession Indicators for Brazil from the Peak through the Period preceding the Trough (in +1 or 0)"""

        CanadaFromPeakThroughThePeriodPrecedingtheTrough: str = "CANRECDP"
        """OECD based Recession Indicators for Canada from the Peak through the Period preceding the Trough (in +1 or 0)"""

        SwitzerlandFromPeakThroughThePeriodPrecedingtheTrough: str = "CHERECDP"
        """OECD based Recession Indicators for Switzerland from the Peak through the Period preceding the Trough (in +1 or 0)"""

        ChileFromPeakThroughThePeriodPrecedingtheTrough: str = "CHLRECDP"
        """OECD based Recession Indicators for Chile from the Peak through the Period preceding the Trough (in +1 or 0)"""

        ChinaFromPeakThroughThePeriodPrecedingtheTrough: str = "CHNRECDP"
        """OECD based Recession Indicators for China from the Peak through the Period preceding the Trough (in +1 or 0)"""

        CzechRepublicFromPeakThroughThePeriodPrecedingtheTrough: str = "CZERECDP"
        """OECD based Recession Indicators for the Czech Republic from the Peak through the Period preceding the Trough (in +1 or 0)"""

        GermanyFromPeakThroughThePeriodPrecedingtheTrough: str = "DEURECDP"
        """OECD based Recession Indicators for Germany from the Peak through the Period preceding the Trough (in +1 or 0)"""

        DenmarkFromPeakThroughThePeriodPrecedingtheTrough: str = "DNKRECDP"
        """OECD based Recession Indicators for Denmark from the Peak through the Period preceding the Trough (in +1 or 0)"""

        SpainFromPeakThroughThePeriodPrecedingtheTrough: str = "ESPRECDP"
        """OECD based Recession Indicators for Spain from the Peak through the Period preceding the Trough (in +1 or 0)"""

        EstoniaFromPeakThroughThePeriodPrecedingtheTrough: str = "ESTRECDP"
        """OECD based Recession Indicators for Estonia from the Peak through the Period preceding the Trough (in +1 or 0)"""

        EuroAreaFromPeakThroughThePeriodPrecedingtheTrough: str = "EURORECDP"
        """OECD based Recession Indicators for Euro Area from the Peak through the Period preceding the Trough (in +1 or 0)"""

        FinlandFromPeakThroughThePeriodPrecedingtheTrough: str = "FINRECDP"
        """OECD based Recession Indicators for Finland from the Peak through the Period preceding the Trough (in +1 or 0)"""

        FranceFromPeakThroughThePeriodPrecedingtheTrough: str = "FRARECDP"
        """OECD based Recession Indicators for France from the Peak through the Period preceding the Trough (in +1 or 0)"""

        UnitedKingdomFromPeakThroughThePeriodPrecedingtheTrough: str = "GBRRECDP"
        """OECD based Recession Indicators for the United Kingdom from the Peak through the Period preceding the Trough (in +1 or 0)"""

        GreeceFromPeakThroughThePeriodPrecedingtheTrough: str = "GRCRECDP"
        """OECD based Recession Indicators for Greece from the Peak through the Period preceding the Trough (in +1 or 0)"""

        HungaryFromPeakThroughThePeriodPrecedingtheTrough: str = "HUNRECDP"
        """OECD based Recession Indicators for Hungary from the Peak through the Period preceding the Trough (in +1 or 0)"""

        IndonesiaFromPeakThroughThePeriodPrecedingtheTrough: str = "IDNRECDP"
        """OECD based Recession Indicators for Indonesia from the Peak through the Period preceding the Trough (in +1 or 0)"""

        IndiaFromPeakThroughThePeriodPrecedingtheTrough: str = "INDRECDP"
        """OECD based Recession Indicators for India from the Peak through the Period preceding the Trough (in +1 or 0)"""

        IrelandFromPeakThroughThePeriodPrecedingtheTrough: str = "IRLRECDP"
        """OECD based Recession Indicators for Ireland from the Peak through the Period preceding the Trough (in +1 or 0)"""

        IsraelFromPeakThroughThePeriodPrecedingtheTrough: str = "ISRRECDP"
        """OECD based Recession Indicators for Israel from the Peak through the Period preceding the Trough (in +1 or 0)"""

        ItalyFromPeakThroughThePeriodPrecedingtheTrough: str = "ITARECDP"
        """OECD based Recession Indicators for Italy from the Peak through the Period preceding the Trough (in +1 or 0)"""

        JapanFromPeakThroughThePeriodPrecedingtheTrough: str = "JPNRECDP"
        """OECD based Recession Indicators for Japan from the Peak through the Period preceding the Trough (in +1 or 0)"""

        KoreaFromPeakThroughThePeriodPrecedingtheTrough: str = "KORRECDP"
        """OECD based Recession Indicators for Korea from the Peak through the Period preceding the Trough (in +1 or 0)"""

        LuxembourgFromPeakThroughThePeriodPrecedingtheTrough: str = "LUXRECDP"
        """OECD based Recession Indicators for Luxembourg from the Peak through the Period preceding the Trough (in +1 or 0)"""

        MajorFiveAsiaFromPeakThroughThePeriodPrecedingtheTrough: str = "MAJOR5ASIARECDP"
        """OECD based Recession Indicators for Major 5 Asia from the Peak through the Period preceding the Trough (in +1 or 0)"""

        MexicoFromPeakThroughThePeriodPrecedingtheTrough: str = "MEXRECDP"
        """OECD based Recession Indicators for Mexico from the Peak through the Period preceding the Trough (in +1 or 0)"""

        MajorSevenCountriesFromPeakThroughThePeriodPrecedingtheTrough: str = "MSCRECDP"
        """OECD based Recession Indicators for Major Seven Countries from the Peak through the Period preceding the Trough (in +1 or 0)"""

        NAFTAAreaFromPeakThroughThePeriodPrecedingtheTrough: str = "NAFTARECDP"
        """OECD based Recession Indicators for NAFTA Area from the Peak through the Period preceding the Trough (in +1 or 0)"""

        NetherlandsFromPeakThroughThePeriodPrecedingtheTrough: str = "NDLRECDP"
        """OECD based Recession Indicators for Netherlands from the Peak through the Period preceding the Trough (in +1 or 0)"""

        NorwayFromPeakThroughThePeriodPrecedingtheTrough: str = "NORRECDP"
        """OECD based Recession Indicators for Norway from the Peak through the Period preceding the Trough (in +1 or 0)"""

        NewZealandFromPeakThroughThePeriodPrecedingtheTrough: str = "NZLRECDP"

        OECDEuropeFromPeakThroughThePeriodPrecedingtheTrough: str = "OECDEUROPERECDP"
        """OECD based Recession Indicators for OECD Europe from the Peak through the Period preceding the Trough (in +1 or 0)"""

        OECDandNonmemberEconomiesFromPeakThroughThePeriodPrecedingtheTrough: str = "OECDNMERECDP"
        """OECD based Recession Indicators for OECD and Non-member Economies from the Peak through the Period preceding the Trough (in +1 or 0)"""

        OECDTotalAreaFromPeakThroughThePeriodPrecedingtheTrough: str = "OECDRECDP"
        """OECD based Recession Indicators for the OECD Total Area from the Peak through the Period preceding the Trough (in +1 or 0)"""

        PolandFromPeakThroughThePeriodPrecedingtheTrough: str = "POLRECDP"
        """OECD based Recession Indicators for Poland from the Peak through the Period preceding the Trough (in +1 or 0)"""

        PortugalFromPeakThroughThePeriodPrecedingtheTrough: str = "PRTRECDP"
        """OECD based Recession Indicators for Portugal from the Peak through the Period preceding the Trough (in +1 or 0)"""

        RussianFederationFromPeakThroughThePeriodPrecedingtheTrough: str = "RUSRECDP"
        """OECD based Recession Indicators for Russian Federation from the Peak through the Period preceding the Trough (in +1 or 0)"""

        SlovakRepublicFromPeakThroughThePeriodPrecedingtheTrough: str = "SVKRECDP"
        """OECD based Recession Indicators for the Slovak Republic from the Peak through the Period preceding the Trough (in +1 or 0)"""

        SloveniaFromPeakThroughThePeriodPrecedingtheTrough: str = "SVNRECDP"
        """OECD based Recession Indicators for Slovenia from the Peak through the Period preceding the Trough (in +1 or 0)"""

        SwedenFromPeakThroughThePeriodPrecedingtheTrough: str = "SWERECDP"
        """OECD based Recession Indicators for Sweden from the Peak through the Period preceding the Trough (in +1 or 0)"""

        TurkeyFromPeakThroughThePeriodPrecedingtheTrough: str = "TURRECDP"
        """OECD based Recession Indicators for Turkey from the Peak through the Period preceding the Trough (in +1 or 0)"""

        UnitedStatesFromPeakThroughThePeriodPrecedingtheTrough: str = "USARECDP"
        """OECD based Recession Indicators for the United States from the Peak through the Period preceding the Trough (in +1 or 0)"""

        SouthAfricaFromPeakThroughThePeriodPrecedingtheTrough: str = "ZAFRECDP"
        """OECD based Recession Indicators for South Africa from the Peak through the Period preceding the Trough (in +1 or 0)"""

    class CBOE(System.Object):
        """This class has no documentation."""

        VIXOnGoogle: str = "VXGOGCLS"
        """CBOE Equity VIX on Google (in Index)"""

        VXD: str = "VXDCLS"
        """CBOE DJIA Volatility Index (in Index)"""

        VIXOnGoldmanSachs: str = "VXGSCLS"
        """CBOE Equity VIX on Goldman Sachs (in Index)"""

        VIXOnIBM: str = "VXIBMCLS"
        """CBOE Equity VIX on IBM (in Index)"""

        VIXOnAmazon: str = "VXAZNCLS"
        """CBOE Equity VIX on Amazon (in Index)"""

        VXO: str = "VXOCLS"
        """CBOE S&P 100 Volatility Index: VXO (in Index)"""

        VXN: str = "VXNCLS"
        """CBOE NASDAQ 100 Volatility Index (in Index)"""

        TenYearTreasuryNoteVolatilityFutures: str = "VXTYN"
        """CBOE 10-Year Treasury Note Volatility Futures (in Index)"""

        RVX: str = "RVXCLS"
        """CBOE Russell 2000 Volatility Index (in Index)"""

        SP500ThreeMonthVolatilityIndex: str = "VXVCLS"
        """CBOE S&P 500 3-Month Volatility Index (in Index)"""

        VIXOnApple: str = "VXAPLCLS"
        """CBOE Equity VIX on Apple (in Index)"""

        GoldMinersETFVolatilityIndex: str = "VXGDXCLS"
        """CBOE Gold Miners ETF Volatility Index (in Index)"""

        ChinaETFVolatilityIndex: str = "VXFXICLS"
        """CBOE China ETF Volatility Index (in Index)"""

        BrazilETFVolatilityIndex: str = "VXEWZCLS"
        """CBOE Brazil ETF Volatility Index (in Index)"""

        EmergingMarketsETFVolatilityIndex: str = "VXEEMCLS"
        """CBOE Emerging Markets ETF Volatility Index (in Index)"""

        EuroCurrencyETFVolatilityIndex: str = "EVZCLS"
        """CBOE EuroCurrency ETF Volatility Index (in Index)"""

        GoldETFVolatilityIndex: str = "GVZCLS"
        """CBOE Gold ETF Volatility Index (in Index)"""

        CrudeOilETFVolatilityIndex: str = "OVXCLS"
        """CBOE Crude Oil ETF Volatility Index (in Index)"""

        SilverETFVolatilityIndex: str = "VXSLVCLS"
        """CBOE Silver ETF Volatility Index (in Index)"""

        EnergySectorETFVolatilityIndex: str = "VXXLECLS"
        """CBOE Energy Sector ETF Volatility Index (in Index)"""

        VIX: str = "VIXCLS"
        """CBOE Volatility Index: VIX (in Index)"""

    class CentralBankInterventions(System.Object):
        """This class has no documentation."""

        JapaneseBankPurchasesOfDmEuroAgainstJpy: str = "JPINTDDMEJPY"
        """Japan Intervention: Japanese Bank purchases of DM/Euro against JPY (in 100 Million Yen)"""

        JapaneseBankPurchasesOfUsdAgainstDm: str = "JPINTDEXR"
        """Japan Intervention: Japanese Bank purchases of USD against DM (in 100 Million Yen)"""

        JapaneseBankPurchasesOfUsdAgainstRupiah: str = "JPINTDUSDRP"
        """Japan Intervention: Japanese Bank purchases of USD against Rupiah (in 100 Million Yen)"""

        USInterventionInMarketTransactionsInTheJpyUsd: str = "USINTDMRKTJPY"
        """U.S. Intervention: in Market Transactions in the JPY/USD (Millions of USD) (in Millions of USD)"""

        USInterventionWithCustomerTransactionsInOtherCurrencies: str = "USINTDCSOTH"
        """U.S. Intervention: With-Customer Transactions in Other Currencies (Millions of USD) (in Millions of USD)"""

        USInterventionWithCustomerTransactionsInTheJpyUsd: str = "USINTDCSJPY"
        """U.S. Intervention: With-Customer Transactions in the JPY/USD (Millions of USD) (in Millions of USD)"""

        USInterventionWithCustomerTransactionsInTheDemUsdEuro: str = "USINTDCSDM"
        """U.S. Intervention: With-Customer Transactions in the DEM/USD (Euro since 1999) (Millions of USD) (in Millions of USD)"""

        USInterventionInMarketTransactionsInOtherCurrencies: str = "USINTDMRKTOTH"
        """U.S. Intervention: in Market Transactions in Other Currencies (Millions of USD) (in Millions of USD)"""

        CentralBankOfTurkeyPurchasesOfUsd: str = "TRINTDEXR"
        """Turkish Intervention: Central Bank of Turkey Purchases of USD (Millions of USD) (in Millions of USD)"""

        JapaneseBankPurchasesOfUsdAgainstJpy: str = "JPINTDUSDJPY"
        """Japan Intervention: Japanese Bank purchases of USD against JPY (in 100 Million Yen)"""

        USInterventionInMarketTransactionsInTheDemUsdEuro: str = "USINTDMRKTDM"
        """U.S. Intervention: in Market Transactions in the DEM/USD (Euro since 1999) (Millions of USD) (in Millions of USD)"""

        SwissNationalBankPurchasesOfDemAgainstChfMillionsOfDem: str = "CHINTDCHFDM"
        """Swiss Intervention: Swiss National Bank Purchases of DEM against CHF (Millions of DEM) (in Millions of DEM)"""

        SwissNationalBankPurchasesOfUsdAgainstDem: str = "CHINTDUSDDM"
        """Swiss Intervention: Swiss National Bank Purchases of USD against DEM (Millions of USD) (in Millions of USD)"""

        SwissNationalBankPurchasesOfUsdAgainstJpy: str = "CHINTDUSDJPY"
        """Swiss Intervention: Swiss National Bank Purchases of USD against JPY (Millions of USD) (in Millions of USD)"""

        SwissNationalBankPurchasesOfUsdAgainstChf: str = "CHINTDCHFUSD"
        """Swiss Intervention: Swiss National Bank Purchases of USD against CHF (Millions of USD) (in Millions of USD)"""

        BancoDeMexicoPurchaseOnTheUsd: str = "MEXINTDUSD"
        """Mexican Intervention: Banco de Mexico Purchase on the USD (in Millions of USD)"""

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Return the URL string source of the file. This will be converted to a stream
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: String URL of source file.
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


class Observation(System.Object):
    """This class has no documentation."""

    @property
    def RealtimeStart(self) -> str:
        ...

    @RealtimeStart.setter
    def RealtimeStart(self, value: str):
        ...

    @property
    def RealtimeEnd(self) -> str:
        ...

    @RealtimeEnd.setter
    def RealtimeEnd(self, value: str):
        ...

    @property
    def Date(self) -> datetime.datetime:
        ...

    @Date.setter
    def Date(self, value: datetime.datetime):
        ...

    @property
    def Value(self) -> str:
        ...

    @Value.setter
    def Value(self, value: str):
        ...


class FredApi(QuantConnect.Data.BaseData):
    """This class has no documentation."""

    @property
    def RealtimeStart(self) -> str:
        ...

    @RealtimeStart.setter
    def RealtimeStart(self, value: str):
        ...

    @property
    def RealtimeEnd(self) -> str:
        ...

    @RealtimeEnd.setter
    def RealtimeEnd(self, value: str):
        ...

    @property
    def ObservationStart(self) -> str:
        ...

    @ObservationStart.setter
    def ObservationStart(self, value: str):
        ...

    @property
    def ObservationEnd(self) -> str:
        ...

    @ObservationEnd.setter
    def ObservationEnd(self, value: str):
        ...

    @property
    def Units(self) -> str:
        ...

    @Units.setter
    def Units(self, value: str):
        ...

    @property
    def OutputType(self) -> int:
        ...

    @OutputType.setter
    def OutputType(self, value: int):
        ...

    @property
    def FileType(self) -> str:
        ...

    @FileType.setter
    def FileType(self, value: str):
        ...

    @property
    def OrderBy(self) -> str:
        ...

    @OrderBy.setter
    def OrderBy(self, value: str):
        ...

    @property
    def SortOrder(self) -> str:
        ...

    @SortOrder.setter
    def SortOrder(self, value: str):
        ...

    @property
    def Count(self) -> int:
        ...

    @Count.setter
    def Count(self, value: int):
        ...

    @property
    def Offset(self) -> int:
        ...

    @Offset.setter
    def Offset(self, value: int):
        ...

    @property
    def Limit(self) -> int:
        ...

    @Limit.setter
    def Limit(self, value: int):
        ...

    @property
    def Observations(self) -> System.Collections.Generic.IList[QuantConnect.Data.Custom.Fred.Observation]:
        ...

    @Observations.setter
    def Observations(self, value: System.Collections.Generic.IList[QuantConnect.Data.Custom.Fred.Observation]):
        ...

    AuthCode: str
    """Gets the FRED API token."""

    IsAuthCodeSet: bool
    """Returns true if the FRED API token has been set."""

    @staticmethod
    def SetAuthCode(authCode: str) -> None:
        """
        Sets the EIA API token.
        
        :param authCode: The EIA API token
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Return the URL string source of the file. This will be converted to a stream
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: String URL of source file.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, content: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Readers the specified configuration.
        
        :param config: The configuration.
        :param content: The content.
        :param date: The date.
        :param isLiveMode: if set to true [is live mode].
        """
        ...


