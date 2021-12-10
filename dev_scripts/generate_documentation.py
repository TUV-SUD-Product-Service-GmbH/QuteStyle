"""
Generate the documentation for the edoc database in Confluence.

You will need to provide valid confluence credentials as environment variables
(USER, PASSWORD) when running it.
"""

import json
import os
from typing import Any, Tuple, Type
from xml.etree import ElementTree

import requests
from sqlalchemy.orm.attributes import InstrumentedAttribute

from tsl.edoc_database import Base

BASE_URL = "https://pswiki.tuev-sued.com/rest/api/content"
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

TYPE_BASE_LINK = (
    "https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types."
)

TYPE_LINKS = {
    "INTEGER": "Integer",
    "VARCHAR": "String",
    "DATETIME": "DateTime",
    "BIT": "Boolean",
    "BIGINT": "BigInteger",
    "BOOLEAN": "Boolean",
    "NUMERIC": "Numeric",
    "BLOB": "Blob",
    "FLOAT": "Float",
    "NCHAR": "Unicode",
    "DECIMAL": "Numeric",
    "MONEY": "Numeric",
    "IMAGE": "LargeBinary",
}


def get_class_name_by_table(table_name: str) -> str:
    """Return the class name for a given table name."""
    for model in Base.__subclasses__():
        if model.__table__ == table_name:  # type: ignore
            return model.__name__
    raise ValueError("Could not find class with table " + table_name)


def generate_documentation(model: Type[Base]) -> Tuple[str, str]:
    """Return the documentation as an page_html str."""
    model_name = str(model.__name__)

    html = ElementTree.Element("page_html")
    body = ElementTree.Element("body")
    html.append(body)
    desc_head = ElementTree.Element("h2")
    desc_head.text = "Description"
    body.append(desc_head)
    if hasattr(model, "doc"):
        for doc_str in model.doc:  # type: ignore
            doc = ElementTree.Element("p")
            doc.text = doc_str
            body.append(doc)

    table_name_head = ElementTree.Element("h2")
    table_name_head.text = "Table name"
    body.append(table_name_head)
    body.append(_create_table_name_table(model))

    table_head = ElementTree.Element("h2")
    table_head.text = "Table definition"
    body.append(table_head)
    table = ElementTree.Element("table")
    body.append(table)
    row = ElementTree.Element("tr")
    for header in (
        "Column name",
        "Data type",
        "Description",
        "Index",
        "Default (Server)",
        "Default (Library)",
        "Nullable",
    ):
        head = ElementTree.Element("th")
        head.text = header
        row.append(head)
    table.append(row)

    for element in [
        a for a in dir(model) if not a.startswith("_") and not a == "metadata"
    ]:
        method = getattr(model, element)
        if not hasattr(method, "comparator"):
            continue
        if not hasattr(method.comparator, "type"):
            continue
        row = _create_table_row(method)

        table.append(row)

    return model_name, ElementTree.tostring(
        html, encoding="unicode", method="html"
    )


def _create_table_name_table(model: Type[Base]) -> ElementTree.Element:
    """Create the table for the table name."""
    table_name_table = ElementTree.Element("table")
    row = ElementTree.Element("tr")
    head = ElementTree.Element("th")
    head.text = "Table name"
    row.append(head)
    table_name_table.append(row)
    row = ElementTree.Element("tr")
    name = ElementTree.Element("td")
    name.text = model.__table__.name  # type: ignore
    row.append(name)
    table_name_table.append(row)
    return table_name_table


def _create_table_row(att: InstrumentedAttribute) -> ElementTree.Element:
    """Create the row for a given Attribute."""
    row = ElementTree.Element("tr")
    row.append(_create_name_element(att))
    row.append(_create_type_element(att))
    row.append(_create_desc_element(att))
    row.append(_create_idx_element(att))
    row.append(_create_server_default_element(att))
    row.append(_create_lib_default_element(att))
    row.append(_create_nullable_element(att))
    return row


def _create_nullable_element(
    att: InstrumentedAttribute,
) -> ElementTree.Element:
    """Create the table element for nullability."""
    td_null = ElementTree.Element("td")
    td_null.text = str(att.nullable)
    return td_null


def _create_server_default_element(
    att: InstrumentedAttribute,
) -> ElementTree.Element:
    """Create the table element for the server's default value."""
    td_s_default = ElementTree.Element("td")
    if att.server_default:
        text = att.server_default.arg.text
        while text.startswith("(") and text.endswith(")"):
            text = text[1:-1]
        td_s_default.text = text
    return td_s_default


def _create_lib_default_element(
    att: InstrumentedAttribute,
) -> ElementTree.Element:
    """Create the table element for the default value."""
    td_s_default = ElementTree.Element("td")
    if att.default:
        if att.default.is_callable:
            td_s_default.text = "INTERNAL CALLABLE"
        else:
            if att.comparator.default.arg == "":
                td_s_default.text = '""'
            elif isinstance(att.comparator.default.arg, (int, float)):
                td_s_default.text = str(att.comparator.default.arg)
            else:
                td_s_default.text = att.comparator.default.arg.text
    if att.onupdate:
        if att.onupdate.is_callable:
            ou_text = "On Update: INTERNAL CALLABLE"
        else:
            ou_text = f"On Update: {att.comparator.onupdate.arg.text}"
        if td_s_default.text:
            td_s_default.text = ", ".join((td_s_default.text, ou_text))
        else:
            td_s_default.text = ou_text
    return td_s_default


def _create_idx_element(att: InstrumentedAttribute) -> ElementTree.Element:
    """Create the table element for the index."""
    td_idx = ElementTree.Element("td", {"style": "text-align: center;"})
    if att.comparator.index:
        td_idx.text = "x"
    return td_idx


def _create_desc_element(att: InstrumentedAttribute) -> ElementTree.Element:
    """Create the table element for the description."""
    td_desc = ElementTree.Element("td")
    if att.comparator.foreign_keys:
        name = get_foreign_model_name(att)
        foreign_element = ElementTree.Element("p")
        foreign_element.text = "This key is a reference to "
        link_element = ElementTree.Element("a")
        link = "https://pswiki.tuev-sued.com/display/TSL/" + name
        link_element.set("href", link)
        link_element.text = name + "."
        foreign_element.append(link_element)
        td_desc.append(foreign_element)
        desc_element = ElementTree.Element("p")
        td_desc.append(desc_element)
    elif att.comparator.primary_key:
        desc_element = ElementTree.Element("p")
        desc_element.text = "The primary key of the table."
        td_desc.append(desc_element)
    elif att.key == "reg":
        desc_element = ElementTree.Element("p")
        desc_element.text = "Date and time the element was created."
        td_desc.append(desc_element)
    elif att.key == "reg_by":
        desc_element = ElementTree.Element("p")
        desc_element.text = "User that created the element."
        td_desc.append(desc_element)
    elif att.key == "update":
        desc_element = ElementTree.Element("p")
        desc_element.text = "Date and time the element was last updated."
        td_desc.append(desc_element)
    elif att.key == "update_by":
        desc_element = ElementTree.Element("p")
        desc_element.text = "User that updated the element last."
        td_desc.append(desc_element)
    elif att.prop.deferred:
        desc_element = ElementTree.Element("p")
        desc_element.text = "This column is loaded deferred."
        td_desc.append(desc_element)
    if att.doc:
        desc_element = ElementTree.Element("p")
        td_desc.append(desc_element)
        if att.doc.startswith("UNKNOWN") or att.doc.startswith("WARNING"):
            desc_element.set("style", "color: rgb(255,0,0);")
        desc_element.text = att.doc
    return td_desc


def _create_type_element(att: InstrumentedAttribute) -> ElementTree.Element:
    """Create the table element for the type."""
    td_type = ElementTree.Element("td")
    try:
        type_str = str(att.comparator.type)
        type_key = type_str.split("(", maxsplit=1)[0]
        link = TYPE_BASE_LINK + TYPE_LINKS[type_key]
        element = ElementTree.Element("a", {"href": link})
        element.text = type_str
        td_type.append(element)
    except AttributeError:
        pass
    return td_type


def _create_name_element(att: InstrumentedAttribute) -> ElementTree.Element:
    """Create the table element for the name."""
    td_name = ElementTree.Element("td")
    if att.key != att.expression.key:
        att_name = f"{att.key} ({att.expression.key})"
    else:
        att_name = att.key
    if att.comparator.primary_key:
        strong = ElementTree.Element("strong")
        strong.text = att_name
        td_name.append(strong)
    else:
        if att.doc and att.doc.startswith("DEPRECATED"):
            name = ElementTree.Element("s")
            td_name.append(name)
        else:
            name = td_name
        if att.comparator.foreign_keys:
            parent_name = get_foreign_model_name(att)
            link = ElementTree.Element(
                "a",
                {
                    "href": "https://pswiki.tuev-sued.com/display/TSL/"
                    + parent_name
                },
            )
            link.text = att_name
            name.append(link)
        else:
            name.text = att_name
    return td_name


def get_foreign_model_name(att: InstrumentedAttribute) -> str:
    """Get the model name for a ForeignKey."""
    keys = list(att.comparator.foreign_keys)
    table_name = keys[0].column.table
    parent_name = get_class_name_by_table(table_name)
    return parent_name


def get_page_ancestors(auth: Tuple[str, str], pageid: str) -> Any:
    """Get basic page information plus the ancestors property."""
    url = f"{BASE_URL}/{pageid}?expand=ancestors"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()["ancestors"]


def get_page_info(auth: Tuple[str, str], pageid: str) -> Any:
    """Get the page info for a specific page."""
    response = requests.get(f"{BASE_URL}/{pageid}", auth=auth)
    response.raise_for_status()
    return response.json()


def write_data(auth: Tuple[str, str], html: str, pageid: str) -> None:
    """Write the given page_html data to the page with the given id."""
    info = get_page_info(auth, pageid)

    ver = int(info["version"]["number"]) + 1

    ancestors = get_page_ancestors(auth, pageid)

    anc = ancestors[-1]
    del anc["_links"]
    del anc["_expandable"]
    del anc["extensions"]

    data = {
        "id": str(pageid),
        "type": "page",
        "title": info["title"],
        "version": {"number": ver},
        "ancestors": [anc],
        "body": {
            "storage": {
                "representation": "storage",
                "value": str(html),
            }
        },
    }

    response = requests.put(
        f"{BASE_URL}/{pageid}",
        data=json.dumps(data),
        auth=auth,
        headers={"Content-Type": "application/json"},
    )

    response.raise_for_status()


def get_page_id(title: str, auth: Tuple[str, str]) -> str:
    """Return the page id by title."""
    response = requests.get(
        f"{BASE_URL}?title={title}&spaceKey=TSL",
        auth=auth,
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()

    return str(response.json()["results"][0]["id"])


def create_page(title: str, data: str, auth: Tuple[str, str]) -> str:
    """Create the page with the given title and data."""
    parent_id = get_page_id("Datenbank-Definition (EDOC)", auth)
    assert parent_id
    request_data = {
        "type": "page",
        "title": title,
        "ancestors": [{"id": parent_id}],
        "space": {"key": "TSL"},
        "body": {
            "storage": {
                "value": data,
                "representation": "storage",
            }
        },
    }
    response = requests.post(
        BASE_URL,
        data=json.dumps(request_data),
        auth=auth,
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()

    return str(response.json()["id"])


if __name__ == "__main__":
    for doc_class in Base.__subclasses__():
        if not doc_class.__name__ == "DefaultModuleItem":
            continue
        print("Creating documentation for " + doc_class.__name__)
        page_title, page_html = generate_documentation(doc_class)

        assert USER
        assert PASSWORD

        try:
            write_data(
                (USER, PASSWORD),
                page_html,
                get_page_id(page_title, (USER, PASSWORD)),
            )
        except IndexError:
            create_page(page_title, page_html, (USER, PASSWORD))
