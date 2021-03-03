"""Functions for common eDOC database operations."""
import logging
from typing import List, cast

from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from tsl.edoc_database import (
    Navigation,
    Package,
    PackageElement,
    PackageElementCalculation,
    PackageElementFilter,
    ProofElement,
    ServiceClass,
)

log = logging.getLogger("tsl.edoc_database")  # pylint: disable=invalid-name


def insert_package_into_nav(
    nav_id: int,
    package_id: int,
    session: Session,
    copy_pe: bool = True,
    copy_filters: bool = False,
) -> int:
    """
    Insert a copy of the given package into the given navigation.

    Returns the id of the new package.

    If copy_pe is false, the PackageElements won"t be copied along with the
    Package. This should be used if the PackageElements will be created
    otherwise (i.e. copied from the LIDL Phasen Service).

    If copy_filters is True, all filters for each PackageElement are copied.

    Based on dbo.SP_NAV_INSERT_PACKAGE in dbo.EDOC.
    """
    log.debug("Copying package %s into nav %s", package_id, nav_id)
    assert session.query(Navigation).get(nav_id)
    pack: Package = (
        session.query(Package)
        .filter_by(NP_ID=package_id)
        .options(
            joinedload(Package.package_elements).options(
                joinedload(PackageElement.package_calculations),
                joinedload(PackageElement.proof_elements),
                joinedload(PackageElement.filters),
            ),
            joinedload(Package.service_classes),
        )
        .one()
    )

    new_pack = Package(
        N_ID=nav_id,
        NP_NAME_DE=pack.NP_NAME_DE,
        NP_NAME_EN=pack.NP_NAME_EN,
        NP_COMMENT_DE=pack.NP_COMMENT_DE,
        NP_COMMENT_EN=pack.NP_COMMENT_EN,
        CL_ID=pack.CL_ID,
        NP_CLEARDATE=pack.NP_CLEARDATE,
        NP_CLEARBY=pack.NP_CLEARBY,
        ZM_PRODUCT=pack.ZM_PRODUCT,
        PT_ID=pack.PT_ID,
        NP_TESTSAMPLES=pack.NP_TESTSAMPLES,
        NP_IS_TEMPLATE=False,
        NP_TEMPLATE_ID=pack.NP_ID,
        PN_ID=pack.PN_ID,
    )
    session.add(new_pack)
    session.flush()

    new_pack_id = new_pack.NP_ID

    for service_class in cast(List[ServiceClass], pack.service_classes):
        log.debug("Creating new service class: %s", service_class.SCL_ID)
        new_class = ServiceClass(
            NP_ID=new_pack.NP_ID, SCL_ID=service_class.SCL_ID
        )
        session.add(new_class)

    if copy_pe:
        for package_element in cast(
            List[PackageElement], pack.package_elements
        ):
            copy_package_element(
                new_pack.NP_ID, package_element, session, copy_filters
            )
    session.flush()
    return new_pack_id


def copy_package_element(
    new_pack_id: int,
    package_element: PackageElement,
    session: Session,
    copy_filters: bool = False,
) -> int:
    """
    Copy the PackageElement to the Package with the given id.

    If copy_filters is True, all filters for the PackageElement are copied.
    """
    log.debug(
        "Copying PackageElement %s to Package %s. Copying filters: %s",
        package_element.NPE_ID,
        new_pack_id,
        copy_filters,
    )
    new_element = PackageElement(
        NP_ID=new_pack_id,
        DM_ID=package_element.DM_ID,
        NL_ID=package_element.NL_ID,
        ZM_LOCATION=package_element.ZM_LOCATION,
        CT_ID=package_element.CT_ID,
        NPE_CREATE=package_element.NPE_CREATE,
        NPE_CREATE_SO=package_element.NPE_CREATE_SO,
    )
    session.add(new_element)
    session.flush()
    for calculation in cast(
        List[PackageElementCalculation], package_element.package_calculations
    ):
        new_calc = PackageElementCalculation(
            NPE_ID=new_element.NPE_ID,
            ST_ID=calculation.ST_ID,
            NPEC_DELTA_START=calculation.NPEC_DELTA_START,
            NPEC_TIME_DAYS=calculation.NPEC_TIME_DAYS,
            NPEC_TIME_HOURS=calculation.NPEC_TIME_HOURS,
            NPEC_RATE=calculation.NPEC_RATE,
            NPEC_COSTS=calculation.NPEC_COSTS,
            NPEC_TRAVEL=calculation.NPEC_TRAVEL,
            NPEC_FACTOR=calculation.NPEC_FACTOR,
            NPEC_PRICE=calculation.NPEC_PRICE,
            NPEC_COMMENT=calculation.NPEC_COMMENT,
            NPEC_TASK=calculation.NPEC_TASK,
            ZM_ID=calculation.ZM_ID,
            NPOS_ID=calculation.NPOS_ID,
        )
        session.add(new_calc)
    for proof_element in cast(
        List[ProofElement], package_element.proof_elements
    ):
        new_proof = ProofElement(
            NPE_ID=new_element.NPE_ID,
            NPEP_TYPE=proof_element.NPEP_TYPE,
            NPR_ID=proof_element.NPR_ID,
            NPEP_TEXT_DE=proof_element.NPEP_TEXT_DE,
            NPEP_TEXT_EN=proof_element.NPEP_TEXT_EN,
        )
        session.add(new_proof)
    if copy_filters:
        for filt in package_element.filters:
            log.debug("Copying filter for DMI id %s", filt.DMI_ID)
            session.add(
                PackageElementFilter(
                    NPE_ID=new_element.NPE_ID, DMI_ID=filt.DMI_ID
                )
            )
    return new_element.NPE_ID
