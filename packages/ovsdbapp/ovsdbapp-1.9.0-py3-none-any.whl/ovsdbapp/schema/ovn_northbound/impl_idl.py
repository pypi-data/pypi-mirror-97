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

from ovsdbapp.backend import ovs_idl
from ovsdbapp.backend.ovs_idl import idlutils
from ovsdbapp import constants as const
from ovsdbapp.schema.ovn_northbound import api
from ovsdbapp.schema.ovn_northbound import commands as cmd
from ovsdbapp import utils


class OvnNbApiIdlImpl(ovs_idl.Backend, api.API):
    schema = 'OVN_Northbound'
    lookup_table = {
        'Logical_Switch': idlutils.RowLookup('Logical_Switch', 'name', None),
        'Logical_Router': idlutils.RowLookup('Logical_Router', 'name', None),
        'Load_Balancer': idlutils.RowLookup('Load_Balancer', 'name', None),
    }

    def ls_add(self, switch=None, may_exist=False, **columns):
        return cmd.LsAddCommand(self, switch, may_exist, **columns)

    def ls_del(self, switch, if_exists=False):
        return cmd.LsDelCommand(self, switch, if_exists)

    def ls_list(self):
        return cmd.LsListCommand(self)

    def ls_get(self, switch):
        return cmd.LsGetCommand(self, switch)

    def ls_set_dns_records(self, switch_uuid, dns_uuids):
        return self.db_set('Logical_Switch', switch_uuid,
                           ('dns_records', dns_uuids))

    def ls_clear_dns_records(self, switch_uuid):
        return self.db_clear('Logical_Switch', switch_uuid, 'dns_records')

    def ls_add_dns_record(self, switch_uuid, dns_uuid):
        return self.db_add('Logical_Switch', switch_uuid, 'dns_records',
                           dns_uuid)

    def ls_remove_dns_record(self, switch_uuid, dns_uuid, if_exists=False):
        return self.db_remove('Logical_Switch', switch_uuid, 'dns_records',
                              dns_uuid, if_exists=if_exists)

    def acl_add(self, switch, direction, priority, match, action, log=False,
                may_exist=False, **external_ids):
        return cmd.AclAddCommand(self, switch, direction, priority,
                                 match, action, log, may_exist, **external_ids)

    def acl_del(self, switch, direction=None, priority=None, match=None):
        return cmd.AclDelCommand(self, switch, direction, priority, match)

    def acl_list(self, switch):
        return cmd.AclListCommand(self, switch)

    def pg_acl_add(self, port_group, direction, priority, match, action,
                   log=False, may_exist=False, severity=None, name=None,
                   meter=None, **external_ids):
        return cmd.PgAclAddCommand(self, port_group, direction, priority,
                                   match, action, log, may_exist,
                                   severity, name, meter,
                                   **external_ids)

    def pg_acl_del(self, port_group, direction=None, priority=None,
                   match=None):
        return cmd.PgAclDelCommand(self, port_group, direction, priority,
                                   match)

    def pg_acl_list(self, port_group):
        return cmd.PgAclListCommand(self, port_group)

    def qos_add(self, switch, direction, priority, match, rate=None,
                burst=None, dscp=None, may_exist=False, **columns):
        return cmd.QoSAddCommand(self, switch, direction, priority, match,
                                 rate, burst, dscp, may_exist, **columns)

    def qos_del(self, switch, direction=None, priority=None, match=None,
                if_exists=True):
        return cmd.QoSDelCommand(self, switch, direction, priority, match,
                                 if_exists)

    def qos_list(self, switch):
        return cmd.QoSListCommand(self, switch)

    def qos_del_ext_ids(self, lswitch_name, external_ids, if_exists=True):
        return cmd.QoSDelExtIdCommand(self, lswitch_name, external_ids,
                                      if_exists=if_exists)

    def lsp_add(self, switch, port, parent_name=None, tag=None,
                may_exist=False, **columns):
        return cmd.LspAddCommand(self, switch, port, parent_name, tag,
                                 may_exist, **columns)

    def lsp_del(self, port, switch=None, if_exists=False):
        return cmd.LspDelCommand(self, port, switch, if_exists)

    def lsp_list(self, switch=None):
        return cmd.LspListCommand(self, switch)

    def lsp_get(self, port):
        return cmd.LspGetCommand(self, port)

    def lsp_get_parent(self, port):
        return cmd.LspGetParentCommand(self, port)

    def lsp_get_tag(self, port):
        # NOTE (twilson) tag can be unassigned for a while after setting
        return cmd.LspGetTagCommand(self, port)

    def lsp_set_addresses(self, port, addresses):
        return cmd.LspSetAddressesCommand(self, port, addresses)

    def lsp_get_addresses(self, port):
        return cmd.LspGetAddressesCommand(self, port)

    def lsp_set_port_security(self, port, addresses):
        return cmd.LspSetPortSecurityCommand(self, port, addresses)

    def lsp_get_port_security(self, port):
        return cmd.LspGetPortSecurityCommand(self, port)

    def lsp_get_up(self, port):
        return cmd.LspGetUpCommand(self, port)

    def lsp_set_enabled(self, port, is_enabled):
        return cmd.LspSetEnabledCommand(self, port, is_enabled)

    def lsp_get_enabled(self, port):
        return cmd.LspGetEnabledCommand(self, port)

    def lsp_set_type(self, port, port_type):
        return cmd.LspSetTypeCommand(self, port, port_type)

    def lsp_get_type(self, port):
        return cmd.LspGetTypeCommand(self, port)

    def lsp_set_options(self, port, **options):
        return cmd.LspSetOptionsCommand(self, port, **options)

    def lsp_get_options(self, port):
        return cmd.LspGetOptionsCommand(self, port)

    def lsp_set_dhcpv4_options(self, port, dhcpopt_uuids):
        return cmd.LspSetDhcpV4OptionsCommand(self, port, dhcpopt_uuids)

    def lsp_get_dhcpv4_options(self, port):
        return cmd.LspGetDhcpV4OptionsCommand(self, port)

    def lr_add(self, router=None, may_exist=False, **columns):
        return cmd.LrAddCommand(self, router, may_exist, **columns)

    def lr_del(self, router, if_exists=False):
        return cmd.LrDelCommand(self, router, if_exists)

    def lr_list(self):
        return cmd.LrListCommand(self)

    def lr_get(self, router):
        return cmd.LrGetCommand(self, router)

    def lrp_add(self, router, port, mac, networks, peer=None, may_exist=False,
                **columns):
        return cmd.LrpAddCommand(self, router, port, mac, networks,
                                 peer, may_exist, **columns)

    def lrp_del(self, port, router=None, if_exists=False):
        return cmd.LrpDelCommand(self, port, router, if_exists)

    def lrp_list(self, router):
        return cmd.LrpListCommand(self, router)

    def lrp_set_enabled(self, port, is_enabled):
        return cmd.LrpSetEnabledCommand(self, port, is_enabled)

    def lrp_get_enabled(self, port):
        return cmd.LrpGetEnabledCommand(self, port)

    def lrp_set_options(self, port, **options):
        return cmd.LrpSetOptionsCommand(self, port, **options)

    def lrp_get_options(self, port):
        return cmd.LrpGetOptionsCommand(self, port)

    def lr_route_add(self, router, prefix, nexthop, port=None,
                     policy='dst-ip', may_exist=False):
        return cmd.LrRouteAddCommand(self, router, prefix, nexthop, port,
                                     policy, may_exist)

    def lr_route_del(self, router, prefix=None, if_exists=False):
        return cmd.LrRouteDelCommand(self, router, prefix, if_exists)

    def lr_route_list(self, router):
        return cmd.LrRouteListCommand(self, router)

    def lr_nat_add(self, router, nat_type, external_ip, logical_ip,
                   logical_port=None, external_mac=None, may_exist=False):
        return cmd.LrNatAddCommand(
            self, router, nat_type, external_ip, logical_ip, logical_port,
            external_mac, may_exist)

    def lr_nat_del(self, router, nat_type=None, match_ip=None,
                   if_exists=False):
        return cmd.LrNatDelCommand(self, router, nat_type, match_ip, if_exists)

    def lr_nat_list(self, router):
        return cmd.LrNatListCommand(self, router)

    def lb_add(self, lb, vip, ips, protocol=const.PROTO_TCP, may_exist=False,
               **columns):
        return cmd.LbAddCommand(self, lb, vip, ips, protocol, may_exist,
                                **columns)

    def lb_del(self, lb, vip=None, if_exists=False):
        return cmd.LbDelCommand(self, lb, vip, if_exists)

    def lb_list(self):
        return cmd.LbListCommand(self)

    def lr_lb_add(self, router, lb, may_exist=False):
        return cmd.LrLbAddCommand(self, router, lb, may_exist)

    def lr_lb_del(self, router, lb=None, if_exists=False):
        return cmd.LrLbDelCommand(self, router, lb, if_exists)

    def lr_lb_list(self, router):
        return cmd.LrLbListCommand(self, router)

    def ls_lb_add(self, switch, lb, may_exist=False):
        return cmd.LsLbAddCommand(self, switch, lb, may_exist)

    def ls_lb_del(self, switch, lb=None, if_exists=False):
        return cmd.LsLbDelCommand(self, switch, lb, if_exists)

    def ls_lb_list(self, switch):
        return cmd.LsLbListCommand(self, switch)

    def dhcp_options_add(self, cidr, **external_ids):
        return cmd.DhcpOptionsAddCommand(self, cidr, **external_ids)

    def dhcp_options_del(self, dhcpopt_uuid):
        return cmd.DhcpOptionsDelCommand(self, dhcpopt_uuid)

    def dhcp_options_list(self):
        return cmd.DhcpOptionsListCommand(self)

    def dhcp_options_get(self, dhcpopt_uuid):
        return cmd.DhcpOptionsGetCommand(self, dhcpopt_uuid)

    def dhcp_options_set_options(self, dhcpopt_uuid, **options):
        return cmd.DhcpOptionsSetOptionsCommand(self, dhcpopt_uuid, **options)

    def dhcp_options_get_options(self, dhcpopt_uuid):
        return cmd.DhcpOptionsGetOptionsCommand(self, dhcpopt_uuid)

    def dns_add(self, **columns):
        return cmd.DnsAddCommand(self, **columns)

    def dns_del(self, uuid):
        return cmd.DnsDelCommand(self, uuid)

    def dns_get(self, uuid):
        return cmd.DnsGetCommand(self, uuid)

    def dns_list(self):
        return cmd.DnsListCommand(self)

    def dns_set_records(self, uuid, **records):
        return cmd.DnsSetRecordsCommand(self, uuid, **records)

    def dns_add_record(self, uuid, hostname, ips):
        if isinstance(ips, list):
            ips = " ".join(utils.normalize_ip_port(ip) for ip in ips)
        return self.db_add('DNS', uuid, 'records', {hostname: ips})

    def dns_remove_record(self, uuid, hostname, if_exists=False):
        return self.db_remove('DNS', uuid, 'records', hostname,
                              if_exists=if_exists)

    def dns_set_external_ids(self, uuid, **external_ids):
        return cmd.DnsSetExternalIdsCommand(self, uuid, **external_ids)

    def pg_add(self, name=None, may_exist=False, **columns):
        return cmd.PgAddCommand(self, name, may_exist=may_exist, **columns)

    def pg_del(self, name, if_exists=False):
        return cmd.PgDelCommand(self, name, if_exists=if_exists)

    def pg_add_ports(self, pg_id, lsp):
        return cmd.PgAddPortCommand(self, pg_id, lsp=lsp)

    def pg_del_ports(self, pg_id, lsp, if_exists=False):
        return cmd.PgDelPortCommand(self, pg_id, lsp=lsp, if_exists=if_exists)

    def pg_get(self, pg):
        return cmd.PgGetCommand(self, pg)

    def ha_chassis_group_add(self, name, may_exist=False, **columns):
        return cmd.HAChassisGroupAddCommand(
            self, name, may_exist=may_exist, **columns)

    def ha_chassis_group_del(self, name, if_exists=False):
        return cmd.HAChassisGroupDelCommand(self, name, if_exists=if_exists)

    def ha_chassis_group_get(self, name):
        return cmd.HAChassisGroupGetCommand(self, name)

    def ha_chassis_group_add_chassis(self, hcg_id, chassis, priority,
                                     **columns):
        return cmd.HAChassisGroupAddChassisCommand(
            self, hcg_id, chassis, priority, **columns)

    def ha_chassis_group_del_chassis(self, hcg_id, chassis, if_exists=False):
        return cmd.HAChassisGroupDelChassisCommand(
            self, hcg_id, chassis, if_exists=if_exists)

    def meter_add(self, name, unit, rate=1, fair=False, burst_size=0,
                  action=None, may_exist=False, **columns):
        return cmd.MeterAddCommand(
            self, name, unit, rate=rate, fair=fair, burst_size=burst_size,
            action=action, may_exist=may_exist, **columns)

    def meter_del(self, meter, if_exists=False):
        return cmd.MeterDelCommand(self, meter, if_exists=if_exists)

    def meter_list(self):
        return cmd.MeterListCommand(self)

    def meter_get(self, meter):
        return cmd.MeterGetCommand(self, meter)
