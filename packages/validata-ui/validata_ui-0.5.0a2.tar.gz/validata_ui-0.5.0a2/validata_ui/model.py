"""Config model using pydantic"""
from typing import List, Optional, Union

from pydantic import BaseModel, HttpUrl, root_validator


class Link(BaseModel):
    title: str
    url: HttpUrl


class ExternalLink(BaseModel):
    name: str
    type: str
    title: str
    description: str
    website: HttpUrl


class Schema(BaseModel):
    name: str
    repo_url: HttpUrl


class Catalog(BaseModel):
    version: int
    schemas: List[Schema]


class Section(BaseModel):
    name: str
    title: str
    description: Optional[str] = None
    catalog: Optional[Union[HttpUrl, Catalog]] = None
    links: Optional[List[ExternalLink]] = None

    @root_validator
    def check_catalog_or_links(cls, values):
        catalog, links = values.get("catalog"), values.get("links")
        if catalog is None and links is None:
            raise ValueError("catalog or links field must be defined")
        if catalog is not None and links is not None:
            raise ValueError("only one of catalog and links must be defined")
        return values


class Footer(BaseModel):
    links: List[Link]


class Header(BaseModel):
    links: List[Link]


class Homepage(BaseModel):
    sections: List[Section]


class Config(BaseModel):
    footer: Footer
    header: Header
    homepage: Homepage
