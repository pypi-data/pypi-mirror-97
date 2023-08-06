import re

PII_REGEX = re.compile(r'(?i)(street|ein|address|zip|post_code|postcode|postal_code|location|locality|latitude|longitude|carrier_route|name|first_name|full_name|last_name|middle_name|suffix|phone|email|ssn|date_of_birth|date_of_death|contact|sms|court_case|sex_offender|deceased|owner|relation|gender|infoprivacy|tax|legal|business_name|businessname|companyname)')
