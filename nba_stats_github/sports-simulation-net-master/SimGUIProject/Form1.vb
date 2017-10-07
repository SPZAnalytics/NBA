Imports SportsSimulation.Player.Base

Public Class Form1

    Public Sub New()

        ' This call is required by the designer.
        InitializeComponent()

        ' Add any initialization after the InitializeComponent() call.
        Dim fn As String = "C:\Users\sansbacon\Documents\Visual Studio 2010\Projects\sportssimulation\trunk\SportsSimulationTestingProject\PlayerTests\BasePlayerTests\SamplePlayerStats.xml"
        Dim id As String = "ALLENRA01"
        Dim playerXML As New BasePlayerXML
        Dim player As BasePlayer = playerXML.LoadStatsFromXML(fn, id)
        Console.WriteLine("seasons: " & player.Seasons.Count.ToString)
        For Each ps As BasePlayerSeason In player.Seasons
            Console.WriteLine("year: " & ps.Year.ToString)
        Next
    End Sub
End Class
