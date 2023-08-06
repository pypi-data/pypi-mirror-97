# CHANGELOG

## 4.4.0 2021-03-05

* Added Turbine plugin decorators to the helpers file.

## 4.3.3 2021-02-17

* updated six from 1.12.0 to 1.13.0

## 4.3.2 - 2021-02-01
* fixed create_attachment so that it works in python3

## 4.3.1 - 2021-01-11
* brought linked header pagination up to date with the base pagination class
* Made flattener faster for large dicts that contain listdicts in them.

## 4.3.0 - 2020-12-31
* in rest.py, request will now return a status action if it is called.
  previously it was only called, expecting a raise to happen in the action.

## 4.2.6 - 2020-12-18
* removed compat.py and made extract ioc never search for yara rules.
* This fixes windows compatibility issues

## 4.2.5 - 2020-12-17
* Made count_results default to return the length of a list.

## 4.2.4 - 2020-12-16
* verbose_errors was not being set by asset_parser, now it is.

## 4.2.3 - 2020-12-9
* Added compat.py which has a patch for iocextract.extract_iocs yara rules.

## 4.2.2 - 2020-11-18
* Default autoparse_dt_str to False in do_flatten and Flattener

## 4.2.1 - 2020-11-03
* Fixed issue with linebreaks causing IOCs to be missed.
* No longer return second level domains in the domain list

## 4.2.0 - 2020-10-29
* Added debugging tool to create_test_connection functionality. 

## 4.1.0 - 2020-10-15
* Moved configure_status_actions to init along with verbose errors and default_status_actions=True

## 4.0.1 - 2020-10-14
* Added ISO 8601 Period time converter to relative times
* Made add_raw_json in do_flatten default to True

## 4.0.0 - 2020-09-25
* Changed the format for relative times

## 3.2.2 - 2020-09-22
* Fixed flatten type override sometimes not working correctly

## 3.2.1 - 2020-09-17
* New option to Flattener, flatten type override dict

## 3.2.0 - 2020-09-16
* New option in do_flatten to add raw_json key

## 3.1.1 - 2020-09-15
* Fix import error

## 3.1.0 - 2020-09-01
* Documentation updates
* Added raw_json to parse_response

## 3.0.0 - 2020-09-01
* Updated pendulum to version 2.1.2

## 2.10.0 - 2020-08-17
* Added comparison time values for querystringparser
* Moved parse_dt func to helpers

## 2.9.6 - 2020-08-11
*  Float timestamps can now be parsed by is_datetime/parse_datetime

## 2.9.5 - 2020-08-11
*  Revert pendulum update

## 2.9.4 - 2020-08-06
*  Updated pendulum to the latest version

## 2.9.3 - 2020-08-06
*  Added result limiting to combine_responses

## 2.9.2 - 2020-07-24
*  Fixed count_result bug in pagination

## 2.9.1 - 2020-07-21
* Fixed parse response bug in pagination

## 2.9.0 - 2020-07-21
* Added limit option to BasicRestPaginationEndpoint
* Added extend_nested_lists to flattener
* Added option to remove placeholder / fixed placeholder issue in merge_dicts with BasicList

## 2.8.1 - 2020-07-14
 * Improved epoch parsing for is_datetime/parse_datetime functions
 
## 2.8.0 - 2020-07-06
 * Refactored HTTP error handling to be more consistent.

## 2.7.0 - 2020-05-28
* Added an "unflatten" function to flattener

## 2.6.0 - 2020-05-20
* Prevent shallow flatten from effecting nested lists

## 2.5.1 - 2020-05-14
* Fixed nested list of None issue with Flattener

## 2.5.0 - 2020-05-13
* Added parse_datetime helpers function

## 2.4.13 - 2020-04-27
* Added fix for uppercase domains

## 2.4.11 - 2020-04-16
* Fix manifest to include data files

## 2.4.10 - 2020-04-14
* Restricted the criteria for a domain type in the ioc typer

## 2.4.9 - 2020-04-3
* Added a relative time format in querystring parser

## 2.4.8 - 2020-03-31
* add better substring generation for ioc parsing

## 2.4.7 - 2020-03-30
* dependency fix

## 2.4.6 - 2020-03-27
* Adding a python library not included in the swimlane container

## 2.4.4-5 - 2020-03-20
* fixing issue with the package setup

## 2.4.3 - 2020-03-20
* Fixed issue with unicode literals in python2.7

## 2.4.2 - 2020-03-19
* Added handling for punycode in URLs to the IOC parser

## 2.4.1 - 2020-03-16
* Removed debug code in previous release

## 2.4.0 - 2020-03-13
* Added an IOC parser and typer

## 2.3.3 - 2020-3-01
* Fixed python3 build

## 2.3.3 - 2020-3-01
* Added QueryStringParser for a standard way to parse querystrings

## 2.3.2 - 2020-2-24
* Added kwarg overwriting to asset_parser

## 2.3.1 - 2020-2-13
* Fixed an edgecase in the flattener due to very nested list data

## 2.3.0 - 2020-01-24
* Added ability to setup Swimlane Exceptions for rest status codes

## 2.2.0 - 2019-12-16
* Added more Exceptions to exception module
* Added the option to provide a port to asset_parser

## 2.1.2 - 2019-11-13
* in LinkHeadersPaginationEndpoint, pagination now ends when the key "next" is not in links

## 2.1.1 - 2019-10-18
* Added ignore_dt_format to ignore datetime formats in parsing

## 2.1.0 - 2019-09-20
* Backwards incompatible bugfixes in flattener
* Docs

## 2.0.0 - 2019-09-06
* Added helper for testconnection
* Added helper for attachments
* Added custom validator
* Mintor Flattener restructure and refactor
* Updated cleanxmltodict in Flattener
* Added optional input flag to InputChecker
* Added option to autoparse out datetime strings
* Added a keep_simple_lists param if stringify is set

## 1.2.3 - 2019-09-04
* Bumped validators to 0.14.0

## 1.2.2 - 2019-09-04
* Bumped dict-plus dependency to 0.1.1

## 1.2.1 - 2019-09-04
* Added Flattener().flatten() alias, do_flatten()
* Moved changelog to correct spot

## 1.2.0 - 2019-08-27
* Updated flattener to be consistent with Py2 & Py3, and previous versions
* Added helper submodule for asset parsing and input checking

## 1.1.8 - 2019-08-08
* Updated package to be consistent with Python3 and Python2
* Added CHANGELOG

## 1.1.7 - 2019-06-19

* Added useragent from PR
* Added Mixin Cleanup from PR
* Added polling

## 1.1.6 - 2019-06-18

* Minor cleanup and fixes
* PR-4 Fixes
* Added clean_xmltodict helper func

## 1.1.2 - 2018-10-24

* Initial Package Version Tracking
