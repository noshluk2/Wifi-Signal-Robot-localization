'''
This script conatins a class to add entries of
Access points details into an excel sheet

Usage :
-> To perform 3 readings appended into excel sheet

object_=Network_data_to_excel("luqman.xls")
object_.open_sheet()


object_.data_append()
object_.line_skip()
object_.data_append()

object_.line_skip(3)
object_.data_append()

object_.save_book()


'''
import subprocess
from xlwt import Workbook


class Network_data_to_excel:
  def __init__(self, file_name):
      self.ssid_command = "nmcli -t -f SSID device wifi"
      self.strength_command = "nmcli -t -f SIGNAL device wifi"
      self.mac_command = "nmcli -t -f BSSID device wifi"
      self.index=1
      self.file_name=file_name

  def open_sheet(self):
      self.excel_book = Workbook()
      self.sheet = self.excel_book.add_sheet('Sheet 1')
      self.sheet.write(0, 0, 'MAC')
      self.sheet.write(0, 1, 'SSID')
      self.sheet.write(0, 2, 'SIGNAL')


  def data_append(self):

      ssid_data   = self.command_data(self.ssid_command    ,0)
      mac_data    = self.command_data(self.mac_command     ,1)
      signal_data = self.command_data(self.strength_command,0)

      values_to_zip = zip(mac_data,ssid_data,signal_data)
      for mac,network_name,signal_strength in values_to_zip:
          self.sheet.write(self.index, 0, mac)
          self.sheet.write(self.index, 1, network_name)
          self.sheet.write(self.index, 2, signal_strength)
          self.index=self.index+1

  def command_data(self,command,replace):
      process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
      data, error = process.communicate()
      if (replace):
          data=data.replace (b'\:', b':')
      data=data.decode('utf-8').split('\n')
      return data

  def save_book(self):
      self.excel_book.save(self.file_name)

  def line_skip(self,lines=1):
      self.index=self.index + lines















