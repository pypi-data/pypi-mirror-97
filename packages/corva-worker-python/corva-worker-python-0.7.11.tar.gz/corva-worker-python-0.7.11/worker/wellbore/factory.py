from typing import Union, List

from worker.data.operations import get_data_by_path, get_config_by_id, compare_float

from worker import API
from worker.exceptions import MissingConfigError

from worker.wellbore.model.drillstring import Drillstring
from worker.wellbore.model.enums import HoleType
from worker.wellbore.model.hole import Hole
from worker.wellbore.model.hole_section import HoleSection
from worker.wellbore.model.riser import Riser
from worker.wellbore.wellbore import Wellbore

MIN_LENGTH = 1  # ft


def run_drillstring_and_create_wellbore(wits: dict, mud_flow_in: float = None) -> Union[Wellbore, None]:
    """
    Get the wits record and create a wellbore
    :param wits: wits records in json format
    :param mud_flow_in: used to determine if under-reamer needs to be activated for hole enlargement
    :return: a wellbore
    """
    if wits is None:
        return None

    api_worker = API()

    drillstring_id = get_data_by_path(wits, "metadata.drillstring", str, default=None)

    if not drillstring_id:
        return None

    drillstring = get_config_by_id(drillstring_id, collection="data.drillstring")

    if not drillstring:
        return None

    active_drillstring_number = drillstring.get("data", {}).get("id")

    # setting active drillstring
    drillstring = Drillstring(drillstring)

    bit = drillstring.get_bit()
    if not bit:
        raise MissingConfigError(f"Bit was not found in the drillstring with _id='{drillstring_id}'")

    asset_id = wits['asset_id']
    bit_size = bit.size

    bit_depth = get_data_by_path(wits, "data.bit_depth", float)
    hole_depth = get_data_by_path(wits, "data.hole_depth", float)

    # setting cased-hole sections
    query = "{data.inner_diameter#gte#%s}" % bit_size
    casings = api_worker.get(path="/v1/data/corva", collection="data.casing", asset_id=asset_id, query=query, limit=100).data
    hole = set_casings(casings)
    smallest_cased_hole_diameter = hole.get_min_inner_diameter() or 100

    # ====== setting open-hole sections
    query = "{data.id#lte#%s}" % active_drillstring_number
    sort = "{data.id:1}"
    drillstrings = api_worker.get(path="/v1/data/corva", collection="data.drillstring", asset_id=asset_id, query=query, sort=sort, limit=100).data
    hole = add_open_holes(hole, drillstrings, smallest_cased_hole_diameter, hole_depth)

    mud_flow_in = get_mud_flow_in(mud_flow_in, wits)

    return Wellbore(
        drillstring=drillstring,
        hole=hole,
        bit_depth=bit_depth,
        hole_depth=hole_depth,
        mud_flow_in=mud_flow_in,
    )


def run_casingstring_and_create_wellbore(wits: dict, mud_flow_in: float = None) -> Union[Wellbore, None]:
    """
    Get the wits record and create a wellbore
    :param wits: wits records in json format
    :param mud_flow_in: used to determine if under-reamer needs to be activated for hole enlargement
    :return: a wellbore
    """
    if wits is None:
        return None

    api_worker = API()

    casingstring_id = get_data_by_path(wits, "metadata.casing", str, default=None)

    if not casingstring_id:
        return None

    casingstring = get_config_by_id(casingstring_id, collection="data.casing")

    if not casingstring:
        return None

    casing_outer_diameter = casingstring.get("data", {}).get("outer_diameter")
    casing_inner_diameter = casingstring.get("data", {}).get("inner_diameter")

    # setting active drillstring
    casingstring = Drillstring(casingstring)

    asset_id = wits['asset_id']

    bit_depth = get_data_by_path(wits, "data.bit_depth", float)
    hole_depth = get_data_by_path(wits, "data.hole_depth", float)

    # setting cased-hole sections
    query = "{data.inner_diameter#gt#%s}" % casing_inner_diameter
    sort = "{data.inner_diameter:-1}"
    casings = api_worker.get(path="/v1/data/corva", collection="data.casing", asset_id=asset_id, query=query, sort=sort, limit=100).data

    # ====== setting open-hole sections
    sort = "{timestamp: -1}"
    drillstrings = api_worker.get(path="/v1/data/corva", collection="data.drillstring", asset_id=asset_id, sort=sort, limit=100).data

    drillstrings = [
        next((string for string in drillstrings if (string.get("data", {}).get("components", [{}])[-1].get("size") or -1) > casing_outer_diameter), {})
    ]

    hole = set_casings(casings)
    smallest_cased_hole_diameter = hole.get_min_inner_diameter() or 100

    hole = add_open_holes(hole, drillstrings, smallest_cased_hole_diameter, hole_depth)

    mud_flow_in = get_mud_flow_in(mud_flow_in, wits)

    return Wellbore(
        drillstring=casingstring,
        hole=hole,
        bit_depth=bit_depth,
        hole_depth=hole_depth,
        mud_flow_in=mud_flow_in,
    )


def get_detailed_hole_from_elements(elements: List[dict],
                                    previous_element_top_depth: float,
                                    possible_top_depth: float,
                                    extend_casing_to_top: bool,
                                    is_riser: bool
                                    ) -> Hole:
    """
    This function converts elements of casing/riser components into a Hole.
    :param elements: list casing/riser components
    :param previous_element_top_depth: will be used as the bottom depth of current component
    :param possible_top_depth:  possible top depth to which a casing/riser can extend. In case of a casing, it will extend to the btm of riser (if available)
    :param extend_casing_to_top: if the casing/riser should extend to the top
    :param is_riser: If its a riser or a cased hole
    :return: Hole with all the components as HoleSections
    """
    casing_hole: Hole = Hole()

    elements = [element for index, element in enumerate(elements) if check_casing_element_validity(element, index, extend_casing_to_top)]

    for element in reversed(elements):
        element_id = element.get("inner_diameter", 0.0)
        element_length = element.get("length", 0.0)
        element_bottom = previous_element_top_depth
        element_top = element_bottom - element_length

        if element_top < possible_top_depth:
            create_section_and_append(casing_hole, element_id, possible_top_depth, element_bottom, HoleType.CASED_HOLE, is_riser)
            break

        create_section_and_append(casing_hole, element_id, element_top, element_bottom, HoleType.CASED_HOLE, is_riser)
        previous_element_top_depth = element_top

    casing_hole.sections.reverse()

    # checking and making sure the top element extends to the possible top depth.
    # This check is needed because we are ignoring components of dp family which maybe at the top of the liner.
    if compare_float(casing_hole.sections[0].top_depth, possible_top_depth, tolerance=0.01) != 0:
        casing_hole.sections[0].set_top_depth(possible_top_depth)
        casing_hole.sections[0].set_length()

    return casing_hole


def create_section_and_append(casing_hole, inner_diameter, top_depth, bottom_depth, hole_type, is_riser):
    sec = HoleSection(inner_diameter=inner_diameter, top_depth=top_depth, bottom_depth=bottom_depth, hole_type=hole_type)
    if is_riser:
        sec = Riser(inner_diameter=inner_diameter, top_depth=top_depth, bottom_depth=bottom_depth, hole_type=hole_type)

    casing_hole.sections.append(sec)


def check_casing_element_validity(casing_element: dict, idx: int, extend_casing_to_top: bool) -> bool:
    """
    Check if the component is a casing and of a significant length
    :param casing_element:
    :param idx:
    :param extend_casing_to_top:
    :return:
    """
    element_length: float = casing_element.get("length")
    element_family: str = casing_element.get("family")

    if not element_family or not isinstance(element_family, str):
        return False

    ignored_families = (
        "dp",
        "hwdp"
    )

    # A dp component in casing is considered invalid. It is ignored when setting casing
    if element_family.lower() in ignored_families:
        return False

    # Ignoring casing components with length less than 20 feet and only components that are not top most or those that don't extend to top depth.
    if element_length < 20.0 and (idx != 0 or not extend_casing_to_top):
        return False

    return True


def set_casings(casings: List[dict]) -> Hole:
    """
    Set the casing by providing the list of the jsons
    :param casings: list of casings from API in json dict format
    :return: None
    """
    if not casings:
        return Hole()

    possible_casing_top_depth: float = 0.0
    riser = next((csg for csg in casings if csg.get('data', {}).get('is_riser', False)), {})

    if riser:
        possible_casing_top_depth = riser.get("data").get("bottom_depth")
        casings.remove(riser)

    # sorting the casings in the ascending order (the smaller the inner_diameter the earlier it is added)
    casings = sorted(casings, key=lambda csg: csg.get('data', {}).get('inner_diameter'))

    # finding if a liner is overlapping outer liners
    # this is common in offshore drilling where they set the casings at the sea floor
    index = 1
    while index < len(casings):
        top_depth_inner = casings[index - 1].get('data', {}).get('top_depth', 1000)
        top_depth_outer = casings[index].get('data', {}).get('top_depth', 1000)
        if top_depth_outer + Wellbore.DEPTH_THRESHOLD > top_depth_inner:
            casings.pop(index)
        else:
            index += 1

    # reversing the order (the larger the inner_diameter the earlier it is)
    casings = reversed(casings)

    casing_holes = []
    for index, casing in enumerate(casings):
        casing_hole = Hole()
        casing_object: dict = casing.get("data", {})
        casing_bottom = casing_object.get("bottom_depth")
        casing_top = possible_casing_top_depth
        current_casing_top_depth = casing_object.get("top_depth")

        # The top depth of the first component should reach to surface regardless
        # Case 1 - Land (Normal)
        # Case 2 - Riser
        # Case 3 - Riserless
        if not (index == 0 and current_casing_top_depth < Wellbore.DEPTH_THRESHOLD):
            casing_top = current_casing_top_depth

        casing_elements: List[dict] = casing_object.get("components", [])
        if not casing_elements:
            hole_section = HoleSection(**casing_object, hole_type=HoleType.CASED_HOLE)
            casing_hole.sections.append(hole_section)
        else:
            previous_casing_element_top_depth = casing_bottom
            # Individual casing elements have to be looped in reverse order to correctly account for the topmost element going to surface is not liner
            extend_casing_to_top: bool = False
            if index == 0:
                extend_casing_to_top = True
            casing_hole = get_detailed_hole_from_elements(casing_elements, previous_casing_element_top_depth, casing_top, extend_casing_to_top, False)

        casing_holes.append(casing_hole)

    # Now adding the components of the riser to casingHoles
    if riser:
        riser_elements: List[dict] = riser.get("data", {}).get("components", [])
        previous_riser_element_top_depth = possible_casing_top_depth
        riser_hole: Hole = get_detailed_hole_from_elements(riser_elements, previous_riser_element_top_depth, 0.0, True, True)
        casing_holes.insert(0, riser_hole)

    return Hole.merge_holes(casing_holes)


def add_open_holes(hole: Hole, drillstrings: List[dict], smallest_cased_hole_diameter: float, hole_depth: float) -> Hole:
    for ds in drillstrings:
        bit = Drillstring(ds).get_bit()
        if not bit:
            drillstring_id = ds.get("_id")
            raise MissingConfigError(f"Bit was not found in the drillstring with _id='{drillstring_id}'")

        bit_size = bit.size
        # only keeping the DSs that ran below the smallest casing
        if bit_size > smallest_cased_hole_diameter:
            continue

        start_depth = ds.get("data", {}).get("start_depth")

        # if due to the side track the hole depth reduced, then it should update the setting depths in the open hole
        hole.sections = [
            sec for sec in hole.sections
            if sec.hole_type != HoleType.OPEN_HOLE or sec.top_depth <= hole_depth
        ]

        # if a new open-hole section is created in addition to the previous one,
        # the previous bottom depth may need to be modified.
        previous_hole_section = hole.get_last_hole_section()

        top_depth = hole.get_bottom_depth()
        bottom_depth = top_depth + 0.0001
        current_hole_section = HoleSection(
            top_depth=top_depth,
            bottom_depth=bottom_depth,
            inner_diameter=bit_size,
            hole_type=HoleType.OPEN_HOLE
        )

        if previous_hole_section:
            # The casing bottom depth can't be modified if the difference is more than 300 ft
            cased_hole_condition = previous_hole_section.hole_type == HoleType.CASED_HOLE and start_depth - previous_hole_section.bottom_depth < 300
            if cased_hole_condition or previous_hole_section.hole_type == HoleType.OPEN_HOLE:
                previous_hole_section.set_bottom_depth(start_depth)
                previous_hole_section.set_length()

            if current_hole_section.eq_without_length(previous_hole_section):
                continue

        current_hole_section.set_length()
        hole.add_section(current_hole_section)

    # In some cases the DS setting depth doesn't match the hole depth so the wits data overrides it;
    # this is only applied to the top depth of the last section and bottom depth of the previous section.
    # Note: only in cases that the wits hole_depth < setting depth
    # Condition: the number of open hole sections should be at least two needs to be satisfied first
    if len(hole) - len(hole.get_cased_hole()) > 1 and 1 < hole_depth < hole[-1].top_depth:
        hole[-2].set_bottom_depth(hole_depth)
        hole[-2].set_length()

        hole[-1].set_top_depth(hole_depth)
        hole[-1].set_length()

    return hole


def get_mud_flow_in(mud_flow_in: [float, None], wits: dict) -> [float, None]:
    """
    Get the mud flow rate from wits if `mud_flow_in` is None
    :param mud_flow_in:
    :param wits:
    :return:
    """
    if mud_flow_in is not None:
        return mud_flow_in

    if not wits:
        return None

    return get_data_by_path(wits, "data.mud_flow_in", default=None)
