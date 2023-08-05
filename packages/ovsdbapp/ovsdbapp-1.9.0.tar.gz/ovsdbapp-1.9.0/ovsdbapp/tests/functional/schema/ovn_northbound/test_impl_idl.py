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

import netaddr
import testscenarios

from ovsdbapp.backend.ovs_idl import idlutils
from ovsdbapp import constants as const
from ovsdbapp.schema.ovn_northbound import impl_idl
from ovsdbapp.tests.functional import base
from ovsdbapp.tests.functional.schema.ovn_northbound import fixtures
from ovsdbapp.tests import utils
from ovsdbapp import utils as ovsdb_utils


class OvnNorthboundTest(base.FunctionalTestCase):
    schemas = ['OVN_Northbound']

    def setUp(self):
        super(OvnNorthboundTest, self).setUp()
        self.api = impl_idl.OvnNbApiIdlImpl(self.connection)


class TestLogicalSwitchOps(OvnNorthboundTest):
    def setUp(self):
        super(TestLogicalSwitchOps, self).setUp()
        self.table = self.api.tables['Logical_Switch']

    def _ls_add(self, *args, **kwargs):
        fix = self.useFixture(fixtures.LogicalSwitchFixture(self.api, *args,
                                                            **kwargs))
        self.assertIn(fix.obj.uuid, self.table.rows)
        return fix.obj

    def _test_ls_get(self, col):
        ls = self._ls_add(switch=utils.get_rand_device_name())
        val = getattr(ls, col)
        found = self.api.ls_get(val).execute(check_error=True)
        self.assertEqual(ls, found)

    def test_ls_get_uuid(self):
        self._test_ls_get('uuid')

    def test_ls_get_name(self):
        self._test_ls_get('name')

    def test_ls_add_no_name(self):
        self._ls_add()

    def test_ls_add_name(self):
        name = utils.get_rand_device_name()
        sw = self._ls_add(name)
        self.assertEqual(name, sw.name)

    def test_ls_add_exists(self):
        name = utils.get_rand_device_name()
        self._ls_add(name)
        cmd = self.api.ls_add(name)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_ls_add_may_exist(self):
        name = utils.get_rand_device_name()
        sw = self._ls_add(name)
        sw2 = self.api.ls_add(name, may_exist=True).execute(check_error=True)
        self.assertEqual(sw, sw2)

    def test_ls_add_columns(self):
        external_ids = {'mykey': 'myvalue', 'yourkey': 'yourvalue'}
        ls = self._ls_add(external_ids=external_ids)
        self.assertEqual(external_ids, ls.external_ids)

    def test_ls_del(self):
        sw = self._ls_add()
        self.api.ls_del(sw.uuid).execute(check_error=True)
        self.assertNotIn(sw.uuid, self.table.rows)

    def test_ls_del_by_name(self):
        name = utils.get_rand_device_name()
        self._ls_add(name)
        self.api.ls_del(name).execute(check_error=True)

    def test_ls_del_no_exist(self):
        name = utils.get_rand_device_name()
        cmd = self.api.ls_del(name)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_ls_del_if_exists(self):
        name = utils.get_rand_device_name()
        self.api.ls_del(name, if_exists=True).execute(check_error=True)

    def test_ls_list(self):
        switches = {self._ls_add() for _ in range(3)}
        switch_set = set(self.api.ls_list().execute(check_error=True))
        self.assertTrue(switches.issubset(switch_set))


class TestAclOps(OvnNorthboundTest):
    def setUp(self):
        super(TestAclOps, self).setUp()
        self.switch = self.useFixture(
            fixtures.LogicalSwitchFixture(self.api)).obj
        self.port_group = self.useFixture(
            fixtures.PortGroupFixture(self.api)).obj

    def _acl_add(self, entity, *args, **kwargs):
        self.assertIn(entity, ['lswitch', 'port_group'])
        if entity == 'lswitch':
            cmd = self.api.acl_add(self.switch.uuid, *args, **kwargs)
            resource = self.switch
        else:
            cmd = self.api.pg_acl_add(self.port_group.uuid, *args, **kwargs)
            resource = self.port_group

        aclrow = cmd.execute(check_error=True)
        self.assertIn(aclrow._row, resource.acls)
        self.assertEqual(cmd.direction, aclrow.direction)
        self.assertEqual(cmd.priority, aclrow.priority)
        self.assertEqual(cmd.match, aclrow.match)
        self.assertEqual(cmd.action, aclrow.action)
        return aclrow

    def test_acl_add(self):
        self._acl_add('lswitch', 'from-lport', 0,
                      'output == "fake_port" && ip', 'drop')

    def test_acl_add_exists(self):
        args = ('lswitch', 'from-lport', 0, 'output == "fake_port" && ip',
                'drop')
        self._acl_add(*args)
        self.assertRaises(RuntimeError, self._acl_add, *args)

    def test_acl_add_may_exist(self):
        args = ('from-lport', 0, 'output == "fake_port" && ip', 'drop')
        row = self._acl_add('lswitch', *args)
        row2 = self._acl_add('lswitch', *args, may_exist=True)
        self.assertEqual(row, row2)

    def test_acl_add_extids(self):
        external_ids = {'mykey': 'myvalue', 'yourkey': 'yourvalue'}
        acl = self._acl_add('lswitch',
                            'from-lport', 0, 'output == "fake_port" && ip',
                            'drop', **external_ids)
        self.assertEqual(external_ids, acl.external_ids)

    def test_acl_del_all(self):
        r1 = self._acl_add('lswitch', 'from-lport', 0, 'output == "fake_port"',
                           'drop')
        self.api.acl_del(self.switch.uuid).execute(check_error=True)
        self.assertNotIn(r1.uuid, self.api.tables['ACL'].rows)
        self.assertEqual([], self.switch.acls)

    def test_acl_del_direction(self):
        r1 = self._acl_add('lswitch', 'from-lport', 0,
                           'output == "fake_port"', 'drop')
        r2 = self._acl_add('lswitch', 'to-lport', 0,
                           'output == "fake_port"', 'allow')
        self.api.acl_del(self.switch.uuid, 'from-lport').execute(
            check_error=True)
        self.assertNotIn(r1, self.switch.acls)
        self.assertIn(r2, self.switch.acls)

    def test_acl_del_direction_priority_match(self):
        r1 = self._acl_add('lswitch', 'from-lport', 0,
                           'output == "fake_port"', 'drop')
        r2 = self._acl_add('lswitch', 'from-lport', 1,
                           'output == "fake_port"', 'allow')
        cmd = self.api.acl_del(self.switch.uuid,
                               'from-lport', 0, 'output == "fake_port"')
        cmd.execute(check_error=True)
        self.assertNotIn(r1, self.switch.acls)
        self.assertIn(r2, self.switch.acls)

    def test_acl_del_priority_without_match(self):
        self.assertRaises(TypeError, self.api.acl_del, self.switch.uuid,
                          'from-lport', 0)

    def test_acl_del_priority_without_direction(self):
        self.assertRaises(TypeError, self.api.acl_del, self.switch.uuid,
                          priority=0)

    def test_acl_list(self):
        r1 = self._acl_add('lswitch', 'from-lport', 0,
                           'output == "fake_port"', 'drop')
        r2 = self._acl_add('lswitch', 'from-lport', 1,
                           'output == "fake_port2"', 'allow')
        acls = self.api.acl_list(self.switch.uuid).execute(check_error=True)
        self.assertIn(r1, acls)
        self.assertIn(r2, acls)

    def test_pg_acl_add(self):
        self._acl_add('port_group', 'from-lport', 0,
                      'output == "fake_port" && ip', 'drop')

    def test_pg_acl_add_logging(self):
        r1 = self._acl_add('port_group', 'from-lport', 0,
                           'output == "fake_port" && ip', 'drop',
                           log=True, severity="warning", name="test1",
                           meter="meter1", extkey1="extval1")
        self.assertTrue(r1.log)
        self.assertEqual(["meter1"], r1.meter)
        self.assertEqual(["warning"], r1.severity)
        self.assertEqual(["test1"], r1.name)
        self.assertEqual({"extkey1": "extval1"}, r1.external_ids)

    def test_pg_acl_add_logging_weird_severity(self):
        r1 = self._acl_add('port_group', 'from-lport', 0,
                           'output == "fake_port" && ip', 'drop',
                           severity="weird")
        self.assertNotEqual(["weird"], r1.severity)
        self.assertEqual([], r1.severity)

    def test_pg_acl_del_all(self):
        r1 = self._acl_add('port_group', 'from-lport', 0,
                           'output == "fake_port"', 'drop')
        self.api.pg_acl_del(self.port_group.uuid).execute(check_error=True)
        self.assertNotIn(r1.uuid, self.api.tables['ACL'].rows)
        self.assertEqual([], self.port_group.acls)

    def test_pg_acl_list(self):
        r1 = self._acl_add('port_group', 'from-lport', 0,
                           'output == "fake_port"', 'drop')
        r2 = self._acl_add('port_group', 'from-lport', 1,
                           'output == "fake_port2"', 'allow')
        acls = self.api.pg_acl_list(self.port_group.uuid).execute(
            check_error=True)
        self.assertIn(r1, acls)
        self.assertIn(r2, acls)


class TestQoSOps(OvnNorthboundTest):
    def setUp(self):
        super(TestQoSOps, self).setUp()
        self.switch = self.useFixture(
            fixtures.LogicalSwitchFixture(self.api)).obj

    def _qos_add(self, *args, **kwargs):
        cmd = self.api.qos_add(self.switch.uuid, *args, **kwargs)
        row = cmd.execute(check_error=True)
        self.assertIn(row._row, self.switch.qos_rules)
        self.assertEqual(cmd.direction, row.direction)
        self.assertEqual(cmd.priority, row.priority)
        self.assertEqual(cmd.match, row.match)
        self.assertEqual(cmd.rate, row.bandwidth.get('rate', None))
        self.assertEqual(cmd.burst, row.bandwidth.get('burst', None))
        self.assertEqual(cmd.dscp, row.action.get('dscp', None))
        return row

    def test_qos_add_dscp(self):
        self._qos_add('from-lport', 0, 'output == "fake_port" && ip', dscp=33)

    def test_qos_add_rate(self):
        self._qos_add('from-lport', 0, 'output == "fake_port" && ip', rate=100)

    def test_qos_add_rate_burst(self):
        self._qos_add('from-lport', 0, 'output == "fake_port" && ip', rate=101,
                      burst=1001)

    def test_qos_add_rate_dscp(self):
        self._qos_add('from-lport', 0, 'output == "fake_port" && ip', rate=102,
                      burst=1002, dscp=56)

    def test_qos_add_raises(self):
        self.assertRaises(TypeError, self.api.qos_add, 'from-lport', 0,
                          'output == "fake_port" && ip')

    def test_qos_add_direction_raises(self):
        self.assertRaises(TypeError, self.api.qos_add, 'foo', 0, 'ip',
                          bandwidth={'rate': 102, 'burst': 1002})

    def test_qos_add_priority_raises(self):
        self.assertRaises(TypeError, self.api.qos_add, 'from-lport', 32768,
                          'ip', bandwidth={'rate': 102, 'burst': 1002})

    def test_qos_add_exists(self):
        args = ('from-lport', 0, 'output == "fake_port" && ip', 1000)
        self._qos_add(*args)
        self.assertRaises(RuntimeError, self._qos_add, *args)

    def test_qos_add_may_exist(self):
        args = ('from-lport', 0, 'output == "fake_port" && ip', 1000)
        row = self._qos_add(*args)
        row2 = self._qos_add(*args, may_exist=True)
        self.assertEqual(row, row2)

    def test_qos_add_extids(self):
        external_ids = {'mykey': 'myvalue', 'yourkey': 'yourvalue'}
        qos = self._qos_add('from-lport', 0, 'output == "fake_port" && ip',
                            dscp=11, external_ids=external_ids)
        self.assertEqual(external_ids, qos.external_ids)

    def test_qos_del_all(self):
        r1 = self._qos_add('from-lport', 0, 'output == "fake_port"', 1000)
        self.api.qos_del(self.switch.uuid).execute(check_error=True)
        self.assertNotIn(r1.uuid, self.api.tables['QoS'].rows)
        self.assertEqual([], self.switch.qos_rules)

    def test_qos_del_direction(self):
        r1 = self._qos_add('from-lport', 0, 'output == "fake_port"', 1000)
        r2 = self._qos_add('to-lport', 0, 'output == "fake_port"', 1000)
        self.api.qos_del(self.switch.uuid, 'from-lport').execute(
            check_error=True)
        self.assertNotIn(r1, self.switch.qos_rules)
        self.assertIn(r2, self.switch.qos_rules)

    def test_qos_del_direction_priority_match(self):
        r1 = self._qos_add('from-lport', 0, 'output == "fake_port"', 1000)
        r2 = self._qos_add('from-lport', 1, 'output == "fake_port"', 1000)
        cmd = self.api.qos_del(self.switch.uuid,
                               'from-lport', 0, 'output == "fake_port"')
        cmd.execute(check_error=True)
        self.assertNotIn(r1, self.switch.qos_rules)
        self.assertIn(r2, self.switch.qos_rules)

    def test_qos_del_priority_without_match(self):
        self.assertRaises(TypeError, self.api.qos_del, self.switch.uuid,
                          'from-lport', 0)

    def test_qos_del_priority_without_direction(self):
        self.assertRaises(TypeError, self.api.qos_del, self.switch.uuid,
                          priority=0)

    def test_qos_del_ls_not_present_if_exists_true(self):
        self.api.qos_del('some_other_ls').execute(check_error=True)

    def test_qos_del_ls_not_present_if_exists_false(self):
        cmd = self.api.qos_del('some_other_ls', if_exists=False)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_qos_list(self):
        r1 = self._qos_add('from-lport', 0, 'output == "fake_port"', 1000)
        r2 = self._qos_add('from-lport', 1, 'output == "fake_port2"', 1000)
        qos_rules = self.api.qos_list(self.switch.uuid).execute(
            check_error=True)
        self.assertIn(r1, qos_rules)
        self.assertIn(r2, qos_rules)

    def _create_fip_qoses(self):
        ext_ids_1 = {'key1': 'value1', 'key2': 'value2'}
        self.qos_1 = self._qos_add('from-lport', 0, 'output == "fake_port1"',
                                   dscp=11, external_ids=ext_ids_1)
        ext_ids_2 = {'key3': 'value3', 'key4': 'value4'}
        self.qos_2 = self._qos_add('from-lport', 1, 'output == "fake_port2"',
                                   dscp=11, external_ids=ext_ids_2)
        self.qos_3 = self._qos_add('from-lport', 2, 'output == "fake_port3"',
                                   dscp=10)

    def test_qos_delete_external_ids(self):
        self._create_fip_qoses()
        self.api.qos_del_ext_ids(self.switch.name,
                                 {'key1': 'value1'}).execute(check_error=True)
        qos_rules = self.api.qos_list(
            self.switch.uuid).execute(check_error=True)
        self.assertCountEqual([self.qos_2, self.qos_3], qos_rules)

        self.api.qos_del_ext_ids(
            self.switch.name,
            {'key3': 'value3', 'key4': 'value4'}).execute(check_error=True)
        qos_rules = self.api.qos_list(
            self.switch.uuid).execute(check_error=True)
        self.assertCountEqual([self.qos_3], qos_rules)

    def test_qos_delete_external_ids_wrong_keys_or_values(self):
        self._create_fip_qoses()
        self.api.qos_del_ext_ids(self.switch.name,
                                 {'key_z': 'value1'}).execute(check_error=True)
        qos_rules = self.api.qos_list(
            self.switch.uuid).execute(check_error=True)
        self.assertCountEqual([self.qos_1, self.qos_2, self.qos_3], qos_rules)

        self.api.qos_del_ext_ids(self.switch.name,
                                 {'key1': 'value_z'}).execute(check_error=True)
        qos_rules = self.api.qos_list(
            self.switch.uuid).execute(check_error=True)
        self.assertCountEqual([self.qos_1, self.qos_2, self.qos_3], qos_rules)

        self.api.qos_del_ext_ids(
            self.switch.name,
            {'key3': 'value3', 'key4': 'value_z'}).execute(check_error=True)
        qos_rules = self.api.qos_list(
            self.switch.uuid).execute(check_error=True)
        self.assertCountEqual([self.qos_1, self.qos_2, self.qos_3], qos_rules)

    def test_qos_delete_external_ids_empty_dict(self):
        self.assertRaises(TypeError, self.api.qos_del_ext_ids,
                          self.switch.name, {})

    def test_qos_delete_external_ids_if_exists(self):
        self._create_fip_qoses()
        cmd = self.api.qos_del_ext_ids('wrong_ls_name',
                                       {'key1': 'value1'}, if_exists=False)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

        self.api.qos_del_ext_ids('wrong_ls_name',
                                 {'key1': 'value1'}).execute(check_error=True)
        # No qos rule has been deleted from the correct logical switch.
        qos_rules = self.api.qos_list(
            self.switch.uuid).execute(check_error=True)
        self.assertCountEqual([self.qos_1, self.qos_2, self.qos_3], qos_rules)


class TestLspOps(OvnNorthboundTest):
    def setUp(self):
        super(TestLspOps, self).setUp()
        name = utils.get_rand_device_name()
        self.switch = self.useFixture(
            fixtures.LogicalSwitchFixture(self.api, name)).obj

    def _lsp_add(self, switch, name, *args, **kwargs):
        name = utils.get_rand_device_name() if name is None else name
        lsp = self.api.lsp_add(switch.uuid, name, *args, **kwargs).execute(
            check_error=True)
        self.assertIn(lsp, switch.ports)
        return lsp

    def _test_lsp_get(self, col):
        lsp = self._lsp_add(self.switch, None)
        val = getattr(lsp, col)
        found = self.api.lsp_get(val).execute(check_error=True)
        self.assertEqual(lsp, found)

    def test_lsp_get_uuid(self):
        self._test_lsp_get('uuid')

    def test_ls_get_name(self):
        self._test_lsp_get('name')

    def test_lsp_add(self):
        self._lsp_add(self.switch, None)

    def test_lsp_add_exists(self):
        lsp = self._lsp_add(self.switch, None)
        self.assertRaises(RuntimeError, self._lsp_add, self.switch,
                          lsp.name)

    def test_lsp_add_may_exist(self):
        lsp1 = self._lsp_add(self.switch, None)
        lsp2 = self._lsp_add(self.switch, lsp1.name, may_exist=True)
        self.assertEqual(lsp1, lsp2)

    def test_lsp_add_may_exist_wrong_switch(self):
        sw = self.useFixture(fixtures.LogicalSwitchFixture(self.api)).obj
        lsp = self._lsp_add(self.switch, None)
        self.assertRaises(RuntimeError, self._lsp_add, sw, lsp.name,
                          may_exist=True)

    def test_lsp_add_parent(self):
        lsp1 = self._lsp_add(self.switch, None)
        lsp2 = self._lsp_add(self.switch, None, parent_name=lsp1.name, tag=0)
        # parent_name, being optional, is stored as a list
        self.assertIn(lsp1.name, lsp2.parent_name)

    def test_lsp_add_parent_no_tag(self):
        self.assertRaises(TypeError, self._lsp_add, self.switch,
                          None, parent_name="fake_parent")

    def test_lsp_add_parent_may_exist(self):
        lsp1 = self._lsp_add(self.switch, None)
        lsp2 = self._lsp_add(self.switch, None, parent_name=lsp1.name, tag=0)
        lsp3 = self._lsp_add(self.switch, lsp2.name, parent_name=lsp1.name,
                             tag=0, may_exist=True)
        self.assertEqual(lsp2, lsp3)

    def test_lsp_add_parent_may_exist_no_parent(self):
        lsp1 = self._lsp_add(self.switch, None)
        self.assertRaises(RuntimeError, self._lsp_add, self.switch,
                          lsp1.name, parent_name="fake_parent", tag=0,
                          may_exist=True)

    def test_lsp_add_parent_may_exist_different_parent(self):
        lsp1 = self._lsp_add(self.switch, None)
        lsp2 = self._lsp_add(self.switch, None, parent_name=lsp1.name, tag=0)
        self.assertRaises(RuntimeError, self._lsp_add, self.switch,
                          lsp2.name, parent_name="fake_parent", tag=0,
                          may_exist=True)

    def test_lsp_add_parent_may_exist_different_tag(self):
        lsp1 = self._lsp_add(self.switch, None)
        lsp2 = self._lsp_add(self.switch, None, parent_name=lsp1.name, tag=0)
        self.assertRaises(RuntimeError, self._lsp_add, self.switch,
                          lsp2.name, parent_name=lsp1.name, tag=1,
                          may_exist=True)

    def test_lsp_add_may_exist_existing_parent(self):
        lsp1 = self._lsp_add(self.switch, None)
        lsp2 = self._lsp_add(self.switch, None, parent_name=lsp1.name, tag=0)
        self.assertRaises(RuntimeError, self._lsp_add, self.switch,
                          lsp2.name, may_exist=True)

    def test_lsp_add_columns(self):
        options = {'myside': 'yourside'}
        external_ids = {'myside': 'yourside'}
        lsp = self._lsp_add(self.switch, None, options=options,
                            external_ids=external_ids)
        self.assertEqual(options, lsp.options)
        self.assertEqual(external_ids, lsp.external_ids)

    def test_lsp_del_uuid(self):
        lsp = self._lsp_add(self.switch, None)
        self.api.lsp_del(lsp.uuid).execute(check_error=True)
        self.assertNotIn(lsp, self.switch.ports)

    def test_lsp_del_name(self):
        lsp = self._lsp_add(self.switch, None)
        self.api.lsp_del(lsp.name).execute(check_error=True)
        self.assertNotIn(lsp, self.switch.ports)

    def test_lsp_del_switch(self):
        lsp = self._lsp_add(self.switch, None)
        self.api.lsp_del(lsp.uuid, self.switch.uuid).execute(check_error=True)
        self.assertNotIn(lsp, self.switch.ports)

    def test_lsp_del_switch_name(self):
        lsp = self._lsp_add(self.switch, None)
        self.api.lsp_del(lsp.uuid,
                         self.switch.name).execute(check_error=True)
        self.assertNotIn(lsp, self.switch.ports)

    def test_lsp_del_wrong_switch(self):
        lsp = self._lsp_add(self.switch, None)
        sw = self.useFixture(fixtures.LogicalSwitchFixture(self.api)).obj
        cmd = self.api.lsp_del(lsp.uuid, sw.uuid)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_lsp_del_switch_no_exist(self):
        lsp = self._lsp_add(self.switch, None)
        cmd = self.api.lsp_del(lsp.uuid, utils.get_rand_device_name())
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_lsp_del_no_exist(self):
        cmd = self.api.lsp_del("fake_port")
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_lsp_del_if_exist(self):
        self.api.lsp_del("fake_port", if_exists=True).execute(check_error=True)

    def test_lsp_list(self):
        ports = {self._lsp_add(self.switch, None) for _ in range(3)}
        port_set = set(self.api.lsp_list(self.switch.uuid).execute(
            check_error=True))
        self.assertTrue(ports.issubset(port_set))

    def test_lsp_list_no_switch(self):
        ports = {self._lsp_add(self.switch, None) for _ in range(3)}
        other_switch = self.useFixture(fixtures.LogicalSwitchFixture(
            self.api, name=utils.get_rand_device_name())).obj
        other_port = self._lsp_add(other_switch, None)
        all_ports = set(self.api.lsp_list().execute(check_error=True))
        self.assertTrue((ports.union(set([other_port]))).issubset(all_ports))

    def test_lsp_get_parent(self):
        ls1 = self._lsp_add(self.switch, None)
        ls2 = self._lsp_add(self.switch, None, parent_name=ls1.name, tag=0)
        self.assertEqual(
            ls1.name, self.api.lsp_get_parent(ls2.name).execute(
                check_error=True))

    def test_lsp_get_tag(self):
        ls1 = self._lsp_add(self.switch, None)
        ls2 = self._lsp_add(self.switch, None, parent_name=ls1.name, tag=0)
        self.assertIsInstance(self.api.lsp_get_tag(ls2.uuid).execute(
            check_error=True), int)

    def test_lsp_set_addresses(self):
        lsp = self._lsp_add(self.switch, None)
        for addr in ('dynamic', 'unknown', 'router', 'de:ad:be:ef:4d:ad',
                     'de:ad:be:ef:4d:ad 192.0.2.1'):
            self.api.lsp_set_addresses(lsp.name, [addr]).execute(
                check_error=True)
            self.assertEqual([addr], lsp.addresses)

    def test_lsp_set_addresses_invalid(self):
        self.assertRaises(
            TypeError,
            self.api.lsp_set_addresses, 'fake', ['invalidaddress'])

    def test_lsp_get_addresses(self):
        addresses = [
            '01:02:03:04:05:06 192.0.2.1',
            'de:ad:be:ef:4d:ad 192.0.2.2']
        lsp = self._lsp_add(self.switch, None)
        self.api.lsp_set_addresses(
            lsp.name, addresses).execute(check_error=True)
        self.assertEqual(set(addresses), set(self.api.lsp_get_addresses(
            lsp.name).execute(check_error=True)))

    def test_lsp_get_set_port_security(self):
        port_security = [
            '01:02:03:04:05:06 192.0.2.1',
            'de:ad:be:ef:4d:ad 192.0.2.2']
        lsp = self._lsp_add(self.switch, None)
        self.api.lsp_set_port_security(lsp.name, port_security).execute(
            check_error=True)
        ps = self.api.lsp_get_port_security(lsp.name).execute(
            check_error=True)
        self.assertEqual(port_security, ps)

    def test_lsp_get_up(self):
        lsp = self._lsp_add(self.switch, None)
        self.assertFalse(self.api.lsp_get_up(lsp.name).execute(
            check_error=True))

    def test_lsp_get_set_enabled(self):
        lsp = self._lsp_add(self.switch, None)
        # default is True
        self.assertTrue(self.api.lsp_get_enabled(lsp.name).execute(
            check_error=True))
        self.api.lsp_set_enabled(lsp.name, False).execute(check_error=True)
        self.assertFalse(self.api.lsp_get_enabled(lsp.name).execute(
            check_error=True))
        self.api.lsp_set_enabled(lsp.name, True).execute(check_error=True)
        self.assertTrue(self.api.lsp_get_enabled(lsp.name).execute(
            check_error=True))

    def test_lsp_get_set_type(self):
        type_ = 'router'
        lsp = self._lsp_add(self.switch, None)
        self.api.lsp_set_type(lsp.uuid, type_).execute(check_error=True)
        self.assertEqual(type_, self.api.lsp_get_type(lsp.uuid).execute(
            check_error=True))

    def test_lsp_get_set_options(self):
        options = {'one': 'two', 'three': 'four'}
        lsp = self._lsp_add(self.switch, None)
        self.api.lsp_set_options(lsp.uuid, **options).execute(
            check_error=True)
        self.assertEqual(options, self.api.lsp_get_options(lsp.uuid).execute(
            check_error=True))

    def test_lsp_set_get_dhcpv4_options(self):
        lsp = self._lsp_add(self.switch, None)
        dhcpopt = self.useFixture(
            fixtures.DhcpOptionsFixture(self.api, '192.0.2.1/24')).obj
        self.api.lsp_set_dhcpv4_options(
            lsp.name, dhcpopt.uuid).execute(check_error=True)
        options = self.api.lsp_get_dhcpv4_options(
            lsp.uuid).execute(check_error=True)
        self.assertEqual(dhcpopt, options)


class TestDhcpOptionsOps(OvnNorthboundTest):
    def _dhcpopt_add(self, cidr, *args, **kwargs):
        dhcpopt = self.useFixture(fixtures.DhcpOptionsFixture(
            self.api, cidr, *args, **kwargs)).obj
        self.assertEqual(cidr, dhcpopt.cidr)
        return dhcpopt

    def test_dhcp_options_get(self):
        dhcpopt = self._dhcpopt_add('192.0.2.1/24')
        found = self.api.dhcp_options_get(dhcpopt.uuid).execute(
            check_error=True)
        self.assertEqual(dhcpopt, found)

    def test_dhcp_options_get_no_exist(self):
        cmd = self.api.dhcp_options_get("noexist")
        self.assertRaises(idlutils.RowNotFound, cmd.execute, check_error=True)

    def test_dhcp_options_add(self):
        self._dhcpopt_add('192.0.2.1/24')

    def test_dhcp_options_add_v6(self):
        self._dhcpopt_add('2001:db8::1/32')

    def test_dhcp_options_invalid_cidr(self):
        self.assertRaises(netaddr.AddrFormatError, self.api.dhcp_options_add,
                          '256.0.0.1/24')

    def test_dhcp_options_add_ext_ids(self):
        ext_ids = {'subnet-id': '1', 'other-id': '2'}
        dhcpopt = self._dhcpopt_add('192.0.2.1/24', **ext_ids)
        self.assertEqual(ext_ids, dhcpopt.external_ids)

    def test_dhcp_options_list(self):
        dhcpopts = {self._dhcpopt_add('192.0.2.1/24') for d in range(3)}
        dhcpopts_set = set(
            self.api.dhcp_options_list().execute(check_error=True))
        self.assertTrue(dhcpopts.issubset(dhcpopts_set))

    def test_dhcp_options_get_set_options(self):
        dhcpopt = self._dhcpopt_add('192.0.2.1/24')
        options = {'a': 'one', 'b': 'two'}
        self.api.dhcp_options_set_options(
            dhcpopt.uuid, **options).execute(check_error=True)
        cmd = self.api.dhcp_options_get_options(dhcpopt.uuid)
        self.assertEqual(options, cmd.execute(check_error=True))


class TestLogicalRouterOps(OvnNorthboundTest):
    def _lr_add(self, *args, **kwargs):
        lr = self.useFixture(
            fixtures.LogicalRouterFixture(self.api, *args, **kwargs)).obj
        self.assertIn(lr.uuid, self.api.tables['Logical_Router'].rows)
        return lr

    def test_lr_add(self):
        self._lr_add()

    def test_lr_add_name(self):
        name = utils.get_rand_device_name()
        lr = self._lr_add(name)
        self.assertEqual(name, lr.name)

    def test_lr_add_columns(self):
        external_ids = {'mykey': 'myvalue', 'yourkey': 'yourvalue'}
        lr = self._lr_add(external_ids=external_ids)
        self.assertEqual(external_ids, lr.external_ids)

    def test_lr_del(self):
        lr = self._lr_add()
        self.api.lr_del(lr.uuid).execute(check_error=True)
        self.assertNotIn(lr.uuid,
                         self.api.tables['Logical_Router'].rows.keys())

    def test_lr_del_name(self):
        lr = self._lr_add(utils.get_rand_device_name())
        self.api.lr_del(lr.name).execute(check_error=True)
        self.assertNotIn(lr.uuid,
                         self.api.tables['Logical_Router'].rows.keys())

    def test_lr_list(self):
        lrs = {self._lr_add() for _ in range(3)}
        lr_set = set(self.api.lr_list().execute(check_error=True))
        self.assertTrue(lrs.issubset(lr_set), "%s vs %s" % (lrs, lr_set))

    def _lr_add_route(self, router=None, prefix=None, nexthop=None, port=None,
                      **kwargs):
        lr = self._lr_add(router or utils.get_rand_device_name(),
                          may_exist=True)
        prefix = prefix or '192.0.2.0/25'
        nexthop = nexthop or '192.0.2.254'
        sr = self.api.lr_route_add(lr.uuid, prefix, nexthop, port,
                                   **kwargs).execute(check_error=True)
        self.assertIn(sr, lr.static_routes)
        self.assertEqual(prefix, sr.ip_prefix)
        self.assertEqual(nexthop, sr.nexthop)
        sr.router = lr
        return sr

    def test_lr_route_add(self):
        self._lr_add_route()

    def test_lr_route_add_invalid_prefix(self):
        self.assertRaises(netaddr.AddrFormatError, self._lr_add_route,
                          prefix='192.168.1.1/40')

    def test_lr_route_add_invalid_nexthop(self):
        self.assertRaises(netaddr.AddrFormatError, self._lr_add_route,
                          nexthop='256.0.1.3')

    def test_lr_route_add_exist(self):
        router_name = utils.get_rand_device_name()
        self._lr_add_route(router_name)
        self.assertRaises(RuntimeError, self._lr_add_route, router=router_name)

    def test_lr_route_add_may_exist(self):
        router_name = utils.get_rand_device_name()
        self._lr_add_route(router_name)
        self._lr_add_route(router_name, may_exist=True)

    def test_lr_route_del(self):
        prefix = "192.0.2.0/25"
        route = self._lr_add_route(prefix=prefix)
        self.api.lr_route_del(route.router.uuid, prefix).execute(
            check_error=True)
        self.assertNotIn(route, route.router.static_routes)

    def test_lr_route_del_all(self):
        router = self._lr_add()
        for p in range(3):
            self._lr_add_route(router.uuid, prefix="192.0.%s.0/24" % p)
        self.api.lr_route_del(router.uuid).execute(check_error=True)
        self.assertEqual([], router.static_routes)

    def test_lr_route_del_no_router(self):
        cmd = self.api.lr_route_del("fake_router", '192.0.2.0/25')
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_lr_route_del_no_exist(self):
        lr = self._lr_add()
        cmd = self.api.lr_route_del(lr.uuid, '192.0.2.0/25')
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_lr_route_del_if_exist(self):
        lr = self._lr_add()
        self.api.lr_route_del(lr.uuid, '192.0.2.0/25', if_exists=True).execute(
            check_error=True)

    def test_lr_route_list(self):
        lr = self._lr_add()
        routes = {self._lr_add_route(lr.uuid, prefix="192.0.%s.0/25" % p)
                  for p in range(3)}
        route_set = set(self.api.lr_route_list(lr.uuid).execute(
            check_error=True))
        self.assertTrue(routes.issubset(route_set))

    def _lr_nat_add(self, *args, **kwargs):
        lr = kwargs.pop('router', self._lr_add(utils.get_rand_device_name()))
        nat = self.api.lr_nat_add(
            lr.uuid, *args, **kwargs).execute(
            check_error=True)
        self.assertIn(nat, lr.nat)
        nat.router = lr
        return nat

    def test_lr_nat_add_dnat(self):
        ext, log = ('10.172.4.1', '192.0.2.1')
        nat = self._lr_nat_add(const.NAT_DNAT, ext, log)
        self.assertEqual(ext, nat.external_ip)
        self.assertEqual(log, nat.logical_ip)

    def test_lr_nat_add_snat(self):
        ext, log = ('10.172.4.1', '192.0.2.0/24')
        nat = self._lr_nat_add(const.NAT_SNAT, ext, log)
        self.assertEqual(ext, nat.external_ip)
        self.assertEqual(log, nat.logical_ip)

    def test_lr_nat_add_port(self):
        sw = self.useFixture(
            fixtures.LogicalSwitchFixture(self.api)).obj
        lsp = self.api.lsp_add(sw.uuid, utils.get_rand_device_name()).execute(
            check_error=True)
        lport, mac = (lsp.name, 'de:ad:be:ef:4d:ad')
        nat = self._lr_nat_add(const.NAT_BOTH, '10.172.4.1', '192.0.2.1',
                               lport, mac)
        self.assertIn(lport, nat.logical_port)  # because optional
        self.assertIn(mac, nat.external_mac)

    def test_lr_nat_add_port_no_mac(self):
        # yes, this and other TypeError tests are technically unit tests
        self.assertRaises(TypeError, self.api.lr_nat_add, 'faker',
                          const.NAT_DNAT, '10.17.4.1', '192.0.2.1', 'fake')

    def test_lr_nat_add_port_wrong_type(self):
        for nat_type in (const.NAT_DNAT, const.NAT_SNAT):
            self.assertRaises(
                TypeError, self.api.lr_nat_add, 'faker', nat_type,
                '10.17.4.1', '192.0.2.1', 'fake', 'de:ad:be:ef:4d:ad')

    def test_lr_nat_add_exists(self):
        args = (const.NAT_SNAT, '10.17.4.1', '192.0.2.0/24')
        nat1 = self._lr_nat_add(*args)
        cmd = self.api.lr_nat_add(nat1.router.uuid, *args)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_lr_nat_add_may_exist(self):
        sw = self.useFixture(
            fixtures.LogicalSwitchFixture(self.api)).obj
        lsp = self.api.lsp_add(sw.uuid, utils.get_rand_device_name()).execute(
            check_error=True)
        args = (const.NAT_BOTH, '10.17.4.1', '192.0.2.1')
        nat1 = self._lr_nat_add(*args)
        lp, mac = (lsp.name, 'de:ad:be:ef:4d:ad')
        nat2 = self.api.lr_nat_add(
            nat1.router.uuid, *args, logical_port=lp,
            external_mac=mac, may_exist=True).execute(check_error=True)
        self.assertEqual(nat1, nat2)
        self.assertIn(lp, nat2.logical_port)  # because optional
        self.assertIn(mac, nat2.external_mac)

    def test_lr_nat_add_may_exist_remove_port(self):
        sw = self.useFixture(
            fixtures.LogicalSwitchFixture(self.api)).obj
        lsp = self.api.lsp_add(sw.uuid, utils.get_rand_device_name()).execute(
            check_error=True)
        args = (const.NAT_BOTH, '10.17.4.1', '192.0.2.1')
        lp, mac = (lsp.name, 'de:ad:be:ef:4d:ad')
        nat1 = self._lr_nat_add(*args, logical_port=lp, external_mac=mac)
        nat2 = self.api.lr_nat_add(
            nat1.router.uuid, *args, may_exist=True).execute(check_error=True)
        self.assertEqual(nat1, nat2)
        self.assertEqual([], nat2.logical_port)  # because optional
        self.assertEqual([], nat2.external_mac)

    def _three_nats(self):
        lr = self._lr_add(utils.get_rand_device_name())
        for n, nat_type in enumerate((const.NAT_DNAT, const.NAT_SNAT,
                                     const.NAT_BOTH)):
            nat_kwargs = {'router': lr, 'nat_type': nat_type,
                          'logical_ip': '10.17.4.%s' % (n + 1),
                          'external_ip': '192.0.2.%s' % (n + 1)}
            self._lr_nat_add(**nat_kwargs)
        return lr

    def _lr_nat_del(self, *args, **kwargs):
        lr = self._three_nats()
        self.api.lr_nat_del(lr.name, *args, **kwargs).execute(check_error=True)
        return lr

    def test_lr_nat_del_all(self):
        lr = self._lr_nat_del()
        self.assertEqual([], lr.nat)

    def test_lr_nat_del_type(self):
        lr = self._lr_nat_del(nat_type=const.NAT_SNAT)
        types = tuple(nat.type for nat in lr.nat)
        self.assertNotIn(const.NAT_SNAT, types)
        self.assertEqual(len(types), len(const.NAT_TYPES) - 1)

    def test_lr_nat_del_specific_dnat(self):
        lr = self._lr_nat_del(nat_type=const.NAT_DNAT, match_ip='192.0.2.1')
        self.assertEqual(len(lr.nat), len(const.NAT_TYPES) - 1)
        for nat in lr.nat:
            self.assertNotEqual('192.0.2.1', nat.external_ip)
            self.assertNotEqual(const.NAT_DNAT, nat.type)

    def test_lr_nat_del_specific_snat(self):
        lr = self._lr_nat_del(nat_type=const.NAT_SNAT, match_ip='10.17.4.2')
        self.assertEqual(len(lr.nat), len(const.NAT_TYPES) - 1)
        for nat in lr.nat:
            self.assertNotEqual('10.17.4.2', nat.external_ip)
            self.assertNotEqual(const.NAT_SNAT, nat.type)

    def test_lr_nat_del_specific_both(self):
        lr = self._lr_nat_del(nat_type=const.NAT_BOTH, match_ip='192.0.2.3')
        self.assertEqual(len(lr.nat), len(const.NAT_TYPES) - 1)
        for nat in lr.nat:
            self.assertNotEqual('192.0.2.3', nat.external_ip)
            self.assertNotEqual(const.NAT_BOTH, nat.type)

    def test_lr_nat_del_specific_not_found(self):
        self.assertRaises(idlutils.RowNotFound, self._lr_nat_del,
                          nat_type=const.NAT_BOTH, match_ip='10.17.4.2')

    def test_lr_nat_del_specific_if_exists(self):
        lr = self._lr_nat_del(nat_type=const.NAT_BOTH, match_ip='10.17.4.2',
                              if_exists=True)
        self.assertEqual(len(lr.nat), len(const.NAT_TYPES))

    def test_lr_nat_del_specific_snat_ip_network(self):
        lr = self._lr_add(utils.get_rand_device_name())
        self._lr_nat_add(router=lr,
                         nat_type=const.NAT_SNAT,
                         logical_ip='10.17.4.0/24',
                         external_ip='192.0.2.2')
        # Attempt to delete NAT rule of type const.NAT_SNAT by passing
        # an IP network (corresponding to logical_ip) as match_ip
        self.api.lr_nat_del(lr.name,
                            nat_type=const.NAT_SNAT,
                            match_ip='10.17.4.0/24').execute(check_error=True)
        # Assert that the NAT rule of type const.NAT_SNAT is deleted
        self.assertEqual([], lr.nat)

    def test_lr_nat_del_specific_snat_ip_network_not_found(self):
        self.assertRaises(idlutils.RowNotFound, self._lr_nat_del,
                          nat_type=const.NAT_SNAT, match_ip='10.17.4.0/24')

    def test_lr_nat_del_specific_dnat_ip_network(self):
        self.assertRaises(ValueError, self._lr_nat_del,
                          nat_type=const.NAT_DNAT, match_ip='192.0.2.1/32')

    def test_lr_nat_del_specific_both_ip_network(self):
        self.assertRaises(ValueError, self._lr_nat_del,
                          nat_type=const.NAT_BOTH, match_ip='192.0.2.0/24')

    def test_lr_nat_list(self):
        lr = self._three_nats()
        nats = self.api.lr_nat_list(lr.uuid).execute(check_error=True)
        self.assertEqual(lr.nat, nats)


class TestLogicalRouterPortOps(OvnNorthboundTest):
    def setUp(self):
        super(TestLogicalRouterPortOps, self).setUp()
        self.lr = self.useFixture(fixtures.LogicalRouterFixture(self.api)).obj

    def _lrp_add(self, port, mac='de:ad:be:ef:4d:ad',
                 networks=None, *args, **kwargs):
        if port is None:
            port = utils.get_rand_device_name()
        if networks is None:
            networks = ['192.0.2.0/24']
        lrp = self.api.lrp_add(self.lr.uuid, port, mac, networks,
                               *args, **kwargs).execute(check_error=True)
        self.assertIn(lrp, self.lr.ports)
        self.assertEqual(mac, lrp.mac)
        self.assertEqual(set(networks), set(lrp.networks))
        return lrp

    def test_lrp_add(self):
        self._lrp_add(None, 'de:ad:be:ef:4d:ad', ['192.0.2.0/24'])

    def test_lpr_add_peer(self):
        lrp = self._lrp_add(None, 'de:ad:be:ef:4d:ad', ['192.0.2.0/24'],
                            peer='fake_peer')
        self.assertIn('fake_peer', lrp.peer)

    def test_lpr_add_multiple_networks(self):
        networks = ['192.0.2.0/24', '192.2.1.0/24']
        self._lrp_add(None, 'de:ad:be:ef:4d:ad', networks)

    def test_lrp_add_invalid_mac(self):
        self.assertRaises(
            netaddr.AddrFormatError,
            self.api.lrp_add, "fake", "fake", "000:11:22:33:44:55",
            ['192.0.2.0/24'])

    def test_lrp_add_invalid_network(self):
        self.assertRaises(
            netaddr.AddrFormatError,
            self.api.lrp_add, "fake", "fake", "01:02:03:04:05:06",
            ['256.2.0.1/24'])

    def test_lrp_add_exists(self):
        name = utils.get_rand_device_name()
        args = (name, 'de:ad:be:ef:4d:ad', ['192.0.2.0/24'])
        self._lrp_add(*args)
        self.assertRaises(RuntimeError, self._lrp_add, *args)

    def test_lrp_add_may_exist(self):
        name = utils.get_rand_device_name()
        args = (name, 'de:ad:be:ef:4d:ad', ['192.0.2.0/24'])
        self._lrp_add(*args)
        self.assertRaises(RuntimeError, self._lrp_add, *args, may_exist=True)

    def test_lrp_add_may_exist_different_router(self):
        name = utils.get_rand_device_name()
        args = (name, 'de:ad:be:ef:4d:ad', ['192.0.2.0/24'])
        lr2 = self.useFixture(fixtures.LogicalRouterFixture(self.api)).obj
        self._lrp_add(*args)
        cmd = self.api.lrp_add(lr2.uuid, *args, may_exist=True)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_lrp_add_may_exist_different_mac(self):
        name = utils.get_rand_device_name()
        args = {'port': name, 'mac': 'de:ad:be:ef:4d:ad',
                'networks': ['192.0.2.0/24']}
        self._lrp_add(**args)
        args['mac'] = 'da:d4:de:ad:be:ef'
        self.assertRaises(RuntimeError, self._lrp_add, may_exist=True, **args)

    def test_lrp_add_may_exist_different_networks(self):
        name = utils.get_rand_device_name()
        args = (name, 'de:ad:be:ef:4d:ad')
        self._lrp_add(*args, networks=['192.0.2.0/24'])
        self.assertRaises(RuntimeError, self._lrp_add, *args,
                          networks=['192.2.1.0/24'], may_exist=True)

    def test_lrp_add_may_exist_different_peer(self):
        name = utils.get_rand_device_name()
        args = (name, 'de:ad:be:ef:4d:ad', ['192.0.2.0/24'])
        self._lrp_add(*args)
        self.assertRaises(RuntimeError, self._lrp_add, *args,
                          peer='fake', may_exist=True)

    def test_lrp_add_columns(self):
        options = {'myside': 'yourside'}
        external_ids = {'myside': 'yourside'}
        lrp = self._lrp_add(None, options=options, external_ids=external_ids)
        self.assertEqual(options, lrp.options)
        self.assertEqual(external_ids, lrp.external_ids)

    def test_lrp_add_gw_chassis(self):
        name, c1, c2 = [utils.get_rand_device_name() for _ in range(3)]
        args = (name, 'de:ad:be:ef:4d:ad')
        lrp = self._lrp_add(*args, gateway_chassis=(c1, c2))
        c1 = self.api.lookup('Gateway_Chassis', "%s_%s" % (lrp.name, c1))
        c2 = self.api.lookup('Gateway_Chassis', "%s_%s" % (lrp.name, c2))
        self.assertIn(c1, lrp.gateway_chassis)
        self.assertIn(c2, lrp.gateway_chassis)

    def test_lrp_del_uuid(self):
        lrp = self._lrp_add(None)
        self.api.lrp_del(lrp.uuid).execute(check_error=True)
        self.assertNotIn(lrp, self.lr.ports)

    def test_lrp_del_name(self):
        lrp = self._lrp_add(None)
        self.api.lrp_del(lrp.name).execute(check_error=True)
        self.assertNotIn(lrp, self.lr.ports)

    def test_lrp_del_router(self):
        lrp = self._lrp_add(None)
        self.api.lrp_del(lrp.uuid, self.lr.uuid).execute(check_error=True)
        self.assertNotIn(lrp, self.lr.ports)

    def test_lrp_del_router_name(self):
        lrp = self._lrp_add(None)
        self.api.lrp_del(lrp.uuid,
                         self.lr.name).execute(check_error=True)
        self.assertNotIn(lrp, self.lr.ports)

    def test_lrp_del_wrong_router(self):
        lrp = self._lrp_add(None)
        sw = self.useFixture(fixtures.LogicalSwitchFixture(self.api)).obj
        cmd = self.api.lrp_del(lrp.uuid, sw.uuid)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_lrp_del_router_no_exist(self):
        lrp = self._lrp_add(None)
        cmd = self.api.lrp_del(lrp.uuid, utils.get_rand_device_name())
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_lrp_del_no_exist(self):
        cmd = self.api.lrp_del("fake_port")
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_lrp_del_if_exist(self):
        self.api.lrp_del("fake_port", if_exists=True).execute(check_error=True)

    def test_lrp_list(self):
        ports = {self._lrp_add(None) for _ in range(3)}
        port_set = set(self.api.lrp_list(self.lr.uuid).execute(
            check_error=True))
        self.assertTrue(ports.issubset(port_set))

    def test_lrp_get_set_enabled(self):
        lrp = self._lrp_add(None)
        # default is True
        self.assertTrue(self.api.lrp_get_enabled(lrp.name).execute(
            check_error=True))
        self.api.lrp_set_enabled(lrp.name, False).execute(check_error=True)
        self.assertFalse(self.api.lrp_get_enabled(lrp.name).execute(
            check_error=True))
        self.api.lrp_set_enabled(lrp.name, True).execute(check_error=True)
        self.assertTrue(self.api.lrp_get_enabled(lrp.name).execute(
            check_error=True))

    def test_lrp_get_set_options(self):
        options = {'one': 'two', 'three': 'four'}
        lrp = self._lrp_add(None)
        self.api.lrp_set_options(lrp.uuid, **options).execute(
            check_error=True)
        self.assertEqual(options, self.api.lrp_get_options(lrp.uuid).execute(
            check_error=True))


class TestLoadBalancerOps(OvnNorthboundTest):

    def _lb_add(self, lb, vip, ips, protocol=const.PROTO_TCP, may_exist=False,
                **columns):
        lbal = self.useFixture(fixtures.LoadBalancerFixture(
            self.api, lb, vip, ips, protocol, may_exist, **columns)).obj
        self.assertEqual(lb, lbal.name)
        norm_vip = ovsdb_utils.normalize_ip_port(vip)
        self.assertIn(norm_vip, lbal.vips)
        self.assertEqual(",".join(ovsdb_utils.normalize_ip(ip) for ip in ips),
                         lbal.vips[norm_vip])
        self.assertIn(protocol, lbal.protocol)  # because optional
        return lbal

    def test_lb_add(self):
        vip = '192.0.2.1'
        ips = ['10.0.0.1', '10.0.0.2', '10.0.0.3']
        self._lb_add(utils.get_rand_device_name(), vip, ips)

    def test_lb_add_port(self):
        vip = '192.0.2.1:80'
        ips = ['10.0.0.1', '10.0.0.2', '10.0.0.3']
        self._lb_add(utils.get_rand_device_name(), vip, ips)

    def test_lb_add_protocol(self):
        vip = '192.0.2.1'
        ips = ['10.0.0.1', '10.0.0.2', '10.0.0.3']
        self._lb_add(utils.get_rand_device_name(), vip, ips, const.PROTO_UDP)

    def test_lb_add_new_vip(self):
        name = utils.get_rand_device_name()
        lb1 = self._lb_add(name, '192.0.2.1', ['10.0.0.1', '10.0.0.2'])
        lb2 = self._lb_add(name, '192.0.2.2', ['10.1.0.1', '10.1.0.2'])
        self.assertEqual(lb1, lb2)
        self.assertEqual(2, len(lb1.vips))

    def test_lb_add_exists(self):
        name = utils.get_rand_device_name()
        vip = '192.0.2.1'
        ips = ['10.0.0.1', '10.0.0.2', '10.0.0.3']
        self._lb_add(name, vip, ips)
        cmd = self.api.lb_add(name, vip, ips)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_lb_add_may_exist(self):
        name = utils.get_rand_device_name()
        vip = '192.0.2.1'
        ips = ['10.0.0.1', '10.0.0.2', '10.0.0.3']
        lb1 = self._lb_add(name, vip, ips)
        ips += ['10.0.0.4']
        lb2 = self.api.lb_add(name, vip, ips, may_exist=True).execute(
            check_error=True)
        self.assertEqual(lb1, lb2)
        self.assertEqual(",".join(ips), lb1.vips[vip])

    def test_lb_add_columns(self):
        ext_ids = {'one': 'two'}
        name = utils.get_rand_device_name()
        lb = self._lb_add(name, '192.0.2.1', ['10.0.0.1', '10.0.0.2'],
                          external_ids=ext_ids)
        self.assertEqual(ext_ids, lb.external_ids)

    def test_lb_del(self):
        name = utils.get_rand_device_name()
        lb = self._lb_add(name, '192.0.2.1', ['10.0.0.1', '10.0.0.2']).uuid
        self.api.lb_del(lb).execute(check_error=True)
        self.assertNotIn(lb, self.api.tables['Load_Balancer'].rows)

    def test_lb_del_vip(self):
        name = utils.get_rand_device_name()
        lb1 = self._lb_add(name, '192.0.2.1', ['10.0.0.1', '10.0.0.2'])
        lb2 = self._lb_add(name, '192.0.2.2', ['10.1.0.1', '10.1.0.2'])
        self.assertEqual(lb1, lb2)
        self.api.lb_del(lb1.name, '192.0.2.1').execute(check_error=True)
        self.assertNotIn('192.0.2.1', lb1.vips)
        self.assertIn('192.0.2.2', lb1.vips)

    def test_lb_del_no_exist(self):
        cmd = self.api.lb_del(utils.get_rand_device_name())
        self.assertRaises(idlutils.RowNotFound, cmd.execute, check_error=True)

    def test_lb_del_if_exists(self):
        self.api.lb_del(utils.get_rand_device_name(), if_exists=True).execute(
            check_error=True)

    def test_lb_del_vip_if_exists(self):
        name = utils.get_rand_device_name()
        lb = self._lb_add(name, '192.0.2.1', ['10.0.0.1'])
        lb2 = self._lb_add(name, '192.0.2.2', ['10.1.0.1'])
        self.assertEqual(lb, lb2)
        # Remove vip that does not exist.
        self.api.lb_del(lb.name, '9.9.9.9', if_exists=True
                        ).execute(check_error=True)
        self.assertIn('192.0.2.1', lb.vips)
        self.assertIn('192.0.2.2', lb.vips)
        # Remove one vip.
        self.api.lb_del(lb.name, '192.0.2.1', if_exists=True
                        ).execute(check_error=True)
        self.assertNotIn('192.0.2.1', lb.vips)
        # Attempt to remove same vip a second time with if_exists=True.
        self.api.lb_del(lb.name, '192.0.2.1', if_exists=True).execute(
            check_error=True)
        # Attempt to remove same vip a third time with if_exists=False.
        cmd = self.api.lb_del(lb.name, '192.0.2.1', if_exists=False)
        self.assertRaises(idlutils.RowNotFound, cmd.execute, check_error=True)
        # Remove last vip and make sure that lb is also removed.
        self.assertIn('192.0.2.2', lb.vips)
        self.api.lb_del(lb.name, '192.0.2.2').execute(check_error=True)
        cmd = self.api.lb_del(lb.name)
        self.assertRaises(idlutils.RowNotFound, cmd.execute, check_error=True)

    def test_lb_list(self):
        lbs = {self._lb_add(utils.get_rand_device_name(), '192.0.2.1',
                            ['10.0.0.1', '10.0.0.2']) for _ in range(3)}
        lbset = self.api.lb_list().execute(check_error=True)
        self.assertTrue(lbs.issubset(lbset))


class TestObLbOps(testscenarios.TestWithScenarios, OvnNorthboundTest):
    scenarios = [
        ('LrLbOps', dict(fixture=fixtures.LogicalRouterFixture,
                         _add_fn='lr_lb_add', _del_fn='lr_lb_del',
                         _list_fn='lr_lb_list')),
        ('LsLbOps', dict(fixture=fixtures.LogicalSwitchFixture,
                         _add_fn='ls_lb_add', _del_fn='ls_lb_del',
                         _list_fn='ls_lb_list')),
    ]

    def setUp(self):
        super(TestObLbOps, self).setUp()
        self.add_fn = getattr(self.api, self._add_fn)
        self.del_fn = getattr(self.api, self._del_fn)
        self.list_fn = getattr(self.api, self._list_fn)
        # They must be in this order because the load balancer
        # can't be deleted when there is a reference in the router
        self.lb = self.useFixture(fixtures.LoadBalancerFixture(
            self.api, utils.get_rand_device_name(), '192.0.2.1',
            ['10.0.0.1', '10.0.0.2'])).obj
        self.lb2 = self.useFixture(fixtures.LoadBalancerFixture(
            self.api, utils.get_rand_device_name(), '192.0.2.2',
            ['10.1.0.1', '10.1.0.2'])).obj
        self.lr = self.useFixture(self.fixture(
            self.api, utils.get_rand_device_name())).obj

    def test_ob_lb_add(self):
        self.add_fn(self.lr.name, self.lb.name).execute(
            check_error=True)
        self.assertIn(self.lb, self.lr.load_balancer)

    def test_ob_lb_add_exists(self):
        cmd = self.add_fn(self.lr.name, self.lb.name)
        cmd.execute(check_error=True)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_ob_lb_add_may_exist(self):
        cmd = self.add_fn(self.lr.name, self.lb.name, may_exist=True)
        lb1 = cmd.execute(check_error=True)
        lb2 = cmd.execute(check_error=True)
        self.assertEqual(lb1, lb2)

    def test_ob_lb_del(self):
        self.add_fn(self.lr.name, self.lb.name).execute(
            check_error=True)
        self.assertIn(self.lb, self.lr.load_balancer)
        self.del_fn(self.lr.name).execute(check_error=True)
        self.assertEqual(0, len(self.lr.load_balancer))

    def test_ob_lb_del_lb(self):
        self.add_fn(self.lr.name, self.lb.name).execute(
            check_error=True)
        self.add_fn(self.lr.name, self.lb2.name).execute(
            check_error=True)
        self.del_fn(self.lr.name, self.lb2.name).execute(
            check_error=True)
        self.assertNotIn(self.lb2, self.lr.load_balancer)
        self.assertIn(self.lb, self.lr.load_balancer)

    def test_ob_lb_del_no_exist(self):
        cmd = self.del_fn(self.lr.name, 'fake')
        self.assertRaises(idlutils.RowNotFound, cmd.execute, check_error=True)

    def test_ob_lb_del_if_exists(self):
        self.del_fn(self.lr.name, 'fake', if_exists=True).execute(
            check_error=True)

    def test_ob_lb_list(self):
        self.add_fn(self.lr.name, self.lb.name).execute(
            check_error=True)
        self.add_fn(self.lr.name, self.lb2.name).execute(
            check_error=True)
        rows = self.list_fn(self.lr.name).execute(check_error=True)
        self.assertIn(self.lb, rows)
        self.assertIn(self.lb2, rows)


class TestCommonDbOps(OvnNorthboundTest):
    def setUp(self):
        super(TestCommonDbOps, self).setUp()
        name = utils.get_rand_device_name()
        self.switch = self.useFixture(
            fixtures.LogicalSwitchFixture(self.api, name)).obj
        self.lsps = [
            self.api.lsp_add(
                self.switch.uuid,
                utils.get_rand_device_name()).execute(check_error=True)
            for _ in range(3)]
        self.api.db_set('Logical_Switch', self.switch.uuid,
                        ('external_ids', {'one': '1', 'two': '2'})).execute(
                            check_error=True)

    def _ls_get_extids(self):
        return self.api.db_get('Logical_Switch', self.switch.uuid,
                               'external_ids').execute(check_error=True)

    def test_db_remove_map_key(self):
        ext_ids = self._ls_get_extids()
        removed = ext_ids.popitem()
        self.api.db_remove('Logical_Switch', self.switch.uuid,
                           'external_ids', removed[0]).execute(
            check_error=True)
        self.assertEqual(ext_ids, self.switch.external_ids)

    def test_db_remove_map_value(self):
        ext_ids = self._ls_get_extids()
        removed = dict([ext_ids.popitem()])
        self.api.db_remove('Logical_Switch', self.switch.uuid,
                           'external_ids', **removed).execute(
            check_error=True)
        self.assertEqual(ext_ids, self.switch.external_ids)

    def test_db_remove_map_bad_key(self):
        # should be a NoOp, not fail
        self.api.db_remove('Logical_Switch', self.switch.uuid,
                           'external_ids', "badkey").execute(check_error=True)

    def test_db_remove_map_bad_value(self):
        ext_ids = self._ls_get_extids()
        removed = {ext_ids.popitem()[0]: "badvalue"}
        # should be a NoOp, not fail
        self.api.db_remove('Logical_Switch', self.switch.uuid,
                           'external_ids', **removed).execute(check_error=True)

    def test_db_remove_value(self):
        ports = self.api.db_get('Logical_Switch', self.switch.uuid,
                                'ports').execute(check_error=True)
        removed = ports.pop()
        self.api.db_remove('Logical_Switch', self.switch.uuid, 'ports',
                           removed).execute(check_error=True)
        self.assertEqual(ports, [x.uuid for x in self.switch.ports])

    def test_db_remove_bad_value(self):
        # should be a NoOp, not fail
        self.api.db_remove('Logical_Switch', self.switch.uuid, 'ports',
                           "badvalue").execute(check_error=True)


class TestDnsOps(OvnNorthboundTest):
    def _dns_add(self, *args, **kwargs):
        dns = self.useFixture(
            fixtures.DnsFixture(self.api, *args, **kwargs)).obj
        return dns

    def test_dns_get(self):
        dns = self._dns_add()
        found = self.api.dns_get(dns.uuid).execute(
            check_error=True)
        self.assertEqual(dns, found)

    def test_dns_get_no_exist(self):
        cmd = self.api.dns_get("noexist")
        self.assertRaises(idlutils.RowNotFound, cmd.execute, check_error=True)

    def test_dns_add(self):
        self._dns_add()

    def test_dns_add_ext_ids(self):
        ext_ids = {'net-id': '1', 'other-id': '2'}
        dns = self._dns_add(external_ids=ext_ids)
        self.assertEqual(ext_ids, dns.external_ids)

    def test_dns_list(self):
        dnses = {self._dns_add() for d in range(3)}
        dnses_set = set(
            self.api.dns_list().execute(check_error=True))
        self.assertTrue(dnses.issubset(dnses_set))

    def test_dns_set_records(self):
        dns = self._dns_add()
        records = {'a': 'one', 'b': 'two'}
        self.api.dns_set_records(
            dns.uuid, **records).execute(check_error=True)
        dns = self.api.dns_get(dns.uuid).execute(
            check_error=True)
        self.assertEqual(records, dns.records)
        self.api.dns_set_records(
            dns.uuid, **{}).execute(check_error=True)
        self.assertEqual({}, dns.records)

    def test_dns_set_external_ids(self):
        dns = self._dns_add()
        external_ids = {'a': 'one', 'b': 'two'}
        self.api.dns_set_external_ids(
            dns.uuid, **external_ids).execute(check_error=True)
        dns = self.api.dns_get(dns.uuid).execute(
            check_error=True)
        self.assertEqual(external_ids, dns.external_ids)
        self.api.dns_set_external_ids(
            dns.uuid, **{}).execute(check_error=True)
        self.assertEqual({}, dns.external_ids)

    def test_dns_add_remove_records(self):
        dns = self._dns_add()
        self.api.dns_add_record(dns.uuid, 'a', 'one').execute()
        self.api.dns_add_record(dns.uuid, 'b', 'two').execute()
        dns = self.api.dns_get(dns.uuid).execute(
            check_error=True)
        records = {'a': 'one', 'b': 'two'}
        self.assertEqual(records, dns.records)
        self.api.dns_remove_record(dns.uuid, 'a').execute()
        records.pop('a')
        self.assertEqual(records, dns.records)
        self.api.dns_remove_record(dns.uuid, 'b').execute()
        self.assertEqual({}, dns.records)


class TestLsDnsOps(OvnNorthboundTest):
    def _dns_add(self, *args, **kwargs):
        dns = self.useFixture(
            fixtures.DnsFixture(self.api, *args, **kwargs)).obj
        return dns

    def _ls_add(self, *args, **kwargs):
        fix = self.useFixture(
            fixtures.LogicalSwitchFixture(self.api, *args, **kwargs))
        return fix.obj

    def test_ls_dns_set_clear_records(self):
        dns1 = self._dns_add()
        dns2 = self._dns_add()

        ls1 = self._ls_add('ls1')
        self.api.ls_set_dns_records(ls1.uuid, [dns1.uuid, dns2.uuid]).execute()
        self.assertCountEqual([dns1.uuid, dns2.uuid],
                              [dns.uuid for dns in ls1.dns_records])

        self.api.ls_clear_dns_records(ls1.uuid).execute()
        self.assertEqual([], ls1.dns_records)

    def test_ls_dns_add_remove_records(self):
        dns1 = self._dns_add()
        dns2 = self._dns_add()

        ls1 = self._ls_add('ls1')

        self.api.ls_add_dns_record(ls1.uuid, dns1.uuid).execute()
        self.assertCountEqual([dns1.uuid],
                              [dns.uuid for dns in ls1.dns_records])

        self.api.ls_add_dns_record(ls1.uuid, dns2.uuid).execute()
        self.assertCountEqual([dns1.uuid, dns2.uuid],
                              [dns.uuid for dns in ls1.dns_records])

        self.api.ls_remove_dns_record(ls1.uuid, dns2.uuid).execute()
        self.assertCountEqual([dns1.uuid],
                              [dns.uuid for dns in ls1.dns_records])
        self.api.ls_remove_dns_record(ls1.uuid, dns1.uuid).execute()
        self.assertEqual([], ls1.dns_records)


class TestPortGroup(OvnNorthboundTest):

    def setUp(self):
        super(TestPortGroup, self).setUp()
        self.switch = self.useFixture(
            fixtures.LogicalSwitchFixture(self.api)).obj
        self.pg_name = 'testpg-%s' % ovsdb_utils.generate_uuid()

    def test_port_group(self):
        # Assert the Port Group was added
        self.api.pg_add(self.pg_name).execute(check_error=True)
        row = self.api.db_find(
            'Port_Group',
            ('name', '=', self.pg_name)).execute(check_error=True)
        self.assertIsNotNone(row)
        self.assertEqual(self.pg_name, row[0]['name'])
        self.assertEqual([], row[0]['ports'])
        self.assertEqual([], row[0]['acls'])

        # Assert the Port Group was deleted
        self.api.pg_del(self.pg_name).execute(check_error=True)
        row = self.api.db_find(
            'Port_Group',
            ('name', '=', self.pg_name)).execute(check_error=True)
        self.assertEqual([], row)

    def test_port_group_ports(self):
        lsp_add_cmd = self.api.lsp_add(self.switch.uuid, 'testport')
        with self.api.transaction(check_error=True) as txn:
            txn.add(lsp_add_cmd)
            txn.add(self.api.pg_add(self.pg_name))

        port_uuid = lsp_add_cmd.result.uuid

        # Lets add the port using the UUID instead of a `Command` to
        # exercise the API
        self.api.pg_add_ports(self.pg_name, port_uuid).execute(
            check_error=True)
        row = self.api.db_find(
            'Port_Group',
            ('name', '=', self.pg_name)).execute(check_error=True)
        self.assertIsNotNone(row)
        self.assertEqual(self.pg_name, row[0]['name'])
        # Assert the port was added from the Port Group
        self.assertEqual([port_uuid], row[0]['ports'])

        # Delete the Port from the Port Group
        with self.api.transaction(check_error=True) as txn:
            txn.add(self.api.pg_del_ports(self.pg_name, port_uuid))

        row = self.api.db_find(
            'Port_Group',
            ('name', '=', self.pg_name)).execute(check_error=True)
        self.assertIsNotNone(row)
        self.assertEqual(self.pg_name, row[0]['name'])
        # Assert the port was removed from the Port Group
        self.assertEqual([], row[0]['ports'])

    def test_pg_del_ports_if_exists(self):
        self.api.pg_add(self.pg_name).execute(check_error=True)
        non_existent_res = ovsdb_utils.generate_uuid()

        # Assert that if if_exists is False (default) it will raise an error
        self.assertRaises(RuntimeError, self.api.pg_del_ports(self.pg_name,
                          non_existent_res).execute, True)

        # Assert that if if_exists is True it won't raise an error
        self.api.pg_del_ports(self.pg_name, non_existent_res,
                              if_exists=True).execute(check_error=True)


class TestHAChassisGroup(OvnNorthboundTest):

    def setUp(self):
        super(TestHAChassisGroup, self).setUp()
        self.hcg_name = 'ha-group-%s' % ovsdb_utils.generate_uuid()
        self.chassis = 'chassis-%s' % ovsdb_utils.generate_uuid()

    def test_ha_chassis_group(self):
        # Assert the HA Chassis Group was added
        self.api.ha_chassis_group_add(self.hcg_name).execute(check_error=True)
        hcg = self.api.ha_chassis_group_get(self.hcg_name).execute(
            check_error=True)
        self.assertEqual(self.hcg_name, hcg.name)

        # Assert the HA Chassis Group was deleted
        self.api.ha_chassis_group_del(self.hcg_name).execute(check_error=True)
        cmd = self.api.ha_chassis_group_get(self.hcg_name)
        self.assertRaises(idlutils.RowNotFound, cmd.execute, check_error=True)

    def test_ha_chassis_group_add_delete_chassis(self):
        self.api.ha_chassis_group_add(self.hcg_name).execute(check_error=True)
        priority = 20
        self.api.ha_chassis_group_add_chassis(
            self.hcg_name, self.chassis, priority).execute(check_error=True)

        # Assert that the HA Chassis entry was created
        row = self.api.db_find(
            'HA_Chassis',
            ('chassis_name', '=', self.chassis)).execute(check_error=True)
        self.assertEqual(priority, row[0]['priority'])

        # Assert that the HA Chassis entry was associated with
        # the HA Chassis Group
        hcg = self.api.ha_chassis_group_get(self.hcg_name).execute(
            check_error=True)
        self.assertEqual(self.chassis, hcg.ha_chassis[0].chassis_name)

        # Deletes the HA Chassis entry
        self.api.ha_chassis_group_del_chassis(
            self.hcg_name, self.chassis).execute(check_error=True)
        row = self.api.db_find(
            'HA_Chassis',
            ('chassis_name', '=', self.chassis)).execute(check_error=True)
        self.assertEqual([], row)

        # Assert that the deleted HA Chassis entry was dissociated from
        # the HA Chassis Group
        hcg = self.api.ha_chassis_group_get(self.hcg_name).execute(
            check_error=True)
        self.assertEqual([], hcg.ha_chassis)

    def test_ha_chassis_group_if_exists(self):
        self.api.ha_chassis_group_add(self.hcg_name).execute(check_error=True)
        self.api.ha_chassis_group_add_chassis(
            self.hcg_name, self.chassis, priority=10).execute(check_error=True)

        # Deletes the HA Chassis entry
        self.api.ha_chassis_group_del_chassis(
            self.hcg_name, self.chassis).execute(check_error=True)
        row = self.api.db_find(
            'HA_Chassis',
            ('chassis_name', '=', self.chassis)).execute(check_error=True)
        self.assertEqual([], row)

        # Tries to delete it again, since if_exists=True it shouldn't raise
        # any errors
        self.api.ha_chassis_group_del_chassis(
            self.hcg_name, self.chassis, if_exists=True).execute(
            check_error=True)

        # Tries to delete it again with if_exists=False, now it should raise
        # a RuntimeError
        cmd = self.api.ha_chassis_group_del_chassis(
            self.hcg_name, self.chassis, if_exists=False)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

        # Deletes the HA Chassis Group entry
        self.api.ha_chassis_group_del(self.hcg_name).execute(check_error=True)
        cmd = self.api.ha_chassis_group_get(self.hcg_name)
        self.assertRaises(idlutils.RowNotFound, cmd.execute, check_error=True)

        # Tries to delete it again, since if_exists=True it shouldn't raise
        # any errors
        self.api.ha_chassis_group_del(
            self.hcg_name, if_exists=True).execute(check_error=True)

        # Tries to delete it again with if_exists=False, now it should raise
        # a RuntimeError
        cmd = self.api.ha_chassis_group_del(self.hcg_name)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_ha_chassis_group_may_exist(self):
        cmd = self.api.ha_chassis_group_add(self.hcg_name, may_exist=True)
        hcg1 = cmd.execute(check_error=True)
        hcg2 = cmd.execute(check_error=True)
        self.assertEqual(hcg1, hcg2)


class TestReferencedObjects(OvnNorthboundTest):
    """Exercise adding a ls, lsp and lsp_address in a single transaction.

    The main goal of this test is to make sure a transaction can use either
    a name or an object notation in order to create an ls+lsp while in a
    transaction context.
    """
    def setUp(self):
        super(TestReferencedObjects, self).setUp()
        self.ls_name = utils.get_rand_device_name()
        self.lsp_name = utils.get_rand_device_name()
        self.lsp_test_addresses = ['de:ad:be:ef:4d:ad 192.0.2.1']

    def _check_values(self):
        # Check: Make sure ls_get and lsp_get work (no RowNotFound exception)
        self.api.ls_get(self.ls_name).execute(check_error=True)
        self.api.lsp_get(self.lsp_name).execute(check_error=True)
        self.assertEqual(self.lsp_test_addresses,
                         self.api.lsp_get_addresses(self.lsp_name).execute(
                             check_error=True))

    def test_lsp_add_by_name(self):
        with self.api.transaction(check_error=True) as txn:
            txn.add(self.api.ls_add(self.ls_name))
            txn.add(self.api.lsp_add(self.ls_name, self.lsp_name))
            txn.add(self.api.lsp_set_addresses(self.lsp_name,
                                               self.lsp_test_addresses))
        self._check_values()

    def test_lsp_add_by_object_via_db_create(self):
        with self.api.transaction(check_error=True) as txn:
            sw = txn.add(self.api.db_create_row('Logical_Switch',
                                                name=self.ls_name))
            prt = txn.add(self.api.db_create_row('Logical_Switch_Port',
                                                 name=self.lsp_name))
            txn.add(self.api.db_add('Logical_Switch', sw, "ports", prt))
            txn.add(self.api.db_add('Logical_Switch_Port', prt,
                                    "addresses", self.lsp_test_addresses[0]))
        self._check_values()


class TestMeterOps(OvnNorthboundTest):

    def setUp(self):
        super(TestMeterOps, self).setUp()
        self.table = self.api.tables['Meter']

    def _meter_add(self, name=None, unit=None, rate=1, fair=False,
                   burst_size=0, action=None, may_exist=False, **columns):
        if name is None:
            name = utils.get_rand_name()
        if unit is None:
            unit = 'pktps'
        # NOTE(flaviof): action drop is the only one option in the schema when
        #                this test was implemented. That is expected to be
        #                properly handled by api.
        exp_action = 'drop' if action is None else action
        meter = self.useFixture(fixtures.MeterFixture(
            self.api, name, unit, rate, fair, burst_size, action, may_exist,
            **columns)).obj
        meter_band = meter.bands[0]
        self.assertEqual(name, meter.name)
        self.assertEqual(unit, meter.unit)
        self.assertEqual([fair], meter.fair)
        self.assertEqual(exp_action, meter_band.action)
        self.assertEqual(rate, meter_band.rate)
        self.assertEqual(burst_size, meter_band.burst_size)
        return meter

    def _meter_del(self, row, col):
        name404 = utils.get_rand_name()
        self.api.meter_del(name404, if_exists=True).execute(check_error=True)
        self.assertIn(row.uuid, self.table.rows)
        self.api.meter_del(row.uuid).execute(check_error=True)
        self.assertNotIn(row.uuid, self.table.rows)
        self.api.meter_del(col, if_exists=True).execute(check_error=True)
        cmd = self.api.meter_del(col)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def _meter_get(self, col):
        meter = self._meter_add()
        val = getattr(meter, col)
        found = self.api.meter_get(val).execute(check_error=True)
        self.assertEqual(meter, found)

    def test_meter_add_non_defaults(self):
        self._meter_add(utils.get_rand_name(), "kbps", 321, True, 500, None)

    def test_meter_add_ext_ids(self):
        ext_ids = {
            utils.get_rand_name(prefix="random_"): utils.get_random_string(10)
            for _ in range(3)}
        meter = self._meter_add(external_ids=ext_ids)
        self.assertEqual(ext_ids, meter.external_ids)

    def test_meter_add_may_exist(self):
        cmd = self.api.meter_add("same_name", "kbps", may_exist=True)
        m1 = cmd.execute(check_error=True)
        m2 = cmd.execute(check_error=True)
        self.assertEqual(m1, m2)

    def test_meter_add_duplicate(self):
        cmd = self.api.meter_add("same_name", "kbps", may_exist=False)
        cmd.execute(check_error=True)
        self.assertRaises(RuntimeError, cmd.execute, check_error=True)

    def test_meter_del_by_uuid(self):
        meter = self._meter_add()
        self._meter_del(meter, meter.uuid)

    def test_meter_del_by_name(self):
        name = utils.get_rand_name()
        meter = self._meter_add(name)
        self._meter_del(meter, name)

    def test_meter_list(self):
        meters = {self._meter_add() for _ in range(3)}
        meter_set = set(self.api.meter_list().execute(check_error=True))
        self.assertTrue(meters.issubset(meter_set))

    def test_meter_get_uuid(self):
        self._meter_get('uuid')

    def test_meter_get_name(self):
        self._meter_get('name')
