from Kalman import KalmanAngle
import smbus
import time
import math


class angleOmeter(object):
	def __init__(self):
		self.kalmanX = KalmanAngle()
		self.kalmanY = KalmanAngle()
		self.Restrictedpitch = True
		self.radToDeg = 57.2957786
		self.kalAngleX = 0
		self.kalAngleY = 0
		self.ACCEL_XOUT_H = 0x3B
		self.ACCEL_YOUT_H = 0x3D
		self.ACCEL_YOUT_H = 0x3F
		self.bus = smbus.SMBus(1)
		self.DeviceAddress = 0x68
		self.MPU_Init()

		time.sleep(1)
		self.accX = self.read_raw_data(self.ACCEL_XOUT_H)
		self.accY = self.read_raw_data(self.ACCEL_YOUT_H)
		self.accZ = self.read_raw_data(self.ACCEL_YOUT_H)
		if (self.Restrictedpitch):
			self.roll = math.atan2(self.accY,self.accZ) * self.radToDeg
			self.pitch = math.atan(-self.accX/math.sqrt((self.accY**2)+(self.accZ**2))) * self.radToDeg
		else:
			self.roll = math.atan(self.accY/math.sqrt((self.accX**2)+(self.accZ**2))) * self.radToDeg
			self.pitch = math.atan2(-self.accX,self.accZ) * self.radToDeg
		print(self.roll)
		self.kalmanX.setAngle(self.roll)
		self.kalmanY.setAngle(self.pitch)
		self.gyroXAngle = self.roll;
		self.gyroYAngle = self.pitch;
		self.compAngleX = self.roll;
		self.compAngleY = self.pitch;

		self.timer = time.time()

	def MPU_Init(self):
		self.bus.write_byte_data(self.DeviceAddress, 0x19, 7)
		self.bus.write_byte_data(self.DeviceAddress, 0x6B, 1)
		self.bus.write_byte_data(self.DeviceAddress, 0x1A, int('0000110',2))
		self.bus.write_byte_data(self.DeviceAddress, 0x1B, 24)
		self.bus.write_byte_data(self.DeviceAddress, 0x38, 1)


	def read_raw_data(self,addr):
			high = self.bus.read_byte_data(self.DeviceAddress, addr)
			low = self.bus.read_byte_data(self.DeviceAddress, addr+1)
			value = ((high << 8) | low)
			if(value > 32768):
					value = value - 65536
			return value

	def get_angle(self):
		self.accX = self.read_raw_data(self.ACCEL_XOUT_H)
		self.accY = self.read_raw_data(self.ACCEL_YOUT_H)
		self.accZ = self.read_raw_data(self.ACCEL_YOUT_H)
		self.gyroX = self.read_raw_data(0x43)
		self.gyroY = self.read_raw_data(0x45)
		self.gyroZ = self.read_raw_data(0x47)
		dt = time.time() - self.timer
		self.timer = time.time()

		if (self.Restrictedpitch):
			self.roll = math.atan2(self.accY,self.accZ) * self.radToDeg
			self.pitch = math.atan(-self.accX/math.sqrt((self.accY**2)+(self.accZ**2))) * self.radToDeg
		else:
			self.roll = math.atan(self.accY/math.sqrt((self.accX**2)+(self.accZ**2))) * self.radToDeg
			self.pitch = math.atan2(-self.accX,self.accZ) * self.radToDeg
		self.gyroXRate = self.gyroX/131
		self.gyroYRate = self.gyroY/131

		if (self.Restrictedpitch):
			if((self.roll < -90 and self.kalAngleX >90) or (self.roll > 90 and self.kalAngleX < -90)):
				self.kalmanX.setAngle(self.roll)
				self.complAngleX = self.roll
				self.kalAngleX   = self.roll
				self.gyroXAngle  = self.roll
			else:
				self.kalAngleX = self.kalmanX.getAngle(self.roll,self.gyroXRate,dt)

			if(abs(self.kalAngleX)>90):
				self.gyroYRate  = -self.gyroYRate
				self.kalAngleY  = self.kalmanY.getAngle(self.pitch,self.gyroYRate,dt)
		else:
			if((self.pitch < -90 and self.kalAngleY >90) or (self.pitch > 90 and self.kalAngleY < -90)):

				self.kalmanY.setAngle(self.pitch)

				complAngleY = self.pitch

				self.kalAngleY   = self.pitch

				self.gyroYAngle  = self.pitch

			else:

				self.kalAngleY = self.kalmanY.getAngle(self.pitch,self.gyroYRate,dt)


			if(abs(self.kalAngleY)>90):

				self.gyroXRate  = -self.gyroXRate

				self.kalAngleX = self.kalmanX.getAngle(self.roll,self.gyroXRate,dt)


		self.gyroXAngle = self.gyroXRate * dt

		self.gyroYAngle = self.gyroYAngle * dt


		self.compAngleX = 0.93 * (self.compAngleX + self.gyroXRate * dt) + 0.07 * self.roll

		self.compAngleY = 0.93 * (self.compAngleY + self.gyroYRate * dt) + 0.07 * self.pitch


		if ((self.gyroXAngle < -180) or (self.gyroXAngle > 180)):

			self.gyroXAngle = self.kalAngleX

		if ((self.gyroYAngle < -180) or (self.gyroYAngle > 180)):

			self.gyroYAngle = self.kalAngleY



		print("Angle X: " + str(self.kalAngleX)+"   " +"Angle Y: " + str(self.kalAngleY))













