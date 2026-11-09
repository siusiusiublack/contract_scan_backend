from judgment_ingest.pipeline.normalize import assign_practice_areas, make_doc_id


def test_housing_keywords_tagged() -> None:
    areas = assign_practice_areas(
        "Landlord and Tenant",
        "Claim for possession under an assured shorthold tenancy and deposit.",
    )
    assert areas == ["housing"]


def test_unrelated_unclassified() -> None:
    areas = assign_practice_areas("Tax appeal", "Capital gains computation dispute.")
    assert areas == ["unclassified"]


def test_doc_id() -> None:
    assert make_doc_id("fcl", "uksc/2024/1") == "fcl:uksc/2024/1"
