"""Functions for common eDOC database operations."""
import logging
from typing import Any, Sequence, cast

from sqlalchemy import desc, text
from sqlalchemy.orm import joinedload, load_only
from sqlalchemy.orm.session import Session

from tsl.edoc_database import (
    Package,
    PackageElement,
    PackageElementCalculation,
    PackageElementFilter,
    ProofElement,
    ServiceClass,
    get_user_id,
)

log = logging.getLogger("tsl.edoc_database")  # pylint: disable=invalid-name


def _sp_insert_package_with_filter(
    nav_id: int, package_id: int, session: Session, copy_filter: bool = False
) -> int:
    """
    Copy a Package with all its PackageElements and NavPackFilters.

    Calls the internal database procedure SP_NAV_INSERT_PACKAGE/
    SP_NAV_INSERT_PACKAGE_WITH_FILTER depending on copy_filter.
    """
    if copy_filter:
        procedure = "SP_NAV_INSERT_PACKAGE_WITH_FILTER"
    else:
        procedure = "SP_NAV_INSERT_PACKAGE"
    execute_stored_procedure(
        session, procedure, (nav_id, package_id, get_user_id())
    )
    session.flush()

    # The stored procedure doesn't return the ID of the new Package hence we
    # need to get it manually (It's not nice, but should be safe because this
    # would fail only if the user manages to insert a Package in parallel and
    # faster to/as this method).
    new_package = (
        session.query(Package)
        .filter_by(
            reg_by=get_user_id(), N_ID=nav_id, NP_TEMPLATE_ID=package_id
        )
        .order_by(desc(Package.reg))
        .options(load_only(Package.NP_ID))
        .limit(1)
        .all()[0]
    )
    log.debug("NP_ID of new Package: %s", new_package.NP_ID)
    return cast(int, new_package.NP_ID)


def execute_stored_procedure(
    session: Session, procedure: str, args: Sequence[Any]
) -> None:
    """Execute a stored procedure on the database."""
    statement = f"EXEC dbo.{procedure} " + ", ".join(str(arg) for arg in args)
    log.debug("Constructed statement: %s", statement)
    session.execute(text(f"SET NOCOUNT ON;{statement};SET NOCOUNT OFF;"))


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

    If copy_pe is false, the PackageElements won't be copied along with the
    Package. This should be used if the PackageElements will be created
    otherwise (i.e. copied from the LIDL Phasen Service).

    Otherwise, we will use the database procedure dbo.SP_NAV_INSERT_PACKAGE
    when coyping without PackageElementFilters or
    dbo.SP_NAV_INSERT_PACKAGE_WITH_FILTER when also copying filters.
    """
    log.debug("Copying package %s into nav %s", package_id, nav_id)

    # cannot copy NavPackFilters when not copying PackageElements
    assert not (
        copy_pe is False and copy_filters is True
    ), "Can't copy PackageElementFilters when not copying PackageElements."

    if copy_pe:
        return _sp_insert_package_with_filter(
            nav_id, package_id, session, copy_filters
        )

    log.debug("Copying manually because copying PackageElements is off.")
    pack: Package = (
        session.query(Package)
        .filter_by(NP_ID=package_id)
        .options(
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

    for service_class in pack.service_classes:
        log.debug("Creating new service class: %s", service_class.SCL_ID)
        new_pack.service_classes.append(
            ServiceClass(SCL_ID=service_class.SCL_ID)
        )

    session.add(new_pack)
    session.flush()

    return new_pack.NP_ID


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
    for calculation in package_element.package_calculations:
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
    for proof_element in package_element.proof_elements:
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
    # new element was flushed, hence NPE_ID must available at this point
    return new_element.NPE_ID
