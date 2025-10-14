# Competition Submissions

Your notebook submission and corresponding Markdown form will live **here** in this directory.

## Submission form

To acknowledge you agree to the rules and requirements of this competition, you must submit a Markdown form alongside your notebook.

You can find a template of the form in the root of the repository named `SUBMISSION_FORM_TEMPLATE.md` [here](../SUBMISSION_FORM_TEMPLATE.md). Copy this form, name it `submission.md` and fill out both the `yaml` metadata and the `Markdown` sections.

You can find the `JSON Schema` that your forms `yaml` metadata will be evaluated against [here](../.github/workflows/submission-md-schema.json). An annotated example of the metadata is also below:

```yaml
# ALL FIELDS ARE REQUIRED
---
contact_name: "My Name" 
email_address: "me@my-email.com"
notebook_authors: [ # Must contain at least one entry
    "Author 1",
    "Author 2"
]
notebook_title: "Doing cool things with EOPF data"
docker_image_used: "R" # One of "R", "Python", or "Julia"
makes_use_of_eopf_zarr_sample_service_data: true # Must be true
incorporates_one_or_more_eopf_plugins: true # Either true or false
data_sources_used: ["Sentinel-1", "Sentinel-3"] # Must contain at least one of "Sentinel-1", "Sentinel-2", or "Sentinel-3"
all_declarations_affirmed: true # Must be true
---
```

The `Markdown` sections are freeform - Please do **not** modify the headings.

## Organising your submission

Create a directory in `submissions/` named after the title of your notebook; it should be all lowercase and using `_` in place of spaces. Then place your notebook (named `submission.ipynb`), and form (named `submission.md`) inside.

For example, if your notebook was titled: `Exploring Sentinel 2 for use in Agriculture`, you would create a directory: `exploring_sentinel_2_for_use_in_agriculture`.

The full path of your submission would be:

```bash
# From the root of the repository
submissions/exploring_sentinel_2_for_use_in_agriculture/submission.ipynb
submissions/exploring_sentinel_2_for_use_in_agriculture/submission.md
```

## Submitting to the competition

If you are familiar with using `git` and `GitHub`, create a branch, commit your submission files created following the above instructions, and then raise a `Pull Request` against this repository.

If you are new to `git` and `GitHub`, please refer to the following guides on how to contribute to this repository:

- Cloning a repository, creating a branch, creating a commit, and pushing that branch: https://docs.github.com/en/get-started/using-git/about-git#example-contribute-to-an-existing-repository
- Creating a Pull Request once you have a branch with your changes: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request#creating-the-pull-request

Please set the `Title` of your Pull Request to the title of your notebook.
