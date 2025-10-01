import re
import logging
from constants import Constants 


log = logging.getLogger('app.processing')


RANK_MAPPINGS = {
    "E-1 (AB)": "AB",
    "E-2 (Amn)": "Amn",
    "E-3 (A1C)": "A1C",
    "E-4 (SrA)": "SrA",
    "E-1 (Spc1)": "Spc1",
    "E-2 (Spc2)": "Spc2",
    "E-3 (Spc3)": "Spc3",
    "E-4 (Spc4)": "Spc4",
}

BRANCH_MAPPINGS = {
    "U.S. Air Force": "USAF",
    "U.S. Space Force": "USSF",
    "U.S. Army": "USA",
    "U.S. Navy": "USN",
    "U.S. Marine Corps": "USMC",
    "U.S. Coast Guard": "USCG",
}

CQ_ROLE_ORDER = [
    "ALD (Weekends Only)", 
    "ALD Shadow (Weekends Only)", 
    None, 
    "AL Cards", 
    "AL Cards Shadow", 
    None, 
    "CQ Lead", 
    "CQ Door Guard", 
    "CQ Runner"
]

REQUIRED_AL_ROLES = [
    "AL Cards"
]

REQUIRED_CQ_ROLES = [
    "CQ Lead", 
    "CQ Door Guard"
]

REQUIRE_SIGNATURE_FIELDS = [
    "Rank", 
    "Last", "First", "MI", 
    "AFSC/Job", 
    "Squadron"
]


class ValidationException(Exception):
    """Custom exception to hold a list of validation errors."""
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__(f"Validation failed with {len(errors)} errors.")


def get_mtl_from_room(manor: str, room_number: str) -> str:
    """Parses a manor and room number to find the corresponding MTL."""
    if not manor or not room_number:
        return "N/A"

    # 1. Get the first letter of the Manor (F or W)
    manor_char = manor[0].upper()

    # 2. Get the Bay and Floor from the room number (e.g., C1 from "C116")
    cleaned_room = room_number.upper().replace(" ", "").replace("-", "")
    if len(cleaned_room) < 2:
        return "N/A"
    bay_and_floor = cleaned_room[:2]

    # 3. Combine them into the key (e.g., "FC1")
    bay_key = f"{manor_char}{bay_and_floor}"
    
    return Constants.bay_mtls.get(bay_key, "<Unknown MTL>")


def _validate_room_number(room: str) -> str:
    """
    Validates and formats a room number.
    
    A valid format is a letter (A-C) followed by floor (1-3) and two digits (e.g., 'C116').
    """
    cleaned_room = room.upper().strip().replace(" ", "").replace("-", "")
    
    # Pattern: [A-D] [1-3] [0-9]{2}
    if not re.fullmatch(r"[A-D][1-3]\d{2}", cleaned_room):
        raise ValidationException(f"Invalid room format: '{room}'. Must be like 'A101', 'B205', etc.")
        
    return cleaned_room


def _get_person_data(entries: dict, role_context: str, is_late_entry: bool) -> dict | None:
    """
    Extracts, formats, and validates data from a set of person entry widgets.
    
    Returns None if all name/rank fields are empty.
    """
    rank = entries["Rank"].get()
    last = entries["Last"].get().strip()
    first = entries["First"].get().strip()
    mi = entries["MI"].get().strip()

    if not rank and not last and not first and not mi:
        return None
    
    # Validation: If any data is entered, Rank/Last Name are required.
    if not rank or not last:
        raise ValidationException(f"Missing Rank/Last Name for entry: {role_context}")

    # Auto-formatting
    last = last.title()
    first = first.title()
    if mi:
        mi = mi[0].upper() # Just take the first character and capitalize

    return {
        "rank": rank,
        "last": last,
        "first": first,
        "mi": mi,
    }


def get_form_data(ui_elements: dict) -> dict:
    """Gathers all data from the UI widgets into a dictionary and validates inputs."""
    log.debug("Gathering form data.")
    data = {"al_team": {}, "cq_team": {}, "red_card_lates": [], "lates": [], "manor": ui_elements["manor"].get()}
    errors = []

    # Unpack UI elements for clarity
    al_members = ui_elements["al_members"]
    cq_members = ui_elements["cq_members"]
    red_card_lates = ui_elements["red_card_lates"]
    lates = ui_elements["lates"]
    notes_vars = ui_elements["notes"]
    signature = ui_elements["signature"]
    
    # 0. Manor selection check
    if not data["manor"]:
        errors.append("Please select a Manor (Winters or Fosters).")

    # 1. AL Team
    for role, entries in al_members.items():
        try:
            if person_data := _get_person_data(entries, role, False):
                data["al_team"][role] = person_data
        except ValueError as e:
            errors.append(str(e))
    
    for role in REQUIRED_AL_ROLES:
        if role not in data["al_team"]:
            errors.append(f"Required: Please fill out **{role}**.")

    # 2. CQ Team
    for role, entries in cq_members.items():
        try:
            if role == "CQ Runner":
                runner_data = [_get_person_data(runner_set, "CQ Runner", False) for runner_set in entries]
                data["cq_team"][role] = [r for r in runner_data if r]
            else:
                if person_data := _get_person_data(entries, role, False):
                    data["cq_team"][role] = person_data
        except ValueError as e:
            errors.append(str(e))
    
    for role in REQUIRED_CQ_ROLES:
        if role not in data["cq_team"]:
            errors.append(f"Required: Please fill out **{role}**.")

    # Check for at least one CQ Runner
    if not data["cq_team"].get("CQ Runner"):
        errors.append("Required: Please fill out at least one **CQ Runner**.")


    # 2. Lates Sections
    for key, entries in [("red_card_lates", red_card_lates), ("lates", lates)]:
        is_red_card = (key == "red_card_lates")
        title = "Red-Card Lates" if is_red_card else "Standard Lates"
        
        for i, entry_set in enumerate(entries):
            context = f"{title} Row {i+1}"
            try:
                if person_data := _get_person_data(entry_set, context, is_late_entry=True):
                    late_data = person_data.copy()
                    
                    # Get and validate Room
                    raw_room = entry_set["Room"].get()
                    late_data["room"] = _validate_room_number(raw_room)
                    
                    # Check for other required fields
                    missing_fields = []
                    if not entry_set["Time"].get(): missing_fields.append("Time")
                    if not entry_set["Reason"].get(): missing_fields.append("Reason")
                    
                    late_type = ""
                    if is_red_card:
                        # For Red-Card Lates, 'Type/Late To' is required and collected
                        late_type = entry_set["Type"].get()
                        if not late_type:
                            missing_fields.append("Type/Late To")
                    
                    if missing_fields:
                        errors.append(f"{context}: Missing required field(s): {', '.join(missing_fields)}")
                        continue
                        
                    late_data.update({
                        "time": entry_set["Time"].get(),
                        "type": late_type, # Empty string for Standard Lates
                        "reason": entry_set["Reason"].get().strip(),
                    })
                    data[key].append(late_data)
            except ValueError as e:
                # Only append the error if data was partially entered
                if not entry_set["Rank"].get() and not entry_set["Last"].get():
                     continue 
                errors.append(str(e))


    # 3. Notes and Signature (all signature inputs now required)
    data["notes"] = {
        "cac_scanner_unavailable": notes_vars["cac_scanner"].get(),
        "on_call_mtl": notes_vars["on_call_mtl"].get(),
        "additional_notes": [note.get().strip() for note in notes_vars["additional_notes"] if note.get().strip()],
    }
    
    data["signature"] = {key: widget.get().strip() for key, widget in signature.items()}
    
    missing_fields = [
        field for field in REQUIRE_SIGNATURE_FIELDS 
        if not data["signature"].get(field)
    ]
    
    if missing_fields:
        errors.append(f"Signature section requires all inputs. Missing: {', '.join(missing_fields)}.")

    # Raise all collected errors
    if errors:
        log.error(f"Validation failed with {len(errors)} errors.")
        raise ValidationException(errors)

    log.debug("Finished gathering and validating form data.")
    return data


def get_form_data_for_preview(ui_elements: dict) -> dict:
    """
    Gathers form data for preview purposes, ignoring validation errors.
    Returns partial data even if some fields are incomplete.
    """
    log.debug("Gathering form data for preview.")
    data = {"al_team": {}, "cq_team": {}, "red_card_lates": [], "lates": [], "manor": ui_elements["manor"].get()}

    # Unpack UI elements for clarity
    al_members = ui_elements["al_members"]
    cq_members = ui_elements["cq_members"]
    red_card_lates = ui_elements["red_card_lates"]
    lates = ui_elements["lates"]
    notes_vars = ui_elements["notes"]
    signature = ui_elements["signature"]
    
    # 1. AL Team - ignore validation errors
    for role, entries in al_members.items():
        try:
            if person_data := _get_person_data(entries, role, False):
                data["al_team"][role] = person_data
        except:
            pass

    # 2. CQ Team - ignore validation errors
    for role, entries in cq_members.items():
        try:
            if role == "CQ Runner":
                runner_data = []
                for runner_set in entries:
                    try:
                        if person_data := _get_person_data(runner_set, "CQ Runner", False):
                            runner_data.append(person_data)
                    except:
                        pass
                if runner_data:
                    data["cq_team"][role] = runner_data
            else:
                try:
                    if person_data := _get_person_data(entries, role, False):
                        data["cq_team"][role] = person_data
                except:
                    pass
        except:
            pass

    # 2. Lates Sections - ignore validation errors
    for key, entries in [("red_card_lates", red_card_lates), ("lates", lates)]:
        is_red_card = (key == "red_card_lates")
        
        for entry_set in entries:
            try:
                if person_data := _get_person_data(entry_set, "", is_late_entry=True):
                    late_data = person_data.copy()
                    
                    # Get room, time, reason - use what's available
                    raw_room = entry_set["Room"].get()
                    if raw_room:
                        try:
                            late_data["room"] = _validate_room_number(raw_room)
                        except:
                            late_data["room"] = raw_room  # Use raw value if validation fails
                    else:
                        late_data["room"] = ""
                    
                    late_data["time"] = entry_set["Time"].get()
                    late_data["reason"] = entry_set["Reason"].get().strip()
                    
                    if is_red_card:
                        late_data["type"] = entry_set["Type"].get()
                    else:
                        late_data["type"] = ""
                        
                    data[key].append(late_data)
            except:
                pass

    # 3. Notes and Signature
    data["notes"] = {
        "cac_scanner_unavailable": notes_vars["cac_scanner"].get(),
        "on_call_mtl": notes_vars["on_call_mtl"].get(),
        "additional_notes": [note.get().strip() for note in notes_vars["additional_notes"] if note.get().strip()],
    }
    
    data["signature"] = {key: widget.get().strip() for key, widget in signature.items()}

    return data


def _format_person(person_data: dict) -> str | None:
    """Formats a person's data into a 'Rank Last, First MI' string."""
    if not person_data or not person_data.get("rank"):
        return None
    rank = RANK_MAPPINGS.get(person_data["rank"], "")
    name_part = f"{person_data.get('last', '')}, {person_data.get('first', '')}"
    if mi := person_data.get("mi"):
        name_part += f" {mi}" # Add a period for middle initial
    return f"{rank} {name_part.strip()}"


def format_email_body(data: dict) -> str:
    """Formats the collected data into the final email body string."""
    log.debug("Formatting email body.")
    parts = []
    
    # Combined Team Display (AL Team + CQ Team in order)
    for role in CQ_ROLE_ORDER:
        if role is None:
            # Add a separator only if there's content and it doesn't already end with a separator
            if parts and parts[-1] != "":
                parts.append("")
            continue
        
        # Check AL team first, then CQ team
        role_data = data["al_team"].get(role) or data["cq_team"].get(role)
        
        # Special handling for roles that should always appear even if empty
        if role in ["AL Cards", "CQ Lead", "CQ Door Guard", "CQ Runner"]:
            display_role = role.split('(')[0].strip()
            if role_data:
                if isinstance(role_data, list):
                    for person in role_data:
                        if person_str := _format_person(person):
                            parts.append(f"{display_role}: {person_str}")
                elif person_str := _format_person(role_data):
                    parts.append(f"{display_role}: {person_str}")
                else:
                    parts.append(f"{display_role}:")
            else:
                parts.append(f"{display_role}:")
            continue
        
        if not role_data:
            continue
        
        display_role = role.split('(')[0].strip()
        if isinstance(role_data, list):
            for person in role_data:
                if person_str := _format_person(person):
                    parts.append(f"{display_role}: {person_str}")
        elif person_str := _format_person(role_data):
            parts.append(f"{display_role}: {person_str}")

    # Lates Sections
    manor = data["manor"]
    
    # 1. Red-Card Lates (MUST always be present, showing - N/A if empty)
    parts.append(f"\nRed-Card Lates:")
    if late_entries := data.get("red_card_lates"):
        for entry in late_entries:
            person_str = _format_person(entry)
            bay_mtl = get_mtl_from_room(manor, entry['room'])
            
            # Format the type field - change "Both" to "Sign-in & Turn-in"
            type_text = entry['type']
            if type_text == "Both":
                type_text = "Sign-in & Turn-in"
            
            # Handle empty reason
            reason = entry['reason'].strip() if entry['reason'] else "No reason provided"
            
            parts.append(f"- {person_str} - {entry['room']} - {bay_mtl} - Missed {entry['time']} {type_text} - {reason}")
    else:
        parts.append("- N/A")

    # 2. Standard Lates (MUST always be present, showing - N/A if empty)
    parts.append(f"\nLates:")
    if late_entries := data.get("lates"):
        for entry in late_entries:
            person_str = _format_person(entry)
            bay_mtl = get_mtl_from_room(manor, entry['room'])
            
            # Type is guaranteed to be an empty string for standard lates, so we omit it from the output
            # 'type_info' is only included if it has a value (e.g., from Red-Card Lates in the future)
            type_info = f" {entry['type']}" if entry.get('type') else ""
            
            # Handle empty reason
            reason = entry['reason'].strip() if entry['reason'] else "No reason provided"
            
            parts.append(f"- {person_str} - {entry['room']} - {bay_mtl} - Missed {entry['time']}{type_info} - {reason}")
    else:
        parts.append("- N/A")
        
    # Notes (MUST always be present, showing - N/A if empty)
    parts.append("\nNotes:")
    notes_data = data["notes"]
    notes_content = []
    if notes_data["cac_scanner_unavailable"]:
        notes_content.append("- CAC System Non-Operational: Manual Accountability Used.")
    if on_call_mtl := notes_data["on_call_mtl"]:
        notes_content.append(f"- On-Call MTL: {on_call_mtl}")
    notes_content.extend([f"- {note}" for note in notes_data["additional_notes"]])
    
    if notes_content:
        parts.extend(notes_content)
    else:
        parts.append("- N/A")

    # Signature
    sig = data["signature"]
    if any(sig.values()):
        parts.append("\n\nV/r")
        rank_short = RANK_MAPPINGS.get(sig["Rank"], "")
        name_line = f"{rank_short} {sig['Last']}, {sig['First']}"
        if sig['MI']: name_line += f" {sig['MI']}"
        # Remove branch reference since it's no longer an input option
        parts.append(name_line)
        
        afsc_job = sig["AFSC/Job"]
        if afsc_job and afsc_job != "Not Available":
            parts.append(afsc_job)
            
        if sig["Squadron"]:
            parts.append(f"{sig['Squadron']} Training Squadron")
        parts.append("Keesler AFB, MS")

    final_body = "\n".join(parts)
    log.debug("Email body formatted successfully.")
    return final_body
