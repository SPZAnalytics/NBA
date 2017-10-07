'Option Strict On

'Imports NUnit.Framework
'Imports SportsSimulation.Player.Base

'<TestFixture()> _
'Public Class PlayerSeasonTests

'    Public Property PlayerSeason As BasePlayerSeason
'    Public Property pts1 As Dictionary(Of String, Object)
'    Public Property pts2 As Dictionary(Of String, Object)

'    <SetUp()> _
'    Public Sub SetUp()
'        Me.PlayerSeason = New BasePlayerSeason(2006)
'        pts1 = New Dictionary(Of String, Object) From {
'                    {"Minutes", 1100},
'                    {"Games", 40},
'                    {"Points", 1100},
'                    {"Rebounds", 400}
'                }
'        pts2 = New Dictionary(Of String, Object) From {
'                    {"Minutes", 1200},
'                    {"Games", 42},
'                    {"Points", 1100},
'                    {"Rebounds", 520}
'                }
'    End Sub
'    <TearDown()> _
'    Public Sub TearDown()
'        'nothing to go here
'    End Sub

'    <Test()> _
'    Public Sub New_ValidYear_ReturnsTrue()
'        Dim year As Integer = 2006
'        Assert.AreEqual(year, Me.PlayerSeason.Year, "years are not the same.")
'    End Sub

'    <Test()> _
'    Public Sub New_NoTeamSeasons_ReturnsTrue()
'        Assert.AreEqual(0, Me.PlayerSeason.NumberOfPlayerTeamSeasons, "number of playerteamseasons are not the same.")
'    End Sub

'    <Test()> _
'    Public Sub AddPlayerTeamSeason_ArrayContainsNewTeamSeason_ReturnsTrue()
'        Dim pts = New PlayerTeamSeason(Me.pts1)
'        Me.PlayerSeason.AddPlayerTeamSeason(pts)
'        Assert.Contains(pts, Me.PlayerSeason.PlayerTeamSeasons, "playerteamseason not successfully added")
'    End Sub

'    <Test()> _
'    Public Sub AddPlayerTeamSeasons_ArrayContainsNewTeamSeasons_ReturnsTrue()
'        Dim ptsList As New List(Of PlayerTeamSeason) From {
'            {New PlayerTeamSeason(Me.pts1)},
'            {New PlayerTeamSeason(Me.pts2)}
'        }
'        Me.PlayerSeason.AddPlayerTeamSeasons(ptsList)
'        Assert.AreEqual(2, Me.PlayerSeason.NumberOfPlayerTeamSeasons, "number of playerteamseasons are not the same.")
'    End Sub

'    <Test()> _
'    Public Sub GetSeasonTotal_ValidStat_ReturnsTrue()
'        Dim ptsList As New List(Of PlayerTeamSeason) From {
'            {New PlayerTeamSeason(Me.pts1)},
'            {New PlayerTeamSeason(Me.pts2)}
'        }
'        Me.PlayerSeason.AddPlayerTeamSeasons(ptsList)
'        Dim actualTotal As Integer = 2200
'        Dim total As Integer = CInt(Me.PlayerSeason.GetSeasonTotal("Points"))
'        Assert.AreEqual(actualTotal, total, "points do not match up")
'    End Sub

'    <Test()> _
'    Public Sub PerGame_ValidTotalAndGamesPlayed_ReturnsTrue()
'        Dim ptsList As New List(Of PlayerTeamSeason) From {
'            {New PlayerTeamSeason(Me.pts1)},
'            {New PlayerTeamSeason(Me.pts2)}
'        }
'        Me.PlayerSeason.AddPlayerTeamSeasons(ptsList)
'        Dim actualTotal As Integer = 2200
'        Dim actualGp As Integer = 82
'        Dim ppg As Double = actualTotal / actualGp
'        Dim total As Integer = CInt(Me.PlayerSeason.GetSeasonTotal("Points"))
'        Dim gp As Integer = CInt(Me.PlayerSeason.GetSeasonTotal("Games"))
'        Assert.AreEqual(ppg, Me.PlayerSeason.PerGame(total, gp), "ppg not equal")
'    End Sub

'    <Test()> _
'    Public Sub PerTimePeriod_ValidTotalAndMinutes_ReturnsTrue()
'        Dim ptsList As New List(Of PlayerTeamSeason) From {
'            {New PlayerTeamSeason(Me.pts1)},
'            {New PlayerTeamSeason(Me.pts2)}
'        }
'        Me.PlayerSeason.AddPlayerTeamSeasons(ptsList)
'        Dim actualTotal As Integer = 2200
'        Dim actualMin As Integer = 2300
'        Dim timeperiod As Integer = 40
'        Dim actualPp40 As Double = actualTotal / actualMin * timeperiod
'        Dim expectedTotal As Integer = CInt(Me.PlayerSeason.GetSeasonTotal("Points"))
'        Dim expectedMin As Integer = CInt(Me.PlayerSeason.GetSeasonTotal("Minutes"))
'        Assert.AreEqual(Me.PlayerSeason.PerTimePeriod(expectedTotal, expectedMin, 40), actualPp40, "pp40 not equal")
'    End Sub

'End Class