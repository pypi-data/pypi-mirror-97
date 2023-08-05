# modified by fix_any.py
# -*- mode:python; coding:utf-8 -*-
# Copyright (c) 2020 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# generated by datamodel-codegen:
#   filename:  oscal_catalog_schema.json

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import AnyUrl, EmailStr, Field, constr
from trestle.core.base_model import OscalBaseModel


class Address(OscalBaseModel):
    type: Optional[str] = Field(
        None, description='Indicates the type of address.', title='Address Type'
    )
    addr_lines: Optional[List[str]] = Field(None, alias='addr-lines', min_items=1)
    city: Optional[str] = Field(
        None,
        description='City, town or geographical region for the mailing address.',
        title='City',
    )
    state: Optional[str] = Field(
        None,
        description='State, province or analogous geographical region for mailing address',
        title='State',
    )
    postal_code: Optional[str] = Field(
        None,
        alias='postal-code',
        description='Postal or ZIP code for mailing address',
        title='Postal Code',
    )
    country: Optional[str] = Field(
        None,
        description='The ISO 3166-1 alpha-2 country code for the mailing address.',
        title='Country Code',
    )


class Type(Enum):
    person = 'person'
    organization = 'organization'


class TelephoneNumber(OscalBaseModel):
    type: Optional[str] = Field(
        None, description='Indicates the type of phone number.', title='type flag'
    )
    number: str


class RoleId(OscalBaseModel):
    __root__: str = Field(
        ..., description='A reference to the roles served by the user.'
    )


class Remarks(OscalBaseModel):
    __root__: str = Field(
        ..., description='Additional commentary on the containing object.'
    )


class Property(OscalBaseModel):
    uuid: Optional[
        constr(
            regex=r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'
        )
    ] = Field(
        None,
        description='A unique identifier that can be used to reference this property elsewhere in an OSCAL document. A UUID should be consistantly used for a given location across revisions of the document.',
        title='Property Universally Unique Identifier',
    )
    name: str = Field(
        ...,
        description="A textual label that uniquely identifies a specific attribute, characteristic, or quality of the property's containing object.",
        title='Property Name',
    )
    ns: Optional[AnyUrl] = Field(
        None,
        description="A namespace qualifying the property's name. This allows different organizations to associate distinct semantics with the same name.",
        title='Property Namespace',
    )
    class_: Optional[str] = Field(
        None,
        alias='class',
        description="A textual label that provides a sub-type or characterization of the property's name. This can be used to further distinguish or discriminate between the semantics of multiple properties of the same object with the same name and ns.",
        title='Property Class',
    )
    value: str


class PartyUuid(OscalBaseModel):
    __root__: constr(
        regex=r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'
    ) = Field(..., description='References a party defined in metadata.')


class ParameterValue(OscalBaseModel):
    __root__: str = Field(..., description='A parameter value or set of values.')


class ParameterSelection(OscalBaseModel):
    how_many: Optional[str] = Field(
        None,
        alias='how-many',
        description='Describes the number of selections that must occur.',
        title='Parameter Cardinality',
    )
    choice: Optional[List[str]] = Field(None, min_items=1)


class ParameterGuideline(OscalBaseModel):
    prose: str = Field(
        ...,
        description='Prose permits multiple paragraphs, lists, tables etc.',
        title='Guideline Text',
    )


class MemberOfOrganization(OscalBaseModel):
    __root__: constr(
        regex=r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'
    ) = Field(
        ...,
        description='Identifies that the party object is a member of the organization associated with the provided UUID.',
    )


class LocationUuid(OscalBaseModel):
    __root__: constr(
        regex=r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'
    ) = Field(..., description='References a location defined in metadata.')


class Link(OscalBaseModel):
    href: str = Field(
        ...,
        description='A resolvable URL reference to a resource.',
        title='Hypertext Reference',
    )
    rel: Optional[str] = Field(
        None,
        description="Describes the type of relationship provided by the link. This can be an indicator of the link's purpose.",
        title='Relation',
    )
    media_type: Optional[str] = Field(
        None,
        alias='media-type',
        description='Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) Media Types Registry.',
        title='Media Type',
    )
    text: Optional[str] = Field(
        None,
        description='A textual label to associate with the link, which may be used for presentation in a tool.',
        title='Link Text',
    )


class Hash(OscalBaseModel):
    algorithm: str = Field(
        ..., description='Method by which a hash is derived', title='Hash algorithm'
    )
    value: str


class ExternalId(OscalBaseModel):
    scheme: AnyUrl = Field(
        ...,
        description='Indicates the type of external identifier.',
        title='External Identifier Schema',
    )
    id: str


class EmailAddress(OscalBaseModel):
    __root__: EmailStr = Field(
        ..., description='An email address as defined by RFC 5322 Section 3.4.1.'
    )


class DocumentId(OscalBaseModel):
    scheme: AnyUrl = Field(
        ...,
        description='Qualifies the kind of document identifier.',
        title='Document Identification Scheme',
    )
    identifier: str


class Base64(OscalBaseModel):
    filename: Optional[str] = Field(
        None,
        description='Name of the file before it was encoded as Base64 to be embedded in a resource. This is the name that will be assigned to the file when the file is decoded.',
        title='File Name',
    )
    media_type: Optional[str] = Field(
        None,
        alias='media-type',
        description='Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) Media Types Registry.',
        title='Media Type',
    )
    value: str


class Annotation(OscalBaseModel):
    name: str = Field(
        ...,
        description="A textual label that uniquely identifies a specific attribute, characteristic, or quality of the annotated property's containing object.",
        title='Annotated Property Name',
    )
    uuid: Optional[
        constr(
            regex=r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'
        )
    ] = Field(
        None,
        description='A unique identifier that can be used to reference this annotated property elsewhere in an OSCAL document. A UUID should be consistantly used for a given location across revisions of the document.',
        title='Annotated Property Universally Unique Identifier',
    )
    ns: Optional[AnyUrl] = Field(
        None,
        description="A namespace qualifying the annotated property's name. This allows different organizations to associate distinct semantics with the same name.",
        title='Annotated Property Namespace',
    )
    value: str = Field(
        ...,
        description='Indicates the value of the attribute, characteristic, or quality.',
        title='Annotated Property Value',
    )
    remarks: Optional[Remarks] = None


class Test(OscalBaseModel):
    expression: str = Field(
        ...,
        description='A formal (executable) expression of a constraint',
        title='Constraint test',
    )
    remarks: Optional[Remarks] = None


class Role(OscalBaseModel):
    id: str = Field(
        ...,
        description="A unique identifier for a specific role instance. This identifier's uniqueness is document scoped and is intended to be consistent for the same role across minor revisions of the document.",
        title='Role Identifier',
    )
    title: str = Field(
        ...,
        description='A name given to the role, which may be used by a tool for display and navigation.',
        title='Role Title',
    )
    short_name: Optional[str] = Field(
        None,
        alias='short-name',
        description='A short common name, abbreviation, or acronym for the role.',
        title='Role Short Name',
    )
    description: Optional[str] = Field(
        None,
        description="A summary of the role's purpose and associated responsibilities.",
        title='Role Description',
    )
    props: Optional[List[Property]] = Field(None, min_items=1)
    annotations: Optional[List[Annotation]] = Field(None, min_items=1)
    links: Optional[List[Link]] = Field(None, min_items=1)
    remarks: Optional[Remarks] = None


class Rlink(OscalBaseModel):
    href: str = Field(
        ...,
        description='A resolvable URI reference to a resource.',
        title='Hypertext Reference',
    )
    media_type: Optional[str] = Field(
        None,
        alias='media-type',
        description='Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) Media Types Registry.',
        title='Media Type',
    )
    hashes: Optional[List[Hash]] = Field(None, min_items=1)


class Revision(OscalBaseModel):
    title: Optional[str] = Field(
        None,
        description='A name given to the document revision, which may be used by a tool for display and navigation.',
        title='Document Title',
    )
    published: Optional[datetime] = Field(
        None,
        description='The date and time the document was published. The date-time value must be formatted according to RFC 3339 with full time and time zone included.',
        title='Publication Timestamp',
    )
    last_modified: Optional[datetime] = Field(
        None,
        alias='last-modified',
        description='The date and time the document was last modified. The date-time value must be formatted according to RFC 3339 with full time and time zone included.',
        title='Last Modified Timestamp',
    )
    version: Optional[str] = Field(
        None,
        description='A string used to distinguish the current version of the document from other previous (and future) versions.',
        title='Document Version',
    )
    oscal_version: Optional[constr(regex=r'1\.0\.0[ -]*rc[ -]*1')] = Field(
        None,
        alias='oscal-version',
        description='The OSCAL model version the document was authored against.',
        title='OSCAL version',
    )
    props: Optional[List[Property]] = Field(None, min_items=1)
    annotations: Optional[List[Annotation]] = Field(None, min_items=1)
    links: Optional[List[Link]] = Field(None, min_items=1)
    remarks: Optional[Remarks] = None


class ResponsibleRole(OscalBaseModel):
    props: Optional[List[Property]] = Field(None, min_items=1)
    annotations: Optional[List[Annotation]] = Field(None, min_items=1)
    links: Optional[List[Link]] = Field(None, min_items=1)
    party_uuids: Optional[List[PartyUuid]] = Field(
        None, alias='party-uuids', min_items=1
    )
    remarks: Optional[Remarks] = None


class ResponsibleParty(OscalBaseModel):
    party_uuids: List[PartyUuid] = Field(..., alias='party-uuids', min_items=1)
    props: Optional[List[Property]] = Field(None, min_items=1)
    annotations: Optional[List[Annotation]] = Field(None, min_items=1)
    links: Optional[List[Link]] = Field(None, min_items=1)
    remarks: Optional[Remarks] = None


class Party(OscalBaseModel):
    uuid: constr(
        regex=r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'
    ) = Field(
        ...,
        description='A unique identifier that can be used to reference this defined location elsewhere in an OSCAL document. A UUID should be consistantly used for a given party across revisions of the document.',
        title='Party Universally Unique Identifier',
    )
    type: Type = Field(
        ...,
        description='A category describing the kind of party the object describes.',
        title='Party Type',
    )
    name: Optional[str] = Field(
        None,
        description='The full name of the party. This is typically the legal name associated with the party.',
        title='Party Name',
    )
    short_name: Optional[str] = Field(
        None,
        alias='short-name',
        description='A short common name, abbreviation, or acronym for the party.',
        title='Party Short Name',
    )
    external_ids: Optional[List[ExternalId]] = Field(
        None, alias='external-ids', min_items=1
    )
    props: Optional[List[Property]] = Field(None, min_items=1)
    annotations: Optional[List[Annotation]] = Field(None, min_items=1)
    links: Optional[List[Link]] = Field(None, min_items=1)
    email_addresses: Optional[List[EmailAddress]] = Field(
        None, alias='email-addresses', min_items=1
    )
    telephone_numbers: Optional[List[TelephoneNumber]] = Field(
        None, alias='telephone-numbers', min_items=1
    )
    addresses: Optional[List[Address]] = Field(None, min_items=1)
    location_uuids: Optional[List[LocationUuid]] = Field(
        None, alias='location-uuids', min_items=1
    )
    member_of_organizations: Optional[List[MemberOfOrganization]] = Field(
        None, alias='member-of-organizations', min_items=1
    )
    remarks: Optional[Remarks] = None


class Part(OscalBaseModel):
    id: Optional[str] = Field(
        None,
        description="A unique identifier for a specific part instance. This identifier's uniqueness is document scoped and is intended to be consistent for the same part across minor revisions of the document.",
        title='Part Identifier',
    )
    name: str = Field(
        ...,
        description="A textual label that uniquely identifies the part's semantic type.",
        title='Part Name',
    )
    ns: Optional[AnyUrl] = Field(
        None,
        description="A namespace qualifying the part's name. This allows different organizations to associate distinct semantics with the same name.",
        title='Part Namespace',
    )
    class_: Optional[str] = Field(
        None,
        alias='class',
        description="A textual label that provides a sub-type or characterization of the part's name. This can be used to further distinguish or discriminate between the semantics of multiple parts of the same control with the same name and ns.",
        title='Part Class',
    )
    title: Optional[str] = Field(
        None,
        description='A name given to the part, which may be used by a tool for display and navigation.',
        title='Part Title',
    )
    props: Optional[List[Property]] = Field(None, min_items=1)
    annotations: Optional[List[Annotation]] = Field(None, min_items=1)
    prose: Optional[str] = Field(
        None,
        description='Permits multiple paragraphs, lists, tables etc.',
        title='Part Text',
    )
    parts: Optional[List[Part]] = None
    links: Optional[List[Link]] = Field(None, min_items=1)


class ParameterConstraint(OscalBaseModel):
    description: Optional[str] = Field(
        None,
        description='A textual summary of the constraint to be applied.',
        title='Constraint Description',
    )
    tests: Optional[List[Test]] = Field(None, min_items=1)


class Parameter(OscalBaseModel):
    id: str = Field(
        ...,
        description="A unique identifier for a specific parameter instance. This identifier's uniqueness is document scoped and is intended to be consistent for the same parameter across minor revisions of the document.",
        title='Parameter Identifier',
    )
    class_: Optional[str] = Field(
        None,
        alias='class',
        description='A textual label that provides a characterization of the parameter.',
        title='Parameter Class',
    )
    depends_on: Optional[str] = Field(
        None,
        alias='depends-on',
        description='Another parameter invoking this one',
        title='Depends on',
    )
    props: Optional[List[Property]] = Field(None, min_items=1)
    annotations: Optional[List[Annotation]] = Field(None, min_items=1)
    links: Optional[List[Link]] = Field(None, min_items=1)
    label: Optional[str] = Field(
        None,
        description='A short, placeholder name for the parameter, which can be used as a subsitute for a value if no value is assigned.',
        title='Parameter Label',
    )
    usage: Optional[str] = Field(
        None,
        description='Describes the purpose and use of a parameter',
        title='Parameter Usage Description',
    )
    constraints: Optional[List[ParameterConstraint]] = None
    guidelines: Optional[List[ParameterGuideline]] = None
    values: Optional[List[ParameterValue]] = None
    select: Optional[ParameterSelection] = None


class Location(OscalBaseModel):
    uuid: constr(
        regex=r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'
    ) = Field(
        ...,
        description='A unique identifier that can be used to reference this defined location elsewhere in an OSCAL document. A UUID should be consistantly used for a given location across revisions of the document.',
        title='Location Universally Unique Identifier',
    )
    title: Optional[str] = Field(
        None,
        description='A name given to the location, which may be used by a tool for display and navigation.',
        title='Location Title',
    )
    address: Address = Field(
        ..., description='A postal address for the location.', title='Address'
    )
    email_addresses: Optional[List[EmailAddress]] = Field(
        None, alias='email-addresses', min_items=1
    )
    telephone_numbers: Optional[List[TelephoneNumber]] = Field(
        None, alias='telephone-numbers', min_items=1
    )
    urls: Optional[List[AnyUrl]] = Field(None, min_items=1)
    props: Optional[List[Property]] = Field(None, min_items=1)
    annotations: Optional[List[Annotation]] = Field(None, min_items=1)
    links: Optional[List[Link]] = Field(None, min_items=1)
    remarks: Optional[Remarks] = None


class Control(OscalBaseModel):
    id: str = Field(
        ...,
        description="A unique identifier for a specific control instance that can be used to reference the control in other OSCAL documents. This identifier's uniqueness is document scoped and is intended to be consistent for the same control across minor revisions of the document.",
        title='Control Identifier',
    )
    class_: Optional[str] = Field(
        None,
        alias='class',
        description='A textual label that provides a sub-type or characterization of the control.',
        title='Control Class',
    )
    title: str = Field(
        ...,
        description='A name given to the control, which may be used by a tool for display and navigation.',
        title='Control Title',
    )
    params: Optional[List[Parameter]] = Field(None, min_items=1)
    props: Optional[List[Property]] = Field(None, min_items=1)
    annotations: Optional[List[Annotation]] = Field(None, min_items=1)
    links: Optional[List[Link]] = Field(None, min_items=1)
    parts: Optional[List[Part]] = Field(None, min_items=1)
    controls: Optional[List[Control]] = None


class Citation(OscalBaseModel):
    text: str = Field(
        ..., description='A line of citation text.', title='Citation Text'
    )
    props: Optional[List[Property]] = Field(None, min_items=1)
    annotations: Optional[List[Annotation]] = Field(None, min_items=1)
    biblio: Optional[Dict[str, Any]] = Field(
        None,
        description='A container for structured bibliographic information. The model of this information is undefined by OSCAL.',
        title='Bibliographic Definition',
    )


class Resource(OscalBaseModel):
    uuid: constr(
        regex=r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'
    ) = Field(
        ...,
        description='A globally unique identifier that can be used to reference this defined resource elsewhere in an OSCAL document. A UUID should be consistantly used for a given resource across revisions of the document.',
        title='Resource Universally Unique Identifier',
    )
    title: Optional[str] = Field(
        None,
        description='A name given to the resource, which may be used by a tool for display and navigation.',
        title='Resource Title',
    )
    description: Optional[str] = Field(
        None,
        description='A short summary of the resource used to indicate the purpose of the resource.',
        title='Resource Description',
    )
    props: Optional[List[Property]] = Field(None, min_items=1)
    annotations: Optional[List[Annotation]] = Field(None, min_items=1)
    document_ids: Optional[List[DocumentId]] = Field(
        None, alias='document-ids', min_items=1
    )
    citation: Optional[Citation] = Field(
        None,
        description='A citation consisting of end note text and optional structured bibliographic data.',
        title='Citation',
    )
    rlinks: Optional[List[Rlink]] = Field(None, min_items=1)
    base64: Optional[Base64] = Field(
        None,
        description='The Base64 alphabet in RFC 2045 - aligned with XSD.',
        title='Base64',
    )
    remarks: Optional[Remarks] = None


class Metadata(OscalBaseModel):
    title: str = Field(
        ...,
        description='A name given to the document, which may be used by a tool for display and navigation.',
        title='Document Title',
    )
    published: Optional[datetime] = Field(
        None,
        description='The date and time the document was published. The date-time value must be formatted according to RFC 3339 with full time and time zone included.',
        title='Publication Timestamp',
    )
    last_modified: datetime = Field(
        ...,
        alias='last-modified',
        description='The date and time the document was last modified. The date-time value must be formatted according to RFC 3339 with full time and time zone included.',
        title='Last Modified Timestamp',
    )
    version: str = Field(
        ...,
        description='A string used to distinguish the current version of the document from other previous (and future) versions.',
        title='Document Version',
    )
    oscal_version: constr(regex=r'1\.0\.0[ -]*rc[ -]*1') = Field(
        ...,
        alias='oscal-version',
        description='The OSCAL model version the document was authored against.',
        title='OSCAL version',
    )
    revisions: Optional[List[Revision]] = Field(None, min_items=1)
    document_ids: Optional[List[DocumentId]] = Field(
        None, alias='document-ids', min_items=1
    )
    props: Optional[List[Property]] = Field(None, min_items=1)
    annotations: Optional[List[Annotation]] = Field(None, min_items=1)
    links: Optional[List[Link]] = Field(None, min_items=1)
    roles: Optional[List[Role]] = Field(None, min_items=1)
    locations: Optional[List[Location]] = Field(None, min_items=1)
    parties: Optional[List[Party]] = Field(None, min_items=1)
    responsible_parties: Optional[Dict[str, ResponsibleParty]] = Field(
        None, alias='responsible-parties'
    )
    remarks: Optional[Remarks] = None


class Group(OscalBaseModel):
    id: Optional[str] = Field(
        None,
        description="A unique identifier for a specific group instance that can be used to reference the group within this and in other OSCAL documents. This identifier's uniqueness is document scoped and is intended to be consistent for the same group across minor revisions of the document.",
        title='Group Identifier',
    )
    class_: Optional[str] = Field(
        None,
        alias='class',
        description='A textual label that provides a sub-type or characterization of the group.',
        title='Group Class',
    )
    title: str = Field(
        ...,
        description='A name given to the group, which may be used by a tool for display and navigation.',
        title='Group Title',
    )
    params: Optional[List[Parameter]] = Field(None, min_items=1)
    props: Optional[List[Property]] = Field(None, min_items=1)
    annotations: Optional[List[Annotation]] = Field(None, min_items=1)
    links: Optional[List[Link]] = Field(None, min_items=1)
    parts: Optional[List[Part]] = Field(None, min_items=1)
    groups: Optional[List[Group]] = None
    controls: Optional[List[Control]] = Field(None, min_items=1)


class BackMatter(OscalBaseModel):
    resources: Optional[List[Resource]] = Field(None, min_items=1)


class Catalog(OscalBaseModel):
    uuid: constr(
        regex=r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'
    ) = Field(
        ...,
        description='A globally unique identifier for this catalog instance. This UUID should be changed when this document is revised.',
        title='Catalog Universally Unique Identifier',
    )
    metadata: Metadata
    params: Optional[List[Parameter]] = Field(None, min_items=1)
    controls: Optional[List[Control]] = Field(None, min_items=1)
    groups: Optional[List[Group]] = Field(None, min_items=1)
    back_matter: Optional[BackMatter] = Field(None, alias='back-matter')


class Model(OscalBaseModel):
    catalog: Catalog


Part.update_forward_refs()
Control.update_forward_refs()
Group.update_forward_refs()
