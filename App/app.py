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

        self.webview = wx.html2.WebView.New(self,  size=(350,450))

        # data table
        self.table = wx.grid.Grid(self, size=(200,300))

        self.btnsavecanvas = wx.Button(self, label="Save Canvas")
        self.Bind(wx.EVT_BUTTON, self.OnClickSaveCanvas,self.btnsavecanvas)

        self.btnclearcanvas = wx.Button(self, label="Clear Canvas")
        self.Bind(wx.EVT_BUTTON, self.OnClickClearCanvas,self.btnclearcanvas)

        self.btnrestorecanvas = wx.Button(self, label="Restore Canvas")
        self.Bind(wx.EVT_BUTTON, self.OnClickRestoreCanvas, self.btnrestorecanvas)

        # the edit control - one line version.
        self.lblname = wx.StaticText(self, label="Http Url:")
        grid.Add(self.lblname, pos=(1,0))
        self.editname = wx.TextCtrl(self, value=os.environ.get("APP_COURSE_URL", "Your Url Here"), size=(140,-1))
        grid.Add(self.editname, pos=(1,1))

        # A button
        self.button_load = wx.Button(self, label="Load")
        self.Bind(wx.EVT_BUTTON, self.OnClickLoad, self.button_load)
        grid.Add(self.button_load, pos=(1,2))

        # add a spacer to the sizer
        grid.Add((10, 40), pos=(2,0))

        grid.Add(self.table, pos=(3,0))

        hSizer.Add(grid, 0, wx.ALL, 5)
        hSizer.Add(self.webview)
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        mainSizer.Add(self.btnsavecanvas, 0, wx.CENTER)
        mainSizer.Add(self.btnclearcanvas, 0, wx.CENTER)
        mainSizer.Add(self.btnrestorecanvas, 0, wx.CENTER)


        self.SetSizerAndFit(mainSizer)

    def RefreshTable(self):
        rows = self.db.select_all()
        self.table.CreateGrid(len(rows), 3)
        self.table.SetColLabelValue(0, "Id")
        self.table.SetColLabelValue(1, "Content")
        self.table.SetColLabelValue(2, "Date")
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.SetCellValue(i, j, str(val))

    def OnClickLoad(self, event):
        print self.editname.Value
        self.webview.LoadURL(self.editname.Value)

    def OnClickSaveCanvas(self, event):
        self.webview.RunScript("document.getElementById('btn_export').click();")
        self.db.insert((self.webview.GetSelectedText(),))
        self.RefreshTable()

    def OnClickClearCanvas(self, event):
        self.webview.RunScript("document.getElementById('btn_clear').click();")

    def OnClickRestoreCanvas(self, event):
        content = self.db.last()[1]
        self.webview.RunScript("""\
        window.__canvas.clear();
        window.__canvas.loadFromJSON(%s);""" % content)








app = wx.App(False)
frame = wx.Frame(None, title="Python Basecamp Course - Demo", size=(600,800))

ep = ExamplePanel(frame)
frame.Show()
app.MainLoop()
