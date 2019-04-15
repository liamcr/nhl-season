# nhl-season

This script uses data from regular season NHL games to simulate an entire NHL season and crown a Stanley Cup champion.

## Usage

First, you must use loadSeasonDataJSON.py to load the necessary regular season data into a json file. You will be asked to provide some information:

  * `Filename`: The name of the file that the data will be stored in. Must be .json
  * `Start date`: The date the program will begin collecting data from
  * `End date`: The date the program will stop collecting data from

For example, if you input 10-01-18 as the start date, and 04-10-19 as the end date, the data the program stores in the file will be based on how the teams performed between October 1st, 2018 and April 10th, 2019.

After that is done, you can simulate a season by using fullNHLSeason.py:

  `python ./fullNHLSeason.py seasonDataFile.json`

The output will look something like:

  ```TOR 2 - 4 MTL
  WSH 5 - 3 BOS     
  VAN 3 - 4 CGY     
  SJS 2 - 0 ANA
  ...
  CGY 4 - 1 EDM     
  LAK 5 - 4 VGK (OT)
  SJS 2 - 4 COL     
  1.	TBL	61-18-3 	125 pts
  2.	CGY	51-25-6 	108 pts
  3.	NYI	52-28-2 	106 pts
  ...
  30.	ANA	25-45-12 	62 pts
  31.	OTT	27-50-5 	59 pts
  CGY 4 - 3 MIN      [CGY 1 - 0 MIN]
  CGY 5 - 2 MIN      [CGY 2 - 0 MIN]
  MIN 1 - 2 CGY      [CGY 3 - 0 MIN]
  MIN 0 - 1 CGY      [CGY 4 - 0 MIN]
  CGY wins the series 4-0
  ------------------------------
  WPG 8 - 0 DAL      [WPG 1 - 0 DAL]
  WPG 4 - 1 DAL      [WPG 2 - 0 DAL]
  DAL 2 - 3 WPG      [WPG 3 - 0 DAL]
  DAL 2 - 4 WPG      [WPG 4 - 0 DAL]
  WPG wins the series 4-0
  ------------------------------
  ...
  TBL 5 - 2 CGY      [TBL 1 - 0 CGY]
  TBL 3 - 7 CGY      [TBL 1 - 1 CGY]
  CGY 4 - 2 TBL      [TBL 1 - 2 CGY]
  CGY 4 - 3 TBL (OT) [TBL 1 - 3 CGY]
  TBL 2 - 1 CGY      [TBL 2 - 3 CGY]
  CGY 3 - 4 TBL      [TBL 3 - 3 CGY]
  TBL 4 - 3 CGY (OT) [TBL 4 - 3 CGY]
  TBL wins the series 4-3
  ------------------------------
  Stanley Cup Champions: TBL```
