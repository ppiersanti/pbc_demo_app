import wx
import wx.html2
import wx.grid
import fetch
import Database.db
import os

class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.db = Database.db.Db()

        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.webview = wx.html2.WebView.New(self,  size=(340,390))

        # data table
        self.table = wx.grid.Grid(self, size=(340,385))
        self.table.CreateGrid(0, 3)
        self.table.SetColLabelValue(0, "Id")
        self.table.SetColLabelValue(1, "Content")
        self.table.SetColLabelValue(2, "Date")

        self.btnsavecanvas = wx.Button(self, label="Save Canvas")
        self.Bind(wx.EVT_BUTTON, self.OnClickSaveCanvas,self.btnsavecanvas)

        self.btnclearcanvas = wx.Button(self, label="Clear Canvas")
        self.Bind(wx.EVT_BUTTON, self.OnClickClearCanvas,self.btnclearcanvas)

        self.btnrestorecanvas = wx.Button(self, label="Restore Canvas")
        self.Bind(wx.EVT_BUTTON, self.OnClickRestoreCanvas, self.btnrestorecanvas)


        sz = wx.BoxSizer(wx.HORIZONTAL)

        self.lblname = wx.StaticText(self, label="Http Url:")
        self.editname = wx.TextCtrl(self, value=os.environ.get("APP_COURSE_URL", "Your Url Here"), size=(450,-1))

        self.button_load = wx.Button(self, label="Load", size=(80, -1))
        self.Bind(wx.EVT_BUTTON, self.OnClickLoad, self.button_load)

        sz.Add(self.lblname, 0)
        sz.Add(self.editname, 1, wx.EXPAND | wx.ALL)
        sz.Add(self.button_load, 2, wx.SHAPED | wx.ALL)
        mainSizer.Add(sz, 0, wx.TOP, 15)



        grid.Add(self.webview, pos=(1,0))
        grid.Add(self.table, pos=(1,1))

        hSizer.Add(grid, 0, wx.ALL, 5)


        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnsizer.Add(self.btnsavecanvas, 1)
        btnsizer.Add(self.btnclearcanvas, 1)
        btnsizer.Add(self.btnrestorecanvas, 1)

        mainSizer.Add(hSizer, 1, wx.ALL, 1)
        mainSizer.Add(btnsizer, 2, wx.ALL)

        self.SetSizerAndFit(mainSizer)


    def RefreshTable(self):
        rows = self.db.select_all()
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.SetCellValue(i, j, str(val))


    def OnClickLoad(self, event):
        print self.editname.Value
        self.webview.LoadURL(self.editname.Value)

    def OnClickSaveCanvas(self, event):
        self.webview.RunScript("document.getElementById('btn_export').click();")
        self.db.insert((self.webview.GetSelectedText(),))
        self.table.AppendRows()
        self.RefreshTable()

    def OnClickClearCanvas(self, event):
        self.webview.RunScript("document.getElementById('btn_clear').click();")

    def OnClickRestoreCanvas(self, event):
        content = self.db.last()[1]
        self.webview.RunScript("""\
        window.__canvas.clear();
        window.__canvas.loadFromJSON(%s);""" % content)








app = wx.App(False)
frame = wx.Frame(None, title="Python Basecamp Course - Demo", size=(720,530))

ep = ExamplePanel(frame)
frame.Show()
app.MainLoop()
