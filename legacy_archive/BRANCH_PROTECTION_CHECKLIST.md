# Branch Protection Checklist

Use this checklist to configure GitHub branch protection for the default branch.

## Required checks
- [ ] Require status checks to pass before merging
- [ ] Require the `CI Quality Gate` workflow to pass
- [ ] Require the `Pre-Launch Test` workflow to pass
- [ ] Require the `Release Package` workflow on tag validation only
- [ ] Require conversation resolution before merging

## Merge safety
- [ ] Require at least 1 approving review
- [ ] Dismiss stale reviews on new commits
- [ ] Require branches to be up to date before merge
- [ ] Restrict force pushes
- [ ] Restrict branch deletion

## Repository hygiene
- [ ] Enable signed commits if supported by the team
- [ ] Require linear history if desired
- [ ] Protect environment secrets in GitHub Actions
- [ ] Review workflow permissions and keep them minimal

## Recommended status checks
- [ ] `CI Quality Gate / test-and-validate`
- [ ] `Pre-Launch Test / test-launch`
- [ ] Coverage threshold from the CI workflow

## Release process
- [ ] Only create releases from version tags like `v1.0.0`
- [ ] Verify the release archive artifact before publishing
- [ ] Attach release notes summarizing user-visible changes

## Notes
- GitHub branch protection cannot be applied from this repo alone.
- Apply these settings in the repository's GitHub Settings panel.
- Keep this checklist updated as workflow names change.
