#!/c/Anaconda/envs/py3p7/python

import usb
import argparse
import sys


def find_device(vendor_id):
	print('search devices')
	buses = usb.busses()
	for bus in buses:
		for device in bus.devices:
			print('idVendor: %x' % device.idVendor)
			if device.idVendor == vendor_id:
				print('Found')
				return device
	return None


class VUsb:

	USB_VENDOR_ID = 0x16C0
	REQUEST_TYPE_I = usb.TYPE_VENDOR | usb.RECIP_DEVICE | usb.ENDPOINT_IN
	REQUEST_TYPE_O = usb.TYPE_VENDOR | usb.RECIP_DEVICE | usb.ENDPOINT_OUT
	USB_BUFFER_SIZE = 16

	def __init__(self):
		print('init class')
		device = find_device(self.USB_VENDOR_ID)
		print('Connect USB')
		if not device:
			raise Exception('Device not available')
		self.handle = device.open()

	def send_buffer_size(self, str_i):
		return self.send_cmd(self.REQUEST_TYPE_O, 4, str_i)

	def get_buffer_size(self):
		return self.send_cmd(self.REQUEST_TYPE_I, 2, self.USB_BUFFER_SIZE)

	def set_led_off(self):
		return self.send_cmd(self.REQUEST_TYPE_I, 0, self.USB_BUFFER_SIZE)

	def set_led_on(self):
		return self.send_cmd(self.REQUEST_TYPE_I, 1, self.USB_BUFFER_SIZE)

	def send_cmd(self, req_t, cmd, buf):
		val = self.handle.controlMsg(req_t, request=cmd, buffer=buf)
		return val


def main():
	print(sys.version)

	parser = argparse.ArgumentParser(description='AVR VUSB command line example.')
	parser.add_argument('-on', action='store_true', help='Turn on LED')
	parser.add_argument('-off', action='store_true', help='Turn off LED')
	parser.add_argument('-out', action='store_true', help='Print text from USB device')
	parser.add_argument('-wr_s', action='store_true', help='Write [Value, Index] to device')
	parser.add_argument('-in_s', action='store', type=str, help='Write String to device')

	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
		sys.exit(1)

	args = parser.parse_args()

	print('start')
	client = VUsb()

	if args.on:
		client.set_led_on()
	if args.off:
		client.set_led_off()
	if args.out:
		res = client.get_buffer_size()
		print("".join(chr(v) for v in res))
	if args.in_s:
		print(args.in_s)
		res = client.send_buffer_size(args.in_s)
		print(f'Sent bytes: {res}')


if __name__ == '__main__':
	main()
