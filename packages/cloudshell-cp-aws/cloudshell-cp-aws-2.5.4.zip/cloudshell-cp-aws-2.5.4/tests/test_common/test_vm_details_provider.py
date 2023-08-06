from unittest import TestCase
from mock import Mock

from cloudshell.cp.aws.domain.common.vm_details_provider import VmDetailsProvider


class TestVmDetailsProvider(TestCase):

    def setUp(self):
        self.vm_details_provider = VmDetailsProvider()

    def test_prepare_vm_details(self):
        instance = Mock()
        instance.image_id = 'image_id'
        instance.instance_type = 'instance_type'
        instance.platform = 'instance_platform'
        instance.network_interfaces = []
        instance.volumes.all = lambda: []
        instance.iam_instance_profile = {"Arn": "arn:aws:iam::admin_role"}

        vm_instance_data = self.vm_details_provider.create(instance).vmInstanceData

        self.assertTrue(self._get_value(vm_instance_data, 'AMI ID') == instance.image_id)
        self.assertTrue(self._get_value(vm_instance_data, 'instance type') == instance.instance_type)
        self.assertTrue(self._get_value(vm_instance_data, 'platform') == instance.platform)
        self.assertTrue(self._get_value(vm_instance_data, 'IAM Role') == instance.iam_instance_profile['Arn'])

    def test_prepare_network_interface_objects_with_elastic_ip(self):
        # elastic_ip
        network_interface = Mock()
        network_interface.association_attribute = {'IpOwnerId': '9929230',
                                                   'PublicIp': 'public_ip'}

        network_interface.network_interface_id = 'interface_id'
        network_interface.mac_address = 'mac_address'
        network_interface.subnet_id = 'subnet_id'
        network_interface.attachment = {'DeviceIndex': 0}
        network_interface.private_ip_address = 'private_ip'

        instance = Mock()
        instance.network_interfaces = [
            network_interface
        ]

        network_interface_objects = self.vm_details_provider._get_vm_network_data(instance)

        nio = network_interface_objects[0]

        self.assertTrue(nio.interfaceId == 'interface_id')
        self.assertTrue(nio.networkId == 'subnet_id')
        self.assertTrue(nio.isPrimary == True)
        nio_data = nio.networkData
        self.assertTrue(self._get_value(nio_data, 'MAC Address') == 'mac_address')
        self.assertTrue(self._get_value(nio_data, 'Elastic IP') == True)
        self.assertTrue(self._get_value(nio_data, 'IP') == 'private_ip')
        self.assertTrue(self._get_value(nio_data, 'Public IP') == 'public_ip')

    def test_prepare_network_interface_objects_with_public_ip(self):
        network_interface = Mock()
        network_interface.association_attribute = dict()

        network_interface.network_interface_id = 'interface_id'
        network_interface.mac_address = 'mac_address'
        network_interface.subnet_id = 'subnet_id'
        network_interface.attachment = {'DeviceIndex': 0}
        network_interface.private_ip_address = 'private_ip'

        instance = Mock()
        instance.public_ip_address = 'public_ip'
        instance.network_interfaces = [
            network_interface
        ]

        network_interface_objects = self.vm_details_provider._get_vm_network_data(instance)

        nio = network_interface_objects[0]

        self.assertTrue(nio.interfaceId == 'interface_id')
        self.assertTrue(nio.networkId == 'subnet_id')
        self.assertTrue(nio.isPrimary == True)
        nio_data = nio.networkData

        self.assertTrue(self._get_value(nio_data, 'MAC Address') == 'mac_address')
        self.assertTrue(self._get_value(nio_data, 'Elastic IP') == False)
        self.assertTrue(self._get_value(nio_data, 'IP') == 'private_ip')
        self.assertTrue(self._get_value(nio_data, 'Public IP') == '')

    def test_prepare_network_interface_objects_without_public_ip(self):
        network_interface = Mock()
        network_interface.association_attribute = dict()

        network_interface.network_interface_id = 'interface_id'
        network_interface.mac_address = 'mac_address'
        network_interface.subnet_id = 'subnet_id'
        network_interface.attachment = {'DeviceIndex': 1}
        network_interface.private_ip_address = 'private_ip'

        instance = Mock()
        instance.network_interfaces = [
            network_interface
        ]

        network_interface_objects = self.vm_details_provider._get_vm_network_data(instance)

        nio = network_interface_objects[0]

        self.assertTrue(nio.interfaceId == 'interface_id')
        self.assertTrue(nio.networkId == 'subnet_id')
        self.assertTrue(nio.isPrimary == False)
        nio_data = nio.networkData

        self.assertTrue(self._get_value(nio_data, 'MAC Address') == 'mac_address')
        self.assertTrue(self._get_value(nio_data, 'Elastic IP') == False)
        self.assertTrue(self._get_value(nio_data, 'IP') == 'private_ip')
        self.assertTrue(self._get_value(nio_data, 'Public IP') == "")

    def _get_value(self, data, key):
        for item in data:
            if item.key == key:
                return item.value
        return None
