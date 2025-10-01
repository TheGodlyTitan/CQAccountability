class Constants:
    """
    Holds constant values for dropdowns and selections.
    It is only recommended to edit this file if you know what you're doing.
    
    Notes
    -----
    Remove all USSF Signature Options.
        
    Missing MTL Assignments (D-Bays)
        - FD2 
        - FD3
        - WD2
    """
    
    # Dropdown options for the manor selector
    manor_options = [
        "Winters",
        "Fosters",
    ]
    
    # AL Team roles
    al_roles = [
        "ALD (Weekends Only)", 
        "ALD Shadow (Weekends Only)", 
        "AL Cards", 
        "AL Cards Shadow"
    ]
    
    # CQ Team roles  
    cq_roles = [
        "CQ Lead", 
        "CQ Door Guard", 
        "CQ Runner"
    ]
    
    # Rank options for personnel selection
    # This includes Space Force E-1 to E-4 equivalencies (Winters)
    rank_options = [
        "E-1 (AB)",
        "E-2 (Amn)",
        "E-3 (A1C)",
        "E-4 (SrA)",
        "E-1 (Spc1)",
        "E-2 (Spc2)",
        "E-3 (Spc3)",
        "E-4 (Spc4)",
    ]
    
    # List of all MTLs for notes section
    on_call_mtls = [
        "TSgt Culpepper",
        "TSgt Brown",
        "TSgt McDonald",
        "TSgt Poe",
        "TSgt Wellman",
        "TSgt Bigham",
        "SSgt Bridgeman",
        "SSgt Mitchell",
        "SSgt Seifert",
        "SSgt Martin",
    ]
    
    # Options for red card late types and times
    # Sign-in - Airman didn't sign-in at CQ.
    # Turn-in - Airman didn't turn-in red card.
    redcard_late_types = ["Sign-in", "Turn-in", "Both"]
    redcard_late_times = ['0900', '1200', '1500', '1800', '2100']
    
    # Standard late times for curfew violations
    # 2100 - Phase 1   (All Weeknights)
    # 2200 - Phase 2/3 (Weekdays)
    # 0000 - Phase 2/3 (Weekends)
    standard_late_times = ['2100', '2200', '0000']
    
    # 338th - Dark Knights - U.S. Air Force
    # 333rd - Mad Ducks    - U.S. Air Force
    # 533rd - Centurions 
    squadron_options = ["338th", "333rd", "533rd"]
    
    # Job titles for USAF and USSF
    job_options = [
        "Network System Operations",
        "Radio Frequency Transmission",
        "Cyber Warfare Operations",
    ]

    # MTL assignments by bay and floor
    # FD1/WD1 - Does not exist
    bay_mtls = {
        # Fosters - Floor 1
        "FA1": "TSgt Culpepper",
        "FB1": "TSgt Culpepper",
        "FC1": "SSgt Mitchell",
        # Fosters - Floor 2
        "FA2": "TSgt McDonald",
        "FB2": "TSgt Brown",
        "FC2": "TSgt Brown",
        "FD2": "N/A",
        # Fosters - Floor 3
        "FA3": "TSgt McDonald",
        "FB3": "SSgt Bridgeman",
        "FC3": "SSgt Bridgeman",
        "FD3": "N/A",
        # Winters - Floor 1
        "WA1": "TSgt Bigham",
        "WB1": "SSgt Seifert",
        "WC1": "SSgt Seifert",
        # Winters - Floor 2
        "WA2": "TSgt Bigham",
        "WB2": "SSgt Martin",
        "WC2": "TSgt Poe",
        "WD2": "N/A",
        # Winters - Floor 3 (Space Force)
        "WA3": "TSgt Wellman",
        "WB3": "TSgt Wellman",
        "WC3": "TSgt Wellman",
        "WD3": "TSgt Wellman",
    }
    
    
