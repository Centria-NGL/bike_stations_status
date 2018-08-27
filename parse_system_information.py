def parseSystemInformation(bundle):
    systemData = bundle["data"]
    system_info_bundle = dict()
    system_info_bundle["SYSTEM_ID"] = systemData["system_id"]
    system_info_bundle["LANGUAGE"] = systemData["language"]
    system_info_bundle["NAME"] = systemData["name"]
    system_info_bundle["SHORT_NAME"] = systemData["short_name"]
    system_info_bundle["OPERATOR"] = systemData["operator"]
    system_info_bundle["URL"] = systemData["url"]
    system_info_bundle["PURCHASE_URL"] = systemData["purchase_url"]
    system_info_bundle["START_DATE"] = systemData["start_date"]
    system_info_bundle["PHONE_NUMBER"] = systemData["phone_number"]
    system_info_bundle["EMAIL"] = systemData["email"]
    system_info_bundle["TIMEZONE"] = systemData["timezone"]
    system_info_bundle["LICENSE_URL"] = systemData["license_url"]
    return system_info_bundle
