import wx
import wx.html2
import wx.grid
import fetch
import Database.db

class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.db = Database.db.Db()
        self.db.insert(('The Joy Of Clojure',))

        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.webview = wx.html2.WebView.New(self,  size=(500,700))

        # data table
        self.table = wx.grid.Grid(self, size=(200,300))


        # A button
        self.button = wx.Button(self, label="Save")
        self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)

        # the edit control - one line version.
        self.lblname = wx.StaticText(self, label="Http Url:")
        grid.Add(self.lblname, pos=(1,0))
        self.editname = wx.TextCtrl(self, value="file:///Users/gon/projects/python-basecamp-course/js-page/index.html", size=(140,-1))
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
        mainSizer.Add(self.button, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)

    def OnClick(self, obj):
        rows = self.db.select_all()

        self.table.CreateGrid(len(rows), 3)

        self.table.SetColLabelValue(0, "First")
        self.table.SetColLabelValue(1, "Middle")
        self.table.SetColLabelValue(2, "Last")

        print self.webview.GetSelectedText()

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.SetCellValue(i, j, str(val))


    def OnClickLoad(self, event):
        print self.editname.Value
        self.webview.LoadURL(self.editname.Value)


app = wx.App(False)
frame = wx.Frame(None, title="Python Basecamp Course - Demo")

ep = ExamplePanel(frame)
frame.Show()
app.MainLoop()
