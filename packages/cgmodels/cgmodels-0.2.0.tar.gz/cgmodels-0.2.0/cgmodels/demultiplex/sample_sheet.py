import csv
from pathlib import Path
from typing import List

from cgmodels.exceptions import SampleSheetError
from pydantic import BaseModel, Field, parse_obj_as
from typing_extensions import Literal


class Sample(BaseModel):
    flow_cell: str = Field(..., alias="FCID")
    lane: int = Field(..., alias="Lane")
    sample_id: str = Field(..., alias="SampleID")
    reference: str = Field(..., alias="SampleRef")
    index: str = Field(..., alias="index")
    sample_name: str = Field(..., alias="SampleName")
    control: str = Field(..., alias="Control")
    recipe: str = Field(..., alias="Recipe")
    operator: str = Field(..., alias="Operator")
    project: str = Field(..., alias="Project")


class NovaSeqSample(Sample):
    second_index: str = Field(..., alias="index2")


class SampleSheet(BaseModel):
    type: str
    samples: List[Sample]


def validate_unique_sample(samples: List[Sample]) -> None:
    """Validate that each sample only exists once"""
    sample_ids: set = set()
    for sample in samples:
        sample_id: str = sample.sample_id.split("_")[0]
        if sample_id in sample_ids:
            raise SampleSheetError(
                f"Sample {sample.sample_id} exists multiple times in sample sheet"
            )
        sample_ids.add(sample_id)


def get_sample_sheet(infile: Path, sheet_type: Literal["2500", "SP", "S2", "S4"]) -> SampleSheet:
    """Parse and validate a sample sheet

    return the information as a SampleSheet object
    """

    with open(infile, "r") as csv_file:
        # Skip the [data] header
        next(csv_file)
        raw_samples: List[dict] = [row for row in csv.DictReader(csv_file)]
    sample_type = Sample if sheet_type == "2500" else NovaSeqSample
    samples = parse_obj_as(List[sample_type], raw_samples)
    validate_unique_sample(samples)
    return SampleSheet(type=sheet_type, samples=samples)
