# pre-commit hook

## Replace reference of included gitlab-ci files

`check_included_ci_ref.py`

Replaces the reference/branch of remotely included `.gitlab-ci.yml` files directly within the file (overwrites the file).


We use base or common gitlab stages, that are included into the project's `.gitlab-ci.yml` file like this:
```
include:
  - project: 'general/common-gitlab-stages'
    ref: master
    file: '/.gitlab-ci-deploy_image.yml'
```

`ref` defines the branch of the remote repository to get the `.gitlab-ci` file from.

In the project - where common gitlab stages are included - committing on the `develop` branch does not required any specific `ref`.

However,
* committing on the `staging` branch requires the `staging` or `master` refs.
* committing on the `master` branch requires the `master` ref.

So, for `staging` and `master` we want to include from the appropriate references/branches only.

Goal:
  * Rewrite included `.gitlab-ci.yml` references.

How to:
  * Get help
    - `check_included_ci_ref.py -h`
    - `python check_included_ci_ref.py <file1> <another_file> <path_to_file>`
  * Files can be given as arguments to the script.

Optimizations:
  * Only simple words are considered in ref/branch name, using `\w+`
