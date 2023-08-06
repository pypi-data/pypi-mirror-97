# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from __future__ import print_function
import click
import oci  # noqa: F401
import six  # noqa: F401
import sys  # noqa: F401
from oci_cli import cli_constants  # noqa: F401
from oci_cli import cli_util
from oci.util import formatted_flat_dict
from oci_cli import json_skeleton_utils
from oci_cli import custom_types  # noqa: F401
from services.rover.src.oci_cli_rover.generated import rover_service_cli
from services.rover.src.oci_cli_rover_cluster.generated import rovercluster_cli
from services.rover.src.oci_cli_rover.rover_utils import get_compute_image_helper, export_compute_image_helper

cli_util.rename_command(rover_service_cli, rover_service_cli.rover_service_group, rovercluster_cli.rover_cluster_group, 'cluster')
cli_util.rename_command(rover_service_cli, rovercluster_cli.rover_cluster_group, rovercluster_cli.get_rover_cluster, 'show')
cli_util.rename_command(rover_service_cli, rovercluster_cli.rover_cluster_group, rovercluster_cli.list_rover_clusters, 'list')


def complex_shipping_address_param(**kwargs):

    kwargs['customer_shipping_address'] = {}

    customer_address_options = {
        'addressee': 'addressee',
        'care_of': 'careOf',
        'address1': 'address1',
        'address2': 'address2',
        'address3': 'address3',
        'address4': 'address4',
        'city_or_locality': 'cityOrLocality',
        'state_province_region': 'stateOrRegion',
        'country': 'country',
        'zip_postal_code': 'zipcode',
        'phone_number': 'phoneNumber',
        'email': 'email'
    }

    for option, value in customer_address_options.items():
        if option in kwargs:
            kwargs['customer_shipping_address'][value] = kwargs[option]
            kwargs.pop(option)

    return kwargs


def get_rover_cluster_helper(ctx, cluster_id):
    kwargs_request = {
        'opc_request_id': cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    }

    client = cli_util.build_client('rover', 'rover_cluster', ctx)

    return client.get_rover_cluster(
        rover_cluster_id=cluster_id,
        **kwargs_request
    )


@cli_util.copy_params_from_generated_command(rovercluster_cli.create_rover_cluster, params_to_exclude=['customer_shipping_address', 'display_name', 'compartment_id', 'cluster_size'])
@rovercluster_cli.rover_cluster_group.command(name=rovercluster_cli.create_rover_cluster.name, help=rovercluster_cli.create_rover_cluster.help)
@cli_util.option('--display-name', required=True, help=u"""A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.""")
@cli_util.option('--compartment-id', required=True, help=u"""The OCID of the compartment containing the RoverCluster.""")
@cli_util.option('--cluster-size', required=True, type=click.INT, help=u"""Number of nodes desired in the cluster, between 5 and 15.""")
@cli_util.option('--cluster-workloads', type=custom_types.CLI_COMPLEX_TYPE, help=u"""List of existing workloads that should be provisioned on the nodes.

This option is a JSON list with items of type RoverWorkload.  For documentation on RoverWorkload please see our API reference: https://docs.cloud.oracle.com/api/#/en/rovercluster/20201210/datatypes/RoverWorkload.""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--super-user-password', help=u"""Root password for the rover cluster.""")
@cli_util.option('--enclosure-type', type=custom_types.CliCaseInsensitiveChoice(["RUGGADIZED", "NON_RUGGADIZED"]), help=u"""The type of enclosure rover nodes in this cluster are shipped in.""")
@cli_util.option('--unlock-passphrase', help=u"""Password to unlock the rover cluster.""")
@cli_util.option('--point-of-contact', help=u"""Name of point of contact for this order if customer is picking up.""")
@cli_util.option('--point-of-contact-phone-number', help=u"""Phone number of point of contact for this order if customer is picking up.""")
@cli_util.option('--shipping-preference', type=custom_types.CliCaseInsensitiveChoice(["ORACLE_SHIPPED", "CUSTOMER_PICKUP"]), help=u"""Preference for device delivery.""")
@cli_util.option('--shipping-vendor', help=u"""Shipping vendor of choice for orace to customer shipping.""")
@cli_util.option('--oracle-shipping-tracking-url', help=u"""Tracking Url for the shipped Rover Cluster.""")
@cli_util.option('--addressee', help=u"""Company or person to send the appliance to""")
@cli_util.option('--care-of', help=u"""Place/person to direct the package to.""")
@cli_util.option('--address1', help=u"""Address line 1.""")
@cli_util.option('--address2', help=u"""Optional address line 2.""")
@cli_util.option('--address3', help=u"""Optional address line 3.""")
@cli_util.option('--address4', help=u"""Optional address line 4.""")
@cli_util.option('--city-or-locality', help=u"""City or Locality.""")
@cli_util.option('--state-province-region', help=u"""State or Province or Region.""")
@cli_util.option('--country', help=u"""Country.""")
@cli_util.option('--zip-postal-code', help=u"""Zip or Postal Code""")
@cli_util.option('--phone-number', help=u"""Phone number.""")
@cli_util.option('--email', help=u"""Email address.""")
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""The freeform tags associated with this resource, if any. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags]. Example: `{\"Department\": \"Finance\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""The defined tags associated with this resource, if any. Each key is predefined and scoped to namespaces. For more information, see [Resource Tags]. Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'customer-shipping-address': {'module': 'rover', 'class': 'ShippingAddress'}, 'cluster-workloads': {'module': 'rover', 'class': 'list[RoverWorkload]'}, 'freeform-tags': {'module': 'rover', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'rover', 'class': 'dict(str, dict(str, object))'}, 'system-tags': {'module': 'rover', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'rover', 'class': 'RoverCluster'})
@cli_util.wrap_exceptions
def create_rover_cluster_extended(ctx, **kwargs):
    client = cli_util.build_client('rover', 'rover_cluster', ctx)
    kwargs = complex_shipping_address_param(**kwargs)
    kwargs['cluster_workloads'] = []
    ctx.invoke(rovercluster_cli.create_rover_cluster, **kwargs)


@rovercluster_cli.rover_cluster_group.command(name=rovercluster_cli.get_rover_cluster.name, help=rovercluster_cli.get_rover_cluster.help)
@cli_util.option('--cluster-id', required=True, help=u"""Unique RoverCluster identifier""")
@cli_util.help_option
@json_skeleton_utils.get_cli_json_input_option({})
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'rover', 'class': 'RoverCluster'})
@cli_util.wrap_exceptions
def show_rover_cluster_extended(ctx, **kwargs):
    if isinstance(kwargs['cluster_id'], six.string_types) and len(kwargs['cluster_id'].strip()) == 0:
        raise click.UsageError('Parameter --cluster-id cannot be whitespace or empty string')

    result = get_rover_cluster_helper(ctx, kwargs['cluster_id'])
    cli_util.render_response(result, ctx)


@cli_util.copy_params_from_generated_command(rovercluster_cli.update_rover_cluster, params_to_exclude=['customer_shipping_address', 'rover_cluster_id', 'display_name'])
@rovercluster_cli.rover_cluster_group.command(name=rovercluster_cli.update_rover_cluster.name, help=rovercluster_cli.update_rover_cluster.help)
@cli_util.option('--cluster-id', required=True, help=u"""Unique RoverCluster identifier""")
@cli_util.option('--display-name', help=u"""A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.""")
@cli_util.option('--cluster-size', type=click.INT, help=u"""Number of nodes desired in the cluster, between 5 and 15.""")
@cli_util.option('--cluster-workloads', type=custom_types.CLI_COMPLEX_TYPE, help=u"""List of existing workloads that should be provisioned on the nodes.

This option is a JSON list with items of type RoverWorkload.  For documentation on RoverWorkload please see our API reference: https://docs.cloud.oracle.com/api/#/en/rovercluster/20201210/datatypes/RoverWorkload.""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--super-user-password', help=u"""Root password for the rover cluster.""")
@cli_util.option('--lifecycle-state', type=custom_types.CliCaseInsensitiveChoice(["CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED"]), help=u"""The current state of the RoverCluster.""")
@cli_util.option('--lifecycle-state-details', help=u"""A property that can contain details on the lifecycle.""")
@cli_util.option('--unlock-passphrase', help=u"""Password to unlock the rover cluster.""")
@cli_util.option('--enclosure-type', type=custom_types.CliCaseInsensitiveChoice(["RUGGADIZED", "NON_RUGGADIZED"]), help=u"""The type of enclosure rover nodes in this cluster are shipped in.""")
@cli_util.option('--point-of-contact', help=u"""Name of point of contact for this order if customer is picking up.""")
@cli_util.option('--point-of-contact-phone-number', help=u"""Phone number of point of contact for this order if customer is picking up.""")
@cli_util.option('--shipping-preference', type=custom_types.CliCaseInsensitiveChoice(["ORACLE_SHIPPED", "CUSTOMER_PICKUP"]), help=u"""Preference for device delivery.""")
@cli_util.option('--oracle-shipping-tracking-url', help=u"""Tracking Url for the shipped Rover Cluster.""")
@cli_util.option('--shipping-vendor', help=u"""Shipping vendor of choice for orace to customer shipping.""")
@cli_util.option('--addressee', help=u"""Company or person to send the appliance to""")
@cli_util.option('--care-of', help=u"""Place/person to direct the package to.""")
@cli_util.option('--address1', help=u"""Address line 1.""")
@cli_util.option('--address2', help=u"""Optional address line 2.""")
@cli_util.option('--address3', help=u"""Optional address line 3.""")
@cli_util.option('--address4', help=u"""Optional address line 4.""")
@cli_util.option('--city-or-locality', help=u"""City or Locality.""")
@cli_util.option('--state-province-region', help=u"""State or Province or Region.""")
@cli_util.option('--country', help=u"""Country.""")
@cli_util.option('--zip-postal-code', help=u"""Zip or Postal Code""")
@cli_util.option('--phone-number', help=u"""Phone number.""")
@cli_util.option('--email', help=u"""Email address.""")
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `if-match` parameter to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@cli_util.option('--force', help="""Perform update without prompting for confirmation.""", is_flag=True)
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'customer-shipping-address': {'module': 'rover', 'class': 'ShippingAddress'}, 'cluster-workloads': {'module': 'rover', 'class': 'list[RoverWorkload]'}, 'freeform-tags': {'module': 'rover', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'rover', 'class': 'dict(str, dict(str, object))'}, 'system-tags': {'module': 'rover', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'rover', 'class': 'RoverCluster'})
@cli_util.wrap_exceptions
def update_rover_cluster_extended(ctx, **kwargs):

    # Get the RoverCluster and check if the policy language has been added by Oracle
    client = cli_util.build_client('rover', 'rover_cluster', ctx)

    kwargs = complex_shipping_address_param(**kwargs)
    kwargs['lifecycle_state_details'] = "PENDING_SUBMISSION"
    kwargs.update({
        'rover_cluster_id': kwargs['cluster_id']
    })
    kwargs.pop('cluster_id')

    ctx.invoke(rovercluster_cli.update_rover_cluster, **kwargs)


@rovercluster_cli.rover_cluster_group.command(name="request-approval", help=u"""Submit request for Rover Cluster""")
@cli_util.option('--cluster-id', required=True, help=u"""Unique RoverCluster identifier""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'rover', 'class': 'RoverCluster'})
@cli_util.wrap_exceptions
def request_rover_cluster(ctx, **kwargs):

    kwargs_request = {'rover_cluster_id': kwargs['cluster_id'],
                      'lifecycle_state': "ACTIVE",
                      'lifecycle_state_details': "PENDING_APPROVAL"}
    click.echo("Changing the state of the rover cluster to PENDING_APPROVAL")
    ctx.invoke(rovercluster_cli.update_rover_cluster, **kwargs_request)


@cli_util.copy_params_from_generated_command(rovercluster_cli.delete_rover_cluster, params_to_exclude=['rover_cluster_id'])
@rovercluster_cli.rover_cluster_group.command(name=rovercluster_cli.delete_rover_cluster.name, help=rovercluster_cli.delete_rover_cluster.help)
@cli_util.option('--cluster-id', required=True, help=u"""Unique RoverCluster identifier""")
@cli_util.confirm_delete_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def delete_rover_cluster_extended(ctx, **kwargs):

    if isinstance(kwargs['cluster_id'], six.string_types) and len(kwargs['cluster_id'].strip()) == 0:
        raise click.UsageError('Parameter --cluster-id cannot be whitespace or empty string')

    kwargs_request = {}
    kwargs_request['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('rover', 'rover_cluster', ctx)
    result = client.delete_rover_cluster(
        rover_cluster_id=kwargs['cluster_id'],
        **kwargs_request
    )
    cli_util.render_response(result, ctx)


@rovercluster_cli.rover_cluster_group.command(name="set-secrets", help=u"""Assign super-user-password and unlock-password for Rover Cluster""")
@cli_util.option('--cluster-id', required=True, help=u"""Unique RoverCluster identifier""")
@cli_util.option('--super-user-password', required=False, is_flag=True, help=u"""Assign super-user-password for RoverCluster Identifier""")
@cli_util.option('--unlock-passphrase', required=False, is_flag=True, help=u"""Assign unlock-passphrase for RoverCluster Identifier""")
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'rover', 'class': 'RoverCluster'})
@cli_util.wrap_exceptions
def set_secrets_rover_cluster(ctx, **kwargs):

    kwargs_request = {'rover_cluster_id': kwargs['cluster_id']}

    if kwargs['super_user_password'] or (not kwargs['super_user_password'] and not kwargs['unlock_passphrase']):
        super_user_password = click.prompt(text='Enter super-user password', default='',
                                           hide_input=True, show_default=False, confirmation_prompt=True)
        if not super_user_password:
            raise click.UsageError('Super user password cannot be whitespace or empty string')
        kwargs_request['super_user_password'] = super_user_password

    if kwargs['unlock_passphrase'] or (not kwargs['super_user_password'] and not kwargs['unlock_passphrase']):
        unlock_passphrase = click.prompt(text='Enter unlock passphrase', default='',
                                         hide_input=True, show_default=False, confirmation_prompt=True)
        if not unlock_passphrase:
            raise click.UsageError('Unlock passphrase cannot be whitespace or empty string')
        kwargs_request['unlock_passphrase'] = unlock_passphrase

    ctx.invoke(rovercluster_cli.update_rover_cluster, **kwargs_request)


@cli_util.copy_params_from_generated_command(rovercluster_cli.change_rover_cluster_compartment, params_to_exclude=['rover_cluster_id'])
@rovercluster_cli.rover_cluster_group.command(name=rovercluster_cli.change_rover_cluster_compartment.name, help=rovercluster_cli.change_rover_cluster_compartment.help)
@cli_util.option('--cluster-id', required=True, help=u"""Unique RoverCluster identifier""")
@cli_util.option('--compartment-id', required=True, help=u"""The [OCID]  of the compartment into which the resources should be moved.""")
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `if-match` parameter to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def change_rover_cluster_compartment(ctx, **kwargs):

    if isinstance(kwargs['cluster_id'], six.string_types) and len(kwargs['cluster_id'].strip()) == 0:
        raise click.UsageError('Parameter --cluster-id cannot be whitespace or empty string')
    kwargs.update({'rover_cluster_id': kwargs['cluster_id']})
    kwargs.pop('cluster_id')
    ctx.invoke(rovercluster_cli.change_rover_cluster_compartment, **kwargs)


@rovercluster_cli.rover_cluster_group.command(name="add-workload", help=u"""Add workload information to Rover Cluster""")
@cli_util.option('--cluster-id', required=True, help=u"""Unique RoverCluster identifier""")
@cli_util.option('--compartment-id', required=True, help=u"""Compartment Id of Bucket""")
@cli_util.option('--type', required=True, type=custom_types.CliCaseInsensitiveChoice(["BUCKET", "IMAGE"]), help=u"""Type of workload""")
@cli_util.option('--image-id', help=u"""Object Store Image OCID for the workload""")
@cli_util.option('--bucket-id', help=u"""Object Store Bucket OCID for the workload""")
@cli_util.option('--bucket-name', help=u"""Object Store Bucket name for the workload""")
@cli_util.option('--prefix', help=u"""List of objects with names matching this prefix would be part of this export job.""")
@cli_util.option('--range-start', help=u"""Object names returned by a list query must be greater or equal to this parameter.""")
@cli_util.option('--range-end', help=u"""Object names returned by a list query must be strictly less than this parameter.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'rover', 'class': 'RoverCluster'})
@cli_util.wrap_exceptions
def add_workload(ctx, **kwargs):

    workload_data = image_id = workload_id = compute_obj = destination_uri = None
    result = get_rover_cluster_helper(ctx, kwargs['cluster_id'])

    if kwargs['type'].lower() == "bucket":
        if not ('bucket_id' in kwargs and kwargs['bucket_id']) or not ('bucket_name' in kwargs and kwargs['bucket_name']):
            raise click.UsageError('Parameter bucket-id and bucket-name cannot be whitespace or empty string')
        workload_id = kwargs['bucket_id']
        workload_data = [{
            "workloadType": "BUCKET", "id": kwargs['bucket_id'], "name": kwargs['bucket_name'], "compartmentId": kwargs['compartment_id'],
            'prefix': kwargs['prefix'], 'rangeStart': kwargs['range_start'], 'rangeEnd': kwargs['range_end']
        }]

    elif kwargs['type'].lower() == "image":
        if 'image_id' in kwargs and not kwargs['image_id']:
            raise click.UsageError('Parameter image-id cannot be whitespace or empty string')
        workload_id = image_id = kwargs['image_id']
        compute_image_obj = get_compute_image_helper(ctx, image_id)
        destination_uri = result.data.image_export_par + compute_image_obj.data.display_name + "_" + image_id + ".oci"
        workload_data = [
            {'workloadType': "IMAGE", 'id': image_id, 'name': compute_image_obj.data.display_name,
             'size': compute_image_obj.data.size_in_mbs, 'compartmentId': kwargs['compartment_id'],
             }
        ]
    confirm_prompt = "Would you like to submit the following workload information ? " + formatted_flat_dict(workload_data)
    if result.data.cluster_workloads:
        if any(existing_workload.id == workload_id for existing_workload in result.data.cluster_workloads):
            raise click.UsageError("Workload with {} is already attached".format(workload_id))

    if not click.confirm(click.style(confirm_prompt, fg="yellow")):
        click.echo("Aborting workload selection for Rover Cluster")
        ctx.abort()
    if kwargs['type'].lower() == "image":
        export_compute_image_helper(ctx, image_id, destination_uri)

    if result.data.cluster_workloads:
        workload_data.extend(result.data.cluster_workloads)
    kwargs_request = {'rover_cluster_id': kwargs['cluster_id'],
                      'cluster_workloads': workload_data}
    ctx.invoke(rovercluster_cli.update_rover_cluster, **kwargs_request)


@rovercluster_cli.rover_cluster_group.command(name="delete-workload", help=u"""Delete workload information from Rover Cluster""")
@cli_util.option('--cluster-id', required=True, help=u"""Unique RoverCluster identifier""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'rover', 'class': 'RoverCluster'})
@cli_util.wrap_exceptions
def delete_workload(ctx, **kwargs):

    result = get_rover_cluster_helper(ctx, kwargs['cluster_id'])
    workload_index = 0
    workload_data = result.data.cluster_workloads
    if workload_data:
        if len(workload_data) > 1:
            for idx, each_workload in enumerate(workload_data, 1):
                click.echo("{}. {}".format(idx, formatted_flat_dict(each_workload)))
            workload_index = click.prompt("Enter workload number to be deleted", type=int)
            if workload_index > len(workload_data) or workload_index < 1:
                raise click.UsageError("Please try again with valid selection")
        confirm_prompt = "Are you sure you want to delete following workload ? " + formatted_flat_dict(
            workload_data[workload_index - 1])
        if not click.confirm(click.style(confirm_prompt, fg="yellow")):
            raise click.UsageError("Aborting workload deletion from Rover Cluster")
        workload_data.pop(workload_index - 1)
    else:
        raise click.UsageError("Cluster has no associated workloads.")
    kwargs_request = {'rover_cluster_id': kwargs['cluster_id'],
                      'cluster_workloads': workload_data}
    ctx.invoke(rovercluster_cli.update_rover_cluster, **kwargs_request)


@rovercluster_cli.rover_cluster_group.command(name="list-workload", help=u"""List workload information of Rover Cluster""")
@cli_util.option('--cluster-id', required=True, help=u"""Unique RoverCluster identifier""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'rover', 'class': 'RoverCluster'})
@cli_util.wrap_exceptions
def list_workload(ctx, **kwargs):

    result = get_rover_cluster_helper(ctx, kwargs['cluster_id'])
    workload_data = result.data.cluster_workloads
    if workload_data:
        for idx, each_workload in enumerate(workload_data, 1):
            click.echo("{}. {}".format(idx, formatted_flat_dict(each_workload)))
    else:
        raise click.UsageError("Cluster has no associated workloads.")
