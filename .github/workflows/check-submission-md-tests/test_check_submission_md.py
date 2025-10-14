from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from check_submission_md import check_submission_md


def test_that_good_submission_exits_with_0():
    test_dir = Path(__file__).parent
    good_md_path = test_dir / "submissions" / "good.md"
    code, message = check_submission_md(good_md_path)
    assert code == 0
    assert message == "`submission.md` validation passed"


def test_that_bad_submission_exits_with_1():
    test_dir = Path(__file__).parent
    bad_md_path = test_dir / "submissions" / "bad.md"
    code, message = check_submission_md(bad_md_path)
    assert code == 1
    expected = (
        "`submission.md` validation failed with the following issues:\n"
        "- `<root>`: 'data_sources_used' is a required property\n"
        "- `all_declarations_affirmed`: True was expected\n"
        "- `contact_name`: '' should be non-empty\n"
        "- `docker_image_used`: 'MY_OWN' is not one of ['Julia', 'Python', 'R']\n"
        "- `email_address`: 'me/my-email.com' is not a 'email'\n"
        "- `makes_use_of_eopf_zarr_sample_service_data`: True was expected\n"
        "- `notebook_authors`: [] should be non-empty\n"
        "- `notebook_title`: '' should be non-empty\n"
    )
    assert message == expected
