""" Represents a Supertag and its functionality. """
from conductor.airfinder.devices.node import Node
from conductor.airfinder.messages import DownlinkMessageSpec
from conductor.devices.lte_module import LTEmModule
from conductor.util import Version


class SupertagDownlinkMessageSpecV1(DownlinkMessageSpec):
    """ Supertag Message Specification v1.0.0. """

    header = {
        'def': ['msg_type', 'msg_spec_vers'],
        'struct': '>BB',
        'defaults': [0x00, 0x01]
    }

    msg_types = {
        'Configuration': {
            'def': ['mask', 'heartbeat', 'no_ap_heartbeat', 'no_sym_heartbeat', 'location_update_rate',
                    'no_ap_location_update_rate', 'no_sym_location_update_rate', 'scans_per_fix', 'max_wifi_aps',
                    'max_cell_ids', 'location_update_order', 'network_lost_timeout', 'ref_lost_timeout',
                    'network_scan_interval'],
            'struct': '>HIIIIIIBBBBHHH',
            'defaults': [0x0000, 0x0000003c, 0x00015180, 0x00015180,
                         0x0000000b, 0x00005460, 0x00005460, 0x04,
                         0x0a, 0x00, 0x1b, 0x0258, 0x0258, 0x00b4]
        }
    }


class SupertagDownlinkMessageSpecV2(SupertagDownlinkMessageSpecV1):
    """ Supertag Message Specification v2.0.0"""

    def __init__(self):
        super().__init__()

        # Update Message Spec Version.
        self.header.update({'defaults': [0x00, 0x02]})

        # Update Configuration Message.
        #   - Increase Change Mask Size
        #   - Added Help Mode fields
        #   - Added Accelerometer fields
        #   - Added Caching fields
        #   - Added GPS Power Settings
        self.msg_types['Configuration'].update({
            'def': ['mask', 'heartbeat', 'no_ap_heartbeat', 'no_sym_heartbeat',
                    'location_update_rate', 'no_ap_location_update_rate', 'no_sym_location_update_rate',
                    'help_location_update_rate', 'scans_per_fix', 'max_wifi_aps', 'max_cell_ids',
                    'location_update_order', 'acc_enable', 'acc_duration', 'acc_threshold', 'shock_threshold',
                    'cache_enable', 'cache_length', 'gps_power_mode', 'gps_timeout', 'net_lost_timeout',
                    'ref_lost_timeout', 'network_scan_interval'],
            'struct': '>IIIIIIIIBBBBBHHHBBBHHHH',
            'defaults': [0x00000000, 0x0000003c, 0x00015180, 0x00015180,
                         0x0000000b, 0x0000003c, 0x00005460, 0x0000000b, 0x04,
                         0x0a, 0x00, 0x1b, 0x01, 0x0003, 0x0050, 0x00a0, 0x00,
                         0x00, 0x00, 0x00b4, 0x0258, 0x0258, 0x00b4]
        })

        # Add new Message Types
        #   - Test Mode Enable
        #   - Help Mode Ack
        self.msg_types.update({
            'EnableTestMode': {},
            'Ack': {
                'def': ['help_rxed'],
                'struct': '>H',
                'defaults': [0x1105]
            }
        })


class LocationUpdateOrder:

    def __init__(self, cell_id_order=0, wifi_order=0, gps_order=0, polte_order=0):
        self.cell_id = cell_id_order
        self.wifi = wifi_order
        self.gps = gps_order
        self.polte = polte_order

    @property
    def value(self):
        bin_str = "{:02b}{:02b}{:02b}{:02b}".format(self.polte, self.gps, self.wifi, self.cell_id)
        return int(bin_str, 2)


class Supertag(Node):
    """ """
    application = "20028716136f69533e19"
    virtual_ap_app = "91fd9564b752338eac77"
    af_subject_name = "supertag"

    @property
    def symble_version(self):
        pass

    @property
    def version(self):
        major = self._md.get('fwVersionMajor')
        minor = self._md.get('fwVersionMinor')
        tag = self._md.get('fwVersionTag')
        if not major or not minor or not tag:
            return None
        return Version(major, minor, tag)

    @property
    def virtual_access_point(self):
        """ The 'virtual' LTEm Access Point for the Supertag. """
        vap = self._md.get("virtualAccessPoint")
        return LTEmModule(self.session, vap, self.instance) if vap else None

    @property
    def msg_spec_version(self):
        vers = self._md.get("msgSpecVersion")
        return Version(int(vers), 0, 0) if vers else None

    @property
    def hw_id(self):
        return self._make_prop(int, 'hwId')

    @classmethod
    def _get_spec(cls, vers):
        if vers.major == 1:
            return SupertagDownlinkMessageSpecV1()
        elif vers.major == 2:
            return SupertagDownlinkMessageSpecV2()
        else:
            raise Exception("No Supported Message Specification.")

    @property
    def heartbeat(self):
        return self._make_prop(int, "heartbeatInterval")

    @property
    def no_ap_heartbeat(self):
        return self._make_prop(int, "noApHeartbeatInterval")

    @property
    def no_sym_heartbeat(self):
        return self._make_prop(int, "noSymHeartbeatInterval")

    @property
    def location_update_rate(self):
        return self._make_prop(int, "locationUpdateRate")

    @property
    def no_ap_location_update_rate(self):
        return self._make_prop(int, "noApLocationUpdateRate")

    @property
    def no_sym_location_update_rate(self):
        return self._make_prop(int, "noSymLocationUpdateRate")

    def configure(self, time_to_live_s=60.0, access_point=None, **kwargs):
        """ TODO: docs
            'batt_cap', 'start_up_power', 'alive_time_power',
            'location_update_power', 'net_scan_power', 'ble_conn_power',
            'lte_success_power', 'lte_failed_power', 'gps_avg_power',
            'wifi_avg_power', 'temp_read_power', 'batt_read_power',
            'led_power', 'ftp_power'
        """
        vers = self.msg_spec_version
        pld = self._get_spec(vers).build_message("Configuration", **kwargs)
        return self._send_message(pld, time_to_live_s)

    @classmethod
    def multicast_configure(cls, vers, gws, time_to_live_s=60.0, access_point=None, ap_vers=None, **kwargs):
        pld = cls._get_spec(vers).build_message("Configuration", **kwargs)
        return cls._send_multicast_message(pld, time_to_live_s, ap_vers, gws)

    def ack(self, time_to_live_s=60.0, access_point=None):
        """ TODO """
        vers = self.msg_spec_version
        pld = self._get_spec(vers).build_message("Ack")
        return self._send_message(pld, time_to_live_s)

    @classmethod
    def multicast_ack(cls, vers, gws, time_to_live_s=60.0, access_point=None,
                      ap_vers=None):
        """ TODO """
        pld = cls._get_spec(vers).build_message("Ack")
        return cls._send_message(pld, time_to_live_s)

    def activate_test_mode(self, time_to_live_s=60.0, access_point=None):
        """ TODO """
        vers = self.msg_spec_version
        pld = self._get_spec(vers).build_message("EnableTestMode")
        return self._send_message(pld, time_to_live_s)

    @classmethod
    def multicast_activate_test_mode(cls, time_to_live_s=60.0, access_point=None, ap_vers=None):
        """ TODO """
        pld = cls.get_spec().build_message("EnableTestMode")
        return cls._send_message(pld, time_to_live_s)
