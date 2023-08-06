# Copyright (C) 2020, Hitachi, Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
"""Fibre channel module for Hitachi HBSD Driver."""

from oslo_config import cfg

from cinder import interface
from cinder import utils as cinder_utils
from cinder.volume import configuration
from cinder.volume import driver
from cinder.volume.drivers.hitachi import hbsd_common as common
from cinder.volume.drivers.hitachi import hbsd_utils as utils

FC_VOLUME_OPTS = [
    cfg.BoolOpt(
        'hitachi_zoning_request',
        default=False,
        help='If True, the driver will configure FC zoning between the server '
             'and the storage system provided that FC zoning manager is '
             'enabled.'),
]

MSG = utils.HBSDMsg

_DRIVER_INFO = {
    'proto': 'FC',
    'hba_id': 'wwpns',
    'hba_id_type': 'World Wide Name',
    'msg_id': {
        'target': MSG.CREATE_HOST_GROUP_FAILED,
    },
    'volume_backend_name': '%(prefix)sFC' % {
        'prefix': utils.DRIVER_PREFIX,
    },
    'volume_opts': FC_VOLUME_OPTS,
    'volume_type': 'fibre_channel',
}

CONF = cfg.CONF
CONF.register_opts(FC_VOLUME_OPTS, group=configuration.SHARED_CONF_GROUP)


@interface.volumedriver
class HBSDFCDriver(driver.FibreChannelDriver):
    """Fibre channel class for Hitachi HBSD Driver.

    Version history:

    .. code-block:: none

        1.0.0 - Initial driver.
        1.1.0 - Add manage_existing/manage_existing_get_size/unmanage methods
        2.0.0 - Major redesign of the driver. This version requires the REST
                API for communication with the storage backend.

    """

    VERSION = common.VERSION

    # ThirdPartySystems wiki page
    CI_WIKI_NAME = "Hitachi_VSP_CI"

    def __init__(self, *args, **kwargs):
        """Initialize instance variables."""
        utils.output_log(MSG.DRIVER_INITIALIZATION_START,
                         driver=self.__class__.__name__,
                         version=self.get_version())
        super(HBSDFCDriver, self).__init__(*args, **kwargs)

        self.configuration.append_config_values(common.COMMON_VOLUME_OPTS)
        self.configuration.append_config_values(FC_VOLUME_OPTS)
        self.common = utils.import_object(
            self.configuration, _DRIVER_INFO, kwargs.get('db'))

    def check_for_setup_error(self):
        pass

    @cinder_utils.trace
    def create_volume(self, volume):
        """Create a volume and return its properties."""
        return self.common.create_volume(volume)

    @cinder_utils.trace
    def create_volume_from_snapshot(self, volume, snapshot):
        """Create a volume from a snapshot and return its properties."""
        return self.common.create_volume_from_snapshot(volume, snapshot)

    @cinder_utils.trace
    def create_cloned_volume(self, volume, src_vref):
        """Create a clone of the specified volume and return its properties."""
        return self.common.create_cloned_volume(volume, src_vref)

    @cinder_utils.trace
    def delete_volume(self, volume):
        """Delete the specified volume."""
        self.common.delete_volume(volume)

    @cinder_utils.trace
    def create_snapshot(self, snapshot):
        """Create a snapshot from a volume and return its properties."""
        return self.common.create_snapshot(snapshot)

    @cinder_utils.trace
    def delete_snapshot(self, snapshot):
        """Delete the specified snapshot."""
        self.common.delete_snapshot(snapshot)

    def local_path(self, volume):
        pass

    def get_volume_stats(self, refresh=False):
        """Return properties, capabilities and current states of the driver."""
        data = self.common.get_volume_stats(refresh)
        if 'pools' in data:
            data["pools"][0]["filter_function"] = self.get_filter_function()
            data["pools"][0]["goodness_function"] = (
                self.get_goodness_function())
        return data

    @cinder_utils.trace
    def update_migrated_volume(
            self, ctxt, volume, new_volume, original_volume_status):
        """Do any remaining jobs after migration."""
        self.common.discard_zero_page(new_volume)
        super(HBSDFCDriver, self).update_migrated_volume(
            ctxt, volume, new_volume, original_volume_status)

    @cinder_utils.trace
    def copy_image_to_volume(self, context, volume, image_service, image_id):
        """Fetch the image from image_service and write it to the volume."""
        super(HBSDFCDriver, self).copy_image_to_volume(
            context, volume, image_service, image_id)
        self.common.discard_zero_page(volume)

    @cinder_utils.trace
    def extend_volume(self, volume, new_size):
        """Extend the specified volume to the specified size."""
        self.common.extend_volume(volume, new_size)

    @cinder_utils.trace
    def manage_existing(self, volume, existing_ref):
        """Return volume properties which Cinder needs to manage the volume."""
        return self.common.manage_existing(volume, existing_ref)

    @cinder_utils.trace
    def manage_existing_get_size(self, volume, existing_ref):
        """Return the size[GB] of the specified volume."""
        return self.common.manage_existing_get_size(existing_ref)

    @cinder_utils.trace
    def unmanage(self, volume):
        """Prepare the volume for removing it from Cinder management."""
        self.common.unmanage(volume)

    @cinder_utils.trace
    def do_setup(self, context):
        """Prepare for the startup of the driver."""
        self.common.do_setup(context)

    def ensure_export(self, context, volume):
        """Synchronously recreate an export for a volume."""
        pass

    def create_export(self, context, volume, connector):
        """Export the volume."""
        pass

    def remove_export(self, context, volume):
        """Remove an export for a volume."""
        pass

    def create_export_snapshot(self, context, snapshot, connector):
        pass

    def remove_export_snapshot(self, context, snapshot):
        pass

    @cinder_utils.trace
    def initialize_connection(self, volume, connector):
        """Initialize connection between the server and the volume."""
        return self.common.initialize_connection(volume, connector)

    @cinder_utils.trace
    def terminate_connection(self, volume, connector, **kwargs):
        """Terminate connection between the server and the volume."""
        if connector is None:
            connector = {}
        if utils.is_shared_connection(volume, connector):
            return
        self.common.terminate_connection(volume, connector)

    @cinder_utils.trace
    def initialize_connection_snapshot(self, snapshot, connector, **kwargs):
        """Initialize connection between the server and the snapshot."""
        return self.common.initialize_connection(snapshot, connector)

    @cinder_utils.trace
    def terminate_connection_snapshot(self, snapshot, connector, **kwargs):
        """Terminate connection between the server and the snapshot."""
        self.common.terminate_connection(snapshot, connector)

    @cinder_utils.trace
    def unmanage_snapshot(self, snapshot):
        """Prepare the snapshot for removing it from Cinder management."""
        return self.common.unmanage_snapshot(snapshot)

    @cinder_utils.trace
    def retype(self, ctxt, volume, new_type, diff, host):
        """Retype the specified volume."""
        return self.common.retype()

    def backup_use_temp_snapshot(self):
        return True

    @cinder_utils.trace
    def revert_to_snapshot(self, context, volume, snapshot):
        """Rollback the specified snapshot"""
        return self.common.revert_to_snapshot(volume, snapshot)
