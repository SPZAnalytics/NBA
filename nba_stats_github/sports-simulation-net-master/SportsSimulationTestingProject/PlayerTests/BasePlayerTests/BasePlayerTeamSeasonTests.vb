Option Strict On

Imports NUnit.Framework
Imports SportsSimulation.Player.Base

<TestFixture()> _
Public Class BasePlayerTeamSeasonTests

    Public Property PlayerTeamSeason As BasePlayerTeamSeason
    Public Property Stats As Dictionary(Of String, Object)
    Public Property Year As Integer = 2006

    <SetUp()> _
    Public Sub SetUp()
        Me.Stats = New Dictionary(Of String, Object) From {
            {"Minutes", 2000},
            {"Games", 72},
            {"Points", 2100},
            {"Rebounds", 800}
        }
        Me.PlayerTeamSeason = (New BasePlayerTeamSeason(Me.Stats))
    End Sub
    <TearDown()> _
    Public Sub TearDown()
        'nothing to go here
    End Sub

    <Test()> _
    Public Sub New_NoParameters_ReturnsTrue()
        Dim pts As New BasePlayerTeamSeason
        Assert.NotNull(pts, "Variable is not instance of class")
    End Sub

    <Test()> _
    Public Sub New_YearParameter_ReturnsTrue()
        Dim pts As New BasePlayerTeamSeason(Me.Year)
        Assert.NotNull(pts, "Variable is not instance of class")
    End Sub

    <Test()> _
    Public Sub New_StatsParameter_ReturnsTrue()
        Dim pts As New BasePlayerTeamSeason(Me.Stats)
        Assert.NotNull(pts, "Variable is not instance of class")
    End Sub

    <Test()> _
    Public Sub New_YearAndStatsParameter_ReturnsTrue()
        Dim pts As New BasePlayerTeamSeason(Me.Year, Me.Stats)
        Assert.NotNull(pts, "Variable is not instance of class")
    End Sub

    <Test()> _
    Public Sub Year_GetValue_ReturnsTrue()
        Dim year As Integer = Me.Year
        Assert.AreEqual(year, Me.Year, "Years are not the same.")
    End Sub

    <Test()> _
    Public Sub Stats_GetValue_ReturnsTrue()
        Dim stats As Dictionary(Of String, Object) = Me.Stats
        Assert.AreSame(stats, Me.Stats, "Stats are not the same.")
    End Sub

    <Test()> _
    Public Sub AddStat_AddNewStat_ReturnsTrue()
        Dim StatName As String = "Assists"
        Dim Stat As New Dictionary(Of String, Object) From {{StatName, 250}}
        Me.PlayerTeamSeason.AddStat(Stat.Keys(0), Stat.Values(0))
        Assert.AreEqual(Me.PlayerTeamSeason.GetStat(StatName), Me.Stats(StatName), StatName & " not equal")
    End Sub

    <Test()> _
    Public Sub AddStats_AddNewStats_ReturnsTrue()
        Dim Stats As New Dictionary(Of String, Object) From {
            {"Assists", 250},
            {"Steals", 120}
        }
        Me.PlayerTeamSeason.AddStats(Stats)
        For Each key As String In Stats.Keys
            Assert.AreEqual(Me.PlayerTeamSeason.GetStat(key), Me.Stats(key), key & " not equal")
        Next
    End Sub

    <Test()> _
    Public Sub GetStat_GetMinutes_ReturnsTrue()
        Dim stat As String = "Minutes"
        Assert.AreEqual(Me.PlayerTeamSeason.GetStat(stat), Me.Stats(stat), stat & " not equal")
    End Sub

    <Test()> _
    Public Sub GetStat_GetGames_ReturnsTrue()
        Dim stat As String = "Games"
        Assert.AreEqual(Me.PlayerTeamSeason.GetStat(stat), Me.Stats(stat), stat & " not equal")
    End Sub

    <Test()> _
    Public Sub GetStat_GetPoints_ReturnsTrue()
        Dim stat As String = "Points"
        Assert.AreEqual(Me.PlayerTeamSeason.GetStat(stat), Me.Stats(stat), stat & " not equal")
    End Sub

    <Test()> _
    Public Sub GetStat_GetRebounds_ReturnsTrue()
        Dim stat As String = "Rebounds"
        Assert.AreEqual(Me.PlayerTeamSeason.GetStat(stat), Me.Stats(stat), stat & " not equal")
    End Sub
End Class