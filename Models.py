from typing import List, Literal, Optional
from pydantic import BaseModel, Field

# Medical Specialties Hierarchy
MEDICAL_HIERATCHY = {
    "internalMedicine": ["cardiology", "endocrinologyAndDiabetesAndMetabolism", "gastroenterology",
                         "geriatricsInternalMedicine", "hematology", "hospiceAndPalliativeInternalMedicine",
                         "infectiousDiseases", "nephrology", "medicalOncology", "pulmonology", "rheumatology"],
    "familyMedicine": [],
    "pediatrics": ["neonatologyPerinatalMedicine", "pediatricCardiology", "pediatricEmergencyMedicine"],
    "emergencyMedicine": [],
    "gynecologyAndObstetrics": ["gynecologicalOncology", "maternalFetalMedicineOrPerinatology",
                                 "obstetricsAndMaternityCare"],
    "generalSurgery": ["cardiacSurgery", "neurosurgery", "orthopedicSurgery", "plasticSurgery",
                       "thoracicSurgery", "vascularSurgery", "hepatopancreatobiliarySurgery"],
    "anesthesia": [],
    "pathology": [],
    "radiology": [],
    "psychiatry": ["addictionPsychiatry", "communityAndPublicPsychiatry"],
    "physicalMedicineAndRehabilitation": ["sportsMedicinePMR"],
    "otolaryngology": [],
    "ophthalmology": ["cataractAndAnteriorSegmentSurgery", "glaucomaOphthalmology",
                       "retinaAndVitreoretinalOphthalmology", "oculoplasticAndOrbitOphthalmology"],
    "dermatology": [],
    "dentistry": ["orthodontics"],
    "criticalCareMedicine": [],
    "clinicalPsychology": [],
    "diagnosticAndLaboratoryServices": [],
    "dietetics": []
}


def flatten_specialties_to_level(hierarchy: dict, level: int) -> List[str]:
    """Flatten the specialty hierarchy to a specific level."""
    specialties = []
    for main_specialty, sub_specialties in hierarchy.items():
        specialties.append(main_specialty)
        if level > 0 and sub_specialties:
            specialties.extend(sub_specialties)
    return sorted(specialties)


# Organization Extraction Models
class OrganizationExtractionOutput(BaseModel):
    ngos: Optional[List[str]] = Field(default_factory=list)
    facilities: Optional[List[str]] = Field(default_factory=list)
    other_organizations: Optional[List[str]] = Field(default_factory=list)


# Base Organization Models
class BaseOrganization(BaseModel):
    """Base model containing shared fields between Facility and NGO."""
    name: str = Field(..., description="Official name of the organization")
    phone_numbers: Optional[List[str]] = Field(None)
    officialPhone: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    websites: Optional[List[str]] = Field(None)
    officialWebsite: Optional[str] = Field(None)
    yearEstablished: Optional[int] = Field(None)
    acceptsVolunteers: Optional[bool] = Field(None)
    facebookLink: Optional[str] = Field(None)
    twitterLink: Optional[str] = Field(None)
    linkedinLink: Optional[str] = Field(None)
    instagramLink: Optional[str] = Field(None)
    logo: Optional[str] = Field(None)
    address_line1: Optional[str] = Field(None)
    address_line2: Optional[str] = Field(None)
    address_line3: Optional[str] = Field(None)
    address_city: Optional[str] = Field(None)
    address_stateOrRegion: Optional[str] = Field(None)
    address_zipOrPostcode: Optional[str] = Field(None)
    address_country: Optional[str] = Field(None)
    address_countryCode: Optional[str] = Field(None)


class Facility(BaseOrganization):
    """Pydantic model for facility structured output extraction."""
    facilityTypeId: Optional[Literal["hospital", "pharmacy", "doctor", "clinic", "dentist"]] = Field(None)
    operatorTypeId: Optional[Literal["public", "private"]] = Field(None)
    affiliationTypeIds: Optional[List[Literal["faith-tradition", "philanthropy-legacy", "community", "academic", "government"]]] = Field(None)
    description: Optional[str] = Field(None)
    area: Optional[int] = Field(None)
    numberDoctors: Optional[int] = Field(None)
    capacity: Optional[int] = Field(None)


class NGO(BaseOrganization):
    """Pydantic model for NGO structured output extraction."""
    countries: Optional[List[str]] = Field(None)
    missionStatement: Optional[str] = Field(None)
    missionStatementLink: Optional[str] = Field(None)
    organizationDescription: Optional[str] = Field(None)


# Medical Specialties Model
class MedicalSpecialties(BaseModel):
    specialties: Optional[List[str]] = Field(..., description="The medical specialties associated with the organization")


# Facility Facts Model
class FacilityFacts(BaseModel):
    procedure: Optional[List[str]] = Field(description="Specific clinical services performed at the facility")
    equipment: Optional[List[str]] = Field(description="Physical medical devices and infrastructure")
    capability: Optional[List[str]] = Field(description="Medical capabilities defining care delivery levels")