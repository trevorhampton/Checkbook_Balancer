
#+--------------------------------------------------+
#|                  updateCheck.py                  |
#|                       v1.0                       |
#+--------------------------------------------------+
#| This module checks your program's version        |
#| against a file on the internet.                  |
#+--------------------------------------------------+
#|                      Usage                       |
#+--------------------------------------------------+
#| from updateCheck import Updater                  |
#|                                                  |
#| Updater(self, version, file, url[, silent=False])|
#|    version                                       |
#|        Your program's current version (float).   |
#|    file                                          |
#|        A URL for a file containing only a        |
#|        version number (float).                   |
#|    url                                           |
#|        A URL to a page with the latest version.  |
#|    silent=True                                   |
#|        The window will be shown only if an       |
#|        update is available.                      |
#+--------------------------------------------------+

import wx
import urllib
import base64
from webbrowser import open as openSite
from wx.lib.embeddedimage import PyEmbeddedImage

class Updater(wx.Frame):
	def __init__(self, parent, version, file, url, silent=False):
		updaterSize = (190, 130)
		wx.Frame.__init__(self, parent, -1, 'Updater', size=updaterSize, pos=(wx.GetDisplaySize()[0] / 2 - updaterSize[0] / 2, wx.GetDisplaySize()[1] / 2 - updaterSize[1] / 2), style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.FRAME_FLOAT_ON_PARENT)

		icon = PyEmbeddedImage(
			"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAABFFJ"
			"REFUWIXtlmtMW2Ucxp+eU4oFegltaUJvxjJBF4hiRMGlWzLZcGOMIINNVOY+bArOXRK3mTmy"
			"TAIJzkyNYraYBWFMhY6gwwW8EDK8bBgXXYaajUPhtIfRAoVzgEJL2+MHUgO0XKf7xPPtvM8/"
			"/+d33vNejkAgEAiwAr1bFylquhPxEQBkrnG9/mbeuGclfQQrAdjx+2/aO588YPY4/0oBAFH0"
			"Ix1rXpvMrX/sCdv/DvDplnrTe9KounByKkav1wMAaJqG2xfmONBv2flqW1HbcvqRywHIb377"
			"4KU/1DXRskiJTqcDSZIgCAJyuRxejyuyFUTBs2fiRzsvXL221J5LmoHy4syIpujmc4OdtS9o"
			"NBrI5fKQdSMjI2AYBsq1BRcznRl73/q4yXXPAJrcGw8pZHyDb7QnSa/XQywWL9hwYmICNE2D"
			"lDx4c4gV5DDm5O6F6omFzHLdtgwJ2dch9NxNMhqNi4YDgFgshtFohNBzN0lC9nWU67ZlLFQf"
			"cg1wqVqis+K549+P5J9TRssiNBoNSJJcNDwggiAgk8nA+zzin+Rxu54pIf2/9rE/lts4fm5t"
			"0CeoPPS09LOwH6pY6ptsrVYLqVS65OBQ4jgONpsNMuPWxsKpjbuLzlzj5gXoY+yPbj7ebcZk"
			"f4Jer0d4eHhQQ57nMd+ymc9zu92gaRp8eMztb8vicmI16j+DAI54RDlfFdRVSSJEUaGmnOd5"
			"2O12DA0NQalUQq1Wz/LtdjsGBwehUCigVquDQHw+HxiGwajLM7a9Nm93hcjTAAAEl6olMs6a"
			"yhrzq80xCllUYH/PlN/vB03TcLITI8q1BRdZlg16S5ZloUp8+YKTm3T29vbC5/PN8kmShE6n"
			"Q4xCFtWYX23OOGsq41K1BLHJ1FVnaSk+ZjAYoFKpgsinpqbQ3d0NN6Rd1z/fl5awo6E15PwD"
			"iH++vm3UF5viDVPfoigKbrd7li8QCKBSqWAwGGBpKT62ydRVR2w9n36e5+GfSwwALpcLFEVB"
			"GJ101Vy6IU1G9v09X3hAjDm5+wYTnxZp2NxIURQ4jguqmZycBA/SU9BWUUmcGGi/klx0+zDD"
			"MBgfH581pRaLBYrEPVW71iduStD7BhcLD0jYIh37rj0+Ny6r5hRNW/0DAwPg+ekdODw8DLvd"
			"4c+qyXpx//WSVgIAvkg/8WFs6tFKmqbhdrvhcDhgtdr8iYU/H2kv4fas5KqV/mLzNxVePpn9"
			"5Ut5jiF2zGazgWVZMAyDJw/1v3E6UmQGZpyE73RUHIzSrW+mKAoDTm4s78rRHPP2D04vN3iu"
			"KkSehvq91nUur7jHarXi4ezaU7WmA5UB/1+AdfV53leQtVOi39BcndtqKnX3fH2v4QElpe+/"
			"ealsY8rj+24dbiq8fHKmJ5z5MH1KxWx56r9KnqHpNVT6/tzxBS+j+6FVgFWAVYBVgFUA4eIl"
			"wfL7/bP+HQJj9w3A6/XCYrGEcETL7vUPqzHGHPy6TMAAAAAASUVORK5CYII=").GetIcon()

		self.url = url
		self.checkUpdate(version, file)

		if (not silent) or (silent and self.updaterMessage[0] != 'N'):
			updaterPanel = wx.Panel(self, -1)
			updaterText = wx.StaticText(updaterPanel, -1, self.updaterMessage, pos=(10, 10))
			updaterButton = wx.Button(updaterPanel, -1, 'Go to Site', pos=(100, 70))
			self.Bind(wx.EVT_BUTTON, self.updaterButtonEvent, updaterButton)
			self.SetIcon(icon)
			self.Show()
			
			self.GetParent().Disable()
			self.Bind(wx.EVT_CLOSE, self.onClose)

	def onClose(self, event):
		self.GetParent().Enable()
		self.Destroy()

	def checkUpdate(self, ver, file):
		try:
			html = urllib.urlopen(file)
			latest = float(html.readline())
		except (IOError, ValueError):
			self.updaterMessage = 'Can\'t retrieve update information.\n\nVersion: ' + str(ver)
		else:
			if ver != latest and ver < latest:
				self.updaterMessage = 'An update is available.\n\nVersion: ' + str(ver) + '\nLatest: ' + str(latest)
			else:
				self.updaterMessage = 'No updates available.\n\nVersion: ' + str(ver) + '\nLatest: ' + str(latest)
		finally:
			html.close()

	def updaterButtonEvent(self, event):
		openSite(self.url)
		self.Close()
