#!/usr/bin/env python
"""Shared resources, so that commonly used information is all in one place.
"""

__license__ = "GPL"
__version__ = "0.0"
__status__ = "Development"


# names of the columns in the pandas dataframe
pandas_column_names = ['zillow_id',
                       'zillow_addressStreet',
                       'zillow_addressCity',
                       'zillow_addressState',
                       'zillow_zipcode',
                       'zillow_features',
                       'zillow_price',
                       'zillow_longitude',
                       'zillow_latitude',
                       'zillow_status',
                       'zillow_homeType',
                       'date_scraped',
                       'location',
                       'google_start_address',
                       'google_start_location',
                       'google_end_address',
                       'google_end_location',
                       'morning_drive_duration',
                       'morning_drive_duration_with_traffic',
                       'evening_drive_duration',
                       'evening_drive_duration_with_traffic',
                       'morning_transit_duration',
                       'evening_transit_duration']


# Grabbed from http://www.city-data.com/county/Santa_Clara_County-CA.html
santa_clara_county_zip ='\
94022 \
94023 \
94024 \
94040 \
94041 \
94042 \
94043 \
94085 \
94086 \
94087 \
94089 \
94301 \
94304 \
94305 \
94306 \
95002 \
95008 \
95014 \
95020 \
95030 \
95031 \
95032 \
95033 \
95035 \
95037 \
95038 \
95046 \
95050 \
95051 \
95054 \
95056 \
95070 \
95108 \
95110 \
95111 \
95112 \
95113 \
95116 \
95117 \
95118 \
95119 \
95120 \
95121 \
95122 \
95123 \
95124 \
95125 \
95126 \
95127 \
95128 \
95129 \
95130 \
95131 \
95132 \
95133 \
95134 \
95135 \
95136 \
95138 \
95139 \
95140 \
95148 \
95150 \
95151 \
95158 \
95160 \
95164'
santa_clara_county_zip = santa_clara_county_zip.split(' ')


# http://www.city-data.com/county/Santa_Cruz_County-CA.html
santa_cruz_county_zip = '\
95001 \
95003 \
95005 \
95006 \
95010 \
95017 \
95018 \
95019 \
95060 \
95061 \
95062 \
95063 \
95064 \
95065 \
95066 \
95067 \
95073 \
95076'
santa_cruz_county_zip = santa_cruz_county_zip.split(' ')

# http://www.city-data.com/county/San_Mateo_County-CA.html
san_mateo_county_zip = '\
94002 \
94005 \
94010 \
94014 \
94015 \
94018 \
94019 \
94020 \
94021 \
94025 \
94026 \
94027 \
94028 \
94029 \
94030 \
94037 \
94038 \
94044 \
94060 \
94061 \
94062 \
94063 \
94065 \
94066 \
94070 \
94074 \
94080 \
94128 \
94303 \
94401 \
94402 \
94403 \
94404'
san_mateo_county_zip = san_mateo_county_zip.split(' ')

# http://www.city-data.com/county/San_Francisco_County-CA.html
san_francisco_county_zip ='\
94103 \
94102 \
94104 \
94105 \
94107 \
94108 \
94109 \
94110 \
94111 \
94112 \
94114 \
94115 \
94116 \
94117 \
94118 \
94119 \
94121 \
94122 \
94123 \
94124 \
94127 \
94129 \
94131 \
94132 \
94133 \
94134 \
94137 \
94142 \
94188'
san_francisco_county_zip = san_francisco_county_zip.split(' ')

# http://www.city-data.com/county/Alameda_County-CA.html
alameda_county_zip = '\
94501 \
94502 \
94536 \
94538 \
94539 \
94541 \
94542 \
94544 \
94545 \
94546 \
94550 \
94551 \
94552 \
94555 \
94560 \
94566 \
94568 \
94577 \
94578 \
94579 \
94580 \
94582 \
94586 \
94587 \
94588 \
94601 \
94602 \
94603 \
94605 \
94606 \
94607 \
94608 \
94609 \
94610 \
94611 \
94612 \
94618 \
94619 \
94621 \
94650 \
94702 \
94703 \
94704 \
94705 \
94706 \
94707 \
94708 \
94709 \
94710'
alameda_county_zip = alameda_county_zip.split(' ')

# http://www.city-data.com/county/Contra_Costa_County-CA.html
contra_costa_county_zip = '\
94506 \
94507 \
94509 \
94511 \
94513 \
94514 \
94516 \
94517 \
94518 \
94519 \
94520 \
94521 \
94523 \
94524 \
94525 \
94526 \
94528 \
94530 \
94531 \
94547 \
94549 \
94553 \
94556 \
94561 \
94563 \
94564 \
94565 \
94583 \
94595 \
94596 \
94597 \
94598 \
94801 \
94803 \
94804 \
94805 \
94806'
contra_costa_county_zip = contra_costa_county_zip.split(' ')

# http://www.city-data.com/county/Marin_County-CA.html
marin_county_zip = '\
94901 \
94903 \
94904 \
94920 \
94924 \
94925 \
94930 \
94933 \
94937 \
94939 \
94941 \
94942 \
94945 \
94946 \
94947 \
94949 \
94950 \
94956 \
94957 \
94960 \
94965 \
94970 \
94973 \
94979'
marin_county_zip = marin_county_zip.split(' ')

# http://www.city-data.com/county/Solano_County-CA.html
solano_county_zip ='\
94510 \
94533 \
94534 \
94571 \
94585 \
94589 \
94590 \
94591 \
95620 \
95687 \
95688'
solano_county_zip = solano_county_zip.split(' ')

# http://www.city-data.com/county/Sonoma_County-CA.html
sonoma_county_zip ='\
94927 \
94928 \
94931 \
94951 \
94952 \
94954 \
95401 \
95402 \
95403 \
95404 \
95405 \
95407 \
95409 \
95416 \
95425 \
95436 \
95439 \
95442 \
95446 \
95448 \
95452 \
95471 \
95472 \
95473 \
95476 \
95486 \
95492 \
95497'
sonoma_county_zip = sonoma_county_zip.split(' ')

# http://www.city-data.com/county/Napa_County-CA.html
napa_county_zip = '\
94503 \
94508 \
94515 \
94558 \
94559 \
94574 \
94581 \
94599'
napa_county_zip = napa_county_zip.split(' ')

# http://www.city-data.com/county/San_Joaquin_County-CA.html
san_joaquin_county_zip ='\
95204 \
95205 \
95206 \
95207 \
95209 \
95210 \
95212 \
95215 \
95219 \
95220 \
95227 \
95236 \
95237 \
95240 \
95242 \
95258 \
95269 \
95290 \
95304 \
95320 \
95330 \
95336 \
95337 \
95366 \
95376 \
95377'
san_joaquin_county_zip = san_joaquin_county_zip.split(' ')

all_counties = santa_clara_county_zip + santa_cruz_county_zip + \
    san_mateo_county_zip + san_francisco_county_zip + alameda_county_zip + \
    contra_costa_county_zip + marin_county_zip + solano_county_zip + \
    sonoma_county_zip + napa_county_zip + san_joaquin_county_zip


kane_county_zip = '\
60505 \
60120 \
60506 \
60123 \
60504 \
60110 \
60538 \
60102 \
60510 \
60134 \
60142 \
60174 \
60175 \
60177 \
60502 \
60124 \
60140 \
60118 \
60542 \
60554 \
60119 \
60136 \
60184 \
60151 \
60511 \
60144 \
60539 \
60109 \
60183 \
60170 \
60121 \
60147 \
60507 \
60568'
kane_county_zip = kane_county_zip.split(' ')

dupage_county_zip ='\
60148 \
60126 \
60564 \
60540 \
60188 \
60103 \
60504 \
60133 \
60563 \
60101 \
60565 \
60137 \
60185 \
60517 \
60139 \
60181 \
60532 \
60187 \
60515 \
60527 \
60516 \
60189 \
60108 \
60502 \
60439 \
60561 \
60559 \
60172 \
60106 \
60521 \
60191 \
60555 \
60143 \
60523 \
60190 \
60514 \
60184 \
60570 \
60157 \
60125 \
60199 \
60666 \
60519 \
60569 \
60116 \
60117 \
60122 \
60128 \
60132 \
60138 \
60186 \
60197 \
60522 \
60566 \
60567 \
60572 \
60598 \
60599 \
60399'
dupage_county_zip = dupage_county_zip.split(' ')

cook_county_zip ='\
60629 \
60618 \
60639 \
60804 \
60647 \
60632 \
60617 \
60623 \
60608 \
60625 \
60634 \
60620 \
60657 \
60614 \
60641 \
60640 \
60628 \
60609 \
60402 \
60651 \
60619 \
60638 \
60453 \
60016 \
60056 \
60630 \
60622 \
60411 \
60120 \
60004 \
60613 \
60616 \
60010 \
60643 \
60626 \
60645 \
60644 \
60637 \
60193 \
60649 \
60062 \
60107 \
60659 \
60067 \
60707 \
60652 \
60610 \
60462 \
60025 \
60169 \
60068 \
60103 \
60477 \
60660 \
60133 \
60089 \
60074 \
60201 \
60624 \
60090 \
60615 \
60409 \
60612 \
60714 \
60007 \
60202 \
60302 \
60076 \
60631 \
60636 \
60653 \
60611 \
60525 \
60646 \
60607 \
60438 \
60005 \
60527 \
60077 \
60655 \
60018 \
60621 \
60605 \
60459 \
60487 \
60663 \
60091 \
60452 \
60053 \
60160 \
60467 \
60153 \
60679 \
60827 \
60473 \
60706 \
60439 \
60406 \
60656 \
60443 \
60172 \
60642 \
60426 \
60131 \
60803 \
60654 \
60008 \
60419 \
60597 \
60513 \
60805 \
60430 \
60164 \
60466 \
60093 \
60104 \
60304 \
60455 \
60465 \
60546 \
60521 \
60070 \
60118 \
60445 \
60154 \
60429 \
60633 \
60457 \
60173 \
60415 \
60026 \
60463 \
60478 \
60458 \
60526 \
60130 \
60712 \
60558 \
60192 \
60428 \
60422 \
60176 \
60601 \
60501 \
60305 \
60471 \
60534 \
60482 \
60171 \
60464 \
60661 \
60418 \
60475 \
60162 \
60155 \
60022 \
60480 \
60425 \
60606 \
60398 \
60461 \
60674 \
60469 \
60472 \
60163 \
60203 \
60165 \
60456 \
60195 \
60194 \
60208 \
60476 \
60301 \
60043 \
60499 \
60603 \
60179 \
60602 \
60666 \
60604 \
60029 \
60141 \
60196 \
60669 \
60290 \
60209 \
60082 \
60204 \
60675 \
60688 \
60701 \
60006 \
60009 \
60011 \
60017 \
60019 \
60038 \
60055 \
60065 \
60078 \
60094 \
60095 \
60105 \
60159 \
60161 \
60168 \
60303 \
60412 \
60454 \
60664 \
60668 \
60670 \
60673 \
60677 \
60678 \
60681 \
60680 \
60684 \
60682 \
60686 \
60685 \
60687 \
60690 \
60689 \
60693 \
60691 \
60695 \
60694 \
60697 \
60696 \
60699'
cook_county_zip = cook_county_zip.split(' ')

will_county_zip ='\
60440 \
60435 \
60586 \
60564 \
60446 \
60565 \
60451 \
60517 \
60441 \
60423 \
60544 \
60487 \
60448 \
60585 \
60491 \
60439 \
60432 \
60431 \
60490 \
60404 \
60466 \
60436 \
60417 \
60403 \
60433 \
60503 \
60442 \
60410 \
60481 \
60475 \
60449 \
60484 \
60401 \
60468 \
60408 \
60421 \
60407 \
60434'
will_county_zip = will_county_zip.split(' ')

mchenry_county_zip = '\
60014 \
60098 \
60102 \
60050 \
60142 \
60156 \
60013 \
60051 \
60033 \
60012 \
60152 \
60081 \
60097 \
60042 \
60071 \
60021 \
60180 \
60072 \
60034 \
60297 \
60296 \
60001 \
60039'
mchenry_county_zip = mchenry_county_zip.split(' ')

lake_county_zip = '\
60085 \
60073 \
60010 \
60047 \
60030 \
60060 \
60089 \
60031 \
60099 \
60046 \
60048 \
60035 \
60015 \
60061 \
60087 \
60002 \
60013 \
60051 \
60045 \
60064 \
60084 \
60041 \
60083 \
60081 \
60044 \
60088 \
60069 \
60042 \
60020 \
60096 \
60040 \
60037 \
60049 \
60092 \
60075 \
60079 \
60086'
lake_county_zip = lake_county_zip.split(' ')

kendall_county_zip ='\
60586 \
60543 \
60538 \
60544 \
60560 \
60431 \
60447 \
60545 \
60503 \
60541 \
60536 \
60512 \
60537'
kendall_county_zip = kendall_county_zip.split(' ')

all_chicago_counties = kane_county_zip + dupage_county_zip + \
    cook_county_zip + will_county_zip + mchenry_county_zip + \
    lake_county_zip + kendall_county_zip
