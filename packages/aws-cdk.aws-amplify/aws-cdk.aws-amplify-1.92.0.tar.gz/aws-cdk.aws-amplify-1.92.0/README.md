# AWS Amplify Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

The AWS Amplify Console provides a Git-based workflow for deploying and hosting fullstack serverless web applications. A fullstack serverless app consists of a backend built with cloud resources such as GraphQL or REST APIs, file and data storage, and a frontend built with single page application frameworks such as React, Angular, Vue, or Gatsby.

## Setting up an app with branches, custom rules and a domain

To set up an Amplify Console app, define an `App`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_amplify as amplify
import aws_cdk.core as cdk

amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=cdk.SecretValue.secrets_manager("my-github-token")
    ),
    build_spec=codebuild.BuildSpec.from_object({# Alternatively add a `amplify.yml` to the repo
        "version": "1.0",
        "frontend": {
            "phases": {
                "pre_build": {
                    "commands": ["yarn"
                    ]
                },
                "build": {
                    "commands": ["yarn build"
                    ]
                }
            },
            "artifacts": {
                "base_directory": "public",
                "files": "**/*"
            }
        }})
)
```

To connect your `App` to GitLab, use the `GitLabSourceCodeProvider`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitLabSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=cdk.SecretValue.secrets_manager("my-gitlab-token")
    )
)
```

To connect your `App` to CodeCommit, use the `CodeCommitSourceCodeProvider`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
repository = codecommit.Repository(self, "Repo",
    repository_name="my-repo"
)

amplify_app = amplify.App(self, "App",
    source_code_provider=amplify.CodeCommitSourceCodeProvider(repository=repository)
)
```

The IAM role associated with the `App` will automatically be granted the permission
to pull the CodeCommit repository.

Add branches:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
master = amplify_app.add_branch("master")# `id` will be used as repo branch name
dev = amplify_app.add_branch("dev")
dev.add_environment("STAGE", "dev")
```

Auto build and pull request preview are enabled by default.

Add custom rules for redirection:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
amplify_app.add_custom_rule(
    source="/docs/specific-filename.html",
    target="/documents/different-filename.html",
    status=amplify.RedirectStatus.TEMPORARY_REDIRECT
)
```

When working with a single page application (SPA), use the
`CustomRule.SINGLE_PAGE_APPLICATION_REDIRECT` to set up a 200
rewrite for all files to `index.html` except for the following
file extensions: css, gif, ico, jpg, js, png, txt, svg, woff,
ttf, map, json, webmanifest.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_single_page_app.add_custom_rule(amplify.CustomRule.SINGLE_PAGE_APPLICATION_REDIRECT)
```

Add a domain and map sub domains to branches:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain = amplify_app.add_domain("example.com")
domain.map_root(master)# map master branch to domain root
domain.map_sub_domain(master, "www")
domain.map_sub_domain(dev)
```

## Restricting access

Password protect the app with basic auth by specifying the `basicAuth` prop.

Use `BasicAuth.fromCredentials` when referencing an existing secret:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
amplify_app = amplify.App(self, "MyApp",
    repository="https://github.com/<user>/<repo>",
    oauth_token=cdk.SecretValue.secrets_manager("my-github-token"),
    basic_auth=amplify.BasicAuth.from_credentials("username", cdk.SecretValue.secrets_manager("my-github-token"))
)
```

Use `BasicAuth.fromGeneratedPassword` to generate a password in Secrets Manager:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
amplify_app = amplify.App(self, "MyApp",
    repository="https://github.com/<user>/<repo>",
    oauth_token=cdk.SecretValue.secrets_manager("my-github-token"),
    basic_auth=amplify.BasicAuth.from_generated_password("username")
)
```

Basic auth can be added to specific branches:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app.add_branch("feature/next",
    basic_auth=amplify.BasicAuth.from_generated_password("username")
)
```

## Automatically creating and deleting branches

Use the `autoBranchCreation` and `autoBranchDeletion` props to control creation/deletion
of branches:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
amplify_app = amplify.App(self, "MyApp",
    repository="https://github.com/<user>/<repo>",
    oauth_token=cdk.SecretValue.secrets_manager("my-github-token"),
    auto_branch_creation={# Automatically connect branches that match a pattern set
        "patterns": ["feature/*", "test/*"]},
    auto_branch_deletion=True
)
```
