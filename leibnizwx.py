import leibniz
import wx
from wx.html import HtmlEasyPrinting

class Printer(HtmlEasyPrinting):
    def __init__(self):
        HtmlEasyPrinting.__init__(self)

    def GetHtmlText(self,text):
        "Simple conversion of text.  Use a more powerful version"
        html_text = text.replace('\n\n','<P>')
        html_text = text.replace('\n', '<BR>')
        return html_text

    def Print(self, text, doc_name):
        self.SetHeader(doc_name)
        self.PrintText(self.GetHtmlText(text),doc_name)

    def PreviewText(self, text, doc_name):
        self.SetHeader(doc_name)
        HtmlEasyPrinting.PreviewText(self, self.GetHtmlText(text))

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500,350))
        
        # crypto object
        self.leb = leibniz()

		# status bar and menu
        self.CreateStatusBar()
        self.setup_menu()

        # message text fields
        self.decrypted = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.encrypted = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        # encrypt/decrypt buttons
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        self.buttons.append(wx.Button(self, -1, u"Encrypt \u2193"))
        self.buttons.append(wx.Button(self, -1, u"Decrypt \u2191"))
        self.sizer2.Add(self.buttons[0], 1, wx.EXPAND)
        self.sizer2.Add(self.buttons[1], 1, wx.EXPAND)
        
        self.Bind(wx.EVT_BUTTON, self.OnEncrypt, self.buttons[0])
        self.Bind(wx.EVT_BUTTON, self.OnDecrypt, self.buttons[1])

        # vertical sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.decrypted, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)
        self.sizer.Add(self.encrypted, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        
        self.Show(True)

    def Print(self,e):
    	printer = Printer()
    	text = "<strong>Alphabets</strong>:\n"
    	i = 0
    	for a in self.leb.alphabets:
    		i = i + 1
    		text += "%d. %s\n" % (i, a)
    	text += "\n<strong>Leibniz Gear</strong>:\n"
    	text += self.leb.gear
    	text += "\n\n<strong>Decrypted Message</strong>:\n"
    	text += self.decrypted.GetValue().encode('ascii','ignore')
    	text += "\n\n<strong>Encrypted Message</strong>:\n"
    	text += self.encrypted.GetValue().encode('ascii','ignore')
    	printer.PreviewText(text,"Leibniz Encryption")

    def OnEncrypt(self,e):
    	#self.encrypted.SetValue(self.leb.encrypt(self.decrypted.GetValue()))
    	message = self.decrypted.GetValue().encode('ascii','ignore')
    	self.encrypted.SetValue(self.leb.encrypt(message))

    def OnDecrypt(self,e):
    	message = self.encrypted.GetValue().encode('ascii','ignore')
    	self.decrypted.SetValue(self.leb.decrypt(message))

    def setup_menu(self):
        filemenu = wx.Menu()
        helpmenu = wx.Menu()
        menuAbout = helpmenu.Append(wx.ID_ABOUT, "&About"," About this program")
        menuSetGear = filemenu.Append(wx.ID_ANY, "Set &Gear..."," Print")
        menuSetAlphabets = filemenu.Append(wx.ID_ANY, "Set &Alphabets..."," Set Alphabets...")
        menuPrint = filemenu.Append(wx.ID_PRINT, "&Print"," Set Alphabets")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Exit program")
        
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(helpmenu,"&Help")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.Print, menuPrint)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.SetGear, menuSetGear)
        self.Bind(wx.EVT_MENU, self.SetAlphabets, menuSetAlphabets)

    def SetGear(self, e):
    	ted = wx.TextEntryDialog(self, "Set Leibniz Gear:","Set Leibniz Gear",defaultValue = self.leb.get_file_contents('gear.txt'))
    	ted.ShowModal()
    	self.leb.set_gear(ted.GetValue())
    	self.leb.set_file_contents('gear.txt', ted.GetValue())
    	ted.Destroy()

    def SetAlphabets(self, e):
    	ted = wx.TextEntryDialog(self, "Set Alphabets (newline-delimited):", "Set Alphabets", defaultValue = self.leb.get_file_contents('cyphers.txt'),style=wx.TE_MULTILINE|wx.OK|wx.CANCEL)
    	ted.ShowModal()
    	self.leb.set_alphabets(ted.GetValue())
    	self.leb.set_file_contents('cyphers.txt', ted.GetValue())
    	ted.Destroy()

    def OnAbout(self,e):
        dlg = wx.MessageDialog( self, "An implementation of Leibniz' encryption scheme.", "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self,e):
        self.Close(True)


def main():
	app = wx.App(False)
	frame = MainWindow(None, "Leibniz Encryption")
	frame.Show(True)
	app.MainLoop()


if __name__ == "__main__":
	main()
