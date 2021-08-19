"""Test for edoc database methods."""
import logging
from datetime import datetime
from typing import Any, List, Sequence, cast

import pytest
from _pytest.monkeypatch import MonkeyPatch
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.elements import TextClause

from tsl import edoc_database_functions
from tsl.edoc_database import (
    AdminSession,
    Clearing,
    Country,
    KindOfTest,
    Navigation,
    Package,
    PackageElement,
    PackageName,
    PackageType,
    Product,
    ServiceClass,
    ServiceClassDefinition,
    get_user_id,
    session_scope,
)
from tsl.edoc_database_functions import (
    execute_stored_procedure,
    insert_package_into_nav,
)

log = logging.getLogger(  # pylint: disable=invalid-name
    "tests.test_database_functions"
)


def test_execute_stored_procedure(monkeypatch: MonkeyPatch) -> None:
    """Test that executing a stored procedure works as expected."""

    def mock_execute(_: Session, statement: TextClause) -> None:
        assert (
            statement.text == "SET NOCOUNT ON;"
            "EXEC dbo.TEST_PROCEDURE 1, 2, Test-Arg;"
            "SET NOCOUNT OFF;"
        )

    monkeypatch.setattr(Session, "execute", mock_execute)

    session = AdminSession()
    execute_stored_procedure(session, "TEST_PROCEDURE", [1, 2, "Test-Arg"])
    session.close()


def test_copy_filters_only_with_pe() -> None:
    """Test copying PackageElementFilters works only with PackageElements."""
    with pytest.raises(AssertionError):
        with session_scope(False) as session:
            insert_package_into_nav(
                1, 1, session=session, copy_pe=False, copy_filters=True
            )


def test_insert_package_into_nav_without_pe() -> None:
    """Test that inserting a Package works with the stored procedure."""
    package_id = create_test_package()
    new_nav_id = create_test_navigation()

    with session_scope(True) as session:
        new_package_id = insert_package_into_nav(
            new_nav_id, package_id, session, copy_pe=False, copy_filters=False
        )

    with session_scope(False) as session:
        old_package: Package = (
            session.query(Package)
            .options(joinedload(Package.package_elements))
            .filter_by(NP_ID=package_id)
            .one()
        )
        new_package: Package = (
            session.query(Package)
            .options(joinedload(Package.package_elements))
            .filter_by(NP_ID=new_package_id)
            .one()
        )

        assert len(old_package.package_elements) > 0
        assert len(new_package.package_elements) == 0

        _check_copied_package(new_nav_id, new_package, old_package)


def test_insert_package_into_nav_without_filter(
    monkeypatch: MonkeyPatch,
) -> None:
    """Test copying a Package works with the stored procedure."""
    generic_copy_test_with_sp(monkeypatch, False)


def test_insert_package_into_nav_with_filter(
    monkeypatch: MonkeyPatch,
) -> None:
    """Test copying a Package with filters works with the stored procedure."""
    generic_copy_test_with_sp(monkeypatch, True)


def generic_copy_test_with_sp(
    monkeypatch: MonkeyPatch, copy_filter: bool
) -> None:
    """Test that inserting a Package works with the stored procedure."""
    package_id = create_test_package()
    new_nav_id = create_test_navigation()

    def mock_sp(  # type: ignore
        _: Session, procedure: str, args: Sequence[Any]
    ) -> None:
        if copy_filter:
            assert procedure == "SP_NAV_INSERT_PACKAGE_WITH_FILTER"
        else:
            assert procedure == "SP_NAV_INSERT_PACKAGE"
        assert args[0] == new_nav_id
        assert args[1] == package_id

        with session_scope(True) as session:
            # use insert_package_into_nav to mock the procedure behaviour
            insert_package_into_nav(
                new_nav_id,
                package_id,
                session,
                copy_pe=False,
                copy_filters=False,
            )

    monkeypatch.setattr(
        edoc_database_functions, "execute_stored_procedure", mock_sp
    )
    with session_scope(True) as session:
        new_package_id = insert_package_into_nav(
            new_nav_id,
            package_id,
            session,
            copy_pe=True,
            copy_filters=copy_filter,
        )
    with session_scope(False) as session:
        old_package: Package = (
            session.query(Package).filter_by(NP_ID=package_id).one()
        )
        new_package: Package = (
            session.query(Package).filter_by(NP_ID=new_package_id).one()
        )

        _check_copied_package(new_nav_id, new_package, old_package)


def _check_copied_package(  # noqa: MC0001  # pylint: disable=too-many-branches
    new_nav_id: int, new_package: Package, old_package: Package
) -> None:
    """Check that a copied Package is correct."""
    for column in Package.__table__.columns:
        log.debug("Checking column: %s", column.name)
        try:
            old_value = old_package.__getattribute__(column.name)
            new_value = new_package.__getattribute__(column.name)
            if column.primary_key:
                # Primary key must differ
                assert old_value != new_value
            elif column.name == "N_ID":
                assert new_value == new_nav_id
            elif column.name == "NP_TEMPLATE_ID":
                assert new_value == old_package.NP_ID
            else:
                assert old_value == new_value
        except AttributeError as att_error:
            if column.name == "NP_REG":
                assert new_package.reg
                assert new_package.reg.date() == datetime.now().date()
            elif column.name == "NP_UPDATE":
                assert new_package.update is None
            elif column.name == "NP_REGBY":
                assert new_package.reg_by == get_user_id()
            elif column.name == "NP_UPDATEBY":
                assert new_package.update_by is None
            else:
                raise ValueError(
                    "Found unknown Attribute: " + column.name
                ) from att_error

    old_scl = [scl.definition.SCL_ID for scl in old_package.service_classes]
    new_scl = [scl.definition.SCL_ID for scl in new_package.service_classes]

    assert sorted(cast(List[int], old_scl)) == sorted(cast(List[int], new_scl))


def create_test_navigation() -> int:
    """Create a test Navigation."""
    with session_scope(True) as session:
        nav = Navigation(N_MASTER=False, HR_NEW_ID=1)
        nav.country = Country()
        nav.product = Product()
        nav.kind_of_test = KindOfTest()
        session.add(nav)
        session.flush()
    return cast(int, nav.N_ID)


def create_test_package() -> int:
    """Create a test Package to be copied."""
    with session_scope(True) as session:
        package = Package(
            N_ID=create_test_navigation(),
            NP_NAME_DE="Test-Package",
            NP_NAME_EN="Test-Package_EN",
            NP_COMMENT_DE="Comment DE",
            NP_COMMENT_EN="Comment EN",
            NP_CLEARDATE=datetime.now(),
            NP_CLEARBY=get_user_id(),
            ZM_PRODUCT="T10",
            NP_TESTSAMPLES=1,
            NP_IS_TEMPLATE=False,
        )
        package.clearing_state = Clearing(
            CL_NAME_DE="00 - Test", CL_NAME_EN="00 - Test"
        )
        package.package_type = PackageType()
        package.package_name = PackageName()
        service_class = ServiceClass()
        service_class.definition = ServiceClassDefinition(SCL_LEVEL=0)
        package.service_classes.append(service_class)
        session.add(package)

        for _ in range(1, 4):
            package_element = PackageElement(NPE_CREATE_SO=False)
            package.package_elements.append(package_element)
        session.flush()
    return cast(int, package.NP_ID)
