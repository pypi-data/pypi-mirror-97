import contextlib
import datetime
import glob
import hashlib
import io
import os
import shutil
import stat
import sys
import tempfile
import zipfile
from pathlib import Path

import boto3
import botocore
import botocore.exceptions
import click
import yaml
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, TaggedScalar, Tag

# Create a config
session_config = botocore.config.Config(user_agent="cfn-mod/cli")


@click.group()
def cli():
    pass


@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


def add_file(zip_file, path, in_zip_path):
    click.echo(f"Adding path = {path}")
    permission = 0o555 if os.access(path, os.X_OK) else 0o444
    zip_info = zipfile.ZipInfo.from_file(in_zip_path)
    zip_info.date_time = (2020, 1, 1, 0, 0, 0)
    zip_info.external_attr = (stat.S_IFREG | permission) << 16
    with open(path, "rb") as fp:
        zip_file.writestr(zip_info, fp.read())


def generate_versioned_conf(folder, path, version):
    path = Path(folder) / path
    with open(path, "r") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    conf["module"]["version"] = version
    f = tempfile.NamedTemporaryFile(mode="w", delete=False)
    yaml.dump(conf, f)
    return f.name


def create_zip(files, version=None):
    zip_bytes = io.BytesIO()
    with zipfile.ZipFile(zip_bytes, "w") as zip_file:
        for folder, files in files:
            with pushd(folder):
                for path in files:
                    if version is not None and folder == "." and path == "module.yml":
                        new_module_path = generate_versioned_conf(folder, path, version)
                        add_file(zip_file, new_module_path, path)
                        os.unlink(new_module_path)
                    elif os.path.isfile(path):
                        add_file(zip_file, path, path)
        zip_bytes.seek(0)
        return zip_bytes


def calc_md5(md5_files):
    zip_bytes = create_zip(md5_files)
    md5hash = hashlib.md5(zip_bytes.getvalue())
    return md5hash.hexdigest()


def get_object(bucket, key):
    s3 = boto3.client("s3", config=session_config)
    try:
        s3 = boto3.client(
            "s3",
            config=session_config,
            aws_access_key_id="",
            aws_secret_access_key="",
            aws_session_token=""
        )
    except Exception as exc:
        if (
            hasattr(exc, "response")
            and exc.response.get("Error", {}).get("Code") == "NoSuchKey"
        ):
            return None
        elif hasattr(exc, "response") and exc.response.get("Error", {}).get("Code"):
            err = exc.response.get("Error", {}).get("Code")
            click.echo(f"Error {err}. Quitting.")
            raise
        else:
            raise


def get_latest_details(bucket, module_name):
    key = f"latest/{module_name}-latest.yml"
    response = get_object(bucket, key)
    if response is None:
        return None, None
    else:
        latest = yaml.load(response["Body"], Loader=yaml.FullLoader)
        return latest["version"], latest["md5sum"]


def collect_files(artifacts):
    md5 = {}
    full = {}
    for artifact_item in artifacts:
        folder = artifact_item.get("folder", ".")
        with pushd(folder):
            for pattern in artifact_item.get("pattern", ["*"]):
                recursive = artifact_item.get("recursive", False)
                click.echo(
                    f"Collecting Folder = {folder}, Pattern = {pattern}, Recursive = {recursive}"
                )
                files = sorted(glob.glob(pattern, recursive=recursive))
                full.setdefault(folder, []).extend(files)
                if artifact_item.get("include_in_md5", False):
                    click.echo("Including in md5sum-able artifacts")
                    md5.setdefault(folder, []).extend(files)
        full[folder] = sorted(list(set(full.get(folder, []))))
        md5[folder] = sorted(list(set(md5.get(folder, []))))
    return sorted(full.items()), sorted(md5.items())


def install_module(folder, bucket, module_name, version=None):
    path = Path(".") / folder / module_name
    try:
        if os.path.exists(path):
            click.echo(f"... Folder {path} already exists. Removing.")
            shutil.rmtree(path)
    except Exception:
        click.echo("Error occurred removing folder. Quitting.")
        sys.exit(1)
    if version is None or version == "latest":
        version, _ = get_latest_details(bucket, module_name)
    if version is None:
        version = "latest"
        click.echo(
            f"Module {module_name}=={version} does not exist in bucket {bucket}. Skipping."
        )
        return
    key = (
        f"modules/dev/{module_name}-{version}.zip"
        if "dev" in version
        else f"modules/{module_name}-{version}.zip"
    )
    click.echo(f"Downloading s3://{bucket}/{key}")
    response = get_object(bucket, key)
    if response is None:
        click.echo(
            f"... Module {module_name}=={version} not found in bucket {bucket}. Skipping."
        )
        return
    else:
        try:
            click.echo(f"Creating folder {path} for module {module_name}")
            os.makedirs(path)
            click.echo("Unzipping module")
            zip_file = zipfile.ZipFile(io.BytesIO(response["Body"].read()))
            zip_file.extractall(path)
            return version
        except Exception as exc:
            click.echo(f"... Error occurred creating folder or unzipping: {exc}")
            click.echo("Quitting.")
            sys.exit(1)


def add_resource_and_outputs(
    resource_id, module_doc, module_template_path, target_doc
):
    target_doc.setdefault("Resources", CommentedMap())
    target_doc.setdefault("Outputs", CommentedMap())
    target_doc["Resources"][resource_id] = CommentedMap()
    target_doc["Resources"][resource_id]["Type"] = "AWS::CloudFormation::Stack"
    target_doc["Resources"][resource_id]["Properties"] = CommentedMap()
    target_doc["Resources"][resource_id]["Properties"][
        "TemplateURL"
    ] = module_template_path
    target_doc["Resources"][resource_id]["Properties"]["Parameters"] = CommentedMap()
    params = target_doc["Resources"][resource_id]["Properties"]["Parameters"]
    interface = module_doc.get("Metadata", {}).get("AWS::CloudFormation::Interface", {})
    parameter_groups = interface.get("ParameterGroups", [])
    parameter_labels = interface.get("ParameterLabels", {})
    parameters = module_doc.get("Parameters", {})
    outputs = module_doc.get("Outputs", {})
    for output_name, output_value in outputs.items():
        if output_value.get('Export'):
            del output_value['Export']
        if output_value.get('Condition'):
            del output_value['Condition']
        target_doc["Outputs"][f'{resource_id}{output_name}'] = output_value
        tag = Tag()
        tag.value = '!GetAtt'
        target_doc["Outputs"][f'{resource_id}{output_name}']['Value']._yaml_tag = tag
        target_doc["Outputs"][f'{resource_id}{output_name}']['Value'].value = f'{resource_id}.Outputs.{output_name}'
    comments = []
    before = None
    for group in parameter_groups:
        label = group.get("Label", {}).get("default", "Undefined Group Name")
        group_name = f"#### {label} ####"
        box = "#" * len(group_name)
        comments.extend([box, group_name, box])
        for parameter in group.get("Parameters", []):
            if parameter in parameters:
                parameter_label = parameter_labels.get(parameter, {}).get(
                    "default", parameter
                )
                parameter_type = parameters[parameter].get("Type", "Unspecified Type")
                parameter_description = parameters[parameter].get(
                    "Description", "Unspecified Description"
                )
                comments.append(f"## {parameter_label} ({parameter_type}) ##")
                comments.append(f"##     {parameter_description}")
                if before is None:
                    params.yaml_set_start_comment("\n".join(comments), indent=8)
                else:
                    params.yaml_set_comment_before_after_key(
                        parameter, "\n".join(comments), after=before, indent=8
                    )
                before = parameter
                params[parameter] = ""
                comments = []
                del parameters[parameter]
    if parameters:
        comments = []
        comments.append("##############################")
        comments.append("#### Ungrouped Parameters ####")
        comments.append("##############################")
    for parameter in parameters.keys():
        parameter_label = parameter_labels.get(parameter, {}).get("default", parameter)
        parameter_type = parameters[parameter].get("Type", "Unspecified Type")
        parameter_description = parameters[parameter].get(
            "Description", "Unspecified Description"
        )
        comments.append(f"## {parameter_label} ({parameter_type}) ##")
        comments.append(f"##     {parameter_description}")
        if before is None:
            params.yaml_set_start_comment("\n".join(comments), indent=8)
        else:
            params.yaml_set_comment_before_after_key(
                parameter, "\n".join(comments), after=before, indent=8
            )
        before = parameter
        params[parameter] = ""
        comments = []
    return target_doc


@cli.command()
def freeze():
    path = Path("modules")
    for entry in os.listdir(path):
        if os.path.isdir(path / entry):
            module_conf_file = path / entry / "module.yml"
            if not os.path.exists(module_conf_file) or not os.path.isfile(
                module_conf_file
            ):
                click.echo(
                    f"Folder {entry} in modules folder does not have module.yml.  Skipping.",
                    err=True,
                )
                continue
            with open(module_conf_file, "r") as f:
                conf = yaml.load(f, Loader=yaml.FullLoader)
            module_name = conf["module"]["name"]
            version = conf["module"]["version"]
            click.echo(f"{module_name}=={version}")


def get_mod_path(modules_path, module_name):
    path = Path(modules_path) / module_name / "module.yml"
    with open(path, "r") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    entrypoint = conf["module"]["entrypoint"]
    return Path(modules_path) / module_name / entrypoint, entrypoint


def write_document(template, document):
    yaml = YAML()
    with open(template, "w") as f:
        yaml.dump(document, f)


def load_document(template, ignore_empty=False):
    yaml = YAML()
    try:
        with open(template, "r") as f:
            document = yaml.load(f.read())
    except FileNotFoundError:
        if ignore_empty:
            return {}
        else:
            raise
    if not document:
        return {}
    else:
        return document


@cli.command()
@click.option("--bucket", "-b", required=True)
@click.option("--template", "-t", required=True)
@click.argument("module", nargs=-1)
def add(bucket, template, module):
    if not module:
        click.echo("No module supplied. Exiting without action.")
        sys.exit(1)
    installed = []
    for mod in module:
        mod = mod.strip()
        if "==" in mod:
            mod, version = mod.split("==")
            click.echo(f"Installing module {mod}=={version}")
            installed_ver = install_module("modules", bucket, mod, version)
        else:
            click.echo(f"Installing module {mod}")
            installed_ver = install_module("modules", bucket, mod)
        if installed_ver is not None:
            installed.append(mod)
    for mod in installed:
        click.echo(f"Adding module {mod} to temlate file {template} as nested stack.")
        resource_id = click.prompt("Enter logical resource id")
        mod_template_path, entrypoint = get_mod_path("modules", mod)
        click.echo(f"Adding resource {resource_id} to {template}")
        target_doc = load_document(template, ignore_empty=True)
        module_doc = load_document(mod_template_path)
        target_doc = add_resource_and_outputs(
            resource_id, module_doc, f"./modules/{mod}/{entrypoint}", target_doc
        )
        write_document(template, target_doc)


@cli.command()
@click.option("--bucket", "-b", required=True)
@click.option("--modules-file", "-f", type=click.File("r"))
@click.argument("module", nargs=-1)
def install(bucket, modules_file, module):
    if not module and not modules_file:
        click.echo("No module or modules file supplied. Exiting without action.")
        sys.exit(1)
    if module and modules_file:
        click.echo(
            "Both module and modules file supplied. Unsupported option combination. Exiting without action."
        )
        sys.exit(1)
    mod_iter = module if module else modules_file
    for mod in mod_iter:
        mod = mod.strip()
        if "==" in mod:
            module_name, version = mod.split("==")
            click.echo(f"Installing module {module_name}=={version}")
            install_module("modules", bucket, module_name, version)
        else:
            click.echo(f"Installing module {mod}")
            install_module("modules", bucket, mod)


@cli.command()
@click.option("--bucket", "-b", required=True)
def publish(bucket):
    # load configuration
    with open("module.yml", "r") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    module_name = conf["module"]["name"]
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    build_number = os.environ.get(
        conf["module"]["build_number_environment_variable"], f"dev{now}"
    )
    version = f'{conf["module"]["version"]}.{build_number}'
    # entrypoint = conf["module"]["entrypoint"]
    # Check published version
    latest_version, latest_md5sum = get_latest_details(bucket, module_name)
    all_files, md5_files = collect_files(conf["module"]["artifacts"])
    click.echo("# Calculating md5 sum")
    new_md5sum = calc_md5(md5_files)
    if version == latest_version and new_md5sum == latest_md5sum:
        click.echo(f"Version {version} and md5 sum {latest_md5sum} MATCH. Quitting.")
        sys.exit(0)
    elif version == latest_version and new_md5sum != latest_md5sum:
        click.echo(
            f"Building version {version}, but version matches latest published"
            " and the md5 sums DO NOT match.  Quitting."
        )
        sys.exit(1)
    elif new_md5sum == latest_md5sum:
        click.echo(
            f"Artifacts match existing latest version {latest_version}. Quitting."
        )
        sys.exit(0)
    key = (
        f"modules/dev/{module_name}-{version}.zip"
        if "dev" in version
        else f"modules/{module_name}-{version}.zip"
    )
    click.echo("# Creating zip file")
    artifact_zip = create_zip(all_files, version)
    s3 = boto3.client("s3", config=session_config)
    click.echo("# Writing artifact")
    s3.put_object(Body=artifact_zip.getvalue(), Bucket=bucket, Key=key)
    click.echo(f"# Artifact written to s3://{bucket}/{key}")
    if "dev" not in version:
        click.echo(f"# Updating {module_name} module latest details")
        latest = {"version": version, "md5sum": new_md5sum}
        key = f"latest/{module_name}-latest.yml"
        s3.put_object(Body=yaml.dump(latest).encode("utf-8"), Bucket=bucket, Key=key)


if __name__ == "__main__":
    cli(auto_envvar_prefix="CFN_MOD")
